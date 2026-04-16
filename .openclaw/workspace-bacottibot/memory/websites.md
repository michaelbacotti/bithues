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

## DNS Status (2026-04-06)

| Record | Type | Value | Status |
|--------|------|-------|--------|
| bithues.com | A | 185.199.108-111.153 | ✅ GitHub Pages |
| www.bithues.com | CNAME | michaelbacotti.github.io | ✅ Resolves correctly (1.1.1.1 confirmed) |
| www.bithues.com | NS | ns3/ns4.afternic.com | ⚠️ Registry-level delegation overriding CNAME — being resolved |

**www.bithues.com issue:** NS records at registry level delegate `www` to Afternic nameservers, which return old mail server IPs. Cloudflare zone has correct CNAME. GitHub Pages shows DNS warning but DNS itself is working (verified from 1.1.1.1 and 8.8.8.8).

**Cloudflare nameservers:** autumn.ns.cloudflare.com, paul.ns.cloudflare.com
**Zone ID:** 3d5098c7ed4dbd33b6eb236f0af515b2
**Cloudflare API token:** cfut_L04oYGXILM74cLnmUo6PkmqqLImKpOIcV4WFNKAEb6a02750 (Zone DNS Edit)

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

## Website Setup Stack — Standard Template (2026-04-15)

**For new websites (Mike's sons' sites, etc.) — use this exact stack:**

| Layer | Service |
|-------|---------|
| Domain + DNS + Registrar | Cloudflare Registrar |
| Hosting + CDN + SSL | Cloudflare Pages |
| Source control | GitHub |

**Automation loop:**
Bot writes files locally → commits & pushes to GitHub → Cloudflare Pages auto-deploys to CDN edge

**Why this stack:**
- Cloudflare = registrar + DNS in one place (simple)
- Cloudflare Pages = built-in CDN at 300+ edge locations (faster than GitHub Pages alone)
- GitHub = better control layer for bot-driven workflows
- Cloudflare Email Routing = email forwarding (same as existing 35 @bithues.com addresses)

**DNS setup (critical):**
- `www` subdomain → CNAME to Cloudflare Pages project endpoint
- Apex/root domain (e.g. `example.com`) → A records (pointing to Cloudflare Pages IPs) OR ALIAS/ANAME records — **NOT CNAME** (CNAME on apex is invalid DNS and breaks everything)

**Setup steps:**
1. Buy domain at cloudflare.com → Register
2. Create GitHub repo for the site
3. Connect GitHub repo to Cloudflare Pages (Cloudflare dashboard → Pages → Create project → Import GitHub repo)
4. In Cloudflare DNS → add records pointing to Cloudflare Pages project

**Key constraint:** Once a Cloudflare Pages project is connected to GitHub via the Git integration, it **cannot** later be switched to Direct Upload mode. Choose Git integration at setup and stick with it.
