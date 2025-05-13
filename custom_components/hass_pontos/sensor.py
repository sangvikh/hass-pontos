from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import slugify
from datetime import timedelta
import asyncio
import logging

from .utils import fetch_data
from .device import get_device_info
from .const import CONF_FETCH_INTERVAL, CONF_MAKE, CONF_IP_ADDRESS, MAKES

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors for the selected device."""
    # Dynamically import the constants module for this device
    make = entry.data.get(CONF_MAKE)
    device_const = MAKES[make]

    # Now we can access e.g. device_const.SENSOR_DETAILS
    SENSOR_DETAILS = device_const.SENSOR_DETAILS
    URL_LIST = device_const.URL_LIST

    ip_address = entry.options[CONF_IP_ADDRESS]
    fetch_interval = timedelta(seconds=entry.options[CONF_FETCH_INTERVAL])
    device_info, data = await get_device_info(hass, entry)

    # Instantiate and add sensors
    sensors = [PontosSensor(key, sensor_config, device_info) for key, sensor_config in SENSOR_DETAILS.items()]
    async_add_entities(sensors)

    # Update data so sensors is available immediately
    for sensor in sensors:
        sensor.parse_data(data)

    # Store the current fetch_interval and the unsubscribe function
    current_fetch_interval = fetch_interval
    unsubscribe_interval = None

    # Lock to prevent concurrent updates
    update_lock = asyncio.Lock()

    # Function to fetch new data and update all sensors
    async def update_data(_):
        if update_lock.locked():
            LOGGER.debug("Update already in progress, skipping this interval.")
            return
        async with update_lock:
            nonlocal current_fetch_interval, unsubscribe_interval

            # Check if fetch_interval has changed
            new_fetch_interval = timedelta(seconds=entry.options[CONF_FETCH_INTERVAL])
            if new_fetch_interval != current_fetch_interval:
                current_fetch_interval = new_fetch_interval

                # Cancel previous interval
                if unsubscribe_interval:
                    unsubscribe_interval()

                # Schedule a new interval
                unsubscribe_interval = async_track_time_interval(hass, update_data, current_fetch_interval)
                entry.async_on_unload(unsubscribe_interval)

            try:
                # Fetch sensor data
                data = await fetch_data(
                    hass,
                    ip_address,
                    URL_LIST,
                    max_attempts=3,
                    retry_delay=entry.options[CONF_FETCH_INTERVAL]
                )

                # Parse sensor data
                for sensor in sensors:
                    sensor.parse_data(data)
            except Exception as e:
                LOGGER.warning(f"Error fetching data: {e}")

    # Initial scheduling of the update
    unsubscribe_interval = async_track_time_interval(hass, update_data, fetch_interval)
    entry.async_on_unload(unsubscribe_interval)

    return True


class PontosSensor(SensorEntity):
    def __init__(self, key, sensor_config, device_info):
        self._data = None
        self._attr_translation_key = key
        self._attr_has_entity_name = True
        self._endpoint = sensor_config['endpoint']
        self._attr_native_unit_of_measurement = sensor_config.get('unit', None)
        self._attr_device_class = sensor_config.get('device_class', None)
        self._attr_entity_category = sensor_config.get("entity_category", None)
        self._attr_state_class = sensor_config.get('state_class', None)
        self._format_dict = sensor_config.get('format_dict', None)
        self._code_dict = sensor_config.get('code_dict', None)
        self._scale = sensor_config.get('scale', None)
        self._attr_unique_id = slugify(f"{device_info['serial_number']}_{sensor_config['name']}")
        self._device_info = device_info

    def set_data(self, data):
        self._data = data
        self.async_write_ha_state()

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def device_info(self):
        return {
            "identifiers": self._device_info['identifiers'],
        }

    @property
    def native_value(self):
        return self._data

    @property
    def available(self):
        return self._data is not None

    # Parsing and updating sensor data
    def parse_data(self, data):
        """Process, format, and validate sensor data."""
        _data = data.get(self._endpoint, None)

        # If data is None, set to None and return
        if _data is None:
            self.set_data(None)
            return

        # Convert to string for more consistent manipulation later
        _data = str(_data)

        # If the device returns some known error string (e.g., "ERROR: ADM"), mark sensor unavailable
        if "ERROR" in _data.upper():
            self.set_data(None)
            return

        # Apply format replacements if format_dict is present
        if self._format_dict is not None and _data is not None:
            for old, new in self._format_dict.items():
                _data = _data.replace(old, new)

        # Translate alarm codes if code_dict is present
        if self._code_dict is not None and _data is not None:
            _data = self._code_dict.get(_data.upper(), _data)

        # Scale sensor data if scale is present
        if self._scale is not None and _data is not None:
            try:
                _data = round(float(_data) * self._scale, 2)
            except (ValueError, TypeError):
                pass

        # Update sensor data
        self.set_data(_data)
