from datetime import timedelta
from . import const_pontos
from . import const_trio
from . import const_safetech

DOMAIN = "hass_pontos"
CONF_IP_ADDRESS = "ip_address"
CONF_DEVICE_NAME = "device_name"
CONF_MAKE = "make"
FETCH_INTERVAL = timedelta(seconds=10)

MAKES = {
    "pontos": const_pontos,
    "trio": const_trio,
    "safetech": const_safetech,
}
