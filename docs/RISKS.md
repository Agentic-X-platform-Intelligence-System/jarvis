# Risk Register

Track risks that could affect the 12-week AXIS roadmap. Review during monthly meta-retrospective.

| ID | Risk | Likelihood | Impact | Mitigation | Status |
|----|------|------------|--------|------------|--------|
| R1 | Ollama too slow for real-time voice | Medium | High | Fall back to cloud for Aura in M1; benchmark early | Open |
| R2 | LangChain API breaking changes | Medium | Medium | Pin versions; monitor release notes | Open |
| R3 | Time overrun on Cognis Java parsing | High | Medium | Use ripgrep instead of AST; limit scope to REST endpoints | Open |
| R4 | Scope creep on P8 SaaS | High | High | MVP: chat UI + one agent only; defer Stripe | Open |
| R5 | Solo velocity lower than 15 pts/sprint | Medium | Medium | Split stories; use spikes; adjust epic dates | Open |
| R6 | GitHub Project scope / token limits | Low | Low | Document manual setup in GITHUB-PROJECTS.md | Mitigated |

## Review cadence

- **Weekly:** Note new blockers in sprint retro
- **Monthly (every 4 sprints):** Update likelihood/impact; add or close risks

## Modification log

| Date | Change |
|------|--------|
| 2026-06-28 | Initial risk register |
