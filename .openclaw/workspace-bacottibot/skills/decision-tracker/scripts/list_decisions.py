#!/usr/bin/env python3
"""List decisions, optionally filtered."""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
import re

DECISIONS_DIR = Path.home() / ".openclaw/workspace-bacottibot/.memory/decisions"

def list_decisions(days=None, tag=None, status=None):
    results = []

    for f in sorted(DECISIONS_DIR.glob("*.md"), reverse=True):
        with open(f) as fh:
            content = fh.read()

        ts_str = ""
        status_val = "decided"
        tags_val = ""
        title = f.name

        for line in content.splitlines():
            if line.startswith("**Date:**"):
                ts_str = line.split("**Date:**")[1].strip()
            elif line.startswith("**Status:**"):
                status_val = line.split("**Status:**")[1].strip().lower()
            elif line.startswith("## Tags") or line.startswith("**Tags**"):
                tags_val = content.split(line)[1].split("##")[0].strip()
            if line.startswith("# Decision:"):
                title = line.replace("# Decision:", "").strip()

        if tag and tag.lower() not in tags_val.lower():
            continue
        if status and status.lower() != status_val:
            continue
        if days:
            try:
                ts = datetime.strptime(ts_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if ts < datetime.now(timezone.utc) - timedelta(days=days):
                    continue
            except Exception:
                pass

        results.append((f.name, title, ts_str, status_val))

    if not results:
        print("(no decisions match filters)")
        return

    print(f"{'Filename':<40} {'Date':<12} {'Status':<12} {'Title'}")
    print("-" * 90)
    for name, title, ts, status_val in results:
        print(f"{name:<40} {ts:<12} {status_val:<12} {title}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=None)
    parser.add_argument("--tag", default=None)
    parser.add_argument("--status", default=None, choices=["decided", "superseded", "reversed", "ongoing"])
    args = parser.parse_args()
    list_decisions(days=args.days, tag=args.tag, status=args.status)
