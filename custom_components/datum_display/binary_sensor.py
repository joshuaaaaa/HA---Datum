"""Sensor platform for Datum Display integration."""
from __future__ import annotations

import calendar
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from datetime import datetime
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    CONF_LANGUAGE,
    CONF_DATE_FORMAT,
    CONF_SENSORS,
    LANGUAGE_CS,
    SENSOR_IS_LEAP_YEAR,
    SENSOR_IS_WORKDAY,
    FORMAT_DD_MM_YYYY_DOT,
    DEFAULT_SENSORS,
    HOLIDAYS_CS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Datum Display sensors from a config entry."""
    language = config_entry.options.get(
        CONF_LANGUAGE, config_entry.data.get(CONF_LANGUAGE, LANGUAGE_CS)
    )
    date_format = config_entry.options.get(
        CONF_DATE_FORMAT, config_entry.data.get(CONF_DATE_FORMAT, FORMAT_DD_MM_YYYY_DOT)
    )
    sensors_to_create = config_entry.options.get(
        CONF_SENSORS, config_entry.data.get(CONF_SENSORS, DEFAULT_SENSORS)
    )

    entities = []

    sensor_classes = {
        SENSOR_IS_LEAP_YEAR: DatumDisplayIsLeapYearSensor,
        SENSOR_IS_WORKDAY: DatumDisplayIsWorkdaySensor,
    }

    for sensor_type in sensors_to_create:
        if sensor_type in sensor_classes:
            entities.append(
                sensor_classes[sensor_type](
                    config_entry.entry_id,
                    language,
                    date_format,
                )
            )
    async_add_entities(entities, True)

class DatumDisplayBaseBinarySensor(BinarySensorEntity):
    """Base class for Datum Display binary sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry_id: str,
        language: str,
        date_format: str,
        sensor_type: str,
        name: str,
        icon: str,
    ) -> None:
        """Initialize the binary sensor."""
        self._entry_id = entry_id
        self._language = language
        self._date_format = date_format
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{entry_id}_{sensor_type}"
        self._unsub_update = None
        self._unsub_midnight = None

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "Datum Display",
            "manufacturer": "Custom",
            "model": "Date Sensors",
            "sw_version": "1.0.0",
        }

    async def async_added_to_hass(self) -> None:
        """Run when entity is added to hass."""
        self._unsub_update = async_track_time_change(
            self.hass,
            self._async_update_callback,
            minute=0,
            second=0,
        )
        self._unsub_midnight = async_track_time_change(
            self.hass,
            self._async_update_callback,
            hour=0,
            minute=0,
            second=0,
        )

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        if self._unsub_update:
            self._unsub_update()
        if self._unsub_midnight:
            self._unsub_midnight()

    async def _async_update_callback(self, now=None) -> None:
        """Update the binary sensor."""
        self.async_schedule_update_ha_state(True)

    def _get_now(self) -> datetime:
        """Get current datetime."""
        return dt_util.now()

class DatumDisplayIsWorkdaySensor(DatumDisplayBaseBinarySensor):
    """Sensor for displaying if today is a workday."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_IS_WORKDAY,
            "Pracovní den" if language == LANGUAGE_CS else "Workday",
            "mdi:briefcase",
        )

    async def async_update(self) -> None:
        """Update the binary sensor."""
        now = self._get_now()
        weekday = now.weekday()
        key = (now.month, now.day)

        is_weekend = weekday >= 5
        is_holiday = key in HOLIDAYS_CS
        is_workday = not is_weekend and not is_holiday

        self._attr_is_on = is_workday

        self._attr_icon = "mdi:briefcase" if is_workday else "mdi:home"

        self._attr_extra_state_attributes = {
            "is_workday": is_workday,
            "is_weekend": is_weekend,
            "is_holiday": is_holiday,
        }

class DatumDisplayIsLeapYearSensor(DatumDisplayBaseBinarySensor):
    """Sensor for displaying if current year is a leap year."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_IS_LEAP_YEAR,
            "Přestupný rok" if language == LANGUAGE_CS else "Leap Year",
            "mdi:calendar-star",
        )

    async def async_update(self) -> None:
        """Update the binary sensor."""
        now = self._get_now()
        self._attr_is_on = calendar.isleap(now.year)
