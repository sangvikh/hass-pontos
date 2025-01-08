import logging
import time
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
import importlib

from .const import DOMAIN, MAKES, CONF_IP_ADDRESS, CONF_DEVICE_NAME, CONF_MAKE, FETCH_INTERVAL
from .utils import fetch_data

LOGGER = logging.getLogger(__name__)

# Cache to store device data
_device_cache = {}

async def get_device_info(hass, entry):
    entry_id = entry.entry_id
    ip_address = entry.data[CONF_IP_ADDRESS]
    device_name = entry.data[CONF_DEVICE_NAME]
    make = entry.data[CONF_MAKE]
    config_module = importlib.import_module(f".{MAKES[make]}", package=__name__)

    # Check if the data is already cached and not expired
    if entry_id in _device_cache:
        cache_entry = _device_cache[entry_id]
        cache_age = time.time() - cache_entry['timestamp']
        if cache_age < FETCH_INTERVAL.total_seconds():
            LOGGER.debug(f"Using cached data for device {entry_id} (age: {cache_age} seconds)")
            return cache_entry['device_info'], cache_entry['data']
        else:
            LOGGER.debug(f"Cache expired for device {entry_id} (age: {cache_age} seconds)")

    LOGGER.debug(f"Fetching data for device {entry_id} from the device")

    # Fetch data from the device
    data = await fetch_data(ip_address, config_module.URL_LIST)

    # Assign data to variables using the relevant sensor configuration
    mac_address = data.get(config_module.SENSOR_DETAILS['mac_address']['endpoint'], "00:00:00:00:00:00:00:00")
    serial_number = data.get(config_module.SENSOR_DETAILS['serial_number']['endpoint'], "")
    firmware_version = data.get(config_module.SENSOR_DETAILS['firmware_version']['endpoint'], "")
    device_type = data.get(config_module.SENSOR_DETAILS['device_type']['endpoint'], "")

    device_info = {
        "identifiers": {(DOMAIN, serial_number)},
        "name": device_name,
        "manufacturer": make,
        "model": device_type,
        "sw_version": firmware_version,
    }

    # Cache the device info and data
    _device_cache[entry_id] = {
        "timestamp": time.time(),
        "device_info": device_info,
        "data": data,
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
