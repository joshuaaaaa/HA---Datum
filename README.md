# Datum Display - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/joshuaaaaa/HA---Datum.svg)](https://GitHub.com/joshuaaaaa/HA---Datum/releases/)

Pokročilá integrace pro zobrazení data v Home Assistant s podporou českých a anglických názvů dnů a měsíců.

## Funkce

- **Více formátů data** - 15+ různých stylů zobrazení
- **České a anglické názvy** - plná lokalizace dnů a měsíců
- **Více senzorů** (28 celkem):
  - Datum (různé formáty)
  - Den v týdnu
  - Týden v roce
  - Měsíc
  - Rok
  - Počet dnů v měsíci/roce
  - Přestupný rok
  - Čtvrtletí
  - **Svátky** (české státní svátky)
  - **Jmeniny** (kompletní český kalendář)
  - **Pracovní den** (Ano/Ne)
  - **Fáze měsíce** (nov, úplněk, čtvrtě...)
  - **Roční období** (jaro, léto, podzim, zima)
  - **Znamení zvěrokruhu**
  - **Odpočty** (do Vánoc, Nového roku, Velikonoc)
  - **Pracovní dny** (v měsíci, zbývající)
- **Konfigurace přes UI** - žádné YAML úpravy

## Instalace přes HACS

1. Otevřete HACS v Home Assistant
2. Klikněte na **Integrations**
3. Klikněte na tři tečky (menu) vpravo nahoře
4. Vyberte **Custom repositories**
5. Zadejte URL: `https://github.com/joshuaaaaa/HA---Datum`
6. Kategorie: **Integration**
7. Klikněte **Add**
8. Najděte "Datum Display" a klikněte **Download**
9. Restartujte Home Assistant

## Konfigurace

1. Jděte do **Settings** → **Devices & Services**
2. Klikněte **+ Add Integration**
3. Vyhledejte "Datum Display"
4. Vyberte požadované senzory a formáty

## Dostupné formáty data

| Formát | Příklad (český) | Příklad (anglický) |
|--------|-----------------|-------------------|
| `DD.MM.YYYY` | 25.01.2026 | 25.01.2026 |
| `DD. MM. YYYY` | 25. 01. 2026 | 25. 01. 2026 |
| `D.M.YYYY` | 25.1.2026 | 25.1.2026 |
| `DD/MM/YYYY` | 25/01/2026 | 25/01/2026 |
| `MM/DD/YYYY` | 01/25/2026 | 01/25/2026 |
| `YYYY-MM-DD` | 2026-01-25 | 2026-01-25 |
| `DD. měsíc YYYY` | 25. ledna 2026 | 25 January 2026 |
| `Den DD. měsíc YYYY` | Neděle 25. ledna 2026 | Sunday 25 January 2026 |
| `Den DD. měsíc` | Neděle 25. ledna | Sunday 25 January |
| `DD měsíc` | 25 ledna | 25 January |
| `Den, DD.MM.` | Ne, 25.01. | Sun, 25.01. |
| `Krátký den DD.MM.` | Ne 25.01. | Sun 25.01. |
| `ISO 8601` | 2026-01-25 | 2026-01-25 |
| `Relativní` | Dnes | Today |
| `Slovní` | Dvacátého pátého ledna | Twenty-fifth of January |

## Dostupné senzory

### sensor.datum_display_date
Hlavní senzor data ve zvoleném formátu.

### sensor.datum_display_day_name
Název dne v týdnu (Pondělí, Úterý... / Monday, Tuesday...).

### sensor.datum_display_day_name_short
Zkrácený název dne (Po, Út... / Mon, Tue...).

### sensor.datum_display_week_number
Číslo týdne v roce (1-53).

### sensor.datum_display_month_name
Název měsíce (Leden, Únor... / January, February...).

### sensor.datum_display_year
Aktuální rok.

### sensor.datum_display_day_of_year
Den v roce (1-366).

### sensor.datum_display_days_in_month
Počet dnů v aktuálním měsíci.

### sensor.datum_display_is_leap_year
Zda je přestupný rok (True/False).

### sensor.datum_display_quarter
Čtvrtletí (Q1, Q2, Q3, Q4).

### sensor.datum_display_days_until_end_of_year
Počet dnů do konce roku.

### sensor.datum_display_week_dates
Všechna data aktuálního týdne.

### sensor.datum_display_holiday
Aktuální státní svátek (pokud je).
- Atributy: `is_holiday`, `upcoming_holidays`

### sensor.datum_display_name_day
Kdo má dnes svátek (české jmeniny).
- Atributy: `tomorrow` (jmeniny zítra)

### sensor.datum_display_is_workday
Je dnes pracovní den? (Ano/Ne).
- Atributy: `is_workday`, `is_weekend`, `is_holiday`

### sensor.datum_display_moon_phase
Aktuální fáze měsíce (Nov, Úplněk, První čtvrť...).
- Ikona se dynamicky mění podle fáze
- Atributy: `phase_id`, `illumination`

### sensor.datum_display_season
Aktuální roční období (Jaro, Léto, Podzim, Zima).
- Ikona se dynamicky mění podle období
- Atributy: `season_id`

### sensor.datum_display_zodiac
Aktuální znamení zvěrokruhu.
- Ikona odpovídá znamení
- Atributy: `zodiac_id`

### sensor.datum_display_days_until_christmas
Počet dnů do Štědrého dne (24.12.).

### sensor.datum_display_days_until_new_year
Počet dnů do Nového roku.

### sensor.datum_display_days_until_easter
Počet dnů do Velikonoc (automatický výpočet data).
- Atributy: `easter_date`, `easter_year`

### sensor.datum_display_workdays_in_month
Celkový počet pracovních dnů v aktuálním měsíci.

### sensor.datum_display_workdays_left
Počet zbývajících pracovních dnů do konce měsíce.

## Příklad použití v Lovelace

```yaml
type: entities
title: Datum
entities:
  - entity: sensor.datum_display_date
    name: Datum
  - entity: sensor.datum_display_day_name
    name: Den
  - entity: sensor.datum_display_week_number
    name: Týden
```

### Markdown karta s vlastním stylem

```yaml
type: markdown
content: |
  <div style="font-family: 'Roboto', sans-serif; font-size: 2em; text-align: center;">
    {{ states('sensor.datum_display_date') }}
  </div>
  <div style="font-family: 'Roboto', sans-serif; font-size: 1.2em; text-align: center; color: gray;">
    {{ states('sensor.datum_display_day_name') }}
  </div>
```

### Kompletní přehled s novými senzory

```yaml
type: entities
title: Datum a čas
entities:
  - entity: sensor.datum_display_date
    name: Datum
  - entity: sensor.datum_display_day_name
    name: Den
  - entity: sensor.datum_display_name_day
    name: Svátek má
  - entity: sensor.datum_display_moon_phase
    name: Měsíc
  - entity: sensor.datum_display_zodiac
    name: Znamení
  - entity: sensor.datum_display_season
    name: Období
```

### Odpočty do svátků

```yaml
type: glance
title: Odpočty
entities:
  - entity: sensor.datum_display_days_until_christmas
    name: Vánoce
  - entity: sensor.datum_display_days_until_new_year
    name: Nový rok
  - entity: sensor.datum_display_days_until_easter
    name: Velikonoce
```

### Pracovní dny

```yaml
type: entities
title: Práce
entities:
  - entity: sensor.datum_display_is_workday
    name: Dnes je pracovní den
  - entity: sensor.datum_display_workdays_in_month
    name: Pracovních dnů v měsíci
  - entity: sensor.datum_display_workdays_left
    name: Zbývá pracovních dnů
```

## Změna fontu

Pro změnu fontu v dashboardu můžete použít custom CSS nebo theme:

```yaml
# V themes/custom.yaml
my_date_theme:
  card-mod-card: |
    ha-card {
      font-family: 'Montserrat', 'Roboto', sans-serif;
    }
```

## Podpora

- [GitHub Issues](https://github.com/joshuaaaaa/HA---Datum/issues)
- [Home Assistant Community](https://community.home-assistant.io/)

## Licence

MIT License
