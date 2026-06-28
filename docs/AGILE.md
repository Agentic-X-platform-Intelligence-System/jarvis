# AXIS Agile Operating Guide

Operational Agile practices for the **AXIS/Jarvis** monorepo. Solo developer, **1-week sprints**, **15–20 story points** target velocity.

## Quick links

| Resource | Location |
|----------|----------|
| GitHub Project board | [AXIS/Jarvis Agile Board](https://github.com/orgs/Agentic-X-platform-Intelligence-System/projects) |
| Sprint burndown | [`docs/sprints/`](sprints/) |
| Retrospective template | [`retro-template.md`](retro-template.md) |
| Ceremony calendar | [`CEREMONY-CALENDAR.md`](CEREMONY-CALENDAR.md) |
| Risk register | [`RISKS.md`](RISKS.md) |
| GitHub Projects setup | [`GITHUB-PROJECTS.md`](GITHUB-PROJECTS.md) |
| Sprint 0 checklist | [`sprints/SPRINT0-CHECKLIST.md`](sprints/SPRINT0-CHECKLIST.md) |

## Hierarchy

```text
Epic (P1–P8 portfolio) → User Story → Tasks (in issue body or sub-issues)
```

| Work type | Label | Issue template |
|-----------|-------|----------------|
| Epic | `epic` | Epic |
| User story | `story` | User Story |
| Research | `spike` | Spike |
| Defect | `bug` | Bug Report |

## Definition of Ready (DoR)

Stories enter a sprint only when:

- [ ] User value statement: *As a [persona], I want [goal] so that [benefit]*
- [ ] 3–5 testable acceptance criteria
- [ ] Story point estimate (1, 2, 3, 5, 8, 13)
- [ ] Dependencies identified
- [ ] Linked to parent Epic
- [ ] Technical approach sketched (for stories > 5 points)

## Definition of Done (DoD)

Stories are **Done** when:

- [ ] Code committed on a feature branch and merged to `main`
- [ ] Unit or smoke tests pass
- [ ] Documentation updated (README, docstrings, or learning notes)
- [ ] Self-review completed (solo checklist below)
- [ ] Demo-able (CLI output, screenshot, or walkthrough note)

### Solo self-review checklist

- [ ] No secrets or `.env` values committed
- [ ] Types and docstrings on public APIs
- [ ] Error paths handled (tool failures, LLM timeouts)
- [ ] Acceptance criteria verified manually or via test

## Story point scale

| Points | Effort | Example |
|--------|--------|---------|
| 1 | 1–2 h | Config tweak, doc update |
| 2 | 2–4 h | Single function + basic test |
| 3 | 4–6 h | Module with tests |
| 5 | 6–10 h | Multi-file feature |
| 8 | 10–15 h | Large feature needing design |
| 13 | Too big | Split into smaller stories |

**Target velocity:** 15–20 points per 1-week sprint (20–30 hrs/week including learning).

## Sprint ceremonies (solo-adapted)

| Ceremony | Duration | When | Output |
|----------|----------|------|--------|
| Daily standup | 5 min | Start of each dev session | Journal: done / next / blockers |
| Sprint planning | 30 min | Monday | Sprint goal + committed stories |
| Backlog refinement | 20 min | Thursday | Next sprint stories refined |
| Sprint review | 20 min | Sunday | Demo notes; update burndown |
| Sprint retro | 15 min | Sunday | Use [`retro-template.md`](retro-template.md) |

### Daily standup prompt

```markdown
## Standup YYYY-MM-DD

**Done:** 
**Next:** 
**Blockers:** 
```

## GitHub Project workflow

### Views

1. **Backlog** (Table) — all epics and stories; group by Epic; sort by priority
2. **Sprint Board** (Board) — columns: **To Do → In Progress → Review → Done**
3. **Roadmap** (Roadmap) — epics on timeline (12-week plan)
4. **Learning Tracker** (Table) — filter label `learning`

### Custom fields (recommended)

| Field | Type | Values |
|-------|------|--------|
| Status | Single select | To Do, In Progress, Review, Done |
| Sprint | Text | Sprint 0, Sprint 1, … |
| Story Points | Number | 1–13 |
| Epic | Text | E1–E9 |
| Priority | Single select | P0, P1, P2, P3 |

### Board rules

- Move card to **In Progress** when work starts
- Move to **Review** when code is ready for self-review
- Move to **Done** when DoD is satisfied and issue is closed
- Close GitHub issue when story is Done

## Epic roadmap (12 weeks)

| Epic | Portfolio | Weeks | Sub-projects |
|------|-----------|-------|--------------|
| E1 | P1 stem + CLI | 1–2 | stem, jarvis |
| E2 | P1 Aura voice | 2 | aura |
| E3 | P2 RAG | 3–4 | edith |
| E4 | P3 Code review | 5–6 | karen |
| E5 | P4 Research | 7–8 | friday |
| E6 | P5 Java migrator | 9–10 | cognis |
| E7 | P6 Dev crew | 10 | kinetix |
| E8 | P7 Production API | 11 | aero |
| E9 | P8 SaaS capstone | 12 | aero, aura, jarvis |

See [`../agentic-ai-ideas/scope.md`](../../agentic-ai-ideas/scope.md) for full scope.

## Metrics

| Metric | How |
|--------|-----|
| Velocity | Sum story points of Done stories each sprint |
| Burndown | Daily remaining points in `docs/sprints/sprint-N.md` |
| Cycle time | Issue created → closed (GitHub insights) |
| Learning rate | Count closed issues with `learning` label |

## Labels reference

See [`.github/labels.json`](../.github/labels.json) for the canonical label list and colors.

## Scripts

```powershell
# Create labels (repo scope)
.\scripts\agile\setup-labels.ps1

# Create epics + Sprint 1 stories (repo scope)
.\scripts\agile\setup-issues.ps1

# GitHub Project board (requires project scope — see GITHUB-PROJECTS.md)
.\scripts\agile\setup-github-project.ps1
```

## Modification log

| Date | Change |
|------|--------|
| 2026-06-28 | Initial Agile operating guide (Sprint 0) |
