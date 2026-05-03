#!/usr/bin/env python3
"""Update ASINs for books that got wrong matches in first pass."""
import re, os

# ASINs from Amazon tracker (only books with non-empty titles in tracker)
CORRECT_ASINS = {
    'the-martian': 'B00DKVGT3W',  # Andy Weir, traditional pub
    'microbiology-abc-s': 'B0GR7R6HT1',
    'three-seas': 'B0D38W5972',
}

REVIEWS_DIR = "/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo/content/reviews"

for slug, asin in CORRECT_ASINS.items():
    path = os.path.join(REVIEWS_DIR, f"{slug}.md")
    if not os.path.exists(path):
        path = os.path.join(REVIEWS_DIR, f"19.md")  # microbiology-abc-s might be 19
        if not os.path.exists(path):
            continue
    
    with open(path) as f:
        content = f.read()
    
    if asin:
        new_content = re.sub(r'^(genre:.+)$', rf'\1\nisbn: "{asin}"', content, count=1, flags=re.MULTILINE)
    else:
        new_content = content
    
    with open(path, 'w') as f:
        f.write(new_content)
    print(f"Updated: {slug} → {asin}")

# Also verify key books have correct ASINs
print("\n=== Verify key books ===")
key_books = ['the-martian', 'home-for-anya', 'the-richmond-cipher', 'microbiology-abc-s']
for slug in key_books:
    # Try both slug and numeric
    for fname in [f"{slug}.md"]:
        path = os.path.join(REVIEWS_DIR, fname)
        if os.path.exists(path):
            with open(path) as f:
                c = f.read()
            m = re.search(r'^isbn:\s*"?(\w+)"?\s*$', c, re.MULTILINE)
            print(f"{slug}: isbn={m.group(1) if m else 'none'}")
            break