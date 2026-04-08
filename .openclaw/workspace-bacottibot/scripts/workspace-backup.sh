#!/bin/bash
# Workspace backup script — keeps last 2 days
# Destination: iCloud Drive

DEST_DIR="/Users/mike/Library/Mobile Documents/com~apple~CloudDocs/OpenClaw Workspace Backup"
WORKSPACE_DIR="/Users/mike/.openclaw/workspace-bacottibot"
RETENTION=2

# Ensure destination exists
mkdir -p "$DEST_DIR"

# SAFETY: Scrub ALL non-backup loose files from destination before archiving.
# This prevents artifacts (sub-agent exports, iCloud sync quirks, temp files)
# from accumulating in the backup folder. Only *.tar.gz should live here.
echo "Cleaning destination folder..."
cd "$DEST_DIR" || exit 1
for f in *; do
  [[ "$f" == *.tar.gz ]] && continue
  [[ -z "$f" || "$f" == "*" ]] && continue
  rm -rf -- "$f" && echo "  Removed loose item: $f"
done

# Create backup filename with timestamp
TIMESTAMP=$(date +"%Y-%m-%d-%H%M%S")
BACKUP_NAME="workspace-backup-${TIMESTAMP}.tar.gz"
BACKUP_PATH="${DEST_DIR}/${BACKUP_NAME}"

# Create the archive (excluding temp/cache dirs)
tar -czf "$BACKUP_PATH" \
  --exclude='.DS_Store' \
  --exclude='*.tmp' \
  --exclude='node_modules' \
  --exclude='.git/objects' \
  -C "$WORKSPACE_DIR" .

echo "Backup created: $BACKUP_PATH"

# Prune old backups — keep only the last $RETENTION
BACKUPS=($(ls -1t workspace-backup-*.tar.gz 2>/dev/null))

if [ ${#BACKUPS[@]} -gt $RETENTION ]; then
  echo "Pruning old backups (keeping $RETENTION of ${#BACKUPS[@]})..."
  for ((i=$RETENTION; i<${#BACKUPS[@]}; i++)); do
    rm -f "${BACKUPS[$i]}"
    echo "  Removed: ${BACKUPS[$i]}"
  done
fi

echo "Backup complete. $(ls -1t workspace-bacottibot-*.tar.gz 2>/dev/null | wc -l | tr -d ' ') backup(s) retained."
