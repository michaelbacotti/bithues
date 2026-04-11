import base64, json, sys

with open('/Users/mike/.openclaw/workspace-bacottibot/sitemap_new.xml', 'rb') as f:
    encoded = base64.b64encode(f.read()).decode()

# Write to temp file for inspection
with open('/Users/mike/.openclaw/workspace-bacottibot/sitemap_b64.txt', 'w') as f:
    f.write(encoded)

print(f"Encoded length: {len(encoded)}")
print(f"First 80 chars: {encoded[:80]}")