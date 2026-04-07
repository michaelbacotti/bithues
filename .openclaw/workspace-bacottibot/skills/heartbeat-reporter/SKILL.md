# SKILL.md — heartbeat-reporter

## What it does
Runs on a schedule (daily/weekly) to compile a status report by reading memory-of-time events, decision-tracker entries, and dependability P/L — writes summary to HEARTBEAT.md or stdout.

## When to use
- Daily or weekly heartbeat cron job
- When user asks "heartbeat report" or "status report"
- Weekly memory maintenance review

## When NOT to use
- For real-time queries (just read the source files directly)
- When recent context is already fresh in session
- For detailed entity or trading analysis (use dedicated skills)

## Inputs
- Memory events: `~/.openclaw/workspace-bacottibot/.memory/events/` (memory-of-time)
- Decisions: `~/.openclaw/workspace-bacottibot/.memory/decisions/` (decision-tracker)
- Dependability P/L: `~/.openclaw/workspace-bacottibot/dependability_pl_tracker.csv` (if available)
- Past period: configurable (default: last 7 days)

## Outputs
- HEARTBEAT.md summary written to workspace root OR stdout
- Flagged items needing attention (missed meetings, stale decisions, P/L gaps)
- Key events from the period
- Recent decisions with outcomes

## Report Sections

1. **Period Summary** — "Past 7 days: X events, Y decisions"
2. **Key Events** — Timeline of significant events
3. **Recent Decisions** — Status of decisions made
4. **Financial Update** — Dependability P/L if data exists
5. **Flagged Items** — Needs attention, follow-up required

## Cost / Risk notes
No external calls. Read-only aggregation from workspace memory files.
