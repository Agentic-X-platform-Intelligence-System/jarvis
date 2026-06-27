# Aura

Voice, ambient, and multimodal interface.

## Owns

| Module | Purpose |
|--------|---------|
| `aura/audio.py` | Microphone capture |
| `aura/stt.py` | faster-whisper STT |
| `aura/tts.py` | Edge / Coqui TTS |
| `aura/wake_word.py` | Porcupine wake word |

## Entry

- `apps/voice/main.py` — voice loop (wake → record → STT → brain → TTS)
- `main.py` — legacy root shim

## Legacy shims (temporary)

| Shim | Canonical |
|------|-----------|
| `core/stt.py`, `tts.py`, `wake_word.py`, `audio.py` | `aura/` |

Depends on **stem** for LLM brain (`stem/agent/brain.py`).

**Roadmap:** P1 (voice), P8 (SaaS UI)
