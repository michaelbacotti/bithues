# Learning: GitHub PAT Token

**Date:** 2026-04-04

## What

GitHub Personal Access Token for all API work:
```
[GITHUB_TOKEN_REDACTED]
```

## Details

- Owner: michaelbacotti
- Scope: repo (full repo access)
- Used by: openclaw-bot

## Where Stored

- ~/.openclaw/credentials/github.txt (primary source of truth)
- DO NOT hardcode in scripts — reference ~/.openclaw/credentials/github.txt

## Usage

```bash
curl -H "Authorization: Bearer $(cat ~/.openclaw/credentials/github.txt)" \
  https://api.github.com/repos/michaelbacotti/bithues/contents/articles
```

## Repos

- bithues
- dependability-us
- succession-holding-llc
