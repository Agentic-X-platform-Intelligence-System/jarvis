# AXIS — Agentic X-platform Intelligence System

GitHub organization monorepo for agentic AI. **Jarvis** is the flagship orchestrator; all sub-projects share **stem**.

## Hierarchy

```text
Jarvis (orchestrator)
├── stem      LLM providers, hybrid router, tools, agent loop, config, memory
├── Aura      Voice / multimodal (aura/ + apps/voice/)
├── Edith     RAG / knowledge
├── Karen     Code review
├── Friday    Research
├── Cognis    Planning / reasoning
├── Kinetix   Automation / workflows
├── Aero      APIs / MCP / deploy
└── apps/     CLI, API, voice surfaces
```

## Docs

- Workspace map: [`../README.md`](../README.md)
- Master scope: [`../agentic-ai-ideas/scope.md`](../agentic-ai-ideas/scope.md)
- Repo structure: [`docs/STRUCTURE.md`](docs/STRUCTURE.md)
- **Agile / sprints:** [`docs/AGILE.md`](docs/AGILE.md)
- GitHub org setup: [`docs/GITHUB.md`](docs/GITHUB.md)
- GitHub Projects: [`docs/GITHUB-PROJECTS.md`](docs/GITHUB-PROJECTS.md)

## Install

```powershell
cd D:\Upgrade\AXIS
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[windows]"   # or: pip install -r requirements.txt
```

Target package manager: `uv` + `pyproject.toml`.

## Run voice assistant

```powershell
python main.py              # legacy root shim
python -m apps.voice.main   # canonical entry
python main.py --no-wake --once
```

## Git remote

```bash
git remote set-url origin https://github.com/Agentic-X-platform-Intelligence-System/jarvis.git
```

See [docs/GITHUB.md](docs/GITHUB.md) — org slug required before push.
