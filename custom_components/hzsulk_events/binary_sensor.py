"""Binary sensors pro HZSULK Events."""

import logging
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HZSULK Events binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        HZSULKHasActiveIncidentsBinarySensor(coordinator, entry),
    ]

    async_add_entities(entities, update_before_add=True)


class HZSULKHasActiveIncidentsBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Jsou nějaké aktivní incidenty?"""

    _attr_attribution = "Data from HZSULK (udalosti.hzsulk.cz)"
    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY
    _attr_name = "HZSULK Aktivní incidenty"

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_has_active_incidents"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def is_on(self):
        """Return True if any incidents are active."""
        if self.coordinator.data is None:
            return False
        return self.coordinator.data.get("has_active", False)
