"""Jednotlivé události HZS ÚK jako geo_location entity (zobrazí se na mapě)."""

from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any

from homeassistant.components.geo_location import GeolocationEvent
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HZSULKConfigEntry
from .const import ATTRIBUTION, DEFAULT_ICON, DOMAIN, SUBTYPE_ICONS, TYPE_ICONS, WEB_URL
from .coordinator import HZSEvent, HZSULKDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

SOURCE = DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HZSULKConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Přidávej a odebírej entity podle aktuálních událostí."""
    coordinator = entry.runtime_data
    registry = er.async_get(hass)
    tracked: dict[int, HZSULKEventEntity] = {}

    # Úklid entit po událostech, které mezitím zmizely (např. po restartu HA)
    current = {_unique_id(entry.entry_id, event_id) for event_id in coordinator.data or {}}
    for reg_entry in er.async_entries_for_config_entry(registry, entry.entry_id):
        if reg_entry.domain == "geo_location" and reg_entry.unique_id not in current:
            registry.async_remove(reg_entry.entity_id)

    @callback
    def _sync() -> None:
        data = coordinator.data or {}
        new = [
            HZSULKEventEntity(coordinator, event_id, _remove_entity)
            for event_id in data
            if event_id not in tracked
        ]
        for entity in new:
            tracked[entity.event_id] = entity
        if new:
            async_add_entities(new)

        for event_id in [eid for eid in tracked if eid not in data]:
            entity = tracked.pop(event_id)
            hass.async_create_task(entity.async_remove_event())

    @callback
    def _remove_entity(entity_id: str) -> None:
        if registry.async_get(entity_id):
            registry.async_remove(entity_id)

    _sync()
    entry.async_on_unload(coordinator.async_add_listener(_sync))


def _unique_id(entry_id: str, event_id: int) -> str:
    return f"{entry_id}_{event_id}"


class HZSULKEventEntity(CoordinatorEntity[HZSULKDataUpdateCoordinator], GeolocationEvent):
    """Jedna událost."""

    _attr_attribution = ATTRIBUTION
    _attr_should_poll = False
    _attr_unit_of_measurement = UnitOfLength.KILOMETERS

    def __init__(
        self,
        coordinator: HZSULKDataUpdateCoordinator,
        event_id: int,
        remove_from_registry: Callable[[str], None],
    ) -> None:
        super().__init__(coordinator)
        self.event_id = event_id
        self._remove_from_registry = remove_from_registry
        self._attr_unique_id = _unique_id(coordinator.config_entry.entry_id, event_id)
        self._event: HZSEvent = coordinator.data[event_id]
        self._apply()

    async def async_remove_event(self) -> None:
        """Odeber entitu i záznam v registru, když událost zmizí."""
        entity_id = self.entity_id
        await self.async_remove(force_remove=True)
        if entity_id:
            self._remove_from_registry(entity_id)

    @callback
    def _handle_coordinator_update(self) -> None:
        event = (self.coordinator.data or {}).get(self.event_id)
        if event is None:
            return  # entitu odebere listener v async_setup_entry
        self._event = event
        self._apply()
        self.async_write_ha_state()

    def _apply(self) -> None:
        event = self._event
        self._attr_name = event.title
        self._attr_icon = SUBTYPE_ICONS.get(event.subtype_id or 0) or TYPE_ICONS.get(
            event.type_id or 0, DEFAULT_ICON
        )
        self._attr_source = SOURCE
        self._attr_latitude = event.latitude
        self._attr_longitude = event.longitude
        self._attr_distance = event.distance_km

    @property
    def available(self) -> bool:
        return super().available and self.event_id in (self.coordinator.data or {})

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        event = self._event
        # Technika seskupená podle jednotek: {"HS Šluknov": ["CAS < 30", "2× DA"]}
        by_unit: dict[str, list[str]] = {}
        for item in event.units:
            unit = item.get("jednotka") or "?"
            vehicles_of_unit = by_unit.setdefault(unit, [])
            vehicle = item.get("typ")
            count = item.get("pocet") or 0
            if vehicle and count > 0:
                vehicles_of_unit.append(f"{count}× {vehicle}" if count > 1 else vehicle)
        units = list(by_unit)
        vehicles = [
            f"{unit}: {', '.join(items)}" if items else unit for unit, items in by_unit.items()
        ]
        return {
            "event_id": event.id,
            "reported": event.reported.isoformat() if event.reported else None,
            "type": event.type_name,
            "subtype": event.subtype_name,
            "status": event.status_name or event.status_id,
            "active": event.active,
            "description": event.description,
            "address": event.address,
            "district": event.district,
            "municipality": event.municipality,
            "municipality_part": event.municipality_part,
            "orp": event.orp,
            "street": event.street,
            "road": event.road,
            "units": units,
            "vehicles": vehicles,
            "url": WEB_URL,
        }
