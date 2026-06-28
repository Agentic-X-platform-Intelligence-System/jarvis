# Agile setup scripts

PowerShell scripts to bootstrap GitHub labels, milestones, issues, and Projects for AXIS/Jarvis.

## Prerequisites

```powershell
gh auth status
gh api repos/Agentic-X-platform-Intelligence-System/jarvis --jq ".permissions"
# Required: "push": true for labels/issues; project scopes for board
```

Grant project scopes:

```powershell
gh auth refresh -s read:project,project
```

## Scripts

| Script | Purpose |
|--------|---------|
| `setup-labels.ps1` | Create/update labels from `.github/labels.json` |
| `setup-milestones.ps1` | Create milestones M1–M9 |
| `setup-github-project.ps1` | Create org project + link repo |
| `setup-issues.ps1` | Create epics E1–E9 + Sprint 1 stories |
| `setup-all.ps1` | Run all of the above |

## Usage

```powershell
cd D:\Upgrade\AXIS
.\scripts\agile\setup-all.ps1
```

If project creation fails on scopes:

```powershell
.\scripts\agile\setup-all.ps1 -SkipProject
gh auth refresh -s read:project,project
.\scripts\agile\setup-github-project.ps1
.\scripts\agile\setup-issues.ps1 -ProjectNumber <N>
```

## Outputs

- `.github/project-state.json` — project number and URL
- `.github/issue-map.json` — epic/story issue numbers (after setup-issues)

## Manual fallback

See [docs/sprints/GITHUB-ISSUES-BACKLOG.md](../../docs/sprints/GITHUB-ISSUES-BACKLOG.md).
