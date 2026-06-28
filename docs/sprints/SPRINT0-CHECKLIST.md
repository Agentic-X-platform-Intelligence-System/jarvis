# Sprint 0 Completion Checklist

Use before Sprint 1 kickoff (2026-07-03).

> **Local repo:** templates, docs, labels manifest, epic/story bodies, and scripts are in place.  
> **GitHub remote:** run `scripts/agile/setup-all.ps1` after `gh api` shows `"push": true` on the jarvis repo.

## GitHub Projects setup

- [ ] Project created: [AXIS/Jarvis Agile Board](https://github.com/orgs/Agentic-X-platform-Intelligence-System/projects)
- [ ] Backlog table view configured
- [ ] Sprint board view configured (To Do → In Progress → Review → Done)
- [ ] Roadmap view configured
- [ ] Learning Tracker view configured
- [ ] Custom fields added (Status, Sprint, Story Points, Epic, Priority)
- [ ] Workflow automations enabled (see [`GITHUB-PROJECTS.md`](../GITHUB-PROJECTS.md))

## Labels and templates

- [x] 15+ labels defined in `.github/labels.json` (apply via `setup-labels.ps1`)
- [x] Epic template: `.github/ISSUE_TEMPLATE/epic.md`
- [x] Story template: `.github/ISSUE_TEMPLATE/story.md`
- [x] Spike template: `.github/ISSUE_TEMPLATE/spike.md`
- [x] Bug template: `.github/ISSUE_TEMPLATE/bug.md`
- [ ] Labels applied on GitHub remote (requires push access)

## Epic issues

- [x] Epic bodies drafted in `.github/epics/E1–E9`
- [x] Sprint 1 story bodies in `.github/stories/S1.1–S1.5`
- [x] Backlog manifest: `docs/sprints/GITHUB-ISSUES-BACKLOG.md`
- [ ] Issues created on GitHub (run `setup-issues.ps1`)

## Documentation

- [x] `docs/AGILE.md`
- [x] `docs/retro-template.md`
- [x] `docs/RISKS.md`
- [x] `docs/GITHUB-PROJECTS.md`
- [x] `docs/CEREMONY-CALENDAR.md`
- [x] `docs/PORTFOLIO.md`
- [x] `docs/sprints/sprint-0.md`
- [x] `docs/sprints/sprint-1.md`
- [x] `docs/sprints/standup-notes.md`
- [x] Calendar file: `docs/sprints/ceremonies.ics`

## Development environment

- [ ] Python 3.11+ venv active
- [ ] `pip install -e ".[windows]"` succeeds
- [ ] `python -m apps.voice.main --no-wake --once` runs (or documented blocker)

## Sprint 1 prep

- [x] Sprint 1 stories S1.1–S1.5 documented (`.github/stories/` + `sprint-1.md`)
- [ ] Stories created on GitHub and on Sprint board **To Do**
- [x] Sprint 1 goal documented in `docs/sprints/sprint-1.md`
- [x] Total committed points documented (23 pts — split if velocity lower)

## Sign-off

**Sprint 0 complete date:** _______________  
**Notes:**
