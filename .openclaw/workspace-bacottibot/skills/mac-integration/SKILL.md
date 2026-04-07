# SKILL.md — mac-integration

## What it does
Interacts with Mac apps (Reminders, Calendar, Notes) via AppleScript to read lists, events, and notes.

## When to use
- User asks to show reminders, today's tasks, or what's on the calendar
- User asks to list or read notes from Notes app
- Checking what's happening today or upcoming

## When NOT to use
- For non-Mac environments
- For writing to Reminders/Calendar/Notes (read-only AppleScript access)
- For complex query needs beyond basic list/show

## Inputs
- AppleScript commands to query Reminders, Calendar, Notes apps

## Outputs
- Formatted reminders, calendar events, or note lists

## Cost / Risk notes
Read-only AppleScript execution on macOS. No external calls.
