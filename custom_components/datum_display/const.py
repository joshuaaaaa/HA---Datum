"""Constants for Datum Display integration."""
from typing import Final

DOMAIN: Final = "datum_display"
CONF_LANGUAGE: Final = "language"
CONF_DATE_FORMAT: Final = "date_format"
CONF_SENSORS: Final = "sensors"

# Available languages
LANGUAGE_CS: Final = "cs"
LANGUAGE_EN: Final = "en"

LANGUAGES: Final = {
    LANGUAGE_CS: "Čeština",
    LANGUAGE_EN: "English",
}

# Date format identifiers
FORMAT_DD_MM_YYYY_DOT: Final = "dd.mm.yyyy"
FORMAT_DD_MM_YYYY_DOT_SPACE: Final = "dd. mm. yyyy"
FORMAT_D_M_YYYY_DOT: Final = "d.m.yyyy"
FORMAT_DD_MM_YYYY_SLASH: Final = "dd/mm/yyyy"
FORMAT_MM_DD_YYYY_SLASH: Final = "mm/dd/yyyy"
FORMAT_YYYY_MM_DD: Final = "yyyy-mm-dd"
FORMAT_DD_MONTH_YYYY: Final = "dd_month_yyyy"
FORMAT_DAY_DD_MONTH_YYYY: Final = "day_dd_month_yyyy"
FORMAT_DAY_DD_MONTH: Final = "day_dd_month"
FORMAT_DD_MONTH: Final = "dd_month"
FORMAT_DAY_SHORT_DD_MM: Final = "day_short_dd_mm"
FORMAT_DAY_ABBR_DD_MM: Final = "day_abbr_dd_mm"
FORMAT_ISO8601: Final = "iso8601"
FORMAT_RELATIVE: Final = "relative"
FORMAT_VERBAL: Final = "verbal"

DATE_FORMATS: Final = {
    FORMAT_DD_MM_YYYY_DOT: "DD.MM.YYYY",
    FORMAT_DD_MM_YYYY_DOT_SPACE: "DD. MM. YYYY",
    FORMAT_D_M_YYYY_DOT: "D.M.YYYY",
    FORMAT_DD_MM_YYYY_SLASH: "DD/MM/YYYY",
    FORMAT_MM_DD_YYYY_SLASH: "MM/DD/YYYY",
    FORMAT_YYYY_MM_DD: "YYYY-MM-DD",
    FORMAT_DD_MONTH_YYYY: "DD. měsíc YYYY",
    FORMAT_DAY_DD_MONTH_YYYY: "Den DD. měsíc YYYY",
    FORMAT_DAY_DD_MONTH: "Den DD. měsíc",
    FORMAT_DD_MONTH: "DD měsíc",
    FORMAT_DAY_SHORT_DD_MM: "Den, DD.MM.",
    FORMAT_DAY_ABBR_DD_MM: "Zkr. den DD.MM.",
    FORMAT_ISO8601: "ISO 8601",
    FORMAT_RELATIVE: "Relativní (Dnes/Včera...)",
    FORMAT_VERBAL: "Slovní",
}

# Sensor types
SENSOR_DATE: Final = "date"
SENSOR_DAY_NAME: Final = "day_name"
SENSOR_DAY_NAME_SHORT: Final = "day_name_short"
SENSOR_WEEK_NUMBER: Final = "week_number"
SENSOR_MONTH_NAME: Final = "month_name"
SENSOR_MONTH_NUMBER: Final = "month_number"
SENSOR_YEAR: Final = "year"
SENSOR_DAY_OF_YEAR: Final = "day_of_year"
SENSOR_DAYS_IN_MONTH: Final = "days_in_month"
SENSOR_IS_LEAP_YEAR: Final = "is_leap_year"
SENSOR_QUARTER: Final = "quarter"
SENSOR_DAYS_UNTIL_END_OF_YEAR: Final = "days_until_end_of_year"
SENSOR_WEEK_DATES: Final = "week_dates"
SENSOR_TOMORROW: Final = "tomorrow"
SENSOR_YESTERDAY: Final = "yesterday"
SENSOR_WEEK_START: Final = "week_start"
SENSOR_WEEK_END: Final = "week_end"

SENSOR_TYPES: Final = {
    SENSOR_DATE: "Datum",
    SENSOR_DAY_NAME: "Název dne",
    SENSOR_DAY_NAME_SHORT: "Zkrácený název dne",
    SENSOR_WEEK_NUMBER: "Číslo týdne",
    SENSOR_MONTH_NAME: "Název měsíce",
    SENSOR_MONTH_NUMBER: "Číslo měsíce",
    SENSOR_YEAR: "Rok",
    SENSOR_DAY_OF_YEAR: "Den v roce",
    SENSOR_DAYS_IN_MONTH: "Počet dnů v měsíci",
    SENSOR_IS_LEAP_YEAR: "Přestupný rok",
    SENSOR_QUARTER: "Čtvrtletí",
    SENSOR_DAYS_UNTIL_END_OF_YEAR: "Dnů do konce roku",
    SENSOR_WEEK_DATES: "Data týdne",
    SENSOR_TOMORROW: "Zítra",
    SENSOR_YESTERDAY: "Včera",
    SENSOR_WEEK_START: "Začátek týdne",
    SENSOR_WEEK_END: "Konec týdne",
}

# Czech day names
DAYS_CS: Final = {
    0: "Pondělí",
    1: "Úterý",
    2: "Středa",
    3: "Čtvrtek",
    4: "Pátek",
    5: "Sobota",
    6: "Neděle",
}

DAYS_CS_SHORT: Final = {
    0: "Po",
    1: "Út",
    2: "St",
    3: "Čt",
    4: "Pá",
    5: "So",
    6: "Ne",
}

# English day names
DAYS_EN: Final = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

DAYS_EN_SHORT: Final = {
    0: "Mon",
    1: "Tue",
    2: "Wed",
    3: "Thu",
    4: "Fri",
    5: "Sat",
    6: "Sun",
}

# Czech month names (nominative)
MONTHS_CS: Final = {
    1: "Leden",
    2: "Únor",
    3: "Březen",
    4: "Duben",
    5: "Květen",
    6: "Červen",
    7: "Červenec",
    8: "Srpen",
    9: "Září",
    10: "Říjen",
    11: "Listopad",
    12: "Prosinec",
}

# Czech month names (genitive - for dates like "25. ledna")
MONTHS_CS_GENITIVE: Final = {
    1: "ledna",
    2: "února",
    3: "března",
    4: "dubna",
    5: "května",
    6: "června",
    7: "července",
    8: "srpna",
    9: "září",
    10: "října",
    11: "listopadu",
    12: "prosince",
}

# English month names
MONTHS_EN: Final = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

# Relative date translations
RELATIVE_CS: Final = {
    -2: "Předevčírem",
    -1: "Včera",
    0: "Dnes",
    1: "Zítra",
    2: "Pozítří",
}

RELATIVE_EN: Final = {
    -2: "Day before yesterday",
    -1: "Yesterday",
    0: "Today",
    1: "Tomorrow",
    2: "Day after tomorrow",
}

# Czech ordinal numbers for verbal dates (1-31)
ORDINALS_CS: Final = {
    1: "Prvního",
    2: "Druhého",
    3: "Třetího",
    4: "Čtvrtého",
    5: "Pátého",
    6: "Šestého",
    7: "Sedmého",
    8: "Osmého",
    9: "Devátého",
    10: "Desátého",
    11: "Jedenáctého",
    12: "Dvanáctého",
    13: "Třináctého",
    14: "Čtrnáctého",
    15: "Patnáctého",
    16: "Šestnáctého",
    17: "Sedmnáctého",
    18: "Osmnáctého",
    19: "Devatenáctého",
    20: "Dvacátého",
    21: "Dvacátého prvního",
    22: "Dvacátého druhého",
    23: "Dvacátého třetího",
    24: "Dvacátého čtvrtého",
    25: "Dvacátého pátého",
    26: "Dvacátého šestého",
    27: "Dvacátého sedmého",
    28: "Dvacátého osmého",
    29: "Dvacátého devátého",
    30: "Třicátého",
    31: "Třicátého prvního",
}

# English ordinal numbers for verbal dates (1-31)
ORDINALS_EN: Final = {
    1: "First",
    2: "Second",
    3: "Third",
    4: "Fourth",
    5: "Fifth",
    6: "Sixth",
    7: "Seventh",
    8: "Eighth",
    9: "Ninth",
    10: "Tenth",
    11: "Eleventh",
    12: "Twelfth",
    13: "Thirteenth",
    14: "Fourteenth",
    15: "Fifteenth",
    16: "Sixteenth",
    17: "Seventeenth",
    18: "Eighteenth",
    19: "Nineteenth",
    20: "Twentieth",
    21: "Twenty-first",
    22: "Twenty-second",
    23: "Twenty-third",
    24: "Twenty-fourth",
    25: "Twenty-fifth",
    26: "Twenty-sixth",
    27: "Twenty-seventh",
    28: "Twenty-eighth",
    29: "Twenty-ninth",
    30: "Thirtieth",
    31: "Thirty-first",
}

# Default sensors to enable
DEFAULT_SENSORS: Final = [
    SENSOR_DATE,
    SENSOR_DAY_NAME,
    SENSOR_WEEK_NUMBER,
]

# Update interval (in minutes)
UPDATE_INTERVAL: Final = 1
