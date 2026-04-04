# Workspace Backup — iCloud

## ✅ Backup Setup (2026-04-04)

### Cron Job
- **Schedule:** Daily at 2:00 AM EDT
- **Job ID:** `da9af2a7-e46d-41e6-8964-75a8fcb24149`
- **Session:** isolated

### Backup Script
- **Path:** `scripts/workspace-backup.sh`
- **Destination:** `/Users/mike/Library/Mobile Documents/com~apple~CloudDocs/OpenClaw Workspace Backup/`
- **Format:** `workspace-backup-YYYY-MM-DD-HHMMSS.tar.gz`
- **Retention:** 2 most recent backups (auto-pruned)
- **Size:** ~2.5 GB per backup

### What's Backed Up
- Entire workspace: `memory/`, `References/`, `skills/`, `*.md` files
- Excludes: `.DS_Store`, `*.tmp`, `node_modules`, `.git/objects`

### Restore Instructions
1. Navigate to backup destination in Finder or Terminal
2. Double-click `.tar.gz` to decompress (Finder), or:
   ```bash
   cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/OpenClaw\ Workspace\ Backup/
   tar -xzf workspace-backup-YYYY-MM-DD-HHMMSS.tar.gz
   ```
3. Contents extract to `workspace-bacottibot/` folder

### Notes
- Cron schedules stored in OpenClaw config (persist independently)
- Backup is iCloud-synced (local + cloud redundancy)
- First test backup ran successfully: `workspace-backup-2026-04-04-111151.tar.gz` (~2.5 GB)
