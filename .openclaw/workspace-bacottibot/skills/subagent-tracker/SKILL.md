# Subagent Tracker Skill

## Purpose
Track subagent work, capture outputs, learnings, and mistakes. Make subagent sessions first-class citizens in your memory system — not fire-and-forget.

## Core Principle
**If a subagent ran, something worth remembering happened.** Capture it. Don't assume the work will be incorporated naturally — it often isn't.

---

## After Any Subagent Completes

### Step 1: Capture the Completion Record

Create a file at `memory/subagent-log/YYYY-MM-DD.md` with:

```markdown
## [HH:MM] Subagent: [brief task description]
- **Session:** [session-id]
- **Model:** [model used]
- **Runtime:** [ms]
- **Spawned by:** [parent session]

### What it was asked to do
[1-2 sentence summary of the task]

### What it delivered
[specific outputs — files created, commits, skills installed, etc.]

### Mistakes / Issues
[anything it got wrong, retried, or struggled with]

### Lessons
[anything worth remembering for next time]

### Output verified?
[YES/NO] — [where it landed — file, commit, memory, etc.]
```

### Step 2: Check Commitments
- Did it commit its work? If not, commit it yourself.
- Did it update memory? If not, do it now.
- Did it create new skills? Update the skills inventory in MEMORY.md.

### Step 3: Merge Learnings
If the subagent made a notable mistake (wrong tool, wrong format, hallucination, etc.):
- Add the lesson to `skills/self-improving-agent/.learnings/` as a per-SKILL correction
- Add to AGENTS.md if it's a pattern to avoid

---

## When Reviewing Subagent History

Before deleting old subagent sessions from NERVE, check:
1. Is the work committed to the workspace? → safe to delete transcript
2. Did it create files? → confirm they're in place and committed
3. Did it update memory? → confirm entries exist
4. Is there a lesson to extract? → extract it first

**If any of the above are uncertain, read the session transcript before deleting.**

---

## Subagent Spawn Best Practices

**Always include in the spawn prompt:**
- Explicit output destination: "commit to [file/path]" or "update [memory file]"
- Explicit quality bar: "do not return until [specific deliverable]"
- Error handling: "if [X] fails, do [Y] instead"
- Callback instruction: "report what you did in `memory/subagent-log/YYYY-MM-DD.md`"

**Model selection:**
- Quick tasks: `MiniMax-M2.7`
- Code/skills: `ollama/gemma4:26b` (confirmed working fast)
- Isolated large tasks: `isolated` sessionTarget

**Never spawn without a clear deliverable.**

---

## Maintenance

- Weekly: review `memory/subagent-log/` entries, merge patterns into `.learnings/`
- After each batch of subagents: confirm all work is committed and memory is updated
- Before NERVE cleanup: verify outputs exist in workspace before discarding session logs