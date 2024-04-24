import asyncio
from datetime import datetime, timedelta
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
import logging

from . import DOMAIN

LOGGER = logging.getLogger(__name__)
FETCH_INTERVAL = timedelta(seconds=10)  # Set fetch interval to 60 seconds

class PontosSensor(SensorEntity):
    def __init__(self, name, endpoint, unit, device_class, format_dict=None, code_dict=None, scale=None):
        self._data = None
        self._attr_name = f"Pontos {name}"
        self._endpoint = endpoint
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._format_dict = format_dict
        self._code_dict = code_dict
        self._scale = scale
        self._attr_unique_id = f"pontos_{name}"

    def set_data(self, data):
        """Set the sensor data and perform any necessary processing."""
        self._data = data
        # You can add additional checks or processing here
        self.async_write_ha_state()

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return self._attr_unique_id

    async def async_update(self):
        pass

    @property   
    def state(self):
        return self._data

alarm_codes = {
    "FF": "no alarm",
    "A1": "ALARM END SWITCH",
    "A2": "ALARM: Turbine blocked!",
    "A3": "ALARM: Leakage volume reached!",
    "A4": "ALARM: Leakage time reached!",
    "A5": "ALARM: Maximum flow rate reached!",
    "A6": "ALARM: Microleakage detected!",
    "A7": "ALARM EXT. SENSOR LEAKAGE RADIO",
    "A8": "ALARM EXT. SENSOR LEAKAGE CABLE",
    "A9": "ALARM: Pressure sensor faulty!",
    "AA": "ALARM: Temperature sensor faulty!",
    "AB": "ALARM: Weak battery!",
    "AE": "Error: no information available"
}

profile_codes = {
    "1": "Present",
    "2": "Absent",
    "3": "Vacation",
    "4": "Increased consumption",
    "5": "Maximum consumption",
    "6": "not defined",
    "7": "not defined",
    "8": "not defined"
}

valve_codes = {
    "10": "Closed",
    "11": "Closing",
    "20": "Open",
    "21": "Opening"
}

sensors = [
        PontosSensor("Total consumption in liters", "getVOL", "L", "water", format_dict={"Vol[L]": ""}),
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
        PontosSensor("Alarm", "getALA", None, None, code_dict=alarm_codes),
        PontosSensor("Active profile", "getPRF", None, None, code_dict=profile_codes),
        PontosSensor("Valve status", "getVLV", None, None, code_dict=valve_codes),
        PontosSensor("Water conductivity", "getCND", "µS/cm", None),
        PontosSensor("Water hardness", "getCND", "dH", None, scale=1/30)
    ]

async def async_setup_entry(hass, entry, async_add_entities):
    config = entry.data
    ip_address = config['ip_address']

    async_add_entities(sensors)

    # Fetching data
    async def fetch_data(ip):
        urls = {
            "cnd": f"http://{ip}:5333/pontos-base/get/cnd",
            "all": f"http://{ip}:5333/pontos-base/get/all"
        }
        data = {}
        async with aiohttp.ClientSession() as session:
            for key, url in urls.items():
                async with session.get(url) as response:
                    if response.status == 200:
                        data[key] = await response.json()
                    else:
                        LOGGER.error(f"Failed to fetch {key} data: HTTP {response.status}")
        return data

    # Parsing sensor data
    def parse_data(data, sensor):
        """Process, format, and validate sensor data."""
        if data is not None:
            _data = data.get(sensor._endpoint, None)
        else:
            return None

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
                return float(_data) * sensor._scale
            except (ValueError, TypeError):
                return _data
        else:
            return _data

    # Function to fetch new data and update all sensors
    async def update_data(_):
        new_data = await fetch_data(ip_address)
        for sensor in sensors:
            if sensor._endpoint in ["getCND"]:
                sensor.set_data(parse_data(new_data['cnd'], sensor))
            else:
                sensor.set_data(parse_data(new_data['all'], sensor))

    # Schedule updates using the fetch interval
    async_track_time_interval(hass, update_data, FETCH_INTERVAL)