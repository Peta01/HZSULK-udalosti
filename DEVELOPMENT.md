# Návod na vývoj

Chceš přispívat vývoji? Super! Tento dokument ti ukáže, jak si nastavit dev prostředí.

## Požadavky

- Python 3.9+
- Home Assistant (místní instalace nebo dev instance)
- Git

## Nastavení Dev Prostředí

### 1. Clone projekt

```bash
git clone https://github.com/tvoje-uzivatelske-jmeno/HZSULK-udalosti.git
cd HZSULK-udalosti
```

### 2. Vytvoř virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo
venv\Scripts\activate  # Windows
```

### 3. Instaluj dev závislosti

```bash
pip install -r requirements-dev.txt
```

### 4. Kopíruj integraci do Home Assistant

Předpokládá se, že máš Home Assistant running na `~/.homeassistant`:

```bash
cp -r custom_components/hzsulk_events ~/.homeassistant/custom_components/
```

### 5. Restartuj Home Assistant

```bash
# Pokud máš HA v kontejneru
docker restart homeassistant

# Nebo přes UI: Settings → System → System Options → Restart
```

## Vývoj

### Struktura

```
custom_components/hzsulk_events/
├── __init__.py           # Integration entry point
├── const.py              # Konstanty
├── coordinator.py        # API coordinator
├── config_flow.py        # Setup UI
├── sensor.py             # Sensor definitions
├── binary_sensor.py      # Binary sensor
└── manifest.json         # Metadata
```

### Typický workflow

1. Vytvoř feature branch: `git checkout -b feature/tvoje-feature`
2. Edituj kód
3. Restartuj HA (Settings → System → System Options → Restart)
4. Ověř chování v UI
5. Spusť linting: `flake8 custom_components/hzsulk_events`
6. Commit: `git commit -am "feat: Popis"`
7. Push: `git push origin feature/tvoje-feature`
8. Otevři Pull Request

## Linting & Formátování

### Flake8 (Style)

```bash
flake8 custom_components/hzsulk_events --max-line-length=100
```

### MyType (Type checking)

```bash
mypy custom_components/hzsulk_events --ignore-missing-imports
```

### Black (Formatting)

```bash
black custom_components/hzsulk_events
```

### isort (Import sorting)

```bash
isort custom_components/hzsulk_events
```

## Debugging

### 1. Enable Debug Logging

V Home Assistant `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.hzsulk_events: debug
```

### 2. Watch Logs

```bash
# Pokud máš HA v kontejneru
docker logs -f homeassistant | grep hzsulk_events
```

### 3. Developer Tools

Používej Developer Tools v HA UI:
- Services: Testuj coordinator
- Statistics: Sleduj sensor hodnoty
- Developer Mode (F12): Console logs

## Testování

```bash
# Run tests (až budou implementovány)
pytest

# S coverage
pytest --cov=custom_components/hzsulk_events
```

## Časté Problémy

### "Integration not found"

Zkontroluj, že:
1. Složka je v `~/.homeassistant/custom_components/`
2. Soubor `manifest.json` je přítomný
3. Restartl jsi HA

### "Module not found: aiohttp"

```bash
pip install aiohttp
```

### "Coordinator data is None"

Check:
1. API je dostupný? `curl https://udalosti.hzsulk.cz/api/`
2. Logs v Developer Tools
3. Network tab v DevTools

## Otázky?

Napiš issue nebo se zeptej v Pull Request! 💙

---

Happy coding! 🚀
