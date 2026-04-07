# Learning: GitHub API Push for Website Updates

**Date:** 2026-04-04

## What Happened

The bithues article sub-agent successfully pushed **31 files** to the bithues GitHub repo using the GitHub API `PUT` method.

## Key Details

- Method: `PUT /repos/{owner}/{repo}/contents/{path}`
- Each file requires: `message`, `content` (base64), `sha` (of existing file for updates)
- For new files: no `sha` required
- The sub-agent worked from a local workspace copy, which can leave intermediate files

## Correct Approach for Website Updates

1. Fetch current file list via `GET /repos/{owner}/{repo}/contents/{path}`
2. Get SHA for each existing file
3. Use `PUT` to update/create each file
4. Clean up any stray intermediate files from local workspace copies

## Note on Stray Files

The backup folder contained 2 stray HTML files that were intermediates from the article update sub-agent's local workspace copy. These are not harmful but should be cleaned up periodically.
