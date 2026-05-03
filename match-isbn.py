#!/usr/bin/env python3
"""Build ASIN→slug mapping from Amazon tracker CSV and Hugo content titles."""
import csv
import re

# Load Amazon tracker
with open('/Users/mike/.openclaw/workspace-bacottibot/scripts/amazon-book-tracker/data/2026-04-13.csv') as f:
    tracker = {row['Title'].strip().lower(): row['ASIN'] for row in csv.DictReader(f)}

print(f"Loaded {len(tracker)} titles from Amazon tracker")
print()

# Load Hugo reviews
import os, re

REVIEWS_DIR = "/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo/content/reviews"
matches = []
unmatched = []

for filename in os.listdir(REVIEWS_DIR):
    if not filename.endswith('.md'):
        continue
    path = os.path.join(REVIEWS_DIR, filename)
    slug = filename.replace('.md', '')
    
    # Get title and author
    with open(path) as f:
        content = f.read()
    
    title_match = re.search(r'^title:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
    author_match = re.search(r'^author:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ''
    author = author_match.group(1).strip() if author_match else ''
    
    # Normalize for lookup
    lookup_key = title.strip().lower()
    
    if lookup_key in tracker:
        asin = tracker[lookup_key]
        matches.append((slug, title, asin))
        print(f"MATCH  {asin} → {slug}")
    else:
        # Try partial match on first meaningful words
        title_words = ' '.join(title.split()[:4]).lower()
        for tracker_title, asin in tracker.items():
            if title_words in tracker_title or tracker_title in title_words:
                matches.append((slug, title, asin))
                print(f"PARTIAL {asin} → {slug} (matched '{tracker_title[:50]}' to '{title[:50]}')")
                break
        else:
            unmatched.append((slug, title))

print(f"\nMatched: {len(matches)}")
print(f"Unmatched: {len(unmatched)}")
if unmatched:
    print("\nUnmatched reviews:")
    for slug, title in unmatched:
        print(f"  {slug}: {title[:60]}")