import logging
from homeassistant.components.select import SelectEntity
from homeassistant.util import slugify
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers import entity_registry as er
from homeassistant.const import STATE_UNAVAILABLE

from .const import DOMAIN, CONF_MAKE, CONF_IP_ADDRESS, MAKES
from .profile_select import PontosProfileSelect

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up select entities from config."""
    make = entry.data.get(CONF_MAKE)
    device_const = MAKES[make]
    SELECTORS = device_const.SELECTORS

    device_info = hass.data[DOMAIN]["entries"][entry.entry_id]["device_info"]
    entities = []

    for key, config in SELECTORS.items():
        select_type = config.get("type", "default")

        if select_type == "profile_select":
            entities.append(PontosProfileSelect(hass, entry, device_info))
        else:
            entities.append(PontosDropdownSelect(hass, entry, device_info, key, config))

    async_add_entities(entities, True)


class PontosDropdownSelect(SelectEntity):
    def __init__(self, hass, entry, device_info, key, config):
        self._hass = hass
        self._entry = entry
        self._device_info = device_info
        self._key = key
        self._config = config
        self._sensor = config["sensor"]
        self._service = config["service"]
        self._options_dict = config["options"]  # code -> raw sensor value
        self._code_to_raw_map = self._options_dict  # code -> raw string
        self._raw_to_code_map = {
            v: k for k, v in self._code_to_raw_map.items()
        }  # raw -> code
        self._sensor_unique_id = slugify(
            f"{device_info['serial_number']}_{self._sensor}"
        )
        self._attr_entity_category = config.get("entity_category", None)
        self._attr_translation_key = key
        self._attr_has_entity_name = True
        self._attr_unique_id = slugify(f"{device_info['serial_number']}_{key}_select")
        self._attr_options = list(
            self._code_to_raw_map.values()
        )  # raw values as options
        self._attr_current_option = None
        self._available = True
        self._sensor_entity_id = None

    async def async_added_to_hass(self):
        registry = er.async_get(self._hass)
        self._sensor_entity_id = registry.async_get_entity_id(
            "sensor", DOMAIN, self._sensor_unique_id
        )

        if self._sensor_entity_id:
            state = self._hass.states.get(self._sensor_entity_id)
            if state:
                self._available = state.state != STATE_UNAVAILABLE
                if self._available:
                    self._update_current_option(state.state)

            async_track_state_change_event(
                self._hass, self._sensor_entity_id, self._sensor_state_changed
            )
        else:
            _LOGGER.warning(
                f"Sensor for {self._key} not found: {self._sensor_unique_id}"
            )
            self._available = False

        self.async_write_ha_state()

    @callback
    def _sensor_state_changed(self, event):
        new_state = event.data.get("new_state")
        if new_state is not None:
            self._available = new_state.state != STATE_UNAVAILABLE
            if self._available:
                self._update_current_option(new_state.state)
            self.async_write_ha_state()

    def _update_current_option(self, state_value):
        try:
            code = int(state_value)
        except (ValueError, TypeError):
            code = self._raw_to_code_map.get(str(state_value).strip())

        if code is None:
            _LOGGER.warning(f"{self._key} state value '{state_value}' not in options")
            return

        raw_value = self._code_to_raw_map.get(code)
        if raw_value and raw_value != self._attr_current_option:
            _LOGGER.debug(f"{self._key} updated to '{raw_value}'")
            self._attr_current_option = raw_value
            self.async_write_ha_state()

    async def async_select_option(self, option: str):
        code = self._raw_to_code_map.get(option)
        if code is None:
            _LOGGER.warning(f"No matching code for option: {option}")
            return

        _LOGGER.info(f"Select option chosen: {option} → {code}")
        await self._hass.services.async_call(
            DOMAIN,
            self._service,
            {
                "ip_address": self._entry.options[CONF_IP_ADDRESS],
                "data": code,
            },
        )
        self._attr_current_option = option
        self.async_write_ha_state()

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def device_info(self):
        return {
            "identifiers": self._device_info["identifiers"],
        }

    @property
    def available(self):
        return self._available
