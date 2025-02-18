import logging
from homeassistant.components.select import SelectEntity
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import callback, Event

from .device import get_device_info
from .const import DOMAIN, CONF_MAKE, MAKES, CONF_IP_ADDRESS, MAKES

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the custom profile select entity."""
    # Get the device info
    device_info, _ = await get_device_info(hass, entry)

    # Instantiate the select entity, passing in the needed constants
    select_entity = PontosProfileSelect(hass, entry, device_info)
    async_add_entities([select_entity], True)


class PontosProfileSelect(SelectEntity):
    """Representation of a Select entity for setting profiles."""

    def __init__(self, hass, entry, device_info):
        """Initialize the profile select entity."""
        self._hass = hass
        self._entry = entry
        self._device_info = device_info

        # Get device-specific constants directly from the entry data
        make = self._entry.data.get(CONF_MAKE)
        device_const = MAKES[make]
        
        # Store the device-specific data
        self._profile_codes = device_const.PROFILE_CODES
        self._services = device_const.SERVICES

        # Build name/unique_id from device info
        self._attr_name = f"{device_info['name']} Profile"
        self._attr_unique_id = f"{device_info['serial_number']}_profile_select"
        self._sensor_unique_id = f"{device_info['serial_number']}_active_profile"

        # Build the list of valid profile options (skip "not defined")
        self._attr_options = [
            name if name else "Not Defined"
            for name in self._profile_codes.values()
            if name and name != "not defined"
        ]

        self._attr_current_option = None

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()

        # Get the entity ID of the sensor using the unique ID
        entity_registry = er.async_get(self._hass)
        sensor_entity_id = entity_registry.async_get_entity_id(
            "sensor",
            DOMAIN,
            self._sensor_unique_id
        )
        
        # Fetch the initial state from the sensor entity
        if sensor_entity_id:
            sensor_state = self._hass.states.get(sensor_entity_id)
            initial_state = sensor_state.state if sensor_state else None
            LOGGER.debug(f"Fetched initial profile state from sensor: {initial_state}")
            self._attr_current_option = initial_state
            self.async_write_ha_state()

            # Register a listener for state changes on that sensor
            LOGGER.debug(f"Registering state change listener for {sensor_entity_id}")
            async_track_state_change_event(
                self._hass,
                sensor_entity_id,
                self._sensor_state_changed
            )
        else:
            LOGGER.error(f"Sensor with unique ID {self._sensor_unique_id} not found")

    @callback
    def _sensor_state_changed(self, event: Event) -> None:
        """Handle active profile sensor state changes."""
        new_state = event.data.get("new_state")
        if new_state is not None:
            new_option = new_state.state
            if new_option != self._attr_current_option:
                LOGGER.debug(f"Profile state changed to: {new_option}")
                self.set_state(new_option)

    def set_state(self, state):
        """Set the current profile option and update Home Assistant."""
        self._attr_current_option = state
        self.async_write_ha_state()

    async def async_select_option(self, option: str):
        """Handle the user selecting an option."""
        LOGGER.info(f"Setting profile to {option}")
        profile_number = self._map_profile_name_to_number(option)

        # Call the set_profile service
        await self._hass.services.async_call(
            DOMAIN,
            "set_profile",
            service_data={
                "profile_number": profile_number,
                "ip_address": self._entry.data[CONF_IP_ADDRESS],
            },
        )

        self._attr_current_option = option
        self.async_write_ha_state()

    @property
    def device_info(self):
        """Link this entity to the device registry entry."""
        return {
            "identifiers": self._device_info["identifiers"],
        }
    
    @property
    def available(self):
        """Entity is unavailable if the last known profile is STATE_UNAVAILABLE."""
        return self._attr_current_option != STATE_UNAVAILABLE

    def _map_profile_name_to_number(self, profile_name):
        """Convert the profile's display name to the numeric code in the dictionary."""
        for code, name in self._profile_codes.items():
            if name == profile_name:
                return int(code)
        return None
