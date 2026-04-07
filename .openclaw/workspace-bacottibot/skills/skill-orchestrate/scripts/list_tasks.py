#!/usr/bin/env python3
"""List tasks in the orchestration queue."""

import sys
import json
import argparse
from pathlib import Path

QUEUE_DIR = Path.home() / ".openclaw/workspace-bacottibot/.orchestration/queue"

def list_tasks(stage=None, status=None, show_all=False):
    tasks = []
    for f in sorted(QUEUE_DIR.glob("task-*.json")):
        with open(f) as fh:
            tasks.append(json.load(fh))

    if stage:
        tasks = [t for t in tasks if t.get("stage") == stage]
    if status and not show_all:
        tasks = [t for t in tasks if t.get("status") == status]
    if not show_all:
        tasks = [t for t in tasks if t.get("status") != "archived"]

    if not tasks:
        print("(no tasks match filters)")
        return

    print(f"{'ID':<12} {'Stage':<10} {'Status':<10} {'Title'}")
    print("-" * 70)
    for t in tasks:
        print(f"{t['id']:<12} {t['stage']:<10} {t['status']:<10} {t['title']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["research", "execute", "review"])
    parser.add_argument("--status", choices=["active", "blocked", "done", "archived"])
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    list_tasks(stage=args.stage, status=args.status, show_all=args.all)
