#!/usr/bin/env python3
"""Fix duplicate isbn lines - keep the one with actual value, remove empty duplicates."""
import os, re

REVIEWS_DIR = "/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo/content/reviews"
fixed = 0

for filename in sorted(os.listdir(REVIEWS_DIR)):
    if not filename.endswith('.md'):
        continue
    path = os.path.join(REVIEWS_DIR, filename)
    with open(path) as f:
        lines = f.readlines()
    
    # Find all isbn lines
    isbn_positions = [i for i, l in enumerate(lines) if l.strip().startswith('isbn:')]
    
    if len(isbn_positions) <= 1:
        continue
    
    # Find which line has the actual value
    good_isbn_line = None
    empty_isbn_lines = []
    for pos in isbn_positions:
        val = lines[pos].strip().split(':', 1)[1].strip().strip('"').strip()
        if val:
            good_isbn_line = pos
        else:
            empty_isbn_lines.append(pos)
    
    if good_isbn_line is not None and empty_isbn_lines:
        # Remove empty isbn lines that come AFTER the good one
        to_remove = [p for p in empty_isbn_lines if p > good_isbn_line]
        new_lines = [l for i, l in enumerate(lines) if i not in to_remove]
        with open(path, 'w') as f:
            f.writelines(new_lines)
        fixed += 1
        print(f"Fixed {filename}: removed {len(to_remove)} empty duplicate(s), kept isbn at line {good_isbn_line+1}")

print(f"\nFixed {fixed} files")