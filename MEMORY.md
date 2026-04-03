# MEMORY.md — Long-Term Memory

## 🏢 Business Entities (Source: Tax Files > All Other Sources)

**⚠️ TAX FILES ARE FINAL AUTHORITY.** When tax files contradict any other document, trust the tax file.

### Ownership Structure
```
Bacotti Family Trust
└── Succession Holding LLC (Michael 50%, Michaella 50%)
    ├── 100% of Bacotti Inc. (formerly Ventureprise Corp, EIN 86-2669759)
    │   └── 20% of Dependability Holding LLC
    └── Partial owner of MNC Housing LLC
└── Other entity (80% of Dependability Holding LLC — identity TBD)
```

### Tax-Verified Entities
| Entity | EIN | Ownership | Tax Form |
|--------|-----|-----------|----------|
| **Dependability Holding, LLC** | 86-2606053 | Michael Bacotti 80%, Bacotti Inc. 20% | 1065 |
| **Succession Holding, LLC** | 86-2556181 | Michael Bacotti 50%, Michaella Bacotti 50% | 1065 |
| **MNC Housing, LLC** | 87-2708822 | Dissolving July 2025 (final return) | 1120 |
| **HOUSE Inc.** | 87-1948148 | 501c3 Nonprofit | 990 |
| **Bacotti Inc.** | 86-2669759 | 100% owned by Succession Holding LLC | — |

### Entity Responsibilities
| Entity | What it handles |
|--------|---------------|
| **Dependability Holding LLC** | All stock & options trading, investment management, capital markets |
| **Succession Holding LLC** | Real estate investments, subsidiary management |
| **Bacotti Inc.** | Parent of Dependability (20% ownership), general corporate |
| **HOUSE Inc.** | Nonprofit, 501c3 |

**⚠️ All stock/options/trading matters** → Tag to Dependability Holding → Add to: dependability.us website, meeting minutes, trading SOPs, skills

### Key Facts from 2023-2024 Tax Returns
- **Dependability:** $29k loan FROM Bacotti Inc. | $12k guaranteed payments to Bacotti Inc.
- **Succession:** Real estate holding, formed 02/28/2021; owns Bacotti Inc. 100%
- **MNC Housing:** Final return filed, dissolution July 2025
- **HOUSE:** 2023 receipts $3,111 | Expenses $5,002 | Assets $16,742 cash

### 2025 Performance Highlights (Dependability Holding)
- **Net realized gain:** $50,927.22 on $106,344.82 capital = **47.89% return**
- Beat S&P 500 (17.88%), Russell 2000 (12.81%), Nasdaq-100 (20.17%)
- **Wash-sale loss carryforward (tax asset):** $220,714.75
- **Estimated tax savings:** $25,000–$40,000 from loss harvesting

---

## 🌐 Website Portfolio

| Domain | GitHub Repo | Hosting | AdSense | Notes |
|--------|-----------|---------|---------|-------|
| **bithues.com** | michaelbacotti/bithues | **GitHub Pages** (switched from Cloudflare Pages 2026-04-02) | ✅ Ready | Was on Cloudflare Pages but build kept failing — migrated to GitHub Pages |
| **dependability.us** | michaelbacotti/dependability-us | GitHub Pages | ✅ Ready | DNS at GoDaddy |
| **successionholdingllc.com** | michaelbacotti/succession-holding-llc | GitHub Pages | ✅ Ready | DNS at Squarespace |

**Publisher ID (all sites):** `pub-9312870448453345`

### Design Standard (updated 2026-04-02)
All sites now use the same navy/gold professional design:
- **Colors:** Navy #0a1628, Gold #c8a96e, Off-white #f5f6f8
- **Fonts:** Playfair Display (headings) + Inter (body)
- **Nav:** Sticky navy bar, gold bottom border, brand links to home
- **Hero:** Gradient navy with SVG pattern overlay
- **Cards:** White with gold top accent border
- **Footer:** Simple navy bar, Playfair brand, copyright

### Website SOP
See: `References/website-sop.md`

### Cloudflare Pages Note
- bithues.com was ON Cloudflare Pages but the build kept failing (git submodule error)
- Deleted Cloudflare Pages project, switched to GitHub Pages
- DNS now points directly to GitHub Pages IPs (185.199.108-111.153) with DNS-only (grey cloud)
- GitHub Pages is now enabled on the bithues repo — pushes auto-deploy

### Dependability Forecast Page
- URL: dependability.us/dependability-forecast.html
- Contains: Weekly/monthly SPX contract tables, bullish thesis, Wall Street targets, option spread strategies
- S&P data verified: Close April 1 2026: 6,575.32 | Morgan Stanley: 7,800 | Goldman: 7,600 | JPMorgan: 7,500 | Citi: 7,700 | Barclays: 7,400
- Nav has anchor links: Weekly, Monthly, Thesis, Levels, Global, Strategy

### Option Spread Preferences (Mike's)
- Almost always use vertical or diagonal spreads — NOT naked long options
- Will buy 2 calls and sell 1 (ratio spread)
- Always sell an option so theta works FOR us, not against
- Avoid pure long calls/puts due to time decay

---

## 📂 Website Source Files (Local Workspace)
| Site | Local Path |
|------|-----------|
| bithues | `~/openclaw/workspace/icloud/Bacotti Bot/Website/bithues/` |
| dependability | `/tmp/dep-us/` (cloned from GitHub) |
| succession | `/tmp/succession-site/` (cloned from GitHub) |

---

## 📧 Email Access
- **Gmail:** michaelbacotti@gmail.com — connected via gog (read, send, calendar)
- **iCloud:** michaelbacotti@mac.com — connected via himalaya (read, send)

---

## 🏥 Healthcare
- **Military Service:** Retired Army Captain — eligible for VA healthcare
- **MyChart:** https://mychart.bilh.org/MyChart-BILH/Home/
- **Neurologist:** Uladzimir Luchanok, MD (covering) / Jeffrey D Rind, MD (Botox for migraines)

---

## 🛠️ Skills & Tools
| Skill | Purpose | Location |
|-------|---------|----------|
| **Options Pro** | Stock/options analysis, Greeks, spread strategies (for Dependability) | `skills/options-pro/` |
| **Nightly Cleanup** | Auto-runs at 1 AM to archive sessions, update memory, clean temp | `skills/nightly-cleanup/` |
| **Stock Market Pro** | Stock market analysis via ClawHub | `skills/stock-market-pro/` |
| **Polyclaw** | Portfolio tracking | `skills/polyclaw/` |
| **x-social-manager** | Daily X engagement — browser-based posting, replying, liking, quote-posting | `skills/x-social-manager/` |
| Skill | Purpose | Location |
|-------|---------|----------|
| **Options Pro** | Stock/options analysis, Greeks, spread strategies (for Dependability) | `skills/options-pro/` |
| **Nightly Cleanup** | Auto-runs at 1 AM to archive sessions, update memory, clean temp | `skills/nightly-cleanup/` |
| **Stock Market Pro** | Stock market analysis via ClawHub | `skills/stock-market-pro/` |
| **Polyclaw** | Portfolio tracking | `skills/polyclaw/` |

---

## 📅 Cron Jobs
| Job | Schedule | What it does |
|-----|----------|-------------|
| **Nightly Cleanup** | 1 AM daily | Archive sessions, update memory/YYYY-MM-DD.md, push learnings to MEMORY.md, clean temp files |
| **Nightly Memory** | 1 AM daily | Update daily memory file with key events |

---

## 📁 Key Files
| File | Purpose |
|------|---------|
| `References/website-sop.md` | How to manage websites (for Mike) |
| `References/Domains/DOMAIN_INVENTORY.md` | All domain/DNS/email details |
| `memory/YYYY-MM-DD.md` | Daily session notes |
| `skills/options-pro/scripts/` | Options analysis Python scripts |

---

## 🧠 Lessons Learned
- **Website SOP**: GitHub/Cloudflare deployment — edits → commit → push → auto-deploy
- **Cloudflare Pages failure**: bithues build failed due to git submodule error — switched to GitHub Pages instead
- **Git push via subagent**: Always use GIT_DIR and GIT_WORK_TREE env vars to isolate from workspace git repo
- **Subagent file writes**: Instruct subagents to write results to files before finishing
- **Design consistency**: All 3 sites now share the same navy/gold template — keep this consistent going forward
- **Nav brand links**: Brand name in nav should be `<a href="index.html">` with `text-decoration: none`
- **Python over bash**: For cross-platform scripts, use Python not bash (macOS bash 3.2 lacks associative arrays)

---

## 🔑 Tax Preparer
- **Christia Thompson** — Senior Tax Associate, Anderson Advisors
- 500 N Rainbow Blvd. Suite 110, Las Vegas, NV 89107
- P: 702.628.5236 | F: 702.664.0545
- Handling: Dependability Holding LLC, Succession Holding LLC, Bacotti Trust
- HOUSE Inc. — Mike handles directly

---

## X (Twitter) Integration ✅
- **xurl CLI** — authenticated as @SpaceCat_SC001
- Can post, reply, quote, search, like, repost, follow, DMs, media upload
- **NOTE: X API credits exhausted** — search and other API calls return errors. Use **browser-based** approach for engagement.
- Browser profile: `openclaw`

## 📚 Little Mike Books
- **Author: Mike's son** (NOT Mike himself — important for correct attribution)
- Books: Little Mike: Fun at the Beach, Little Mike: Learns to Fly, Little Mike: Builds a Robot, Microbiology ABC's
- X account: **@LittleMikeReads** (dormant since March 2025 — opportunity to grow)
- Website: **littlemikebooks.com**
- Amazon link: amzn.to/4sZxujl

## 🐦 X Engagement Strategy (@SpaceCat_SC001)
### What works
- **Science/physics posts** get the most engagement (38-1555 views): quantum mechanics, block universe, time dilation
- **Finance/markets** posts get moderate engagement
- **Book promo posts** (standalone) get almost NO traction — avoid standalone book ads
- **Quote-posting high performers** is effective

### Engagement rules
1. **NEVER claim Mike is the author of Little Mike books** — his son wrote them
2. **No links in replies** — comes across as spammy, X algorithm penalizes links
3. **Soft sell** — mention @LittleMikeReads (not links) in replies
4. **No Amazon/website links** — put them in profile bio or pinned post only
5. **Engage with relevant posts** (science, tech, finance) — not just book promotion

### Topics to engage on (Mike's interests)
- Physics/quantum mechanics
- Finance/markets/investing
- Technology/AI
- Geopolitics
- Space/science

### Accounts to watch
- @zerohedge, @BillAckman (Mike quotes/reposts these)
- Book-related accounts: @hmdpublishing, @i_s_a_tokyo, @kneanews, @publicschoolext

### Daily engagement workflow
- Find 2-3 relevant posts (browser search on x.com)
- Reply with helpful, natural-sounding comments
- Mention @LittleMikeReads when relevant
- Like the post after replying

## Skill: x-social-manager
- Purpose: Daily X engagement (browser-based, no API needed)
- Location: `skills/x-social-manager/`
- Status: In development (created 2026-04-02)

---

_Last updated: 2026-04-02_
