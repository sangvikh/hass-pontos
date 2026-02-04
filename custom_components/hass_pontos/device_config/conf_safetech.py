from homeassistant.components.valve import STATE_OPEN, STATE_OPENING, STATE_CLOSED, STATE_CLOSING
from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.sensor import SensorDeviceClass

PLATFORMS = ['sensor', 'button', 'valve', 'select', 'time']

MODEL = "SafeTech+"
MANUFACTURER = "SYR"

BASE_URL = "http://{ip}:5333/trio/"
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
    "AB": "alarm_weak_battery",
    "AE": "error_no_information"
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
    "FF": "no_warning"
}

VALVE_CODES = {
    "10": STATE_CLOSED,
    "11": STATE_CLOSING,
    "20": STATE_OPEN,
    "21": STATE_OPENING
}

MICROLEAKAGE_SCHEDULE_CODES = {
    "1": "daily",
    "2": "weekly",
    "3": "monthly"
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
        "state_class": "total_increasing"
    },
    "water_pressure": {
        "name": "Water pressure",
        "endpoint": "getBAR",
        "unit": "bar",
        "device_class": SensorDeviceClass.PRESSURE,
        "scale": 0.001
    },
    "water_temperature": {
        "name": "Water temperature",
        "endpoint": "getCEL",
        "unit": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "scale": 0.1
    },
    "water_flow": {
        "name": "Water flow",
        "endpoint": "getFLO",
        "unit": "L/h",
        "device_class": SensorDeviceClass.VOLUME_FLOW_RATE,
        "scale": 1
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
        "scale": 0.01,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "mains_voltage": {
        "name": "Mains voltage",
        "endpoint": "getNET",
        "unit": "V",
        "device_class": SensorDeviceClass.VOLTAGE,
        "scale": 0.01,
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
    },
    "alarm_status": {
        "name": "Alarm status",
        "endpoint": "getALA",
        "code_dict": ALARM_CODES,
        "attributes": {
            "raw": "getALA"
        }
    },
    "warning_status": {
        "name": "Warning status",
        "endpoint": "getWRN",
        "code_dict": WARNING_CODES,
        "attributes": {
            "raw": "getWRN"
        }
    },
    "notification_status": {
        "name": "Notification status",
        "endpoint": "getNOT",
        "code_dict": NOTIFICATION_CODES,
        "attributes": {
            "raw": "getNOT"
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
        "name": "Microleakage test schedule",
        "endpoint": "getDRP",
        "code_dict": MICROLEAKAGE_SCHEDULE_CODES,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "microleakage_status": {
        "name": "Microleakage test status",
        "endpoint": "getDRP",
        "code_dict": {"0": "not_active", "1": "active", "2": "aborted", "3": "skipped"},
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "microleakage_time": {
        "name": "Microleakage test time",
        "endpoint": "getDTT",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "profile_1": {
        "name": "Profile 1 name",
        "endpoint": "getPN1",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume_liters": "getPV1",
            "allowed_leakage_time_minutes": "getPT1",
            "permissible_flow_liters_per_hour": "getPF1",
            "microleakage_test_enabled": "getPM1",
            "return_time_hours": "getPR1"
        }
    },
    "profile_2": {
        "name": "Profile 2 name",
        "endpoint": "getPN2",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume_liters": "getPV2",
            "allowed_leakage_time_minutes": "getPT2",
            "permissible_flow_liters_per_hour": "getPF2",
            "microleakage_test_enabled": "getPM2",
            "return_time_hours": "getPR2"
        }
    },
    "profile_3": {
        "name": "Profile 3 name",
        "endpoint": "getPN3",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume_liters": "getPV3",
            "allowed_leakage_time_minutes": "getPT3",
            "permissible_flow_liters_per_hour": "getPF3",
            "microleakage_test_enabled": "getPM3",
            "return_time_hours": "getPR3"
        }
    },
    "profile_4": {
        "name": "Profile 4 name",
        "endpoint": "getPN4",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume_liters": "getPV4",
            "allowed_leakage_time_minutes": "getPT4",
            "permissible_flow_liters_per_hour": "getPF4",
            "microleakage_test_enabled": "getPM4",
            "return_time_hours": "getPR4"
        }
    },
    "profile_5": {
        "name": "Profile 5 name",
        "endpoint": "getPN5",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume_liters": "getPV5",
            "allowed_leakage_time_minutes": "getPT5",
            "permissible_flow_liters_per_hour": "getPF5",
            "microleakage_test_enabled": "getPM5",
            "return_time_hours": "getPR5"
        }
    },
    "profile_6": {
        "name": "Profile 6 name",
        "endpoint": "getPN6",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume_liters": "getPV6",
            "allowed_leakage_time_minutes": "getPT6",
            "permissible_flow_liters_per_hour": "getPF6",
            "microleakage_test_enabled": "getPM6",
            "return_time_hours": "getPR6"
        }
    },
    "profile_7": {
        "name": "Profile 7 name",
        "endpoint": "getPN7",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume_liters": "getPV7",
            "allowed_leakage_time_minutes": "getPT7",
            "permissible_flow_liters_per_hour": "getPF7",
            "microleakage_test_enabled": "getPM7",
            "return_time_hours": "getPR7"
        }
    },
    "profile_8": {
        "name": "Profile 8 name",
        "endpoint": "getPN8",
        "entity_category": EntityCategory.DIAGNOSTIC,
        "attributes": {
            "allowed_leakage_volume_liters": "getPV8",
            "allowed_leakage_time_minutes": "getPT8",
            "permissible_flow_liters_per_hour": "getPF8",
            "microleakage_test_enabled": "getPM8",
            "return_time_hours": "getPR8"
        }
    },
}

SERVICES = {
    "open_valve": {
        "name": "Open valve",
        "endpoint": "set/ab/false"
    },
    "close_valve": {
        "name": "Close valve",
        "endpoint": "set/ab/true"
    },
    "clear_alarms": {
        "name": "Clear alarms",
        "endpoint": "set/ala/255"
    },
    "clear_warnings": {
        "name": "Clear warnings",
        "endpoint": "set/wrn/255"
    },
    "clear_notifications": {
        "name": "Clear notifications",
        "endpoint": "set/not/255"
    },
    "set_profile": {
        "name": "Set Profile",
        "endpoint": "set/prf/{data}"
    },
    "microleakage_test": {
        "name": "Start microleakage test",
        "endpoint": "set/dex"
    },
    "microleakage_time": {
        "name": "Set microleakage test time",
        "endpoint": "set/dtt/{data}"
    },
    "microleakage_schedule": {
        "name": "Set microleakage test schedule",
        "endpoint": "set/drp/{data}"
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
    },
    "clear_warnings": {
        "name": "Clear warnings",
        "service": "clear_warnings",
        "availability_sensor": "warning_status"
    },
    "clear_notifications": {
        "name": "Clear notifications",
        "service": "clear_notifications",
        "availability_sensor": "notification_status"
    },
    "microleakage_test": {
        "name": "Start microleakage test",
        "service": "microleakage_test",
        "availability_sensor": "Microleakage test status",
        "entity_category": EntityCategory.DIAGNOSTIC
    }
}

SELECTORS = {
    "profile_select": {
        "name": "Profile",
        "type": "profile_select"
    },
    "microleakage_schedule": {
        "name": "Microleakage test interval",
        "options": MICROLEAKAGE_SCHEDULE_CODES,
        "sensor": "Microleakage test schedule",
        "service": "microleakage_schedule",
        "entity_category": EntityCategory.CONFIG
    },
}

TIME_ENTRIES = {
    "microleakage_time": {
        "name": "Microleakage test time",
        "sensor": "Microleakage test time",
        "service": "microleakage_time",
        "entity_category": EntityCategory.CONFIG
    }
}