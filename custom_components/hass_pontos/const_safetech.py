from datetime import  timedelta
from homeassistant.components.valve import STATE_OPEN, STATE_OPENING, STATE_CLOSED, STATE_CLOSING
from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.sensor import SensorDeviceClass

PLATFORMS = ['sensor', 'button', 'valve', 'select']

DOMAIN = "hass_pontos"
MODEL = "SafeTech+"
MANUFACTURER = "SYR"
CONF_IP_ADDRESS = "ip_address"
CONF_DEVICE_NAME = "device_name"
FETCH_INTERVAL = timedelta(seconds=10)

BASE_URL = "http://{ip}:5333/trio/"
URL_ALL_DATA = f"{BASE_URL}get/all"

URL_LIST = [
    URL_ALL_DATA
]

ALARM_CODES = {
    "ff": "No alarm",
    "A1": "ALARM END SWITCH",
    "A2": "ALARM: Turbine blocked!",
    "A3": "ALARM: Leakage volume reached!",
    "A4": "ALARM: Leakage time reached!",
    "A5": "ALARM: Maximum flow rate reached!",
    "A6": "ALARM: Microleakage detected!",
    "A7": "ALARM EXT. SENSOR LEAKAGE RADIO",
    "A8": "ALARM EXT. SENSOR LEAKAGE CABLE",
    "A9": "ALARM: Pressure sensor faulty!",
    "AA": "ALARM: Temperature sensor faulty!",
    "AB": "ALARM: Weak battery!",
    "AE": "Error: no information available"
}

WARING_CODES = {
    "1": "Power outage",
    "7": "Leak warning",
    "8": "Battery low",
    "ff": "No warning"
}

NOTIFICATION_CODES = {
    "1": "New Software Update Available!",
    "4": "New software update installed!",
    "ff": "No notification",
}

PROFILE_CODES = {
    1: "Home",
    2: "Away",
    3: "Holiday",
    4: "Increased consumption",
    5: "Max. consumption",
    6: "not defined",
    7: "not defined",
    8: "not defined"
}

VALVE_CODES = {
    10: STATE_CLOSED,
    11: STATE_CLOSING,
    20: STATE_OPEN,
    21: STATE_OPENING
}

SENSOR_DETAILS = {
    "total_consumption": {
        "name": "Total water consumption",
        "endpoint": "getVOL",
        "unit": "L",
        "device_class": "water",
        "state_class": "total_increasing"
    },
    "water_pressure": {
        "name": "Water pressure",
        "endpoint": "getBAR",
        "unit": "bar",
        "device_class": "pressure",
        "scale": 0.001
    },
    "water_temperature": {
        "name": "Water temperature",
        "endpoint": "getCEL",
        "unit": "°C",
        "device_class": "temperature",
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
        "entity_category": EntityCategory.DIAGNOSTIC,
        "scale": 0.001
    },
    "leak_test_pressure": {
        "name": "Leak test pressure drop",
        "endpoint": "getDBD",
        "unit": "bar",
        "device_class": "pressure",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "wifi_state": {
        "name": "Wifi state",
        "endpoint": "getWFS",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "wifi_signal_strength": {
        "name": "Wifi signal strength",
        "endpoint": "getWFR",
        "unit": "dBm",
        "device_class": "signal_strength",
        "scale": -1,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "battery_voltage": {
        "name": "Battery voltage",
        "endpoint": "getBAT",
        "unit": "V",
        "device_class": "voltage",
        "scale": 0.01,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "mains_voltage": {
        "name": "Mains voltage",
        "endpoint": "getNET",
        "unit": "V",
        "device_class": "voltage",
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
        "code_dict": WARING_CODES
    },
    "notification_status": {
        "name": "Notification status",
        "endpoint": "getNOT",
        "code_dict": NOTIFICATION_CODES
    },
    "active_profile": {
        "name": "Active profile",
        "endpoint": "getPRF",
        "code_dict": PROFILE_CODES,
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
    }
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
    "set_profile": {
        "name": "Set Profile",
        "endpoint": "set/prf/{profile_number}"
    },
}