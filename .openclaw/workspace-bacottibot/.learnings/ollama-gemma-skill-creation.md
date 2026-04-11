# Skill Creation for Ollama/gemma4 Subagents

## What Happened

Gemma subagent (gemma4:26b via Ollama) was tasked with creating a SKILL.md for itself. It timed out at 2m22s, outputting only "Now I have what I need. Let me create the skill." before the session ended.

The skill directory was created but empty — Gemma didn't complete the task.

## Why It Likely Failed

1. **gemma4:26b context window limits** — The skill-creator SKILL.md is ~300 lines. Loading it + the Gemma task prompt + workspace context may have exceeded capacity or caused confusion about what to output.

2. **No bundled resources needed** — The Gemma skill is mostly text-based guidance (high-freedom instructions). No scripts/assets needed, so the skill stays lean.

3. **Ollama models drift more** — gemma4:26b is a smaller model than hosted frontier models. Longer multi-step tasks with many files to read increase drift risk.

## What I Did Instead

Created the SKILL.md manually in about 5 minutes. Key decisions:
- Kept it short (~100 lines) — lean enough for a smaller model
- Focused on: core loop, staying on task, workspace files, git workflow, HOUSE Inc rules
- No scripts or references — not needed for this skill

## Lessons for Future Ollama Skill Creation

1. **Keep Ollama skills SHORT** — smaller models have less context tolerance. ~100-150 lines max in SKILL.md body.

2. **Don't spawn Ollama subagents to build skills** — they time out more than hosted models. Build skills directly or use a faster subagent (MiniMax, Gemini) to create the file, then let Ollama subagent use it.

3. **One-shot tasks work better for Ollama** — skill creation is multi-step (read SKILL.md → plan → create files → verify). Break it into simpler one-shot tasks or do it directly.

4. **Gemma skill works fine for Gemma** — once the SKILL.md exists, Gemma can use it. The issue was creating it, not using it.

5. **For complex skills on Ollama** — consider having a hosted model create the skill first, then validate and hand off to Ollama subagent.

## Files Created

- `/Users/mike/.openclaw/workspace-bacottibot/skills/gemma-assistant/SKILL.md` — skill for Gemma

_Learned: 2026-04-09_