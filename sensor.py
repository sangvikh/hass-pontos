import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
import logging

from .const import *

LOGGER = logging.getLogger(__name__)

class PontosSensor(SensorEntity):
    def __init__(self, sensor_config):
        self._data = None
        self._attr_name = f"Pontos {sensor_config['name']}"
        self._endpoint = sensor_config['endpoint']
        self._attr_native_unit_of_measurement = sensor_config.get('unit', None)
        self._attr_device_class = sensor_config.get('device_class', None)
        self._attr_state_class = sensor_config.get('state_class', None)
        self._format_dict = sensor_config.get('format_dict', None)
        self._code_dict = sensor_config.get('code_dict', None)
        self._scale = sensor_config.get('scale', None)
        self._attr_unique_id = f"pontos_{sensor_config['name']}"
        self._device_id = None

    def set_data(self, data):
        self._data = data
        self.async_write_ha_state()

    def set_device_id(self, device_id):
        self._device_id = device_id

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def device_info(self):
        return {
            "identifiers": self._device_id,
        }

    @property   
    def state(self):
        return self._data

sensors = [PontosSensor(config) for key, config in SENSOR_DETAILS.items()]

# Fetching data
async def fetch_data(ip, url_list):
    urls = [url.format(ip=ip) for url in url_list]
    data = {}
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as response:
                if response.status == 200:
                    data.update(await response.json())
                else:
                    LOGGER.error(f"Failed to fetch data: HTTP {response.status}")
    return data

# Parsing sensor data
def parse_data(data, sensor):
    """Process, format, and validate sensor data."""
    if data is None:
        return None
    _data = data.get(sensor._endpoint, None)

    # Apply format replacements if format_dict is present
    if sensor._format_dict is not None and _data is not None:
        for old, new in sensor._format_dict.items():
            _data = _data.replace(old, new)

    # Translate alarm codes if code_dict is present
    if sensor._code_dict is not None and _data is not None:
        _data = sensor._code_dict.get(_data, _data)

    # Scale sensor data if scale is present
    if sensor._scale is not None and _data is not None:
        try:
            _data = float(_data) * sensor._scale
        except (ValueError, TypeError):
            pass

    return _data

async def async_setup_entry(hass, entry, async_add_entities):
    config = entry.data
    ip_address = config[CONF_IP_ADDRESS]
    device_registry = async_get_device_registry(hass)

    # Fetching all relevant data from the device
    data = await fetch_data(ip_address, [URL_ALL_DATA])  # Assuming URL_ALL_DATA points to the endpoint containing all necessary data

    # Assign data to variables
    mac_address = data.get("getMAC", "00:00:00:00:00:00:00:00")
    serial_number = data.get("getSRN", "")
    firmware_version = data.get("getVER", "")
    device_type = data.get("getTYP", "")

    # Create a device entry with fetched data
    device_info = {
        "identifiers": {(DOMAIN, "pontos_base")},
        "connections": {(CONNECTION_NETWORK_MAC, mac_address)},
        "name": "Pontos Base",
        "manufacturer": "Hansgrohe",
        "model": device_type,
        "sw_version": firmware_version,
        "serial_number": serial_number,
    }

    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        **device_info
    )

    # Assign device id to each sensor and add entities
    for sensor in sensors:
        sensor.set_device_id(device_info['identifiers'])
    async_add_entities(sensors)

    # Function to fetch new data and update all sensors
    async def update_data(_):
        data = await fetch_data(ip_address, URL_LIST)
        for sensor in sensors:
                sensor.set_data(parse_data(data, sensor))

    # Schedule updates using the fetch interval
    async_track_time_interval(hass, update_data, FETCH_INTERVAL)

    # Lastly update data to get fresh data immediately
    await update_data(None)