import asyncio
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady

from .services import register_services
from .device import register_device
from .coordinator import PontosDataUpdateCoordinator
from .const import DOMAIN, CONF_IP_ADDRESS, CONF_FETCH_INTERVAL, CONF_MAKE, MAKES

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Access which 'make' the user selected in config_flow
    make = entry.data.get(CONF_MAKE)
    device_const = MAKES[make]

    # Set up the coordinator for data fetching
    coordinator = PontosDataUpdateCoordinator(hass, entry, device_const)
    await coordinator.async_config_entry_first_refresh()

    # Store entries in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault("entries", {})[entry.entry_id] = {
        "entry": entry,
        "coordinator": coordinator,
        "device_info": None,  # to be set after register_device()
    }

    try:
        # Register the device
        await register_device(hass, entry, coordinator)
    except Exception as e:
        LOGGER.error(f"Error setting up device: {e}")
        raise ConfigEntryNotReady from e

    # Register services
    await register_services(hass)

    # Forward entry setup to all platforms for this device
    platforms = getattr(device_const, "PLATFORMS", [])
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, platforms)
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Dynamically figure out which device_const file to unload from
    make = entry.data.get(CONF_MAKE)
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
        hass.data[DOMAIN]["entries"].pop(entry.entry_id, None)
    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle config entry reload (triggered by options flow changes)."""
    await async_unload_entry(hass, entry)
    return await async_setup_entry(hass, entry)

async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry data to new format/version."""
    if config_entry.version < 2:
        new_data = dict(config_entry.data)

        # Ensure 'make' is set
        if CONF_MAKE not in new_data:
            new_data[CONF_MAKE] = "Hansgrohe Pontos"

        # Update the entry by passing version=2
        hass.config_entries.async_update_entry(
            config_entry,
            data=new_data,
            version=2,
        )

        LOGGER.info(
            "Migrated config entry '%s' from version 1 to 2",
            config_entry.entry_id
        )

    if config_entry.version < 3:
        new_data = dict(config_entry.data)

        # Ensure 'fetch_interval' is set in options
        if CONF_FETCH_INTERVAL not in new_data:
            new_data[CONF_FETCH_INTERVAL] = 10  # Default to 10 seconds

        # Update the entry to version 3
        hass.config_entries.async_update_entry(
            config_entry,
            data=new_data,
            version=3,
        )

        LOGGER.info(
            "Migrated config entry '%s' from version 2 to 3",
            config_entry.entry_id
        )

    if config_entry.version < 4:
        # Copy existing data and options
        old_data = dict(config_entry.data)
        old_options = dict(config_entry.options)

        # Move relevant values from data to options if they exist
        if CONF_FETCH_INTERVAL in old_data:
            old_options.setdefault(CONF_FETCH_INTERVAL, old_data.pop(CONF_FETCH_INTERVAL))
        if CONF_IP_ADDRESS in old_data:
            old_options.setdefault(CONF_IP_ADDRESS, old_data.pop(CONF_IP_ADDRESS))

        hass.config_entries.async_update_entry(
            config_entry,
            data=old_data,
            options=old_options,
            version=4,
        )

        LOGGER.info(
            "Migrated config entry '%s' from version 3 to 4",
            config_entry.entry_id
        )

    # Return True if migration was successful (or if no migration needed)
    return True