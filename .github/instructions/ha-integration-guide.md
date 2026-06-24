# HA Integrace: HZSULK Události

## Cíl
Vytvořit Home Assistant integraci, která zobrazuje aktuální hasiče/záchranné akce (HZSULK - events) na HA dashboardu.

## Zdrojová data

### Web
- **URL**: https://udalosti.hzsulk.cz/
- **Typ**: Veřejná webová aplikace s tabulkou event
- **Aktualizace**: Každých ~60 sekund

### Data struktura
Každá událost (event) obsahuje:
- **Čas**: 24.6.2026 21:36 (datum a čas)
- **Stav**: Otevřená, Uzavřená, Lokalizovaná, Prevzatá, Ukončená, atd.
- **Typ**: POŽÁR, TECHNICKÁ POMOC, DOPRAVNÍ NEHODA, PLANÝ POPLACH, ÚNIK NEBEZPEČNÝCH LÁTEK, ZÁCHRANA OSOB A ZVÍŘAT
- **Detaily typu**: Specifičtější klasifikace (POŽÁR → ODPAD OSTATNÍ, POLNÍ POROST, POPELNICE, atd.)
- **Kraj**: Ústecký
- **Okres**: Chomutov, Děčín, Litoměřice, Most, Teplice, Ústí nad Labem, Louny
- **Město/Obec**: Lokace
- **Ulice**: Konkrétní lokace (CAN BE NULL)
- **Popis**: Textový popis akce (CAN BE NULL - viz event z 20:03!)
- **GPS**: Souřadnice (SJTSK)
- **Počet**: Odhadovaný počet věcí (míst, vozů, osob)

### Príklad data struktury
```
{
  "timestamp": "24.6.2026 21:36",
  "status": "Otevřená, SaP na místě",
  "type": "TECHNICKÁ POMOC",
  "type_detail": "ODSTRANĚNÍ STROMU",
  "region": "Ústecký",
  "district": "Ústí nad Labem",
  "city": "Ústí nad Labem",
  "place": "Povrly",
  "street": "Povrly",
  "description": "Odtsranění větve z..."
}
```

## Technické informace

### Stack projektu
- **Backend**: .NET 10.0
- **Frontend**: Node.js 22 (React, Next.js apod. - TBD)
- **Container**: devcontainer s .NET + Node.js
- **CI/CD**: GitHub (GitHub Actions)

### Architektura HA integrace
Možnosti:
1. **Python Custom Integration** - Python package instalovatelný přes HACS
   - Vhodné pro: Dlouhodobá údržba, plný přístup k HA API
   - Složitost: Středně vysoká
   
2. **REST/HTTP binding** - Přímé volání z HA do externího API
   - Vhodné pro: Rychlá integrace, minimální údržba
   - Složitost: Nízká

## API Endpoint (Zjištěno ✅)

### URL
```
GET https://udalosti.hzsulk.cz/api/
```

### Query Parameters
```
casOd=2026-06-23T22:00:00.000Z        # Čas od (ISO datetime)
casDo=2026-06-24T21:59:59.999Z        # Čas do (ISO datetime)
krajId=60                              # ID kraje (60=Ústecký)
stavIds=210&stavIds=400&...            # Array stavů (status IDs)
```

### Response
Array JSON objektů s events. Příklad jednoho eventu:

```json
{
  "id": 347488042,
  "casOhlaseni": "2026-06-24T21:36:12",     // čas ohlášení
  "casVzniku": null,                        // čas vzniku (Often null)
  "stavId": 420,                            // status ID
  "typId": 3500,                            // type ID
  "podtypId": 3505,                         // sub-type ID
  "poznamkaProMedia": "Odstranění větve z komunikace",  // popis pro média
  "kraj": {"id": 60, "nazev": "Ústecký"},
  "okres": {"id": 3510, "nazev": "Ústí nad Labem"},
  "obec": "Povrly",                         // obec
  "castObce": "Povrly",                     // část obce
  "ORP": "Ústí nad Labem",                  // ORP
  "ulice": null,                            // ulice
  "gis1": "754586",                         // GPS X
  "gis2": "973505",                         // GPS Y
  "zoc": false,                             // zona ohrožené komunity?
  "silnice": null                           // silnice/trasa
}
```

### Authentication
- ✅ **ŽÁDNÉ** - Veřejný API, bez autentizace

### Rate Limiting
- Frontend volá API každých ~60 sekund
- Bez explicitního rate limitingu (prozatím bez CORS omezení)

### Status IDs (stavIds) Reference
| ID | Stav |
|---|---|
| 210 | ? |
| 400 | ? |
| 410 | ? |
| 420 | Otevřená |
| 430 | ? |
| 440 | ? |
| 500 | ? |
| 510 | Uzavřená OS |
| 520 | ? |
| 600 | Převzatá VZ |
| 610 | Uzavřená (jiný stav) |
| 620 | ? |
| 700 | Ukončená (stav) |
| 710 | Ukončená ZPP |
| 750 | ? |
| 760 | ? |
| 780 | ? |
| 800 | Ukončená garantem |

## Kroky k implementaci

### Fáze 1: Zjištění API ✅
- [x] Najít exaktní API endpoint (network analysis - DevTools)
- [x] Zmapovat request/response strukturu
- [x] Zjistit authentication (NENÍ potřeba)
- [x] Zjistit rate limiting (~60s polling)

### Fáze 2: Návrh HA integrace
- [ ] Zvolit typ integrace (Custom Integration vs REST)
- [ ] Navrhnout entity/sensory pro HA
- [ ] Navrhnout update mechanism (polling interval, caching)

### Fáze 3: Implementace
- [ ] Vytvořit HA integraci
- [ ] Implementovat data fetching
- [ ] Implementovat data parsing
- [ ] Implementovat entity/sensory

### Fáze 4: Testing & docs
- [ ] Unit testy
- [ ] Integration testy
- [ ] Dokumentace instalace a použití

## HA Entity design

### Option A: Jednotlivé sensory per event type
- `sensor.hzsulk_pozary_pocet` - počet aktivních požárů
- `sensor.hzsulk_nehody_pocet` - počet aktivních nehod
- `sensor.hzsulk_technicka_pomoc_pocet` - atd.

### Option B: Event list
- `calendar.hzsulk_events` - seznam všech events
- `binary_sensor.hzsulk_active_incidents` - je něco aktivního?

### Option C: Kombinace
- Jednotlivé entity per typ
- + Generic event list sensor

## Next steps
1. Prozkoumat DevTools → Network tab pro přesný API endpoint
2. Rozhodnutí: Custom Integration vs REST
3. Návrh entity struktur
4. Implementace
