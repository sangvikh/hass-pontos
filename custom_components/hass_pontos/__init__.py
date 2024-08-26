from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .services import register_services

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Register entities
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ['sensor', 'button', 'valve'])
    )

    # Register services
    await register_services(hass)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, 'sensor')
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
