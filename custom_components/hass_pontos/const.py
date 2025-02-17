from datetime import timedelta
from . import const_pontos
from . import const_trio
from . import const_safetech

DOMAIN = "hass_pontos"
CONF_IP_ADDRESS = "ip_address"
CONF_DEVICE_NAME = "device_name"
CONF_MAKE = "make"

MAKES = {
    "Hansgrohe Pontos": const_pontos,
    "SYR Trio": const_trio,
    "SYR SafeTech+": const_safetech,
}
