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
| 1–5 files | One subagent |
| 6–15 files | One subagent (10 is the safe max for GitHub API read-modify-push cycles) |
| 16–30 files | Two subagents in parallel, each doing 8-15 files |
| 31–60 files | Three subagents sequentially, ~15-20 files each |
| 60+ files | Sequential batches of 10 pages — NEVER more than 10 pages per subagent |
| Visual rewrite | Do NOT run as subagent — token-heavy, OOM risk. Do in main session |
| Any task requiring reading PDFs | Limit to 2 PDFs max per subagent |

**Hard rule: 10 pages per subagent maximum for GitHub API batch operations.**

Reason: A GitHub read-modify-push cycle takes ~2-5 seconds per file. At 10 files that's 20-50 seconds of pure API time, plus thinking time, plus push time. A subagent with a 5-minute timeout needs 80%+ of its time for actual work, not waiting on I/O. 10 files is the safe ceiling.

For simple read-only audits (word count, link check), 20-25 pages is fine. For read-modify-push, cap at 10.

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
1. Check git history or live files to see if it delivered any work
2. If partial work: re-spawn with EXACTLY the remaining files (not the full batch)
3. If no work delivered: re-spawn the same batch (may have been a capacity fluke)
4. If a subagent consistently times out on the same batch: take that specific task into the main session
5. NEVER claim the task is done if the subagent timed out before completing
6. NEVER do the work yourself unless it's a trivial one-off (e.g., adding one meta tag, fixing one link)

**The delegation contract:** If you spawn a subagent, you must see it through to completion or explicit failure. If it times out, you re-spawn with remaining scope. The buck stops with delegation, not with you doing the work.

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

## Website Subagent Additions

For any website task subagent, always include:

```
WEBSITE RULES (in addition to Scope Formula above):
- Read the homepage BEFORE touching any page — nav, footer, hero, card styles, shared CSS
- Run `curl -s -o /dev/null -w "%{http_code}"` on any URL you create or怀疑 is broken
- Check sitemap for any new stale entries after your changes
- If you delete a file: verify canonical tag exists and target is live before deleting
- If you create a new page: add it to sitemap.xml and link from at least one parent page
- Compare your output to the homepage for: nav structure, footer, hero section, card class, typography
- Report: files changed, links checked, style consistency status, any remaining issues
```

### Website Task Scope Sizes

| Task | Recommended |
|------|-------------|
| Fix 1–5 broken links | One subagent, direct link checks |
| Update nav/dropdown on N pages | One subagent, batch by template |
| Add section to homepage | One subagent, main session for style comparison |
| Rebuild a corrupted page | Main session preferred (subagent only after shell verified) |
| Bulk style alignment (50+ pages) | Sequential subagents by directory, push between batches |
| Any visual redesign | Main session only — never subagent for visual work |

## Spawn Syntax Reference

```javascript
sessions_spawn(
  mode="run",           // one-shot, announces result
  runtime="subagent",   // OpenClaw subagent
  task="[full prompt]"   // include goal/scope/steps/verification/rules
)
```
