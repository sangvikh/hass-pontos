# FILE: services.py
import logging
import importlib
import aiohttp

from .const import DOMAIN, MAKES, CONF_MAKE
from .const import FETCH_INTERVAL  # if needed globally
LOGGER = logging.getLogger(__name__)

async def async_service_handler(hass, call, service_name):
    """Generic handler that sends commands to the device, using the device's endpoints."""
    # We'll need to figure out which entry / device(s) to call. 
    # For each entry in hass.data[DOMAIN], load that device's consts, etc.
    for entry_data in hass.data[DOMAIN].values():
        make = entry_data.get(CONF_MAKE, "pontos")
        module_name = MAKES.get(make, "const_pontos")
        device_const = importlib.import_module(f".{module_name}", __package__)

        ip_address = entry_data.get("ip_address")
        endpoint = device_const.SERVICES[service_name]["endpoint"]

        # If you have placeholders in the endpoint, e.g. format them with call.data
        endpoint = endpoint.format(**call.data) if call.data else endpoint

        # Then do your actual HTTP request
        url = device_const.BASE_URL.format(ip=ip_address) + endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    LOGGER.info(f"Successfully sent command '{service_name}' to {url}")
                else:
                    LOGGER.error(f"Failed to send command '{service_name}' to {url} (status={response.status})")

async def register_services(hass):
    """Register all custom services from the device's service definitions."""
    for entry_data in hass.data[DOMAIN].values():
        make = entry_data.get(CONF_MAKE, "pontos")
        module_name = MAKES.get(make, "const_pontos")
        device_const = importlib.import_module(f".{module_name}", __package__)

        for service_name in device_const.SERVICES.keys():
            # Only register once. If multiple entries are the same make,
            # you can skip re-registering. Or each device might have unique endpoints.
            if not hass.services.has_service(DOMAIN, service_name):
                async def _service_handler(call, service_name=service_name):
                    await async_service_handler(hass, call, service_name)

                hass.services.async_register(
                    DOMAIN,
                    service_name,
                    _service_handler,
                    schema=None
                )
