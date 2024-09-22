import aiohttp
import logging
import asyncio

LOGGER = logging.getLogger(__name__)

# Fetching data with error handling and URL logging
async def fetch_data(ip, url_list):
    urls = [url.format(ip=ip) for url in url_list]
    data = {}
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data.update(await response.json())
                    else:
                        LOGGER.error(f"Failed to fetch data from {url}: HTTP {response.status}")
            # Handle connection errors
            except aiohttp.ClientConnectorError as e:
                LOGGER.error(f"Connection failed for {url}: {str(e)}")
            # Handle network unreachable errors
            except OSError as e:
                LOGGER.error(f"Network error for {url}: {str(e)}")
            # Handle request timeout
            except asyncio.TimeoutError:
                LOGGER.error(f"Request to {url} timed out.")
    
    return data
