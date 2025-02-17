import logging
import aiohttp

from .const import DOMAIN, MAKES, CONF_MAKE  # Import constants for devices
LOGGER = logging.getLogger(__name__)

async def async_send_command(hass, ip_address, endpoint, data=None):
    """Helper function to send commands to the device."""
    # Format the endpoint with the provided data if available
    if data:
        endpoint = endpoint.format(**data)
    
    # Construct the full URL
    url = BASE_URL.format(ip=ip_address) + endpoint

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                LOGGER.info(f"Successfully sent command to {endpoint}.")
            else:
                LOGGER.error(f"Failed to send command to {endpoint}: HTTP {response.status}")

async def async_service_handler(hass, call, service_name):
    """General service handler to handle different services."""
    for entry_data in hass.data[DOMAIN].values():
        ip_address = entry_data.get("ip_address")
        
        # Dynamically determine which device constants to use
        make = entry_data.get(CONF_MAKE, "pontos")
        device_const = MAKES[make]

        # Extract service endpoint from the corresponding device constants
        endpoint = device_const.SERVICES[service_name]["endpoint"]
        
        # Handle the service call with dynamic data if provided
        await async_send_command(hass, ip_address, endpoint, call.data)

async def register_services(hass):
    """Register all custom services based on the device's service definitions."""
    for entry_data in hass.data[DOMAIN].values():
        make = entry_data.get(CONF_MAKE, "pontos")
        device_const = MAKES[make]

        # Register services for the specific device
        for service_name in device_const.SERVICES.keys():
            if not hass.services.has_service(DOMAIN, service_name):
                async def _service_handler(call, service_name=service_name):
                    await async_service_handler(hass, call, service_name)

                # Register each service with Hass
                hass.services.async_register(
                    DOMAIN,
                    service_name,
                    _service_handler,
                    schema=None
                )
