"""Coordinator pro HZSULK Events - stahování dat z API."""

from datetime import UTC, datetime, timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
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
        now = datetime.now(UTC)
        time_from = now - timedelta(hours=DEFAULT_HOURS_LOOKBACK)

        # API chce UTC čas s "Z" suffixem
        cas_od = time_from.isoformat().replace("+00:00", "Z")
        cas_do = now.isoformat().replace("+00:00", "Z")

        params: list[tuple[str, str | int]] = [
            ("casOd", cas_od),
            ("casDo", cas_do),
            ("krajId", DEFAULT_REGION_ID),
        ]
        params.extend(("stavIds", stav_id) for stav_id in DEFAULT_STATUS_IDS)

        # Fetch z API
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(API_BASE_URL, params=params, timeout=10) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"API vrátilo status {resp.status}")

                data = await resp.json()
                _LOGGER.debug("Staženo %s eventů z HZSULK API", len(data))
                return data
        except Exception as err:
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
        counts["last_update"] = datetime.now(UTC).isoformat()
        counts["has_active"] = counts["total"] > 0

        _LOGGER.debug(
            "Zpracovano: Pozary=%s, Nehody=%s, Technicka=%s",
            counts["fires"],
            counts["accidents"],
            counts["technical_help"],
        )

        return counts
