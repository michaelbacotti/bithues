#!/usr/bin/env python3
"""Record a new decision in the decision tracker."""

import sys
import argparse
import uuid
import re
from pathlib import Path
from datetime import datetime, timezone

DECISIONS_DIR = Path.home() / ".openclaw/workspace-bacottibot/.memory/decisions"
DECISIONS_DIR.mkdir(parents=True, exist_ok=True)

def slugify(text):
    s = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    s = s.lower().replace(' ', '-')[:50]
    return s

def record_decision(title, decided_date, alternatives, rationale, outcome="", tags=None, decided_by="main-agent"):
    decision_id = str(uuid.uuid4())[:8]
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = f"{decided_date}-{slugify(title)}.md"
    filepath = DECISIONS_DIR / filename

    tags = tags or []
    tag_block = " ".join(f"`#{t}`" for t in tags) if tags else ""

    alternatives_block = ""
    if alternatives:
        for alt in alternatives:
            alternatives_block += f"- **{alt.get('name', 'Option')}**: {alt.get('note', '')}\n"

    content = f"""# Decision: {title}

**Date:** {decided_date}
**Status:** decided
**Decided by:** {decided_by}
{tag_block}

## What was decided
{title}

## Alternatives considered
{alternatives_block or "*None recorded*"}

## Rationale
{rationale}

## Outcome (if known)
{outcome or "*Not yet evaluated*"}

## Related decisions
_(None yet)_

## Tags
{tags}
"""
    with open(filepath, "w") as f:
        f.write(content)

    print(f"Recorded decision: {filepath.name}")
    print(f"  Title: {title}")
    print(f"  Date: {decided_date}")
    return filepath

def parse_alts(alt_str):
    """Parse pipe-separated alternatives string into list of dicts."""
    if not alt_str:
        return []
    result = []
    for i, alt in enumerate(alt_str.split("|")):
        name, _, note = alt.partition(":")
        result.append({"name": name.strip() or f"Option {i+1}", "note": note.strip()})
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record a decision")
    parser.add_argument("--title", "-t", required=True)
    parser.add_argument("--decided", "-d", required=True, help="YYYY-MM-DD")
    parser.add_argument("--alternatives", "-a", default="", help="Pipe-separated: OptA:reason|OptB:reason")
    parser.add_argument("--rationale", "-r", required=True)
    parser.add_argument("--outcome", "-o", default="")
    parser.add_argument("--tags", default="", help="Comma-separated")
    parser.add_argument("--decided-by", default="main-agent")
    args = parser.parse_args()

    tag_list = [t.strip() for t in args.tags.split(",") if t.strip()]
    alts = parse_alts(args.alternatives)
    record_decision(args.title, args.decided, alts, args.rationale, args.outcome, tag_list, args.decided_by)
