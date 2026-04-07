# SKILL.md — memory-of-time

## What it does
Logs time-indexed events (model changes, skill updates, decisions, milestones) to markdown files with frontmatter, enabling answers to "when did X happen" questions.

## When to use
- Model changes (switching AI models)
- Skill installs or modifications
- Major decisions or preference changes
- System or workflow configuration changes
- User says "remember this event" or "when did we last..."

## When NOT to use
- Minor routine actions
- One-off queries that don't create lasting context
- Learning/correction items (use skill-learn instead)

## Inputs
- Event type, title, optional description, and tags via CLI
- Auto-capture triggers on model changes, skill updates, major config changes

## Outputs
- Markdown files with YAML frontmatter in `~/.openclaw/workspace-bacottibot/.memory/events/`
- Event types: model_change, skill_added, skill_modified, decision, preference_change, system_change, workflow_change, external_event, milestone

## Cost / Risk notes
No external calls. Writes markdown files to workspace memory directory.
