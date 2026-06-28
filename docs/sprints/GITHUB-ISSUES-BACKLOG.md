# GitHub Issues Backlog (local manifest)

Use this file when creating issues on [Agentic-X-platform-Intelligence-System/jarvis](https://github.com/Agentic-X-platform-Intelligence-System/jarvis).

**Automated creation:** After you have **write** access to the repo:

```powershell
gh auth status   # confirm push/admin on jarvis
.\scripts\agile\setup-all.ps1
```

**Manual creation:** Use issue templates in `.github/ISSUE_TEMPLATE/` and bodies in `.github/epics/` and `.github/stories/`.

---

## Epics

| ID | Title | Labels | Milestone | Body file |
|----|-------|--------|-----------|-----------|
| E1 | Epic 1: P1 - stem Kernel & Jarvis CLI | epic, p1-high, stem, jarvis | M1 | `.github/epics/E1-stem-cli.md` |
| E2 | Epic 2: P1 - Aura Voice Migration | epic, p1-high, aura, stem | M2 | `.github/epics/E2-aura-voice.md` |
| E3 | Epic 3: P2 - Edith RAG Knowledge Base | epic, p2-medium, edith | M3 | `.github/epics/E3-edith-rag.md` |
| E4 | Epic 4: P3 - Karen Code Review Bot | epic, p2-medium, karen | M4 | `.github/epics/E4-karen-review.md` |
| E5 | Epic 5: P4 - Friday Research Agent | epic, p2-medium, friday | M5 | `.github/epics/E5-friday-research.md` |
| E6 | Epic 6: P5 - Cognis Java Migrator | epic, p2-medium, cognis | M6 | `.github/epics/E6-cognis-migrator.md` |
| E7 | Epic 7: P6 - Kinetix Dev Crew | epic, p2-medium, kinetix | M7 | `.github/epics/E7-kinetix-crew.md` |
| E8 | Epic 8: P7 - Aero Production API | epic, p2-medium, aero | M8 | `.github/epics/E8-aero-api.md` |
| E9 | Epic 9: P8 - Full-Stack AI SaaS | epic, p2-medium, aero, jarvis, aura | M9 | `.github/epics/E9-saas-capstone.md` |

---

## Sprint 1 stories (Epic E1)

| ID | Title | Points | Labels | Body file |
|----|-------|--------|--------|-----------|
| S1.1 | [Story] Multi-provider LLM interface | 5 | story, p1-high, stem, sprint-1 | `.github/stories/S1.1-llm-providers.md` |
| S1.2 | [Story] Hybrid LLM router | 5 | story, p1-high, stem, sprint-1 | `.github/stories/S1.2-hybrid-router.md` |
| S1.3 | [Story] Pydantic tool framework | 5 | story, p1-high, stem, sprint-1 | `.github/stories/S1.3-tool-framework.md` |
| S1.4 | [Story] P1 tools — filesystem | 3 | story, p1-high, stem, sprint-1 | `.github/stories/S1.4-filesystem-tools.md` |
| S1.5 | [Story] P1 tools — shell and web | 5 | story, p1-high, stem, sprint-1 | `.github/stories/S1.5-shell-web-tools.md` |

**Sprint 1 total:** 23 points

---

## CLI one-liners (after labels + milestones exist)

```powershell
$Repo = "Agentic-X-platform-Intelligence-System/jarvis"
gh issue create --repo $Repo --title "Epic 1: P1 - stem Kernel & Jarvis CLI" --label "epic,p1-high,stem,jarvis" --body-file .github/epics/E1-stem-cli.md --milestone "M1 — stem + CLI"
```

Repeat for each row above.
