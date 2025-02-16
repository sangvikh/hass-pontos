import logging
import asyncio
from aiohttp import ClientConnectorError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

LOGGER = logging.getLogger(__name__)

# Fetching data with error handling and URL logging
async def fetch_data(hass, ip, url_list):
    """Fetch data from the Pontos device using the shared aiohttp session."""
    if isinstance(url_list, str):
        # Convert to a one-element list
        url_list = [url_list]

    urls = [url.format(ip=ip) for url in url_list]
    data = {}

    # Get the shared aiohttp session from Home Assistant
    session = async_get_clientsession(hass)
    
    # Iterate over each URL and fetch data
    for url in urls:
        try:
            # Use async with only on the request, not the session
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data.update(await response.json())  # Update data with response
                else:
                    LOGGER.error(f"Failed to fetch data from {url}: HTTP {response.status}")
        except (ClientConnectorError, asyncio.TimeoutError) as e:
            LOGGER.error(f"Error fetching data from {url}: {e}")

    return data
