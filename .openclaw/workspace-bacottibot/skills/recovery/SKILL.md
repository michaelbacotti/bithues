# SKILL.md — recovery

## What it does
Provides disaster response playbook when the workspace is wiped or goes dark — assess damage, restore from git/backup, rebuild skills, verify websites.

## When to use
- Workspace appears empty or has BOOTSTRAP.md (workspace was wiped)
- Files are missing, session starts fresh with no memory
- "Workspace incident", "workspace wiped", "files are gone"

## When NOT to use
- For routine workspace management
- For git operations without disaster context
- When workspace is healthy and functional

## Inputs
- Git status and log analysis
- Backup commit identification
- GitHub repo verification (websites are always safe on GitHub)

## Outputs
- Restoration commands and verification steps
- Communication template for notifying Mike
- Prevention checklist verification

## Cost / Risk notes
Git operations and local file reads only. No external calls beyond git/github CLI.
