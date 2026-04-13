#!/usr/bin/env python3
"""Fix common issues in bithues review pages."""
import os
import re
from pathlib import Path

REVIEWS_DIR = Path("reviews")
CSS_FILE = Path("css/main.css")

def process_file(filepath):
    """Fix inline styles and structural issues in a review HTML file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changed = []

    # ── 1. Fix inline back-link breadcrumbs ──
    # Pattern A: class="back-link" style="color:var(--text-dim); font-size: 0.85rem;"
    content = re.sub(
        r'<a href="([^"]*)" class="back-link" style="color:var\(--text-dim\); font-size: 0\.85rem;">',
        r'<a href="\1" class="back-link">',
        content
    )
    if re.search(r'<a href="[^"]*" class="back-link" style="color:var\(--text-dim\); font-size: 0\.85rem;">', original):
        changed.append("breadcrumb-style-A")

    # Pattern B: no class=back-link, just inline style with text-decoration none variant
    content = re.sub(
        r'<a href="([^"]*)" style="color:var\(--text-dim\); font-size: 0\.85rem; text-decoration: none;">',
        r'<a href="\1" class="back-link">',
        content
    )
    if re.search(r'<a href="[^"]*" style="color:var\(--text-dim\); font-size: 0\.85rem; text-decoration: none;">', original):
        changed.append("breadcrumb-style-B")

    # ── 2. Fix inline accent on author links ──
    content = re.sub(
        r'<a href="([^"]*)" style="color:var\(--accent\);">',
        r'<a href="\1" class="author-link">',
        content
    )
    if re.search(r'<a href="[^"]*" style="color:var\(--accent\);">', original):
        changed.append("author-link-style")

    # ── 3. Fix inline current-book chip span ──
    content = re.sub(
        r'<span style="color: #7c3aed; font-size: 0\.85rem;">',
        r'<span class="current-book">',
        content
    )
    if re.search(r'<span style="color: #7c3aed; font-size: 0\.85rem;">', original):
        changed.append("current-book-style")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return changed

def add_css_classes():
    """Append missing CSS rules to main.css if not already present."""
    css_path = CSS_FILE
    existing = css_path.read_text(encoding="utf-8")

    rules = """.back-link {
  color: var(--text-dim);
  font-size: 0.85rem;
  text-decoration: none;
}
.back-link:hover { text-decoration: underline; }
.author-link { color: var(--accent); }
.author-link:hover { text-decoration: underline; }
.current-book {
  color: #7c3aed;
  font-size: 0.85rem;
}
"""

    # Only add if not already there
    if ".back-link {" not in existing:
        with open(css_path, "a", encoding="utf-8") as f:
            f.write("\n/* Review page utility classes */\n" + rules)
        return True
    return False

def main():
    css_updated = add_css_classes()
    total = 0
    files_changed = 0
    details = []

    for html_file in sorted(REVIEWS_DIR.glob("*.html")):
        # Skip author pages and special files
        if html_file.name in ("index.html", "fix-review-pages.sh"):
            continue
        total += 1
        changes = process_file(html_file)
        if changes:
            files_changed += 1
            details.append(f"  {html_file.name}: {', '.join(changes)}")

    print(f"Total review files scanned: {total}")
    print(f"Files modified: {files_changed}")
    if css_updated:
        print("CSS updated: added .back-link, .author-link, .current-book rules")
    else:
        print("CSS: rules already present (no change)")
    print()
    if details:
        print("Changes by file:")
        for d in details:
            print(d)
    else:
        print("No inline style issues found — files were already clean.")

if __name__ == "__main__":
    main()