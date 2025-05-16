from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
import logging
import asyncio

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
        self._lock = asyncio.Lock()
        self._cached_data = None

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_coordinator_{entry.entry_id}",
            update_interval=self.fetch_interval,
        )

    @property
    def data(self):
        # Expose the cached data (None if last fetch failed)
        return self._cached_data

    async def _async_update_data(self):
        async with self._lock:
            try:
                data = await fetch_data(
                    self.hass,
                    self.ip_address,
                    self.url_list,
                    max_attempts=4,
                    retry_delay=self.entry.options[self.device_const.CONF_FETCH_INTERVAL]
                )
                if not data:
                    self._cached_data = None
                    raise UpdateFailed("No data received from device")
                self._cached_data = data
                return data
            except Exception as err:
                self._cached_data = None
                raise UpdateFailed(f"Error fetching data: {err}") from err