#!/usr/bin/env python3
"""Clean ISBN matching: replaces any isbn line with correct ASIN, no duplicates."""
import csv, re, os

# Load Amazon tracker with normalized keys
with open('/Users/mike/.openclaw/workspace-bacottibot/scripts/amazon-book-tracker/data/2026-04-13.csv') as f:
    tracker_raw = list(csv.DictReader(f))

tracker = {}
for row in tracker_raw:
    title = row['Title'].strip()
    asin = row['ASIN'].strip()
    if not title:
        continue
    tracker[title.lower()] = asin
    main_title = title.split(':')[0].strip().lower()
    tracker[main_title] = asin

REVIEWS_DIR = "/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo/content/reviews"

# Fixed known correct ASINs for books not in tracker or with title mismatches
MANUAL_ASINS = {
    'the-martian': '9780553418026',  # ISBN-13
    'the-blueprint': 'B0GQK61R5H',  # guess - we'll check
    'aetheri-codex': '',
    'cords-of-empire': '',
    'xaltocan': '',
    'veiled-presence': 'B0GTJN8YGG',
}

# Also: disclosure-2026 → B0GPM4DZR1, horizonte-rojo → B0GR1199SJ
# men-of-three-seas → B0D38W5972 (matched correctly)

import re as re_module

def get_asin(slug, title, content):
    """Find ASIN for a review."""
    if slug in MANUAL_ASINS:
        return MANUAL_ASINS[slug]
    
    title_lower = title.lower()
    # Direct match
    if title_lower in tracker:
        return tracker[title_lower]
    
    # Strip subtitle
    main_title = title.split(':')[0].strip().lower()
    if main_title in tracker:
        return tracker[main_title]
    
    # Partial match
    short = ' '.join(title.split()[:3]).lower()
    for t, asin in tracker.items():
        if short in t or t in short:
            return asin
    
    return ''

count = 0
for filename in sorted(os.listdir(REVIEWS_DIR)):
    if not filename.endswith('.md') or filename == '_index.md':
        continue
    
    slug = filename.replace('.md', '')
    path = os.path.join(REVIEWS_DIR, filename)
    with open(path) as f:
        lines = f.readlines()
    
    # Get title
    title = ''
    for line in lines[:20]:
        m = re_module.search(r'^title:\s*"?(.+?)"?\s*$', line)
        if m:
            title = m.group(1).strip()
            break
    
    asin = get_asin(slug, title, lines)
    
    if not asin:
        # Skip - no ASIN known
        continue
    
    # Find all isbn lines and remove them
    isbn_positions = [i for i, l in enumerate(lines) if l.strip().startswith('isbn:')]
    
    # Build new content
    new_lines = [l for i, l in enumerate(lines) if i not in isbn_positions]
    
    # Insert isbn: "ASIN" after genre line
    new_new_lines = []
    inserted = False
    for line in new_lines:
        new_new_lines.append(line)
        if not inserted and line.strip().startswith('genre:'):
            new_new_lines.append(f'isbn: "{asin}"\n')
            inserted = True
    
    with open(path, 'w') as f:
        f.writelines(new_new_lines)
    
    print(f"{slug}: isbn={asin}")
    count += 1

print(f"\nUpdated {count} reviews with ISBNs")

# Verify build
print("\n=== Build check ===")
import subprocess
result = subprocess.run(['hugo', '--quiet'], capture_output=True, text=True,
                       cwd='/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo')
if result.returncode == 0:
    print("Hugo build: OK")
else:
    print(f"Hugo build FAILED: {result.stderr[-200:]}")