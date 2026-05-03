#!/usr/bin/env python3
"""Build ASIN map from Amazon tracker CSV and update Hugo review frontmatter."""
import csv, re, os

# Load Amazon tracker with normalized keys
with open('/Users/mike/.openclaw/workspace-bacottibot/scripts/amazon-book-tracker/data/2026-04-13.csv') as f:
    tracker_raw = list(csv.DictReader(f))

# Build a map of (title_lower -> ASIN) handling "Book Title : Subtitle" → "Book Title"
tracker = {}
for row in tracker_raw:
    title = row['Title'].strip()
    asin = row['ASIN'].strip()
    tracker[title.lower()] = asin
    # Also strip subtitle for matching
    main_title = title.split(':')[0].strip().lower()
    tracker[main_title] = asin

print(f"Loaded {len(tracker)} titles")

REVIEWS_DIR = "/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo/content/reviews"

# Known Amazon cover URL pattern for ASIN
# We'll store ASIN as isbn field (abusing isbn field for Amazon covers)
ASIN_MAP = {}
unmatched = []

for filename in sorted(os.listdir(REVIEWS_DIR)):
    if not filename.endswith('.md'):
        continue
    path = os.path.join(REVIEWS_DIR, filename)
    slug = filename.replace('.md', '')
    
    with open(path) as f:
        content = f.read()
    
    title_match = re.search(r'^title:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ''
    
    # Already has ASIN?
    if re.search(r'^isbn:\s*"B0', content, re.MULTILINE):
        asin_match = re.search(r'^isbn:\s*"?(B0\w+)"?\s*$', content, re.MULTILINE)
        if asin_match:
            ASIN_MAP[slug] = asin_match.group(1)
            continue
    
    lookup_keys = [title.lower()]
    if ':' in title:
        lookup_keys.append(title.split(':')[0].strip().lower())
    
    found = False
    for key in lookup_keys:
        if key in tracker:
            ASIN_MAP[slug] = tracker[key]
            print(f"✓ {slug} ({title[:40]}) → {tracker[key]}")
            found = True
            break
    
    if not found:
        # Try partial match
        short_title = ' '.join(title.split()[:3]).lower()
        for t, asin in tracker.items():
            if short_title in t or t in short_title:
                ASIN_MAP[slug] = asin
                print(f"≈ {slug} ({title[:40]}) → {asin} (partial: '{t[:40]}')")
                found = True
                break
        if not found:
            unmatched.append((slug, title))

print(f"\nMatched: {len(ASIN_MAP)}")
print(f"Unmatched: {len(unmatched)}")
for slug, title in sorted(unmatched):
    print(f"  ✗ {slug}: {title[:60]}")

# Now write ASIN to isbn field in each matched review
print("\n=== Writing ASIN to frontmatter ===")
count = 0
for slug, asin in sorted(ASIN_MAP.items()):
    path = os.path.join(REVIEWS_DIR, f"{slug}.md")
    if not os.path.exists(path):
        continue
    with open(path) as f:
        content = f.read()
    
    if re.search(r'^isbn:\s*"B0', content, re.MULTILINE):
        new_content = re.sub(r'^isbn:\s*"?(B0\w+)"?\s*$', f'isbn: "{asin}"', content, count=1, flags=re.MULTILINE)
    elif re.search(r'^isbn:\s*""', content):
        new_content = re.sub(r'^isbn:\s*""', f'isbn: "{asin}"', content, count=1, flags=re.MULTILINE)
    elif re.search(r'^isbn:\s*$', content, re.MULTILINE):
        new_content = re.sub(r'^isbn:\s*$', f'isbn: "{asin}"', content, count=1, flags=re.MULTILINE)
    else:
        # Insert after year or genre line
        new_content = re.sub(r'^(genre:.+)$', rf'\1\nisbn: "{asin}"', content, count=1, flags=re.MULTILINE)
    
    if new_content != content:
        with open(path, 'w') as f:
            f.write(new_content)
        count += 1

print(f"Updated {count} files with ASIN (Amazon cover URLs)")