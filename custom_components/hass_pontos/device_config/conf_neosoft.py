from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.sensor import SensorDeviceClass

PLATFORMS = ["sensor", "button"]

MODEL = "NeoSoft"
MANUFACTURER = "SYR"

BASE_URL = "http://{ip}:5333/neosoft/"
URL_ALL_DATA = f"{BASE_URL}get/all"

URL_LIST = [
    URL_ALL_DATA
]

ALARM_CODES = {
    "FF": "no_alarm",
    "A1": "alarm_end_switch",
    "A2": "alarm_turbine_blocked",
    "A3": "alarm_leakage_volume_reached",
    "A4": "alarm_leakage_time_reached",
    "A5": "alarm_max_flow_rate_reached",
    "A6": "alarm_microleakage_detected",
    "A7": "alarm_external_sensor_leakage_radio",
    "A8": "alarm_external_sensor_leakage_cable",
    "A9": "alarm_pressure_sensor_faulty",
    "AA": "alarm_temperature_sensor_faulty",
    "AB": "fault_conductance_sensor",
    "AC": "fault_conductance_sensor",
    "AE": "error_no_information",
    "AD": "alarm_increased_water_hardness",
    "0D": "alarm_salt_supply_empty",
    "0E": "alarm_valve_position",
}

NOTIFICATION_CODES = {
    "01": "new_software_available",
    "04": "new_software_installed",
    "FF": "no_notification"
}

WARNING_CODES = {
    "01": "power_outage",
    "07": "leak_warning",
    "08": "battery_low",
    "02": "salt_supply_low",
    "FF": "no_warning"
}

REGEN_STATE_CODES = {
    "0": "regeneration_idle",
    "1": "regeneration_bottle_1",
    "2": "regeneration_bottle_2",
}

REGEN_MODE_CODES = {
    "2": "Standard",
    "2": "ECO",
    "3": "Power",
    "4": "Automatic",
}

SENSOR_DETAILS = {
    "total_consumption": {
        "name": "Total water consumption",
        "endpoint": "getVOL",
        "unit": "L",
        "device_class": SensorDeviceClass.WATER,
        "state_class": "total_increasing"
    },
    "input_water_hardness": {
        "name": "Input water hardness",
        "endpoint": "getIWH",
        "unit": "°dH",
        "scale": 1
    },
    "output_water_hardness": {
        "name": "Output water hardness",
        "endpoint": "getOWH",
        "unit": "°dH",
        "scale": 1,
    },
    "salt_amount": {
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
    "regeneration_mode": {
        "name": "Regeneration mode",
        "endpoint": "getRMO ",
        "code_dict": REGEN_MODE_CODES,
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
    "regeneration_schedule": {
        "name": "Regeneration schedule",
        "endpoint": "getRPD",
        "unit": "days",
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
    "clear_alarms": {
        "name": "Clear alarms",
        "endpoint": "set/ala/255"
    },
    "set_regeneration_mode": {
        "name": "Set regeneration mode",
        "endpoint": "set/rmo/{mode}"
    },
    "set_regeneration_interval": {
        "name": "Set regeneration interval",
        "endpoint": "set/rpd/{period}"
    },
    "set_regeneration_time": {
        "name": "Set regeneration time",
        "endpoint": "set/rtm/{time}"
    }
}
