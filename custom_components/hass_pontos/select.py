import logging
from homeassistant.components.select import SelectEntity
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.core import callback, Event
from .device import get_device_info
from .const import DOMAIN, PROFILE_CODES

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the custom profile select entity."""
    device_info, data = await get_device_info(hass, entry)
    select_entity = PontosProfileSelect(hass, entry, device_info)
    async_add_entities([select_entity], True)

class PontosProfileSelect(SelectEntity):
    """Representation of a Select entity for setting profiles."""

    def __init__(self, hass, entry, device_info):
        """Initialize the profile select entity."""
        self._hass = hass
        self._entry = entry
        self._attr_name = f"{device_info['name']} Profile"
        self._attr_unique_id = f"{device_info['serial_number']}_profile_select"
        self._sensor_unique_id = f"{device_info['serial_number']}_active_profile"
        self._attr_options = [
            name if name else "Not Defined"
            for name in PROFILE_CODES.values()
            if name and name != "not defined"
        ]
        self._attr_current_option = None
        self._device_info = device_info

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()

        # Get the entity ID of the sensor using the unique ID
        entity_registry = er.async_get(self.hass)
        sensor_entity_id = entity_registry.async_get_entity_id("sensor", DOMAIN, self._sensor_unique_id)
        
        # Fetch the initial state from the sensor entity
        if sensor_entity_id:
            sensor_state = self.hass.states.get(sensor_entity_id)
            initial_state = sensor_state.state if sensor_state else None
            LOGGER.debug(f"Fetched initial profile state from sensor: {initial_state}")
            self._attr_current_option = initial_state
            self.async_write_ha_state()

            # Register state change listener
            LOGGER.debug(f"Registering state change listener for {sensor_entity_id}")
            async_track_state_change_event(
                self.hass,
                sensor_entity_id,
                self._sensor_state_changed
            )
        else:
            LOGGER.error(f"Sensor with unique ID {self._sensor_unique_id} not found")

    @callback
    def _sensor_state_changed(self, event: Event) -> None:
        """Handle active profile sensor state changes."""
        new_state = event.data.get('new_state')
        if new_state is not None:
            new_option = new_state.state
            if new_option != self._attr_current_option:
                LOGGER.debug(f"Profile state changed to: {new_option}")
                self.set_state(new_option)

    def set_state(self, state):
        """Set the valve state and update Home Assistant."""
        self._attr_current_option = state
        self.async_write_ha_state()

    async def async_select_option(self, option: str):
        """Handle the user selecting an option."""
        LOGGER.info(f"Setting profile to {option}")
        profile_number = self.map_profile_name_to_number(option)
        await self._hass.services.async_call(
            DOMAIN, 
            "set_profile",
            service_data={"profile_number": profile_number, "ip_address": self._entry.data["ip_address"]}
        )
        self._attr_current_option = option
        self.async_write_ha_state()

    @property
    def device_info(self):
        """Return device info to link this entity with the device."""
        return {
            "identifiers": self._device_info['identifiers'],
        }

    def map_profile_name_to_number(self, profile_name):
        """Map profile name to profile number."""
        for number, name in PROFILE_CODES.items():
            if name == profile_name:
                return int(number)
        return None
