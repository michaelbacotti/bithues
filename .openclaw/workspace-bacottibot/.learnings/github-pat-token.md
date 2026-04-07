# Learning: GitHub PAT Token

**Date:** 2026-04-04

## What

GitHub Personal Access Token for all API work:
```
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
```

## Details

- Owner: michaelbacotti
- Scope: repo (full repo access)
- Used by: openclaw-bot

## Where Stored

- TOOLS.md (primary source of truth)
- DO NOT hardcode in scripts — reference TOOLS.md

## Usage

```bash
curl -H "Authorization: Bearer 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" \
  https://api.github.com/repos/michaelbacotti/bithues/contents/articles
```

## Repos

- bithues
- dependability-us
- succession-holding-llc
