# stem

Shared agentic kernel for all AXIS sub-projects.

## Owns

- `config/settings.py` — pydantic-settings (`AXIS_*` / `JARVIS_*` env vars)
- `llm/` — Anthropic, OpenAI, Ollama providers + hybrid router (M1)
- `tools/` — registry, Pydantic → JSON schema (migrated from `skills/`)
- `agent/brain.py` — Claude tool-use loop (migrated from `core/brain.py`)
- `memory/conversation.py` — rolling history + SQLite logger (migrated from `memory/`)

## Legacy shims (temporary)

| Shim | Canonical |
|------|-----------|
| `config.py` | `stem/config/settings.py` |
| `skills/` | `stem/tools/` |
| `core/brain.py` | `stem/agent/brain.py` |
| `memory/` | `stem/memory/` |

**Roadmap:** P1 (Milestone 1)
