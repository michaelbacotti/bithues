# Learning: Backup Folder Stray Files

**Date:** 2026-04-04

## What Happened

The workspace backup destination folder (iCloud Drive: `OpenClaw Workspace Backup`) contained 2 stray HTML files that were not part of the backup archive.

## Cause

These were intermediate files from the bithues article sub-agent's local workspace copy. When the sub-agent generates or processes HTML content, it can leave behind temporary or draft HTML files in the working directory.

## Are They Harmful?

**No.** The backup script explicitly excludes `*.tmp` files and uses tar's archive format. These HTML files are simply sitting in the destination folder alongside the actual backup archives — they don't affect backup integrity.

## Action Taken

None required — noted as informational. The backup system is working correctly.

## Prevention

Sub-agents that generate HTML content should clean up intermediate files before completing. This is a cosmetic issue only.
