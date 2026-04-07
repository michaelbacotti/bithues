---
name: github-safe-push
description: Use whenever pushing to any GitHub repository. Prevents repo corruption from force-pushes, stale parent SHAs, and unsafe merge strategies. Required for all git push operations in this workspace.
---

# github-safe-push

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
1. Sub-agent should clone the repo fresh OR do `git fetch origin` at start
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

## Repo-Specific Notes

| Repo | Branch | Push Rules |
|------|--------|-----------|
| michaelbacotti/bithues | main | Normal push only, never force |
| michaelbacotti/dependability-us | main | Normal push only |
| michaelbacotti/succession-holding-llc | main | Normal push only |
| michaelbacotti/bithues-lab | main | Normal push |

## If Push Is Rejected

1. `git fetch origin`
2. `git merge origin/main` — resolve any conflicts
3. `git push origin main`
4. If still rejected → check for branch protection rules at github.com/{owner}/{repo}/settings/branches

## After Every Successful Push

```bash
# Verify
git log --oneline -3
echo "Pushed to: $(git remote get-url origin)"
```

## Quick Reference

```bash
# Safe commit sequence
git add <files>
git commit -m "descriptive message"
git fetch origin
git merge origin/main  # if behind
git push origin main
```
