from homeassistant.components.valve import STATE_OPEN, STATE_OPENING, STATE_CLOSED, STATE_CLOSING
from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.sensor import SensorDeviceClass

PLATFORMS = ['sensor', 'button', 'valve', 'select']

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
    "1": "new_software_available",
    "4": "new_software_installed",
    "FF": "no_notification"
}

WARNING_CODES = {
    "1": "power_outage",
    "7": "leak_warning",
    "8": "battery_low",
    "FF": "no_warning"
}

VALVE_CODES = {
    "10": STATE_CLOSED,
    "11": STATE_CLOSING,
    "20": STATE_OPEN,
    "21": STATE_OPENING
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
        "unit": "L/min",
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
        "code_dict": {"0":"Not connected","1":"Connecting","2":"Connected"}
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
        "code_dict": ALARM_CODES
    },
    "warning_status": {
        "name": "Warning status",
        "endpoint": "getWRN",
        "code_dict": WARNING_CODES
    },
    "notification_status": {
        "name": "Notification status",
        "endpoint": "getNOT",
        "code_dict": NOTIFICATION_CODES
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
        "code_dict": {"1": "daily", "2": "weekly", "3": "montly"},
        "entity_category": EntityCategory.DIAGNOSTIC
    },
        "microleakage_status": {
        "name": "Microleakage test status",
        "endpoint": "getDRP",
        "code_dict": {"0": "not_active", "1": "active", "2": "aborted", "3": "skipped"},
        "entity_category": EntityCategory.DIAGNOSTIC
    },
        "profile_name_1": {
        "name": "Profile 1 name",
        "endpoint": "getPN1",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
        "profile_name_2": {
        "name": "Profile 2 name",
        "endpoint": "getPN2",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
        "profile_name_3": {
        "name": "Profile 3 name",
        "endpoint": "getPN3",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
        "profile_name_4": {
        "name": "Profile 4 name",
        "endpoint": "getPN4",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
        "profile_name_5": {
        "name": "Profile 5 name",
        "endpoint": "getPN5",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
        "profile_name_6": {
        "name": "Profile 6 name",
        "endpoint": "getPN6",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
        "profile_name_7": {
        "name": "Profile 7 name",
        "endpoint": "getPN7",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
        "profile_name_8": {
        "name": "Profile 8 name",
        "endpoint": "getPN8",
        "entity_category": EntityCategory.DIAGNOSTIC
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
        "endpoint": "set/prf/{profile_number}"
    },
    "microleakage_test": {
        "name": "Start microleakage test",
        "endpoint": "set/dex"
    },
    "microleakage_time": {
        "name": "Set microleakage test time",
        "endpoint": "set/dtt/{time}"
    },
    "microleakage_schedule": {
        "name": "Set microleakage test schedule",
        "endpoint": "set/drp/{schedule}"
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
    }
}

SELECT_CONFIG = {
    "profile_select": {
        "name": "Profile select",
        "type": "profile_select"
    }
}