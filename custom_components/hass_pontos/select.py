import logging
from homeassistant.components.select import SelectEntity
from homeassistant.core import callback
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
        self._attr_options = [name for name in PROFILE_CODES.values() if name != "not defined"]
        self._attr_current_option = None
        self._device_info = device_info

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()
        # Retrieve the current profile from the device and set it as the current option
        current_profile = await self.get_current_profile()
        self._attr_current_option = self.map_profile_number_to_name(current_profile)
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

    async def get_current_profile(self):
        """Fetch the current profile from the device."""
        # Add your logic here to fetch the current profile from the device
        return 1  # Example return value

    def map_profile_number_to_name(self, profile_number):
        """Map profile number to profile name."""
        return PROFILE_CODES.get(str(profile_number), "Unknown")

    def map_profile_name_to_number(self, profile_name):
        """Map profile name to profile number."""
        for number, name in PROFILE_CODES.items():
            if name == profile_name:
                return int(number)
        return None
