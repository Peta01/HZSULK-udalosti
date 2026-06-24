"""Константы для HZSULK Events интеграции."""

# API
API_BASE_URL = "https://udalosti.hzsulk.cz/api/"

# V1: Hardcoded values
DEFAULT_REGION_ID = 60  # Ústecký

# Status IDs (stavIds) - všechny stavy (otevřené + uzavřené)
DEFAULT_STATUS_IDS = [
    210, 400, 410, 420, 430, 440, 500,  # Otevřené
    510, 520, 600, 610, 620, 700, 710, 750, 760, 780, 800  # Uzavřené
]

# Event Types (typIds)
EVENT_TYPE_FIRE = 3100  # POŽÁR
EVENT_TYPE_ACCIDENT = 3200  # DOPRAVNÍ NEHODA
EVENT_TYPE_HAZMAT = 3400  # ÚNIK NEBEZPEČNÝCH LÁTEK
EVENT_TYPE_TECHNICAL_HELP = 3500  # TECHNICKÁ POMOC
EVENT_TYPE_RESCUE = 3550  # ZÁCHRANA OSOB A ZVÍŘAT
EVENT_TYPE_FALSE_ALARM = 3800  # PLANÝ POPLACH
EVENT_TYPE_OTHER = [3700, 3600, 3900, 5000]  # Ostatní

EVENT_TYPES = {
    EVENT_TYPE_FIRE: "POŽÁR",
    EVENT_TYPE_ACCIDENT: "DOPRAVNÍ NEHODA",
    EVENT_TYPE_HAZMAT: "ÚNIK NEBEZPEČNÝCH LÁTEK",
    EVENT_TYPE_TECHNICAL_HELP: "TECHNICKÁ POMOC",
    EVENT_TYPE_RESCUE: "ZÁCHRANA OSOB A ZVÍŘAT",
    EVENT_TYPE_FALSE_ALARM: "PLANÝ POPLACH",
}

# Domain
DOMAIN = "hzsulk_events"

# Default update interval (seconds)
DEFAULT_UPDATE_INTERVAL = 60

# Timeframe for events (hours)
DEFAULT_HOURS_LOOKBACK = 24
