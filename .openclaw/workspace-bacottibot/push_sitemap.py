import base64, json, urllib.request

TOKEN = "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"
SHA = "13bf768d7234f63777d30527a8af9560b3ee2295"
REPO = "michaelbacotti/bithues"

with open('/Users/mike/.openclaw/workspace-bacottibot/sitemap_new.xml', 'rb') as f:
    content_b64 = base64.b64encode(f.read()).decode()

payload = json.dumps({
    "message": "Update sitemap.xml with current HTML file list",
    "content": content_b64,
    "sha": SHA
})

req = urllib.request.Request(
    f"https://api.github.com/repos/{REPO}/contents/sitemap.xml",
    data=payload.encode(),
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28"
    },
    method="PUT"
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.load(resp)
        print(f"SUCCESS! SHA: {result.get('commit', {}).get('sha', 'N/A')}")
        print(f"URL: {result.get('content', {}).get('html_url', 'N/A')}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP {e.code}: {body}")