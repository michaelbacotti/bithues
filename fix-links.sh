#!/usr/bin/env bash
# fix-links.sh — comprehensive link fix for bithues.com
set -euo pipefail
cd "$(dirname "$0")"

echo "=== FIX 1: reviews/otomi.html — wrong author link (missing accent í) ==="
sed -i '' 's|href="../authors/e-j-marin.html"|href="../authors/e-j-marín.html"|g' reviews/otomi.html
grep -n "e-j-mar" reviews/otomi.html | head -3
echo "✅ Fixed"

echo ""
echo "=== FIX 2: authors/template.html — nav-brand links to index.html (needs ../) ==="
sed -i '' 's|href="index.html" class="nav-brand"|href="../index.html" class="nav-brand"|g' authors/template.html
grep -n 'nav-brand' authors/template.html
echo "✅ Fixed"

echo ""
echo "=== FIX 3: articles/hopepunk-fiction.html — bad ../ links to files in articles/ ==="
sed -i '' 's|href="../best-sci-fi-2026.html"|href="best-sci-fi-2026.html"|g' articles/hopepunk-fiction.html
sed -i '' 's|href="../books-like-physics-of-time.html"|href="books-like-physics-of-time.html"|g' articles/hopepunk-fiction.html
grep -n "best-sci-fi-2026\|books-like-physics" articles/hopepunk-fiction.html
echo "✅ Fixed"

echo ""
echo "=== FIX 4: category/nonfiction.html — wrong /categories link ==="
sed -i '' 's|href="/categories"|href="/category"|g' category/nonfiction.html
grep -n 'href="/category"' category/nonfiction.html
echo "✅ Fixed"

echo ""
echo "=== FIX 5: Delete orphaned categories/ directory ==="
if [ -d "categories" ]; then
    rm -rf categories/
    echo "✅ Deleted categories/ directory"
else
    echo "⚠️  categories/ directory not found — skipping"
fi

echo ""
echo "=== FIX 6: Canonical URLs — non-www bithues.com → www.bithues.com ==="
COUNT=$(grep -r 'canonical.*https://bithues\.com/' . --include='*.html' | grep -v 'www\.bithues' | wc -l | tr -d ' ')
echo "Found $COUNT file(s) with non-www canonical"
grep -r 'canonical.*https://bithues\.com/' . --include='*.html' | grep -v 'www\.bithues'
sed -i '' 's|href="https://bithues\.com/|href="https://www.bithues.com/|g' \
    $(grep -rl 'canonical.*https://bithues\.com/' . --include='*.html' | grep -v 'www\.bithues' | tr '\n' ' ')
echo "✅ Fixed"

echo ""
echo "=== FIX 7: reviews/ — breadcrumb href=\"index.html\" → href=\"../index.html\" ==="
# The breadcrumb pattern has TWO index.html links per file:
#   <a href="../index.html" ...>Home</a> › <a href="index.html" ...>Reviews</a>
# We need to change the SECOND one (the Reviews link) from "index.html" to "../index.html"
# Pattern: after "› " the second href="index.html" (Reviews breadcrumb) needs fixing

# Fix all review HTML files using a Python script for precision
python3 - <<'PYEOF'
import os, re, glob

review_files = glob.glob('reviews/*.html')
fixed = 0
for filepath in review_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern: the breadcrumb has Home link (../index.html) followed by Reviews link (index.html)
    # We need to change the Reviews breadcrumb link from href="index.html" to href="../index.html"
    # but only in the context of the breadcrumb (after Home › ...)
    #
    # The breadcrumb looks like:
    #   <a href="../index.html" ...>Home</a> › <a href="index.html" ...>Reviews</a>
    #
    # We replace: href="index.html" that appears AFTER ../index.html" ...>Home</a> › 
    # This is safe because the only second-level breadcrumb link in reviews/ files is the Reviews index link.
    
    # Replace the Reviews breadcrumb link specifically
    content = re.sub(
        r'(<a href="\.\./index\.html"[^>]*>Home</a> › <a) href="index\.html"',
        r'\1 href="../index.html"',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Fixed: {filepath}")
        fixed += 1

print(f"✅ Fixed {fixed} review file(s)")
PYEOF

echo ""
echo "=== VERIFICATION ==="
echo "reviews/otomi.html author link:"
grep -n "e-j-mar" reviews/otomi.html
echo ""
echo "authors/template.html nav-brand:"
grep -n 'nav-brand' authors/template.html
echo ""
echo "articles/hopepunk-fiction.html article-internal links:"
grep -n "best-sci-fi-2026\|books-like-physics" articles/hopepunk-fiction.html
echo ""
echo "category/nonfiction.html categories link:"
grep -n 'href="/category"' category/nonfiction.html
echo ""
echo "categories/ directory (should be gone):"
ls categories/ 2>&1 || echo "(directory deleted ✓)"
echo ""
echo "Canonical URLs with non-www:"
grep -r 'canonical.*bithues\.com' . --include='*.html' | grep -v 'www\.bithues' || echo "(none ✓)"
echo ""
echo "reviews/ remaining bad breadcrumb href='index.html':"
count=$(grep -rn 'Home.*›.*href="index\.html"' reviews/ | grep -v '\.\./index\.html' | wc -l | tr -d ' ')
echo "Remaining bad breadcrumb links: $count"
if [ "$count" -gt 0 ]; then
    grep -rn 'Home.*›.*href="index\.html"' reviews/ | grep -v '\.\./index\.html'
fi
echo ""
echo "=== ALL FIXES COMPLETE ==="
