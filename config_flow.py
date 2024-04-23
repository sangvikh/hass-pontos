import aiohttp
import asyncio
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_IP_ADDRESS

class PontosConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            valid = await self._test_connection(user_input[CONF_IP_ADDRESS])
            if valid:
                return self.async_create_entry(title="Pontos Base", data=user_input)
            else:
                errors['base'] = 'cannot_connect'

        return self.async_show_form(
            step_id='user', 
            data_schema=vol.Schema({
                vol.Required(CONF_IP_ADDRESS, description={"suggested_value": "192.168.1.100"}): str,
            }),
            errors=errors
        )

    async def _test_connection(self, ip_address):
        url = f"http://{ip_address}:5333/pontos-base/set/ADM/(2)f"
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(url, timeout=5) as response:
                return response.status == 200
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PontosOptionsFlowHandler(config_entry)

class PontosOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            valid = await self._test_connection(user_input[CONF_IP_ADDRESS])
            if valid:
                return self.async_create_entry(title="", data=user_input)
            else:
                errors['base'] = 'cannot_connect'

        ip_address = self.config_entry.data.get(CONF_IP_ADDRESS)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_IP_ADDRESS, default=ip_address): str,
            }),
            errors=errors
        )

    async def _test_connection(self, ip_address):
        url = f"http://{ip_address}:5333/pontos-base/set/ADM/(2)f"
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(url, timeout=5) as response:
                return response.status == 200
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return False
