import aiohttp
import asyncio
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN, 
    CONF_IP_ADDRESS, 
    CONF_DEVICE_NAME, 
    CONF_MAKE,
    MAKES,         # The dict mapping make -> module
)

class PontosConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step where users enter IP, device name, and pick the make."""
        errors = {}
        
        if user_input is not None:
            # Optional: Validate IP or do a test connection
            valid = await self._test_connection(user_input[CONF_IP_ADDRESS])
            if valid:
                # Make sure the selected make is in our dictionary
                if user_input[CONF_MAKE] in MAKES:
                    return self.async_create_entry(
                        title=user_input.get(CONF_DEVICE_NAME, "Pontos Device"),
                        data=user_input
                    )
                else:
                    errors["base"] = "invalid_make"
            else:
                errors["base"] = "cannot_connect"
        
        # Show the form (including the selection for make)
        schema = vol.Schema({
            vol.Required(CONF_IP_ADDRESS, description={"suggested_value": "192.168.1.100"}): str,
            vol.Optional(CONF_DEVICE_NAME, default="Pontos Base"): str,
            vol.Required(CONF_MAKE, default="pontos"): vol.In(list(MAKES.keys())),
        })
        
        return self.async_show_form(
            step_id="user", 
            data_schema=schema,
            errors=errors
        )

    async def _test_connection(self, ip_address: str) -> bool:
        """Test the connection to the device (optional)."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(f"http://{ip_address}:5333/pontos-base/get/all", timeout=5) as response:
                return response.status == 200
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow if any."""
        return PontosOptionsFlowHandler(config_entry)


class PontosOptionsFlowHandler(config_entries.OptionsFlow):
    """Example of an OptionsFlow if you want to edit IP or other settings."""
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        # Similar form for editing IP, or make, etc.
        return self.async_show_form(step_id="user")
