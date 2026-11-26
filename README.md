# HZSULK Events - Home Assistant Integration

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Home Assistant custom integrace, která zobrazuje **jednotlivé zásahy hasičů v Ústeckém kraji** v okruhu kolem zvoleného místa. U každé události ukáže typ, stav, popis, adresu, polohu na mapě a zasahující jednotky s technikou.

Data pocházejí z veřejného API webu [udalosti.hzsulk.cz](https://udalosti.hzsulk.cz/) (HZS Ústeckého kraje).

## 🚀 Funkce

- **Každá událost jako entita na mapě** (`geo_location`): zobrazí se na kartě Mapa, stav entity je vzdálenost v km
- **Podrobnosti v atributech**: typ a podtyp, stav, popis pro média, adresa, čas ohlášení, zasahující jednotky a technika
- **Filtr podle okruhu** kolem zóny Domov nebo libovolného bodu na mapě
- **Binární senzor „Probíhá zásah v okolí“** pro automatizace
- Ukončené události zmizí po uplynutí časového okna (výchozí 24 h), probíhající se zobrazují vždy
- Aktualizace každých 60 s; jednotky se u probíhajících událostí obnovují každých 5 minut

Integraci lze přidat vícekrát, např. pro domov a chalupu.

## 📋 Požadavky

- Home Assistant 2024.12 nebo novější

## 📦 Instalace přes HACS

1. Otevři HACS v Home Assistant.
2. Zvol **Custom repositories** a přidej tento repozitář jako **Integration**.
3. Nainstaluj **HZSULK Events** a restartuj Home Assistant.
4. V **Nastavení → Zařízení a služby** přidej integraci **HZSULK Events**.
5. Zvol název místa, střed a okruh na mapě, časové okno a zda zobrazovat jen probíhající události.

Nastavení jde později změnit tlačítkem **Konfigurovat** u integrace.

## 🔌 Entity

### `geo_location.*` – jednotlivé události

Název např. `Požár – nízké budovy, Klášterec nad Ohří`, stav = vzdálenost od středu v km. Ikona odpovídá podtypu (strom, výtah, popelnice, sanitka…).

| Atribut | Popis |
|---|---|
| `event_id` | ID události v systému HZS |
| `reported` | Čas ohlášení |
| `type`, `subtype` | Typ a podtyp (např. POŽÁR / NÍZKÉ BUDOVY) |
| `status`, `active` | Stav (např. „Otevřená, SaP na místě“) a zda událost probíhá |
| `description` | Popis pro média (nemusí být vyplněn) |
| `address`, `municipality`, `municipality_part`, `street`, `road`, `district`, `orp` | Místo |
| `units` | Seznam zasahujících jednotek |
| `vehicles` | Technika po jednotkách, např. `HS Šluknov: cisternová automobilová stříkačka < 30, 2× dopravní automobil` |
| `latitude`, `longitude`, `source` | Poloha (`source: hzsulk_events`) |

Entity vznikají a zanikají automaticky podle aktuálních dat.

### `binary_sensor.*_probiha_zasah_v_okoli`

Zapnutý, pokud v okruhu probíhá alespoň jedna událost. Atributy: `active_count`, `events_count`, `radius_km`, `active_events` (seřazené podle vzdálenosti).

## 🗺️ Karta Mapa

```yaml
type: map
geo_location_sources:
  - source: hzsulk_events
    label_mode: icon
entities:
  - zone.home
hours_to_show: 0
```

## 📝 Seznam událostí (Markdown karta)

```yaml
type: markdown
content: >
  {% for s in states.geo_location
       | selectattr('attributes.source', 'eq', 'hzsulk_events')
       | sort(attribute='attributes.reported', reverse=true) %}
  **{{ s.name }}** – {{ s.state }} km{{ ' 🔴' if s.attributes.active }}
  {{ as_timestamp(s.attributes.reported) | timestamp_custom('%d.%m. %H:%M') }} · {{ s.attributes.status }}
  {% if s.attributes.description %}_{{ s.attributes.description }}_{% endif %}
  {% for v in s.attributes.vehicles %}🚒 {{ v }}
  {% endfor %}

  {% else %}
  V okolí nejsou žádné události.
  {% endfor %}
```

## 🎨 Automatizace: upozornění na nový zásah v okolí

```yaml
automation:
  - alias: "Zásah hasičů do 5 km"
    triggers:
      - trigger: geo_location
        source: hzsulk_events
        zone: zone.home
        event: enter
    actions:
      - action: notify.mobile_app_telefon
        data:
          title: "🚒 {{ trigger.to_state.name }}"
          message: >
            {{ trigger.to_state.state }} km ·
            {{ trigger.to_state.attributes.description or trigger.to_state.attributes.status }}
```

Trigger `geo_location` reaguje na události uvnitř zóny (např. `zone.home` s poloměrem 5 km). Okruh integrace může být větší, třeba pro mapu.

## 🏗️ Architektura

```
custom_components/hzsulk_events/
├── __init__.py       # Setup, migrace z verze 1
├── api.py            # Klient API udalosti.hzsulk.cz
├── coordinator.py    # Stahování, filtr okruhu, doplnění jednotek
├── geo.py            # Převod S-JTSK → WGS84
├── geo_location.py   # Entity jednotlivých událostí
├── binary_sensor.py  # Probíhá zásah v okolí
├── config_flow.py    # Nastavení a možnosti
└── translations/     # cs, en
```

## 🔄 API

Základ: `https://udalosti.hzsulk.cz/api/`

| Endpoint | Obsah |
|---|---|
| `?casOd=…&casDo=…&krajId=60&stavIds=…` | Seznam událostí (čas `casOhlaseni` je v místním čase) |
| `udalosti/{id}/technika` | Zasahující jednotky a technika |
| `typy`, `podtypy`, `stavy`, `okresy` | Číselníky |

Souřadnice `gis1`/`gis2` jsou v S-JTSK (Y, X) a integrace je přepočítává na WGS84.

## 🤝 Přispívání

Vítáme pull requesty! Prosím:

1. Fork projekt
2. Vytvoř feature branch (`git checkout -b feature/nova-funkcionalita`)
3. Commituj změny (`git commit -am 'Přidej novou funkcionalitu'`)
4. Push na branch (`git push origin feature/nova-funkcionalita`)
5. Otevři Pull Request

Více informací v [CONTRIBUTING.md](CONTRIBUTING.md).

## 📝 Licence

Projekt je licencován pod [MIT License](LICENSE).

## ⚠️ Disclaimer

Tato integrace není oficiálně součástí Home Assistant nebo HZSULK. Údaje jsou čerpány z veřejného API a mohou podléhat podmínkám HZSULK.

## 🆘 Podpora

Máš problém? Otevři [issue na GitHubu](https://github.com/Peta01/HZSULK-udalosti/issues).

---

Made with ❤️ for Home Assistant enthusiasts
