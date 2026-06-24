# Přispívání do HZSULK Events

Děkujeme za zájem o přispívání! Tenhle dokument vysvětluje, jak můžeš pomoci.

## Jak hlásit chyby

Našel jsi bug? Otevři issue s:

1. **Popisem problému** – Co se stalo?
2. **Očekávaným chováním** – Co mělo nastat?
3. **Verzí Home Assistant** – Kterou verzi používáš?
4. **Logs** – Chyby z home-assistant.log
5. **Kroky k reprodukci** – Jak bug opakuješ?

```markdown
### Popis
Integrace se nepřipojuje k API.

### Očekáváno
Integrace by se měla připojit a stáhnout data.

### Skutečně
Chyba `Connection timeout`.

### Verze HA
2024.6.1

### Kroky k reprodukci
1. Nainstaluj integraci
2. Přidej config entry
3. Čekej 60 sekund
```

## Jak navrhnout novou funkcionalitu

Máš nápad? Otevři feature request issue s:

1. **Popisem funkcionality** – Co chceš přidat?
2. **Případem užití** – Proč to potřebuješ?
3. **Návrhem řešení** – Jak by to mělo fungovat?

## Proces vývoje

1. **Fork** – Forkni projekt na svém GitHubu
2. **Clone** – `git clone https://github.com/tvoje-uzivatelske-jmeno/HZSULK-udalosti.git`
3. **Branch** – `git checkout -b feature/tvoje-funkcionalita`
4. **Kóduj** – Implementuj změny
5. **Test** – Ověř, že vše funguje
6. **Commit** – `git commit -am "Popis změn"`
7. **Push** – `git push origin feature/tvoje-funkcionalita`
8. **Pull Request** – Otevři PR na hlavním repozitáři

## Kodex chování

Vezmi si na vědomí náš [Code of Conduct](CODE_OF_CONDUCT.md).

## Coding Style

### Python

- Používej **PEP 8** standard
- Délka řádku: max. 100 znaků
- Type hints: preferuj pro nové kódy
- Docstrings: Prosím, pro všechny funkce/třídy
- Komentáře: Česky, krátké a věcné

```python
"""Příklad správného stylu."""

from typing import Optional


def process_event(event: dict[str, Any]) -> Optional[str]:
    """Zpracuj event a vrať ID.
    
    Args:
        event: Raw event dict z API.
        
    Returns:
        Event ID nebo None, pokud event není platný.
    """
    if not event.get("id"):
        return None
    
    return event["id"]
```

### Commit Messages

- **Jazyk**: Česky nebo Anglicky (konzistentně)
- **Format**: `[type] Short description`
- **Types**: feat, fix, docs, style, refactor, test, chore

```
feat: Přidej support pro více krajů
fix: Oprav NULL handling v poznamkaProMedia
docs: Aktualizuj API reference
test: Přidej unit testy pro coordinator
```

## Testování

```bash
# Spusť testy (až budou)
pytest

# Ověř typing
mypy custom_components/hzsulk_events

# Linting
flake8 custom_components/hzsulk_events
```

## Verzování

Používáme **Semantic Versioning**:

- **MAJOR** – Breaking changes (V1 → V2)
- **MINOR** – Nové features, zpětně kompatibilní
- **PATCH** – Bug fixes

Format: `v1.0.0`

## Licence

Tím, že přispíváš, souhlasíš s licencováním svého kódu pod MIT License.

---

Máš otázky? Napiš mi issue! 🚀
