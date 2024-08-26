import logging
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

from .const import DOMAIN, URL_LIST, CONF_IP_ADDRESS
from .utils import fetch_data

LOGGER = logging.getLogger(__name__)

# Cache to store device data
_device_cache = {}

async def get_device_info(hass, entry):
    entry_id = entry.entry_id
    ip_address = entry.data[CONF_IP_ADDRESS]

    # Check if the data is already cached
    if entry_id in _device_cache:
        LOGGER.debug(f"Using cached data for device {entry_id}")
        return _device_cache[entry_id]['device_info'], _device_cache[entry_id]['data']

    LOGGER.debug(f"Fetching data for device {entry_id} from the device")

    # Fetching all relevant data from the device
    data = await fetch_data(ip_address, URL_LIST)

    # Assign data to variables
    mac_address = data.get("getMAC", "00:00:00:00:00:00:00:00")
    serial_number = data.get("getSRN", "")
    firmware_version = data.get("getVER", "")
    device_type = data.get("getTYP", "")

    # Create a device entry with fetched data
    device_registry = async_get_device_registry(hass)
    device_info = {
        "identifiers": {(DOMAIN, "pontos_base")},
        "connections": {(CONNECTION_NETWORK_MAC, mac_address)},
        "name": "Pontos Base",
        "manufacturer": "Hansgrohe",
        "model": device_type,
        "sw_version": firmware_version,
        "serial_number": serial_number,
    }

    # Register device in the device registry
    device_registry.async_get_or_create(
        config_entry_id=entry_id,
        **device_info
    )

    # Cache the device info and data
    _device_cache[entry_id] = {
        'device_info': device_info,
        'data': data
    }

    return device_info, data
