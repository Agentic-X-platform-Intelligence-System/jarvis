# GitHub Organization Setup

**AXIS** = Agentic X-platform Intelligence System  
**Flagship repo:** [`Agentic-X-platform-Intelligence-System/jarvis`](https://github.com/Agentic-X-platform-Intelligence-System/jarvis)

## Remote URL

```bash
git remote set-url origin https://github.com/Agentic-X-platform-Intelligence-System/jarvis.git
git remote -v
```

## Push

Requires **write** access on the org repo:

```bash
git push -u origin main
```

## Agile setup (labels, issues, project board)

All scripts and templates live in this repo. Run after you have **push** access:

```powershell
cd D:\Upgrade\AXIS

# 1. Labels + milestones + epics + Sprint 1 stories
.\scripts\agile\setup-all.ps1

# If project scope is missing:
gh auth refresh -s read:project,project
.\scripts\agile\setup-github-project.ps1
.\scripts\agile\setup-issues.ps1 -ProjectNumber <N>
```

| Resource | Location |
|----------|----------|
| Agile operating guide | [AGILE.md](AGILE.md) |
| GitHub Projects setup | [GITHUB-PROJECTS.md](GITHUB-PROJECTS.md) |
| Issue backlog manifest | [sprints/GITHUB-ISSUES-BACKLOG.md](sprints/GITHUB-ISSUES-BACKLOG.md) |
| Labels definition | [`.github/labels.json`](../.github/labels.json) |
| Sprint 0 checklist | [sprints/SPRINT0-CHECKLIST.md](sprints/SPRINT0-CHECKLIST.md) |

**Note:** `gh api` permissions must include `push: true` on the repo to create labels and issues. Project board creation additionally requires `read:project` and `project` scopes.

## Suggested future org repos

| Repo | Contents |
|------|----------|
| `jarvis` | Hub monorepo (this repo) |
| `edith` | Optional RAG portfolio extract |
| `friday` | Optional research agent extract |
| `aero` | Optional production API extract |

See [agentic-ai-ideas/scope.md](../../agentic-ai-ideas/scope.md) §16 for org registry.
