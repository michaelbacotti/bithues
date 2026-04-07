# Websites — Portfolio, Hosting & AdSense

## Website Portfolio

| Domain | GitHub Repo | Hosting | AdSense | Notes |
|--------|-----------|---------|---------|-------|
| **bithues.com** | michaelbacotti/bithues | **GitHub Pages** (switched from Cloudflare Pages 2026-04-02) | ✅ Ready | Was on Cloudflare Pages but build kept failing — migrated to GitHub Pages |
| **dependability.us** | michaelbacotti/dependability-us | GitHub Pages | ✅ Ready | DNS at GoDaddy |
| **successionholdingllc.com** | michaelbacotti/succession-holding-llc | GitHub Pages | ✅ Ready | DNS at Squarespace |

**Publisher ID (all sites):** `pub-9312870448453345`

## Design Standard (updated 2026-04-02)

All sites use the same navy/gold professional design:
- **Colors:** Navy #0a1628, Gold #c8a96e, Off-white #f5f6f8
- **Fonts:** Playfair Display (headings) + Inter (body)
- **Nav:** Sticky navy bar, gold bottom border, brand links to home
- **Hero:** Gradient navy with SVG pattern overlay
- **Cards:** White with gold top accent border
- **Footer:** Simple navy bar, Playfair brand, copyright

## Cloudflare Pages Note

- bithues.com was ON Cloudflare Pages but the build kept failing (git submodule error)
- Deleted Cloudflare Pages project, switched to GitHub Pages
- DNS now points directly to GitHub Pages IPs (185.199.108-111.153) with DNS-only (grey cloud)
- GitHub Pages is now enabled on the bithues repo — pushes auto-deploy

## Dependability Forecast Page

- URL: dependability.us/dependability-forecast.html
- Contains: Weekly/monthly SPX contract tables, bullish thesis, Wall Street targets, option spread strategies
- S&P data verified: Close April 1 2026: 6,575.32 | Morgan Stanley: 7,800 | Goldman: 7,600 | JPMorgan: 7,500 | Citi: 7,700 | Barclays: 7,400
- Nav has anchor links: Weekly, Monthly, Thesis, Levels, Global, Strategy

## Website SOP

See: `References/website-sop.md`

## Local Source Files

| Site | Local Path |
|------|-----------|
| bithues | `~/openclaw/workspace/icloud/Bacotti Bot/Website/bithues/` |
| dependability | `/tmp/dep-us/` (cloned from GitHub) |
| succession | `/tmp/succession-site/` (cloned from GitHub) |

---

_Last updated: 2026-04-03_
