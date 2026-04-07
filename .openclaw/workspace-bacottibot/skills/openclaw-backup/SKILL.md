# SKILL.md — openclaw-backup

## What it does
Runs automated daily backup of the bacottibot workspace to iCloud Drive using a tar/gzip archive with 2-backup retention.

## When to use
- Manual backup verification
- Restoring from a previous backup
- Checking backup cron status
- Troubleshooting failed backups

## When NOT to use
- For file-level restore (use git checkout instead)
- For GitHub recovery (websites are on GitHub, not in this backup)
- When iCloud Drive is not available or syncing

## Inputs
- Backup script: `scripts/workspace-backup.sh`
- Optional: specific backup commit hash for restore

## Outputs
- Compressed tarball: `workspace-backup-YYYY-MM-DD-HHMMSS.tar.gz`
- Destination: `/Users/mike/Library/Mobile Documents/com~apple~CloudDocs/OpenClaw Workspace Backup/`

## Cost / Risk notes
Local file writes only. Excludes .DS_Store, *.tmp, node_modules/, .git/objects/. Cron job at 2 AM ET daily.
