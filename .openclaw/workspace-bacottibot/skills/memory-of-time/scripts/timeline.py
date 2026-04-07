#!/usr/bin/env python3
"""Show a timeline of events from memory-of-time."""

import sys
import argparse
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta

EVENTS_DIR = Path.home() / ".openclaw/workspace-bacottibot/.memory/events"

def parse_frontmatter(content):
    fm = {}
    body_lines = []
    in_fm = False
    for line in content.splitlines():
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                in_fm = False
                continue
        if in_fm:
            if ":" in line:
                key, _, val = line.partition(":")
                fm[key.strip()] = val.strip()
        else:
            body_lines.append(line)
    fm["_body"] = "\n".join(body_lines).strip()
    return fm

def timeline(days=7, event_type=None, tag=None):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    events = []

    for f in sorted(EVENTS_DIR.glob("*.md"), reverse=True):
        with open(f) as fh:
            content = fh.read()
        fm = parse_frontmatter(content)
        ts_str = fm.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except Exception:
            continue
        if ts < cutoff:
            continue
        if event_type and fm.get("type") != event_type:
            continue
        if tag and tag not in fm.get("tags", ""):
            continue
        events.append((f, fm, ts))

    if not events:
        print(f"(no events in the last {days} day(s))")
        return

    print(f"Timeline — last {days} day(s)")
    print("=" * 60)
    for f, fm, ts in events:
        date_str = ts.strftime("%Y-%m-%d %H:%M")
        etype = fm.get("type", "?")
        body = fm.get("_body", "").split("\n")[0].strip()
        if body.startswith("#"):
            body = body.lstrip("# ").strip()
        print(f"[{date_str}] ({etype}) {body}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", "-n", type=int, default=7)
    parser.add_argument("--type", "-t", default=None)
    parser.add_argument("--tag", "-g", default=None)
    args = parser.parse_args()
    timeline(days=args.days, event_type=args.type, tag=args.tag)
