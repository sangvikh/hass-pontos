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

    def __init__(self, ip, name, endpoint, unit, device_class):
        self._ip = ip
        self._attr_name = name
        self._endpoint = endpoint
        self._attr_unit_of_measurement = unit
        self._attr_device_class = device_class

    async def async_update(self):
        if not self._data or not self._last_fetch or (datetime.now() - self._last_fetch) > FETCH_INTERVAL:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{self._ip}:5333/pontos-base/get/all") as response:
                    if response.status == 200:
                        PontosSensor._data = await response.json()
                        PontosSensor._last_fetch = datetime.now()
                    else:
                        raise Exception(f"Failed to fetch data: HTTP {response.status}")
    
    @property
    def state(self):
        return self._data.get(self._endpoint) if self._data else None

async def async_setup_entry(hass, entry, async_add_entities):
    config = entry.data
    ip_address = config['ip_address']
    async_add_entities([
        PontosSensor(ip_address, "Total consumption in liters", "getVOL", VOLUME_LITERS, "water"),
        PontosSensor(ip_address, "Water pressure", "getBAR", "mbar", "pressure"),
        PontosSensor(ip_address, "Water temperature", "getCEL", "°C", "temperature"),
        PontosSensor(ip_address, "Time in seconds since turbine received no pulse", "getNPS", "s", None),
        PontosSensor(ip_address, "Volume of current water consumption in ml", "getAVO", "mL", "water"),
        PontosSensor(ip_address, "Configured Micro Leakage Test, pressure drop in bar", "getDBD", "bar", "pressure"),
        PontosSensor(ip_address, "Wifi connection state", "getWFS", None, None),
        PontosSensor(ip_address, "Wifi signal strength (RSSI)", "getWFR", "dB", "signal_strength"),
        PontosSensor(ip_address, "Battery voltage", "getBAT", "V", "voltage"),
        PontosSensor(ip_address, "Mains voltage", "getNET", "V", "voltage"),
        PontosSensor(ip_address, "Serial number", "getSRN", None, None),
        PontosSensor(ip_address, "Firmware version", "getVER", None, None),
        PontosSensor(ip_address, "Type", "getTYP", None, None),
        PontosSensor(ip_address, "Code number", "getCNO", None, None),
        PontosSensor(ip_address, "MAC Address", "getMAC", None, None),
        PontosSensor(ip_address, "Alarm", "getALA", None, None),
        PontosSensor(ip_address, "Active profile", "getPRF", None, None),
        PontosSensor(ip_address, "Valve status", "getVLV", None, None)
    ])
