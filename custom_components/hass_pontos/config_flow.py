import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .utils import fetch_data
from .const import DOMAIN, CONF_FETCH_INTERVAL, CONF_IP_ADDRESS, CONF_DEVICE_NAME, CONF_MAKE, MAKES

class PontosConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 4
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
                data = {
                    CONF_DEVICE_NAME: user_input[CONF_DEVICE_NAME],
                    CONF_MAKE: user_input[CONF_MAKE],
                }
                options = {
                    CONF_IP_ADDRESS: user_input[CONF_IP_ADDRESS],
                    CONF_FETCH_INTERVAL: user_input[CONF_FETCH_INTERVAL],
                }

                # Now create the config entry
                return self.async_create_entry(
                    title=user_input[CONF_DEVICE_NAME],
                    data=data,
                    options=options,
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
        """Store the config_entry's entry_id so we can retrieve/update it."""
        self.config_entry_id = config_entry.entry_id  # Use a different attribute name

    async def async_step_init(self, user_input=None):
        """
        The first (and possibly only) step of the options flow.
        We'll let the user change the IP address and fetch interval.
        """
        errors = {}

        if user_input is not None:
            # Validate the new IP by fetching from the device
            new_ip = user_input[CONF_IP_ADDRESS]
            config_entry = self.hass.config_entries.async_get_entry(self.config_entry_id)
            make = config_entry.data[CONF_MAKE]

            if await self._test_connection(new_ip, make):
                # If valid, create (or update) the options
                return self.async_create_entry(
                    title="",
                    data=user_input,
                )
            else:
                errors["base"] = "cannot_connect"

        # Show the form to edit IP address and fetch interval
        config_entry = self.hass.config_entries.async_get_entry(self.config_entry_id)
        current_ip = config_entry.options.get(CONF_IP_ADDRESS)
        current_fetch_interval = config_entry.options.get(CONF_FETCH_INTERVAL, 10)

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
