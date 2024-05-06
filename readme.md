# hass-pontos

HACS integration for Hansgrohe Pontos

# Installation

1. Install HACS if you haven't already (see [installation guide](https://hacs.xyz/docs/configuration/basic/)).
2. Add custom repository https://github.com/sangvikh/hass-pontos as "Integration" in the settings tab of HACS.
3. Find and install Hansgrohe Pontos integration in HACS's "Integrations" tab.
4. Restart Home Assistant.
5. Go to your integrations page and click Add Integration and look for Hansgrohe Pontos.
6. Set up sensor using IP address of your pontos, fixed ip is reccomended

# Known issues

- Removing and then adding integration does not work without a restart inbetween. Sensors are not unregistered properly.

# TODO

- [ ] Add services
- [ ] Add water valve button
- [ ] Read profile names
- [ ] Include in HACS