# SKILL.md — credentials-manager

## What it does
Tracks credentials and account information for the Bacotti family in a markdown file.

## When to use
- User says "add credential [service]", "new account [service]"
- User says "get [service]", "show password for [service]"
- User says "list credentials", "show all accounts"

## When NOT to use
- For actual password retrieval in external systems (use actual password manager)
- This is reference-only tracking, not a secure credential store

## Inputs
- Service name, username, password, account type, notes

## Outputs
- Markdown table entries in `credentials.md`

## Cost / Risk notes
No external calls. Writes to workspace credentials file. WARNING: Not a secure password manager — use 1Password, Bitwarden, or Apple Keychain for actual passwords.
