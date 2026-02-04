import logging
from homeassistant.components.select import SelectEntity
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_call_later, async_track_state_change_event
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import callback, Event
from homeassistant.util import slugify

from .const import DOMAIN, CONF_IP_ADDRESS

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the custom profile select entity."""
    device_info = hass.data[DOMAIN]["entries"][entry.entry_id]["device_info"]

    # Instantiate the select entity
    select_entity = PontosProfileSelect(hass, entry, device_info)
    async_add_entities([select_entity], True)


class PontosProfileSelect(SelectEntity):
    """
    A SelectEntity that:
      - Reads numeric codes (1..8) from the "active_profile" sensor.
      - Looks up user-friendly names from profile_name_x sensors.
      - Calls set_profile with the numeric code when a user picks a name.
    """

    def __init__(self, hass, entry, device_info):
        """Initialize the Pontos profile select entity."""
        self._hass = hass
        self._entry = entry
        self._device_info = device_info

        # Construct entity metadata
        serial_number = device_info["serial_number"]
        self._attr_translation_key = "profile_select"
        self._attr_has_entity_name = True
        self._attr_unique_id = slugify(f"{serial_number}_profile_select")

        # The sensor that holds the numeric active profile code
        self._active_profile_sensor_unique_id = slugify(
            f"{serial_number}_active_profile"
        )

        # Track which entity_id corresponds to each profile code's name sensor
        self._profile_name_entity_ids = {}

        # Start with an empty dropdown and no selected option
        self._attr_options = []
        self._attr_current_option = None

    async def async_added_to_hass(self):
        """When entity is added, set up registry lookups and listeners."""
        await super().async_added_to_hass()
        entity_registry = er.async_get(self._hass)

        # 1) Locate the "active_profile" numeric sensor
        active_sensor_id = entity_registry.async_get_entity_id(
            "sensor", DOMAIN, self._active_profile_sensor_unique_id
        )
        LOGGER.debug(
            f"Active profile sensor unique id: {self._active_profile_sensor_unique_id}"
        )
        LOGGER.debug(f"Active profile sensor name: {active_sensor_id}")

        if active_sensor_id:
            # Fetch its initial state
            sensor_state_obj = self._hass.states.get(active_sensor_id)
            initial_code_str = sensor_state_obj.state if sensor_state_obj else None
            LOGGER.debug(
                f"Fetched initial profile state from sensor: {initial_code_str}"
            )

            # Convert code -> name
            self._attr_current_option = self._code_to_name(initial_code_str)
            self.async_write_ha_state()

            # Listen for future changes
            LOGGER.debug(f"Registering state change listener for {active_sensor_id}")
            async_track_state_change_event(
                self._hass, active_sensor_id, self._active_profile_changed
            )
        else:
            LOGGER.error(
                f"Sensor with unique ID {self._active_profile_sensor_unique_id} not found"
            )

        # 2) For each code 1..8, see if we have a name sensor
        for code in range(1, 9):
            profile_sensor_uid = slugify(
                f"{self._device_info['serial_number']}_profile_{code}_name"
            )
            profile_sensor_entity_id = entity_registry.async_get_entity_id(
                "sensor", DOMAIN, profile_sensor_uid
            )
            if profile_sensor_entity_id:
                self._profile_name_entity_ids[code] = profile_sensor_entity_id
                LOGGER.debug(
                    f"Found dynamic name sensor for code {code}: {profile_sensor_entity_id}"
                )
                async_track_state_change_event(
                    self._hass, profile_sensor_entity_id, self._profile_name_changed
                )

        # Build the dropdown from current sensor states
        self._rebuild_options()
        self.async_write_ha_state()

        # After 2s, re-check in case no sensor state_changed was triggered
        async_call_later(self._hass, 2.0, self._delayed_recheck)

    @callback
    def _delayed_recheck(self, _):
        """
        Called ~2s after startup to ensure name sensors are populated
        and we can match numeric code => text label.
        """
        LOGGER.debug("Running delayed startup re-check for profile select.")
        self._rebuild_options()
        self.async_write_ha_state()

        # Re-check the active_profile sensor in case it wasn't ready earlier
        entity_registry = er.async_get(self._hass)
        active_sensor_id = entity_registry.async_get_entity_id(
            "sensor", DOMAIN, self._active_profile_sensor_unique_id
        )
        if active_sensor_id:
            state_obj = self._hass.states.get(active_sensor_id)
            if state_obj:
                code_str = state_obj.state
                new_name = self._code_to_name(code_str)
                if new_name != self._attr_current_option:
                    LOGGER.debug(f"Delayed check: code {code_str} => {new_name}")
                    self.set_state(new_name)

    @callback
    def _active_profile_changed(self, event: Event):
        """When the numeric code for active_profile changes, update the label in the UI."""
        new_state_obj = event.data.get("new_state")
        if not new_state_obj:
            return

        code_str = new_state_obj.state
        new_name = self._code_to_name(code_str)
        if new_name != self._attr_current_option:
            LOGGER.debug(
                f"Active profile code changed => {code_str} => label '{new_name}'"
            )
            self.set_state(new_name)

    def set_state(self, new_label: str):
        """Set the currently selected label in the UI."""
        self._attr_current_option = new_label
        self.async_write_ha_state()

    @callback
    def _profile_name_changed(self, event: Event):
        """When a user renames a profile or the sensor updates, rebuild the dropdown."""
        self._rebuild_options()
        self.async_write_ha_state()

        # Also re-check the numeric code in case we can now map it to a label
        entity_registry = er.async_get(self._hass)
        active_sensor_id = entity_registry.async_get_entity_id(
            "sensor", DOMAIN, self._active_profile_sensor_unique_id
        )
        if active_sensor_id:
            state_obj = self._hass.states.get(active_sensor_id)
            if state_obj:
                code_str = state_obj.state
                new_name = self._code_to_name(code_str)
                if new_name != self._attr_current_option:
                    LOGGER.debug(
                        f"After name sensor updated, code {code_str} => {new_name}"
                    )
                    self.set_state(new_name)

    def _rebuild_options(self):
        """
        Rebuild the dropdown from each profile_name_x sensor's current state,
        skipping empties/unavailable.
        """
        new_options = []
        for code, name_entity_id in self._profile_name_entity_ids.items():
            state_obj = self._hass.states.get(name_entity_id)
            if state_obj and state_obj.state not in (
                "unknown",
                "unavailable",
                STATE_UNAVAILABLE,
                "",
                None,
            ):
                label = state_obj.state.strip()
                if label:
                    new_options.append(label)

        self._attr_options = new_options
        LOGGER.debug(f"Rebuilt profile options => {new_options}")

        # If the current option is no longer valid, clear it out
        if self._attr_current_option and self._attr_current_option not in new_options:
            LOGGER.debug(
                f"Current option '{self._attr_current_option}' not in new_options => clearing."
            )
            self._attr_current_option = None

    async def async_select_option(self, option: str):
        """
        When a user picks an option (e.g. "Kitchen"), find its numeric code
        and call set_profile.
        """
        LOGGER.info(f"User selected '{option}'")
        profile_number = self._name_to_code(option)
        if profile_number is None:
            LOGGER.warning(f"No code found for dynamic name: '{option}'")
            return

        LOGGER.debug(f"Mapping '{option}' => code {profile_number}")
        await self._hass.services.async_call(
            DOMAIN,
            "set_profile",
            {
                "data": profile_number,
                "ip_address": self._entry.options[CONF_IP_ADDRESS],
            },
        )
        self.set_state(option)

    def _name_to_code(self, label: str):
        """Return the profile code for the given label by scanning name sensors."""
        for code, name_entity_id in self._profile_name_entity_ids.items():
            state_obj = self._hass.states.get(name_entity_id)
            if state_obj and state_obj.state == label:
                return code
        return None

    def _code_to_name(self, code_str: str):
        """
        Convert a numeric code string (e.g. "2") to the text from sensor.my_device_profile_2_name.
        Returns None if there's no match or the sensor is empty/unavailable.
        """
        if not code_str:
            return None
        try:
            code = int(code_str)
        except ValueError:
            return None

        name_entity_id = self._profile_name_entity_ids.get(code)
        if not name_entity_id:
            return None

        state_obj = self._hass.states.get(name_entity_id)
        if state_obj and state_obj.state not in (
            "unknown",
            "unavailable",
            STATE_UNAVAILABLE,
            "",
            None,
        ):
            return state_obj.state.strip()

        return None

    @property
    def device_info(self):
        """Link this select entity to the device registry entry."""
        return {"identifiers": self._device_info["identifiers"]}

    @property
    def available(self):
        """Entity is unavailable if the current option is STATE_UNAVAILABLE."""
        return self._attr_current_option != None
