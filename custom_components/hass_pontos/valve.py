# custom_components/hass_pontos/valve.py
import logging
from homeassistant.components.valve import ValveEntity
from .device import get_device_info  # Import the get_device_info function
from .const import DOMAIN

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the dummy valve entity."""
    device_info, _ = await get_device_info(hass, entry)
    async_add_entities([DummyValve(entry, device_info)], True)

class DummyValve(ValveEntity):
    """A minimal implementation of a dummy valve entity."""

    def __init__(self, entry, device_info):
        """Initialize the dummy valve."""
        self._is_open = False  # Initial state: valve is closed
        self._attr_unique_id = f"{entry.entry_id}_dummy_valve"
        self._attr_name = "Dummy Valve"
        
        # This is crucial to avoid the error
        self._attr_reports_position = False

        # Link the entity to the pontos_base device
        self._attr_device_info = device_info

    @property
    def is_open(self) -> bool:
        """Return true if the valve is open."""
        return self._is_open

    async def async_open(self, **kwargs) -> None:
        """Open the valve."""
        self._is_open = True
        self.async_write_ha_state()

    async def async_close(self, **kwargs) -> None:
        """Close the valve."""
        self._is_open = False
        self.async_write_ha_state()

    async def async_update(self):
        """Update the valve's state. This could fetch data from an API in a real implementation."""
        # For a minimal example, we won't implement data fetching. The state is controlled by async_open and async_close.
        pass
