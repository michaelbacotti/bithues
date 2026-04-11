# Gemma Skill Creation — 2026-04-09

## What Worked

- **Short, directive SKILL.md** — Gemma (26b) benefits from concise, action-oriented instructions rather than long explanations. No fluff, just "do this, then this."
- **Task completion template** — Subagents (especially smaller models) tend to trail off or keep going after they're done. A template forces a clear stop.
- **Concrete tool guidance** — Specifying `read` vs `web_fetch` vs `browser` helps a model that might otherwise pick the wrong tool or use it incorrectly.
- **Git safety rules front-loaded** — The workspace IS the bithues git repo. Forgetting to fetch before push has caused repo wipes before. Putting it in the skill's core instructions makes it harder to miss.
- **Local-only files marked explicitly** — HOUSE Inc tracker data is sensitive. Explicitly calling out "LOCAL ONLY — never push" with specific file paths is clearer than a generic "be careful with sensitive data."
- **Referencing other skills** — Rather than duplicating the house-board-comm or applicant-due-diligence workflow, pointing to them keeps the skill lean and accurate.

## What Didn't Work (Lessons from Other Skills)

- **Verbose skills get ignored** — Skills longer than ~100 lines of actual content tend to get skimmed or partially followed by subagents. Keep it tight.
- **Workflows should be in the skill, not just references** — Reference files are fine for data, but procedural steps belong in SKILL.md so Gemma reads them without extra prompting.
- **Don't assume model knows workspace layout** — Smaller models (even 26b) benefit from explicit paths like `~/.openclaw/workspace-bacottibot/SOUL.md` rather than "read SOUL.md" (which might not resolve correctly in a subagent context).

## Key Insight for Ollama Subagents

Ollama models like Gemma don't have the same ambient context awareness as cloud models. They need:
1. Explicit workspace path on every file read
2. Clear task scope and stop conditions
3. Explicit safety guardrails (not just "be careful")
4. File-path-level specificity for sensitive operations

## Status
✅ Created `/Users/mike/.openclaw/workspace-bacottibot/skills/gemma-assistant/SKILL.md`
