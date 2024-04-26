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