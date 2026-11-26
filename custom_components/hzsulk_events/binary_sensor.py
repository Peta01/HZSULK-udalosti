"""Binární senzor: probíhá v okolí zásah?"""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HZSULKConfigEntry
from .const import ATTRIBUTION, DOMAIN, WEB_URL
from .coordinator import HZSULKDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HZSULKConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Nastav binární senzor."""
    async_add_entities([HZSULKActiveBinarySensor(entry.runtime_data)])


class HZSULKActiveBinarySensor(CoordinatorEntity[HZSULKDataUpdateCoordinator], BinarySensorEntity):
    """Zapnuto, pokud v okruhu probíhá alespoň jedna událost."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True
    _attr_translation_key = "active_incident"
    _attr_icon = "mdi:fire-truck"

    def __init__(self, coordinator: HZSULKDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        entry = coordinator.config_entry
        self._attr_unique_id = f"{entry.entry_id}_active_incident"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="HZS Ústeckého kraje",
            entry_type=DeviceEntryType.SERVICE,
            configuration_url=WEB_URL,
        )

    def _active(self) -> list:
        return [e for e in (self.coordinator.data or {}).values() if e.active]

    @property
    def is_on(self) -> bool:
        return bool(self._active())

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        active = sorted(self._active(), key=lambda e: e.distance_km)
        return {
            "active_count": len(active),
            "events_count": len(self.coordinator.data or {}),
            "radius_km": self.coordinator.radius_km,
            "active_events": [
                {
                    "title": e.title,
                    "distance_km": e.distance_km,
                    "status": e.status_name,
                    "reported": e.reported.isoformat() if e.reported else None,
                }
                for e in active
            ],
        }
