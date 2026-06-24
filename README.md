# HZSULK Events - Home Assistant Integration

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Home Assistant custom integration pro zobrazení informací o hasiči a záchranných akcích v Ústeckém kraji v reálném čase.

Data pocházejí z veřejného API webu [HZSULK](https://udalosti.hzsulk.cz/).

## 🚀 Funkce (V1 MVP)

- **Agregované počty incidentů** – Požáry, dopravní nehody, technická pomoc, záchrana osob, únik nebezpečných látek, falešné poplachy, ostatní
- **Celkový počet incidentů** – Suma všech aktivních akcí
- **Detekce aktivních incidentů** – Binary sensor pro automatizace
- **Poslední aktualizace** – Timestamp poslední synchronizace
- **Automatické obnovování** – Každých 60 sekund

## 📋 Požadavky

- Home Assistant 2024.6 nebo novější
- Python 3.9+
- aiohttp 3.8.0+

## 📦 Instalace

### Manuálně

1. Klonuj repository:
   ```bash
   git clone https://github.com/tvoje-uzivatelske-jmeno/HZSULK-udalosti.git
   cd HZSULK-udalosti
   ```

2. Zkopíruj integraci do Home Assistant:
   ```bash
   cp -r custom_components/hzsulk_events ~/.homeassistant/custom_components/
   ```

3. Restartuj Home Assistant

4. Přidej integraci:
   - Jdi do **Settings → Devices & Services**
   - Klikni na **Create Automation**
   - Hledej **HZSULK Events**
   - Klikni **Create Entry**

### Přes HACS (plánováno)

```
HACS → Integrations → Explore & Download Repositories → HZSULK Events
```

## 🔌 Dostupné Entity

### Sensors (počty incidentů)

- `sensor.hzsulk_events_fires` – Požáry
- `sensor.hzsulk_events_accidents` – Dopravní nehody
- `sensor.hzsulk_events_hazmat` – Únik nebezpečných látek
- `sensor.hzsulk_events_technical_help` – Technická pomoc
- `sensor.hzsulk_events_rescues` – Záchrana osob a zvířat
- `sensor.hzsulk_events_false_alarms` – Falešné poplachy
- `sensor.hzsulk_events_other` – Ostatní incidenty
- `sensor.hzsulk_events_total` – Celkem incidentů
- `sensor.hzsulk_events_last_update` – Poslední aktualizace

### Binary Sensors

- `binary_sensor.hzsulk_events_active_incidents` – Jsou aktivní incidenty?

## 🎨 Příklad v automacích

```yaml
# Oznamení, když dojde k požáru
automation:
  - alias: "Upozornění na požár"
    trigger:
      platform: state
      entity_id: sensor.hzsulk_events_fires
      from: "0"
    action:
      service: notify.pushbullet
      data:
        message: "Nový požár v Ústeckém kraji!"

# Upozornění na aktivní incidenty
automation:
  - alias: "Aktivní incidenty"
    trigger:
      platform: state
      entity_id: binary_sensor.hzsulk_events_active_incidents
      to: "on"
    action:
      service: logbook.log
      data:
        name: "Hasiči v akci"
        message: "Detekován nový incident"
```

## 🏗️ Architektura

```
custom_components/hzsulk_events/
├── __init__.py           # Integration entry point
├── const.py              # Konstanty a mapování
├── coordinator.py        # API coordinator
├── config_flow.py        # Setup UI
├── sensor.py             # Sensor entity definitions
├── binary_sensor.py      # Binary sensor entity
├── manifest.json         # Integration metadata
├── strings.json          # Localization
└── README.md             # Integration documentation
```

## 🔄 API Reference

**Endpoint**: `https://udalosti.hzsulk.cz/api/`

**V1 Parametry**:
- `casOd` – ISO 8601 UTC (od kdy)
- `casDo` – ISO 8601 UTC (do kdy)
- `krajId` – ID kraje (V1: 60 = Ústecký)
- `stavIds` – Stavy incidentů (query param, vícekrát)

## 🚧 Budoucí Rozšíření (V2+)

- [ ] Konfigurovatelný kraj/okres
- [ ] Filtrace dat na frontendu
- [ ] Podrobné informace o jednotlivých incidentech
- [ ] WebSocket support pro real-time updates
- [ ] HACS integrace
- [ ] Jednotky a složitější filtrování

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

Máš problém? Otevři [issue na GitHubu](https://github.com/tvoje-uzivatelske-jmeno/HZSULK-udalosti/issues).

---

Made with ❤️ for Home Assistant enthusiasts
