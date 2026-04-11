import urllib.request, json
with open('/Users/mike/.openclaw/workspace-bacottibot/.gh_token') as f:
    TOKEN = f.read().strip()
REPO = "michaelbacotti/bithues"
BROKEN = ["complete-fantasy-encyclopedia.html","thriller-mystery-guide.html","ultimate-sci-fi-guide.html","books-like-physics-of-time.html","books-like-project-hail-mary.html","business-leadership-guide.html","fantasy-for-beginners.html","horror-for-beginners.html","memoir-biography-guide.html"]
for filename in BROKEN:
    url = f"https://api.github.com/repos/{REPO}/commits?path=articles/{filename}&per_page=5"
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    print(f"{filename}:")
    for c in data:
        print(f"  {c['sha']} - {c['commit']['message'][:60]}")
