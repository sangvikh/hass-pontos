import logging
from datetime import datetime, time as dtime

from homeassistant.components.time import TimeEntity
from homeassistant.util import slugify
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers import entity_registry as er
from homeassistant.const import STATE_UNAVAILABLE

from .const import DOMAIN, CONF_MAKE, CONF_IP_ADDRESS, MAKES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up time entry entities from config."""
    make = entry.data.get(CONF_MAKE)
    device_const = MAKES[make]
    TIME_ENTRIES = device_const.TIME_ENTRIES

    device_info = hass.data[DOMAIN]["entries"][entry.entry_id]["device_info"]
    entities = []

    for key, config in TIME_ENTRIES.items():
        entities.append(PontosTimeEntry(hass, entry, device_info, key, config))

    async_add_entities(entities, True)


class PontosTimeEntry(TimeEntity):
    """Represents a device time value that mirrors a sensor and calls a service on change."""

    def __init__(self, hass, entry, device_info, key, config):
        self._hass = hass
        self._entry = entry
        self._device_info = device_info
        self._key = key
        self._config = config
        self._sensor = config.get("sensor")
        self._service = config.get("service")
        self._attr_translation_key = key
        self._attr_has_entity_name = True
        self._attr_entity_category = config.get("entity_category", None)
        self._attr_unique_id = slugify(f"{device_info['serial_number']}_{key}_time")
        self._attr_native_value = None
        self._available = True
        self._sensor_unique_id = (
            slugify(f"{device_info['serial_number']}_{self._sensor}")
            if self._sensor
            else None
        )
        self._sensor_entity_id = None

    async def async_added_to_hass(self):
        registry = er.async_get(self._hass)
        if not self._sensor_unique_id:
            _LOGGER.warning("No sensor configured for time entry %s", self._key)
            self._available = False
            self.async_write_ha_state()
            return

        self._sensor_entity_id = registry.async_get_entity_id(
            "sensor", DOMAIN, self._sensor_unique_id
        )

        if self._sensor_entity_id:
            state = self._hass.states.get(self._sensor_entity_id)
            if state:
                self._available = state.state != STATE_UNAVAILABLE
                if self._available:
                    self._update_current_time(state.state)

            async_track_state_change_event(
                self._hass, self._sensor_entity_id, self._sensor_state_changed
            )
        else:
            _LOGGER.warning(
                f"Sensor for %s not found: %s", self._key, self._sensor_unique_id
            )
            self._available = False

        self.async_write_ha_state()

    @callback
    def _sensor_state_changed(self, event):
        new_state = event.data.get("new_state")
        if new_state is not None:
            self._available = new_state.state != STATE_UNAVAILABLE
            if self._available:
                self._update_current_time(new_state.state)
            self.async_write_ha_state()

    def _update_current_time(self, state_value):
        """Parse sensor state into a time object and update native value."""
        if state_value is None:
            return

        # If sensor returns number or formatted string, try to coerce to HH:MM or HH:MM:SS
        value = str(state_value).strip()

        # Accept empty/invalid values as unavailable
        if not value or "ERROR" in value.upper():
            _LOGGER.debug(
                "Time entry %s received invalid sensor value: %s", self._key, value
            )
            return

        parsed = None
        for fmt in ("%H:%M", "%H:%M:%S"):
            try:
                parsed_dt = datetime.strptime(value, fmt)
                parsed = parsed_dt.time()
                break
            except ValueError:
                continue

        if parsed is None:
            # Try to parse as HHMM or HMM
            try:
                if value.isdigit() and (3 <= len(value) <= 4):
                    if len(value) == 3:
                        h = int(value[0])
                        m = int(value[1:])
                    else:
                        h = int(value[:2])
                        m = int(value[2:])
                    parsed = dtime(hour=h, minute=m)
            except Exception:
                parsed = None

        if parsed:
            if parsed != self._attr_native_value:
                _LOGGER.debug("%s updated to %s", self._key, parsed.isoformat())
                self._attr_native_value = parsed
                self.async_write_ha_state()
        else:
            _LOGGER.warning(
                "%s state value '%s' could not be parsed as time", self._key, value
            )

    async def async_set_value(self, value):
        """Handle user setting a new time value.

        Value will typically be a datetime.time instance.
        """
        # Accept datetime.time or string
        if isinstance(value, dtime):
            time_str = value.strftime("%H:%M")
            native = value
        else:
            # try to coerce string
            time_str = str(value)
            try:
                native = datetime.strptime(time_str, "%H:%M").time()
            except Exception:
                try:
                    native = datetime.strptime(time_str, "%H:%M:%S").time()
                except Exception:
                    _LOGGER.error("Invalid time provided for %s: %s", self._key, value)
                    return

        _LOGGER.info("Time set for %s → %s", self._key, time_str)
        await self._hass.services.async_call(
            DOMAIN,
            self._service,
            {
                "ip_address": self._entry.options[CONF_IP_ADDRESS],
                "data": time_str,
            },
        )

        self._attr_native_value = native
        self.async_write_ha_state()

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def device_info(self):
        return {
            "identifiers": self._device_info["identifiers"],
        }

    @property
    def available(self):
        return self._available
