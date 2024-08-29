import logging
from homeassistant.components.valve import ValveEntity, ValveEntityFeature, ValveDeviceClass
from homeassistant.helpers.event import async_track_time_interval
from .device import get_device_info
from .const import DOMAIN, VALVE_STATUS_SENSOR, FETCH_INTERVAL

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the valve entity."""
    device_info, _ = await get_device_info(hass, entry)

    # Explicitly instantiate the PontosValve entity
    valve_entity = PontosValve(hass, entry, device_info)

    # Add the entity to Home Assistant
    async_add_entities([valve_entity], True)

    # Schedule periodic updates to check the valve state
    async_track_time_interval(hass, valve_entity.async_update, FETCH_INTERVAL)

class PontosValve(ValveEntity):
    """Representation of the Pontos Valve entity."""

    def __init__(self, hass, entry, device_info):
        """Initialize the Pontos Valve."""
        self._hass = hass
        self._entry = entry
        self._attr_name = f"{device_info['name']} Water Supply"
        self._attr_unique_id = f"{device_info['serial_number']}_water_supply"
        self._attr_reports_position = False
        self._attr_device_class = ValveDeviceClass.WATER
        self._state = None  # Initial state will be set during the first update
        self._device_id = device_info['identifiers']

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
            "identifiers": self._device_id,
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

    async def async_update(self, time_event=None):
        """Update the valve's state from the valve status sensor."""
        sensor_entity_id = f"sensor.{VALVE_STATUS_SENSOR}"

        # Fetch the state of the sensor
        sensor_state = self._hass.states.get(sensor_entity_id)

        if sensor_state:
            self._state = sensor_state.state
        else:
            LOGGER.error(f"Could not find sensor state for {sensor_entity_id}")
            self._state = None  # If sensor state is not found, set to None

        # Write the state to Home Assistant
        if self.entity_id:
            self.async_write_ha_state()
