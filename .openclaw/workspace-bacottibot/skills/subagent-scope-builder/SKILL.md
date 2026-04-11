---
name: subagent-scope-builder
description: Use whenever writing a subagent task prompt. Ensures tight scope, one-shot goals, verifiable checkpoints, and accuracy-focused instructions. Prevents timeouts and hallucinated completions.
---

# sub-agent-scope-builder

## The Problem

Most subagent failures fall into three buckets:
1. **Scope too large** → times out, delivers nothing
2. **No verification step** → reports "done" without actually completing  
3. **Vague success criteria** → subagent decides it's done when it isn't

This skill forces you to write tighter, more accurate subagent prompts.

---

## Before Writing Any Subagent Prompt — Ask These Questions

1. **What is the ONE thing this subagent must accomplish?** (If you wrote more than one, split it.)
2. **How will it know when it's done?** (Not "I think it's done" — specific check.)
3. **What tools does it actually have?** (GitHub API? browser? exec?)
4. **What can go wrong, and how does it recover?** (Timeout? API error?)
5. **Is this a one-shot or does it need session persistence?** (Almost always one-shot for fix-it tasks.)

---

## The Scope Formula

```
GOAL: [one specific, verifiable thing]

SCOPE: [exact files, directories, or pages — no vague "etc."]

STEPS: [numbered, 1-5 max — if more than 5 steps, split into 2 subagents]

VERIFICATION: [exactly how to confirm success — screenshot, API check, grep output]

RULES: [constraints — fetch SHA first, no force-push, etc.]

FAILURE RECOVERY: [what to do if timeout/error — report partial results, don't claim false success]
```

---

## Scope Size Guidelines

| Task size | Recommended scope |
|-----------|-------------------|
| Small (1-10 files) | One subagent, all in one prompt |
| Medium (10-50 files) | One subagent, batch processing with checkpoint reporting |
| Large (50+ files) | Sequential subagents by directory or batch |
| Visual rewrite | Do NOT run as subagent — token-heavy, OOM risk. Do in main session. Subagent only after functional bugs are fixed.
| Any task requiring reading PDFs | Limit to 2 PDFs max per subagent |

**Hard rule:** One bug fix per subagent. Do NOT combine "fix ESC key" + "fix walking speed" + "rewrite visuals" into one subagent. If one times out, you lose all three.

---

## Writing Verification Steps

Bad verification (too vague):
> "Take a screenshot to confirm it works"

Good verification (specific):
> "After pushing, verify by:
> 1. curl the live URL → confirm file size matches local (wc -c)
> 2. grep the pushed file for 'TWN_H + 100' → confirm the fix is present
> 3. Take browser screenshot of https://www.bithues.com/games/autoduel/"
> 4. Report: live file size, grep result, screenshot URL"

---

## Handling Timeout

If a subagent times out:
- Check the result — was anything useful delivered?
- If partial work: spawn a new subagent with EXACTLY the remaining work (not the full task)
- If no work delivered: spawn fresh with tighter scope
- NEVER claim the task is done if the subagent timed out before completing

---

## Accuracy Reminder (include in every subagent prompt)

Add this block to every subagent task:
```
## ACCURACY REMINDER
- Read actual lines before claiming fixed
- Take screenshot BEFORE saying "done"
- If uncertain: report what you checked and what you found — do not guess
- File size alone is not proof of success — verify content
- Mike's browser report > your headless browser result — if a bug is reported, investigate don't deflect
```

---

## Spawn Syntax Reference

```javascript
sessions_spawn(
  mode="run",           // one-shot, announces result
  runtime="subagent",   // OpenClaw subagent
  task="[full prompt]"   // include goal/scope/steps/verification/rules
)
```
