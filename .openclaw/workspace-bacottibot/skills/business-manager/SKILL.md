# SKILL.md — business-manager

## What it does
Tracks and reports on all Bacotti family business entities (Bacotti Inc., Dependability Holding, HOUSE Inc., Succession Holding, Trust) including P/L, meetings, and compliance.

## When to use
- User provides business updates, financial data, or entity information
- User asks for a business report, summary, or entity status
- Tracking P/L, meetings, compliance, or entity activities

## When NOT to use
- For specific deep-dive expertise (use kb-dependability-holding, kb-succession-holding, etc.)
- For tax filing questions (use kb-tax-preparation)
- For trading decisions (use options-pro)

## Inputs
- User-provided business updates (entity, month, amounts)
- Entity data folders at `~/openclaw/workspace/[entity-folder]/`
- P/L tracker CSV

## Outputs
- Update files in entity folders (`updates/YYYY-MM.md`)
- Detailed business reports with financials, meetings, compliance status

## Cost / Risk notes
No external calls. Read/write to entity folders in workspace.
