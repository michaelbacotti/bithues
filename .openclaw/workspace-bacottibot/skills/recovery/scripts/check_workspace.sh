#!/bin/bash
# Workspace Health Check
# Run this to quickly assess if the workspace is healthy

WORKSPACE="/Users/mike/.openclaw/workspace-bacottibot"
cd "$WORKSPACE"

echo "=== WORKSPACE HEALTH CHECK ==="
echo ""

# 1. File count
FILE_COUNT=$(ls -1 | wc -l)
echo "Files in workspace: $FILE_COUNT"

# 2. Critical files
echo ""
echo "Critical files:"
for f in MEMORY.md SOUL.md AGENTS.md TOOLS.md; do
    if [ -f "$f" ]; then
        echo "  ✅ $f"
    else
        echo "  ❌ $f MISSING"
    fi
done

# 3. BOOTSTRAP check
if [ -f "BOOTSTRAP.md" ]; then
    echo ""
    echo "🚨 BOOTSTRAP.MD EXISTS - WORKSPACE WAS WIPED"
fi

# 4. Git status
echo ""
echo "Git status:"
git status --short 2>/dev/null | head -5
if [ $? -ne 0 ]; then
    echo "  ❌ Not a git repo"
fi

# 5. Recent commits
echo ""
echo "Last 3 commits:"
git log --oneline -3 2>/dev/null || echo "  No commits found"

# 6. Skills count
echo ""
SKILL_COUNT=$(ls -d skills/*/ 2>/dev/null | wc -l | tr -d ' ')
echo "Skills: $SKILL_COUNT"

# 7. Cron check
echo ""
echo "Backup cron (nightly):"
openclaw cron list 2>/dev/null | grep -i backup || echo "  No backup cron found"

# 8. Disk space
echo ""
echo "Disk space:"
df -h "$WORKSPACE" | tail -1 | awk '{print "  Available: " $4}'

echo ""
echo "=== CHECK COMPLETE ==="
