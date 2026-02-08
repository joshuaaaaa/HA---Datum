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
    SENSOR_HOLIDAY,
    SENSOR_NAME_DAY,
    SENSOR_IS_WORKDAY,
    SENSOR_MOON_PHASE,
    SENSOR_SEASON,
    SENSOR_ZODIAC,
    SENSOR_DAYS_UNTIL_CHRISTMAS,
    SENSOR_DAYS_UNTIL_NEW_YEAR,
    SENSOR_DAYS_UNTIL_EASTER,
    SENSOR_WORKDAYS_IN_MONTH,
    SENSOR_WORKDAYS_LEFT,
    SENSOR_HOLIDAY_DE,
    SENSOR_HOLIDAY_SK,
    SENSOR_NAME_DAY_SK,
    SENSOR_NAME_DAY_DE,
    SENSOR_WEEK_PARITY,
    SENSOR_DST,
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
    HOLIDAYS_CS,
    HOLIDAYS_EN,
    NAME_DAYS_CS,
    MOON_PHASES_CS,
    MOON_PHASES_EN,
    MOON_PHASE_ICONS,
    SEASONS_CS,
    SEASONS_EN,
    SEASON_ICONS,
    ZODIAC_SIGNS,
    ZODIAC_CS,
    ZODIAC_EN,
    ZODIAC_ICONS,
    HOLIDAYS_DE,
    HOLIDAYS_SK,
    NAME_DAYS_SK,
    NAME_DAYS_DE,
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
        SENSOR_HOLIDAY: DatumDisplayHolidaySensor,
        SENSOR_NAME_DAY: DatumDisplayNameDaySensor,
        SENSOR_IS_WORKDAY: DatumDisplayIsWorkdaySensor,
        SENSOR_MOON_PHASE: DatumDisplayMoonPhaseSensor,
        SENSOR_SEASON: DatumDisplaySeasonSensor,
        SENSOR_ZODIAC: DatumDisplayZodiacSensor,
        SENSOR_DAYS_UNTIL_CHRISTMAS: DatumDisplayDaysUntilChristmasSensor,
        SENSOR_DAYS_UNTIL_NEW_YEAR: DatumDisplayDaysUntilNewYearSensor,
        SENSOR_DAYS_UNTIL_EASTER: DatumDisplayDaysUntilEasterSensor,
        SENSOR_WORKDAYS_IN_MONTH: DatumDisplayWorkdaysInMonthSensor,
        SENSOR_WORKDAYS_LEFT: DatumDisplayWorkdaysLeftSensor,
        SENSOR_HOLIDAY_DE: DatumDisplayHolidayDESensor,
        SENSOR_HOLIDAY_SK: DatumDisplayHolidaySKSensor,
        SENSOR_NAME_DAY_SK: DatumDisplayNameDaySKSensor,
        SENSOR_NAME_DAY_DE: DatumDisplayNameDayDESensor,
        SENSOR_WEEK_PARITY: DatumDisplayWeekParitySensor,
        SENSOR_DST: DatumDisplayDSTSensor,
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


class DatumDisplayHolidaySensor(DatumDisplayBaseSensor):
    """Sensor for displaying current holiday."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_HOLIDAY,
            "Svátek" if language == LANGUAGE_CS else "Holiday",
            "mdi:party-popper",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        key = (now.month, now.day)
        holidays = HOLIDAYS_CS if self._language == LANGUAGE_CS else HOLIDAYS_EN
        holiday = holidays.get(key)
        if holiday:
            self._attr_native_value = holiday
            self._attr_icon = "mdi:party-popper"
        else:
            self._attr_native_value = "Není svátek" if self._language == LANGUAGE_CS else "No holiday"
            self._attr_icon = "mdi:calendar-blank"

        # Add upcoming holidays as attributes
        upcoming = []
        for i in range(1, 31):
            future = now + timedelta(days=i)
            future_key = (future.month, future.day)
            if future_key in holidays:
                upcoming.append({
                    "date": f"{future.day}.{future.month}.",
                    "name": holidays[future_key],
                    "days_until": i,
                })
                if len(upcoming) >= 3:
                    break
        self._attr_extra_state_attributes = {
            "is_holiday": holiday is not None,
            "upcoming_holidays": upcoming,
        }


class DatumDisplayNameDaySensor(DatumDisplayBaseSensor):
    """Sensor for displaying name day (Czech jmeniny)."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_NAME_DAY,
            "Jmeniny" if language == LANGUAGE_CS else "Name Day",
            "mdi:cake-variant",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        key = (now.month, now.day)
        name = NAME_DAYS_CS.get(key, "")
        self._attr_native_value = name

        # Add tomorrow's name day
        tomorrow = now + timedelta(days=1)
        tomorrow_key = (tomorrow.month, tomorrow.day)
        tomorrow_name = NAME_DAYS_CS.get(tomorrow_key, "")

        self._attr_extra_state_attributes = {
            "tomorrow": tomorrow_name,
            "date": f"{now.day}.{now.month}.",
        }


class DatumDisplayIsWorkdaySensor(DatumDisplayBaseSensor):
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
        """Update the sensor."""
        now = self._get_now()
        weekday = now.weekday()
        key = (now.month, now.day)

        # Check if weekend
        is_weekend = weekday >= 5
        # Check if holiday
        is_holiday = key in HOLIDAYS_CS

        is_workday = not is_weekend and not is_holiday

        if self._language == LANGUAGE_CS:
            self._attr_native_value = "Ano" if is_workday else "Ne"
        else:
            self._attr_native_value = "Yes" if is_workday else "No"

        self._attr_icon = "mdi:briefcase" if is_workday else "mdi:home"

        self._attr_extra_state_attributes = {
            "is_workday": is_workday,
            "is_weekend": is_weekend,
            "is_holiday": is_holiday,
        }


class DatumDisplayMoonPhaseSensor(DatumDisplayBaseSensor):
    """Sensor for displaying moon phase."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_MOON_PHASE,
            "Fáze měsíce" if language == LANGUAGE_CS else "Moon Phase",
            "mdi:moon-waxing-crescent",
        )

    def _calculate_moon_phase(self, dt: datetime) -> tuple[str, float]:
        """Calculate moon phase using a simple algorithm."""
        # Known new moon: January 6, 2000
        known_new_moon = datetime(2000, 1, 6, 18, 14, tzinfo=dt.tzinfo)
        lunar_cycle = 29.53058867  # days

        diff = dt - known_new_moon
        days_since = diff.total_seconds() / 86400
        current_cycle = days_since % lunar_cycle
        phase_percentage = (current_cycle / lunar_cycle) * 100

        # Determine phase name
        if current_cycle < 1.85:
            phase = "new_moon"
        elif current_cycle < 7.38:
            phase = "waxing_crescent"
        elif current_cycle < 9.23:
            phase = "first_quarter"
        elif current_cycle < 14.77:
            phase = "waxing_gibbous"
        elif current_cycle < 16.61:
            phase = "full_moon"
        elif current_cycle < 22.15:
            phase = "waning_gibbous"
        elif current_cycle < 23.99:
            phase = "last_quarter"
        else:
            phase = "waning_crescent"

        return phase, phase_percentage

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        phase, percentage = self._calculate_moon_phase(now)

        phases = MOON_PHASES_CS if self._language == LANGUAGE_CS else MOON_PHASES_EN
        self._attr_native_value = phases[phase]
        self._attr_icon = MOON_PHASE_ICONS[phase]

        self._attr_extra_state_attributes = {
            "phase_id": phase,
            "illumination": round(percentage, 1),
        }


class DatumDisplaySeasonSensor(DatumDisplayBaseSensor):
    """Sensor for displaying current season."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_SEASON,
            "Roční období" if language == LANGUAGE_CS else "Season",
            "mdi:weather-sunny",
        )

    def _get_season(self, dt: datetime) -> str:
        """Get current season based on date (Northern Hemisphere)."""
        month = dt.month
        day = dt.day

        # Spring: March 20 - June 20
        if (month == 3 and day >= 20) or month in [4, 5] or (month == 6 and day < 21):
            return "spring"
        # Summer: June 21 - September 22
        elif (month == 6 and day >= 21) or month in [7, 8] or (month == 9 and day < 23):
            return "summer"
        # Autumn: September 23 - December 20
        elif (month == 9 and day >= 23) or month in [10, 11] or (month == 12 and day < 21):
            return "autumn"
        # Winter: December 21 - March 19
        else:
            return "winter"

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        season = self._get_season(now)

        seasons = SEASONS_CS if self._language == LANGUAGE_CS else SEASONS_EN
        self._attr_native_value = seasons[season]
        self._attr_icon = SEASON_ICONS[season]

        self._attr_extra_state_attributes = {
            "season_id": season,
        }


class DatumDisplayZodiacSensor(DatumDisplayBaseSensor):
    """Sensor for displaying zodiac sign."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_ZODIAC,
            "Znamení" if language == LANGUAGE_CS else "Zodiac",
            "mdi:zodiac-aries",
        )

    def _get_zodiac(self, dt: datetime) -> str:
        """Get zodiac sign based on date."""
        month = dt.month
        day = dt.day

        for sign, ((start_month, start_day), (end_month, end_day)) in ZODIAC_SIGNS.items():
            if sign == "capricorn":
                # Capricorn spans year boundary
                if (month == 12 and day >= 22) or (month == 1 and day <= 19):
                    return sign
            else:
                if start_month == end_month:
                    if month == start_month and start_day <= day <= end_day:
                        return sign
                else:
                    if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                        return sign
        return "aries"  # fallback

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        zodiac = self._get_zodiac(now)

        zodiac_names = ZODIAC_CS if self._language == LANGUAGE_CS else ZODIAC_EN
        self._attr_native_value = zodiac_names[zodiac]
        self._attr_icon = ZODIAC_ICONS[zodiac]

        self._attr_extra_state_attributes = {
            "zodiac_id": zodiac,
        }


class DatumDisplayDaysUntilChristmasSensor(DatumDisplayBaseSensor):
    """Sensor for displaying days until Christmas."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_DAYS_UNTIL_CHRISTMAS,
            "Dnů do Vánoc" if language == LANGUAGE_CS else "Days Until Christmas",
            "mdi:pine-tree",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        christmas = datetime(now.year, 12, 24, tzinfo=now.tzinfo)

        if now.date() > christmas.date():
            # Christmas has passed, calculate for next year
            christmas = datetime(now.year + 1, 12, 24, tzinfo=now.tzinfo)

        delta = christmas.date() - now.date()
        self._attr_native_value = delta.days

        self._attr_extra_state_attributes = {
            "christmas_date": f"24.12.{christmas.year}",
        }


class DatumDisplayDaysUntilNewYearSensor(DatumDisplayBaseSensor):
    """Sensor for displaying days until New Year."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_DAYS_UNTIL_NEW_YEAR,
            "Dnů do Nového roku" if language == LANGUAGE_CS else "Days Until New Year",
            "mdi:firework",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        new_year = datetime(now.year + 1, 1, 1, tzinfo=now.tzinfo)

        delta = new_year.date() - now.date()
        self._attr_native_value = delta.days

        self._attr_extra_state_attributes = {
            "new_year": new_year.year,
        }


class DatumDisplayDaysUntilEasterSensor(DatumDisplayBaseSensor):
    """Sensor for displaying days until Easter."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_DAYS_UNTIL_EASTER,
            "Dnů do Velikonoc" if language == LANGUAGE_CS else "Days Until Easter",
            "mdi:egg-easter",
        )

    def _calculate_easter(self, year: int) -> datetime:
        """Calculate Easter Sunday using the Anonymous Gregorian algorithm."""
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1
        return datetime(year, month, day)

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        easter = self._calculate_easter(now.year)

        if now.date() > easter.date():
            # Easter has passed, calculate for next year
            easter = self._calculate_easter(now.year + 1)

        delta = easter.date() - now.date()
        self._attr_native_value = delta.days

        self._attr_extra_state_attributes = {
            "easter_date": f"{easter.day}.{easter.month}.{easter.year}",
            "easter_year": easter.year,
        }


class DatumDisplayWorkdaysInMonthSensor(DatumDisplayBaseSensor):
    """Sensor for displaying workdays in current month."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_WORKDAYS_IN_MONTH,
            "Pracovních dnů v měsíci" if language == LANGUAGE_CS else "Workdays in Month",
            "mdi:calendar-check",
        )

    def _count_workdays(self, year: int, month: int) -> int:
        """Count workdays in a month."""
        days_in_month = calendar.monthrange(year, month)[1]
        workdays = 0

        for day in range(1, days_in_month + 1):
            dt = datetime(year, month, day)
            weekday = dt.weekday()
            key = (month, day)

            # Not weekend and not holiday
            if weekday < 5 and key not in HOLIDAYS_CS:
                workdays += 1

        return workdays

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        workdays = self._count_workdays(now.year, now.month)
        self._attr_native_value = workdays

        self._attr_extra_state_attributes = {
            "month": now.month,
            "year": now.year,
        }


class DatumDisplayWorkdaysLeftSensor(DatumDisplayBaseSensor):
    """Sensor for displaying workdays left in current month."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_WORKDAYS_LEFT,
            "Zbývá pracovních dnů" if language == LANGUAGE_CS else "Workdays Left",
            "mdi:calendar-clock",
        )

    def _count_workdays_left(self, now: datetime) -> int:
        """Count remaining workdays in current month."""
        year = now.year
        month = now.month
        current_day = now.day
        days_in_month = calendar.monthrange(year, month)[1]
        workdays = 0

        for day in range(current_day + 1, days_in_month + 1):
            dt = datetime(year, month, day)
            weekday = dt.weekday()
            key = (month, day)

            # Not weekend and not holiday
            if weekday < 5 and key not in HOLIDAYS_CS:
                workdays += 1

        return workdays

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        workdays_left = self._count_workdays_left(now)
        self._attr_native_value = workdays_left

        self._attr_extra_state_attributes = {
            "month": now.month,
            "year": now.year,
            "current_day": now.day,
        }


class DatumDisplayHolidayDESensor(DatumDisplayBaseSensor):
    """Sensor for displaying German holidays."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_HOLIDAY_DE,
            "Německý svátek" if language == LANGUAGE_CS else "German Holiday",
            "mdi:party-popper",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        key = (now.month, now.day)
        holiday = HOLIDAYS_DE.get(key)
        if holiday:
            self._attr_native_value = holiday
            self._attr_icon = "mdi:party-popper"
        else:
            self._attr_native_value = "Kein Feiertag" if self._language != LANGUAGE_CS else "Není svátek"
            self._attr_icon = "mdi:calendar-blank"

        # Add upcoming holidays as attributes
        upcoming = []
        for i in range(1, 31):
            future = now + timedelta(days=i)
            future_key = (future.month, future.day)
            if future_key in HOLIDAYS_DE:
                upcoming.append({
                    "date": f"{future.day}.{future.month}.",
                    "name": HOLIDAYS_DE[future_key],
                    "days_until": i,
                })
                if len(upcoming) >= 3:
                    break
        self._attr_extra_state_attributes = {
            "is_holiday": holiday is not None,
            "upcoming_holidays": upcoming,
        }


class DatumDisplayHolidaySKSensor(DatumDisplayBaseSensor):
    """Sensor for displaying Slovak holidays."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_HOLIDAY_SK,
            "Slovenský svátek" if language == LANGUAGE_CS else "Slovak Holiday",
            "mdi:party-popper",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        key = (now.month, now.day)
        holiday = HOLIDAYS_SK.get(key)
        if holiday:
            self._attr_native_value = holiday
            self._attr_icon = "mdi:party-popper"
        else:
            self._attr_native_value = "Nie je sviatok" if self._language != LANGUAGE_CS else "Není svátek"
            self._attr_icon = "mdi:calendar-blank"

        # Add upcoming holidays as attributes
        upcoming = []
        for i in range(1, 31):
            future = now + timedelta(days=i)
            future_key = (future.month, future.day)
            if future_key in HOLIDAYS_SK:
                upcoming.append({
                    "date": f"{future.day}.{future.month}.",
                    "name": HOLIDAYS_SK[future_key],
                    "days_until": i,
                })
                if len(upcoming) >= 3:
                    break
        self._attr_extra_state_attributes = {
            "is_holiday": holiday is not None,
            "upcoming_holidays": upcoming,
        }


class DatumDisplayNameDaySKSensor(DatumDisplayBaseSensor):
    """Sensor for displaying Slovak name day (meniny)."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_NAME_DAY_SK,
            "Slovenské meniny" if language == LANGUAGE_CS else "Slovak Name Day",
            "mdi:cake-variant",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        key = (now.month, now.day)
        name = NAME_DAYS_SK.get(key, "")
        self._attr_native_value = name

        # Add tomorrow's name day
        tomorrow = now + timedelta(days=1)
        tomorrow_key = (tomorrow.month, tomorrow.day)
        tomorrow_name = NAME_DAYS_SK.get(tomorrow_key, "")

        self._attr_extra_state_attributes = {
            "tomorrow": tomorrow_name,
            "date": f"{now.day}.{now.month}.",
        }


class DatumDisplayNameDayDESensor(DatumDisplayBaseSensor):
    """Sensor for displaying German name day (Namenstag)."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_NAME_DAY_DE,
            "Německé jmeniny" if language == LANGUAGE_CS else "German Name Day",
            "mdi:cake-variant",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        key = (now.month, now.day)
        name = NAME_DAYS_DE.get(key, "")
        self._attr_native_value = name

        # Add tomorrow's name day
        tomorrow = now + timedelta(days=1)
        tomorrow_key = (tomorrow.month, tomorrow.day)
        tomorrow_name = NAME_DAYS_DE.get(tomorrow_key, "")

        self._attr_extra_state_attributes = {
            "tomorrow": tomorrow_name,
            "date": f"{now.day}.{now.month}.",
        }


class DatumDisplayWeekParitySensor(DatumDisplayBaseSensor):
    """Sensor for displaying even/odd week."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_WEEK_PARITY,
            "Sudý/Lichý týden" if language == LANGUAGE_CS else "Even/Odd Week",
            "mdi:calendar-week",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        week_number = now.isocalendar()[1]
        is_even = week_number % 2 == 0

        if self._language == LANGUAGE_CS:
            self._attr_native_value = "Sudý" if is_even else "Lichý"
        else:
            self._attr_native_value = "Even" if is_even else "Odd"

        self._attr_extra_state_attributes = {
            "week_number": week_number,
            "is_even": is_even,
        }


class DatumDisplayDSTSensor(DatumDisplayBaseSensor):
    """Sensor for displaying summer/winter time (DST)."""

    def __init__(self, entry_id: str, language: str, date_format: str) -> None:
        """Initialize the sensor."""
        super().__init__(
            entry_id,
            language,
            date_format,
            SENSOR_DST,
            "Letní/Zimní čas" if language == LANGUAGE_CS else "Summer/Winter Time",
            "mdi:clock-check",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        now = self._get_now()
        is_dst = bool(now.dst())

        if self._language == LANGUAGE_CS:
            self._attr_native_value = "Letní čas" if is_dst else "Zimní čas"
        else:
            self._attr_native_value = "Summer Time" if is_dst else "Winter Time"

        self._attr_icon = "mdi:white-balance-sunny" if is_dst else "mdi:snowflake"

        self._attr_extra_state_attributes = {
            "is_dst": is_dst,
            "utc_offset": str(now.utcoffset()),
        }
