---
name: adsense
description: Fix AdSense ads.txt verification issues across bithues.com, dependability.us, and successionholdingllc.com. Use when AdSense reports "ads.txt not found" for any site, or when setting up AdSense for a new site.
metadata:
  {
    "openclaw": { "emoji": "📊" },
  }
---

# AdSense Skill

Fix and manage ads.txt and site verification for Google AdSense.

## CRITICAL RULE: Verify Live State FIRST

**When you suspect a site problem, ALWAYS check the live URL before touching files.**

```bash
# ALWAYS run these checks FIRST when debugging a site issue
curl -s "https://www.sitename.com/ads.txt"
curl -s -I "https://www.sitename.com/ads.txt"
```

**Never assume the workspace file matches what's live.** Files may not have been pushed, or may have been edited on the server.

---

## ads.txt Format

```
google.com, pub-[YOUR_PUBLISHER_ID], DIRECT, [CORRECT_TOKEN_FROM_ADSENSE_PANEL]
```

## Publisher ID
All sites: `pub-9312870448453345`

**The token (last field) changes per site and per AdSense account.** You MUST get the exact token from the Google AdSense dashboard for that specific site. Do NOT guess or copy from other sites.

---

## Step-by-Step: ads.txt "Not Found"

### Step 1: Check Google's AdSense panel
Go to AdSense → Sites → select the problem site. Google will show the EXACT ads.txt snippet for that site. Copy it exactly — including the token.

### Step 2: Check what's LIVE on the site
```bash
curl -s "https://www.sitename.com/ads.txt"
```
Compare live content to what Google shows. Are they different? Same?

### Step 3: Check HTTP status
```bash
curl -s -o /dev/null -w "%{http_code}" "https://www.sitename.com/ads.txt"
curl -s -o /dev/null -w "%{http_code}" "https://www.sitename.com/www/ads.txt"
```
- 200 = file exists and is reachable
- 404 = file not found — fix the hosting/deployment
- 301/302 = redirecting — Googlebot may not follow

### Step 4: Check www vs apex
Some hosts serve from www/ subdirectory. Check both:
```bash
curl -s "https://www.example.com/ads.txt"
curl -s "https://example.com/ads.txt"
curl -s -I "https://www.example.com/ads.txt"
```

### Step 5: Fix workspace files
- Only edit workspace files AFTER knowing what's live
- Use the EXACT token Google shows for THAT site
- Push to GitHub and wait for GitHub Pages to rebuild

### Step 6: Check meta tag (site verification)
Google may also ask for a `<meta>` tag in `<head>`. Check:
```bash
grep -l "google-adsense-account\|google-adsase-account" /path/to/site/*.html
```
**Watch for typos:** `google-adsase-account` is wrong — should be `google-adsense-account`

### Step 7: Wait for re-crawl
Google caches site state. After fixing:
- Wait 30-60 minutes for GitHub Pages to rebuild
- Googlebot usually re-crawls within 24-48 hours
- Can request re-verification from AdSense dashboard

---

## Common Issues & Fixes

### "Not Found" but curl shows 200
→ Googlebot cached an older crawl. Fix is deployed — wait for re-crawl.

### Wrong token in live file
→ Update workspace file with correct token from AdSense panel. Push. Wait.

### 301 redirect on www/ or apex
→ Add ads.txt at BOTH URLs, or configure host to serve from one canonical URL.

### Typo in meta tag name
→ Common typo: `google-adsase-account` (missing 'n'). Fix to `google-adsense-account`.

### File missing from www/ subdirectory
→ Some hosts serve from www/ subdirectory. Check `www/ads.txt` specifically.

---

## Site Status (as of April 17, 2026)

### successionholdingllc.com
- **ads.txt token (per AdSense panel):** `f08c47fec0942fa0`
- **Workspace:** `/Users/mike/.openclaw/workspace-bacottibot/websites/succession-holding-llc/`
- **Files:** `ads.txt`, `www/ads.txt`
- **Issue fixed Apr 17:** Meta tag typo (`google-adsase-account`) in `llc-tax-benefits.html`

### bithues.com
- **ads.txt token (per AdSense panel):** `f08c47fec0942fa0`
- **Workspace:** `/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues/`
- **Files:** `ads.txt`
- **Host:** GitHub Pages (apex CNAME, no www redirect)

### dependability.us
- **ads.txt token (per AdSense panel):** `f08c47fec0942fa0`
- **Workspace:** `/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/dependability-us/`
- **Files:** `ads.txt`, `www/ads.txt`
- **Host:** GitHub Pages

---

## Verification Checklist (before declaring "fixed")

```bash
# 1. Check Google AdSense panel — get exact snippet
# 2. Check live URL
curl -s "https://www.sitename.com/ads.txt"
# 3. Compare — do they match?
# 4. Check HTTP status
curl -s -o /dev/null -w "%{http_code}" "https://www.sitename.com/ads.txt"
# 5. Check meta tag on key pages
grep -l "google-adsense-account" /path/to/site/*.html | wc -l
```

---

## Key Lessons (from April 17, 2026 incident)

1. **Live state first, files second.** Always curl the live URL before diagnosing.
2. **Each site has its own token.** Don't copy tokens between sites.
3. **Workspace ≠ Live site.** GitHub Pages may not have rebuilt, or file may have been edited on server.
4. **Meta tag verification is separate from ads.txt.** Both may be needed.
5. **Watch for typos in meta tag names** — `google-adsase-account` instead of `google-adsense-account`.
