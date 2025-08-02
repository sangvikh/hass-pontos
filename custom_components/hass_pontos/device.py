import logging
import re

from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

from .const import DOMAIN, CONF_DEVICE_NAME, CONF_MAKE, MAKES

LOGGER = logging.getLogger(__name__)

def is_valid_mac(mac_address):
    # Regular expression pattern for a valid MAC address
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return re.match(pattern, mac_address) is not None

async def get_device_info(entry, coordinator):
    entry_id = entry.entry_id
    device_name = entry.data[CONF_DEVICE_NAME]
    make = entry.data.get(CONF_MAKE)
    device_const = MAKES[make]

    data = coordinator.data
    if not data:
        LOGGER.error(f"No data available from coordinator for device {entry_id}")
        raise Exception("No data available from coordinator")

    mac_address = data.get(device_const.SENSOR_DETAILS.get("mac_address", {}).get("endpoint"), "xx:xx:xx:xx:xx:xx")
    serial_number = data.get(device_const.SENSOR_DETAILS.get("serial_number", {}).get("endpoint"), "")
    firmware_version = data.get(device_const.SENSOR_DETAILS.get("firmware_version", {}).get("endpoint"), "")

    if not serial_number:
        LOGGER.error("Invalid serial number")
        raise Exception("Invalid device data")

    device_info = {
        "identifiers": {(DOMAIN, serial_number)},
        "name": device_name,
        "manufacturer": device_const.MANUFACTURER,
        "model": device_const.MODEL,
        "sw_version": firmware_version,
        "serial_number": serial_number,
    }

    # Only add connection info if the MAC address is valid
    if is_valid_mac(mac_address):
        device_info["connections"] = {(CONNECTION_NETWORK_MAC, mac_address)}

    return device_info

async def register_device(hass, entry, coordinator=None):
    entry_id = entry.entry_id

    # Get device info (will raise exception if it fails)
    device_info = await get_device_info(entry, coordinator=coordinator)

    # Store device_info for later use in platforms
    hass.data[DOMAIN]["entries"][entry_id]["device_info"] = device_info

    # Register device in the device registry
    device_registry = async_get_device_registry(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry_id,
        **device_info
    )
