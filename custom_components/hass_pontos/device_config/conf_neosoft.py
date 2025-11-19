from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.sensor import SensorDeviceClass

PLATFORMS = ['sensor', 'button', 'select', 'switch', 'time']

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
    "02": "bi_annual_maintenance",
    "03": "annual_maintenance",
    "04": "new_software_installed",
    "FF": "no_notification"
}

WARNING_CODES = {
    "01": "power_outage",
    "02": "salt_supply_low",
    "07": "leak_warning",
    "08": "battery_low",
    "09": "initial_filling",
    "10": "leak_warning_volume",
    "11": "leak_warning_time",
    "FF": "no_warning"
}

REGEN_STATUS_CODES = {
    "0": "no_regeneration",
    "1": "bottle_1_regenerated",
    "2": "bottle_2_regenerated",
}

REGEN_MODE_CODES = {
    "1": "mode_standard",
    "2": "mode_eco",
    "3": "mode_power",
    "4": "mode_automatic",
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
    "no_pulse_time_1": {
        "name": "No turbine pulses control head 1 since",
        "endpoint": "getVPS1",
        "unit": "s",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "no_pulse_time_2": {
        "name": "No turbine pulses control head 2 since",
        "endpoint": "getVPS2",
        "unit": "s",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "water_flow": {
        "name": "Water flow",
        "endpoint": "getFLO",
        "unit": "L/min",
        "device_class": SensorDeviceClass.VOLUME_FLOW_RATE,
        "scale": 1
    },
    "current_consumption": {
        "name": "Current water consumption",
        "endpoint": "getAVO",
        "unit": "L",
        "device_class": SensorDeviceClass.WATER,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "scale": 0.001
    },
    "last_tapped_volume": {
        "name": "Last tapped volume",
        "endpoint": "getLTV",
        "unit": "L",
        "device_class": SensorDeviceClass.WATER,
        "entity_category": EntityCategory.DIAGNOSTIC,
        "scale": 1
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
    "salt_stock": {
        "name": "Salt stock",
        "endpoint": "getSS1",
        "unit": "weeks"
    },
    "salt_quantity": {
        "name": "Salt quantity",
        "endpoint": "getSV1",
        "unit": "kg"
    },
    "regeneration_mode": {
        "name": "Regeneration mode",
        "endpoint": "getRMO",
        "code_dict": REGEN_MODE_CODES
    },
    "regeneration_status": {
        "name": "Regeneration status",
        "endpoint": "getRG1",
        "code_dict": REGEN_STATUS_CODES,
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "regeneration_time_remaining": {
        "name": "Regeneration time remaining",
        "endpoint": "getRTI",
        "unit": "s",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "reserve_capacity_bottle_1": {
        "name": "Reserve capacity bottle 1",
        "endpoint": "getRE1",
        "unit": "L",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "reserve_capacity_bottle_2": {
        "name": "Reserve capacity bottle 2",
        "endpoint": "getRE2",
        "unit": "L",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "regeneration_schedule": {
        "name": "Regeneration schedule",
        "endpoint": "getRPD",
        "unit": "days",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "regeneration_time": {
        "name": "Regeneration time",
        "endpoint": "getRTM",
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
    "water_conductivity": {
        "name": "Water conductivity",
        "endpoint": "getCND",
        "unit": "µS/cm"
    },
    "next_bi_annual_maintenance": {
        "name": "Next bi-annual maintenance",
        "endpoint": "getSRH",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "next_annual_maintenance": {
        "name": "Next annual maintenance",
        "endpoint": "getSRV",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
    "buzzer_enabled": {
        "name": "Buzzer enabled",
        "endpoint": "getBUZ",
        "entity_category": EntityCategory.DIAGNOSTIC
    },
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
    "clear_warnings": {
        "name": "Clear warnings",
        "endpoint": "set/wrn/255"
    },
    "clear_notifications": {
        "name": "Clear notifications",
        "endpoint": "set/not/255"
    },
    "set_regeneration_mode": {
        "name": "Set regeneration mode",
        "endpoint": "set/rmo/{data}"
    },
    "set_regeneration_interval": {
        "name": "Set regeneration interval",
        "endpoint": "set/rpd/{data}"
    },
    "set_regeneration_time": {
        "name": "Set regeneration time",
        "endpoint": "set/rtm/{data}"
    },
    "enable_buzzer": {
        "name": "Enable buzzer",
        "endpoint": "set/buz/true"
    },
    "disable_buzzer": {
        "name": "Disable buzzer",
        "endpoint": "set/buz/false"
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

SELECTORS = {
    "regeneration_mode": {
        "name": "Regeneration Mode",
        "options": REGEN_MODE_CODES,
        "sensor": "Regeneration Mode",
        "service": "set_regeneration_mode"
    }
}

TIME_ENTRIES = {
    "regeneration_time": {
        "name": "Regeneration time",
        "sensor": "Regeneration time",
        "service": "set_regeneration_time",
        "entity_category": EntityCategory.DIAGNOSTIC
    }
}

SWITCHES = {
    "buzzer": {
        "name": "Buzzer",
        "sensor": "Buzzer enabled",
        "service_on": "enable_buzzer",
        "service_off": "disable_buzzer",
        "entity_category": EntityCategory.DIAGNOSTIC
    }
}