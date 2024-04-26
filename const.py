from datetime import  timedelta
DOMAIN = "hass_pontos"
CONF_IP_ADDRESS = "ip_address"
FETCH_INTERVAL = timedelta(seconds=10)

URL_COMMAND = "http://{ip}:5333/pontos-base/set/ADM/(2)f"
URL_CONDITIONS = "http://{ip}:5333/pontos-base/get/cnd"
URL_ALL_DATA = "http://{ip}:5333/pontos-base/get/all"

URL_LIST = [
    URL_COMMAND,
    URL_CONDITIONS,
    URL_ALL_DATA
]

ALARM_CODES = {
    "FF": "no alarm",
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

PROFILE_CODES = {
    "1": "Present",
    "2": "Absent",
    "3": "Vacation",
    "4": "Increased consumption",
    "5": "Maximum consumption",
    "6": "not defined",
    "7": "not defined",
    "8": "not defined"
}

VALVE_CODES = {
    "10": "Closed",
    "11": "Closing",
    "20": "Open",
    "21": "Opening"
}

# In const.py

SENSOR_DETAILS = {
    "total_consumption": {
        "name": "Total consumption in liters",
        "endpoint": "getVOL",
        "unit": "L",
        "device_class": "water",
        "state_class": "total_increasing",
        "format_dict": {"Vol[L]": ""}
    },
    "water_pressure": {
        "name": "Water pressure",
        "endpoint": "getBAR",
        "unit": "mbar",
        "device_class": "pressure",
        "format_dict": {"mbar": ""}
    },
    "water_temperature": {
        "name": "Water temperature",
        "endpoint": "getCEL",
        "unit": "°C",
        "device_class": "temperature",
        "scale": 0.1
    },
    "no_pulse_time": {
        "name": "Time since last pulse",
        "endpoint": "getNPS",
        "unit": "s"
    },
    "current_consumption": {
        "name": "Current water consumption",
        "endpoint": "getAVO",
        "unit": "mL",
        "device_class": "water",
        "format_dict": {"mL": ""}
    },
    "leak_test_pressure": {
        "name": "Leak test pressure",
        "endpoint": "getDBD",
        "unit": "bar",
        "device_class": "pressure"
    },
    "wifi_state": {
        "name": "Wifi state",
        "endpoint": "getWFS"
    },
    "wifi_signal_strength": {
        "name": "Wifi signal strength",
        "endpoint": "getWFR",
        "unit": "dB",
        "device_class": "signal_strength",
        "scale": -1
    },
    "battery_voltage": {
        "name": "Battery voltage",
        "endpoint": "getBAT",
        "unit": "V",
        "device_class": "voltage",
        "format_dict": {",": "."}
    },
    "mains_voltage": {
        "name": "Mains voltage",
        "endpoint": "getNET",
        "unit": "V",
        "device_class": "voltage",
        "format_dict": {",": "."}
    },
    "serial_number": {
        "name": "Serial number",
        "endpoint": "getSRN"
    },
    "firmware_version": {
        "name": "Firmware version",
        "endpoint": "getVER"
    },
    "device_type": {
        "name": "Device type",
        "endpoint": "getTYP"
    },
    "mac_address": {
        "name": "MAC Address",
        "endpoint": "getMAC"
    },
    "alarm_status": {
        "name": "Alarm status",
        "endpoint": "getALA",
        "code_dict": ALARM_CODES
    },
    "active_profile": {
        "name": "Active profile",
        "endpoint": "getPRF",
        "code_dict": PROFILE_CODES
    },
    "valve_status": {
        "name": "Valve status",
        "endpoint": "getVLV",
        "code_dict": VALVE_CODES
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
