# AXIS — Agentic X-platform Intelligence System

GitHub organization monorepo for agentic AI. **Jarvis** is the flagship orchestrator; all sub-projects share **stem**.

## Hierarchy

```text
Jarvis (orchestrator)
├── stem      LLM providers, hybrid router, tools, agent loop
├── Aura      Voice / multimodal (legacy: root main.py, core/stt, tts)
├── Edith     RAG / knowledge
├── Karen     Code review
├── Friday    Research
├── Cognis    Planning / reasoning
├── Kinetix   Automation / workflows
├── Aero      APIs / MCP / deploy
└── apps/     CLI, API surfaces
```

## Docs

- Workspace map: [`../README.md`](../README.md)
- Master scope: [`../Agentic AI/scope.md`](../Agentic%20AI/scope.md)
- Repo structure: [`docs/STRUCTURE.md`](docs/STRUCTURE.md)

## Run (legacy voice prototype)

```powershell
cd D:\Upgrade\AXIS
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Git remote

```bash
git remote set-url origin https://github.com/<AXIS-ORG-SLUG>/jarvis.git
```
