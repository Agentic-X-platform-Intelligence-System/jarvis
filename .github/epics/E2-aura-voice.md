## Epic Summary

Extract existing voice stack into Aura module on shared stem kernel.

## Goals

- [ ] STT/TTS/wake-word live in `aura/`
- [ ] Voice loop uses stem agent instead of legacy brain
- [ ] Canonical entry at `apps/voice/main.py`

## Sub-Epics

- E2.1: Migrate STT/TTS/wake-word to `aura/`
- E2.2: Voice loop uses stem agent
- E2.3: Canonical entry at `apps/voice/main.py`

## Success Criteria

- [ ] `python -m apps.voice.main` launches voice assistant
- [ ] Voice commands route through stem agent loop
- [ ] Legacy `main.py` shim still works

## Dependencies

- Depends on: E1 (stem kernel)

## Estimated Timeline

1 week (Sprint 2 overlap or dedicated week)

## Portfolio Mapping

**Project:** P1 — Aura voice  
**Phase:** 1  
**Sub-project:** aura
