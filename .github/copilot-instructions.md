## Agentic communication

Applies to all agentic work and tool loops.

- Default to code and direct edits over prose. Explain only when asked or when a decision is non-obvious.
- No progress narration ("Now I will...", "Let me..."). Just do the action.
- No recaps or summaries of completed work unless requested.
- When prose is needed, use short bullets, not paragraphs.

## Klíčové instrukce

**Projekt**: Home Assistant integrace pro HZSULK - zobrazení hasiče/záchranných akcí na HA dashboardu

Relevantní dokumentace:
- [project-guidelines.md](.github/instructions/project-guidelines.md) - Přehled projektu a fází
- [ha-integration-guide.md](.github/instructions/ha-integration-guide.md) - Technické detaily a data struktura
- [discover-api.md](.github/skills/discover-api.md) - Jak zjistit API endpoint
- [design-ha-integration.md](.github/skills/design-ha-integration.md) - Návrh HA integrace
- [implement-ha-integration.md](.github/skills/implement-ha-integration.md) - Implementace

## Moduly aplikace
Vždy když pracuješ v modulech modules/[nazev] tak si musíš přečíst relevantní instrukce ze složky .github/ondemand-instructions/modull[nazev].md

## Jazyková nastavení a komunikace

- komunikace probíhá v českém jazyce (cs-cz)
- zdrojový kód je psán výhradně v anglickém jazyce (en-us)
- komentáře v kódu jsou česky

## Zdrojová data

**Web**: https://udalosti.hzsulk.cz/ (veřejná, bez autentizace)
**Data**: Tabulka hasiče/záchranných akcí (48+ položek, aktualizace každých 60s)
**Struktura**: čas, stav, typ akce, lokace, popis, počty

## Pracovní adresář
```
HZSULK-udalosti/
├── custom_components/hzsulk_events/  # HA integration
├── tests/                             # Testy
├── .github/
│   ├── instructions/                  # Instrukce
│   ├── skills/                        # Skills
│   └── copilot-instructions.md        # Tento soubor
└── README.md
```
