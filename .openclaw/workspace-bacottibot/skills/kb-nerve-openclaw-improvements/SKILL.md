# SKILL.md — kb-nerve-openclaw-improvements

## What it does
Researches, identifies, and implements improvements to the NERVE OpenClaw Cockpit interface and OpenClaw agent system — fixes bugs and improves workflows.

## When to use
- "Improve NERVE", "OpenClaw improvements", "fix OpenClaw", "NERVE bug"
- Exec approval timeouts or permission issues
- Model switching problems
- Session compaction or context limit issues
- Workflow efficiency recommendations

## When NOT to use
- For workspace file recovery (use recovery skill)
- For skill-specific questions (use that skill directly)
- For non-OpenClaw issues

## Inputs
- OpenClaw config: `~/.openclaw/openclaw.json`
- Gateway status: `openclaw gateway status`
- Skill list: `openclaw skills list`

## Outputs
- Identified issues and fixes applied
- Configuration recommendations
- Workflow improvement suggestions

## Cost / Risk notes
OpenClaw CLI commands only. Config edits may require approval. No external calls.
