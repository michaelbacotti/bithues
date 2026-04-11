# Archived Session Review Skill

## Purpose
Weekly scan of archived/deleted session files, extract learnings, update skills and memory accordingly.

## When
Cron job: Sundays at 9:00 AM Eastern

## How It Works

### Step 1 — Find Recent Archived Sessions
```bash
find /Users/mike/.openclaw/agents/main/sessions/*.deleted.* -newer /tmp/archived-session-review-last-run 2>/dev/null
find /Users/mike/.openclaw/agents/bacottibot/sessions/*.deleted.* -newer /tmp/archived-session-review-last-run 2>/dev/null
```

### Step 2 — Read Each Archived Session
For each `.deleted.*` file newer than last run:
1. Read the JSONL transcript
2. Identify: mistakes made, things that worked, incomplete outputs, skill gaps, tool failures
3. For each finding, create an entry in `memory/subagent-log/YYYY-MM-DD.md`

### Step 3 — Categorize Findings
- **Skill gap:** New skill needed → create SKILL.md
- **Tool failure:** Something broke → update the relevant skill's troubleshooting section
- **Mistake:** Accuracy error, hallucination, wrong format → add to `.learnings/` in the relevant skill
- **Good pattern:** Something worked well → add to AGENTS.md or the relevant skill as a best practice

### Step 4 — Update Memory
Add summary to `memory/subagent-log/YYYY-MM-DD.md`:
```
## [Weekly Archive Review — YYYY-MM-DD]
Sessions reviewed: N
Findings: [list]
Actions taken: [skills updated, learnings added, etc.]
```

### Step 5 — Touch Marker File
```bash
touch /tmp/archived-session-review-last-run
```

## Rules
- Focus on actionable improvements, not just noting what happened
- If a deleted session had work that was never committed, commit it now
- If a deleted session reveals a skill that should exist but doesn't, create it
- Never ignore a repeated mistake — add it to the relevant skill's `.learnings/` file