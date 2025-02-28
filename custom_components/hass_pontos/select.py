import logging
from homeassistant.components.select import SelectEntity
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import callback, Event

from .device import get_device_info
from .const import DOMAIN, CONF_MAKE, MAKES, CONF_IP_ADDRESS

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the custom profile select entity."""
    device_info, _ = await get_device_info(hass, entry)
    entity = PontosProfileSelect(hass, entry, device_info)
    async_add_entities([entity], True)


class PontosProfileSelect(SelectEntity):
    """
    A select entity that:
      - Reads numeric code (1..8) from the "active_profile" sensor
      - Looks up the name from "profile_name_x" sensors
      - The user picks one of those names to set the code with the set_profile service.
    """

    def __init__(self, hass, entry, device_info):
        self._hass = hass
        self._entry = entry
        self._device_info = device_info

        # We don't need a fallback dict at all
        make = entry.data.get(CONF_MAKE)
        device_const = MAKES[make]
        self._services = device_const.SERVICES

        # Basic entity info
        serial = device_info["serial_number"]
        self._attr_name = f"{device_info['name']} Profile"
        self._attr_unique_id = f"{serial}_profile_select"

        # The sensor that holds the numeric code for active profile
        self._active_profile_sensor_unique_id = f"{serial}_active_profile"

        # Keep track of the sensor entity_id for each code
        # e.g. {1: "sensor.my_device_profile_1_name", 2: ...}
        self._profile_name_entity_ids = {}

        # Start with empty options and no current selection
        self._attr_options = []
        self._attr_current_option = None

    async def async_added_to_hass(self):
        """Once we are added, find sensors in the entity registry and set up listeners."""
        await super().async_added_to_hass()
        entity_registry = er.async_get(self._hass)

        # 1) Listen for the numeric "active_profile" sensor
        active_eid = entity_registry.async_get_entity_id(
            "sensor", DOMAIN, self._active_profile_sensor_unique_id
        )
        if active_eid:
            # Set initial value from that sensor
            state_obj = self._hass.states.get(active_eid)
            if state_obj:
                self._attr_current_option = self._code_to_name(state_obj.state)
            # Watch future changes
            async_track_state_change_event(self._hass, active_eid, self._active_profile_changed)
        else:
            LOGGER.error(f"Could not find active_profile sensor {self._active_profile_sensor_unique_id}")

        # 2) For codes 1..8, see if we have a profile_name sensor
        for code in range(1, 9):
            profile_uid = f"{self._device_info['serial_number']}_profile_{code}_name"
            eid = entity_registry.async_get_entity_id("sensor", DOMAIN, profile_uid)
            if eid:
                self._profile_name_entity_ids[code] = eid
                # Watch changes on that sensor
                async_track_state_change_event(self._hass, eid, self._profile_name_changed)

        # Build the dropdown
        self._rebuild_options()
        self.async_write_ha_state()

    @callback
    def _active_profile_changed(self, event: Event):
        """When the numeric code for active_profile changes, set the new label in the UI."""
        new_state = event.data.get("new_state")
        if not new_state:
            return

        code_str = new_state.state
        new_name = self._code_to_name(code_str)  # e.g. "Kitchen" if code_str == "2"
        if new_name != self._attr_current_option:
            LOGGER.debug(f"Active profile code changed => {code_str} => label '{new_name}'")
            self._attr_current_option = new_name
            self.async_write_ha_state()

    @callback
    def _profile_name_changed(self, event: Event):
        """When a name sensor changes, rebuild the dropdown in case it changed or got empty."""
        self._rebuild_options()
        self.async_write_ha_state()

    def _rebuild_options(self):
        """
        Collect the text from each profile_name_x sensor,
        skipping empties/unavailable. That's our entire dropdown.
        """
        new_opts = []
        for code, eid in self._profile_name_entity_ids.items():
            st = self._hass.states.get(eid)
            if st and st.state not in ("unknown", "unavailable", STATE_UNAVAILABLE, "", None):
                name = st.state.strip()
                if name:
                    new_opts.append(name)
        self._attr_options = new_opts
        LOGGER.debug(f"Rebuilt profile select options => {new_opts}")

        # If the currently active code was set, let's ensure we are also showing that name
        # in the UI, in case it changed or got removed.
        if self._attr_current_option and self._attr_current_option not in new_opts:
            LOGGER.debug(f"Current option '{self._attr_current_option}' not in new_opts => clearing.")
            self._attr_current_option = None

    async def async_select_option(self, option: str):
        """
        When user picks "Kitchen," find which code that name belongs to,
        then call set_profile with that numeric code.
        """
        code = self._name_to_code(option)
        if code is None:
            LOGGER.warning(f"No code found for dynamic name: {option}")
            return

        LOGGER.info(f"User selected {option} => code {code}")
        await self._hass.services.async_call(
            DOMAIN,
            "set_profile",
            {
                "profile_number": code,
                "ip_address": self._entry.data[CONF_IP_ADDRESS],
            },
        )

        self._attr_current_option = option
        self.async_write_ha_state()

    def _name_to_code(self, name: str):
        """Look for which profile_name_x sensor has the given state, return that code."""
        for code, eid in self._profile_name_entity_ids.items():
            st = self._hass.states.get(eid)
            if st and st.state == name:
                return code
        return None

    def _code_to_name(self, code_str: str):
        """
        The 'active_profile' sensor might say "2", we want the text from sensor.my_device_profile_2_name.
        If there's no match or it's empty, returns None.
        """
        try:
            code = int(code_str)
        except ValueError:
            return None

        eid = self._profile_name_entity_ids.get(code)
        if not eid:
            return None

        st = self._hass.states.get(eid)
        if st and st.state not in ("unknown", "unavailable", STATE_UNAVAILABLE, "", None):
            return st.state.strip()

        return None

    @property
    def device_info(self):
        return {"identifiers": self._device_info["identifiers"]}

    @property
    def available(self):
        return self._attr_current_option != STATE_UNAVAILABLE
