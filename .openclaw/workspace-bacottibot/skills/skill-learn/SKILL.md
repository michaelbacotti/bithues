# SKILL.md — skill-learn

## What it does
Captures corrections, improvements, and lessons from user feedback into structured markdown files for later review and promotion into permanent skill documentation.

## When to use
- User says "actually...", "remember this", "you should...", "next time...", "that's wrong"
- User provides a correction ("No, that's wrong, do X instead")
- A better approach is discovered for a recurring task
- Command or operation fails unexpectedly

## When NOT to use
- Minor one-off formatting preferences (just apply and forget)
- Issues already logged as errors or feature requests
- When a direct skill edit would be faster than capturing a learning

## Inputs
- User feedback (verbal corrections, instructions, or preferences)
- Trigger phrases: "actually...", "remember this", "you should...", "next time...", "that's wrong"

## Outputs
- Markdown files in `~/.openclaw/workspace-bacottibot/.learnings/<topic>/<date>-<summary>.md`
- Optionally proposed edits to relevant SKILL.md files

## Cost / Risk notes
No external calls. Read-only except for writing to .learnings/ directory.
