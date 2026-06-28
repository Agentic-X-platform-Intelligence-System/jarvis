# Ceremony Calendar

Recurring sprint ceremonies for solo AXIS development. Import into your calendar app (Google Calendar, Outlook, etc.).

## Recurring schedule

| Ceremony | Day | Time (suggested) | Duration | Notes |
|----------|-----|------------------|----------|-------|
| Sprint planning | Monday | 09:00 | 30 min | Pick stories; set sprint goal |
| Daily standup | Each dev day | Session start | 5 min | Journal in `docs/sprints/` or personal notes |
| Backlog refinement | Thursday | 18:00 | 20 min | Refine next sprint; split large stories |
| Sprint review | Sunday | 17:00 | 20 min | Demo completed work |
| Sprint retro | Sunday | 17:30 | 15 min | Copy [`retro-template.md`](../retro-template.md) |

## Sprint 0 (setup week)

| Date | Event |
|------|-------|
| 2026-06-30 – 2026-07-02 | Sprint 0: Agile setup (labels, project, epics, docs) |

## Sprint 1 kickoff

| Date | Event |
|------|-------|
| 2026-07-03 (Mon) | Sprint 1 planning — goal: multi-provider LLM + hybrid router + P1 tools foundation |
| 2026-07-06 (Thu) | Backlog refinement for Sprint 2 |
| 2026-07-09 (Sun) | Sprint 1 review + retro |

## iCalendar (.ics) import

Import [`ceremonies.ics`](ceremonies.ics) into your calendar:

1. Open Google Calendar → Settings → Import & export → Import
2. Select `docs/sprints/ceremonies.ics`
3. Adjust times to your timezone (file uses UTC+5:30 / Asia-Kolkata)

## Outlook / Windows Calendar

Double-click `ceremonies.ics` or add via **Add calendar → Subscribe from web** (if hosted on GitHub raw URL after push).

## Monthly meta-retro

Every **4th Sunday** (after Sprint 4, 8, 12…):

- Review velocity trend in `docs/sprints/`
- Update [`RISKS.md`](../RISKS.md)
- Adjust epic dates if needed

## Modification log

| Date | Change |
|------|--------|
| 2026-06-28 | Initial ceremony calendar + ICS file |
