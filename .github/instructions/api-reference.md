# HZSULK API - Kompletní Dokumentace

## API Endpoint Zjištění

### Objeven
✅ **https://udalosti.hzsulk.cz/api/**

## Request

### HTTP Method
```
GET
```

### Query Parameters

| Parametr | Popis | Příklad | Povinný |
|----------|-------|---------|---------|
| `casOd` | Čas od (ISO 8601 UTC) | `2026-06-23T22:00:00.000Z` | Ano |
| `casDo` | Čas do (ISO 8601 UTC) | `2026-06-24T21:59:59.999Z` | Ano |
| `krajId` | ID kraje | `60` (Ústecký) | Ano |
| `stavIds` | Status IDs (repeatable) | `stavIds=210&stavIds=420` | Ano |

### Příklad Request URL
```
https://udalosti.hzsulk.cz/api/?casOd=2026-06-23T22:00:00.000Z&casDo=2026-06-24T21:59:59.999Z&krajId=60&stavIds=210&stavIds=400&stavIds=410&stavIds=420&stavIds=430&stavIds=440&stavIds=500&stavIds=510&stavIds=520&stavIds=600&stavIds=610&stavIds=620&stavIds=700&stavIds=710&stavIds=750&stavIds=760&stavIds=780&stavIds=800
```

### Headers
```
Accept: application/json
```

## Response

### Format
`application/json` - Array objektů

### Response Structure

```json
[
  {
    "id": 347488042,
    "casOhlaseni": "2026-06-24T21:36:12",
    "casVzniku": null,
    "stavId": 420,
    "typId": 3500,
    "podtypId": 3505,
    "poznamkaProMedia": "Odstranění větve z komunikace",
    "kraj": {
      "id": 60,
      "nazev": "Ústecký"
    },
    "okres": {
      "id": 3510,
      "nazev": "Ústí nad Labem"
    },
    "obec": "Povrly",
    "castObce": "Povrly",
    "ORP": "Ústí nad Labem",
    "ulice": null,
    "gis1": "754586",
    "gis2": "973505",
    "zoc": false,
    "silnice": null
  },
  // ... více objektů
]
```

### Response Fields

| Pole | Typ | Popis | Příklad |
|------|-----|-------|---------|
| `id` | number | Unikátní ID eventu | 347488042 |
| `casOhlaseni` | string (ISO8601) | Čas ohlášení | "2026-06-24T21:36:12" |
| `casVzniku` | string\|null | Čas vzniku (often null) | null |
| `stavId` | number | Status ID | 420 |
| `typId` | number | Type ID | 3500 |
| `podtypId` | number | Subtype ID | 3505 |
| `poznamkaProMedia` | string | Popis pro média | "Odstranění větve z..." |
| `kraj` | object | Region info | {"id": 60, "nazev": "Ústecký"} |
| `okres` | object | District info | {"id": 3510, "nazev": "Ústí nad Labem"} |
| `obec` | string | Municipality | "Povrly" |
| `castObce` | string | Part of municipality | "Povrly" |
| `ORP` | string | ORP (správní obvod) | "Ústí nad Labem" |
| `ulice` | string\|null | Street | null |
| `gis1` | string | GPS X coordinate | "754586" |
| `gis2` | string | GPS Y coordinate | "973505" |
| `zoc` | boolean | Zona ohrožené komunity? | false |
| `silnice` | string\|null | Road/Route | null |

## Status Codes

| stavId | Stav | Poznámka |
|--------|------|----------|
| 210 | TBD | ? |
| 400 | TBD | ? |
| 410 | TBD | ? |
| 420 | Otevřená | Open incident |
| 430 | TBD | ? |
| 440 | TBD | ? |
| 500 | TBD | ? |
| 510 | Uzavřená OS | Closed OS |
| 520 | TBD | ? |
| 600 | Převzatá VZ | Taken over by VZ |
| 610 | Uzavřená | Closed |
| 620 | TBD | ? |
| 700 | Ukončená | Finished |
| 710 | Ukončená ZPP | Finished ZPP |
| 750 | TBD | ? |
| 760 | TBD | ? |
| 780 | TBD | ? |
| 800 | Ukončená garantem za SSU | Finished by guarantor |

## Type IDs Reference

| typId | Typ | Podtypy |
|-------|-----|---------|
| 3100 | POŽÁR | 3103 (sláma), 3106 (tráva), 3109 (koš/popelnice), ... |
| 3200 | DOPRAVNÍ NEHODA | 3213 (bez zranění), 3214 (se zraněním), ... |
| 3400 | ÚNIK NEBEZPEČNÝCH LÁTEK | 3401 (kapaliny), ... |
| 3500 | TECHNICKÁ POMOC | 3501 (kouř), 3505 (strom), 3542 (hmyz), ... |
| 3550 | ZÁCHRANA OSOB A ZVÍŘAT | 3543 (transport), 10057 (otevření), ... |
| 3800 | PLANÝ POPLACH | 3811 (planý poplach), ... |

## Characteristics

### Authentication
✅ **Public API** - Žádná autentizace nepotřebná

### Rate Limiting
- **Frequency**: Frontend volá ~každých 60 sekund
- **Throttling**: Žádný explicitní rate limit (dosud)
- **CORS**: ✅ Funguje z frontendu

### Performance
- **Response Time**: ~100-200ms
- **Payload Size**: ~50-100KB (v závislosti na počtu events)
- **Data Freshness**: Reálný čas (real-time updates)

## Usage Notes

1. **Date Range**: Slouží k filtrování events v čase
   - Vždy uvádějte jak `casOd` tak `casDo`
   - ISO 8601 formát UTC

2. **Pagination**: 
   - Není implementováno
   - Předat celý rozsah dat v jedné request

3. **Caching**:
   - Frontend cachuje ~60 sekund
   - Pro HA integraci: polling každých 60 sekund je ideální

4. **Filters**:
   - `krajId`: Nutné specifika (60 = Ústecký)
   - `stavIds`: Lze filtrovat podle stavů
   - Nelze filtrovat podle `typId`

## Testing

### cURL Příklad
```bash
curl "https://udalosti.hzsulk.cz/api/?casOd=2026-06-23T22:00:00.000Z&casDo=2026-06-24T21:59:59.999Z&krajId=60&stavIds=210&stavIds=420"
```

### Python/aiohttp Příklad
```python
import aiohttp
from datetime import datetime, timedelta

async with aiohttp.ClientSession() as session:
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    
    params = {
        'casOd': yesterday.isoformat() + 'Z',
        'casDo': now.isoformat() + 'Z',
        'krajId': 60,  # Ústecký
        'stavIds': [210, 420, 510, 600, 610, 700, 710, 800]
    }
    
    async with session.get('https://udalosti.hzsulk.cz/api/', params=params) as resp:
        data = await resp.json()
        print(f"Events: {len(data)}")
```

## Next Steps
- Design HA integration based on this API
- Implement coordinator with aiohttp
- Create sensors for event types
