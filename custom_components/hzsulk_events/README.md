# HZSULK Events - Home Assistant Custom Integration

Integrace pro Home Assistant, která zobrazuje v reálném čase informace o hasiči a záchranných akcích v Ústeckém kraji z webu [HZSULK](https://udalosti.hzsulk.cz/).

## Funkce (V1 MVP)

- **Počty incidentů by typu**: Požáry, dopravní nehody, technická pomoc, záchrana osob, únik nebezpečných látek, falešné poplachy, ostatní
- **Celkový počet incidentů**: Suma všech akcí
- **Detekce aktivních incidentů**: Binary sensor "Jsou aktivní incidenty?"
- **Poslední aktualizace**: Timestamp poslední synchronizace
- **Aktualizace**: Každých 60 sekund

## Instalace

1. Zkopíruj složku `custom_components/hzsulk_events` do `config/custom_components/` tvého Home Assistant
2. Restartuj Home Assistant
3. Přidej integraci v UI: Settings → Devices & Services → Create Automation → HZSULK Events

## Mapování Eventů

| typId | Popis |
|-------|-------|
| 3100 | Požár |
| 3200 | Dopravní nehoda |
| 3400 | Únik nebezpečných látek |
| 3500 | Technická pomoc |
| 3550 | Záchrana osob a zvířat |
| 3800 | Planý poplach |
| Ostatní | Ostatní incidenty |

## Architektura

- **coordinator.py**: Stahuje data z API a agreguje počty
- **sensor.py**: Vytváří sensors pro jednotlivé kategorie
- **binary_sensor.py**: Detekuje aktivní incidenty
- **const.py**: Konstanty a mapování
- **config_flow.py**: UI pro setup integrace

## API Reference

**Endpoint**: `https://udalosti.hzsulk.cz/api/`

**Parametry**:
- `casOd`: ISO 8601 UTC timestamp (od kdy)
- `casDo`: ISO 8601 UTC timestamp (do kdy)
- `krajId`: ID kraje (V1: 60 = Ústecký)
- `stavIds`: Stav incidentu (query param, vícekrát)

**V1 Default**: Poslednich 24 hodin, všechny stavy, pouze Ústecký kraj

## Budoucí Rozšíření (V2)

- Konfigurovatelný kraj/okres
- Filtrace dat na frontendu
- Podrobné informace o jednotlivých incidentech
- WebSocket support pro real-time updates
