#!/usr/bin/env python3
"""Create a new task in the orchestration queue."""

import sys
import json
import os
from pathlib import Path
from datetime import datetime, timezone

QUEUE_DIR = Path.home() / ".openclaw/workspace-bacottibot/.orchestration/queue"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

def next_task_id():
    existing = list(QUEUE_DIR.glob("task-*.json"))
    if not existing:
        return 1
    nums = []
    for f in existing:
        try:
            nums.append(int(f.stem.split("-")[1]))
        except (IndexError, ValueError):
            pass
    return max(nums) + 1 if nums else 1

def create_task(title, notes=""):
    task_id = next_task_id()
    now = datetime.now(timezone.utc).isoformat()
    task = {
        "id": f"task-{task_id:03d}",
        "title": title,
        "created": now,
        "updated": now,
        "stage": "research",
        "status": "active",
        "research_output": "",
        "execute_output": "",
        "review_output": "",
        "notes": notes
    }
    path = QUEUE_DIR / f"task-{task_id:03d}.json"
    with open(path, "w") as f:
        json.dump(task, f, indent=2)
    print(f"Created: {path.name}")
    print(f"  Title: {title}")
    print(f"  Stage: research")
    print(f"  Status: active")
    return task

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: create_task.py <title> [notes]")
        sys.exit(1)
    title = sys.argv[1]
    notes = sys.argv[2] if len(sys.argv) > 2 else ""
    create_task(title, notes)
