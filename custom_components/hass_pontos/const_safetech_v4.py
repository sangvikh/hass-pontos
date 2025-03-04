from datetime import  timedelta
from homeassistant.components.valve import STATE_OPEN, STATE_OPENING, STATE_CLOSED, STATE_CLOSING
from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.sensor import SensorDeviceClass

PLATFORMS = ['sensor', 'button', 'valve', 'select']

MODEL = "SafeTech+"
MANUFACTURER = "SYR"
CONF_IP_ADDRESS = "ip_address"
CONF_DEVICE_NAME = "device_name"
FETCH_INTERVAL = timedelta(seconds=10)

BASE_URL = "http://{ip}:5333/safe-tec/"
URL_ADMIN = f"{BASE_URL}set/ADM/(2)f"
URL_ALL_DATA = f"{BASE_URL}get/all"

URL_LIST = [
    URL_ADMIN,
    URL_ALL_DATA
]

ALARM_CODES = {
    "FF": "No alarm",
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
        "device_class": "water",
        "state_class": "total_increasing",
        "format_dict": {"Vol[L]": ""}
    },
    "water_pressure": {
        "name": "Water pressure",
        "endpoint": "getBAR",
        "unit": "bar",
        "device_class": "pressure",
        "format_dict": {"mbar": ""},
        "scale": 0.001
    },
    "water_flow": {
        "name": "Water flow",
        "endpoint": "getFLO",
        "unit": "L/min",
        "device_class": "volume_flow_rate",
        "scale": 1
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
        "format_dict": {"mL": ""},
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
        "entity_category": EntityCategory.DIAGNOSTIC,
        "code_dict": {"0":"Not connected","1":"Connecting","2":"Connected"}
    },
    "wifi_signal_strength": {
        "name": "Wifi signal strength",
        "endpoint": "getWFR",
        "unit": "%",
        "device_class": "signal_strength",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "battery_voltage": {
        "name": "Battery voltage",
        "endpoint": "getBAT",
        "unit": "V",
        "device_class": "voltage",
        "format_dict": {",": "."},
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "mains_voltage": {
        "name": "Mains voltage",
        "endpoint": "getNET",
        "unit": "V",
        "device_class": "voltage",
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
        "code_dict": ALARM_CODES
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
        "endpoint": "set/prf/{profile_number}"
    },
}