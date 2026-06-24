---
applyTo: "**/*.md"
title: "HA Integration Project Guidelines"
description: "Guidelines for working on HZSULK Home Assistant integration project"
---

# HA Integration: HZSULK Events - Project Guidelines

## Project Overview
Creating a Home Assistant custom integration that displays current HZSULK (Czech fire/rescue events) on a HA dashboard by reverse-engineering the public events website.

**Website**: https://udalosti.hzsulk.cz/

## Tech Stack
- **Backend**: .NET 10.0
- **Frontend**: Node.js 22 (TBD: React/Next.js)
- **HA Integration**: Python (custom_components/)
- **Container**: devcontainer with .NET + Node.js
- **VCS**: GitHub

## Project Phases

### Phase 1: API Discovery ✅
**Status**: In Progress
**Owner**: Agent
**Skills**: 
- [discover-api.md](.github/skills/discover-api.md) - Find API endpoint and data structure
- [ha-integration-guide.md](.github/instructions/ha-integration-guide.md) - Reference guide

**Deliverables**:
- [ ] API endpoint documented
- [ ] Request/Response structure captured
- [ ] Update frequency determined
- [ ] Authentication requirements identified

### Phase 2: HA Integration Design 🔄
**Status**: Planned
**Owner**: Agent
**Skills**: 
- [design-ha-integration.md](.github/skills/design-ha-integration.md) - Design entities and structure

**Deliverables**:
- [ ] Entity design (sensors, binary sensors)
- [ ] Integration architecture
- [ ] Configuration schema
- [ ] Update strategy flowchart

### Phase 3: Implementation
**Status**: Planned
**Owner**: Agent
**Skills**: 
- [implement-ha-integration.md](.github/skills/implement-ha-integration.md) - Coding HA integration

**Deliverables**:
- [ ] Full working HA integration
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] Documentation

### Phase 4: Testing & Release
**Status**: Planned
**Deliverables**:
- [ ] GitHub Actions CI/CD
- [ ] HACS compatibility
- [ ] Release to GitHub
- [ ] Installation guide

## Communication Style
- **Language**: Czech (Česština) for documentation and communication
- **Code**: English with Czech comments
- **Documentation**: Czech with code examples in English

## Key Resources
- [ha-integration-guide.md](.github/instructions/ha-integration-guide.md) - Main reference
- [discover-api.md](.github/skills/discover-api.md) - API discovery process
- [design-ha-integration.md](.github/skills/design-ha-integration.md) - Design patterns
- [implement-ha-integration.md](.github/skills/implement-ha-integration.md) - Implementation guide

## Working Directory
```
HZSULK-udalosti/
├── custom_components/hzsulk_events/  # HA integration code
├── tests/                             # Unit and integration tests
├── .github/
│   ├── instructions/                  # General instructions
│   ├── skills/                        # Skills for agents
│   ├── workflows/                     # GitHub Actions
│   └── copilot-instructions.md        # This file
└── README.md                          # Project overview
```

## Next Steps
1. **Now**: Discover API endpoint (see discover-api.md)
2. **Then**: Design HA integration (see design-ha-integration.md)
3. **Then**: Implement (see implement-ha-integration.md)
4. **Finally**: Test and release

## Agent Instructions
When working on this project:
1. Always read relevant `.github/instructions/` or `.github/skills/` before starting a phase
2. Keep source code in **English** with Czech comments
3. Update `.github/` documentation with progress
4. Use `custom_components/hzsulk_events/` for HA integration code
5. Write tests for all features
6. Reference this guide for context

---
*Last updated: 2026-06-24*
