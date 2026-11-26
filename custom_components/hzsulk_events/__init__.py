"""Home Assistant integrace HZSULK Events – zásahy HZS Ústeckého kraje v okolí."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import (
    CONF_HOURS,
    CONF_ONLY_ACTIVE,
    DEFAULT_HOURS,
    DEFAULT_ONLY_ACTIVE,
    DEFAULT_RADIUS_KM,
)
from .coordinator import HZSULKDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.GEO_LOCATION, Platform.BINARY_SENSOR]

HZSULKConfigEntry = ConfigEntry[HZSULKDataUpdateCoordinator]


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
