from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.sensor import SensorDeviceClass

PLATFORMS = ["sensor", "button", "select"]

MODEL = "NeoSoft"
MANUFACTURER = "SYR"

BASE_URL = "http://{ip}:5333/neosoft/"
URL_ALL_DATA = f"{BASE_URL}get/all"

URL_LIST = [
    URL_ALL_DATA
]

REGEN_STATE_CODES = {
    "0": "regeneration_idle",
    "1": "regeneration_bottle_1",
    "2": "regeneration_bottle_2",
}

SENSOR_DETAILS = {
    "total_consumption": {
        "name": "Total water consumption",
        "endpoint": "getVOL",
        "unit": "L",
        "device_class": SensorDeviceClass.WATER,
        "state_class": "total_increasing"
    },
    "raw_water_hardness": {
        "name": "Raw water hardness",
        "endpoint": "getIWH",
        "unit": "°dH",
        "scale": 0.1
    },
    "target_water_hardness": {
        "name": "Target water hardness",
        "endpoint": "getOWH",
        "unit": "°dH",
        "scale": 0.1,
        "entity_category": EntityCategory.CONFIG
    },
    "salt_level": {
        "name": "Salt amount",
        "endpoint": "getSV1",
        "unit": "kg",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "salt_level": {
        "name": "Salt supply",
        "endpoint": "getSS1",
        "unit": "weeks",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "regeneration_state": {
        "name": "Regeneration state",
        "endpoint": "getRG1",
        "code_dict": REGEN_STATE_CODES,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "regeneration_time_remaining": {
        "name": "Regeneration time remaining",
        "endpoint": "getRTI",
        "unit": "min",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "regeneration_volume_remaining": {
        "name": "Water until regeneration",
        "endpoint": "getRE1",
        "unit": "L",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "wifi_state": {
        "name": "Wifi state",
        "endpoint": "getWFS",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "code_dict": {"0": "Not connected", "1": "Connecting", "2": "Connected"}
    },
    "wifi_signal_strength": {
        "name": "Wifi signal strength",
        "endpoint": "getWFR",
        "unit": "%",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "serial_number": {
        "name": "Serial number",
        "endpoint": "getSRN",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "firmware_version": {
        "name": "Firmware version",
        "endpoint": "getVER",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "hardware_version": {
        "name": "Hardware version",
        "endpoint": "getHWV",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "mac_address": {
        "name": "MAC address",
        "endpoint": "getMAC1",
        "entity_category": EntityCategory.DIAGNOSTIC
    }
}

SERVICES = {
    "generic_service": {
        "name": "Generic service call",
        "endpoint": "set/{endpoint}/{data}"
    },
}
