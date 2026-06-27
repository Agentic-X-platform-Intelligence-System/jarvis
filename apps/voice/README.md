# apps/voice

Voice assistant entry: wake word → record → STT → LLM (tools) → TTS.

## Run

```powershell
cd D:\Upgrade\AXIS
python main.py              # legacy shim
python -m apps.voice.main   # canonical entry
python main.py --no-wake --once
```

## Modules

| Module | Legacy shim | Purpose |
|--------|-------------|---------|
| `aura/audio.py` | `core/audio.py` | Microphone capture |
| `aura/stt.py` | `core/stt.py` | faster-whisper STT |
| `aura/tts.py` | `core/tts.py` | Edge / Coqui TTS |
| `aura/wake_word.py` | `core/wake_word.py` | Porcupine wake word |
| `stem/agent/brain.py` | `core/brain.py` | Claude tool-use loop |

**Roadmap:** P1 (Aura on stem)
