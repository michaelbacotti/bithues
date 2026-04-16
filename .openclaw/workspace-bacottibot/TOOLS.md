# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Hardware

- **MacBook Pro 16"** — M4 Max (Nov 2024), 48 GB RAM, macOS Tahoe (Sequoia)
  - Serial: M0Y49CX7PP
  - This machine runs OpenClaw locally

## GitHub

- **Token**: `[GITHUB_TOKEN_REDACTED]` (openclaw-bot, repo scope)
- **Owner**: michaelbacotti
- **Repos**: bithues, dependability-us, succession-holding-llc

## GitHub API

Base URL: `https://api.github.com`
Auth header: `Authorization: Bearer <token>`

To fetch repo contents:
```
GET /repos/michaelbacotti/bithues/contents/articles
GET /repos/michaelbacotti/bithues/contents/articles/{filename}
```

To update a file:
```
PUT /repos/michaelbacotti/bithues/contents/articles/{filename}
Body: { "message": "...", "content": "<base64>", "sha": "<file_sha>" }
```

## Backup

- **Backup script**: `scripts/workspace-backup.sh`
- **Destination**: `/Users/mike/Library/Mobile Documents/com~apple~CloudDocs/OpenClaw Workspace Backup/`
- **Schedule**: Daily 2 AM EDT, keeps 2 most recent
- **Format**: `workspace-backup-YYYY-MM-DD-HHMMSS.tar.gz` (~2.5 GB)

---

Add whatever helps you do your job. This is your cheat sheet.
