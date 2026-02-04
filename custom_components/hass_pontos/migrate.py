import logging
from .const import CONF_MAKE, CONF_FETCH_INTERVAL, CONF_IP_ADDRESS

LOGGER = logging.getLogger(__name__)


async def migrate_entry(hass, config_entry) -> bool:
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
            "Migrated config entry '%s' from version 1 to 2", config_entry.entry_id
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
            "Migrated config entry '%s' from version 2 to 3", config_entry.entry_id
        )

    if config_entry.version < 4:
        # Copy existing data and options
        old_data = dict(config_entry.data)
        old_options = dict(config_entry.options)

        # Move relevant values from data to options if they exist
        if CONF_FETCH_INTERVAL in old_data:
            old_options.setdefault(
                CONF_FETCH_INTERVAL, old_data.pop(CONF_FETCH_INTERVAL)
            )
        if CONF_IP_ADDRESS in old_data:
            old_options.setdefault(CONF_IP_ADDRESS, old_data.pop(CONF_IP_ADDRESS))

        hass.config_entries.async_update_entry(
            config_entry,
            data=old_data,
            options=old_options,
            version=4,
        )

        LOGGER.info(
            "Migrated config entry '%s' from version 3 to 4", config_entry.entry_id
        )

    # Return True if migration was successful (or if no migration needed)
    return True
