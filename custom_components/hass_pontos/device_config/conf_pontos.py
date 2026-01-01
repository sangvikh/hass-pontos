from homeassistant.components.valve import STATE_OPEN, STATE_OPENING, STATE_CLOSED, STATE_CLOSING
from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.sensor import SensorDeviceClass

PLATFORMS = ['sensor', 'button', 'valve', 'select']

MODEL = "Pontos Base"
MANUFACTURER = "Hansgrohe"

BASE_URL = "http://{ip}:5333/pontos-base/"
URL_ADMIN = f"{BASE_URL}set/ADM/(2)f"
URL_CONDITION = f"{BASE_URL}get/cnd"
URL_ALL_DATA = f"{BASE_URL}get/all"

URL_LIST = [
    URL_ADMIN,
    URL_CONDITION,
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
    "AB": "alarm_weak_battery",
    "AE": "error_no_information"
}

VALVE_CODES = {
    "10": STATE_CLOSED,
    "11": STATE_CLOSING,
    "20": STATE_OPEN,
    "21": STATE_OPENING
}

WIFI_STATUS_CODES = {
    "0": "not_connected",
    "1": "connecting",
    "2": "connected"
}

SENSOR_DETAILS = {
    "total_consumption": {
        "name": "Total water consumption",
        "endpoint": "getVOL",
        "unit": "L",
        "device_class": SensorDeviceClass.WATER,
        "state_class": "total_increasing",
        "format_dict": {"Vol[L]": ""}
    },
    "water_pressure": {
        "name": "Water pressure",
        "endpoint": "getBAR",
        "unit": "bar",
        "device_class": SensorDeviceClass.PRESSURE,
        "format_dict": {"mbar": ""},
        "scale": 0.001
    },
    "water_temperature": {
        "name": "Water temperature",
        "endpoint": "getCEL",
        "unit": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "scale": 0.1
    },
    "no_pulse_time": {
        "name": "Time since last turbine pulse",
        "endpoint": "getNPS",
        "unit": "s"
    },
    "current_consumption": {
        "name": "Current water consumption",
        "endpoint": "getAVO",
        "unit": "L",
        "device_class": SensorDeviceClass.WATER,
        "format_dict": {"mL": ""},
        "entity_category": EntityCategory.DIAGNOSTIC,
        "scale": 0.001
    },
    "leak_test_pressure": {
        "name": "Leak test pressure drop",
        "endpoint": "getDBD",
        "unit": "bar",
        "device_class": SensorDeviceClass.PRESSURE,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "wifi_state": {
        "name": "Wifi state",
        "endpoint": "getWFS",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "code_dict": WIFI_STATUS_CODES
    },
    "wifi_signal_strength": {
        "name": "Wifi signal strength",
        "endpoint": "getWFR",
        "unit": "%",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "battery_voltage": {
        "name": "Battery voltage",
        "endpoint": "getBAT",
        "unit": "V",
        "device_class": SensorDeviceClass.VOLTAGE,
        "format_dict": {",": "."},
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "mains_voltage": {
        "name": "Mains voltage",
        "endpoint": "getNET",
        "unit": "V",
        "device_class": SensorDeviceClass.VOLTAGE,
        "format_dict": {",": "."},
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
    "device_type": {
        "name": "Device type",
        "endpoint": "getTYP",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "mac_address": {
        "name": "MAC address",
        "endpoint": "getMAC",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "alarm_status": {
        "name": "Alarm status",
        "endpoint": "getALA",
        "code_dict": ALARM_CODES,
        "attributes": {
            "raw": "getALA"
        }
    },
    "active_profile": {
        "name": "Active profile",
        "endpoint": "getPRF",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "valve_status": {
        "name": "Valve status",
        "endpoint": "getVLV",
        "code_dict": VALVE_CODES,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "water_conductivity": {
        "name": "Water conductivity",
        "endpoint": "getCND",
        "unit": "µS/cm"
    },
    "water_hardness": {
        "name": "Water hardness",
        "endpoint": "getCND",
        "unit": "dH",
        "scale": 1/30
    },
        "microleakage_schedule": {
        "name": "Microleakage test interval",
        "endpoint": "getDRP",
        "code_dict": {"1": "daily", "2": "weekly", "3": "montly"},
        "entity_category": EntityCategory.DIAGNOSTIC
    },
        "profile_1": {
        "name": "Profile 1 name",
        "endpoint": "getPN1",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume": "getPV1",
            "allowed_leakage_time": "getPT1",
            "permissible_flow": "getPF1",
            "microleakage_test_enabled": "getPM1",
            "return_time_hours": "getPR1"
        }
    },
        "profile_2": {
        "name": "Profile 2 name",
        "endpoint": "getPN2",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume": "getPV2",
            "allowed_leakage_time": "getPT2",
            "permissible_flow": "getPF2",
            "microleakage_test_enabled": "getPM2",
            "return_time_hours": "getPR2"
        }
    },
        "profile_3": {
        "name": "Profile 3 name",
        "endpoint": "getPN3",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume": "getPV3",
            "allowed_leakage_time": "getPT3",
            "permissible_flow": "getPF3",
            "microleakage_test_enabled": "getPM3",
            "return_time_hours": "getPR3"
        }
    },
        "profile_4": {
        "name": "Profile 4 name",
        "endpoint": "getPN4",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume": "getPV4",
            "allowed_leakage_time": "getPT4",
            "permissible_flow": "getPF4",
            "microleakage_test_enabled": "getPM4",
            "return_time_hours": "getPR4"
        }
    },
        "profile_5": {
        "name": "Profile 5 name",
        "endpoint": "getPN5",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume": "getPV5",
            "allowed_leakage_time": "getPT5",
            "permissible_flow": "getPF5",
            "microleakage_test_enabled": "getPM5",
            "return_time_hours": "getPR5"
        }
    },
        "profile_6": {
        "name": "Profile 6 name",
        "endpoint": "getPN6",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume": "getPV6",
            "allowed_leakage_time": "getPT6",
            "permissible_flow": "getPF6",
            "microleakage_test_enabled": "getPM6",
            "return_time_hours": "getPR6"
        }
    },
        "profile_7": {
        "name": "Profile 7 name",
        "endpoint": "getPN7",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume": "getPV7",
            "allowed_leakage_time": "getPT7",
            "permissible_flow": "getPF7",
            "microleakage_test_enabled": "getPM7",
            "return_time_hours": "getPR7"
        }
    },
        "profile_8": {
        "name": "Profile 8 name",
        "endpoint": "getPN8",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume": "getPV8",
            "allowed_leakage_time": "getPT8",
            "permissible_flow": "getPF8",
            "microleakage_test_enabled": "getPM8",
            "return_time_hours": "getPR8"
        }
    },
}

SERVICES = {
    "open_valve": {
        "name": "Open valve",
        "endpoint": "set/ab/1"
    },
    "close_valve": {
        "name": "Close valve",
        "endpoint": "set/ab/2"
    },
    "clear_alarms": {
        "name": "Clear alarms",
        "endpoint": "clr/ala"
    },
    "set_profile": {
        "name": "Set Profile",
        "endpoint": "set/prf/{data}"
    },
    "generic_service": {
        "name": "Generic service call",
        "endpoint": "set/{endpoint}/{data}"
    },
}

BUTTONS = {
    "clear_alarms": {
        "name": "Clear alarms",
        "service": "clear_alarms",
        "availability_sensor": "alarm_status"
    }
}

SELECTORS = {
    "profile_select": {
        "name": "Profile",
        "type": "profile_select"
    }
}