---
name: lightpanda
version: 1.0.0
description: Fast headless browser for web scraping, screenshots, and dynamic content extraction. Built on Lightpanda (Zig-based, 11x faster than Chrome, 9x less memory). Use when OpenClaw's browser tool is too heavy, or for pages that need JavaScript execution without the Chrome overhead.
metadata:
  author: bacottibot
  source: lightpanda.io + OpenClaw skill
---

# Lightpanda Browser Skill

A fast, lightweight headless browser for automation and web scraping. **11x faster** than Chrome, **9x less memory**. No graphical rendering — purely for data extraction.

## Install (already done)
```bash
# Lightpanda binary is at ~/.local/bin/lightpanda
# playwright-core is in the workspace node_modules
```

## Quick Start

### Start the browser
```bash
bash skills/lightpanda/scripts/start.sh [port=9222]
```

### Stop the browser
```bash
lsof -i :9222 | awk 'NR>1{print $2}' | xargs kill
```

### One-shot screenshot
```bash
bash skills/lightpanda/scripts/browse.sh screenshot https://example.com /tmp/shot.png
```

### One-shot content extract
```bash
bash skills/lightpanda/scripts/browse.sh extract https://example.com body
```

### Get page title only
```bash
bash skills/lightpanda/scripts/browse.sh title https://example.com
```

## Architecture

```
Lightpanda process (port 9222)
    └── CDP websocket (1 connection at a time)
        └── Playwright-core (Node.js)
            ├── Context (isolated)
            │   └── Page (navigate, extract, screenshot)
            └── [Close after each task]
```

**Important constraints:**
- Only **1 CDP connection** per Lightpanda process
- Only **1 context + 1 page** per connection
- Browser resets state on connection close — reconnect for next task
- Lightpanda starts in ~300ms (vs Chrome's 2-5s) — restart-per-task is fast
- For **multiple simultaneous** navigations, run multiple Lightpanda processes on different ports

## When to Use Lightpanda vs Built-in Browser Tool

| Task | Lightpanda | OpenClaw Browser Tool |
|------|-----------|----------------------|
| Simple page fetch | ❌ use `web_fetch` | - |
| Web search | ❌ use `web_search` | - |
| JS-heavy / SPA | ✅ | ✅ |
| Login-protected pages | ✅ | ✅ |
| Screenshot | ✅ fast | ✅ |
| Form filling | ✅ | ✅ |
| Multi-tab automation | ❌ | ✅ |
| Google-dependent | ❌ (blocked) | ✅ (use DuckDuckGo) |

## Important Notes

1. **Google is blocked** — Lightpanda's fingerprint is detected. Use **DuckDuckGo** (`duckduckgo.com`) for searches.
2. **Fast startup** — Each task can start a fresh Lightpanda process. ~300ms startup + ~1s page load ≈ 1.5s total vs Chrome's 5-10s.
3. **State resets** — Each new connection starts clean (no cookies, no cache). Good for privacy and isolation.
4. **JS execution** — Lightpanda executes JavaScript, suitable for SPAs and dynamic content.

## Scripts

- `scripts/start.sh [port]` — Start Lightpanda server
- `scripts/screenshot.js <url> [output] [port]` — Take screenshot
- `scripts/extract.js <url> [selector=body] [port]` — Extract page content
- `scripts/title.js <url> [port]` — Get page title
- `scripts/browse.sh` — Convenience wrapper (start + action)

## Use Cases

- **Research on JS-heavy sites** — pages that need JavaScript to render
- **Screenshots** — fast, lightweight, no display required
- **Scraping dynamic content** — articles behind lazy-load, infinite scroll
- **Form extraction** — follow links, fill forms, submit
- **Price/inventory monitoring** — lightweight alternative to full Chrome

## Troubleshooting

**"Connection refused"**
→ Lightpanda not running. Run `bash scripts/start.sh`

**"Target page closed"**
→ Lightpanda process crashed. Restart: `lsof -i :9222 | awk 'NR>1{print $2}' | xargs kill; bash start.sh`

**Slow on first run**
→ playwright-core connecting for first time. Normal — subsequent uses are fast.

**Google blocks access**
→ Expected. Use DuckDuckGo instead.
