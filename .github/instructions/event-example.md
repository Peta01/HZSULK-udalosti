# Příklad jedné Události - Kompletní Analýza

## Konkrétní Event z API

```json
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
}
```

## Pole - Podrobné Vysvětlení

| Pole | Hodnota | Typ | Popis |
|------|---------|-----|-------|
| `id` | `347488042` | number | **Unikátní ID eventu** - identifikátor |
| `casOhlaseni` | `2026-06-24T21:36:12` | ISO8601 | **Čas ohlášení** - kdy bylo ohlášeno (UTC) |
| `casVzniku` | `null` | ISO8601\|null | **Čas vzniku** - kdy do toho vlastně došlo (često null) |
| `stavId` | `420` | number | **Status ID** - viz status reference<br>420 = "Otevřená" |
| `typId` | `3500` | number | **Typ ID** - hlavní kategorie<br>3500 = "TECHNICKÁ POMOC" |
| `podtypId` | `3505` | number | **Podtyp ID** - podrobný typ<br>3505 = "Odstranění stromu/větve" |
| `poznamkaProMedia` | `"Odstranění větve z komunikace"` | string | **Popis pro média** - lidsky čitelný popis |
| `kraj.id` | `60` | number | **Region ID** - 60 = Ústecký |
| `kraj.nazev` | `"Ústecký"` | string | **Region název** |
| `okres.id` | `3510` | number | **District ID** - Ústí nad Labem |
| `okres.nazev` | `"Ústí nad Labem"` | string | **District název** |
| `obec` | `"Povrly"` | string | **Obec/Město** - město |
| `castObce` | `"Povrly"` | string | **Část obce** - specifičtější lokace |
| `ORP` | `"Ústí nad Labem"` | string | **ORP** (správní obvod Obec s rozšířenou působností) |
| `ulice` | `null` | string\|null | **Ulice** - konkrétní ulice (je null) |
| `gis1` | `"754586"` | string | **GPS X** - E souřadnice (SJTSK) |
| `gis2` | `"973505"` | string | **GPS Y** - N souřadnice (SJTSK) |
| `zoc` | `false` | boolean | **ZOC** - Zona ohrožené komunity? |
| `silnice` | `null` | string\|null | **Silnice** - konkrétní cesta/silnice |

## Příklad HA Entit Z Tohoto Eventu

### Z tohoto eventu by se vytvořily entity:

```yaml
# Agregované počty (pro dashboard)
sensor.hzsulk_technical_help_count: 1  # typId 3500

# Detail eventu (pro automations)
sensor.hzsulk_latest_technical_help:
  state: "Odstranění větve z komunikace"
  attributes:
    id: 347488042
    time: "2026-06-24T21:36:12"
    status: "Otevřená"
    type: "TECHNICKÁ POMOC"
    location: "Povrly, okres Ústí nad Labem"
    gps_x: "754586"
    gps_y: "973505"
```

## Mapování typId → HA Entity

### Tento event (typId 3500) → Technická pomoc
- `sensor.hzsulk_technical_help_count` = +1
- `binary_sensor.hzsulk_has_active_incidents` = true

## Co z API Máme ✅

Všechna potřebná data:
- ✅ Jednoznačné ID
- ✅ Timestamp (čas ohlášení)
- ✅ Status (stavId)
- ✅ Typ (typId + podtypId)
- ✅ Popis (poznamkaProMedia) - **ALE POZOR: Někdy je NULL!**
- ✅ Lokace (obec, okres, ORP, ulice)
- ✅ GPS (gis1, gis2)
- ✅ Region (kraj)

## Chybí v API ❓

- Počet jednotek zasahujících
- Počet zraněných osob
- Foto/videa
- Real-time GPS tracking
- Detaily z webového detailu (Domoušice, typ techniky, počty)

## WICHTIG: Pole `poznamkaProMedia` Nemusí Být Vyplněno

Příklad z API (event 24.6.2026 20:03):
```json
{
  "id": 347479042,
  "casOhlaseni": "2026-06-24T20:03:39",
  "poznamkaProMedia": null,  // ← NULL! Žádný popis
  "obec": "Domoušice",
  "castObce": "Solopysky"
}
```

Web ale zobrazuje detaily:
- **Jednotka**: Domoušice
- **Typ techniky**: dopravní automobil
- **Počet**: 1

**Závěr**: Detaily na webu mohou pocházet z:
1. Jiného API endpointu
2. HTML parsování tabulky
3. Cachovaných dat v localStorage

**Pro HA integraci**: Pokud `poznamkaProMedia` je null, stačí nám typ eventu (`typId`) a lokace. Web zatím ignorujeme.

## Příští Kroky

1. ✅ Máme API endpoint
2. ✅ Máme příklad dat
3. 🔄 **Navrhneme HA entity**
4. ❓ Implementujeme integraci
