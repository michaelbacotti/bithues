---
name: pre-flight-check
description: MANDATORY before claiming any fix, push, or task is "done." Read the actual changed lines. Verify the code. Take a screenshot. This is not optional — it is the final gate before completion.
---

# pre-flight-check

## The Rule

**Before saying "done," "fixed," or "pushed" — you MUST verify the actual code.**

This skill exists because of a recurring failure pattern: asserting something is correct without reading the code, then discovering it wasn't. Mike's explicit instruction: *slow and careful quality over speed.* Truth and accuracy are non-negotiable.

---

## The Pre-Flight Checklist

Before any completion claim, run through this mentally:

- [ ] **Read the actual changed lines** — not "my mental model of the change" but the real file content
- [ ] **Verify the specific fix is in the file** — grep or read the exact line numbers
- [ ] **File size changed?** — `wc -c` local vs live to confirm the push landed
- [ ] **GitHub SHA verified** — fetch SHA before push, confirm 200 response after
- [ ] **Screenshot before claiming success** — open in browser, confirm visually
- [ ] **Mike's browser** — if he reported the bug, his report is ground truth. Take his word over your headless browser.

---

## Common Traps

### Trap 1: "The subagent said it's fixed"
**Wrong response:** "Great, it's fixed!"
**Right response:** Read the result. Check the code. Verify the specific line.

### Trap 2: "My headless browser shows it works"
**Wrong response:** "It works fine, must be your browser."
**Right response:** Your headless browser is one data point. Mike's browser is another. If they disagree, investigate before arguing.

### Trap 3: "The fix was simple, I don't need to verify"
**Wrong response:** "I know what I changed, no need to check."
**Right response:** The most embarrassing bugs are from trivial typos. Read the line.

### Trap 4: Pushing without SHA
**Wrong response:** "Pushed!" (later fails with 422)
**Right response:** Always fetch SHA first. Always.

### Trap 5: Subagent timed out mid-task
**Wrong response:** "The subagent completed" (it didn't)
**Right response:** If it timed out, it delivered nothing usable. Check the result — if it's partial or empty, either fix it yourself or spawn a new subagent with tighter scope. Do NOT tell Mike "it's done" if the subagent didn't reach its verification step.

---

## GitHub Push Verification Sequence

```bash
# 1. Before push: fetch SHA
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/{owner}/{repo}/contents/{path}" > /tmp/gh-file.json
sha=$(python3 -c "import json; print(json.load(open('/tmp/gh-file.json'))['sha'])")

# 2. Push with SHA
# PUT with sha field...

# 3. After push: verify
curl -s "https://www.bithues.com/{path}" | wc -c  # confirm live size matches local
git fetch origin && git log --oneline -1  # confirm commit landed
```

---

## "I'm Not Sure" is Always Acceptable

If you're uncertain whether the fix is correct:
- Say "I need to re-check the file" — then check it
- Say "I'm not confident this is right" — then re-verify
- Say "I should read that line before claiming" — then read it

These are not weaknesses. They are how accurate work gets done.

Mike would rather hear "I need to verify that" ten times than be told once that something was fixed when it wasn't.

---

## After Reading — Update Your Memory

If you discover something was wrong (a bug you missed, a claim you made that was incorrect, an assumption that turned out to be wrong):
- Write it to `memory/YYYY-MM-DD.md` immediately
- Note what the correct answer actually was
- This prevents the same error from being repeated in future sessions
