#!/usr/bin/env python3
import json, base64, sys, os

TOKEN = "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"
REPO = "michaelbacotti/bithues"
BASE_URL = "https://api.github.com/repos/" + REPO + "/contents"

def push_file(path, content, sha, message):
    url = f"{BASE_URL}/{path}"
    encoded = base64.b64encode(content.encode()).decode()
    payload = json.dumps({"message": message, "sha": sha, "content": encoded})
    
    with open("/tmp/push_payload.json", "w") as f:
        f.write(payload)
    
    import urllib.request
    req = urllib.request.Request(url, data=payload.encode(), method="PUT")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print(f"OK: {path}")
            return result.get("content", {}).get("sha")
    except Exception as e:
        print(f"ERROR {path}: {e}")
        return None

articles = {
    "articles/best-books-spring-2026.html": ("c8ecbdb04230859e6f434f63223312f806d63d3d", "Restore spring 2026 books article content"),
    "articles/hopepunk-fiction.html": ("c8ecbdb04230859e6f434f63223312f806d63d3d", "Restore hopepunk-fiction.html article content"),
    "articles/best-sci-fi-2026.html": ("c8ecbdb04230859e6f434f63223312f806d63d3d", "Restore best-sci-fi-2026 article content"),
    "articles/meet-indie-authors.html": ("c8ecbdb04230859e6f434f63223312f806d63d3d", "Restore meet-indie-authors article content"),
    "articles/books-for-dad-gift-guide.html": ("c8ecbdb04230859e6f434f63223312f806d63d3d", "Restore books-for-dad gift guide article"),
    "articles/why-indie-authors-rising.html": ("c8ecbdb04230859e6f434f63223312f806d63d3d", "Restore why-indie-authors-rising article content"),
    "articles/best-books-summer-2026.html": ("c8ecbdb04230859e6f434f63223312f806d63d3d", "Restore summer 2026 books article content"),
}

workspace = "/Users/mike/.openclaw/workspace-bacottibot"
for path, (sha, msg) in articles.items():
    filepath = os.path.join(workspace, path)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            content = f.read()
        push_file(path, content, sha, msg)
    else:
        print(f"MISSING: {filepath}")
