import asyncio
from datetime import datetime, timedelta
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import VOLUME_LITERS
from . import DOMAIN

FETCH_INTERVAL = timedelta(seconds=60)  # Set fetch interval to 60 seconds

class PontosSensor(SensorEntity):
    _last_fetch = None
    _data = None
    _lock = asyncio.Lock()

    def __init__(self, session, ip, name, endpoint, unit, device_class, format_dict=None, code_dict=None, scale=None):
        self._session = session
        self._ip = ip
        self._attr_name = name
        self._endpoint = endpoint
        self._attr_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._format_dict = format_dict
        self._code_dict = code_dict
        self._scale = scale

    async def async_update(self):
        async with PontosSensor._lock:
            if not PontosSensor._data or not PontosSensor._last_fetch or (datetime.now() - PontosSensor._last_fetch) > FETCH_INTERVAL:
                async with self._session.get(f"http://{self._ip}:5333/pontos-base/get/all") as response:
                    if response.status == 200:
                        PontosSensor._data = await response.json()
                        PontosSensor._last_fetch = datetime.now()
                    else:
                        _LOGGER.error(f"Failed to fetch data: HTTP {response.status}")

    @property
    def state(self):
        raw_value = PontosSensor._data.get(self._endpoint) if PontosSensor._data else None

        # Apply format replacements if format_dict is present
        if self._format_dict and isinstance(raw_value, str):
            for old, new in self._format_dict.items():
                raw_value = raw_value.replace(old, new)

        # Translate alarm codes if code_dict is present
        if self._code_dict and raw_value is not None:
            translated_value = self._code_dict.get(raw_value)
            if translated_value is not None:
                return translated_value

        # Scale sensor data if scale is present
        if self._scale is not None and raw_value is not None:
            try:
                value = float(raw_value) * self._scale
                return value
            except ValueError:
                return raw_value
        
        return raw_value
    

async def async_setup_entry(hass, entry, async_add_entities):
    config = entry.data
    ip_address = config['ip_address']
    session = aiohttp.ClientSession()
    async_add_entities([
        PontosSensor(session, ip_address, "Total consumption in liters", "getVOL", VOLUME_LITERS, "water", format_dict={"Vol[L]": ""}),
        PontosSensor(session, ip_address, "Water pressure", "getBAR", "mbar", "pressure", format_dict={"mbar": ""}),
        PontosSensor(session, ip_address, "Water temperature", "getCEL", "°C", "temperature", scale=0.1),
        PontosSensor(session, ip_address, "Time in seconds since turbine received no pulse", "getNPS", "s", None),
        PontosSensor(session, ip_address, "Volume of current water consumption in ml", "getAVO", "mL", "water", format_dict={"mL": ""}),
        PontosSensor(session, ip_address, "Configured Micro Leakage Test, pressure drop in bar", "getDBD", "bar", "pressure"),
        PontosSensor(session, ip_address, "Wifi connection state", "getWFS", None, None),
        PontosSensor(session, ip_address, "Wifi signal strength (RSSI)", "getWFR", "dB", "signal_strength", scale=-1),
        PontosSensor(session, ip_address, "Battery voltage", "getBAT", "V", "voltage", format_dict={",": "."}),
        PontosSensor(session, ip_address, "Mains voltage", "getNET", "V", "voltage", format_dict={",": "."}),
        PontosSensor(session, ip_address, "Serial number", "getSRN", None, None),
        PontosSensor(session, ip_address, "Firmware version", "getVER", None, None),
        PontosSensor(session, ip_address, "Type", "getTYP", None, None),
        PontosSensor(session, ip_address, "MAC Address", "getMAC", None, None),
        PontosSensor(session, ip_address, "Alarm", "getALA", None, None, code_dict=alarm_codes),
        PontosSensor(session, ip_address, "Active profile", "getPRF", None, None, code_dict=profile_codes),
        PontosSensor(session, ip_address, "Valve status", "getVLV", None, None, code_dict=valve_codes)
    ])

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