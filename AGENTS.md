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

### Running the LLM brain on a free Gemini backend (no Anthropic key)
The brain uses the official `anthropic` SDK, which honors `ANTHROPIC_BASE_URL`. So you can run the
full LLM loop on Google AI Studio's free Gemini tier via a LiteLLM proxy that exposes an
Anthropic-compatible `/v1/messages` endpoint — no source changes:
1. Provide `GEMINI_API_KEY` (free, no card: https://aistudio.google.com/apikey), available as an
   env var / secret.
2. Start the proxy (not started by the update script):
   `GEMINI_API_KEY=$GEMINI_API_KEY .venv/bin/litellm --config scripts/litellm_gemini.yaml --port 4000`
3. Ensure `.env` (gitignored, recreate if missing) contains:
   ```
   ANTHROPIC_API_KEY=sk-local-litellm   # any non-empty value; proxy has no master_key
   CLAUDE_MODEL=gemini-2.5-flash
   ```
4. **IMPORTANT:** export `ANTHROPIC_BASE_URL` as a real environment variable when running the app —
   do NOT rely on putting it in `.env`. `stem/config/settings.py` uses pydantic-settings, which
   reads `.env` into the Settings object but does NOT push values into `os.environ`; the `anthropic`
   SDK reads `ANTHROPIC_BASE_URL` straight from `os.environ`. If it is only in `.env`, the SDK
   silently calls the real Anthropic API (you'll get `invalid x-api-key`). Run with:
   `ANTHROPIC_BASE_URL=http://localhost:4000 python main.py --no-wake --once`
Health-check the proxy with `curl http://localhost:4000/health/readiness`. The proxy translates
Anthropic tool definitions to Gemini function calls automatically.

### Non-obvious caveats
- The Claude brain hard-requires `ANTHROPIC_API_KEY` (any non-empty value when using the proxy);
  without it `main.py` logs the error and exits with code 2 before doing anything else.
- The VM is headless: there is no microphone or speaker, so the live wake-word/record/playback
  loop cannot capture or play audio. For end-to-end verification without hardware, drive the
  components directly (e.g. `aura.JarvisTTS.synthesize` -> WAV -> `aura.WhisperSTT.transcribe_file`)
  and exercise tools via `stem.tools.SkillRouter`.
- First STT use downloads the faster-whisper `base` model from Hugging Face (needs network).
- Default TTS backend resolves to Edge TTS (`edge-tts`, needs network); Coqui is optional and not
  installed.
- `web_search` falls back to DuckDuckGo when `SERPER_API_KEY` is absent and emits a deprecation
  warning (`duckduckgo_search` -> `ddgs`); this is harmless.
