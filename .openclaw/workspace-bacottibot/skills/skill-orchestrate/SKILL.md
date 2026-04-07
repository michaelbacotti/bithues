# SKILL.md — skill-orchestrate

## What it does
Manages multi-stage task pipelines (research → execute → review) with persistent JSON queue files, enabling complex workflows to resume across sessions.

## When to use
- Complex multi-step tasks that span sessions
- When work needs clear stages with outputs that feed the next stage
- Long-running tasks where intermediate progress must be tracked

## When NOT to use
- Simple one-liner tasks (just do it directly)
- Tasks that must complete in a single session without persistence
- Trivial lookups or queries

## Inputs
- Task title and initial notes via CLI scripts
- Stage advancement triggers

## Outputs
- JSON files in `~/.openclaw/workspace-bacottibot/.orchestration/queue/<task-id>.json`
- Stage outputs stored in each task JSON (research_output, execute_output, review_output)

## Cost / Risk notes
No external calls. Writes JSON files to workspace orchestration directory.
