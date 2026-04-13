#!/usr/bin/env bash
# fix-fiction-links.sh
# Creates category/fiction.html and redirects all fiction.html links to catalog.html

SITE="/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues"
TARGET="category/fiction.html"

echo "=== Step 1: Create $TARGET ==="

# Build fiction.html — a broad landing page linking to every category
cat > "$SITE/$TARGET" << 'FICTIONEOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fiction Books | Bithues Reading Lab</title>
  <meta name="description" content="Browse all fiction book reviews on Bithues Reading Lab — fantasy, sci-fi, mystery, romance, thriller, and more.">
  <meta name="google-adsense-account" content="ca-pub-9312870448453345" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/main.css">
  <link rel="canonical" href="https://www.bithues.com/category/fiction.html">
</head>

<body>
    <div class="container">
        <header>
              <!-- ── NAV ── -->
  <nav>
    <a href="index.html" class="nav-brand">Bithues <span>Reading Lab</span></a>
    <div class="nav-links">
      <div class="nav-item"><a href="index.html">Home</a></div>
      <div class="nav-item">
        <a href="catalog.html" class="active">Reviews ▾</a>
        <div class="dropdown">
          <a href="catalog.html">All Reviews</a>
          <a href="category/self-help.html">Self-Help</a>
          <a href="category/science-fiction.html">Sci-Fi</a>
          <a href="category/fantasy.html">Fantasy</a>
          <a href="category/nonfiction.html">Nonfiction</a>
          <a href="category/thriller.html">Thriller</a>
          <a href="category/biography.html">Biography</a>
          <a href="category/business.html">Business</a>
        </div>
      </div>
      <div class="nav-item">
        <a href="stories.html">Stories ▾</a>
        <div class="dropdown">
          <a href="stories.html">All Stories</a>
        </div>
      </div>
      <div class="nav-item">
        <a href="articles.html">Articles ▾</a>
        <div class="dropdown">
          <a href="articles.html">All Articles</a>
          <a href="articles/dna-ancestry-historical-fiction.html">DNA &amp; Historical Fiction</a>
        </div>
      </div>
      <div class="nav-item"><a href="about.html">About</a></div>
      <div class="nav-item"><a href="contact.html">Contact</a></div>
    </div>
  </nav>
        </header>

        <section class="page-header">
            <h1 class="header">Fiction Books</h1>
            <p>Browse all fiction genres — fantasy, sci-fi, mystery, romance, thriller, and more.</p>
        </section>

        <section class="book-grid">
            <p style="color:var(--text-secondary);font-style:italic;">
              Fiction is a broad genre. Explore our specific fiction categories below, or browse all reviews in the catalog.
            </p>
        </section>

        <section class="genre-tags" style="margin-top:1.5rem;">
            <a href="catalog.html" class="genre-tag">All Reviews</a>
            <a href="category/science-fiction.html" class="genre-tag">Science Fiction</a>
            <a href="category/fantasy.html" class="genre-tag">Fantasy</a>
            <a href="category/mystery.html" class="genre-tag">Mystery</a>
            <a href="category/thriller.html" class="genre-tag">Thriller</a>
            <a href="category/historical-fiction.html" class="genre-tag">Historical Fiction</a>
            <a href="category/romance.html" class="genre-tag">Romance</a>
            <a href="category/dystopian.html" class="genre-tag">Dystopian</a>
            <a href="category/adventure.html" class="genre-tag">Adventure</a>
            <a href="category/mythology.html" class="genre-tag">Mythology</a>
            <a href="category/literary.html" class="genre-tag">Literary Fiction</a>
            <a href="category/children.html" class="genre-tag">Children's Fiction</a>
            <a href="category/self-help.html" class="genre-tag">Self-Help</a>
        </section>

        
  <!-- ── FOOTER ── -->
  <footer>
    <div class="footer-brand">Bithues <span>Reading Lab</span></div>
    <p>© <span id="year"></span> Bithues Reading Lab · <a href="press.html">Press</a> · <a href="contact.html">Contact</a> · <a href="privacy.html">Privacy</a></p>
  </footer>

  <button class="back-to-top" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>

  <script>
    window.onscroll = function() {
      document.querySelector('.back-to-top').classList.toggle('visible', window.scrollY > 300);
    };
    document.getElementById('year').textContent = new Date().getFullYear();
  </script>

</body>
</html>
FICTIONEOF

echo "Created $TARGET"

echo ""
echo "=== Step 2: Replace fiction.html links ==="

# Count before
BEFORE=$(grep -rl 'href=".*fiction\.html"' "$SITE" | grep -v "category/fiction\.html$" | wc -l | tr -d ' ')
echo "Files with fiction.html links (before): $BEFORE"

# Replace fiction.html links:
# - Root-level files: category/fiction.html → catalog.html
# - Subdirectory files: ../category/fiction.html → ../catalog.html
# - reviews/, stories/, authors/, articles/ subdirs: ../category/fiction.html → ../catalog.html
# - category itself dir: fiction.html → catalog.html (same dir, relative)
# - Also handle href="fiction.html" (no path prefix, same directory)

cd "$SITE"

# Files in root directory (index.html, catalog.html, about.html, etc.)
# Replace: href="category/fiction.html" → href="catalog.html"
for f in index.html catalog.html about.html contact.html articles.html authors.html stories.html reading-lists.html reading-lists/index.html press.html forecast.html author-pitch.html privacy.html games.html 404.html reading-lists.html categories/index.html; do
  if [ -f "$f" ]; then
    sed -i '' 's|href="category/fiction\.html"|href="catalog.html"|g' "$f"
    echo "  Fixed (root): $f"
  fi
done

# Files in category/ subdirectory
# Replace: href="fiction.html" → href="catalog.html" (same directory)
for f in category/*.html; do
  if [ -f "$f" ]; then
    sed -i '' 's|href="fiction\.html"|href="catalog.html"|g' "$f"
    echo "  Fixed (category/): $f"
  fi
done

# Files in reviews/, stories/, authors/, articles/ subdirectories
# Replace: href="../category/fiction.html" → href="../catalog.html"
for dir in reviews stories authors articles; do
  for f in "$dir"/*.html; do
    if [ -f "$f" ]; then
      sed -i '' 's|href="../category/fiction\.html"|href="../catalog.html"|g' "$f"
      echo "  Fixed ($dir/): $f"
    fi
  done
done

# Verify remaining fiction.html links (should only be the new fiction.html itself)
REMAIN=$(grep -rl 'href=".*fiction\.html"' "$SITE" | grep -v "category/fiction\.html$" | wc -l | tr -d ' ')
echo ""
echo "Files with fiction.html links (after): $REMAIN"

if [ "$REMAIN" -gt 0 ]; then
  echo "WARNING: Remaining files with fiction.html links:"
  grep -rl 'href=".*fiction\.html"' "$SITE" | grep -v "category/fiction\.html$"
else
  echo "All fiction.html links successfully replaced!"
fi

echo ""
echo "=== Done ==="
