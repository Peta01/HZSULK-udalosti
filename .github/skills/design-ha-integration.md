---
title: Design HA Integration
description: Design Home Assistant custom integration for HZSULK events
applyTo: 
  - HA integration design
  - Entity planning
  - Dashboard design
---

# Design HA Integration

## Prerequisites
- API endpoint discovered (see discover-api.md)
- Data structure understood
- Decision made: Custom Integration vs REST binding

## Design Steps

### 1. Define HA Entities

#### Option A: Aggregated Sensors (Simple)
Best for: Dashboard summary view

```yaml
# Count sensors per event type
sensor.hzsulk_fires_count          # Počet požárů
sensor.hzsulk_accidents_count      # Počet nehod
sensor.hzsulk_technical_help_count # Počet technických pomocí
sensor.hzsulk_rescues_count        # Počet záchrany osob
sensor.hzsulk_false_alarms_count   # Počet falešných poplachů

# Status sensors
binary_sensor.hzsulk_incidents_active  # Je něco aktivního?
sensor.hzsulk_last_update              # Čas poslední aktualizace
sensor.hzsulk_total_incidents          # Celkový počet event
```

#### Option B: Event List (Detailed)
Best for: Detailed history, automation

```yaml
# Main event list
sensor.hzsulk_latest_events  # JSON array posledních N событ

# Top incidents
sensor.hzsulk_latest_fire         # Poslední požár
sensor.hzsulk_latest_accident     # Poslední nehoda
sensor.hzsulk_active_incidents    # Všechny aktivní events
```

#### Option C: Individual Event Entities (Full)
Best for: Individual automation per event

```yaml
event.hzsulk_incident_001  # Konkrétní event s detaily
event.hzsulk_incident_002
```

### 2. Custom Integration Structure

```
custom_components/
  hzsulk_events/
    __init__.py           # Entry point, setup
    manifest.json         # Integration metadata
    strings.json          # Localization
    config_flow.py        # Configuration UI (if needed)
    coordinator.py        # Data fetching (CoordinatorEntity pattern)
    sensor.py            # Sensor entities
    binary_sensor.py     # Binary sensor entities
    const.py             # Constants
```

### 3. Implementation Pattern

#### manifest.json
```json
{
  "domain": "hzsulk_events",
  "name": "HZSULK Events",
  "codeowners": ["@username"],
  "config_flow": true,
  "documentation": "https://github.com/...",
  "requirements": ["aiohttp>=3.8.0"],
  "version": "1.0.0",
  "homeassistant": "2024.6.0"
}
```

#### __init__.py Pattern
```python
async def async_setup(hass, config):
    # Create coordinator for data fetching
    coordinator = HZSULKDataUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True
```

#### Coordinator Pattern
```python
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

class HZSULKDataUpdateCoordinator(DataUpdateCoordinator):
    async def _async_update_data(self):
        # Fetch from API
        data = await self.hass.helpers.aiohttp_client.async_get_clientsession().get(
            API_URL
        )
        return await data.json()
```

### 4. Data Update Strategy

```
┌─────────────────┐
│  HA Coordinator │ (update every 60s)
├─────────────────┤
│  Fetch API      │
│  Parse JSON     │
│  Update entities│
└────────┬────────┘
         │
         ↓
   ┌──────────────────────────┐
   │  Sensor entities:        │
   │  - Count sensors         │
   │  - Last update time      │
   │  - Status summary        │
   └──────────────────────────┘
```

### 5. Configuration Options

```yaml
# configuration.yaml example
hzsulk_events:
  update_interval: 60  # seconds
  regions: ["Ústecký"]  # Filter by region
  show_types:
    - POŽÁR
    - DOPRAVNÍ NEHODA
    - TECHNICKÁ POMOC
    - ÚNIK NEBEZPEČNÝCH LÁTEK
    - PLANÝ POPLACH
    - ZÁCHRANA OSOB A ZVÍŘAT
  max_events: 50  # Keep last N events
```

## Deliverables

- [ ] Entity design document (YAML structure)
- [ ] Integration structure plan
- [ ] Code architecture diagram
- [ ] Configuration schema
- [ ] Update strategy flowchart
- [ ] Ready for implementation

## Next: Implementation
See: implement-ha-integration.md
