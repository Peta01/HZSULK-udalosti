"""Coordinator: stahuje události, filtruje je podle okruhu a doplňuje jednotky."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
import time
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util
from homeassistant.util.location import distance as geo_distance

from .api import HZSULKApi, HZSULKApiError
from .const import (
    CONF_HOURS,
    CONF_ONLY_ACTIVE,
    DEFAULT_HOURS,
    DEFAULT_ONLY_ACTIVE,
    DEFAULT_RADIUS_KM,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    FALLBACK_TYPES,
    MAX_ACTIVE_AGE_HOURS,
    STATUS_IDS_ACTIVE,
    STATUS_IDS_FINISHED,
    TIMEZONE,
    UNITS_MAX_PARALLEL,
    UNITS_REFRESH_SECONDS,
)
from .geo import parse_jtsk

_LOGGER = logging.getLogger(__name__)

# Rezerva při dotazu na API (filtr API a časy v odpovědi nejsou ve stejném pásmu)
QUERY_MARGIN = timedelta(hours=3)


@dataclass
class HZSEvent:
    """Jedna událost (zásah) po zpracování."""

    id: int
    reported: datetime | None
    type_id: int | None
    type_name: str | None
    subtype_id: int | None
    subtype_name: str | None
    status_id: int | None
    status_name: str | None
    active: bool
    description: str | None
    district: str | None
    municipality: str | None
    municipality_part: str | None
    orp: str | None
    street: str | None
    road: str | None
    latitude: float
    longitude: float
    distance_km: float
    units: list[dict[str, Any]] = field(default_factory=list)

    @property
    def title(self) -> str:
        """Krátký název, např. „Požár – nízké budovy, Šluknov“."""
        kind = _cap(self.type_name) or "Událost"
        if self.subtype_name and self.subtype_name.upper() != (self.type_name or "").upper():
            kind = f"{kind} – {self.subtype_name.lower()}"
        place = self.municipality
        part = self.municipality_part
        # Část obce jen tehdy, když ji upřesňuje (např. „Děčín VI-Letná“)
        if part and (not place or (place in part and part != place)):
            place = part
        return f"{kind}, {place}" if place else kind

    @property
    def address(self) -> str:
        """Adresa ve tvaru „Obec, část, ulice/silnice, okres …“."""
        parts: list[str] = []
        for part in (self.municipality, self.municipality_part, self.street, self.road):
            if part and part not in parts:
                parts.append(part)
        if self.district:
            parts.append(f"okres {self.district}")
        return ", ".join(parts)


def _cap(value: str | None) -> str | None:
    return value.capitalize() if value else value


def _str(value: Any) -> str | None:
    if value is None:
        return None
    value = str(value).strip()
    return value or None


class HZSULKDataUpdateCoordinator(DataUpdateCoordinator[dict[int, HZSEvent]]):
    """Stahuje události v okruhu kolem zadaného místa."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_UPDATE_INTERVAL),
        )
        self.api = HZSULKApi(async_get_clientsession(hass))
        settings = {**entry.data, **entry.options}
        self.latitude: float = settings[CONF_LATITUDE]
        self.longitude: float = settings[CONF_LONGITUDE]
        self.radius_km: float = settings.get(CONF_RADIUS, DEFAULT_RADIUS_KM)
        self.hours: int = settings.get(CONF_HOURS, DEFAULT_HOURS)
        self.only_active: bool = settings.get(CONF_ONLY_ACTIVE, DEFAULT_ONLY_ACTIVE)

        self._tz = dt_util.get_time_zone(TIMEZONE)
        self._types: dict[int, str] = {}
        self._subtypes: dict[int, str] = {}
        self._statuses: dict[int, str] = {}
        # id události -> (čas stažení, byla při stažení ukončená, technika)
        self._units_cache: dict[int, tuple[float, bool, list[dict[str, Any]]]] = {}

    async def _async_load_codebooks(self) -> None:
        """Načti číselníky (jednou, při chybě se zkusí při další aktualizaci)."""
        if self._types and self._subtypes and self._statuses:
            return
        try:
            self._types, self._subtypes, self._statuses = await asyncio.gather(
                self.api.codebook("typy"),
                self.api.codebook("podtypy"),
                self.api.codebook("stavy"),
            )
        except HZSULKApiError as err:
            _LOGGER.warning("Nepodařilo se načíst číselníky HZSULK: %s", err)

    async def _async_update_data(self) -> dict[int, HZSEvent]:
        await self._async_load_codebooks()

        now = dt_util.utcnow()
        window_from = now - timedelta(hours=self.hours)
        query_from = now - timedelta(hours=max(self.hours, MAX_ACTIVE_AGE_HOURS)) - QUERY_MARGIN
        status_ids = STATUS_IDS_ACTIVE + ([] if self.only_active else STATUS_IDS_FINISHED)

        try:
            raw_events = await self.api.events(query_from, now + QUERY_MARGIN, status_ids)
        except HZSULKApiError as err:
            raise UpdateFailed(f"Chyba komunikace s HZSULK API: {err}") from err

        events: dict[int, HZSEvent] = {}
        for raw in raw_events:
            event = self._parse_event(raw)
            if event is None or event.distance_km > self.radius_km:
                continue
            # Ukončené události jen z časového okna, probíhající vždy
            if not event.active and (event.reported is None or event.reported < window_from):
                continue
            events[event.id] = event

        await self._async_fill_units(events)
        _LOGGER.debug(
            "HZSULK: %s událostí v kraji, %s v okruhu %s km", len(raw_events), len(events),
            self.radius_km,
        )
        return events

    def _parse_event(self, raw: dict[str, Any]) -> HZSEvent | None:
        try:
            event_id = int(raw["id"])
        except (KeyError, TypeError, ValueError):
            return None
        coords = parse_jtsk(raw.get("gis1"), raw.get("gis2"))
        if coords is None:
            return None
        lat, lon = coords
        dist = geo_distance(self.latitude, self.longitude, lat, lon)
        if dist is None:
            return None

        reported = None
        if raw.get("casOhlaseni"):
            try:
                reported = datetime.fromisoformat(raw["casOhlaseni"])
                if reported.tzinfo is None:
                    reported = reported.replace(tzinfo=self._tz)
            except ValueError:
                reported = None

        type_id = raw.get("typId")
        subtype_id = raw.get("podtypId")
        status_id = raw.get("stavId")
        okres = raw.get("okres") or {}
        return HZSEvent(
            id=event_id,
            reported=reported,
            type_id=type_id,
            type_name=self._types.get(type_id) or FALLBACK_TYPES.get(type_id),
            subtype_id=subtype_id,
            subtype_name=self._subtypes.get(subtype_id),
            status_id=status_id,
            status_name=self._statuses.get(status_id),
            active=status_id in STATUS_IDS_ACTIVE,
            description=_str(raw.get("poznamkaProMedia")),
            district=_str(okres.get("nazev")) if isinstance(okres, dict) else None,
            municipality=_str(raw.get("obec")),
            municipality_part=_str(raw.get("castObce")),
            orp=_str(raw.get("ORP")),
            street=_str(raw.get("ulice")),
            road=_str(raw.get("silnice")),
            latitude=round(lat, 6),
            longitude=round(lon, 6),
            distance_km=round(dist / 1000, 1),
        )

    async def _async_fill_units(self, events: dict[int, HZSEvent]) -> None:
        """Doplň jednotky a techniku; ukončené události se stahují jen jednou."""
        for stale_id in set(self._units_cache) - set(events):
            del self._units_cache[stale_id]

        now = time.monotonic()
        to_fetch = []
        for event in events.values():
            cached = self._units_cache.get(event.id)
            if cached is None:
                to_fetch.append(event)
                continue
            fetched_at, was_finished, _ = cached
            if not was_finished and (not event.active or now - fetched_at > UNITS_REFRESH_SECONDS):
                to_fetch.append(event)

        semaphore = asyncio.Semaphore(UNITS_MAX_PARALLEL)

        async def fetch(event: HZSEvent) -> None:
            async with semaphore:
                try:
                    units = await self.api.units(event.id)
                except HZSULKApiError as err:
                    _LOGGER.debug("Technika k události %s: %s", event.id, err)
                    return
            self._units_cache[event.id] = (time.monotonic(), not event.active, units)

        if to_fetch:
            await asyncio.gather(*(fetch(event) for event in to_fetch))

        for event in events.values():
            if cached := self._units_cache.get(event.id):
                event.units = cached[2]
