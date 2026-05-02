#!/usr/bin/env python3
"""Batch-convert all 20 category pages to Goodreads style."""
import subprocess, csv, sys

meta = {}
with open('category-meta.txt') as f:
    for row in csv.reader(f):
        if len(row) >= 4:
            slug = row[0]
            title = row[1]
            desc = row[2]
            count = row[3]
            meta[slug] = {'title': title, 'desc': desc, 'count': count}

converted, errors = [], []
for slug, info in meta.items():
    src = f'category/{slug}.html'
    result = subprocess.run(
        [sys.executable, 'fix-category-pages.py',
         src, src, slug,
         info['title'], info['desc'], info['count']],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        converted.append(slug)
        print(f"✅ {slug}")
    else:
        errors.append((slug, result.stderr[:200]))
        print(f"❌ {slug}: {result.stderr[:200]}")

print(f"\nConverted {len(converted)}/20")
if errors:
    for s, e in errors:
        print(f"  ERROR {s}: {e}")