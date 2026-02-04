import logging
from homeassistant.components.valve import (
    STATE_OPEN,
    STATE_OPENING,
    STATE_CLOSED,
    STATE_CLOSING,
)
from homeassistant.components.valve import (
    ValveEntity,
    ValveEntityFeature,
    ValveDeviceClass,
)
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers import entity_registry as er
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.util import slugify
from homeassistant.core import callback, Event
from .const import DOMAIN

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    # Get device info
    device_info = hass.data[DOMAIN]["entries"][entry.entry_id]["device_info"]

    # Instantiate the PontosValve entity
    valve_entity = PontosValve(hass, entry, device_info)

    # Add the entity to Home Assistant
    async_add_entities([valve_entity], True)


class PontosValve(ValveEntity):
    """Representation of the Pontos Valve entity."""

    def __init__(self, hass, entry, device_info):
        """Initialize the Pontos Valve."""
        self._hass = hass
        self._entry = entry
        self._attr_translation_key = "water_supply"
        self._attr_has_entity_name = True
        self._attr_unique_id = slugify(f"{device_info['serial_number']}_water_supply")
        self._attr_reports_position = False
        self._attr_device_class = ValveDeviceClass.WATER
        self._state = None
        self._device_info = device_info
        self._sensor_unique_id = slugify(f"{device_info['serial_number']}_valve_status")

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()

        # Get the entity ID of the sensor using the unique ID
        entity_registry = er.async_get(self.hass)
        sensor_entity_id = entity_registry.async_get_entity_id(
            "sensor", DOMAIN, self._sensor_unique_id
        )

        # Fetch the initial state from the sensor entity
        if sensor_entity_id:
            sensor_state = self.hass.states.get(sensor_entity_id)
            initial_state = sensor_state.state if sensor_state else None
            LOGGER.debug(f"Fetched initial valve state from sensor: {initial_state}")
            self.set_state(initial_state)

            # Register state change listener
            LOGGER.debug(f"Registering state change listener for {sensor_entity_id}")
            async_track_state_change_event(
                self.hass, sensor_entity_id, self._sensor_state_changed
            )
        else:
            LOGGER.error(f"Sensor with unique ID {self._sensor_unique_id} not found")

    def set_state(self, state):
        """Set the valve state and update Home Assistant."""
        self._state = state
        self.async_write_ha_state()

    @callback
    def _sensor_state_changed(self, event: Event) -> None:
        new_state = event.data.get("new_state")
        if new_state is not None:
            self.set_state(new_state.state)

    @property
    def is_open(self):
        return self._state == STATE_OPEN

    @property
    def is_closed(self):
        return self._state == STATE_CLOSED

    @property
    def is_opening(self):
        return self._state == STATE_OPENING

    @property
    def is_closing(self):
        return self._state == STATE_CLOSING

    @property
    def available(self):
        return self._state != STATE_UNAVAILABLE

    @property
    def supported_features(self):
        """Return the features supported by this valve."""
        return ValveEntityFeature.OPEN | ValveEntityFeature.CLOSE

    @property
    def unique_id(self):
        """Return the unique ID of the valve."""
        return self._attr_unique_id

    @property
    def device_info(self):
        """Return device info to link this entity with the device."""
        return {
            "identifiers": self._device_info["identifiers"],
        }

    async def async_open_valve(self, **kwargs):
        await self._hass.services.async_call(
            DOMAIN, "open_valve", service_data={"entry_id": self._entry.entry_id}
        )

    async def async_close_valve(self, **kwargs):
        await self._hass.services.async_call(
            DOMAIN, "close_valve", service_data={"entry_id": self._entry.entry_id}
        )
