"""Konstanty integrace HZSULK Events."""

from __future__ import annotations

DOMAIN = "hzsulk_events"

ATTRIBUTION = "Data: HZS Ústeckého kraje (udalosti.hzsulk.cz)"
WEB_URL = "https://udalosti.hzsulk.cz/"

# API
API_BASE_URL = "https://udalosti.hzsulk.cz/api/"
API_TIMEOUT = 15
REGION_ID = 60  # Ústecký kraj (aplikace HZS ÚK)
TIMEZONE = "Europe/Prague"  # API vrací čas ohlášení v místním čase

# Konfigurace
CONF_HOURS = "hours"
CONF_ONLY_ACTIVE = "only_active"

DEFAULT_RADIUS_KM = 20
DEFAULT_HOURS = 24
DEFAULT_ONLY_ACTIVE = False
DEFAULT_UPDATE_INTERVAL = 60  # sekundy

# Probíhající události bez ohledu na časové okno sledujeme až do tohoto stáří
MAX_ACTIVE_AGE_HOURS = 72

# Jednotky/techniku probíhající události obnovujeme nejvýš jednou za tuto dobu
UNITS_REFRESH_SECONDS = 300
UNITS_MAX_PARALLEL = 5

# Stavy událostí (číselník /api/stavy)
STATUS_IDS_ACTIVE = [
    100,  # Čekající na odbavení
    110,  # Čekající - přečteno
    200,  # Inicializovaná
    210,  # Převzatá
    400,  # Otevřená, bez SaP
    410,  # Otevřená SaP na cestě
    420,  # Otevřená, SaP na místě
    430,  # Lokalizovaná
    440,  # Likvidovaná
]
STATUS_IDS_FINISHED = [
    450,  # Odjezd poslední jednotky
    500,  # Ukončená OS
    510,  # Uzavřená OS
    520,  # Exportovaná do SK
    600,  # Převzatá VZ
    610,  # Ukončená VZ
    620,  # Exportovaná ZOZ Online
    700,  # Převzatá ZPP
    710,  # Ukončená ZPP
    750,  # Převzatá garantem za SSU
    760,  # Ukončená garantem za SSU
    780,  # Potvrzená krajským garantem
    800,  # Připravená k archivaci
]

# Záložní názvy, pokud se nepodaří načíst číselníky z API
FALLBACK_TYPES = {
    3100: "POŽÁR",
    3200: "DOPRAVNÍ NEHODA",
    3400: "ÚNIK NEBEZPEČNÝCH LÁTEK",
    3500: "TECHNICKÁ POMOC",
    3550: "ZÁCHRANA OSOB A ZVÍŘAT",
    3600: "FORMÁLNĚ ZALOŽENÁ UDÁLOST",
    3700: "JINÁ UDÁLOST",
    3800: "PLANÝ POPLACH",
    3900: "TECHNOLOGICKÝ TEST",
    5000: "UDÁLOST NA OBJEKT",
}

TYPE_ICONS = {
    3100: "mdi:fire",
    3200: "mdi:car-emergency",
    3400: "mdi:biohazard",
    3500: "mdi:tools",
    3550: "mdi:lifebuoy",
    3800: "mdi:alarm-light-off-outline",
}
DEFAULT_ICON = "mdi:fire-truck"
