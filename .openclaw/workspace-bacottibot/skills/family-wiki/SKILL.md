# SKILL.md — family-wiki

## What it does
Tracks family members, relationships, important dates, preferences, and contact information for the Bacotti family in JSON format.

## When to use
- User asks about family members, relationships, or tree
- User says "who is [Name]", "show family tree", "birthday"
- Adding or updating family member info

## When NOT to use
- For business entity questions (use business-manager or kb-entity-overview)
- For contact management unrelated to family members

## Inputs
- Family member data (name, relationship, birthday, phone, telegram)
- JSON file at `~/openclaw/workspace/family-wiki/family.json`

## Outputs
- Updated family.json with member entries and relationships

## Cost / Risk notes
No external calls. Read/write to workspace family-wiki JSON file.
