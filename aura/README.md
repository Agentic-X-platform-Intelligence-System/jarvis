# Aura

Voice, ambient, and multimodal interface.

## Legacy code (repo root — migrate here)

| File | Purpose |
|------|---------|
| `main.py` | Voice loop entry |
| `core/stt.py` | Speech-to-text |
| `core/tts.py` | Text-to-speech |
| `core/wake_word.py` | Wake word |
| `core/audio.py` | Recording |

Depends on **stem** for LLM brain (`core/brain.py` → stem).

**Roadmap:** P1 (voice), P8 (SaaS UI)
