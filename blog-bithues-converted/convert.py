#!/usr/bin/env python3
"""
Full conversion of bithues-work → blog-bithues-converted.
Every content type converted and wrapped in blog-bithues style.
"""

import os
import re
from pathlib import Path
import shutil

SRC = Path("/Users/mike/.openclaw/workspace-bacottibot/bithues/bithues-work")
OUT = Path("/Users/mike/.openclaw/workspace-bacottibot/bithues/blog-bithues-converted")

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;500;600;700&display=swap" rel="stylesheet">"""

CSS_LINK = '<link rel="stylesheet" href="css/style.css">'

NAV = '''<nav class="nav">
  <div class="nav-inner">
    <a href="index.html" class="nav-logo">Bithues</a>
    <div class="nav-links">
      <a href="index.html" class="nav-link">Feed</a>
      <a href="browse.html" class="nav-link">Browse</a>
      <a href="about.html" class="nav-link">About</a>
    </div>
  </div>
</nav>'''

FOOTER = '''<footer class="footer">
  <div class="footer-inner">
    <a href="index.html" class="footer-brand">Bithues</a>
    <nav class="footer-nav">
      <a href="index.html">Feed</a>
      <a href="browse.html">Browse</a>
      <a href="about.html">About</a>
    </nav>
    <p class="footer-copy">© <span id="year"></span> Bithues. All rights reserved.</p>
  </div>
</footer>
<script>document.getElementById("year").textContent = new Date().getFullYear();</script>'''

TAG_LABEL = {"article": "Article", "story": "Short Story", "review": "Book Review", "best-list": "Best List", "books-like": "Books Like"}

def get_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    return m.group(1).strip() if m else "Bithues"

def get_description(html):
    m = re.search(r'<meta name="description" content="(.*?)"', html)
    return m.group(1).strip() if m else ""

def clean_title(title):
    return re.sub(r'\s*[-|–]\s*Bithues.*', '', title).strip()

def extract_article_content(html):
    hero_start = html.find('class="article-hero"')
    if hero_start == -1:
        hero_start = html.find("class='article-hero'")
    keep_reading = html.find("Keep Reading")
    if hero_start != -1 and keep_reading != -1:
        return html[hero_start:keep_reading]
    m = re.search(r'class="article-body"[^>]*>(.*?)</div>\s*<div\s+style="margin:2\.5rem', html, re.DOTALL)
    if m:
        return m.group(0)
    return ""

def extract_review_content(html):
    hero_start = html.find('class="review-hero"')
    if hero_start == -1:
        hero_start = html.find('class="review-body"')
    keep_reading = html.find("Keep Reading")
    if hero_start != -1 and keep_reading != -1:
        return html[hero_start:keep_reading]
    # Fallback: no Keep Reading found — extract from hero to </main> or <footer>
    if hero_start != -1:
        main_end = html.find('</main>', hero_start)
        footer_pos = html.find('<footer', hero_start)
        end = min(x for x in [main_end, footer_pos] if x != -1)
        return html[hero_start:end] if end != 999999 else html[hero_start:]
    # Last resort: use review-body
    body_start = html.find('class="review-body"')
    if body_start != -1:
        main_end = html.find('</main>', body_start)
        footer_pos = html.find('<footer', body_start)
        end = min(x for x in [main_end, footer_pos] if x != -1)
        return html[body_start:end] if end != 999999 else html[body_start:]
    return ""

def extract_generic_content(html):
    m = re.search(r'<main[^>]*class="[^"]*feed[^"]*"[^>]*>(.*?)</main>', html, re.DOTALL)
    if m:
        return m.group(1)
    m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if m:
        return m.group(1)
    return html[html.find('<body'):html.find('</body>')] if '<body>' in html else ""

def make_page(title, content_type, body_content):
    clean_t = clean_title(title)
    tag = TAG_LABEL.get(content_type, "Article")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="">
  {FONTS}
  {CSS_LINK}
</head>
<body>
{NAV}
<header class="hero">
  <div class="hero-inner">
    <span style="display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--color-text-light);margin-bottom:10px;">{tag}</span>
    <h1 class="hero-title">{clean_t}</h1>
  </div>
</header>
<main class="main">
  <div class="feed">
{body_content}
  </div>
</main>
{FOOTER}
</body>
</html>'''

def make_simple_page(title, description, body_content):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  {FONTS}
  {CSS_LINK}
</head>
<body>
{NAV}
<header class="hero">
  <div class="hero-inner">
    <h1 class="hero-title">{title}</h1>
  </div>
</header>
<main class="main">
  <div class="feed">
{body_content}
  </div>
</main>
{FOOTER}
</body>
</html>'''

def process(src_path, out_path, content_type, extractor):
    html_content = src_path.read_text(encoding="utf-8", errors="replace")
    title = get_title(html_content)
    description = get_description(html_content)
    body = extractor(html_content)
    page_html = make_page(title, content_type, body)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page_html, encoding="utf-8")

def process_dir(src_dir, out_dir, content_type, extractor, skip_html_redirects=True):
    count = 0
    errors = []
    out_dir.mkdir(parents=True, exist_ok=True)
    for item in src_dir.iterdir():
        if item.is_dir():
            src_file = item / "index.html"
            if src_file.exists():
                slug = item.name
                out_file = out_dir / f"{slug}.html"
                try:
                    process(src_file, out_file, content_type, extractor)
                    count += 1
                except Exception as e:
                    errors.append(f"{content_type}/{slug}: {e}")
        elif skip_html_redirects and item.suffix == ".html" and item.stem not in ("index",):
            # Skip numeric redirect files like "1.html", "2.html" etc.
            pass
        elif item.suffix == ".html" and item.stem not in ("index",):
            slug = item.stem
            out_file = out_dir / f"{slug}.html"
            try:
                process(item, out_file, content_type, extractor)
                count += 1
            except Exception as e:
                errors.append(f"{content_type}/{slug}: {e}")
    return count, errors

def main():
    # Ensure CSS copied
    out_css = OUT / "css"
    out_css.mkdir(parents=True, exist_ok=True)
    for fname in ["style.css", "main.css", "article.css"]:
        src = Path(f"/Users/mike/.openclaw/workspace-bacottibot/bithues/blog-bithues/css/{fname}")
        if src.exists():
            shutil.copy(src, out_css / fname)
    
    total = 0
    all_counts = {}
    all_errors = []
    
    # ----------------------------------------------------------------
    # 1. Articles (58)
    # ----------------------------------------------------------------
    cnt, errs = process_dir(SRC/"articles", OUT/"content", "article", extract_article_content)
    all_counts["Article pages"] = cnt
    all_errors.extend(errs)
    
    # ----------------------------------------------------------------
    # 2. Stories (37)
    # ----------------------------------------------------------------
    cnt, errs = process_dir(SRC/"stories", OUT/"content", "story", extract_generic_content)
    all_counts["Story pages"] = cnt
    all_errors.extend(errs)
    
    # ----------------------------------------------------------------
    # 3. Reviews (60 folder-based — skip 74 numeric redirect .html files)
    # ----------------------------------------------------------------
    cnt, errs = process_dir(SRC/"reviews", OUT/"content", "review", extract_review_content, skip_html_redirects=True)
    all_counts["Review pages"] = cnt
    all_errors.extend(errs)
    
    # ----------------------------------------------------------------
    # 4. Author pages (34)
    # ----------------------------------------------------------------
    cnt, errs = process_dir(SRC/"authors", OUT/"authors", "article", extract_generic_content)
    all_counts["Author pages"] = cnt
    all_errors.extend(errs)
    
    # ----------------------------------------------------------------
    # 5. Best-list pages (19 content folders)
    # ----------------------------------------------------------------
    cnt, errs = process_dir(SRC/"best-list", OUT/"best-list", "best-list", extract_generic_content)
    all_counts["Best-list pages"] = cnt
    all_errors.extend(errs)
    
    # ----------------------------------------------------------------
    # 6. Books-like pages (12)
    # ----------------------------------------------------------------
    cnt, errs = process_dir(SRC/"books-like", OUT/"books-like", "books-like", extract_generic_content)
    all_counts["Books-like pages"] = cnt
    all_errors.extend(errs)
    
    # ----------------------------------------------------------------
    # 7. Book-tracker page (1) — special: single page at /book-tracker/
    # ----------------------------------------------------------------
    tracker_src = SRC/"book-tracker"/"index.html"
    if tracker_src.exists():
        out_tracker = OUT/"book-tracker.html"
        try:
            process(tracker_src, out_tracker, "article", extract_generic_content)
            all_counts["Book-tracker page"] = 1
        except Exception as e:
            all_errors.append(f"book-tracker: {e}")
    
    # ----------------------------------------------------------------
    # 8. Reading-lists page (1) — special: single page
    # ----------------------------------------------------------------
    rl_src = SRC/"reading-lists"/"index.html"
    if rl_src.exists():
        out_rl = OUT/"reading-lists.html"
        try:
            process(rl_src, out_rl, "article", extract_generic_content)
            all_counts["Reading-lists page"] = 1
        except Exception as e:
            all_errors.append(f"reading-lists: {e}")
    
    # ----------------------------------------------------------------
    # 9. Category listing pages (19 genre HTML files at /category/)
    # ----------------------------------------------------------------
    cat_dir = SRC/"category"
    cat_out = OUT/"category"
    cat_out.mkdir(parents=True, exist_ok=True)
    cnt = 0
    for item in cat_dir.iterdir():
        if item.suffix == ".html" and item.stem not in ("index",):
            slug = item.stem
            genre_name = slug.replace("-", " ").title()
            html_content = item.read_text(encoding="utf-8", errors="replace")
            body = extract_generic_content(html_content)
            page_html = make_simple_page(genre_name, f"{genre_name} books and articles on Bithues", body)
            out_file = cat_out / f"{slug}.html"
            out_file.write_text(page_html, encoding="utf-8")
            cnt += 1
    all_counts["Category listing pages"] = cnt
    
    # ----------------------------------------------------------------
    # 10. Genre taxonomy term pages — from /genres/ subdirectories
    #    These are Hugo taxonomy terms for each genre
    # ----------------------------------------------------------------
    genres_out = OUT/"genres"
    genres_out.mkdir(parents=True, exist_ok=True)
    cnt = 0
    for item in (SRC/"genres").iterdir():
        if item.is_dir():
            slug = item.name
            genre_name = slug.replace("-", " ").title()
            genre_file = item / "index.html"
            if genre_file.exists():
                html_content = genre_file.read_text(encoding="utf-8", errors="replace")
                body = extract_generic_content(html_content)
            else:
                body = ""
            page_html = make_simple_page(genre_name, f"Read {genre_name} book reviews and articles on Bithues", body)
            (genres_out / f"{slug}.html").write_text(page_html, encoding="utf-8")
            cnt += 1
        elif item.suffix == ".html" and item.stem not in ("index",):
            slug = item.stem
            genre_name = slug.replace("-", " ").title()
            html_content = item.read_text(encoding="utf-8", errors="replace")
            body = extract_generic_content(html_content)
            page_html = make_simple_page(genre_name, f"Read {genre_name} book reviews and articles on Bithues", body)
            (genres_out / f"{slug}.html").write_text(page_html, encoding="utf-8")
            cnt += 1
    all_counts["Genre term pages"] = cnt
    
    # ----------------------------------------------------------------
    # Print summary
    # ----------------------------------------------------------------
    print("=== Conversion Summary ===")
    for k, v in sorted(all_counts.items()):
        print(f"  {k}: {v}")
    total_pages = sum(all_counts.values())
    print(f"\nTotal pages: {total_pages}")
    
    if all_errors:
        print(f"\nErrors ({len(all_errors)}):")
        for e in all_errors[:30]:
            print(f"  {e}")

if __name__ == "__main__":
    main()