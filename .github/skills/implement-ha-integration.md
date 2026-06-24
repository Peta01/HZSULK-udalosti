---
title: Implement HA Integration
description: Step-by-step implementation of Home Assistant custom integration for HZSULK events
---

# Implement HA Integration

## Prerequisites
- Design completed (see design-ha-integration.md)
- API endpoint known and tested
- Development environment: VS Code + devcontainer (Node.js 22 + .NET 10)

## Directory Structure

```
HZSULK-udalosti/
├── custom_components/
│   └── hzsulk_events/
│       ├── __init__.py
│       ├── manifest.json
│       ├── strings.json
│       ├── const.py
│       ├── coordinator.py
│       ├── sensor.py
│       ├── binary_sensor.py
│       └── config_flow.py
├── tests/
│   ├── test_coordinator.py
│   ├── test_sensor.py
│   └── fixtures/
│       └── sample_api_response.json
├── README.md
└── .github/
    └── workflows/
        └── tests.yml
```

## Implementation Phases

### Phase 1: Core Files

#### 1.1 manifest.json
- Define integration metadata
- Specify dependencies (aiohttp, etc.)
- Set minimum Home Assistant version

#### 1.2 const.py
- API URLs and endpoints
- Update intervals
- Entity naming constants
- Event type classifications

#### 1.3 __init__.py
- Setup coordinator
- Load/unload logic
- Entry management

### Phase 2: Data Fetching

#### 2.1 coordinator.py
Implement `DataUpdateCoordinator`:
- `_async_update_data()` - fetch from API
- Error handling
- Rate limiting
- Data caching

#### 2.2 API client methods
- `async_get_events()` - fetch all events
- `async_get_event_by_type()` - filter by type
- `async_parse_response()` - normalize data

### Phase 3: Entities

#### 3.1 sensor.py
```python
class HZSULKEventCountSensor(CoordinatorEntity, SensorEntity):
    # Implement count sensor for event types
    
class HZSULKLastUpdateSensor(CoordinatorEntity, SensorEntity):
    # Track last update time
    
class HZSULKEventsSensor(CoordinatorEntity, SensorEntity):
    # JSON list of all events
```

#### 3.2 binary_sensor.py
```python
class HZSULKIncidentsActiveBinarySensor(CoordinatorEntity, BinarySensorEntity):
    # On if any incidents active
```

### Phase 4: Configuration

#### 4.1 config_flow.py
- Manual entry configuration
- Optional: region/type filters
- Validation

#### 4.2 strings.json
- Localization for config options
- Entity names and descriptions

## Code Quality

### Testing
- Unit tests for coordinator
- Mock API responses
- Fixtures for sample data
- Test helpers and utilities

### Documentation
- Installation instructions
- Configuration examples
- Dashboard examples
- Troubleshooting

## Implementation Checklist

- [ ] Directory structure created
- [ ] manifest.json defined
- [ ] const.py with all constants
- [ ] __init__.py with coordinator setup
- [ ] coordinator.py with API fetching
- [ ] sensor.py with entity definitions
- [ ] binary_sensor.py entities
- [ ] config_flow.py setup
- [ ] strings.json localization
- [ ] Unit tests written
- [ ] Integration tests written
- [ ] README with install instructions
- [ ] GitHub Actions workflow for tests
- [ ] HACS compatibility verified
- [ ] Documentation completed

## Development Workflow

1. **Setup**: Create directory structure
2. **API**: Implement API client in coordinator
3. **Entities**: Create sensor entities
4. **Test**: Write and run unit tests
5. **Integration**: Test in real HA instance
6. **Polish**: Add config UI, docs, examples
7. **Release**: Tag version, push to GitHub

## Testing Commands

```bash
# Run unit tests
pytest tests/

# Run specific test
pytest tests/test_coordinator.py::test_fetch_events

# Coverage report
pytest --cov=custom_components/hzsulk_events tests/
```

## Reference

- HA Custom Component Development: https://developers.home-assistant.io/
- CoordinatorEntity Pattern: https://developers.home-assistant.io/docs/integration_fetching_data
- Sensor Integration: https://developers.home-assistant.io/docs/core/entity/sensor
- Binary Sensor Integration: https://developers.home-assistant.io/docs/core/entity/binary-sensor

## Success Criteria

✅ Integration loads in HA without errors
✅ Entities appear in HA (Developer Tools → States)
✅ Data updates automatically every 60s
✅ No errors in HA logs
✅ Dashboard displays event counts
✅ Unit tests pass with >80% coverage
✅ Documentation is complete
✅ HACS compatible
