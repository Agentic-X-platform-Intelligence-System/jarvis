# AXIS Repository Structure

**AXIS** = Agentic X-platform Intelligence System (GitHub org)  
**Jarvis** = flagship orchestrator inside this monorepo

## Target layout

```text
AXIS/
├── stem/                 # Shared kernel: LLM, router, tools, agent loop, config, memory
├── jarvis/               # Orchestrator & sub-project routing
├── aura/                 # Voice, STT/TTS, wake word, audio
├── edith/                # RAG / knowledge (P2)
├── karen/                # Code review (P3)
├── friday/               # Research agent (P4)
├── cognis/               # Planning / reasoning (P5)
├── kinetix/              # Automation / workflows (P5/P6)
├── aero/                 # API, MCP, deployment (P7)
├── apps/
│   ├── cli/              # Jarvis CLI (P1)
│   ├── api/              # Production API (P7)
│   └── voice/            # Voice loop entry (P1)
├── docs/
└── tests/
```

## Migration status

Logic has moved to target packages; legacy paths remain as **thin shims** for compatibility.

| Legacy path | Canonical target | Shim |
|-------------|------------------|------|
| `config.py` | `stem/config/settings.py` | re-export |
| `skills/` | `stem/tools/` | re-export |
| `core/brain.py` | `stem/agent/brain.py` | re-export |
| `memory/` | `stem/memory/conversation.py` | re-export |
| `core/stt.py`, `tts.py`, `wake_word.py`, `audio.py` | `aura/` | re-export |
| `main.py` | `apps/voice/main.py` | delegates |

Do not delete legacy paths until all callers import canonical modules and tests pass.

## Sub-project READMEs

Each sub-project folder has a `README.md` with scope and roadmap mapping.

## GitHub

See [GITHUB.md](GITHUB.md) for org remote setup (placeholder slug).
