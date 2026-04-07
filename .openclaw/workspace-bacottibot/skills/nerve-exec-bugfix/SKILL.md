# SKILL.md — nerve-exec-bugfix

## What it does
Diagnoses and fixes exec command approval issues in OpenClaw/NERVE — commands getting denied with "approval-timeout (allowlist-miss)" errors.

## When to use
- "Exec denied", "approval timeout", "command not running", "allowlist miss"
- Commands blocked by security policy
- Subagent exec permissions failing

## When NOT to use
- For workspace recovery (use recovery skill)
- For general OpenClaw improvements (use kb-nerve-openclaw-improvements)
- For non-OpenClaw exec issues

## Inputs
- Gateway status: `openclaw gateway status`
- Approval system: `openclaw approvals --help`
- OpenClaw config: `~/.openclaw/openclaw.json`

## Outputs
- Diagnosis of specific approval issue
- Fix applied (allowlist, config edit, pre-approval) or workaround recommended

## Cost / Risk notes
OpenClaw CLI and config edits. May require approval for config changes. No external calls.
