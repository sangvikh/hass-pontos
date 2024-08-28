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

# Parsing sensor data
def parse_data(data, sensor):
    """Process, format, and validate sensor data."""
    if data is None:
        return None
    _data = data.get(sensor._endpoint, None)

    # Apply format replacements if format_dict is present
    if sensor._format_dict is not None and _data is not None:
        for old, new in sensor._format_dict.items():
            _data = _data.replace(old, new)

    # Translate alarm codes if code_dict is present
    if sensor._code_dict is not None and _data is not None:
        _data = sensor._code_dict.get(_data, _data)

    # Scale sensor data if scale is present
    if sensor._scale is not None and _data is not None:
        try:
            _data = float(_data) * sensor._scale
        except (ValueError, TypeError):
            pass

    return _data
