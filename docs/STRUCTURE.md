# AXIS Repository Structure

**AXIS** = Agentic X-platform Intelligence System (GitHub org)  
**Jarvis** = flagship orchestrator inside this monorepo

## Target layout

```text
AXIS/
├── stem/                 # Shared kernel: LLM, router, tools, agent loop
├── jarvis/               # Orchestrator & sub-project routing
├── aura/                 # Voice, STT/TTS, wake word
├── edith/                # RAG / knowledge (P2)
├── karen/                # Code review (P3)
├── friday/               # Research agent (P4)
├── cognis/               # Planning / reasoning (P5)
├── kinetix/              # Automation / workflows (P5/P6)
├── aero/                 # API, MCP, deployment (P7)
├── apps/
│   ├── cli/              # Jarvis CLI (P1)
│   └── api/              # Production API (P7)
├── docs/
└── tests/
```

## Legacy (migration in progress)

These root-level paths are the **voice prototype** — to be absorbed into `stem/` + `aura/`:

| Legacy path | Target |
|-------------|--------|
| `core/brain.py` | `stem/agent/` + `stem/llm/` |
| `core/stt.py`, `tts.py`, `wake_word.py`, `audio.py` | `aura/` |
| `skills/` | `stem/tools/` |
| `memory/` | `stem/` memory layer |
| `config.py` | `stem/config/` |
| `main.py` | `apps/voice/` or `aura/` entry |

Do not delete legacy paths until imports are updated and tests pass.

## Sub-project READMEs

Each sub-project folder has a `README.md` with scope and roadmap mapping.
