---
name: conversation-hygiene
description: Use when a conversation exceeds ~20 turns or ~30 minutes. Prevents memory degradation, context drift, and recall failures in long sessions. Triggers automatically on long sessions or when asked to "review conversation."
---

# conversation-hygiene

## Purpose

Long conversations cause AI memory degradation. This skill provides structured recovery and prevention.

## Trigger Conditions
- Conversation exceeds ~20 turns
- User says "review", "memory is bad", "something is wrong with you"
- Assistant notices context confusion or repeated questions

## Recovery Protocol

### Step 1: Acknowledge
Apologize briefly. Don't defend or explain. Just acknowledge.

### Step 2: Read Memory Files
In this order:
1. `MEMORY.md` — long-term curated facts
2. `memory/YYYY-MM-DD.md` — today's session notes
3. Any relevant topic file (e.g., `memory/websites.md` if discussing sites)

### Step 3: Rebuild Context
Write a fresh session summary to `memory/YYYY-MM-DD.md` capturing:
- What the user wanted (goal)
- What's done (completed)
- What's pending (next action)
- Key decisions made today
- What NOT to repeat

### Step 4: Commit
```bash
cd ~/.openclaw/workspace-bacottibot
git add memory/YYYY-MM-DD.md MEMORY.md
git commit -m "Session recovery: YYYY-MM-DD"
git push origin main 2>/dev/null || true
```

### Step 5: Tell the User
What was updated, what's still pending, and ask if they want to continue or pivot.

---

## Prevention Rules (for sessions > 10 turns)

1. **Write to memory as things happen** — don't batch at end of session
2. **If confused, say so immediately** — don't guess
3. **Summarize every 15 minutes** — brief mental checkpoint, push if possible
4. **When starting a new topic, read relevant memory first**
5. **Keep topic files current** — websites.md, entities.md, investing.md

---

## Session Summary Template

```markdown
## Session: YYYY-MM-DD HH:MM-HH:MM EDT

### Goal
[What Mike wanted to accomplish]

### Completed
- [x] task 1
- [x] task 2

### In Progress
- [ ] task that's mid-flight

### Pending (carry forward)
- [ ] next action item

### Key Decisions
- Decision 1 → why
- Decision 2 → why

### Mistakes Made
- Mistake 1 (so I don't repeat it)
- Mistake 2

### For Next Session
- [ ] follow-up item
```

---

## When to Escalate

If a sub-task has failed 3+ times, write it to memory as "blocked" and tell Mike. Don't keep retrying the same approach.
