# A collection of documentation for the API's

- Hansgrohe Pontos REST API from:
https://community.home-assistant.io/t/hansgrohe-pontos-syr-safe-tech/576178

- Hansgrohe Pontos API found at:
https://community.symcon.de/t/hansgrohe-pontosbase/128469/6

- SYR API found at, translated to english:
https://iotsyrpublicapi.z1.web.core.windows.net/#support-hilfestellung

# Integration features

## Sensors

The integration provides the following sensors in Home Assistant:

| Sensor Name                | Description                        | Unit      |
|----------------------------|------------------------------------|-----------|
| Total water consumption    | Total water used                   | L         |
| Water pressure             | Current water pressure             | bar       |
| Water temperature          | Current water temperature          | °C        |
| Current water consumption  | Current water draw                 | L         |
| Time since last turbine pulse | Time since last water flow      | s         |
| Leak test pressure drop    | Pressure drop during leak test     | bar       |
| Wifi state                 | WiFi connection status             |           |
| Wifi signal strength       | WiFi signal strength               | %         |
| Battery voltage            | Battery voltage                    | V         |
| Mains voltage              | Mains voltage                      | V         |
| Serial number              | Device serial number               |           |
| Firmware version           | Device firmware version            |           |
| Device type                | Device type                        |           |
| MAC address                | MAC address                        |           |
| Alarm status               | Current alarm status               |           |
| Active profile             | Currently active profile           |           |
| Valve status               | Current valve status               |           |
| Water conductivity         | Water conductivity                 | µS/cm     |
| Water hardness             | Water hardness                     | dH        |
| Raw water hardness         | Inlet water hardness               | °dH       |
| Treated water hardness     | Outlet water hardness              | °dH       |
| Salt quantity              | Remaining salt in the brine tank   | kg        |
| Salt stock                 | Remaining duration of salt         | weeks     |
| Regeneration status        | Current regeneration status        |           |
| Regeneration time remaining| Remaining regeneratio time         | s         |
| Microleakage test interval | Microleakage test schedule         |           |
| Profile 1-8 name           | Name of each profile               |           |

*Note: Available sensors may depend on your device model.*

## Services

The integration provides the following Home Assistant services:

| Service Name                | Description                                      |
|-----------------------------|--------------------------------------------------|
| `hass_pontos.open_valve`    | Opens the water valve                            |
| `hass_pontos.close_valve`   | Closes the water valve                           |
| `hass_pontos.clear_alarms`  | Clears any active alarms                         |
| `hass_pontos.set_profile`   | Sets the active profile (1-8)                    |
| `hass_pontos.microleakage_test` | Starts a microleakage test                  |
| `hass_pontos.microleakage_time` | Sets the time for the microleakage test     |
| `hass_pontos.microleakage_schedule` | Sets the schedule for microleakage test |
| `hass_pontos.set_regeneration_mode` | Switches the NeoSoft regeneration mode |
| `hass_pontos.generic_service` | Sends a custom command to the device           |

*Note: Available services may depend on your device model.*

### Generic service call

The generic service call allows you to send commands to the device using the `/set` endpoints. This is useful for accessing features not covered by predefined services.

Example for changing profile to 1:
- Endpoint: prf
- Data: 1

Change maximum water draw for profile 2 to 250 l:
- Endpoint: pv2
- Data: 250

#### Commands Overview (Based on SYR documentation)

| **Endpoint** | **Type**       | **Description**                                      | **Value Range**       | **GET** | **SET** |
|-------------|----------------|------------------------------------------------------|------------------------|---------|---------|
| **AB**      | Bool           | Locking opening/closing                              | true/false            | ✓       | ✓       |
| **VLV**     | int            | Status of the shut-off                               | 10-21                 | ✓       | X       |
| **PAx**     | Bool           | Profile Availability                                 | true/false            | ✓       | ✓       |
| **PVx**     | int            | Profile permitted volume in liters                  | 0-9000                | ✓       | ✓       |
| **PTx**     | int            | Profile allowed time in minutes                     | 0-1500                | ✓       | ✓       |
| **PFx**     | int            | Profile permitted flow in l/h                       | 0-5000                | ✓       | ✓       |
| **PMx**     | Bool           | Micro leak test Activating/deactivating             | true/false            | ✓       | ✓       |
| **PWx**     | Bool           | Activation/deactivate leakage warning               | true/false            | ✓       | ✓       |
| **PBx**     | Bool           | Buzzer Activating/deactivating                      | true/false            | ✓       | ✓       |
| **PRx**     | int            | Return to Profile Present in hours                  | 0-700                 | ✓       | ✓       |
| **PRF**     | int            | Currently selected profile                          | 1-8                   | ✓       | ✓       |
| **DEX**     | Bool           | Starts the MicroLeakage Test                        | true                  | X       | ✓       |
| **DRP**     | int            | Set the test interval                               | 1-3                   | ✓       | ✓       |
| **DSV**     | int            | Status of the micro leakage                         | 0-3                   | ✓       | X       |
| **DTT**     | string         | Sets the time when the test is performed            | "HH:MM"               | ✓       | ✓       |
| **SLP**     | int            | Starts the self-study phase with duration in days   | 0-28                  | ✓       | ✓       |
| **SLV**     | int            | Determined volume in L during the self-study phase  | 0-9000                | ✓       | X       |
| **SLT**     | int            | Determined time in seconds during self-study phase  | 0-90000               | ✓       | X       |
| **SLF**     | int            | Determined flow rate in l/h during self-study phase | 0-5000                | ✓       | X       |
| **SLD**     | Bool           | Deletes the values when true is sent                | true                  | X       | ✓       |
| **SLE**     | int            | Remaining time in the active self-learning phase    | 0-2419200             | ✓       | X       |
| **WFC**     | string         | WLAN SSID                                           | true                  | ✓       | ✓       |
| **WFD**     | -              | SSID and Key Delete                                 | -                     | ✓       | ✓       |
| **WFK**     | string         | WiFi Key                                            | -                     | X       | ✓       |
| **WFL**     | json           | Provides a list of available networks              | -                     | ✓       | X       |
| **WFR**     | int            | WLAN signal strength in %                           | 1-100                 | ✓       | X       |
| **WFS**     | int            | WLAN connection status                              | 0-2                   | ✓       | X       |
| **WGW**     | string         | WLAN IP                                             | -                     | ✓       | X       |
| **WIP**     | string         | WLAN Gateway                                        | -                     | ✓       | X       |
| **EGW**     | string         | Ethernet IP                                         | -                     | ✓       | X       |
| **EIP**     | string         | Ethernet Gateway                                    | -                     | ✓       | X       |
| **MAC1**    | string         | MAC address WLAN interface                          | -                     | ✓       | X       |
| **MAC2**    | string         | MAC address LAN interface                           | -                     | ✓       | X       |
| **AVO**     | int            | Volume current removal in ml                        | -                     | ✓       | X       |
| **BAR**     | int            | Input pressure in mbar                              | 0-16000               | ✓       | X       |
| **BAT**     | int            | Battery voltage in 1/100 V                          | 0-1000                | ✓       | X       |
| **CEL**     | int            | Temperature in °C                                   | 0-1000                | ✓       | X       |
| **CND**     | int            | Conductance in uS/cm                                | 0-5000                | ✓       | X       |
| **FLO**     | int            | Current Flow rate in l/h                            | 0-5000                | ✓       | X       |
| **LTV**     | int            | Last tapped volume in liters                        | -                     | ✓       | X       |
| **NPS**     | int            | No turbine impulses since.. in s                   | -                     | ✓       | X       |
| **SRN**     | string         | Serial number of the device                         | -                     | ✓       | X       |
| **VER**     | string         | Firmware version of the device                      | -                     | ✓       | X       |
| **VOL**     | int            | Cumulative volume in liters                         | -                     | ✓       | X       |