# GitHub Organization Setup

**AXIS** = Agentic X-platform Intelligence System  
**Flagship repo:** `jarvis` (this monorepo)

## Remote URL (placeholder)

The GitHub org slug is not finalized yet. When the org is created, point the remote at:

```bash
git remote set-url origin https://github.com/<AXIS-ORG-SLUG>/jarvis.git
```

Replace `<AXIS-ORG-SLUG>` with your AXIS organization slug from GitHub org settings.

## Verify remote

```bash
git remote -v
```

## Push (after org is ready)

```bash
git push -u origin main
```

## Notes

- Cannot push until the org slug is known — document only until then.
- Suggested future repos under the org: `jarvis` (hub), optional extracts `edith`, `friday`, `aero`.
- See [agentic-ai-ideas/scope.md](../../agentic-ai-ideas/scope.md) §16 for org registry.
