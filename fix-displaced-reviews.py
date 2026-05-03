#!/usr/bin/env python3
"""Fix wrong frontmatter and body content in displaced review files."""
import os, re

REVIEWS_DIR = "/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo/content/reviews"

# Track what each file SHOULD have (title, author, genre, isbn)
CORRECTIONS = {
    'aetheri-codex.md': {
        'title': 'Echoes of Aetheris',
        'author': 'Aetheri Codex',
        'genre': 'Science Fiction',
        'isbn': 'B0GPPBCKYF',
    },
    'cords-of-empire.md': {
        'title': 'Cords of Empire',
        'author': 'E. J. Marín',
        'genre': 'Historical Fiction',
        'isbn': '',  # not in tracker
    },
    'living-with-a-moving-planet.md': {
        'title': 'Living with a Moving Planet',
        'author': 'J. T. Hartley',
        'genre': 'Nonfiction',
        'isbn': 'B0GQ2YCLD4',
    },
    'xaltocan.md': {
        'title': 'Xaltocan',
        'author': 'E. J. Marín',
        'genre': 'Historical Fiction',
        'isbn': '',  # not in tracker
    },
    'the-martian.md': {
        'title': 'The Martian',
        'author': 'Andy Weir',
        'genre': 'Science Fiction',
        'isbn': '9780553418026',  # ISBN-13
    },
    '19.md': {
        'title': "Microbiology ABC's",
        'author': 'Michael Bacotti',
        'genre': 'Children',
        'isbn': 'B0GR7R6HT1',
    },
}

# Books whose body content is WRONG (they have The Martian text) - clear them
WRONG_BODY = {'aetheri-codex', 'cords-of-empire', 'xaltocan', 'the-martian', 'living-with-a-moving-planet'}

def fix_file(filename, info):
    slug = filename.replace('.md', '')
    path = os.path.join(REVIEWS_DIR, filename)
    with open(path) as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Rebuild frontmatter
    new_frontmatter = []
    seen_fields = set()
    
    for line in lines:
        stripped = line.strip()
        # Skip old frontmatter fields we'll replace
        field_name = stripped.split(':')[0] if ':' in stripped else ''
        if field_name in ('title', 'author', 'genre', 'isbn', 'cover_gradient', 'publisher', 'pages', 'format', 'tldr', 'the_good', 'the_less_good', 'verdict', 'excerpt'):
            if field_name not in seen_fields:
                seen_fields.add(field_name)
                continue  # skip original
        
        # Stop at end of frontmatter
        if stripped == '---' and len(new_frontmatter) > 0:
            break
        
        new_frontmatter.append(line)
    
    # Add correct fields in order
    new_frontmatter.append(f'title: "{info["title"]}"')
    new_frontmatter.append(f'author: "{info["author"]}"')
    new_frontmatter.append(f'genre: "{info["genre"]}"')
    new_frontmatter.append(f'isbn: "{info["isbn"]}"')
    new_frontmatter.append('year: ""')
    new_frontmatter.append('stars: "★★★★☆"')
    new_frontmatter.append(f'description: "In-depth review of {info["title"]} on Bithues."')
    new_frontmatter.append('tldr: ""')
    new_frontmatter.append('the_good: ""')
    new_frontmatter.append('the_less_good: ""')
    new_frontmatter.append('verdict: ""')
    new_frontmatter.append('cover_gradient: "linear-gradient(135deg, #1a3a5c 0%, #0f2540 100%)"')
    new_frontmatter.append('publisher: ""')
    new_frontmatter.append('pages: ""')
    new_frontmatter.append('format: ""')
    new_frontmatter.append('excerpt: ""')
    new_frontmatter.append('adsense: true')
    new_frontmatter.append('---')
    new_frontmatter.append('')
    
    if slug in WRONG_BODY:
        # Add placeholder body
        new_frontmatter.append(f'<!-- Review content for {info["title"]} pending -->')
        new_frontmatter.append('')
    else:
        # Keep body (already correct for 19.md)
        # Append body after frontmatter
        dash_count = 0
        body_start = 0
        for i, l in enumerate(lines):
            if l.strip() == '---':
                dash_count += 1
                if dash_count == 2:
                    body_start = i + 1
                    break
        body = ''.join(lines[body_start:])
        new_frontmatter.append(body)
    
    with open(path, 'w') as f:
        f.write('\n'.join(new_frontmatter))
    
    print(f'Fixed: {filename} → {info["title"]} (isbn={info["isbn"] or "none"})')

for filename, info in CORRECTIONS.items():
    fix_file(filename, info)

print('\nDone')
