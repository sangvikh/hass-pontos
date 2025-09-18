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

SALT_STATUS_CODES = {
    "0": "salt_level_ok",
    "1": "salt_level_low",
    "2": "salt_refill_required"
}

REGEN_STATE_CODES = {
    "0": "regeneration_idle",
    "1": "regeneration_pending",
    "2": "regeneration_running",
    "3": "regeneration_rinsing",
    "4": "regeneration_error"
}

REGEN_TRIGGER_CODES = {
    "0": "trigger_none",
    "1": "trigger_volume",
    "2": "trigger_time",
    "3": "trigger_manual",
    "4": "trigger_service"
}

OPERATING_MODE_CODES = {
    "0": "mode_service",
    "1": "mode_bypass",
    "2": "mode_standby"
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
        "endpoint": "getHWI",
        "unit": "°dH",
        "scale": 0.1
    },
    "treated_water_hardness": {
        "name": "Treated water hardness",
        "endpoint": "getHWO",
        "unit": "°dH",
        "scale": 0.1
    },
    "target_water_hardness": {
        "name": "Target water hardness",
        "endpoint": "getHTG",
        "unit": "°dH",
        "scale": 0.1,
        "entity_category": EntityCategory.CONFIG
    },
    "salt_level": {
        "name": "Salt level",
        "endpoint": "getSLP",
        "unit": "%",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "salt_alarm": {
        "name": "Salt alarm",
        "endpoint": "getSLS",
        "code_dict": SALT_STATUS_CODES,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "operating_mode": {
        "name": "Operating mode",
        "endpoint": "getOPS",
        "code_dict": OPERATING_MODE_CODES,
        "entity_category": EntityCategory.CONFIG
    },
    "regeneration_state": {
        "name": "Regeneration state",
        "endpoint": "getRGN",
        "code_dict": REGEN_STATE_CODES,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "regeneration_trigger": {
        "name": "Last regeneration trigger",
        "endpoint": "getRGT",
        "code_dict": REGEN_TRIGGER_CODES,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "regeneration_time_remaining": {
        "name": "Regeneration time remaining",
        "endpoint": "getRGR",
        "unit": "min",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "regeneration_volume_remaining": {
        "name": "Water until regeneration",
        "endpoint": "getRGV",
        "unit": "L",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "days_since_regeneration": {
        "name": "Days since last regeneration",
        "endpoint": "getRGD",
        "unit": "d",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "next_regeneration_time": {
        "name": "Next regeneration time",
        "endpoint": "getRGTm",
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
    "start_regeneration": {
        "name": "Start regeneration",
        "endpoint": "set/rgn/start"
    },
    "stop_regeneration": {
        "name": "Stop regeneration",
        "endpoint": "set/rgn/stop"
    },
    "set_target_hardness": {
        "name": "Set target water hardness",
        "endpoint": "set/htg/{hardness}"
    },
    "set_operating_mode": {
        "name": "Set operating mode",
        "endpoint": "set/ops/{mode}"
    },
    "generic_service": {
        "name": "Generic service call",
        "endpoint": "set/{endpoint}/{data}"
    },
}
