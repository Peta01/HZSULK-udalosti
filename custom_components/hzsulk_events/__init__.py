"""Home Assistant integrace HZSULK Events – zásahy HZS Ústeckého kraje v okolí."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_registry as er
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import async_get_integration

from .const import (
    CARD_FILENAME,
    CONF_HOURS,
    CONF_ONLY_ACTIVE,
    DEFAULT_HOURS,
    DEFAULT_ONLY_ACTIVE,
    DEFAULT_RADIUS_KM,
    DOMAIN,
    FRONTEND_URL,
)
from .coordinator import HZSULKDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.GEO_LOCATION, Platform.BINARY_SENSOR]
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

HZSULKConfigEntry = ConfigEntry[HZSULKDataUpdateCoordinator]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Zaregistruj Lovelace kartu (custom:hzsulk-events-card)."""
    integration = await async_get_integration(hass, DOMAIN)
    await hass.http.async_register_static_paths(
        [StaticPathConfig(FRONTEND_URL, str(Path(__file__).parent / "frontend"), True)]
    )
    add_extra_js_url(hass, f"{FRONTEND_URL}/{CARD_FILENAME}?v={integration.version}")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: HZSULKConfigEntry) -> bool:
    """Nastav integraci z config entry."""
    coordinator = HZSULKDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_reload))
    return True


async def _async_reload(hass: HomeAssistant, entry: HZSULKConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: HZSULKConfigEntry) -> bool:
    """Odeber integraci."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrace z verze 1 (statistiky za celý kraj) na verzi 2 (události v okruhu)."""
    if entry.version > 2:
        return False

    if entry.version == 1:
        # Staré statistické senzory a binární senzor už neexistují
        registry = er.async_get(hass)
        for reg_entry in er.async_entries_for_config_entry(registry, entry.entry_id):
            registry.async_remove(reg_entry.entity_id)

        hass.config_entries.async_update_entry(
            entry,
            data={
                CONF_LATITUDE: hass.config.latitude,
                CONF_LONGITUDE: hass.config.longitude,
                CONF_RADIUS: DEFAULT_RADIUS_KM,
                CONF_HOURS: DEFAULT_HOURS,
                CONF_ONLY_ACTIVE: DEFAULT_ONLY_ACTIVE,
            },
            title="HZS ÚK – Domov",
            version=2,
        )
        _LOGGER.info(
            "HZSULK Events převedeno na verzi 2: události do %s km od zóny Domov",
            DEFAULT_RADIUS_KM,
        )

    return True
