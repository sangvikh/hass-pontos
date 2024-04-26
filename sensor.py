#import asyncio
#from datetime import datetime, timedelta
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
import logging

from .const import DOMAIN, CONF_IP_ADDRESS, FETCH_INTERVAL, URL_LIST, ALARM_CODES, PROFILE_CODES, VALVE_CODES

LOGGER = logging.getLogger(__name__)

class PontosSensor(SensorEntity):
    def __init__(self, name, endpoint, unit, device_class, state_class = None, format_dict=None, code_dict=None, scale=None):
        self._data = None
        self._attr_name = f"Pontos {name}"
        self._endpoint = endpoint
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._format_dict = format_dict
        self._code_dict = code_dict
        self._scale = scale
        self._attr_unique_id = f"pontos_{name}"
        self._device_id = None

    def set_data(self, data):
        """Set the sensor data and perform any necessary processing."""
        self._data = data
        # You can add additional checks or processing here
        self.async_write_ha_state()

    def set_device_id(self, device_id):
        """Sets the device ID for the sensor."""
        self._device_id = device_id

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return self._attr_unique_id

    @property
    def device_info(self):
        return {
            "identifiers": self._device_id,
        }

    @property   
    def state(self):
        return self._data

sensors = [
        PontosSensor("Total consumption in liters", "getVOL", "L", "water", "total_increasing", format_dict={"Vol[L]": ""}),
        PontosSensor("Water pressure", "getBAR", "mbar", "pressure", format_dict={"mbar": ""}),
        PontosSensor("Water temperature", "getCEL", "°C", "temperature", scale=0.1),
        PontosSensor("Time in seconds since turbine received no pulse", "getNPS", "s", None),
        PontosSensor("Volume of current water consumption in ml", "getAVO", "mL", "water", format_dict={"mL": ""}),
        PontosSensor("Configured Micro Leakage test pressure drop in bar", "getDBD", "bar", "pressure"),
        PontosSensor("Wifi connection state", "getWFS", None, None),
        PontosSensor("Wifi signal strength (RSSI)", "getWFR", "dB", "signal_strength", scale=-1),
        PontosSensor("Battery voltage", "getBAT", "V", "voltage", format_dict={",": "."}),
        PontosSensor("Mains voltage", "getNET", "V", "voltage", format_dict={",": "."}),
        PontosSensor("Serial number", "getSRN", None, None),
        PontosSensor("Firmware version", "getVER", None, None),
        PontosSensor("Type", "getTYP", None, None),
        PontosSensor("MAC Address", "getMAC", None, None),
        PontosSensor("Alarm", "getALA", None, None, code_dict=ALARM_CODES),
        PontosSensor("Active profile", "getPRF", None, None, code_dict=PROFILE_CODES),
        PontosSensor("Valve status", "getVLV", None, None, code_dict=VALVE_CODES),
        PontosSensor("Water conductivity", "getCND", "µS/cm", None),
        PontosSensor("Water hardness", "getCND", "dH", None, scale=1/30)
    ]

async def async_setup_entry(hass, entry, async_add_entities):
    config = entry.data
    ip_address = config[CONF_IP_ADDRESS]
    device_registry = async_get_device_registry(hass)
    
    # Create a device entry
    device_info = {
        "identifiers": {(DOMAIN, "pontos_base")},
        "name": "Pontos Base",
        "manufacturer": "Hansgrohe",
        "model": "Pontos Base",
        "sw_version": "",
    }

    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        **device_info
    )

    # Assign device id to each sensor and add entities
    for sensor in sensors:
        sensor.set_device_id(device_info['identifiers'])
    async_add_entities(sensors)

    # Fetching data
    async def fetch_data(ip):
        urls = [url.format(ip=ip) for url in URL_LIST]
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

    # Function to fetch new data and update all sensors
    async def update_data(_):
        data = await fetch_data(ip_address)
        for sensor in sensors:
                sensor.set_data(parse_data(data, sensor))

    # Schedule updates using the fetch interval
    async_track_time_interval(hass, update_data, FETCH_INTERVAL)