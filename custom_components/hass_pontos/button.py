# custom_components/hass_pontos/button.py
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.util import slugify
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers import entity_registry as er
from homeassistant.const import STATE_UNAVAILABLE

from .const import DOMAIN
from .device import get_device_info

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    # Fetch device info
    device_info, _ = await get_device_info(hass, entry)

    # Instantiate button
    reset_button = PontosClearAlarmsButton(hass, entry, device_info)
    
    # Add entities
    async_add_entities([reset_button], True)

class PontosClearAlarmsButton(ButtonEntity):
    """Button to clear alarms on the Pontos Base device."""

    def __init__(self, hass, entry, device_info):
        """Initialize the button."""
        self._hass = hass
        self._entry = entry
        self._attr_name = f"{device_info['name']} Clear alarms"
        self._attr_unique_id = slugify(f"{device_info['serial_number']}_clear_alarms")
        self._device_info = device_info
        self._availability_sensor_unique_id = slugify(f"{device_info['serial_number']}_alarm_status")
        self._available = True

    async def async_press(self):
        """Handle the button press to clear alarms."""
        LOGGER.info("Clear Alarms button pressed")
        await self._hass.services.async_call(
            DOMAIN, 
            "clear_alarms",  # Assuming the service name for clearing alarms is "clear_alarms"
            service_data={"entry_id": self._entry.entry_id}
        )

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()

        # Get the entity ID of the alarm sensor using the unique ID
        entity_registry = er.async_get(self._hass)
        sensor_entity_id = entity_registry.async_get_entity_id("sensor", DOMAIN, self._availability_sensor_unique_id)
        
        if sensor_entity_id:
            # Fetch the initial availability from the alarm sensor entity
            sensor_state = self._hass.states.get(sensor_entity_id)
            self._available = sensor_state.state != STATE_UNAVAILABLE if sensor_state else False
            LOGGER.debug(f"Fetched initial alarm state availability: {self._available}")
            self.async_write_ha_state()

            # Register state change listener
            LOGGER.debug(f"Registering state change listener for {sensor_entity_id}")
            async_track_state_change_event(
                self._hass,
                sensor_entity_id,
                self._sensor_state_changed
            )
        else:
            LOGGER.error(f"Alarm sensor with unique ID {self._alarm_availability_sensor_unique_id} not found")
            self._available = False
            self.async_write_ha_state()

    @callback
    def _sensor_state_changed(self, event):
        new_state = event.data.get('new_state')
        self._available = new_state.state != STATE_UNAVAILABLE
        if new_state is not None:
            self.async_write_ha_state()

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def device_info(self):
        return {
            "identifiers": self._device_info['identifiers'],
        }

    @property
    def available(self):
        return self._available