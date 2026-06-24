# Changelog

Všechny pozoruhodné změny v tomto projektu budou zdokumentovány v tomto souboru.

Formát je založen na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
a projekt se řídí [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- V1 MVP s agregovanými počty incidentů po typech
- Binary sensor pro detekci aktivních incidentů
- 60-sekundové obnovování dat
- GitHub Actions workflow pro linting

### Changed

### Fixed

### Removed

## [1.0.0] - 2026-06-24

### Added
- Počty incidentů: Požáry, dopravní nehody, technická pomoc, záchrana osob, hazmat, falešné poplachy
- Celkový počet incidentů
- Binary sensor pro aktivní incidenty
- Last update sensor
- Integrace s Home Assistant 2024.6+
- MIT License
- GitHub issue templates
- Contributing guidelines
- Code of Conduct

### Features
- V1: Hardcoded region (Ústecký - krajId=60)
- 24hodinový lookback
- Všechny stavy incidentů zahrnuty (stavIds)
- Graceful NULL handling

---

Formát:

- **Added** – Pro nové funkcionality.
- **Changed** – Pro změny v existující funkcionalitě.
- **Deprecated** – Pro brzy odstraňované funkcionality.
- **Removed** – Pro odstraněné funkcionality.
- **Fixed** – Pro opravy chyb.
- **Security** – V případě zranitelností.
