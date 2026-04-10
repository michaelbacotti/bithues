---
name: bot-manager
description: Manage and orchestrate sub-agent bots. Use when spawning, monitoring, steering, or killing sub-agents. Tracks active bots, delegates tasks, and ensures bots complete their work effectively.
metadata:
  {
    "openclaw": { "emoji": "🤖" },
  }
---

# bot-manager

Manages and orchestrates sub-agent bots: spawning, monitoring, steering, and killing background sessions.

## Core Principle

**Accuracy over speed. Always.**

Mike's rule: *slow and careful quality over speed. Truth and accuracy are non-negotiable.* This applies to subagent work too. A subagent that times out and delivers nothing is better than one that delivers wrong code silently.

---

## When to Delegate

**Delegate when:**
- A task is too large for the main session (many files, batch operations)
- Mike wants to keep chatting while work happens in the background
- Work can be verified after completion
- Mike explicitly asks to "delegate" or "have a subagent handle this"

**Do NOT use when:**
- Task is a simple lookup or one-liner
- Mike needs the answer immediately
- Task requires this conversation's context (subagents get only the task prompt)

---

## How to Delegate

### Step 1: Choose Scope

Before spawning:
- What is the EXACT scope? (not "fix the site" — more like "add nav CSS to the 47 remaining HTML files in authors/ and category/")
- What does done look like? (specific, verifiable criteria)
- What tools does the subagent have?
- **Is this one thing, or should it be split?** (If more than 5 steps, split)

### Step 2: Write the Task Prompt

A good prompt includes:

**1. GOAL** — one clear sentence
**2. SCOPE** — exact files/directories
**3. STEPS** — numbered, 1-5 max
**4. VERIFICATION** — how to confirm success (screenshot, API check, grep)
**5. RULES** — constraints (never force-push, fetch-before-put)
**6. FAILURE RECOVERY** — what to do if timeout/error

### Step 3: Spawn

```
sessions_spawn(
  mode="run",           // one-shot, announces result when done
  runtime="subagent",
  task="...prompt..."
)
```

Use `mode="session"` only when the subagent needs steering mid-task.

### Step 4: Monitor Without Blocking

After spawning:
- Do NOT poll with `sessions_list` or `sessions_history`
- Wait for the completion event as a message
- Mike can talk to you about other things

### Step 5: Audit the Result — MANDATORY

When the subagent completes:
1. **Read the result** — don't assume it got everything right
2. **Verify completeness** — did it touch all the files it claimed?
3. **Verify correctness** — spot-check 3-5 files via GitHub API or browser
4. **Read the actual code** — before telling Mike "it's fixed"
5. **Take a screenshot** — verify the live URL shows the fix
6. If gaps found → spawn a NEW subagent for only the remaining work
7. Report to Mike: what was done, verified, any gaps

**If the subagent timed out:** It delivered nothing. Do NOT tell Mike "it's done." Either fix it yourself (if small) or spawn a new subagent with tighter scope.

---

## Common Failure Patterns

| Failure | Cause | Prevention |
|---------|-------|------------|
| Incomplete work | Scope too large or vague | Break into smaller batches |
| Wrong files | Vague instructions | Be specific about file list |
| Reports done prematurely | No verification required | Mandate verification in prompt |
| GitHub conflicts | Didn't fetch before push | Include fetch-before-push rule |
| Timeout | Too much work | Split into sequential subagents |
| Silent failure | No error reported | Always require screenshot + specific verification |
| Bug not fixed | Said fixed without reading code | pre-flight-check: read actual lines first |
| Broken code pushed | No local verification | Verify file locally before pushing |

---

## Checkpointing Large Jobs

For 100+ file batches:
- "Report every 50 files: done count, remaining, any errors"
- If subagent times out mid-batch, a new subagent can pick up where it left off

---

## The Golden Rule

**Mike must always be able to talk to you.** If a subagent is running and Mike sends a message, respond to Mike. The subagent delivers its completion when done.

---

## Mike's Bug Reports Are Ground Truth

If Mike reports a bug — especially "it doesn't work in my browser" — **investigate immediately.** Do not:
- Argue that it works in your headless browser
- Blame browser cache without evidence
- Dismiss as a one-time fluke

**Correct response to "black screen":**
1. Ask what browser
2. Check the browser console errors
3. Read the relevant code to find the bug
4. Fix it and verify

---

## Spawn Examples

### Example: Batch file fix (tight scope)

```
task: Fix nav dropdown CSS in the 47 remaining HTML pages in authors/ and category/ directories.

Steps:
1. GET each file from GitHub
2. If missing .nav-item:hover .dropdown CSS → add the inline style block before </head>
3. PUT updated file back to GitHub

Verification: After completing, take browser screenshots of:
- https://www.bithues.com/authors/t-stone.html
- https://www.bithues.com/category/adventure.html
Confirm nav dropdowns work.

Rules:
- Always fetch SHA before pushing
- Use mode="run" (one-shot)
- Report exactly which 47 files were fixed

## ACCURACY REMINDER
- Read actual lines before claiming fixed
- Take screenshot BEFORE saying "done"
- If uncertain: report what you checked and what you found — do not guess
- Mike's browser report > your headless browser result
```

### Example: Bug fix (one-shot)

```
task: Fix ESC key not exiting garage screen in /Users/mike/autoduel/index.html

Steps:
1. Read handleKeyDown function — find line where WALKING state returns early
2. Move GARAGE check before WALKING check
3. Verify fix: grep for "gameState === 'GARAGE'" — confirm it comes before WALKING block
4. Push to GitHub with fetch-before-SHA

Verification:
- curl live URL size matches local
- grep confirms fix is in pushed file
- Screenshot of garage screen showing ESC exits

## ACCURACY REMINDER
- Read actual lines before claiming fixed
- Take screenshot BEFORE saying "done"
- If uncertain: report what you checked
```
