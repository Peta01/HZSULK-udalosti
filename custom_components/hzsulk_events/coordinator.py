"""Coordinator pro HZSULK Events - stahování dat z API."""

from datetime import datetime, timedelta
import logging
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_BASE_URL,
    DOMAIN,
    DEFAULT_REGION_ID,
    DEFAULT_STATUS_IDS,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_HOURS_LOOKBACK,
    EVENT_TYPE_FIRE,
    EVENT_TYPE_ACCIDENT,
    EVENT_TYPE_HAZMAT,
    EVENT_TYPE_TECHNICAL_HELP,
    EVENT_TYPE_RESCUE,
    EVENT_TYPE_FALSE_ALARM,
    EVENT_TYPE_OTHER,
)

_LOGGER = logging.getLogger(__name__)


class HZSULKDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator pro stahování HZSULK events dat."""

    def __init__(self, hass: HomeAssistant):
        """Inicializace coordinatoru."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_UPDATE_INTERVAL),
        )
        self.hass = hass

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data z HZSULK API."""
        try:
            data = await self._fetch_events()
            return self._process_events(data)
        except Exception as err:
            raise UpdateFailed(f"Error komunikace s HZSULK API: {err}") from err

    async def _fetch_events(self) -> list[dict]:
        """Stáhni events z API."""
        # Časový rozsah: poslednich 24 hodin
        now = datetime.utcnow()
        time_from = now - timedelta(hours=DEFAULT_HOURS_LOOKBACK)

        # ISO 8601 format
        cas_od = time_from.isoformat() + "Z"
        cas_do = now.isoformat() + "Z"

        # Vytvář URL s parametry
        # stavIds mají být vícekrát
        url = API_BASE_URL
        query_parts = [
            f"casOd={cas_od}",
            f"casDo={cas_do}",
            f"krajId={DEFAULT_REGION_ID}",
        ]

        # Přidej stavIds
        for stav_id in DEFAULT_STATUS_IDS:
            query_parts.append(f"stavIds={stav_id}")

        query_string = "&".join(query_parts)
        full_url = f"{url}?{query_string}"

        _LOGGER.debug(f"API request: {full_url}")

        # Fetch z API
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(full_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        _LOGGER.debug(f"Staženo {len(data)} eventů z HZSULK API")
                        return data
                    else:
                        raise UpdateFailed(f"API vrátilo status {resp.status}")
            except aiohttp.ClientError as err:
                raise UpdateFailed(f"Chyba v komunikaci s API: {err}") from err

    def _process_events(self, events: list[dict]) -> dict[str, Any]:
        """Zpracuj raw events do agregovaného formátu."""
        counts = {
            "fires": 0,
            "accidents": 0,
            "hazmat": 0,
            "technical_help": 0,
            "rescues": 0,
            "false_alarms": 0,
            "other": 0,
            "total": len(events),
        }

        # Agreguj podle typId
        for event in events:
            typ_id = event.get("typId")

            if typ_id == EVENT_TYPE_FIRE:
                counts["fires"] += 1
            elif typ_id == EVENT_TYPE_ACCIDENT:
                counts["accidents"] += 1
            elif typ_id == EVENT_TYPE_HAZMAT:
                counts["hazmat"] += 1
            elif typ_id == EVENT_TYPE_TECHNICAL_HELP:
                counts["technical_help"] += 1
            elif typ_id == EVENT_TYPE_RESCUE:
                counts["rescues"] += 1
            elif typ_id == EVENT_TYPE_FALSE_ALARM:
                counts["false_alarms"] += 1
            elif typ_id in EVENT_TYPE_OTHER:
                counts["other"] += 1

        # Přidej raw events
        counts["events"] = events
        counts["last_update"] = datetime.utcnow().isoformat()
        counts["has_active"] = counts["total"] > 0

        _LOGGER.debug(f"Zpracovano: Požáry={counts['fires']}, Nehody={counts['accidents']}, Technická={counts['technical_help']}")

        return counts
