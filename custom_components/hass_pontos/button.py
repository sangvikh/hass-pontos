# custom_components/hass_pontos/button.py
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the button entity for the Pontos Base device."""
    async_add_entities([PontosClearAlarmsButton(hass, entry)], True)

class PontosClearAlarmsButton(ButtonEntity):
    """Button to clear alarms on the Pontos Base device."""

    def __init__(self, hass, entry):
        """Initialize the button."""
        self._hass = hass
        self._entry = entry
        self._attr_name = "Clear Alarms"
        self._attr_unique_id = f"{entry.entry_id}_clear_alarms"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "pontos_base")},
            "name": "Pontos Base",
            "manufacturer": "Hansgrohe",
        }

    async def async_press(self):
        """Handle the button press to clear alarms."""
        LOGGER.info("Clear Alarms button pressed")
        await self._hass.services.async_call(
            DOMAIN, 
            "clear_alarms",  # Assuming the service name for clearing alarms is "clear_alarms"
            service_data={"entry_id": self._entry.entry_id}
        )
