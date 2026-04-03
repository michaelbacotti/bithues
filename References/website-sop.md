# Website Management SOP

**For Mike** — How to manage your websites

---

## Your 3 Websites

| Site | URL | What it is | Hosting |
|------|-----|------------|---------|
| Bithues Reading Lab | bithues.com | Book reviews and reading lab | **GitHub Pages** |
| Dependability Holdings | dependability.us | Investment company info | GitHub Pages |
| Succession Holding LLC | successionholdingllc.com | Real estate company info | GitHub Pages |

---

## Design Standard (2026-04-02 Update)

All three sites now share the same professional navy/gold design:

| Element | Value |
|---------|-------|
| Navy (primary bg) | `#0a1628` |
| Navy mid | `#132240` |
| Navy light | `#1e3358` |
| Gold accent | `#c8a96e` |
| Gold light | `#e2c99a` |
| Off-white bg | `#f5f6f8` |
| Heading font | Playfair Display |
| Body font | Inter |

### Standard Page Structure
1. **Nav** — Sticky navy bar, gold bottom border (2px solid), brand links to home, nav links in gray → gold on hover
2. **Hero** — Gradient navy background with subtle SVG pattern overlay, Playfair Display serif heading, gold eyebrow text
3. **Content sections** — Off-white background, Playfair Display section titles
4. **Cards** — White background, 3px gold top border, subtle shadow
5. **Footer** — Simple navy bar, Playfair brand name, copyright

### AdSense Tags (every page head)
```html
<meta name="google-adsense-account" content="ca-pub-9312870448453345" />
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
```

---

## Who Has the Keys

| Site | Source Code | DNS | Hosting | Bot Has Access |
|------|-----------|-----|---------|----------------|
| bithues.com | GitHub (michaelbacotti/bithues) | Cloudflare | **GitHub Pages** | ✅ Full |
| dependability.us | GitHub (michaelbacotti/dependability-us) | GoDaddy | GitHub Pages | ✅ Full |
| successionholdingllc.com | GitHub (michaelbacotti/succession-holding-llc) | Squarespace | GitHub Pages | ✅ Full |

---

## How to Update a Site

### The Fast Way (Bacotti Bot does it):
Just ask! Bot clones the repo, edits, and pushes. GitHub Pages auto-deploys in ~1 minute.

### The Manual Way:
1. Go to the GitHub repo
2. Edit the file
3. Commit changes
4. Site auto-updates within ~1 minute

---

## Adding a New Page

1. Ask Bacotti Bot to create it, OR
2. Create a new `.html` file in the GitHub repo
3. Copy the format of an existing page (use the navy/gold design standard above)
4. Link to it from the navigation or another page

---

## Google AdSense — How It Works

All 3 sites are set up for AdSense. Here's what that means:

- **ads.txt** — A file that tells Google "this site is authorized to show ads" ✅ All 3 have it
- **Ad script** — A small code in every page's `<head>` that lets Google show ads ✅ All 3 have it
- **Google approval** — After verifying ownership, Google starts showing ads automatically.

**Current status:** All 3 sites are verified and set up. Google is still processing data. Ads should start appearing within a few days.

---

## Google Search Console — Tracking Traffic

You can see who's visiting your sites at: https://search.google.com/search-console

Bacotti Bot can also check this for you.

---

## DNS — Who Points Where

| Domain | Registrar | DNS Records Point To |
|--------|-----------|---------------------|
| bithues.com | Cloudflare | GitHub Pages servers (185.199.108-111.153) — DNS only, NOT proxied |
| dependability.us | GoDaddy | GitHub Pages servers (A records) |
| successionholdingllc.com | Squarespace | GitHub Pages servers (A records) |

If you need to change DNS, go to the registrar listed above and update the records.

---

## ⚠️ Cloudflare Pages vs GitHub Pages

**bithues.com was on Cloudflare Pages but the build kept failing** (git submodule error). 
We migrated it to **GitHub Pages** on 2026-04-02.

**Current setup:**
- GitHub Pages is enabled on michaelbacotti/bithues
- DNS at Cloudflare points to GitHub Pages IPs (185.199.108-111.153)
- Cloudflare proxy is OFF (DNS only) — this is correct for GitHub Pages
- Future pushes to the bithues repo auto-deploy immediately

**Why this is better:** No build step, no Cloudflare Pages failures, simpler setup.

---

## Adding a New Domain/Site

1. **Buy the domain** — GoDaddy, Squarespace, Cloudflare, etc.
2. **Create a GitHub repo** — `michaelbacotti/your-site-name`
3. **Build the site** — Ask Bacotti Bot or build manually (use navy/gold design standard)
4. **Enable GitHub Pages** — Settings → Pages → Deploy from main branch, / (root)
5. **Set custom domain** — In GitHub Pages settings, add your domain
6. **Update DNS** — Point A/CNAME records at GitHub Pages IPs (DNS only, NOT proxied)
7. **Add ads.txt** — File with `google.com, pub-9312870448453345, DIRECT, f08c47fec0942fa0`
8. **Add AdSense script** — In every page's `<head>` (see tag above)
9. **Verify in Search Console** — Add the domain in GSC and confirm ownership

---

## Website Source Code Locations

| Site | Clone URL |
|------|----------|
| bithues | `https://github.com/michaelbacotti/bithues.git` |
| dependability | `https://github.com/michaelbacotti/dependability-us.git` |
| succession | `https://github.com/michaelbacotti/succession-holding-llc.git` |

---

## Quick Reference

| Item | Value |
|------|-------|
| **AdSense Publisher ID** | `pub-9312870448453345` (same for all sites) |
| **GitHub username** | michaelbacotti |
| **Dependability forecast page** | dependability.us/dependability-forecast.html |

---

_Last updated: 2026-04-02 — Added Cloudflare→GitHub Pages migration, navy/gold design standard_
