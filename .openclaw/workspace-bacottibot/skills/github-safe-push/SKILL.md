---
name: github-safe-push
description: Use whenever pushing to any GitHub repository. Prevents repo corruption from force-pushes, stale parent SHAs, and unsafe merge strategies. Required for all git push operations in this workspace.
---

# github-safe-push

## The Core Rule

**Every push must be verified before claiming success.** Fetch SHA, push, confirm the live URL size matches local. File size mismatch means the push didn't land.

## The Problem

On 2026-04-06, the `michaelbacotti/bithues` repo was wiped/restored 3 times because sub-agents did unsafe git operations:
- Force-pushing to main
- Pushing without fetching first (stale parent SHA)
- Using `git push --force` in sub-agents
- Not checking remote state before push

## Required Workflow — Always

### Before ANY push:

```bash
# 1. Fetch latest from remote
git fetch origin

# 2. Check status
git status

# 3. If behind origin/main, merge (not rebase!)
git merge origin/main

# 4. Only THEN push
git push origin main

# 5. Verify push succeeded
git log --oneline -3
```

### NEVER do:
- `git push --force` / `git push -f`
- `git push` without fetching first
- Sub-agents doing git operations without fetch-first
- Creating commits in /tmp and trying to push from there

## For Sub-agents

If a sub-agent needs to push:
1. Clone the repo fresh OR do `git fetch origin` at start
2. Make changes in the cloned repo
3. Commit with clear message
4. `git push origin main` — simple push, never force
5. If push fails due to stale SHA: fetch → merge → push again

## GitHub API (REST) — Safe Pattern

When using `curl` to call GitHub API for file operations:

```bash
# 1. GET current file SHA (always)
GET /repos/{owner}/{repo}/contents/{path}
Response includes: "sha": "<commit_sha>"

# 2. PUT with current SHA (prevents overwrite conflicts)
PUT /repos/{owner}/{repo}/contents/{path}
Body: { "message": "...", "content": "<base64>", "sha": "<commit_sha>" }
```

**CRITICAL:** Always include the `sha` field from step 1. Without it, the API returns 422.

## After Every Successful Push — VERIFY BEFORE CLAIMING SUCCESS

```bash
# 1. Confirm live file size matches local
curl -s "https://www.bithues.com/{path}" | wc -c
# Compare to local: wc -c /local/file

# 2. Confirm commit landed
git log --oneline -3
git fetch origin
git log --oneline -3  # compare with origin/main

# 3. Browser screenshot — verify visual change
# If a visual change was made, screenshot BEFORE claiming done
```

**Never tell Mike "it's pushed" until steps 1 and 2 are confirmed.** File size mismatch = push failed. Refore and repush.

## Quick Reference

```bash
# Safe commit sequence
git add <files>
git commit -m "descriptive message"
git fetch origin
git merge origin/main  # if behind
git push origin main

# Verify after push
curl -s "https://www.bithues.com/{path}" | wc -c
```

## File Deletion — ABSOLUTE RULE

**NEVER delete files from the workspace.**
- Use `trash` or `mv to a backup folder` instead of `rm`
- Before any delete operation: verify the file is committed to git
- Before any delete operation: verify the file is in the latest iCloud backup
- If a subagent or script requests deletion: refuse and move the file to `~/.openclaw/trash/` instead
- Only permanently delete after confirming: committed to git AND backed up to iCloud

**"I thought it was safe" is not an excuse. Verify before every deletion.**
