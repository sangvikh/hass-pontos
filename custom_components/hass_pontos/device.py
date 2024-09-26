import logging
import time
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

from .const import DOMAIN, URL_LIST, CONF_IP_ADDRESS, CONF_DEVICE_NAME, FETCH_INTERVAL
from .utils import fetch_data

LOGGER = logging.getLogger(__name__)

# Cache to store device data
_device_cache = {}

async def get_device_info(hass, entry):
    entry_id = entry.entry_id
    ip_address = entry.data[CONF_IP_ADDRESS]
    device_name = entry.data[CONF_DEVICE_NAME]

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

    # Fetching all relevant data from the device
    data = await fetch_data(ip_address, URL_LIST)

    # Assign data to variables
    mac_address = data.get("getMAC", "00:00:00:00:00:00:00:00")
    serial_number = data.get("getSRN", "")
    firmware_version = data.get("getVER", "")
    device_type = data.get("getTYP", "")

    # Validate the data (skip if MAC address or serial number is invalid)
    if not mac_address or mac_address == "00:00:00:00:00:00:00:00" or not serial_number:
        LOGGER.error(f"Invalid MAC address or serial number for device {entry_id}. Skipping device registration.")
        return None, None

    device_info = {
        "identifiers": {(DOMAIN, "pontos_base")},
        "connections": {(CONNECTION_NETWORK_MAC, mac_address)},
        "name": device_name,
        "manufacturer": "Hansgrohe",
        "model": device_type,
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

    # Get device info and skip registration if the info is None
    device_info, _ = await get_device_info(hass, entry)
    if device_info is None:
        LOGGER.error(f"Device registration skipped for entry {entry_id} due to missing or invalid data.")
        return

    # Register device in the device registry
    device_registry = async_get_device_registry(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry_id,
        **device_info
    )