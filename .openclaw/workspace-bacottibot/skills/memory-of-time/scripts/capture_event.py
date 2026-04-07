#!/usr/bin/env python3
"""Capture a time-stamped event for memory-of-time skill."""

import sys
import uuid
import argparse
from pathlib import Path
from datetime import datetime, timezone

EVENTS_DIR = Path.home() / ".openclaw/workspace-bacottibot/.memory/events"
EVENTS_DIR.mkdir(parents=True, exist_ok=True)

VALID_TYPES = [
    "model_change", "skill_added", "skill_modified", "decision",
    "preference_change", "system_change", "workflow_change",
    "external_event", "milestone"
]

def capture_event(event_type, title, detail="", tags=None):
    if event_type not in VALID_TYPES:
        print(f"WARNING: Unknown event type '{event_type}'. Valid types: {', '.join(VALID_TYPES)}")

    tags = tags or []
    event_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now(timezone.utc).isoformat()

    filename = f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{event_id}.md"
    filepath = EVENTS_DIR / filename

    content = f"""---
id: {event_id}
timestamp: {timestamp}
type: {event_type}
tags: [{', '.join(tags)}]
---

# {title}

{detail}
""" if detail else f"""---
id: {event_id}
timestamp: {timestamp}
type: {event_type}
tags: [{', '.join(tags)}]
---

# {title}

"""
    with open(filepath, "w") as f:
        f.write(content)

    print(f"Captured event: {filepath.name}")
    print(f"  Type: {event_type}")
    print(f"  Title: {title}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture a time-stamped event")
    parser.add_argument("type", help=f"Event type. Valid: {', '.join(VALID_TYPES)}")
    parser.add_argument("title", help="Event title")
    parser.add_argument("--detail", "-d", default="", help="Detailed description")
    parser.add_argument("--tags", "-t", default="", help="Comma-separated tags")
    args = parser.parse_args()

    tag_list = [t.strip() for t in args.tags.split(",") if t.strip()]
    capture_event(args.type, args.title, args.detail, tag_list)
