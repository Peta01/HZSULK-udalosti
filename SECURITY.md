# Security Policy

## Reporting a Vulnerability

Pokud jsi objevil bezpečnostní zranitelnost, prosím **NEZVEŘEJŇUJ JI VEŘEJNĚ**. Místo toho prosím sděl nám o tom diskrétně.

### Jak hlásit

1. Pošli email na: [DOPLNIT EMAIL]
2. Zahrň popis zranitelnosti
3. Zahrň kroky k reprodukci, pokud je to možné
4. Dej nám čas na vyřešení

Snažíme se odpovědět na všechny bezpečnostní hlášení během 48 hodin.

## Verzování a Bezpečnost

- **Stabilní verze**: Dostávají bezpečnostní opravy
- **Starší verze**: Mohou nebo nemusí dostávat bezpečnostní opravy
- **Beta/RC verze**: Nejsou primární zaměření bezpečnostní podpory

## Požadavky na Bezpečnost

Tato integrace komunikuje s:
- **HZSULK API** (https://udalosti.hzsulk.cz/) – **HTTPS** (šifrované)
- **Home Assistant** – Místní komunikace

Neuchováváme žádné citlivé údaje.

## Best Practices

1. Vždy aktualizuj Home Assistant na nejnovější verzi
2. Hlídej bezpečnostní hlášení v tomto repo
3. Nepoužívej staré verze integrace s známými zranitelnostmi

Díky za pomoc v udržování HZSULK Events bezpečné! 🔒
