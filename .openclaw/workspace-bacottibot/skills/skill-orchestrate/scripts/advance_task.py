#!/usr/bin/env python3
"""Advance a task to the next stage: research -> execute -> review."""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone

QUEUE_DIR = Path.home() / ".openclaw/workspace-bacottibot/.orchestration/queue"

STAGES = ["research", "execute", "review"]

def advance_task(task_id):
    task_path = QUEUE_DIR / f"{task_id}.json"
    if not task_path.exists():
        print(f"ERROR: Task {task_id} not found in queue")
        sys.exit(1)

    with open(task_path) as f:
        task = json.load(f)

    current = task.get("stage", "research")
    if current not in STAGES:
        print(f"ERROR: Unknown stage '{current}'")
        sys.exit(1)

    idx = STAGES.index(current)
    if idx == len(STAGES) - 1:
        print(f"Task {task_id} already at final stage ({current}). Mark as done manually.")
        sys.exit(0)

    task["stage"] = STAGES[idx + 1]
    task["updated"] = datetime.now(timezone.utc).isoformat()
    task["status"] = "active"

    with open(task_path, "w") as f:
        json.dump(task, f, indent=2)

    print(f"Advanced {task_id}: {current} -> {task['stage']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: advance_task.py <task-id>")
        sys.exit(1)
    advance_task(sys.argv[1])
