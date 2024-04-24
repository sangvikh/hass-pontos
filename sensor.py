import asyncio
from datetime import datetime, timedelta
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
import logging

from . import DOMAIN

LOGGER = logging.getLogger(__name__)
FETCH_INTERVAL = timedelta(seconds=60)  # Set fetch interval to 60 seconds

class PontosSensor(SensorEntity):
    def __init__(self, data, name, endpoint, unit, device_class, format_dict=None, code_dict=None, scale=None):
        self._data = data
        self._attr_name = f"Pontos {name}"
        self._endpoint = endpoint
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._format_dict = format_dict
        self._code_dict = code_dict
        self._scale = scale
        self._attr_unique_id = f"pontos_{name}"

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return self._attr_unique_id

    async def async_update(self):
        pass

    @property   
    def state(self):
        if self._data is not None:
            raw_value = self._data.get(self._endpoint, None)
        else:
            return None

        # Apply format replacements if format_dict is present
        if self._format_dict is not None and raw_value is not None:
            for old, new in self._format_dict.items():
                raw_value = raw_value.replace(old, new)

        # Translate alarm codes if code_dict is present
        if self._code_dict is not None and raw_value is not None:
            raw_value = self._code_dict.get(raw_value, raw_value)  # Use original raw_value if no translation found

        # Scale sensor data if scale is present
        if self._scale is not None and raw_value is not None:
            try:
                value = float(raw_value) * self._scale
                return value
            except ValueError:
                pass  # If conversion fails, proceed to return raw_value without scaling

        return raw_value


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


async def async_setup_entry(hass, entry, async_add_entities):
    config = entry.data
    ip_address = config['ip_address']
    data = await fetch_data(ip_address)

    sensors = [
            PontosSensor(data['all'], "Total consumption in liters", "getVOL", "L", "water", format_dict={"Vol[L]": ""}),
            PontosSensor(data['all'], "Water pressure", "getBAR", "mbar", "pressure", format_dict={"mbar": ""}),
            PontosSensor(data['all'], "Water temperature", "getCEL", "°C", "temperature", scale=0.1),
            PontosSensor(data['all'], "Time in seconds since turbine received no pulse", "getNPS", "s", None),
            PontosSensor(data['all'], "Volume of current water consumption in ml", "getAVO", "mL", "water", format_dict={"mL": ""}),
            PontosSensor(data['all'], "Configured Micro Leakage test pressure drop in bar", "getDBD", "bar", "pressure"),
            PontosSensor(data['all'], "Wifi connection state", "getWFS", None, None),
            PontosSensor(data['all'], "Wifi signal strength (RSSI)", "getWFR", "dB", "signal_strength", scale=-1),
            PontosSensor(data['all'], "Battery voltage", "getBAT", "V", "voltage", format_dict={",": "."}),
            PontosSensor(data['all'], "Mains voltage", "getNET", "V", "voltage", format_dict={",": "."}),
            PontosSensor(data['all'], "Serial number", "getSRN", None, None),
            PontosSensor(data['all'], "Firmware version", "getVER", None, None),
            PontosSensor(data['all'], "Type", "getTYP", None, None),
            PontosSensor(data['all'], "MAC Address", "getMAC", None, None),
            PontosSensor(data['all'], "Alarm", "getALA", None, None, code_dict=alarm_codes),
            PontosSensor(data['all'], "Active profile", "getPRF", None, None, code_dict=profile_codes),
            PontosSensor(data['all'], "Valve status", "getVLV", None, None, code_dict=valve_codes),
            PontosSensor(data['cnd'], "Water conductivity", "getCND", "µS/cm", None),
            PontosSensor(data['cnd'], "Water hardness", "getCND", "dH", None, scale=1/30)
        ]

    async_add_entities(sensors)

    # Function to fetch new data and update all sensors
    async def update_data(_):
        new_data = await fetch_data(ip_address)
        for sensor in sensors:
            if sensor._endpoint in ["getCND"]:
                sensor._data = new_data['cnd']
            else:
                sensor._data = new_data['all']
            await sensor.async_update()
            await sensor.async_update_ha_state()

    # Schedule updates using the fetch interval
    async_track_time_interval(hass, update_data, FETCH_INTERVAL)


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