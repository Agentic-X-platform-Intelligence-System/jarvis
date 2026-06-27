# stem

Shared agentic kernel for all AXIS sub-projects.

## Owns

- `config/` — pydantic-settings
- `llm/` — Anthropic, OpenAI, Ollama providers + hybrid router
- `tools/` — registry, Pydantic → JSON schema
- `agent/` — think → act → observe loop

## Legacy source (migrate from)

- `core/brain.py` → agent + llm
- `skills/` → tools
- `config.py` → config
- `memory/` → memory tier

**Roadmap:** P1 (Milestone 1)
