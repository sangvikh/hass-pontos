# hass-pontos

[![GitHub Release](https://img.shields.io/github/release/sangvikh/hass-pontos.svg?style=flat)](https://github.com/sangvikh/hass-pontos/releases)
[![hassfest](https://img.shields.io/github/actions/workflow/status/sangvikh/hass-pontos/hassfest.yaml?branch=master&label=hassfest)](https://github.com/sangvikh/hass-pontos/actions/workflows/hassfest.yaml)
[![HACS](https://img.shields.io/github/actions/workflow/status/sangvikh/hass-pontos/validate.yaml?branch=master&label=HACS)](https://github.com/sangvikh/hass-pontos/actions/workflows/validate.yaml)

HACS integration for Hansgrohe Pontos and SYR water meters

## Features

* Adds sensors for water consumption, water pressure, water temperature +++
* Monitors NeoSoft-specific values such as salt level and regeneration state
* Opening/Closing of water valve

## Supported devices

* Hansgrohe Pontos
* SYR Trio
* SYR SafeTech+
* SYR NeoSoft

## Installation

**Recommended:** Install via HACS

### HACS

1. Install [HACS](https://hacs.xyz/docs/configuration/basic/) if needed.
2. In HACS, search for and install the "Hansgrohe Pontos" integration.
3. Restart Home Assistant.
4. Add the integration via Home Assistant's Integrations page and follow the configuration steps.

### Manual installation

1. Download or clone this repository.
2. Copy `custom_components/hass_pontos` to your Home Assistant `custom_components` directory.
3. Restart Home Assistant.
4. Add the integration via Home Assistant's Integrations page and follow the configuration steps.
