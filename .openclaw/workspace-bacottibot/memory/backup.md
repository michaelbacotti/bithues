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

### 🔧 Incident & Fix (2026-04-05)
**Problem:** Non-backup files accumulated in the backup destination:
- 18 loose files (XLSX XML parts, HTML chat exports, .pyc bytecode) — sub-agent artifacts from `/tmp` that iCloud synced to the backup folder
- `workspace-bacottibot/` subfolder — iCloud sync quirk creating a nested workspace copy
- 3 backups instead of 2 — retention was supposed to prune but didn't catch the extra

**Fix applied to `scripts/workspace-backup.sh`:**
Added a pre-archive scrub step that deletes ALL loose items from `$DEST_DIR` before creating the new tarball. Only `*.tar.gz` files are preserved:
```bash
for f in *; do
  [[ "$f" == *.tar.gz ]] && continue
  [[ -z "$f" || "$f" == "*" ]] && continue
  rm -rf -- "$f" && echo "  Removed loose item: $f"
done
```

This prevents any future artifact accumulation — iCloud sync quirks, sub-agent exports, and temp files are all wiped before each backup runs.
