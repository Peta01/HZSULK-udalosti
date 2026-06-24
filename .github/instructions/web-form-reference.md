# Web Formulář - Číselníky a Filtry

Dokumentace všech dostupných filtrů a číselníků ze **webu https://udalosti.hzsulk.cz/**.

## Pole v Hledacím Formuláři

### 1. Status (Stav) - `select#stav`

| Value | Popis |
|-------|-------|
| `0` | Všechny události |
| `1` | Otevřené události |
| `2` | Uzavřené události |

**Mapování na API `stavIds`:**
- "Otevřené": stavIds=[210, 400, 410, 420, 430, 440, 500]
- "Uzavřené": stavIds=[510, 520, 600, 610, 620, 700, 710, 750, 760, 780, 800]

---

### 2. Typ Události - `select#typ`

| Value | Popis | API typId |
|-------|-------|-----------|
| (prázdný) | --nevybráno-- | - |
| `3100` | POŽÁR | 3100 |
| `3200` | DOPRAVNÍ NEHODA | 3200 |
| `3400` | ÚNIK NEBEZPEČNÝCH LÁTEK | 3400 |
| `3500` | TECHNICKÁ POMOC | 3500 |
| `3550` | ZÁCHRANA OSOB A ZVÍŘAT | 3550 |
| `3700` | JINÁ UDÁLOST | 3700 |
| `3600` | FORMÁLNĚ ZALOŽENÁ UDÁLOST | 3600 |
| `3900` | TECHNOLOGICKÝ TEST | 3900 |
| `3800` | PLANÝ POPLACH | 3800 |
| `5000` | UDÁLOST NA OBJEKT | 5000 |

---

### 3. Region (Kraj) - `select#kraj`

| Value | Popis | API krajId |
|-------|-------|-----------|
| (prázdný) | --nevybráno-- | - |
| `51` | Karlovarský | 51 |
| `78` | Liberecký | 78 |
| `27` | Středočeský | 27 |
| `60` | Ústecký | 60 |

**Poznámka**: Aktuálně se filtruje na Ústecký (60) v API.

---

### 4. Okres (District) - `select#okres`

Dostupné okresy v Ústeckém kraji:

| Value | Popis | API okresId |
|-------|-------|------------|
| (prázdný) | --nevybráno-- | - |
| `3503` | Chomutov | 3503 |
| `3502` | Děčín | 3502 |
| `3506` | Litoměřice | 3506 |
| `3507` | Louny | 3507 |
| `3508` | Most | 3508 |
| `3509` | Teplice | 3509 |
| `3510` | Ústí nad Labem | 3510 |

---

### 5. Časový Rozsah - `p-calendar` + `app-timepicker`

```
od: <datum> HH:MM
do: <datum> HH:MM
```

**Formát**: ISO 8601 s UTC
- Příklad: `2026-06-23T22:00:00.000Z` až `2026-06-24T21:59:59.999Z`

**Komponenty**:
- Datum (date picker)
- Hodiny (0-23)
- Minuty (0-59)
- Sekundy (0-59)

---

### 6. Jednotka (Unit) - `iq-select2#jednotka`

Free-form search
Příklady jednotek (z webu):
- Domoušice
- AGC Teplice
- (další jednotky hasičských jednotek)

---

### 7. Adresa (Address) - `input` s placeholderem

Free-form vyhledávání v adrese: "Vyhledávání v adrese události ..."

---

## API vs. Web Mapování

### Web → API Query

```
Formulář Filtr → API Parameter
─────────────────────────────

Status (stav):
  "Otevřené" → stavIds=[210, 400, 410, 420, 430, 440, 500]
  "Uzavřené" → stavIds=[510, 520, 600, 610, 620, 700, 710, 750, 760, 780, 800]

Typ:
  3100 (POŽÁR) → typId=3100

Kraj:
  60 (Ústecký) → krajId=60

Okres:
  3510 → (není v API, jen pro frontend filtrování)

Čas:
  od/do → casOd, casDo (ISO 8601)

Adresa:
  (frontend filtrování - API nemá support)

Jednotka:
  (frontend filtrování - API nemá support)
```

---

## Klíčové Poznatky

1. **API má omezené filtry**: Jen `casOd`, `casDo`, `krajId`, `stavIds`
2. **Web má více filtrů**: `typ`, `okres`, `jednotka`, `adresa` - ty jsou frontend-side filtrování
3. **stavIds není pevný**: Web mapuje "Otevřené" a "Uzavřené" na konkrétní stavIds
4. **typId NELZE filtrovat v API**: Musíme filtrovat v HA integraci post-processing

---

## Status IDs Detailně

| stavId | Stav | Kategorie | Poznámka |
|--------|------|-----------|----------|
| 210 | ? | Otevřená | Detaily nevím |
| 400 | ? | Otevřená | Detaily nevím |
| 410 | ? | Otevřená | Detaily nevím |
| 420 | Otevřená | Otevřená | Vidět v datech |
| 430 | ? | Otevřená | Detaily nevím |
| 440 | ? | Otevřená | Detaily nevím |
| 500 | ? | Otevřená | Detaily nevím |
| 510 | Uzavřená OS | Uzavřená | Vidět v datech |
| 520 | ? | Uzavřená | Detaily nevím |
| 600 | Převzatá VZ | Uzavřená | Vidět v datech |
| 610 | Uzavřená | Uzavřená | Vidět v datech |
| 620 | ? | Uzavřená | Detaily nevím |
| 700 | Ukončená | Uzavřená | Vidět v datech |
| 710 | Ukončená ZPP | Uzavřená | Vidět v datech |
| 750 | ? | Uzavřená | Detaily nevím |
| 760 | ? | Uzavřená | Detaily nevím |
| 780 | ? | Uzavřená | Detaily nevím |
| 800 | Ukončená garantem za SSU | Uzavřená | Vidět v datech |

---

## Příklad Dotazu s Web Filtry

**Web formulář filtr:**
- Status: "Otevřené"
- Typ: POŽÁR (3100)
- Kraj: Ústecký (60)
- Čas: 24.6.2026 21:36 až 24.6.2026 22:00

**API dotaz by měl být:**
```
GET https://udalosti.hzsulk.cz/api/?
  casOd=2026-06-24T21:36:00.000Z
  &casDo=2026-06-24T22:00:59.999Z
  &krajId=60
  &stavIds=210&stavIds=400&stavIds=410&stavIds=420&stavIds=430&stavIds=440&stavIds=500
```

**Frontend post-processing:**
```
Výsledky filtrovat podle typId == 3100 (POŽÁR)
```

---

## Použití v HA Integraci

1. **API filtry**: Vždy používat `krajId=60` a `stavIds` pro "Otevřené + Uzavřené"
2. **Post-processing filtry**: V HA integraci lze filtrovat podle `typId`
3. **Defaultní chování**: HA integraci by měla zobrazovat VŠECHNY typy (bez filtrování typId)

---

## Next Steps

- ✅ Máme všechny číselníky
- ✅ Víme, jak API mapovat z webu
- 🔄 Připraveni nadesignovat HA entity
