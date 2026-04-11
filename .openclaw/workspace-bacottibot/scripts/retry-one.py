#!/usr/bin/env python3
import base64, json, re, time
import urllib.request

GITHUB_TOKEN = "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"
REPO = "michaelbacotti/bithues"
BRANCH = "main"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

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
    body_match = re.search(r'<div class="article-body"[^>]*>(.*?)</div>\s*<footer', html_content, re.DOTALL)
    if body_match and len(body_match.group(1).strip()) > 100:
        return body_match.group(1).strip()
    ac_match = re.search(r'<!-- ARTICLE CONTENT -->(.*?)<footer', html_content, re.DOTALL)
    if ac_match and len(ac_match.group(1).strip()) > 100:
        return ac_match.group(1).strip()
    div_match = re.search(r'<div class="divider"></div>\s*(.*?)<footer', html_content, re.DOTALL)
    if div_match and len(div_match.group(1).strip()) > 100:
        return div_match.group(1).strip()
    old_format = re.search(r'</header>\s*(.*?)<footer', html_content, re.DOTALL)
    if old_format and len(old_format.group(1).strip()) > 200:
        body = old_format.group(1).strip()
        body = re.sub(r'<div class="toc">.*?</div>\s*', '', body, flags=re.DOTALL)
        return body
    return None

def extract_meta(html):
    title = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html, re.IGNORECASE)
    category = re.search(r'class="hero-eyebrow">([^<]+)<', html)
    h1 = re.search(r'<h1[^>]*>([^<]+)<', html)
    tag = re.search(r'<div class="tag">([^<]+)<', html)
    return {
        "title": title.group(1) if title else "Article",
        "description": desc.group(1) if desc else "",
        "category": category.group(1) if category else (tag.group(1) if tag else "Article"),
        "h1": h1.group(1) if h1 else "Article"
    }

def make_article_html(filename, body_content, title="", description="", category="Article"):
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

filename = "kids-reading-guide.html"
print(f"Retrying {filename}...")

# Get fresh SHA
current = api(f"https://api.github.com/repos/{REPO}/contents/articles/{filename}")
current_sha = current["sha"]
print(f"Current SHA: {current_sha[:8]}")

# Get old content - try the same commit found earlier (f5e2959)
commits = api(f"https://api.github.com/repos/{REPO}/commits?path=articles/{filename}&per_page=5")
for c in commits[:5]:
    try:
        contents = api(f"https://api.github.com/repos/{REPO}/contents/articles/{filename}?ref={c['sha']}")
        if isinstance(contents, dict) and contents.get("content"):
            raw = base64.b64decode(contents["content"]).decode("utf-8", errors="replace")
            if len(raw) > 5000:
                body = extract_body(raw)
                if body and len(body) > 500:
                    print(f"Found body in commit {c['sha'][:8]}: {len(body)} chars")
                    meta = extract_meta(raw)
                    new_html = make_article_html(filename, body, title=meta["title"],
                                                  description=meta["description"], category=meta["category"])
                    result = put_file(f"articles/{filename}", new_html, current_sha,
                                     f"Restore article content: {meta['title']}")
                    print(f"SUCCESS: {meta['title']}")
                    exit(0)
    except Exception as e:
        print(f"  Error with commit {c['sha'][:8]}: {e}")

print("FAILED - could not find body in any commit")
