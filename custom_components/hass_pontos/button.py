# custom_components/hass_pontos/button.py
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import Entity
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
        self._attr_name = f"{device_info['name']} Clear Alarms"
        self._attr_unique_id = f"{device_info['serial_number']}_clear_alarms"
        self._attr_device_id = device_info['identifiers']

    async def async_press(self):
        """Handle the button press to clear alarms."""
        LOGGER.info("Clear Alarms button pressed")
        await self._hass.services.async_call(
            DOMAIN, 
            "clear_alarms",  # Assuming the service name for clearing alarms is "clear_alarms"
            service_data={"entry_id": self._entry.entry_id}
        )

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def device_info(self):
        return {
            "identifiers": self._attr_device_id,
        }