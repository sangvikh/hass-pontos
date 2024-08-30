from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
import logging

from .utils import fetch_data
from .device import get_device_info
from .const import CONF_IP_ADDRESS, SENSOR_DETAILS, FETCH_INTERVAL, URL_LIST

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    ip_address = entry.data[CONF_IP_ADDRESS]
    device_info, data = await get_device_info(hass, entry)

    # Instantiate and add sensors
    sensors = [PontosSensor(sensor_config, device_info) for key, sensor_config in SENSOR_DETAILS.items()]
    async_add_entities(sensors)

    # Update data so sensors is available immediately
    for sensor in sensors:
        sensor.set_state(sensor.parse_data(data))

    # Function to fetch new state and update all sensors
    async def update_state(_):
        state = await fetch_data(ip_address, URL_LIST)
        for sensor in sensors:
                sensor.set_state(sensor.parse_data(data))

    # Schedule updates using the fetch interval
    async_track_time_interval(hass, update_state, FETCH_INTERVAL)

class PontosSensor(SensorEntity):
    def __init__(self, sensor_config, device_info):
        self._state = None
        self._attr_name = f"{device_info['name']} {sensor_config['name']}"
        self._endpoint = sensor_config['endpoint']
        self._attr_native_unit_of_measurement = sensor_config.get('unit', None)
        self._attr_device_class = sensor_config.get('device_class', None)
        self._attr_state_class = sensor_config.get('state_class', None)
        self._format_dict = sensor_config.get('format_dict', None)
        self._code_dict = sensor_config.get('code_dict', None)
        self._scale = sensor_config.get('scale', None)
        self._attr_unique_id = f"{device_info['serial_number']}_{sensor_config['name']}"
        self._device_info = device_info

    def set_state(self, state):
        self._state = state
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
    def state(self):
        return self._state

    # Parsing sensor data
    def parse_data(self, data):
        """Process, format, and validate sensor data."""
        if data is None:
            return None
        _data = data.get(self._endpoint, None)

        # Apply format replacements if format_dict is present
        if self._format_dict is not None and _data is not None:
            for old, new in self._format_dict.items():
                _data = _data.replace(old, new)

        # Translate alarm codes if code_dict is present
        if self._code_dict is not None and _data is not None:
            _data = self._code_dict.get(_data, _data)

        # Scale sensor data if scale is present
        if self._scale is not None and _data is not None:
            try:
                _data = float(_data) * self._scale
            except (ValueError, TypeError):
                pass

        return _data