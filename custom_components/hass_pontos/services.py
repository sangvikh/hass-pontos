import logging
import aiohttp

from .const import DOMAIN, SERVICES, BASE_URL

LOGGER = logging.getLogger(__name__)

async def async_send_command(hass, ip_address, endpoint, data=None):
    """Helper function to send commands to the device."""
    if data:
        # Replace placeholders in the endpoint with actual data
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
        
        # Extract any additional data from the service call
        data = call.data
        
        # Handle the service call with dynamic data if provided
        endpoint = SERVICES[service_name]["endpoint"]
        await async_send_command(hass, ip_address, endpoint, data)

async def register_services(hass):
    """Register all custom services."""
    # Register each service dynamically based on the SERVICES dictionary
    for service_name in SERVICES:
        async def service_handler(call, service_name=service_name):
            await async_service_handler(hass, call, service_name)

        hass.services.async_register(
            DOMAIN,
            service_name,
            service_handler,
            schema=None
        )
