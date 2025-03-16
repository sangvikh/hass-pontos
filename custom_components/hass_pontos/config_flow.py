import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .utils import fetch_data
from .const import DOMAIN, CONF_FETCH_INTERVAL, CONF_IP_ADDRESS, CONF_DEVICE_NAME, CONF_MAKE, MAKES

class PontosConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 3
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user enters IP, device name, and picks the make."""
        errors = {}

        if user_input is not None:
            # Extract IP and make from the form data
            ip = user_input[CONF_IP_ADDRESS]
            make = user_input[CONF_MAKE]

            # Validate the IP by attempting a connection
            valid = await self._test_connection(ip, make)
            if valid:
                return self.async_create_entry(
                    title=user_input.get(CONF_DEVICE_NAME, "Hansgrohe Pontos"),
                    data=user_input,
                )
            else:
                errors["base"] = "cannot_connect"

        # Show the form (including the dropdown for make)
        data_schema = vol.Schema({
            vol.Required(CONF_IP_ADDRESS, description={"suggested_value": "192.168.1.100"}): str,
            vol.Required(CONF_FETCH_INTERVAL, default=10): vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Required(CONF_DEVICE_NAME, default="Pontos"): str,
            vol.Required(CONF_MAKE, default="Hansgrohe Pontos"): vol.In(list(MAKES.keys())),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def _test_connection(self, ip_address: str, make: str) -> bool:
        """Test a connection to the selected device's URLs."""
        device_const = MAKES.get(make)
        if not device_const:
            return False

        url_list = device_const.URL_LIST  # Each make-specific file defines URL_LIST
        data = await fetch_data(self.hass, ip_address, url_list)
        return bool(data)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return PontosOptionsFlowHandler(config_entry)


class PontosOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow, allowing editing the IP address and fetch interval."""

    def __init__(self, config_entry):
        """Store the config_entry so we can retrieve/update it."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """
        The first (and possibly only) step of the options flow.
        We'll let the user change the IP address and fetch interval.
        """
        errors = {}

        if user_input is not None:
            # Validate the new IP by fetching from the device
            new_ip = user_input[CONF_IP_ADDRESS]
            make = self.config_entry.data[CONF_MAKE]

            if await self._test_connection(new_ip, make):
                # If valid, create (or update) the options
                return self.async_create_entry(title="", data=user_input)
            else:
                errors["base"] = "cannot_connect"

        # Show the form to edit IP address and fetch interval
        current_ip = self.config_entry.data.get(CONF_IP_ADDRESS)
        current_fetch_interval = self.config_entry.data.get(CONF_FETCH_INTERVAL, 10)

        if self.config_entry.data.get(CONF_IP_ADDRESS):
            # If there's already an IP in the options, use that instead
            current_ip = self.config_entry.data[CONF_IP_ADDRESS]

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_IP_ADDRESS, default=current_ip): str,
                vol.Required(CONF_FETCH_INTERVAL, default=current_fetch_interval): vol.All(vol.Coerce(int), vol.Range(min=1)),
            }),
            errors=errors
        )

    async def _test_connection(self, ip_address: str, make: str) -> bool:
        """Test if we can successfully reach the device with the new IP."""
        device_const = MAKES.get(make)
        if not device_const:
            return False

        url_list = device_const.URL_LIST
        data = await fetch_data(self.hass, ip_address, url_list)
        return bool(data)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler for this config entry."""
        return PontosOptionsFlowHandler(config_entry)
