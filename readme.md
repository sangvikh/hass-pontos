# hass-pontos

[![GitHub Release](https://img.shields.io/github/release/sangvikh/hass-pontos.svg?style=flat)](https://github.com/sangvikh/hass-pontos/releases)
[![hassfest](https://img.shields.io/github/actions/workflow/status/sangvikh/hass-pontos/hassfest.yaml?branch=master&label=hassfest)](https://github.com/sangvikh/hass-pontos/actions/workflows/hassfest.yaml)
[![HACS](https://img.shields.io/github/actions/workflow/status/sangvikh/hass-pontos/validate.yaml?branch=master&label=HACS)](https://github.com/sangvikh/hass-pontos/actions/workflows/validate.yaml)

HACS integration for Hansgrohe Pontos and SYR water meters

## Features

* Adds sensors for water consumption, water pressure, water temperature +++
* Opening/Closing of water valve
* Clearing alarms

## Supported devices

* Hansgrohe Pontos
* SYR Trio
* SYR SafeTech+

## Installation

Installation via HACS is the recommended method

### HACS

1. Install HACS if you haven't already (see [installation guide](https://hacs.xyz/docs/configuration/basic/)).
2. Find and install Hansgrohe Pontos integration in HACS's "Integrations" tab.
3. Restart Home Assistant.
4. Go to your integrations page, click Add Integration and look for Hansgrohe Pontos.
5. Set up sensor using the IP address of your device, fixed ip is recommended.

### Manual installation

1. Clone repository or download as zip
2. Move the custom_components/hass_pontos folder to the custom_components directory of your Home Assistant installation
3. Restart Home Assistant.
4. Go to your integrations page, click Add Integration and look for Hansgrohe Pontos.
5. Set up sensor using the IP address of your device, fixed ip is recommended.

## Services

### Generic service call

The generic service call allows you to send commands to the device using the `/set` endpoints. This is useful for accessing features not covered by predefined services.

Example for changing profile to 1:
- Endpoint: prf
- Data: 1

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