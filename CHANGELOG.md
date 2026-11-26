# Changelog

Všechny pozoruhodné změny v tomto projektu budou zdokumentovány v tomto souboru.

Formát je založen na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
a projekt se řídí [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.1] - 2026-11-26

### Fixed
- Karta: podkladová mapa se v HA nezobrazovala (OSM blokuje požadavky bez hlavičky Referer). Dlaždice se nově berou přes proxy jádra HA (`/api/map_tiles`, stejný zdroj jako vestavěná karta Mapa); na starších verzích HA přímo z OSM se správnou politikou Referer.

## [2.2.0] - 2026-11-26

### Added
- Lovelace karta `custom:hzsulk-events-card` přibalená k integraci (registruje se automaticky): mapa s malými ikonami a propojený seznam – klik na ikonu zvýrazní událost v seznamu a naopak, tlačítko pro detail entity, světlý i tmavý režim
- Volba „Celý kraj (bez omezení vzdálenosti)“
- Leaflet 1.9.4 (BSD-2-Clause) přibalený v `frontend/leaflet`

## [2.1.0] - 2026-11-26

### Changed
- Atribut `vehicles` je čitelný seznam techniky po jednotkách (dříve strukturovaná data)
- Ikony událostí podle podtypu (strom, výtah, popelnice, sanitka…)
- Příklad karty Mapa s ikonami místo zkratek

## [2.0.0] - 2026-11-26

### Changed
- Integrace přepracována: místo statistik zobrazuje jednotlivé události jako `geo_location` entity (mapa)
- Filtr podle okruhu kolem zvoleného místa (výchozí zóna Domov, 20 km), nastavitelné časové okno a režim „jen probíhající“
- Názvy typů, podtypů a stavů z číselníků API
- Čas ohlášení se správně interpretuje v místním čase (Europe/Prague)
- Minimální verze Home Assistant 2024.12

### Added
- Zasahující jednotky a technika (`/api/udalosti/{id}/technika`)
- Převod souřadnic S-JTSK → WGS84
- Binární senzor „Probíhá zásah v okolí“
- Možnosti (options flow) a podpora více míst
- Automatická migrace z verze 1

### Removed
- Statistické senzory (počty podle typu, celkem, poslední aktualizace)

## [1.0.0] - 2026-06-25

### Added
- Počty incidentů: Požáry, dopravní nehody, technická pomoc, záchrana osob, hazmat, falešné poplachy
- Celkový počet incidentů
- Binary sensor pro aktivní incidenty
- Last update sensor
- Integrace s Home Assistant 2024.6+
- MIT License
- GitHub issue templates
- Contributing guidelines
- Code of Conduct

### Features
- V1: Hardcoded region (Ústecký - krajId=60)
- 24hodinový lookback
- Všechny stavy incidentů zahrnuty (stavIds)
- Graceful NULL handling

---

Formát:

- **Added** – Pro nové funkcionality.
- **Changed** – Pro změny v existující funkcionalitě.
- **Deprecated** – Pro brzy odstraňované funkcionality.
- **Removed** – Pro odstraněné funkcionality.
- **Fixed** – Pro opravy chyb.
- **Security** – V případě zranitelností.
