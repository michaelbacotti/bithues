#!/usr/bin/env python3
import re
import os
import json

REVIEWS_DIR = '/tmp/bithues-review-template/reviews'

# Files to process: 1.html through 36.html (skip _new files and named files)
targets = []
for n in range(1, 37):
    fname = f'{n}.html'
    fpath = os.path.join(REVIEWS_DIR, fname)
    if os.path.exists(fpath):
        targets.append(fpath)

print(f"Found {len(targets)} target review files.")

processed = 0
skipped = 0

for fpath in targets:
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # ── Extract book title and author from <title> tag ──
    title_match = re.search(r'<title>([^<]+)</title>', html)
    full_title = title_match.group(1) if title_match else ''
    
    # Pattern: "Book Title – Author Name | Bithues Reading Lab"
    book_title = 'Unknown'
    author = 'Unknown'
    if full_title:
        # Split on em-dash or regular dash
        parts = re.split(r'\s*[–—-]\s*', full_title, maxsplit=1)
        book_title = parts[0].strip()
        if len(parts) > 1:
            # Remove " | Bithues Reading Lab" suffix
            author_part = parts[1]
            author_part = re.sub(r'\s*\|.*$', '', author_part).strip()
            author = author_part if author_part else 'Unknown'

    # ── Extract TLDR ──
    # Try class="tldr" first
    tldr_match = re.search(r'<p[^>]*class=["\']tldr["\'][^>]*>([^<]+)</p>', html, re.IGNORECASE)
    if not tldr_match:
        # Try meta description
        desc_match = re.search(r'<meta name="description"\s+content="([^"]+)"', html, re.IGNORECASE)
        if desc_match:
            tldr = desc_match.group(1)[:200]
        else:
            tldr = f'Book review by Bithues Reading Lab'
    else:
        tldr = tldr_match.group(1)[:200]

    # Escape for JSON/HTML attributes
    tldr_attr = tldr.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    tldr_json = tldr.replace('"', '\\"').replace('\\', '\\\\')
    book_title_attr = book_title.replace('"', '&quot;')
    book_title_json = book_title.replace('"', '\\"')
    author_attr = author.replace('"', '&quot;')
    author_json = author.replace('"', '\\"')

    modified = False

    # ── Add og:description ──
    if 'og:description' not in html:
        html = html.replace(
            '<meta name="description"',
            f'<meta property="og:description" content="{tldr_attr[:150]}">\n  <meta name="description"',
            1
        )
        modified = True

    # ── Add og:title ──
    if 'og:title' not in html:
        html = html.replace(
            '<meta property="og:description"',
            f'<meta property="og:title" content="{book_title_attr} – {author_attr} | Bithues Reading Lab">\n  <meta property="og:description"',
            1
        )
        modified = True

    # ── Add Review schema ──
    needs_schema = 'application/ld+json' not in html or '"@type": "Review"' not in html
    if needs_schema:
        schema = f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Review",
    "itemReviewed": {{
      "@type": "Book",
      "name": "{book_title_json}",
      "author": {{ "@type": "Person", "name": "{author_json}" }}
    }},
    "reviewRating": {{ "@type": "Rating", "ratingValue": "4", "bestRating": "5" }},
    "author": {{ "@type": "Organization", "name": "Bithues Reading Lab" }},
    "reviewBody": "{tldr_json[:200]}",
    "publisher": {{ "@type": "Organization", "name": "Bithues Reading Lab", "url": "https://www.bithues.com" }}
  }}
  </script>'''
        html = html.replace('</head>', f'{schema}\n</head>', 1)
        modified = True

    if modified:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        fname = os.path.basename(fpath)
        print(f"  ✓ {fname}: title='{book_title}', author='{author}', tldr='{tldr[:60]}...'")
        processed += 1
    else:
        fname = os.path.basename(fpath)
        print(f"  — {fname}: already has OG tags + schema, skipped")
        skipped += 1

print(f"\nDone! Processed: {processed}, Skipped (already done): {skipped}")
