"""Klient pro veřejné API udalosti.hzsulk.cz."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import aiohttp

from .const import API_BASE_URL, API_TIMEOUT, REGION_ID


class HZSULKApiError(Exception):
    """Chyba komunikace s API."""


def _iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


class HZSULKApi:
    """Tenký asynchronní klient API."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session

    async def _get(self, path: str, params: list[tuple[str, Any]] | None = None) -> Any:
        try:
            async with self._session.get(
                API_BASE_URL + path,
                params=params,
                headers={"Accept": "application/json"},
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT),
            ) as resp:
                if resp.status != 200:
                    raise HZSULKApiError(f"{path or '/'}: HTTP {resp.status}")
                return await resp.json(content_type=None)
        except (aiohttp.ClientError, TimeoutError) as err:
            raise HZSULKApiError(f"{path or '/'}: {err!r}") from err

    async def events(
        self, time_from: datetime, time_to: datetime, status_ids: list[int]
    ) -> list[dict[str, Any]]:
        """Seznam událostí v kraji za dané období."""
        params: list[tuple[str, Any]] = [
            ("casOd", _iso_utc(time_from)),
            ("casDo", _iso_utc(time_to)),
            ("krajId", REGION_ID),
        ]
        params.extend(("stavIds", sid) for sid in status_ids)
        data = await self._get("", params)
        return data if isinstance(data, list) else []

    async def units(self, event_id: int) -> list[dict[str, Any]]:
        """Zasahující jednotky a technika u události."""
        data = await self._get(f"udalosti/{event_id}/technika")
        return data if isinstance(data, list) else []

    async def codebook(self, name: str) -> dict[int, str]:
        """Číselník (typy, podtypy, stavy, okresy) jako {id: název}."""
        data = await self._get(name)
        if not isinstance(data, list):
            return {}
        return {
            item["id"]: item["nazev"]
            for item in data
            if isinstance(item, dict) and "id" in item and "nazev" in item
        }
