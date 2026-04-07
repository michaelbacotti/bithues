# SKILL.md — self-improving-agent

## What it does
Captures learnings, errors, and corrections to markdown files for continuous improvement, with promotion of broadly applicable learnings to permanent workspace documentation.

## When to use
- Command or operation fails unexpectedly
- User corrects the AI ("No, that's wrong...", "Actually...")
- User requests a capability that doesn't exist
- External API or tool fails
- AI realizes knowledge is outdated or incorrect
- Better approach discovered for a recurring task

## When NOT to use
- Minor one-off issues with no lasting pattern
- Issues already captured in other skills (skill-learn, decision-tracker)
- Situations where immediate fix is obvious and won't recur

## Inputs
- Error messages, correction context, user feedback
- CLI tools: record_decision.py, query_decisions.py, list_decisions.py, update_decision.py

## Outputs
- Learning/error/feature-request entries to `.learnings/LEARNINGS.md`, `.learnings/ERRORS.md`, `.learnings/FEATURE_REQUESTS.md`
- Promoted rules to AGENTS.md, SOUL.md, TOOLS.md, or CLAUDE.md when broadly applicable

## Cost / Risk notes
No external calls. Read/write to .learnings/ directory and workspace documentation files.
