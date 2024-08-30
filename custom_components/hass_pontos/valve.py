import logging
from homeassistant.components.valve import ValveEntity, ValveEntityFeature, ValveDeviceClass
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.core import callback, Event
from .device import get_device_info
from .const import DOMAIN, VALVE_STATUS_SENSOR

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the valve entity."""
    device_info, data = await get_device_info(hass, entry)

    # Fetch initial state from the sensor entity
    sensor_state = hass.states.get(VALVE_STATUS_SENSOR)
    initial_state = sensor_state.state if sensor_state else None

    # Instantiate the PontosValve entity
    valve_entity = PontosValve(hass, entry, device_info)

    # Add the entity to Home Assistant
    async_add_entities([valve_entity], True)

    # Set initial state
    valve_entity.set_state(initial_state)

class PontosValve(ValveEntity):
    """Representation of the Pontos Valve entity."""

    def __init__(self, hass, entry, device_info):
        """Initialize the Pontos Valve."""
        self._hass = hass
        self._entry = entry
        self._attr_name = f"{device_info['name']} Water supply"
        self._attr_unique_id = f"{device_info['serial_number']}_water_supply"
        self._attr_reports_position = False
        self._attr_device_class = ValveDeviceClass.WATER
        self._state = None
        self._device_info = device_info

    def set_state(self, state):
        self._state = state
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()
        async_track_state_change_event(
            self.hass,
            VALVE_STATUS_SENSOR,
            self._sensor_state_changed
        )

    @callback
    def _sensor_state_changed(self, event: Event) -> None:
        new_state = event.data.get('new_state')
        if new_state is not None:
            self.set_state(new_state.state)

    @property   
    def state(self):
        """Return the current state of the valve."""
        return self._state

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
            "identifiers": self._device_info['identifiers'],
        }

    def open_valve(self) -> None:
        """Synchronously open the valve."""
        # Execute the async function within the event loop
        self._hass.add_job(self.async_open)

    def close_valve(self) -> None:
        """Synchronously close the valve."""
        # Execute the async function within the event loop
        self._hass.add_job(self.async_close)

    async def async_open(self) -> None:
        """Asynchronously open the valve."""
        await self._hass.services.async_call(
            DOMAIN, 
            "open_valve",
            service_data={"entry_id": self._entry.entry_id}
        )

    async def async_close(self) -> None:
        """Asynchronously close the valve."""
        await self._hass.services.async_call(
            DOMAIN, 
            "close_valve",
            service_data={"entry_id": self._entry.entry_id}
        )
