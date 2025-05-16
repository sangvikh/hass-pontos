from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
import logging

from .utils import fetch_data
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class PontosDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry, device_const):
        self.hass = hass
        self.entry = entry
        self.device_const = device_const
        self.ip_address = entry.options[device_const.CONF_IP_ADDRESS]
        self.url_list = device_const.URL_LIST
        self.fetch_interval = timedelta(seconds=entry.options[device_const.CONF_FETCH_INTERVAL])

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_coordinator_{entry.entry_id}",
            update_interval=self.fetch_interval,
        )

    async def _async_update_data(self):
        try:
            data = await fetch_data(
                self.hass,
                self.ip_address,
                self.url_list,
                max_attempts=4,
                retry_delay=self.entry.options[self.device_const.CONF_FETCH_INTERVAL]
            )
            if not data:
                raise UpdateFailed("No data received from device")
            return data
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err