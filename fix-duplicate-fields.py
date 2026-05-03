#!/usr/bin/env python3
"""Remove ALL duplicate frontmatter fields - keep last value."""
import os, re

REVIEWS_DIR = "/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo/content/reviews"
fixed = 0

# Known frontmatter fields (in order)
KNOWN_FIELDS = [
    'title', 'author', 'genre', 'isbn', 'year', 'stars', 'description',
    'tldr', 'the_good', 'the_less_good', 'verdict', 'cover_gradient',
    'publisher', 'pages', 'format', 'excerpt', 'adsense'
]

for filename in sorted(os.listdir(REVIEWS_DIR)):
    if not filename.endswith('.md') or filename == '_index.md':
        continue
    path = os.path.join(REVIEWS_DIR, filename)
    with open(path) as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Split into frontmatter and body
    fm_lines = []
    body_lines = []
    in_frontmatter = False
    dash_count = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '---':
            dash_count += 1
            if dash_count == 1:
                in_frontmatter = True
                continue
            elif dash_count == 2:
                in_frontmatter = False
                body_lines = lines[i+1:]
                break
        if in_frontmatter:
            fm_lines.append((i, stripped))
    
    # Find all duplicate field names
    seen = {}
    dupe_positions = []
    for idx, (orig_idx, field_stripped) in enumerate(fm_lines):
        field_name = field_stripped.split(':')[0] if ':' in field_stripped else field_stripped
        if field_name in seen:
            dupe_positions.append(idx)
        else:
            seen[field_name] = idx
    
    if not dupe_positions:
        continue
    
    # Keep LAST occurrence of each field
    field_positions = {}
    for idx, (orig_idx, field_stripped) in enumerate(fm_lines):
        field_name = field_stripped.split(':')[0] if ':' in field_stripped else field_stripped
        field_positions[field_name] = orig_idx
    
    # Rebuild: keep only last occurrence of each field
    kept_positions = set()
    for field_name, last_pos in field_positions.items():
        for idx, (orig_idx, _) in enumerate(fm_lines):
            if orig_idx == last_pos:
                kept_positions.add(idx)
                break
    
    new_fm_lines = []
    for idx, (orig_idx, field_stripped) in enumerate(fm_lines):
        if idx in kept_positions:
            new_fm_lines.append(lines[orig_idx])
    
    # Reassemble
    new_content = '---\n' + '\n'.join(new_fm_lines) + '\n---\n' + ''.join(body_lines)
    
    with open(path, 'w') as f:
        f.write(new_content)
    
    print(f"Fixed duplicate fields in: {filename}")
    fixed += 1

print(f"\nFixed {fixed} files")
