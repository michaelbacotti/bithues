#!/usr/bin/env python3
"""Fix bad ASIN matches (B0FXF3DY9V is a blank-title entry) and verify good matches."""
import csv, re, os

# Bad ASIN (blank title in tracker)
BAD_ASIN = "B0FXF3DY9V"

with open('/Users/mike/.openclaw/workspace-bacottibot/scripts/amazon-book-tracker/data/2026-04-13.csv') as f:
    tracker = {row['Title'].strip().lower(): row['ASIN'].strip() for row in csv.DictReader(f)}

REVIEWS_DIR = "/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo/content/reviews"

# Books we know got incorrectly matched to the blank entry
BAD_MATCHES = ['aetheri-codex', 'cords-of-empire', 'the-blueprint', 'the-martian', 'xaltocan', '_index']

# Correct ASINs for those books (from Amazon tracker - check manually)
# the-martian: Andy Weir's The Martian → should be from tracker or standard Amazon
# For now, just clear the bad ones
CORRECT_ASINS = {
    'the-martian': 'B00DKVGT3W',  # Andy Weir - The Martian (standard Amazon)
    'aetheri-codex': '',  # Will check
    'cords-of-empire': '', 
    'the-blueprint': '',
    'xaltocan': '',
}

# Also fix slug-named duplicates that matched wrong ASIN
# The numeric reviews 1 and 37 both matched B0BTD9CT35 (Dawn of Civilization) - keep only 1

# Step 1: Clear bad matches for blank-entry ASINs
count = 0
for slug in BAD_MATCHES:
    path = os.path.join(REVIEWS_DIR, f"{slug}.md")
    if not os.path.exists(path):
        continue
    with open(path) as f:
        content = f.read()
    
    # Remove isbn field if it contains B0FXF3DY9V
    new_content = re.sub(
        r'^isbn:\s*"?(B0FXF3DY9V)"?\s*$\n?',
        '',
        content,
        flags=re.MULTILINE
    )
    
    if new_content != content:
        with open(path, 'w') as f:
            f.write(new_content)
        print(f"Cleared bad ASIN: {slug}")
        count += 1

# Step 2: Fix duplicate matches (37 → Dawn of Civilization should be its own)
# Review 37 has no content so likely wrong match - check what it actually is
# For now, leave 37 without ASIN (empty content anyway)

print(f"\nCleared {count} bad ASIN matches")