#!/usr/bin/env python3
"""Update an existing decision with outcome or status change."""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

DECISIONS_DIR = Path.home() / ".openclaw/workspace-bacottibot/.memory/decisions"

def update_decision(filename_pattern, outcome=None, status=None):
    matches = list(DECISIONS_DIR.glob(f"*{filename_pattern}*.md"))
    if not matches:
        print(f"No decision found matching '{filename_pattern}'")
        sys.exit(1)
    if len(matches) > 1:
        print(f"Multiple matches: {[m.name for m in matches]}")
        sys.exit(1)

    filepath = matches[0]
    with open(filepath) as f:
        content = f.read()

    if outcome:
        content = _update_outcome(content, outcome)
    if status:
        content = _update_status(content, status)

    with open(filepath, "w") as f:
        f.write(content)

    print(f"Updated: {filepath.name}")
    if outcome:
        print(f"  Outcome: {outcome}")
    if status:
        print(f"  Status: {status}")

def _update_outcome(content, outcome):
    import re
    pattern = r"(## Outcome \(if known\)\n)(.*?)(\n\n## |\n## Related)"
    replacement = r"\1" + outcome + r"\3"
    new_content, n = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if n == 0:
        # Try simpler replacement
        if "## Outcome (if known)" in content:
            parts = content.split("## Outcome (if known)")
            rest = parts[1]
            if "## Related" in rest:
                outcome_part, after = rest.split("## Related", 1)
                content = parts[0] + "## Outcome (if known)\n" + outcome + "\n## Related" + after
            else:
                content = parts[0] + "## Outcome (if known)\n" + outcome + "\n" + rest
    return content

def _update_status(content, status):
    content = content.replace("**Status:** decided", f"**Status:** {status}")
    content = content.replace("**Status:** superseded", f"**Status:** {status}")
    content = content.replace("**Status:** reversed", f"**Status:** {status}")
    content = content.replace("**Status:** ongoing", f"**Status:** {status}")
    return content

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="Filename or partial match for the decision")
    parser.add_argument("--outcome", "-o", default=None)
    parser.add_argument("--status", "-s", default=None, choices=["decided", "superseded", "reversed", "ongoing"])
    args = parser.parse_args()
    if not args.outcome and not args.status:
        print("Must specify --outcome and/or --status")
        sys.exit(1)
    update_decision(args.pattern, outcome=args.outcome, status=args.status)
