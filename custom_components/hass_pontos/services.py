import logging
from .utils import fetch_data

from .const import DOMAIN, MAKES, CONF_MAKE, CONF_IP_ADDRESS

LOGGER = logging.getLogger(__name__)


async def async_send_command(hass, ip_address, base_url, endpoint, data=None):
    """Helper function to send commands to the device."""
    # Format the endpoint with dynamic data if provided
    if data:
        endpoint = endpoint.format(**data)

    # Construct the full URL from the device-specific base URL
    url = base_url.format(ip=ip_address) + endpoint

    # Use fetch_data for retries
    result = await fetch_data(hass, ip_address, url, max_attempts=4, retry_delay=1)

    # Log the response
    if result:
        LOGGER.debug(f"Command sent successfully to {url}: {result}")
    else:
        LOGGER.error(f"Failed to send command to {url}")


async def async_service_handler(hass, call, service_name):
    """General service handler to handle different services."""

    for entry_id, entry_data in hass.data[DOMAIN].get("entries", {}).items():
        config_entry = entry_data["entry"]
        coordinator = entry_data["coordinator"]
        lock = entry_data["command_lock"]

        if not config_entry or not lock:
            continue

        if lock.locked():
            LOGGER.warning(
                f"Service '{service_name}' skipped: previous command still running"
            )
            continue

        async with lock:
            ip_address = config_entry.options.get(CONF_IP_ADDRESS)
            make = config_entry.data.get(CONF_MAKE)
            device_const = MAKES[make]

            # Grab the device-specific BASE_URL
            base_url = device_const.BASE_URL

            # Extract the endpoint for the requested service
            endpoint = device_const.SERVICES[service_name]["endpoint"]

            # Send the command with dynamic data (if any)
            await async_send_command(hass, ip_address, base_url, endpoint, call.data)

            # Trigger a data refresh after the command
            await coordinator.async_refresh()


async def register_services(hass):
    """Register custom services for all current config entries."""
    entries = hass.data[DOMAIN].get("entries", {})
    for entry_data in entries.values():
        config_entry = entry_data["entry"]
        make = config_entry.data.get(CONF_MAKE)
        device_const = MAKES[make]

        # For each service this device supports, register a handler
        for service_name in device_const.SERVICES.keys():

            async def service_handler(call, service_name=service_name):
                await async_service_handler(hass, call, service_name)

            hass.services.async_register(
                DOMAIN, service_name, service_handler, schema=None
            )
