"""Config flow pro HZSULK Events."""

import logging
from typing import Any, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class HZSULKEventsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow pro HZSULK Events."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[dict[str, Any]] = None
    ) -> FlowResult:
        """Obsluž uživatelský krok (setup integrace)."""
        if user_input is not None:
            return self.async_create_entry(
                title="HZSULK Events",
                data=user_input,
            )

        data_schema = vol.Schema({})

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            description_placeholders={
                "url": "https://udalosti.hzsulk.cz/",
            },
        )
