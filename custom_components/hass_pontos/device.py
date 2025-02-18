# FILE: device.py
import logging
import time

from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

from .const import DOMAIN, CONF_IP_ADDRESS, CONF_DEVICE_NAME, CONF_MAKE, MAKES
from .utils import fetch_data

LOGGER = logging.getLogger(__name__)

_device_cache = {}

async def get_device_info(hass, entry):
    entry_id = entry.entry_id
    ip_address = entry.data[CONF_IP_ADDRESS]
    device_name = entry.data[CONF_DEVICE_NAME]
    make = entry.data.get(CONF_MAKE)
    device_const = MAKES[make]

    # Use the device_const.URL_LIST to fetch data
    if entry_id in _device_cache:
        cache_entry = _device_cache[entry_id]
        cache_age = time.time() - cache_entry['timestamp']
        if cache_age < device_const.FETCH_INTERVAL.total_seconds():
            LOGGER.debug(f"Using cached data for device {entry_id}")
            return cache_entry['device_info'], cache_entry['data']
        else:
            LOGGER.debug(f"Cache expired for device {entry_id}")

    LOGGER.debug(f"Fetching data for device {entry_id} from the device")

    data = await fetch_data(hass, ip_address, device_const.URL_LIST)
    if not data:
        LOGGER.error(f"Failed to fetch data from the device at {ip_address}")
        raise Exception("Failed to fetch data from the device")

    mac_address = data.get(device_const.SENSOR_DETAILS.get("mac_address", {}).get("endpoint"), "00:00:00:00:00:00")
    serial_number = data.get(device_const.SENSOR_DETAILS.get("serial_number", {}).get("endpoint"), "")
    firmware_version = data.get(device_const.SENSOR_DETAILS.get("firmware_version", {}).get("endpoint"), "")

    if not mac_address or not serial_number:
        LOGGER.error("Invalid MAC address or serial number")
        raise Exception("Invalid device data")

    device_info = {
        "identifiers": {(DOMAIN, make)},
        "connections": {(CONNECTION_NETWORK_MAC, mac_address)},
        "name": device_name,
        "manufacturer": device_const.MANUFACTURER,
        "model": device_const.MODEL,
        "sw_version": firmware_version,
        "serial_number": serial_number,
    }

    # Cache the device info and data
    _device_cache[entry_id] = {
        'device_info': device_info,
        'data': data,
        'timestamp': time.time()
    }

    return device_info, data

async def register_device(hass, entry):
    entry_id = entry.entry_id

    # Get device info (will raise exception if it fails)
    device_info, _ = await get_device_info(hass, entry)

    # Register device in the device registry
    device_registry = async_get_device_registry(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry_id,
        **device_info
    )