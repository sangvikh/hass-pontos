# FILE: __init__.py
import asyncio
import importlib
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady

from .services import register_services
from .device import register_device
from .const import DOMAIN, CONF_MAKE, MAKES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Access which 'make' the user selected in config_flow
    make = entry.data.get(CONF_MAKE, "pontos")  # default if missing
    module_name = MAKES.get(make, "const_pontos")  # fallback if needed
    
    # Dynamically import the device-specific constants module, e.g. const_pontos
    device_const = importlib.import_module(f".{module_name}", __package__)
    # For example, device_const.PLATFORMS might be ["sensor", "button", "valve", ...]

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    try:
        # Register the device
        await register_device(hass, entry)
    except Exception as e:
        _LOGGER.error(f"Error setting up device: {e}")
        raise ConfigEntryNotReady from e

    # Register services (services.py also uses dynamic import under the hood)
    await register_services(hass)

    # Forward entry setup to all platforms for this device
    platforms = getattr(device_const, "PLATFORMS", [])
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, platforms)
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Dynamically figure out which device_const file to unload from
    make = entry.data.get(CONF_MAKE, "pontos")
    module_name = MAKES.get(make, "const_pontos")
    device_const = importlib.import_module(f".{module_name}", __package__)

    # Unload each relevant platform
    platforms = getattr(device_const, "PLATFORMS", [])
    tasks = [
        hass.config_entries.async_forward_entry_unload(entry, platform)
        for platform in platforms
    ]
    
    results = await asyncio.gather(*tasks)
    unload_ok = all(results)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
