#!/usr/bin/env python3
"""Update review frontmatter: store ISBNs and Open Library cover URLs."""
import csv, os, re

CSV_PATH = '/Users/mike/.openclaw/workspace-bacottibot/scripts/amazon-book-tracker/data/2026-04-13.csv'
REVIEWS_DIR = '/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo/content/reviews'

tracker = {}
with open(CSV_PATH) as f:
    for row in csv.DictReader(f):
        t = row['Title'].strip()
        asin = row['ASIN'].strip()
        isbn13 = row.get('ISBN-13', '').strip() or row.get('isbn13', '').strip()
        if t:
            tracker[t.lower()] = {'asin': asin, 'isbn13': isbn13}
            tracker[t.lower().split(':')[0].strip()] = {'asin': asin, 'isbn13': isbn13}

MANUAL = {
    'the-martian':                   {'isbn13': '9780553418026'},
    'cords-of-empire':                {'isbn13': '979-8257424519'},
    'aetheri-codex':                 {},
    'living-with-a-moving-planet':   {},
    'xaltocan':                      {},
}

def find_isbn13(title, slug):
    t = title.lower()
    short = t.split(':')[0].strip()
    if slug in MANUAL and MANUAL[slug].get('isbn13'):
        return MANUAL[slug]['isbn13']
    for key in [t, short]:
        if key in tracker and tracker[key].get('isbn13'):
            return tracker[key]['isbn13']
    return ''

def build_ol_url(isbn13):
    if not isbn13:
        return ''
    clean = isbn13.replace('-', '').replace(' ', '')
    if len(clean) not in (10, 13):
        return ''
    return f'https://covers.openlibrary.org/b/isbn/{clean}-L.jpg'

def update_file(filename):
    slug = filename.replace('.md', '')
    path = os.path.join(REVIEWS_DIR, filename)
    with open(path) as f:
        content = f.read()
    
    lines = content.split('\n')
    title = ''
    for line in lines:
        m = re.search(r'^title:\s*"?([^"\n]+)"?', line)
        if m:
            title = m.group(1).strip()
            break
    
    isbn13 = find_isbn13(title, slug)
    cover_url = build_ol_url(isbn13)
    
    new_lines = []
    seen = {}
    for line in lines:
        stripped = line.strip()
        key = stripped.split(':')[0] if ':' in stripped else ''
        # Drop duplicates
        if key in ('isbn', 'cover_url'):
            if key not in seen:
                seen[key] = True
                if key == 'isbn':
                    new_lines.append(f'isbn: "{isbn13}"')
                else:
                    new_lines.append(f'cover_url: "{cover_url}"')
            continue
        new_lines.append(line)
    
    # Add cover_url if not present
    if 'cover_url' not in seen and cover_url:
        # Insert after isbn line
        result = []
        for line in new_lines:
            result.append(line)
            if line.strip().startswith('isbn:'):
                result.append(f'cover_url: "{cover_url}"')
        new_lines = result
    
    with open(path, 'w') as f:
        f.write('\n'.join(new_lines))
    
    return slug, isbn13, cover_url

print("Updating review covers...")
for filename in sorted(os.listdir(REVIEWS_DIR)):
    if not filename.endswith('.md') or filename == '_index.md':
        continue
    slug, isbn13, cover_url = update_file(filename)
    print(f"  {slug}: isbn={isbn13 or 'none'} cover={cover_url or 'none'}")

print("\nDone")
