"""Konstanty integrace HZSULK Events."""

from __future__ import annotations

DOMAIN = "hzsulk_events"

ATTRIBUTION = "Data: HZS Ústeckého kraje (udalosti.hzsulk.cz)"
WEB_URL = "https://udalosti.hzsulk.cz/"

# Lovelace karta přibalená k integraci
FRONTEND_URL = "/hzsulk_events_static"
CARD_FILENAME = "hzsulk-events-card.js"

# API
API_BASE_URL = "https://udalosti.hzsulk.cz/api/"
API_TIMEOUT = 15
REGION_ID = 60  # Ústecký kraj (aplikace HZS ÚK)
TIMEZONE = "Europe/Prague"  # API vrací čas ohlášení v místním čase

# Konfigurace
CONF_HOURS = "hours"
CONF_ONLY_ACTIVE = "only_active"
CONF_WHOLE_REGION = "whole_region"

DEFAULT_RADIUS_KM = 20
DEFAULT_HOURS = 24
DEFAULT_ONLY_ACTIVE = False
DEFAULT_WHOLE_REGION = False
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
    3400: "mdi:barrel-outline",
    3500: "mdi:tools",
    3550: "mdi:lifebuoy",
    3600: "mdi:file-document-outline",
    3700: "mdi:alert-circle-outline",
    3800: "mdi:alarm-light-off-outline",
    3900: "mdi:test-tube",
    5000: "mdi:office-building-marker",
}

# Přesnější ikony podle podtypu (číselník /api/podtypy)
SUBTYPE_ICONS = {
    # Požár
    3101: "mdi:home-alert",
    3102: "mdi:office-building",
    3103: "mdi:factory",
    3104: "mdi:account-group",
    3105: "mdi:tunnel",
    3106: "mdi:grass",
    3107: "mdi:transmission-tower",
    3108: "mdi:car",
    3109: "mdi:delete",
    3110: "mdi:pine-tree-fire",
    3111: "mdi:delete-variant",
    3112: "mdi:barn",
    3113: "mdi:delete-variant",
    3114: "mdi:flask",
    3115: "mdi:hospital-building",
    3116: "mdi:cable-data",
    3117: "mdi:fireplace",
    10035: "mdi:smoke-detector-alert",
    # Dopravní nehoda
    3211: "mdi:car-wrench",
    3212: "mdi:tow-truck",
    3213: "mdi:road-variant",
    3214: "mdi:car-emergency",
    3215: "mdi:bus-alert",
    3231: "mdi:train",
    3241: "mdi:airplane-alert",
    # Únik nebezpečných látek
    3401: "mdi:oil",
    3402: "mdi:barrel-outline",
    3403: "mdi:water-alert",
    3404: "mdi:weather-windy",
    # Technická pomoc
    3501: "mdi:alert",
    3502: "mdi:handshake",
    3503: "mdi:home-remove",
    3504: "mdi:cog",
    3505: "mdi:pine-tree",
    3525: "mdi:door-open",
    3526: "mdi:sign-caution",
    3527: "mdi:water-pump",
    3528: "mdi:gauge",
    3541: "mdi:binoculars",
    3542: "mdi:bee",
    10056: "mdi:door-open",
    # Záchrana osob a zvířat
    3521: "mdi:waves",
    3522: "mdi:ladder",
    3523: "mdi:elevator-passenger",
    3524: "mdi:hard-hat",
    3529: "mdi:arrow-collapse-down",
    3530: "mdi:heart-pulse",
    3531: "mdi:terrain",
    3533: "mdi:hospital-box",
    3543: "mdi:ambulance",
    10057: "mdi:elevator-passenger",
    # Ostatní
    3602: "mdi:weather-lightning-rainy",
    3611: "mdi:radioactive",
    3711: "mdi:exit-run",
    3713: "mdi:traffic-light",
    3931: "mdi:phone-alert",
}
DEFAULT_ICON = "mdi:fire-truck"
