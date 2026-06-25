"""Sensors pro HZSULK Events."""

import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
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
    """Set up HZSULK Events sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        HZSULKFiresCountSensor(coordinator, entry),
        HZSULKAccidentsCountSensor(coordinator, entry),
        HZSULKHazmatCountSensor(coordinator, entry),
        HZSULKTechnicalHelpCountSensor(coordinator, entry),
        HZSULKRescuesCountSensor(coordinator, entry),
        HZSULKFalseAlarmsCountSensor(coordinator, entry),
        HZSULKOtherCountSensor(coordinator, entry),
        HZSULKTotalIncidentsSensor(coordinator, entry),
        HZSULKLastUpdateSensor(coordinator, entry),
    ]

    async_add_entities(entities, update_before_add=True)


class HZSULKSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for HZSULK sensors."""

    _attr_attribution = "Data from HZSULK (udalosti.hzsulk.cz)"
    _attr_native_unit_of_measurement = "events"

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        key: str,
        name: str,
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def native_value(self):
        """Return the state."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._key)


class HZSULKFiresCountSensor(HZSULKSensorBase):
    """Počet požárů."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator, entry, "fires", "HZSULK Požáry")


class HZSULKAccidentsCountSensor(HZSULKSensorBase):
    """Počet dopravních nehod."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator, entry, "accidents", "HZSULK Dopravní nehody")


class HZSULKHazmatCountSensor(HZSULKSensorBase):
    """Počet úniků nebezpečných látek."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator, entry, "hazmat", "HZSULK Únik nebezpečných látek")


class HZSULKTechnicalHelpCountSensor(HZSULKSensorBase):
    """Počet technických pomoc."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator, entry, "technical_help", "HZSULK Technická pomoc")


class HZSULKRescuesCountSensor(HZSULKSensorBase):
    """Počet záchrany osob a zvířat."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator, entry, "rescues", "HZSULK Záchrana osob a zvířat")


class HZSULKFalseAlarmsCountSensor(HZSULKSensorBase):
    """Počet falešných poplachů."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator, entry, "false_alarms", "HZSULK Falešné poplachy")


class HZSULKOtherCountSensor(HZSULKSensorBase):
    """Počet ostatních eventů."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator, entry, "other", "HZSULK Ostatní")


class HZSULKTotalIncidentsSensor(HZSULKSensorBase):
    """Celkový počet incidentů."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator, entry, "total", "HZSULK Celkem incidentů")


class HZSULKLastUpdateSensor(CoordinatorEntity, SensorEntity):
    """Poslední aktualizace."""

    _attr_attribution = "Data from HZSULK (udalosti.hzsulk.cz)"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "HZSULK Poslední aktualizace"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_last_update"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def native_value(self):
        """Return the state."""
        if self.coordinator.data is None:
            return None

        value = self.coordinator.data.get("last_update")
        if not value:
            return None

        if isinstance(value, datetime):
            return value

        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
