"""Home Assistant integrace pro HZSULK Events."""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

from .const import DOMAIN
from .coordinator import HZSULKDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the HZSULK Events integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HZSULK Events from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Vytvoř coordinator
    coordinator = HZSULKDataUpdateCoordinator(hass)

    # Prvnč refresh dat
    await coordinator.async_config_entry_first_refresh()

    # Ulož coordinator do hass.data
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Setup platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload HZSULK Events config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
