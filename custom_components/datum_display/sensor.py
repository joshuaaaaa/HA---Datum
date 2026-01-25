"""Sensor platform for Datum Display integration."""
from __future__ import annotations

import calendar
from datetime import datetime, timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    CONF_LANGUAGE,
    CONF_DATE_FORMAT,
    CONF_SENSORS,
    LANGUAGE_CS,
    LANGUAGE_EN,
    DAYS_CS,
    DAYS_CS_SHORT,
    DAYS_EN,
    DAYS_EN_SHORT,
    MONTHS_CS,
    MONTHS_CS_GENITIVE,
    MONTHS_EN,
    RELATIVE_CS,
    RELATIVE_EN,
    ORDINALS_CS,
    ORDINALS_EN,
    SENSOR_DATE,
    SENSOR_DAY_NAME,
    SENSOR_DAY_NAME_SHORT,
    SENSOR_WEEK_NUMBER,
    SENSOR_MONTH_NAME,
    SENSOR_MONTH_NUMBER,
    SENSOR_YEAR,
    SENSOR_DAY_OF_YEAR,
    SENSOR_DAYS_IN_MONTH,
    SENSOR_IS_LEAP_YEAR,
    SENSOR_QUARTER,
    SENSOR_DAYS_UNTIL_END_OF_YEAR,
    SENSOR_WEEK_DATES,
    SENSOR_TOMORROW,
    SENSOR_YESTERDAY,
    SENSOR_WEEK_START,
    SENSOR_WEEK_END,
    FORMAT_DD_MM_YYYY_DOT,
    FORMAT_DD_MM_YYYY_DOT_SPACE,
    FORMAT_D_M_YYYY_DOT,
    FORMAT_DD_MM_YYYY_SLASH,
    FORMAT_MM_DD_YYYY_SLASH,
    FORMAT_YYYY_MM_DD,
    FORMAT_DD_MONTH_YYYY,
    FORMAT_DAY_DD_MONTH_YYYY,
    FORMAT_DAY_DD_MONTH,
    FORMAT_DD_MONTH,
    FORMAT_DAY_SHORT_DD_MM,
    FORMAT_DAY_ABBR_DD_MM,
    FORMAT_ISO8601,
    FORMAT_RELATIVE,
    FORMAT_VERBAL,
    DEFAULT_SENSORS,
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
        SENSOR_DATE: DatumDisplayDateSensor,
        SENSOR_DAY_NAME: DatumDisplayDayNameSensor,
        SENSOR_DAY_NAME_SHORT: DatumDisplayDayNameShortSensor,
        SENSOR_WEEK_NUMBER: DatumDisplayWeekNumberSensor,
        SENSOR_MONTH_NAME: DatumDisplayMonthNameSensor,
        SENSOR_MONTH_NUMBER: DatumDisplayMonthNumberSensor,
        SENSOR_YEAR: DatumDisplayYearSensor,
        SENSOR_DAY_OF_YEAR: DatumDisplayDayOfYearSensor,
        SENSOR_DAYS_IN_MONTH: DatumDisplayDaysInMonthSensor,
        SENSOR_IS_LEAP_YEAR: DatumDisplayIsLeapYearSensor,
        SENSOR_QUARTER: DatumDisplayQuarterSensor,
        SENSOR_DAYS_UNTIL_END_OF_YEAR: DatumDisplayDaysUntilEndOfYearSensor,
        SENSOR_WEEK_DATES: DatumDisplayWeekDatesSensor,
        SENSOR_TOMORROW: DatumDisplayTomorrowSensor,
        SENSOR_YESTERDAY: DatumDisplayYesterdaySensor,
        SENSOR_WEEK_START: DatumDisplayWeekStartSensor,
        SENSOR_WEEK_END: DatumDisplayWeekEndSensor,
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


class DatumDisplayBaseSensor(SensorEntity):
    """Base class for Datum Display sensors."""

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
        """Initialize the sensor."""
        self._entry_id = entry_id
        self._language = language
        self._date_format = date_format
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{entry_id}_{sensor_type}"
        self._unsub_update = None

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
            self.hass, self._async_update_callback, minute=0, second=0
        )
        # Also update at midnight
        self._unsub_midnight = async_track_time_change(
            self.hass, self._async_update_callback, hour=0, minute=0, second=0
        )

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        if self._unsub_update:
            self._unsub_update()
        if hasattr(self, "_unsub_midnight") and self._unsub_midnight:
            self._unsub_midnight()

    async def _async_update_callback(self, now=None) -> None:
        """Update the sensor."""
        self.async_schedule_update_ha_state(True)

    def _get_now(self) -> datetime:
        """Get current datetime."""
        return dt_util.now()

    def _get_day_name(self, weekday: int, short: bool = False) -> str:
        """Get day name in the configured language."""
        if self._language == LANGUAGE_CS:
            return DAYS_CS_SHORT[weekday] if short else DAYS_CS[weekday]
        return DAYS_EN_SHORT[weekday] if short else DAYS_EN[weekday]

    def _get_month_name(self, month: int, genitive: bool = False) -> str:
        """Get month name in the configured language."""
        if self._language == LANGUAGE_CS:
            return MONTHS_CS_GENITIVE[month] if genitive else MONTHS_CS[month]
        return MONTHS_EN[month]

    def _get_ordinal(self, day: int) -> str:
        """Get ordinal number for the day."""
        if self._language == LANGUAGE_CS:
            return ORDINALS_CS.get(day, str(day))
        return ORDINALS_EN.get(day, str(day))

    def _format_date(self, dt: datetime) -> str:
        """Format date according to the selected format."""
        day = dt.day
        month = dt.month
        year = dt.year
        weekday = dt.weekday()

        formats = {
            FORMAT_DD_MM_YYYY_DOT: f"{day:02d}.{month:02d}.{year}",
            FORMAT_DD_MM_YYYY_DOT_SPACE: f"{day:02d}. {month:02d}. {year}",
            FORMAT_D_M_YYYY_DOT: f"{day}.{month}.{year}",
            FORMAT_DD_MM_YYYY_SLASH: f"{day:02d}/{month:02d}/{year}",
            FORMAT_MM_DD_YYYY_SLASH: f"{month:02d}/{day:02d}/{year}",
            FORMAT_YYYY_MM_DD: f"{year}-{month:02d}-{day:02d}",
            FORMAT_ISO8601: f"{year}-{month:02d}-{day:02d}",
        }

        if self._date_format in formats:
            return formats[self._date_format]

        # Complex formats with names
        if self._date_format == FORMAT_DD_MONTH_YYYY:
            if self._language == LANGUAGE_CS:
                return f"{day}. {self._get_month_name(month, True)} {year}"
            return f"{day} {self._get_month_name(month)} {year}"

        if self._date_format == FORMAT_DAY_DD_MONTH_YYYY:
            if self._language == LANGUAGE_CS:
                return f"{self._get_day_name(weekday)} {day}. {self._get_month_name(month, True)} {year}"
            return f"{self._get_day_name(weekday)} {day} {self._get_month_name(month)} {year}"

        if self._date_format == FORMAT_DAY_DD_MONTH:
            if self._language == LANGUAGE_CS:
                return f"{self._get_day_name(weekday)} {day}. {self._get_month_name(month, True)}"
            return f"{self._get_day_name(weekday)} {day} {self._get_month_name(month)}"

        if self._date_format == FORMAT_DD_MONTH:
            if self._language == LANGUAGE_CS:
                return f"{day}. {self._get_month_name(month, True)}"
            return f"{day} {self._get_month_name(month)}"

        if self._date_format == FORMAT_DAY_SHORT_DD_MM:
            return f"{self._get_day_name(weekday, True)}, {day:02d}.{month:02d}."

        if self._date_format == FORMAT_DAY_ABBR_DD_MM:
            return f"{self._get_day_name(weekday, True)} {day:02d}.{month:02d}."

        if self._date_format == FORMAT_RELATIVE:
            today = dt_util.now().date()
            diff = (dt.date() - today).days
            if self._language == LANGUAGE_CS:
                return RELATIVE_CS.get(diff, f"{day}. {self._get_month_name(month, True)}")
            return RELATIVE_EN.get(diff, f"{day} {self._get_month_name(month)}")

        if self._date_format == FORMAT_VERBAL:
            if self._language == LANGUAGE_CS:
                return f"{self._get_ordinal(day)} {self._get_month_name(month, True)}"
            return f"{self._get_ordinal(day)} of {self._get_month_name(month)}"

        # Default fallback
        return f"{day:02d}.{month:02d}.{year}"


class DatumDisplayDateSensor(DatumDisplayBaseSensor):
    """Sensor for displaying formatted date."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_DATE,
            "Datum" if language == LANGUAGE_CS else "Date",
            "mdi:calendar",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        self._attr_native_value = self._format_date(self._get_now())


class DatumDisplayDayNameSensor(DatumDisplayBaseSensor):
    """Sensor for displaying day name."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_DAY_NAME,
            "Den" if language == LANGUAGE_CS else "Day",
            "mdi:calendar-today",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        self._attr_native_value = self._get_day_name(self._get_now().weekday())


class DatumDisplayDayNameShortSensor(DatumDisplayBaseSensor):
    """Sensor for displaying short day name."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_DAY_NAME_SHORT,
            "Den (zkr.)" if language == LANGUAGE_CS else "Day (short)",
            "mdi:calendar-today",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        self._attr_native_value = self._get_day_name(self._get_now().weekday(), short=True)


class DatumDisplayWeekNumberSensor(DatumDisplayBaseSensor):
    """Sensor for displaying week number."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_WEEK_NUMBER,
            "Týden" if language == LANGUAGE_CS else "Week",
            "mdi:calendar-week",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        self._attr_native_value = self._get_now().isocalendar()[1]


class DatumDisplayMonthNameSensor(DatumDisplayBaseSensor):
    """Sensor for displaying month name."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_MONTH_NAME,
            "Měsíc" if language == LANGUAGE_CS else "Month",
            "mdi:calendar-month",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        self._attr_native_value = self._get_month_name(self._get_now().month)


class DatumDisplayMonthNumberSensor(DatumDisplayBaseSensor):
    """Sensor for displaying month number."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_MONTH_NUMBER,
            "Číslo měsíce" if language == LANGUAGE_CS else "Month Number",
            "mdi:calendar-month",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        self._attr_native_value = self._get_now().month


class DatumDisplayYearSensor(DatumDisplayBaseSensor):
    """Sensor for displaying year."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_YEAR,
            "Rok" if language == LANGUAGE_CS else "Year",
            "mdi:calendar-blank",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        self._attr_native_value = self._get_now().year


class DatumDisplayDayOfYearSensor(DatumDisplayBaseSensor):
    """Sensor for displaying day of year."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_DAY_OF_YEAR,
            "Den v roce" if language == LANGUAGE_CS else "Day of Year",
            "mdi:calendar-range",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        self._attr_native_value = now.timetuple().tm_yday


class DatumDisplayDaysInMonthSensor(DatumDisplayBaseSensor):
    """Sensor for displaying days in current month."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_DAYS_IN_MONTH,
            "Dnů v měsíci" if language == LANGUAGE_CS else "Days in Month",
            "mdi:calendar-month-outline",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        self._attr_native_value = calendar.monthrange(now.year, now.month)[1]


class DatumDisplayIsLeapYearSensor(DatumDisplayBaseSensor):
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
        """Update the sensor."""
        now = self._get_now()
        is_leap = calendar.isleap(now.year)
        if self._language == LANGUAGE_CS:
            self._attr_native_value = "Ano" if is_leap else "Ne"
        else:
            self._attr_native_value = "Yes" if is_leap else "No"


class DatumDisplayQuarterSensor(DatumDisplayBaseSensor):
    """Sensor for displaying quarter."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_QUARTER,
            "Čtvrtletí" if language == LANGUAGE_CS else "Quarter",
            "mdi:calendar-clock",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        month = self._get_now().month
        quarter = (month - 1) // 3 + 1
        self._attr_native_value = f"Q{quarter}"


class DatumDisplayDaysUntilEndOfYearSensor(DatumDisplayBaseSensor):
    """Sensor for displaying days until end of year."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_DAYS_UNTIL_END_OF_YEAR,
            "Dnů do konce roku" if language == LANGUAGE_CS else "Days Until Year End",
            "mdi:calendar-end",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        end_of_year = datetime(now.year, 12, 31, tzinfo=now.tzinfo)
        delta = end_of_year.date() - now.date()
        self._attr_native_value = delta.days


class DatumDisplayWeekDatesSensor(DatumDisplayBaseSensor):
    """Sensor for displaying all dates of current week."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_WEEK_DATES,
            "Data týdne" if language == LANGUAGE_CS else "Week Dates",
            "mdi:calendar-week",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        start_of_week = now - timedelta(days=now.weekday())
        dates = []
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            dates.append(f"{day.day:02d}.{day.month:02d}.")
        self._attr_native_value = " - ".join([dates[0], dates[-1]])
        self._attr_extra_state_attributes = {
            "monday": dates[0],
            "tuesday": dates[1],
            "wednesday": dates[2],
            "thursday": dates[3],
            "friday": dates[4],
            "saturday": dates[5],
            "sunday": dates[6],
            "all_dates": dates,
        }


class DatumDisplayTomorrowSensor(DatumDisplayBaseSensor):
    """Sensor for displaying tomorrow's date."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_TOMORROW,
            "Zítra" if language == LANGUAGE_CS else "Tomorrow",
            "mdi:calendar-arrow-right",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        tomorrow = self._get_now() + timedelta(days=1)
        self._attr_native_value = self._format_date(tomorrow)
        self._attr_extra_state_attributes = {
            "day_name": self._get_day_name(tomorrow.weekday()),
            "day_name_short": self._get_day_name(tomorrow.weekday(), short=True),
        }


class DatumDisplayYesterdaySensor(DatumDisplayBaseSensor):
    """Sensor for displaying yesterday's date."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_YESTERDAY,
            "Včera" if language == LANGUAGE_CS else "Yesterday",
            "mdi:calendar-arrow-left",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        yesterday = self._get_now() - timedelta(days=1)
        self._attr_native_value = self._format_date(yesterday)
        self._attr_extra_state_attributes = {
            "day_name": self._get_day_name(yesterday.weekday()),
            "day_name_short": self._get_day_name(yesterday.weekday(), short=True),
        }


class DatumDisplayWeekStartSensor(DatumDisplayBaseSensor):
    """Sensor for displaying week start date."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_WEEK_START,
            "Začátek týdne" if language == LANGUAGE_CS else "Week Start",
            "mdi:calendar-start",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        start_of_week = now - timedelta(days=now.weekday())
        self._attr_native_value = self._format_date(start_of_week)


class DatumDisplayWeekEndSensor(DatumDisplayBaseSensor):
    """Sensor for displaying week end date."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_WEEK_END,
            "Konec týdne" if language == LANGUAGE_CS else "Week End",
            "mdi:calendar-end",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        end_of_week = now + timedelta(days=6 - now.weekday())
        self._attr_native_value = self._format_date(end_of_week)
