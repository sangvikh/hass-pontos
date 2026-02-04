# custom_components/hass_pontos/button.py
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.util import slugify
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers import entity_registry as er
from homeassistant.const import STATE_UNAVAILABLE

from .const import DOMAIN, MAKES, CONF_MAKE

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    make = entry.data.get(CONF_MAKE)
    device_const = MAKES[make]
    BUTTONS = device_const.BUTTONS

    device_info = hass.data[DOMAIN]["entries"][entry.entry_id]["device_info"]

    buttons = [
        PontosServiceButton(hass, entry, device_info, key, config)
        for key, config in BUTTONS.items()
    ]

    async_add_entities(buttons, True)


class PontosServiceButton(ButtonEntity):
    def __init__(self, hass, entry, device_info, key, config):
        self._hass = hass
        self._entry = entry
        self._device_info = device_info
        self._key = key
        self._config = config
        self._attr_translation_key = key
        self._attr_has_entity_name = True
        self._attr_entity_category = config.get("entity_category", None)
        self._attr_unique_id = slugify(f"{device_info['serial_number']}_{key}")
        self._availability_sensor_unique_id = None
        self._available = True

        availability_sensor_key = config.get("availability_sensor")
        if availability_sensor_key:
            self._availability_sensor_unique_id = slugify(
                f"{device_info['serial_number']}_{availability_sensor_key}"
            )

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        if not self._availability_sensor_unique_id:
            return

        entity_registry = er.async_get(self._hass)
        sensor_entity_id = entity_registry.async_get_entity_id(
            "sensor", DOMAIN, self._availability_sensor_unique_id
        )

        if sensor_entity_id:
            sensor_state = self._hass.states.get(sensor_entity_id)
            self._available = (
                sensor_state.state != STATE_UNAVAILABLE if sensor_state else False
            )
            self.async_write_ha_state()

            async_track_state_change_event(
                self._hass, sensor_entity_id, self._sensor_state_changed
            )
        else:
            LOGGER.warning(
                f"Availability sensor {self._availability_sensor_unique_id} not found"
            )
            self._available = False
            self.async_write_ha_state()

    @callback
    def _sensor_state_changed(self, event):
        new_state = event.data.get("new_state")
        if new_state is not None:
            self._available = new_state.state != STATE_UNAVAILABLE
            self.async_write_ha_state()

    async def async_press(self):
        """Handle button press."""
        service = self._config.get("service")
        if not service:
            LOGGER.error(f"No service defined for button {self._key}")
            return

        LOGGER.info(f"Button pressed: {self._key} → calling service {service}")
        await self._hass.services.async_call(
            DOMAIN,
            service,
            service_data={"entry_id": self._entry.entry_id},
        )

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
