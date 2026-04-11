---
name: claims-tracker
description: Use at the start of any complex task. Creates a claims log, tracks every specific claim made during the task, and verifies each one before declaring done. Prevents hallucination and overclaiming.
---

# claims-tracker

## When to Use

Start a claims log when:
- A task has more than 3 steps
- Any claim about code, files, or facts is being made
- Mike is expecting specific outcomes (a fix, a push, a visual change)
- You're about to do something you haven't done before in this session

**Simple lookups or one-liners: skip this.** The overhead isn't worth it.

---

## The Pattern

### Phase 1: Create the Log (at task start)

```bash
# Create memory/claims-YYYY-MM-DD.md
```

Content:

```markdown
# Claims Log — YYYY-MM-DD

## Task: [one sentence description]

## Claims Made

| # | Claim | Status | Verified |
|---|-------|--------|----------|
| 1 |       | PENDING |          |
| 2 |       | PENDING |          |

## Verification Checklist
- [ ]

## Notes
```

### Phase 2: Log Each Claim (as you go)

When you make a claim — write it to the log immediately:

> "I've fixed the ESC key bug"

→ Log it: `| 1 | Fixed ESC key in handleKeyDown | PENDING | |`

> "The file is 73,957 bytes on GitHub"

→ Log it: `| 2 | Live file size: 73,957 bytes | PENDING | |`

**Rule: If it's not in the log, it's not claimed yet. If it is in the log, it must be verified.**

### Phase 3: Verify Before Done (at task end)

For each PENDING claim:
- Read the actual line / check the actual file
- Mark VERIFIED or WRONG
- If WRONG: fix it before reporting done

**Never tell Mike "it's done" until all claims are verified.**

### Phase 4: Summary to Mike

```markdown
## Done. Claims verified:
- ✅ Fixed ESC key (line 247 → confirmed)
- ✅ File size 73,957 bytes (curl confirmed)
- ✅ Garage state check ordered before WALKING (grep confirmed)

## 1 claim NOT verified (will fix):
- Visual: green world background — still needs second pass
```

---

## Log Format Reference

```markdown
# Claims Log — 2026-04-11

## Task: Fix AutoDuel garage ESC key and start-on-foot spawn

## Claims Made

| # | Claim | Status | Verified |
|---|-------|--------|----------|
| 1 | ESC exits garage (line ~247) | VERIFIED | grep + screenshot |
| 2 | checkTownEntry spawn Y = TWN_H + 100 | VERIFIED | grep line 1037 |
| 3 | Live file 73,957 bytes | VERIFIED | curl wc -c |
| 4 | Game starts on foot in Barren Rock | PENDING | needs Mike's browser |

## Verification Checklist
- [x] Read actual lines (not mental model)
- [x] curl live URL size matches local
- [x] grep confirms fix in pushed file
- [ ] Screenshot of actual browser (Mike's report)

## Notes
- SHA: abc1234
- Mike's browser showed black screen — investigate further
```

---

## Hard Rules

1. **If a claim isn't in the log, don't treat it as done**
2. **If a claim is in the log, verify it before marking done**
3. **WRONG is an acceptable status** — just fix it and update
4. **PENDING is not DONE** — don't report PENDING as success to Mike
5. **Write claims as you go, not at the end** — end-of-task logging is too late

## Anti-Pattern: The Claim Inflation Problem

Don't pad the log with obvious things:
- ❌ "User wants game to work"
- ❌ "Code is in index.html"
- ❌ "GitHub Pages hosts static files"

Only log claims that are:
- Specific outcomes (fixed X, file is Y bytes, line Z contains W)
- Testable/verifiable (can confirm or deny)
- Non-obvious (things you might forget or misremember later)

## Integration with pre-flight-check

The claims log is the *before* — pre-flight-check is the *after gate*. Use both:
- claims-tracker: write claims as you work
- pre-flight-check: verify before claiming done
