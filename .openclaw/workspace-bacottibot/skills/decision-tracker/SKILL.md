# SKILL.md — decision-tracker

## What it does
Logs key decisions with full context (what was decided, alternatives considered, and rationale) to markdown files for future reference.

## When to use
- User says "we decided on X", "let's go with Y", "from now on we'll..."
- Architecture or tool selection decisions
- Business choices with lasting implications
- Preference lock-in moments

## When NOT to use
- Minor formatting preferences (just apply and forget)
- Reversible opinions or one-off choices
- Task-specific lookups (not a decision context)

## Inputs
- Decision title, date, alternatives, rationale via CLI scripts
- Optional: outcome, tags, who decided

## Outputs
- Markdown decision files in `~/.openclaw/workspace-bacottibot/memory/decisions/` (create if missing)
- Integration events written to memory-of-time

## Cost / Risk notes
No external calls. Writes markdown files to workspace memory directory.
