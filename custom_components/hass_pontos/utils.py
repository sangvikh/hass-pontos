import aiohttp
import logging
LOGGER = logging.getLogger(__name__)

# Fetching data
async def fetch_data(ip, url_list):
    urls = [url.format(ip=ip) for url in url_list]
    data = {}
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as response:
                if response.status == 200:
                    data.update(await response.json())
                else:
                    LOGGER.error(f"Failed to fetch data: HTTP {response.status}")
    return data
