#!/usr/bin/env python3
"""Query decisions by keyword."""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

DECISIONS_DIR = Path.home() / ".openclaw/workspace-bacottibot/.memory/decisions"

def query_decisions(query, days=365, limit=5):
    query_lower = query.lower()
    results = []

    for f in sorted(DECISIONS_DIR.glob("*.md"), reverse=True):
        with open(f) as fh:
            content = fh.read()
        ts_str = ""
        for line in content.splitlines():
            if line.startswith("**Date:**"):
                ts_str = line.split("**Date:**")[1].strip()
                break
        if ts_str:
            try:
                ts = datetime.strptime(ts_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except Exception:
                ts = datetime.min
            if ts < datetime.now(timezone.utc) - timedelta(days=days):
                continue
        if query_lower in content.lower():
            results.append((f, content, ts_str))

    if not results:
        print(f"No decisions found matching '{query}'")
        return

    print(f"Decisions matching '{query}':\n")
    for f, content, ts in results[:limit]:
        title = ""
        for line in content.splitlines():
            if line.startswith("# Decision:"):
                title = line.replace("# Decision:", "").strip()
                break
        rationale = ""
        in_rat = False
        for line in content.splitlines():
            if line.startswith("## Rationale"):
                in_rat = True
                continue
            if in_rat and line.startswith("##"):
                in_rat = False
            if in_rat:
                rationale += line + " "
        rationale = rationale.strip()[:200]
        print(f"--- {f.name} ({ts}) ---")
        print(f"Title: {title}")
        print(f"Rationale: {rationale}...")
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Search phrase")
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    query_decisions(args.query, days=args.days, limit=args.limit)
