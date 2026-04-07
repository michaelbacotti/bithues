#!/usr/bin/env python3
"""Query memory-of-time events by keyword or phrase."""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

EVENTS_DIR = Path.home() / ".openclaw/workspace-bacottibot/.memory/events"

def parse_frontmatter(content):
    fm = {}
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
    return fm

def query_events(query, days=30, limit=10):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    results = []

    query_lower = query.lower()
    for f in sorted(EVENTS_DIR.glob("*.md"), reverse=True):
        with open(f) as fh:
            content = fh.read()
        fm = parse_frontmatter(content)
        ts_str = fm.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except Exception:
            ts = datetime.min
        if ts < cutoff:
            continue
        if query_lower in content.lower():
            results.append((f, fm, ts, content))

    if not results:
        print(f"No events found matching '{query}' in last {days} days")
        return

    print(f"Found {len(results)} event(s) matching '{query}':\n")
    for f, fm, ts, content in results[:limit]:
        print(f"--- {f.name} ({ts.strftime('%Y-%m-%d %H:%M')}) ---")
        body_lines = [l for l in content.splitlines() if not l.startswith("---") and not l.startswith("id:") and not l.startswith("timestamp:") and not l.startswith("type:") and not l.startswith("tags:")]
        print("\n".join(body_lines).strip()[:300])
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Search phrase")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    query_events(args.query, days=args.days, limit=args.limit)
