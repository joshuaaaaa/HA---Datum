"""Config flow for Datum Display integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_LANGUAGE,
    CONF_DATE_FORMAT,
    CONF_SENSORS,
    LANGUAGE_CS,
    LANGUAGE_EN,
    LANGUAGES,
    DATE_FORMATS,
    SENSOR_TYPES,
    DEFAULT_SENSORS,
    FORMAT_DD_MM_YYYY_DOT,
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict:
    """Validate the user input."""
    return {"title": f"Datum Display ({LANGUAGES.get(data[CONF_LANGUAGE], data[CONF_LANGUAGE])})"}


class DatumDisplayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Datum Display."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except Exception:
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(f"datum_display_{user_input[CONF_LANGUAGE]}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)

        # Build schema with selectors
        data_schema = vol.Schema(
            {
                vol.Required(CONF_LANGUAGE, default=LANGUAGE_CS): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=LANGUAGE_CS, label="Čeština"),
                            selector.SelectOptionDict(value=LANGUAGE_EN, label="English"),
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    ),
                ),
                vol.Required(CONF_DATE_FORMAT, default=FORMAT_DD_MM_YYYY_DOT): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=key, label=label)
                            for key, label in DATE_FORMATS.items()
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    ),
                ),
                vol.Required(CONF_SENSORS, default=DEFAULT_SENSORS): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=key, label=label)
                            for key, label in SENSOR_TYPES.items()
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        multiple=True,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> DatumDisplayOptionsFlow:
        """Create the options flow."""
        return DatumDisplayOptionsFlow(config_entry)


class DatumDisplayOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Datum Display."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_language = self.config_entry.data.get(CONF_LANGUAGE, LANGUAGE_CS)
        current_format = self.config_entry.data.get(CONF_DATE_FORMAT, FORMAT_DD_MM_YYYY_DOT)
        current_sensors = self.config_entry.data.get(CONF_SENSORS, DEFAULT_SENSORS)

        # Override with options if set
        current_language = self.config_entry.options.get(CONF_LANGUAGE, current_language)
        current_format = self.config_entry.options.get(CONF_DATE_FORMAT, current_format)
        current_sensors = self.config_entry.options.get(CONF_SENSORS, current_sensors)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_LANGUAGE, default=current_language): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=LANGUAGE_CS, label="Čeština"),
                            selector.SelectOptionDict(value=LANGUAGE_EN, label="English"),
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    ),
                ),
                vol.Required(CONF_DATE_FORMAT, default=current_format): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=key, label=label)
                            for key, label in DATE_FORMATS.items()
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    ),
                ),
                vol.Required(CONF_SENSORS, default=current_sensors): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=key, label=label)
                            for key, label in SENSOR_TYPES.items()
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        multiple=True,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )
