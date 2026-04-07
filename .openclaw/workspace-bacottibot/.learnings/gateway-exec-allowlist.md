# Learning: Gateway Exec Binary Allowlist

**Date:** 2026-04-04

## What Happened

The `openclaw` binary itself is blocked by a **binary-level allowlist** that operates separately from the normal approval system. This means `exec` tool calls that invoke `openclaw` (or certain other binaries) will fail with an `allowlist miss` error even when the normal approval flow would allow them.

## Impact

- Cannot run `openclaw gateway` commands via exec
- Cannot use `crontab` via exec (also blocked by allowlist)
- Cannot run backup scripts that use blocked commands
- The approval system (allow-once / approve) is **not the problem** — the binary itself is on a deny list

## Resolution

Always go to **Terminal first** for openclaw commands. The exec tool's binary allowlist is managed independently of the per-command approval system.

## References

- TOOLS.md notes on backup and exec usage
