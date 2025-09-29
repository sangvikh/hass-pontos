import logging
from .const import CONF_MAKE, CONF_FETCH_INTERVAL, CONF_IP_ADDRESS
from .const import CONF_MAKE, CONF_FETCH_INTERVAL, CONF_IP_ADDRESS, MAKES, DOMAIN
from homeassistant.helpers import entity_registry as er, device_registry as dr
from homeassistant.util import slugify

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

    if config_entry.version < 5:
        # Migrate legacy sensor unique_ids that used explicit 'name' to new unique_ids using the sensor key.
        # Legacy unique_id: slugify(f"{serial}_{sensor_config['name']}")
        # New unique_id:    slugify(f"{serial}_{key}")
        try:
            make = config_entry.data.get(CONF_MAKE)
            if not make or make not in MAKES:
                LOGGER.debug("No valid 'make' in config entry; skipping entity unique_id migration")
            else:
                device_const = MAKES[make]
                SENSOR_DETAILS = getattr(device_const, "SENSOR_DETAILS", {})

                ent_reg = er.async_get(hass)
                dev_reg = dr.async_get(hass)
                devices = dr.async_entries_for_config_entry(dev_reg, config_entry.entry_id)

                for device in devices:
                    # device.identifiers is an iterable of tuples (domain, identifier)
                    for identifier in device.identifiers:
                        # take the identifier value (second element) as the serial/unique device id
                        serial = identifier[1] if isinstance(identifier, (list, tuple)) and len(identifier) >= 2 else None
                        if not serial:
                            continue

                        for key, sensor_config in SENSOR_DETAILS.items():
                            legacy_name = sensor_config.get("name")
                            if not legacy_name:
                                continue

                            old_unique = slugify(f"{serial}_{legacy_name}")
                            new_unique = slugify(f"{serial}_{key}")

                            # find the registry entry for the old unique_id belonging to this config_entry
                            old_entry = next(
                                (e for e in ent_reg.entities.values()
                                 if e.config_entry_id == config_entry.entry_id
                                 and e.domain == "sensor"
                                 and e.unique_id == old_unique),
                                None
                            )

                            if not old_entry:
                                continue

                            # ensure no conflict with an existing entity using the new unique_id
                            conflict = next((e for e in ent_reg.entities.values() if e.unique_id == new_unique), None)

                            if not conflict:
                                LOGGER.info("Updating entity %s unique_id %s -> %s", old_entry.entity_id, old_unique, new_unique)
                                ent_reg.async_update_entity(old_entry.entity_id, new_unique_id=new_unique)
                            else:
                                # If a target entity already exists with the new unique_id, remove the legacy entry
                                LOGGER.info("Removing legacy entity %s with unique_id %s because %s already exists", old_entry.entity_id, old_unique, conflict.entity_id)
                                ent_reg.async_remove(old_entry.entity_id)

                # finally bump the version
                hass.config_entries.async_update_entry(config_entry, version=5)
                LOGGER.info("Migrated config entry '%s' to version 5 (sensor unique_id migration)", config_entry.entry_id)
        except Exception as exc:
            LOGGER.exception("Failed migrating entity unique_ids for config entry %s: %s", config_entry.entry_id, exc)

    # Return True if migration was successful (or if no migration needed)
    return True