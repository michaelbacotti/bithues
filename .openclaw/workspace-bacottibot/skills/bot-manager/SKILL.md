# SKILL.md — bot-manager

## What it does
Manages and orchestrates sub-agent bots: spawning, monitoring, steering, and killing background sessions.

## When to use
- Spawning sub-agents for long-running or isolated tasks
- Monitoring active bot sessions
- Steering or redirecting running bots
- Killing stuck or completed bots

## When NOT to use
- Simple tasks that can be done directly in main session
- When real-time interaction is needed throughout the task
- Tasks requiring main session context continuity

## Inputs
- `sessions_spawn` with task description and label
- `sessions_list` to view active sessions
- `sessions_history` to read bot outputs

## Outputs
- New bot sessions with independent context
- Bot steering messages and kill commands

## Cost / Risk notes
No external calls. Uses OpenClaw session management tools only.
