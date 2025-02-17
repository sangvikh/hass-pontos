import asyncio
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
    make = entry.data.get(CONF_MAKE, "pontos")
    device_const = MAKES[make]

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
    device_const = MAKES[make]

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

async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry data to new format/version."""
    if config_entry.version == 1:
        new_data = dict(config_entry.data)

        # Ensure 'make' is set
        if CONF_MAKE not in new_data:
            new_data[CONF_MAKE] = "pontos"

        # Update the entry by passing version=2
        hass.config_entries.async_update_entry(
            config_entry,
            data=new_data,
            version=2,
        )

        _LOGGER.info(
            "Migrated config entry '%s' from version 1 to 2",
            config_entry.entry_id
        )

    # Return True if migration was successful (or if no migration needed)
    return True