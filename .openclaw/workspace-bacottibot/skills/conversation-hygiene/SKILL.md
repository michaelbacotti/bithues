---
name: conversation-hygiene
description: Use when a conversation exceeds ~20 turns or ~30 minutes. Prevents memory degradation, context drift, and recall failures in long sessions. Triggers automatically on long sessions or when asked to "review conversation."
---

# conversation-hygiene

## Purpose

Long conversations cause AI memory degradation, context drift, and tool failures. This skill provides structured recovery and prevention.

## Trigger Conditions
- Conversation exceeds ~20 turns
- User says "review", "memory is bad", "something is wrong with you"
- Assistant notices context confusion or repeated questions
- Any tool failure that looks like a session issue (not responding, stuck, confused)

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

## Critical Rule: Do Work via Subagents

**When to spawn a subagent instead of doing the work directly:**

| Task Type | Use Subagent? |
|-----------|--------------|
| Web research / fetching | ✅ Yes |
| GitHub API operations (PUT/GET) | ✅ Yes |
| File editing / creating | ✅ Yes |
| Anything requiring multiple tool calls | ✅ Yes |
| Long-running tasks (>30s) | ✅ Yes |
| Quick status checks (1 tool call) | ❌ No |
| One-liner questions | ❌ No |

**Why this matters:** Doing work directly in the main session:
- Blocks the conversation (Mike can't chat while work is happening)
- Uses main session tokens for work instead of conversation
- If main session has issues, the work fails AND conversation stops
- Subagents fail safely — main session continues

**How to decide:** If Mike asks you to "update the website" or "check something" or "investigate X" → spawn a subagent. If it would take more than 2 tool calls, it should be a subagent.

**Anti-pattern (what we did wrong this morning):**
- Mike asked for market forecast → did web research directly, then tried to update the page directly
- Should have been: spawn subagent immediately for ALL of it

---

## Prevention Rules (for sessions > 10 turns)

1. **Write to memory as things happen** — don't batch at end of session
2. **If confused, say so immediately** — don't guess
3. **Summarize every 15 minutes** — brief mental checkpoint, push if possible
4. **When starting a new topic, read relevant memory first**
5. **Keep topic files current** — websites.md, entities.md, investing.md
6. **Spawn subagents for ALL substantive tasks** — never block the main session with work

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

If the main session stops responding:
1. Mike can delete subagents: `subagents list` then kill stuck ones
2. Mike can delete cron jobs that might be interfering
3. Restarting the gateway: `openclaw gateway restart`
4. After any fix, write checkpoint to memory before continuing
