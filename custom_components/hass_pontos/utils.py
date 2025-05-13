import logging
import asyncio
from aiohttp import ClientConnectorError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

LOGGER = logging.getLogger(__name__)

# Fetching data with error handling and URL logging
async def fetch_data(hass, ip, url_list, max_attempts=1, retry_delay=10):
    """Fetch data from the Pontos device using the shared aiohttp session (with simple retry logic)."""
    if isinstance(url_list, str):
        # Convert to a one-element list
        url_list = [url_list]

    urls = [url.format(ip=ip) for url in url_list]
    data = {}

    # Get the shared aiohttp session from Home Assistant
    session = async_get_clientsession(hass)
    
    # Loop over attempts for a simple retry mechanism
    for attempt in range(1, max_attempts + 1):
        # Iterate over each URL and fetch data
        for url in urls:
            try:
                # Use async with only on the request, not the session
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        data.update(await response.json())  # Update data with response
                    else:
                        LOGGER.error(f"HTTP request error (status {response.status}): {url}")
            except (ClientConnectorError, asyncio.TimeoutError) as e:
                LOGGER.error(f"HTTP request error for {url}: {e}")

        # If data is not empty, break out of the retry loop
        if data:
            break

        # If still no data, wait before retrying (unless it's the last attempt)
        if attempt < max_attempts:
            LOGGER.warning(
                f"No data retrieved on attempt {attempt}/{max_attempts}. Retrying in {retry_delay*attempt} seconds..."
            )
            await asyncio.sleep(retry_delay*attempt)

    return data