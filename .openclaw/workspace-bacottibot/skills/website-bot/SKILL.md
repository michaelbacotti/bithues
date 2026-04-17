# SKILL.md — website-bot

## What it does
Creates, updates, and manages websites using HTML/CSS/JavaScript, with GitHub Pages deployment support.

## When to use
- Creating new websites from scratch
- Updating existing website content
- Working with HTML, CSS, JavaScript files
- GitHub Pages deployment
- Website troubleshooting and bug fixes

## Live Site Debugging (CRITICAL)

**When debugging a site issue, check the LIVE URL FIRST — before touching files.**

```bash
# ALWAYS verify what's actually live before diagnosing
curl -s "https://www.sitename.com/problem-page.html"
curl -s -o /dev/null -w "%{http_code}" "https://www.sitename.com/problem-page.html"
```

**Never assume the workspace matches the live site.** Files may not have been pushed, GitHub Pages may not have rebuilt, or the hosting may differ from what you expect.

**The correct order:**
1. Curl the live URL — verify actual state
2. Compare to expected state
3. Diagnose the cause
4. Fix workspace files
5. Push to GitHub
6. Verify live site changed

**When NOT to use live fetches for debugging:** Content proofreading, checking local formatting, comparing file versions. Use live fetches ONLY when the user reports a site problem and you need to know what's actually deployed.

## When NOT to use
- For content proofreading/bug checking of local files — use LOCAL files
- Tasks requiring server-side processing

## Inputs
- Project name and specifications
- For site debugging: local files AND live URLs — verify live state first

## Outputs
- HTML, CSS, JavaScript files
- GitHub repo creation and GitHub Pages deployment

## Cost / Risk notes
Writes to workspace and GitHub. For site issues: always check live URL first.
