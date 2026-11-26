"""Config flow: místo, okruh a časové okno."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_LATITUDE, CONF_LOCATION, CONF_LONGITUDE, CONF_NAME, CONF_RADIUS
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_HOURS,
    CONF_ONLY_ACTIVE,
    DEFAULT_HOURS,
    DEFAULT_ONLY_ACTIVE,
    DEFAULT_RADIUS_KM,
    DOMAIN,
)


def _schema(defaults: dict[str, Any], with_name: bool) -> vol.Schema:
    fields: dict[Any, Any] = {}
    if with_name:
        fields[vol.Required(CONF_NAME, default=defaults.get(CONF_NAME, "Domov"))] = (
            selector.TextSelector()
        )
    fields[
        vol.Required(
            CONF_LOCATION,
            default={
                CONF_LATITUDE: defaults[CONF_LATITUDE],
                CONF_LONGITUDE: defaults[CONF_LONGITUDE],
                # Selektor pracuje s poloměrem v metrech
                CONF_RADIUS: defaults.get(CONF_RADIUS, DEFAULT_RADIUS_KM) * 1000,
            },
        )
    ] = selector.LocationSelector(selector.LocationSelectorConfig(radius=True))
    fields[vol.Required(CONF_HOURS, default=defaults.get(CONF_HOURS, DEFAULT_HOURS))] = (
        selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=1, max=168, step=1, unit_of_measurement="h",
                mode=selector.NumberSelectorMode.BOX,
            )
        )
    )
    fields[
        vol.Required(CONF_ONLY_ACTIVE, default=defaults.get(CONF_ONLY_ACTIVE, DEFAULT_ONLY_ACTIVE))
    ] = selector.BooleanSelector()
    return vol.Schema(fields)


def _to_settings(user_input: dict[str, Any]) -> dict[str, Any]:
    location = user_input[CONF_LOCATION]
    radius_m = location.get(CONF_RADIUS) or DEFAULT_RADIUS_KM * 1000
    return {
        CONF_LATITUDE: location[CONF_LATITUDE],
        CONF_LONGITUDE: location[CONF_LONGITUDE],
        CONF_RADIUS: round(radius_m / 1000, 1),
        CONF_HOURS: int(user_input[CONF_HOURS]),
        CONF_ONLY_ACTIVE: user_input[CONF_ONLY_ACTIVE],
    }


class HZSULKEventsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Přidání integrace."""

    VERSION = 2

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            settings = _to_settings(user_input)
            await self.async_set_unique_id(
                f"{settings[CONF_LATITUDE]:.4f}_{settings[CONF_LONGITUDE]:.4f}"
            )
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"HZS ÚK – {user_input[CONF_NAME]}", data=settings
            )

        defaults = {
            CONF_LATITUDE: self.hass.config.latitude,
            CONF_LONGITUDE: self.hass.config.longitude,
        }
        return self.async_show_form(step_id="user", data_schema=_schema(defaults, True))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return HZSULKOptionsFlow()


class HZSULKOptionsFlow(OptionsFlow):
    """Změna místa, okruhu a časového okna."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=_to_settings(user_input))

        defaults = {**self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(step_id="init", data_schema=_schema(defaults, False))
