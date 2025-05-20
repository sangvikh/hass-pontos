from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
import logging
import asyncio

from .utils import fetch_data
from .const import DOMAIN, CONF_IP_ADDRESS, CONF_FETCH_INTERVAL

_LOGGER = logging.getLogger(__name__)

class PontosDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry, device_const):
        self.hass = hass
        self.entry = entry
        self.device_const = device_const
        self.ip_address = entry.options[CONF_IP_ADDRESS]
        self.url_list = device_const.URL_LIST
        self.fetch_interval = timedelta(seconds=entry.options[CONF_FETCH_INTERVAL])
        self._lock = asyncio.Lock()
        self._device_info = None

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_coordinator_{entry.entry_id}",
            update_interval=self.fetch_interval,
        )

    @property
    def device_info(self):
        return self._device_info

    async def _async_update_data(self):
        async with self._lock:
            try:
                data = await fetch_data(
                    self.hass,
                    self.ip_address,
                    self.url_list,
                    max_attempts=4,
                    retry_delay=int(self.fetch_interval.total_seconds())
                )
                if not data:
                    self.async_set_updated_data(None)
                    raise UpdateFailed("No data received from device")

                return data

            except Exception as err:
                self.async_set_updated_data(None)
                raise UpdateFailed(f"Error fetching data: {err}") from err
