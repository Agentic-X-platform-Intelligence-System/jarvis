# AGENTS.md

## Cursor Cloud specific instructions

AXIS / JARVIS is a single Python (>=3.11) monorepo, not networked microservices. The only
runnable product today is the **JARVIS voice assistant** (`apps/voice/main.py`, root `main.py`
is a shim). `stem/` is the shared kernel (agent loop, tools, config, SQLite memory); `aura/`
provides the voice surface (STT/TTS/wake word). Other top-level dirs (`edith/`, `karen/`,
`friday/`, `cognis/`, `kinetix/`, `aero/`, `apps/api/`) are roadmap placeholders.

### Environment
- Dependencies live in a virtualenv at `.venv` (created by the startup update script). Activate
  with `source .venv/bin/activate` or call binaries directly as `.venv/bin/python`.
- Install from `pyproject.toml` (`pip install -e .`), NOT `requirements.txt`: `requirements.txt`
  is missing `pydantic-settings`, which `stem/config/settings.py` imports, so a
  `requirements.txt`-only install fails at import time.
- System libs `libportaudio2` (for `sounddevice`) and `python3-venv` are required and are already
  present in the VM image.
- Config is read from a root `.env` (template `.env.example`); settings accept both `AXIS_*` and
  `JARVIS_*` aliases.

### Run / test / build
- Tests: `.venv/bin/python -m pytest` (suite is import/smoke tests in `tests/`).
- Run the assistant: `python main.py` or `python -m apps.voice.main` (`--no-wake` manual mode,
  `--once` single turn). See `README.md` for all flags.
- No build step, no dev server, no database server (SQLite file auto-created under `data/`).
- There is no configured linter (no ruff/flake8/black config, no CI workflows).

### Non-obvious caveats
- The Claude brain hard-requires `ANTHROPIC_API_KEY`; without it `main.py` logs the error and
  exits with code 2 before doing anything else. Set it in `.env` (or as a secret) to run the full
  LLM loop.
- The VM is headless: there is no microphone or speaker, so the live wake-word/record/playback
  loop cannot capture or play audio. For end-to-end verification without hardware, drive the
  components directly (e.g. `aura.JarvisTTS.synthesize` -> WAV -> `aura.WhisperSTT.transcribe_file`)
  and exercise tools via `stem.tools.SkillRouter`.
- First STT use downloads the faster-whisper `base` model from Hugging Face (needs network).
- Default TTS backend resolves to Edge TTS (`edge-tts`, needs network); Coqui is optional and not
  installed.
- `web_search` falls back to DuckDuckGo when `SERPER_API_KEY` is absent and emits a deprecation
  warning (`duckduckgo_search` -> `ddgs`); this is harmless.
