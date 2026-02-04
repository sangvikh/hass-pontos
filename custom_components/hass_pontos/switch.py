import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.util import slugify
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers import entity_registry as er
from homeassistant.const import STATE_UNAVAILABLE

from .const import DOMAIN, CONF_MAKE, MAKES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up switch entities from config."""
    make = entry.data.get(CONF_MAKE)
    device_const = MAKES[make]
    SWITCHES = device_const.SWITCHES

    device_info = hass.data[DOMAIN]["entries"][entry.entry_id]["device_info"]
    entities = [
        PontosSwitch(hass, entry, device_info, key, config)
        for key, config in SWITCHES.items()
    ]

    async_add_entities(entities, True)


class PontosSwitch(SwitchEntity):
    def __init__(self, hass, entry, device_info, key, config):
        self._hass = hass
        self._entry = entry
        self._device_info = device_info
        self._key = key
        self._config = config
        self._sensor = config["sensor"]
        self._service_on = config["service_on"]
        self._service_off = config["service_off"]
        self._sensor_unique_id = slugify(
            f"{device_info['serial_number']}_{self._sensor}"
        )
        self._attr_entity_category = config.get("entity_category", None)
        self._attr_translation_key = key
        self._attr_has_entity_name = True
        self._attr_unique_id = slugify(f"{device_info['serial_number']}_{key}_switch")
        self._state = None
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
                    self._update_state(state.state)

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
                self._update_state(new_state.state)
            self.async_write_ha_state()

    def _update_state(self, state_value):
        value_str = str(state_value).lower()
        self._state = value_str in ("true", "on", "1")

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        _LOGGER.info(f"Turning on switch: {self._key}")
        await self._hass.services.async_call(
            DOMAIN,
            self._service_on,
            {"entry_id": self._entry.entry_id},
        )

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        _LOGGER.info(f"Turning off switch: {self._key}")
        await self._hass.services.async_call(
            DOMAIN,
            self._service_off,
            {"entry_id": self._entry.entry_id},
        )

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._state

    @property
    def available(self):
        """Return if the switch is available."""
        return self._available

    @property
    def unique_id(self):
        """Return the unique ID of the switch."""
        return self._attr_unique_id

    @property
    def device_info(self):
        """Return device info to link this entity with the device."""
        return {
            "identifiers": self._device_info["identifiers"],
        }
