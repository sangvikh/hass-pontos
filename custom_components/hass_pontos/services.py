import logging
import aiohttp

from .const import DOMAIN, MAKES, CONF_MAKE

LOGGER = logging.getLogger(__name__)

async def async_send_command(hass, ip_address, base_url, endpoint, data=None):
    """Helper function to send commands to the device."""
    # Format the endpoint with dynamic data if provided
    if data:
        endpoint = endpoint.format(**data)

    # Construct the full URL from the device-specific base URL
    url = base_url.format(ip=ip_address) + endpoint

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                LOGGER.info(f"Successfully sent command to {endpoint}.")
            else:
                LOGGER.error(
                    f"Failed to send command to {endpoint}: HTTP {response.status}"
                )

async def async_service_handler(hass, call, service_name):
    """General service handler to handle different services."""
    for entry_data in hass.data[DOMAIN].values():
        ip_address = entry_data.get("ip_address")

        # Dynamically determine which device constants to use
        make = entry_data.get(CONF_MAKE)
        device_const = MAKES[make]

        # Grab the device-specific BASE_URL
        base_url = device_const.BASE_URL

        # Extract the endpoint for the requested service
        endpoint = device_const.SERVICES[service_name]["endpoint"]

        # Send the command with dynamic data (if any)
        await async_send_command(hass, ip_address, base_url, endpoint, call.data)

async def register_services(hass):
    """Register custom services for all current config entries."""
    for entry_data in hass.data[DOMAIN].values():
        make = entry_data.get(CONF_MAKE)
        device_const = MAKES[make]

        # For each service this device supports, register a handler
        for service_name in device_const.SERVICES.keys():
            async def service_handler(call, service_name=service_name):
                await async_service_handler(hass, call, service_name)

            hass.services.async_register(
                DOMAIN,
                service_name,
                service_handler,
                schema=None
            )
