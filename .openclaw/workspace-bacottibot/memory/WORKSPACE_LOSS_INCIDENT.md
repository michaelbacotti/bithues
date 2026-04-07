# Workspace Loss Analysis — April 3, 2026

## Timeline
- **March 25**: Workspace backup created (`openclaw-backup.tgz` at ~19MB)
- **March 26**: Files created in workspace (skills, References, entity folders, etc.)
- **March 29**: OpenClaw wizard ran with `lastRunMode: local` — may have reset something
- **April 2, 23:09-00:30**: Intensive bithues website work, subagents running
- **April 3, 11:21**: `ollama pull gemma4` ran successfully
- **April 3, 11:24**: Directory timestamp changed on `.openclaw/` — something happened here
- **April 3, ~11:24-12:00**: Workspace was wiped/deleted
- **April 3, 12:04**: New session started after user switched to Gemma4 and session froze
- **April 3, 12:26**: HEARTBEAT ran — workspace was already wiped
- **April 3, 13:00+**: Backup restored from March 26, `/tmp/bithues/` used for recovery

## What We Know

### Root Cause (Probable)
The workspace wipe happened **right after** the Ollama/gemma4 switch attempt. The session got stuck, user tried to recover, and something in that process caused the workspace to be reset or reinitialized.

Key evidence:
1. `.openclaw/` directory timestamp changed to April 3 11:24 — exactly when the gemma4 switch happened
2. User noted "when i switched to ollama/gemma4. are you working?" and the session froze
3. New session started at 12:04 after the issue

### Executive Summary
- **Website content**: ✅ Safe on GitHub (all pushed)
- **Workspace files**: ❌ Wiped between 11:21-12:00 April 3
- **Skills lost**: 11 workspace skills (unavailable in NERVE)
- **Files recovered**: Most from March 26 backup + `/tmp/bithues/` work directory
- **Files NOT recovered**: Skills created between March 26-April 3, any unsaved work

## Current State (April 3, 2026)
- Workspace at `~/.openclaw/workspace-bacottibot/` is ~80% restored
- 11 skills still missing (shown as "unavailable" in NERVE)
- GitHub repos have all website content (bithues, dependability-us, succession-holding-llc)
- MEMORY.md exists but may be missing recent entries

## Prevention Plan

### 1. Nightly Workspace Backup (CRITICAL)
Create a cron job that backs up the entire workspace directory to a local tar.gz file EVERY NIGHT at 1AM.

Backup command:
```bash
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/workspace-bacottibot/
```

Keep last 7 backups, delete older:
```bash
find ~/ -name "openclaw-backup-*.tar.gz" -mtime +7 -delete
```

### 2. Git Push for Important Work
Before ending sessions after major work, ensure all important changes are pushed to GitHub.

### 3. Session Compaction Awareness
Session compaction (memory flush) runs when sessions get long. This is normal but can cause issues with very long conversations. Consider:
- Starting fresh sessions for big tasks
- Not relying on session continuity for critical work

### 4. Workspace Location
The workspace is at `~/.openclaw/workspace-bacottibot/`. This should be backed up regularly, not just the entire `.openclaw/` directory.

## Action Items
1. ⬜ Create nightly backup cron job for workspace
2. ⬜ Document exact cause of workspace wipe (still uncertain)
3. ⬜ Rebuild 11 missing skills if subagent conversations reveal what they were
4. ⬜ Update MEMORY.md with this incident
5. ⬜ Set up proper exec allowlisting to prevent approval timeouts

## Missing Skills (NERVE shows 11 unavailable)
Based on subagent conversations, likely includes:
- kb-accounting-review related skills
- kb-dependability-holding-llc skill
- kb-succession-holding-llc skill
- kb-tax-preparation skill
- kb-nerve-openclaw-improvements skill
- options-pro-skill (referenced in subagent list)
- nerve-exec-bugfix skill

These were created between March 26-April 3 and are truly lost.
