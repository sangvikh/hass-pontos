from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
import logging
import asyncio

from .utils import fetch_data
from .const import CONF_DEVICE_NAME, CONF_IP_ADDRESS, CONF_FETCH_INTERVAL

_LOGGER = logging.getLogger(__name__)

class PontosDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry, device_const):
        self.hass = hass
        self.entry = entry
        self.device_name = entry.data[CONF_DEVICE_NAME]
        self.ip_address = entry.options[CONF_IP_ADDRESS]
        self.url_list = device_const.URL_LIST
        self._lock = asyncio.Lock()

        super().__init__(
            hass,
            _LOGGER,
            name=f"{self.device_name} Coordinator",
            update_interval=timedelta(seconds=self.entry.options[CONF_FETCH_INTERVAL]),
        )

    async def _async_update_data(self):
        async with self._lock:
            self._update_options()
            try:
                data = await fetch_data(
                    self.hass,
                    self.ip_address,
                    self.url_list,
                    max_attempts=4,
                    retry_delay=int(self.update_interval.total_seconds())
                )
                if not data:
                    self.async_set_updated_data(None)
                    raise UpdateFailed(f"No data received from device at {self.ip_address}")

                return data

            except Exception as err:
                self.async_set_updated_data(None)
                raise UpdateFailed(f"Error fetching data: {err}")

    def _update_options(self):
        self.update_interval = timedelta(seconds=self.entry.options[CONF_FETCH_INTERVAL])