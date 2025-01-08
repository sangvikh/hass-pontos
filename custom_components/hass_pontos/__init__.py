from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
import asyncio
import logging
import importlib

from .services import register_services
from .device import register_device
from .const import DOMAIN, MAKES, CONF_MAKE

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    
    make = entry.data[CONF_MAKE]
    config_module = importlib.import_module(f".{MAKES[make]}", package=__name__)
    hass.data[DOMAIN][entry.entry_id] = {
        "entry": entry.data,
        "sensor_config": config_module.SENSOR_TYPES,
    }

    try:
        # Register the device
        await register_device(hass, entry)
    except Exception as e:
        LOGGER.error(f"Error setting up device: {e}")
        raise ConfigEntryNotReady from e

    # Register services
    await register_services(hass)

    for platform in config_module.PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
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