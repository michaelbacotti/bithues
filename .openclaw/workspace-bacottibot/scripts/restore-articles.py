#!/usr/bin/env python3
"""Restore article content from Git history and push to GitHub."""
import base64, json, re, sys, time
import urllib.request

GITHUB_TOKEN = "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"
REPO = "michaelbacotti/bithues"
BRANCH = "main"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

ARTICLES = [
    "aliens-disclosure-2026.html","best-books-spring-2026.html","best-books-summer-2026.html",
    "best-sci-fi-2026.html","books-change-how-you-think.html","books-for-dad-gift-guide.html",
    "books-like-physics-of-time.html","books-like-project-hail-mary.html","business-leadership-guide.html",
    "complete-fantasy-encyclopedia.html","fantasy-for-beginners.html","hopepunk-beginners-guide.html",
    "hopepunk-fiction.html","horror-for-beginners.html","how-to-read-more-books.html",
    "how-we-review-books.html","kids-reading-guide.html","little-mike-series.html",
    "meet-indie-authors.html","memoir-biography-guide.html","quantum-physics-beginners-guide.html",
    "quantum-physics-beginners.html","read-more-this-year.html","reading-challenge-2026.html",
    "romance-for-beginners.html","shadow-work-guide.html","speed-reading-basics.html",
    "thriller-mystery-guide.html","ultimate-sci-fi-guide.html","why-indie-authors-rising.html",
    "why-read-outside-your-genre.html"
]

def api(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def put_file(path, content, sha, msg):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    data = json.dumps({
        "message": msg,
        "content": base64.b64encode(content.encode()).decode(),
        "sha": sha,
        "branch": BRANCH
    }).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="PUT")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def extract_body(html_content):
    """Extract the article body (content inside .article-body or main content area)."""
    # Try to find article body div
    body_match = re.search(r'<div class="article-body"[^>]*>(.*?)</div>\s*<footer', html_content, re.DOTALL)
    if body_match:
        return body_match.group(1).strip()
    
    # Try to find content between <!-- ARTICLE CONTENT --> and <footer
    ac_match = re.search(r'<!-- ARTICLE CONTENT -->(.*?)<footer', html_content, re.DOTALL)
    if ac_match:
        return ac_match.group(1).strip()
    
    # Fallback: grab everything between the divider and footer
    div_match = re.search(r'<div class="divider"></div>\s*(.*?)<footer', html_content, re.DOTALL)
    if div_match:
        return div_match.group(1).strip()
    
    return None

def get_old_content(filename):
    """Get article content from previous Git commit."""
    try:
        # Get recent commits for this file
        commits = api(f"https://api.github.com/repos/{REPO}/commits?path=articles/{filename}&per_page=5")
        if not commits or len(commits) < 2:
            print(f"  {filename}: only {len(commits) if commits else 0} commits, skipping")
            return None
        
        # Use the second-most-recent commit (before the bad push)
        prev_sha = commits[1]["sha"]
        commit_data = api(f"https://api.github.com/repos/{REPO}/commits/{prev_sha}")
        
        # Get the file from that commit
        for f in commit_data.get("files", []):
            if f["filename"] == f"articles/{filename}":
                if "raw_content" in f:
                    return f["raw_content"]
        
        # Try getting via contents API with ref=prev_sha
        try:
            contents = api(f"https://api.github.com/repos/{REPO}/contents/articles/{filename}?ref={prev_sha}")
            if isinstance(contents, dict) and contents.get("content"):
                return base64.b64decode(contents["content"]).decode("utf-8", errors="replace")
        except:
            pass
        
        print(f"  {filename}: could not retrieve old content from commit {prev_sha[:7]}")
        return None
    except Exception as e:
        print(f"  {filename}: error - {e}")
        return None

def make_article_html(filename, body_content, title="", description="", category="Article"):
    """Build a complete article HTML file with correct nav/header/footer and old body."""
    if not body_content:
        return None
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="google-adsense-account" content="ca-pub-9312870448453345" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/main.css">
</head>
<body>
  <nav>
    <div class="nav-brand">Bithues <span>Reading Lab</span></div>
    <div class="nav-links">
      <a href="index.html">Home</a>
      <a href="stories.html">Stories</a>
      <a href="catalog.html">Reviews</a>
      <a href="articles.html" class="active">Articles</a>
      <a href="about.html">About</a>
      <a href="contact.html">Contact</a>
    </div>
  </nav>

  <header class="hero" style="padding:3rem 2rem;">
    <div class="hero-eyebrow">{category}</div>
    <h1>{title}</h1>
  </header>

  <div class="divider"></div>

  <!-- ARTICLE CONTENT -->
{body_content}

  <footer>
    <div class="brand">Bithues <span>Reading Lab</span></div>
    <p>© <span id="year"></span> Bithues Reading Lab · <a href="press.html">Press</a> · <a href="contact.html">Contact</a> · <a href="privacy.html">Privacy</a></p>
  </footer>
  <button class="back-to-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>
  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>"""

def extract_meta(html):
    """Extract title, description from old HTML."""
    title = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html, re.IGNORECASE)
    category = re.search(r'class="hero-eyebrow">([^<]+)<', html)
    h1 = re.search(r'<h1[^>]*>([^<]+)<', html)
    
    return {
        "title": title.group(1) if title else "Article",
        "description": desc.group(1) if desc else "",
        "category": category.group(1) if category else "Article",
        "h1": h1.group(1) if h1 else "Article"
    }

print(f"Restoring {len(ARTICLES)} articles...\n")
restored = 0
skipped = 0
errors = 0

for i, filename in enumerate(ARTICLES):
    print(f"[{i+1}/{len(ARTICLES)}] {filename}")
    
    # Get current SHA
    try:
        current = api(f"https://api.github.com/repos/{REPO}/contents/articles/{filename}")
        current_sha = current["sha"]
    except Exception as e:
        print(f"  ERROR: Can't get current SHA: {e}")
        errors += 1
        continue
    
    # Get old content
    old_content = get_old_content(filename)
    if not old_content:
        print(f"  SKIPPED: no old content found")
        skipped += 1
        continue
    
    # Extract body and metadata
    body = extract_body(old_content)
    meta = extract_meta(old_content)
    
    if not body:
        print(f"  SKIPPED: could not extract article body")
        skipped += 1
        continue
    
    # Build new HTML
    new_html = make_article_html(filename, body, title=meta["title"], 
                                  description=meta["description"], category=meta["category"])
    
    if not new_html:
        print(f"  SKIPPED: failed to build HTML")
        skipped += 1
        continue
    
    # Push to GitHub
    try:
        result = put_file(f"articles/{filename}", new_html, current_sha, 
                         f"Restore article content: {meta['title']}")
        print(f"  ✓ Restored: {meta['title']}")
        restored += 1
    except Exception as e:
        print(f"  ERROR pushing: {e}")
        errors += 1
    
    time.sleep(0.5)  # Rate limit buffer

print(f"\n{'='*50}")
print(f"Restored: {restored}")
print(f"Skipped: {skipped}")
print(f"Errors: {errors}")
