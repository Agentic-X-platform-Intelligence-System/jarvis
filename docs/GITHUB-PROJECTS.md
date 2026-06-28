# GitHub Projects Setup

Guide for the **AXIS/Jarvis Agile Board** on GitHub Projects (v2).

## Project URL

After setup:

```text
https://github.com/orgs/Agentic-X-platform-Intelligence-System/projects/<NUMBER>
```

## Prerequisites

GitHub CLI with **project** scopes:

```powershell
gh auth refresh -s read:project,project
```

Verify:

```powershell
gh auth status
gh project list --owner Agentic-X-platform-Intelligence-System
```

## Automated setup

From repo root:

```powershell
cd D:\Upgrade\AXIS
.\scripts\agile\setup-github-project.ps1
```

The script:

1. Creates org project **AXIS/Jarvis Agile Board**
2. Links the `jarvis` repository
3. Documents view configuration steps (views are configured in the UI or via GraphQL)

## Manual view configuration

After the project is created, add these views in the GitHub UI:

### 1. Backlog (Table)

- **Filter:** `repo:Agentic-X-platform-Intelligence-System/jarvis`
- **Columns:** Title, Assignees, Status, Sprint, Story Points, Epic, Priority, Labels
- **Group by:** Epic (custom field or label)
- **Sort:** Priority ascending

### 2. Sprint Board (Board)

- **Filter:** `sprint:"Sprint 1"` (update each week) OR current iteration field
- **Columns:** To Do | In Progress | Review | Done
- **Group by:** Status

### 3. Roadmap (Roadmap)

- **Filter:** `label:epic`
- **Date field:** Start / Target dates on epic issues (use milestones M1–M9)

### 4. Learning Tracker (Table)

- **Filter:** `label:learning`
- **Columns:** Title, Status, Sprint, Story Points

## Custom fields

In **Project settings → Fields**, add:

| Field name | Type |
|------------|------|
| Status | Single select: To Do, In Progress, Review, Done |
| Sprint | Text |
| Story Points | Number |
| Epic | Text (E1–E9) |
| Priority | Single select: P0, P1, P2, P3 |

Map **Status** to board columns for drag-and-drop.

## Workflow automations

In **Project settings → Workflows**, enable:

- **Auto-add to project:** new issues in `jarvis` repo (optional)
- **Auto-archive:** items closed for 14+ days
- **Status sync:** when issue closed → Status = Done (if available)

## Milestones

Create repo milestones (via script or UI):

| Milestone | Due | Epic |
|-----------|-----|------|
| M1 — stem + CLI | 2026-07-17 | E1 |
| M2 — Aura voice | 2026-07-24 | E2 |
| M3 — Edith RAG | 2026-08-07 | E3 |
| M4 — Karen review | 2026-08-21 | E4 |
| M5 — Friday research | 2026-09-04 | E5 |
| M6 — Cognis migrator | 2026-09-18 | E6 |
| M7 — Kinetix crew | 2026-09-25 | E7 |
| M8 — Aero API | 2026-10-02 | E8 |
| M9 — P8 SaaS | 2026-10-09 | E9 |

Run:

```powershell
.\scripts\agile\setup-milestones.ps1
```

## Linking issues to the project

After creating issues:

```powershell
$projectNum = <PROJECT_NUMBER>
gh project item-add $projectNum --owner Agentic-X-platform-Intelligence-System --url https://github.com/Agentic-X-platform-Intelligence-System/jarvis/issues/<ISSUE_NUMBER>
```

Or bulk-link via `setup-issues.ps1` after setting `$ProjectNumber`.

## Modification log

| Date | Change |
|------|--------|
| 2026-06-28 | Initial GitHub Projects setup guide |
