# SKILL.md — memory-maintenance

## What it does
Maintains long-term memory files by reviewing daily logs, pruning stale content, and promoting significant events to topic files.

## When to use
- Weekly memory review (ideally via heartbeat)
- MEMORY.md has grown too large
- Daily files need consolidation
- Need to split content into topic files

## When NOT to use
- After every session (overkill — daily files capture enough)
- When MEMORY.md is already well-organized
- For immediate information retrieval (just read the files)

## Inputs
- Daily memory files: `memory/YYYY-MM-DD.md`
- Topic files: `memory/entities.md`, `memory/investing.md`, etc.
- MEMORY.md index

## Outputs
- Updated topic files with new relevant content
- Pruned stale/outdated content
- Updated MEMORY.md index

## Cost / Risk notes
No external calls. Read/write to workspace memory files.
