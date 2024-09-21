from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import asyncio

from .services import register_services
from .device import register_device
from .const import DOMAIN

platforms = ['sensor', 'button', 'valve', 'select']

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Register the device
    await register_device(hass, entry)

    # Register services
    await register_services(hass)

    # Register entities for each platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, platforms)
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Unload each platform
    tasks = [
        hass.config_entries.async_forward_entry_unload(entry, platform)
        for platform in platforms
    ]
    
    # Wait for all tasks to complete and gather results
    results = await asyncio.gather(*tasks)

    # Ensure all platforms unloaded successfully
    unload_ok = all(results)

    # Remove data related to this entry if everything is unloaded successfully
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok