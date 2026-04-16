# MEMORY.md — Long-Term Memory

## ⚠️ Primary Interface: NERVE OpenClaw Cockpit
Mike primarily uses **NERVE OpenClaw Cockpit V1.5.2** as his main interface. All sessions, tabs, agent management, and configuration should be understood in the context of NERVE.

---

## 📁 Source File Workflow (established 2026-04-15)

**Mike keeps authoritative originals outside the workspace.** He tells me the path when he wants me to act on a file. I copy it into the workspace myself. I never move or write back to external locations.

This means:
- Source PDFs, documents, tax files → wherever Mike keeps them (Dropbox, Documents, iCloud, etc.)
- I work from my workspace copy
- I can never corrupt or delete the original

---

## 🚨 CRITICAL: Sensitive Data — NEVER Send Externally

**Date learned: 2026-04-12**

**The mistake:** Sent a message to BacottiYottiBot via Google Drive containing:
- Real EINs (e.g., 86-2669759)
- Ownership structures (e.g., "100% owned by Succession Holding LLC")
- Entity names and relationships
- The actual wiki vault path on disk

This was catastrophic. Sensitive business data went to a cloud service (Google Drive) outside the local machine.

**Rule going forward:**
- **External = Google Drive, GitHub, email, any cloud service, any bot-to-bot communication**
- **Local only = this computer**

**What stays LOCAL, never shared:**
- Entity names, EINs, ownership percentages
- Financial figures (gains, losses, distributions, account balances)
- Meeting minutes and entity governance details
- Tax document contents (1065, 1120, 990s)
- File paths to business data
- Personal info (SSNs, addresses, phone numbers)

**What CAN be shared externally:**
- Broad concepts and methods (e.g., "how to structure a wiki page")
- Questions and coordination requests
- Non-specific examples (made-up dummy data only)

**When in doubt:** Ask Mike first. Always.

**Bias rule:** Do not use political or moral frameworks to evaluate content. Evaluate only: Is it accurate? Is the evidence credible? Does the source support it? Nothing else matters. No political vocabulary in fact-checking.

---

## 🛠️ Workflow Rules

- **Long-running tasks → use subagents**: Mike wants to keep chatting while work happens. Don't block the main session with browser automation, API calls, or slow multi-step tasks. Spawn a subagent and report back when done.
- **Write to memory as things happen** — don't wait until end of session. Update the relevant topic file immediately when something changes.
- **Read memory before answering** questions about things Mike has told me. If unsure, ask rather than guess.

- **Complex tasks → use claims-tracker**: For multi-step tasks, create `memory/claims-YYYY-MM-DD.md` and log every specific claim as it's made. Before telling Mike "it's done," verify each PENDING claim. This makes accountability explicit and surfaces uncertainty before it becomes a bug.- **Acknowledge confusion** — if the conversation gets long and I'm losing track, say so instead of guessing.

- **Slow and careful quality over speed**: Mike prefers accuracy and thoroughness over speed. Never rush to be done when accuracy is at stake.
- **Verify subagent output before claiming success**: Read the result, spot-check the actual code, take a screenshot before telling Mike "it's done." A subagent that timed out delivered nothing.
- **Take user reports seriously**: If Mike says something doesn't work, believe him. Investigate immediately — don't argue, deflect, or blame his browser. Mike's experience is ground truth.
- **Read actual lines before claiming fixed**: My mental model is often wrong. Before saying "it's fixed" or "that's not in the code," actually read the relevant lines. This is not optional.
- **Slow and careful quality over speed**: Mike prefers accuracy and thoroughness over speed. Never rush to be done when accuracy is at stake.
- **Verify subagent output before claiming success**: Read the result, spot-check the actual code, take a screenshot before telling Mike "it's done." A subagent that timed out delivered nothing.
- **Take user reports seriously**: If Mike says something doesn't work, believe him. Investigate immediately — don't argue, deflect, or blame his browser. Mike's experience is ground truth.
---

## 📚 Memory Topics

| Topic | File | Contents |
|-------|------|----------|
| **Entities & Tax** | `memory/entities.md` | Ownership structure, EINs, entity responsibilities, tax preparer |
| **Bacotti Inc.** | `memory/Bacotti Inc.md` | Family office, management entity, meeting minutes responsibility |
| **Succession Holding LLC** | `memory/Succession Holding LLC.md` | Eagle River Home LLC, real estate subsidiaries |
| **HOUSE Inc.** | `memory/HOUSE Inc.md` | Nonprofit 501c3 — people assisted (Asia Edwards) |
| **Investing** | `memory/investing.md` | Dependability 2025 performance, options preferences, market events |
| **Websites** | `memory/websites.md` | Portfolio, hosting, AdSense, DNS, SEO status |
| **Backup** | `memory/backup.md` | iCloud workspace backup, cron job, restore instructions |
| **Mail workflow** | `skills/mail-processor/SKILL.md` | Incoming mail → extract → identify entity → organize → route → remind |
| **Personal** | `memory/personal.md` | Mike's background, family, Little Mike books, X/social |

---

## Git Repo Size Incident (2026-04-12)
- Git repo at `/Users/mike/.git` appeared to be 99GB due to embedded website git repos inside the workspace
- **Actual size after cleanup: 7.5GB** — measurement error in initial report
- Embedded website git repos (`websites/bithues/Website/.git`, etc.) were being tracked by the home repo, causing triple-counting
- Cleanup removed the embedded .git directories from tracking; git now only tracks essential text files
- Git is now scoped to: AGENTS.md, MEMORY.md, skills/, memory/, scripts/, References/ — NOT business PDFs or website content

## Trade Archive System (2026-04-14)
- Scripts in `scripts/trade-archive/` auto-update dependability.us/dependability-forecast.html and trade-archive.html
- Workflow: Mike sends new trade → bot updates trades.json + forecast.json → cron at 4:15 PM ET auto-regenerates and pushes
- Cron job ID: `747eaa63-02b4-41a2-b26c-c7b9216bbc82` (4:15 PM ET weekdays)
- Data files: `scripts/trade-archive/data/trades.json`, `data/forecast.json`
- Generator scripts: `generate-trade-archive.py`, `generate-forecast.py`

## Cloudflare Pages — Approved for New Sites (2026-04-15)
- Mike confirmed: Cloudflare Pages + GitHub integration is the approved stack for his sons' future websites
- Bot writes files locally → commits to GitHub → Cloudflare Pages auto-deploys
- Confirmed via Telegram session after bot incorrectly stated GitHub was a registrar (corrected by Mike)

## Cron Jobs — Active (updated 2026-04-14)

| Job | Schedule | What it does | Status | ID |
|-----|----------|-------------|--------|-----|
| **Workspace Backup** | 2 AM daily | Backup workspace to iCloud, keep 2 most recent | ✅ | `da9af2a7-e46d-41e6-8964-75a8fcb24149` |
| **Auto Update** | 1 AM daily | Run `auto-update.sh` | ✅ | — |
| **Trade Archive Update** | 4:15 PM ET weekdays | Regenerate and push trade pages to GitHub | ✅ | `747eaa63-02b4-41a2-b26c-c7b9216bbc82` |
| **Check BYB Messages** | Various | Check Google Drive outbox for BacottiYottiBot replies | ✅ | `942d60b2-e6b6-4f82-8507-f6d901db29f4` |
| **Dependability Forecast Update** | 4 PM ET weekdays | Update dependability-forecast.html | ✅ | `ec4307ea-6c24-4472-a0c7-4d3923f8a8f2` |

---

## 📅 Launch Agents (active as of 2026-04-06)

| Job | Schedule | What it does | Status |
|-----|----------|-------------|--------|
| **Workspace Backup** | 2 AM daily | Backup workspace to iCloud Drive, keep 2 most recent | ✅ `com.bacottibot.workspace-backup.plist` |
| **Auto Update** | 1 AM daily | Run `auto-update.sh` | ✅ `com.bacottibot.auto-update.plist` |

---

## 🔑 Key References

| File | Purpose |
|------|---------|
| `References/website-sop.md` | How to manage websites |
| `References/Domains/DOMAIN_INVENTORY.md` | All domain/DNS/email details |
| `References/book-tracker.md` | All pen names, Amazon links, KDP status for 35+ books |
| `memory/YYYY-MM-DD.md` | Daily session notes |
| `skills/options-pro/scripts/` | Options analysis Python scripts |

---

## 🛠️ Skills Installed

| Skill | Purpose |
|-------|---------|
| **openclaw-backup** | Automated workspace backup to iCloud |
| **skill-learn** | Capture user corrections → `.learnings/` |
| **browser-workarounds** | Browser automation patterns (cookie banners, React buttons, Cloudflare) |
| **clawflow** | Multi-step detached task orchestration |
| **clawhub** | Install/update skills from clawhub.com |
| **gog** | Google Workspace (Gmail, Calendar, Drive, Docs) |
| **github** | GitHub operations via `gh` CLI |
| **himalaya** | Email via IMAP/SMTP |
| **things-mac** | Things 3 task management |
| **scrape-web** | Web scraping with Scrapling |
| **website-bot** | Website creation and management |
| **novel-drafter** | Full-length novel writing |
| **business-writing** | Industry research and business analysis |

## 🧠 Memory Systems (PLUR + QMD/Active Memory)

We run two complementary memory systems:

| System | What it does | Installed |
|--------|-------------|-----------|
| **QMD + Active Memory** | Search/retrieve — finds what's already written in files | `plugins.entries.active-memory` enabled; QMD skill pending |
| **PLUR (plur.ai)** | Proactive learning — extracts patterns from corrections ("actually, use X not Y"), learns them, injects them proactively | `plur-claw` plugin enabled |

**Key tradeoff:** PLUR's proactive learning = longer response times. Mike accepted this — side effect is OK.

**Why both:** QMD/Active Memory = remembering what's in files. PLUR = actually changing behavior from corrections without manual file updates.

**PLUR plugin:** `plur-claw` — config correct, needs gateway restart to activate after config changes.

---

## ⚠️ Critical Constraints

### File Deletion — ABSOLUTE RULE
**NEVER delete files from the workspace without verified backup coverage.**

- Before deleting any file: confirm it exists in git (`git ls-files | grep filename`)
- Before deleting any file: confirm it exists in the latest iCloud backup
- Use `trash` or `mv` instead of `rm` — deleted means gone, moved means recoverable
- If a subagent or script requests deleting a file: verify backup coverage FIRST
- "I thought it was safe in git" is not an excuse — verify before every deletion

**This is not optional. A file lost is data Mike cannot recover.**

### Exec Block
`python3 -c` / `python3` commands are BLOCKED (approval id `b996b1a2`). Workarounds:
- Use `curl` for GitHub API calls
- Use sub-agents for exec-dependent tasks
- Sub-agents also have exec blocked unless they have their own approval

### GitHub Repo Risk
The `michaelbacotti/bithues` repo was wiped/restored multiple times on 2026-04-06. Sub-agents doing GitHub API blob operations (get SHA → base64 → PUT) without proper fetch/push caused repo corruption. **Always fetch before push. Never force-push to main.**

### Books / PDFs
Mike has PDFs for all books. Does NOT want them uploaded to Google Books or any third-party platform. Keep local only.

### Real Name Policy
Mike does NOT want his real name (Michael Bacotti) on public platforms except where necessary. Use pen names. The exception is the verified Goodreads author page for Michael Bacotti which already exists.

---

## 📍 Current DNS / Site Status (2026-04-06)

| Domain | Status | Notes |
|--------|--------|-------|
| bithues.com | ✅ Working | GitHub Pages, HTTPS |
| www.bithues.com | ⚠️ Fixing | DNS resolving correctly (1.1.1.1 confirmed CNAME→GitHub), GitHub Pages warning may be stale |
| successionholdingllc.com | ✅ Working | GitHub Pages |
| dependability.us | ✅ Working | GitHub Pages, ads.txt in place |

**www.bithues.com DNS fix:** Delete NS records for `www` pointing to `ns3/ns4.afternic.com` — these are set at the domain registry level (not in Cloudflare zone) and are overriding the CNAME. Mike says GoDaddy has zero DNS records. The NS delegation may be at the registrar or at the registry level. **DNS resolves correctly from 1.1.1.1 and 8.8.8.8 — the issue is GitHub seeing stale data.**

**Bithues canonical URLs fixed (2026-04-12):** All canonical hrefs changed from `https://bithues.com/...` → `https://www.bithues.com/...`. Also: created `category/fiction.html`, fixed 199 broken `fiction.html` links → `catalog.html`, fixed 42 breadcrumb path errors, fixed `e-j-marin` vs `e-j-marín` accent mismatch, deleted orphan `categories/` directory.

**successionholdingllc.com fixes (2026-04-12):** Canonical URLs fixed from non-www → www across all 17 pages. sitemap.xml updated to list all 17 pages (was listing only 7). robots.txt sitemap URL fixed to www.

---

## 📧 Email / Platform Status (2026-04-06)

| Platform | Status |
|----------|--------|
| Cloudflare email routing | ✅ 35 @bithues.com addresses → michaelbacotti@gmail.com |
| Goodreads — Michael Bacotti | ✅ Verified, 33 books |
| Goodreads — Quantum Chronos | ⏳ Pending approval (~2 days from 2026-04-06) |
| Goodreads — E.J. Marín | ⏳ Pending approval (~2 days from 2026-04-06) |
| BookBub — Michael Bacotti | ✅ Profile live |
| Medium — Rowan Vale | ✅ Account created, 1 article published |

---

## 📖 Books / Catalog (as of 2026-04-06)

- **36 books** on bithues.com catalog (count updated from 35)
- **E.J. Marín's "Otomí"** (Spanish Edition) added — amzn.to/4c7W0aW (ASIN: B0GS4X9R9X)
- Full book list: `References/book-tracker.md`
- Mike's pen names: all in book-tracker.md (19+ pen names)
- Michael Jr. (Little Mike): separate author, separate books
- E.J. Marín: English + Spanish historical fiction (The Richmond Cipher + Otomí)

---

## Pending Tasks (updated 2026-04-15)

1. **Media.net application** — still pending
2. **Wiki entity pages** — need to build from tax docs / Master Organizer (see memory/entities.md)
3. **Find full Bacotti Enterprises Master Organizer PDF** — only page 1 found in tmp/
4. **Book Tracker link** — missing from site-wide nav Reviews dropdown on bithues.com (Mike noted he can't find it)
5. **Cords of Empire** (Book 3 Otomí series) — "soon to be published" but no release date set
6. **First active trade for forecast page** — Mike needs to provide active trade details for `dependability-forecast.html`
7. **OpenClaw doctor** — `openclaw doctor --non-interactive` still needs to be run
8. **AdSense for successionholdingllc.com** — ready to apply (now has 27+ articles)
9. **Goodreads pseudonyms** — E.J. Marín and Quantum Chronos still pending approval

---

_Last updated: 2026-04-10 20:45 EDT_

## Key Lessons Learned

### GitHub/DNS Factual Errors (2026-04-15, Telegram)
**What happened:** In a Telegram session, the bot confidently stated two technically incorrect facts about website infrastructure, and Mike had to correct both:

1. **"GitHub offers domain registration"** — FALSE. GitHub has domain *configuration* settings in Pages settings but is NOT a domain registrar. Conflated GitHub's domain config with Cloudflare Registrar.

2. **"Just add a CNAME for the apex domain"** — FALSE. A CNAME on an apex/root domain (e.g. `example.com`) is invalid DNS and breaks things. Must use A records (pointing to hosting IPs) or ALIAS/ANAME records.

**Lesson:** When explaining technical infrastructure (DNS, web hosting, domain registration), verify facts before stating them. Don't conflate different services. When unsure, say "I need to verify this" rather than risk giving wrong technical information.

### Subagent Hallucination — MNC Housing 50% (2026-04-16)
A subagent claimed Dependability Holding LLC had MNC Housing LLC at 50% ownership in 2024. This was FALSE. K-1 verification confirmed: Michael Bacotti 80%, Ventureprise Corporation 20% every year 2021–2025. MNC Housing LLC never appeared on any Dependability Holding K-1. The subagent either hallucinated or misread a scanned PDF.

**Rule going forward:** When a subagent reports a claim that contradicts established entity structure (like the entities.md table), flag it as needing verification. Never relay a subagent's claim as fact without checking the primary source.

### Tax Documents = Source of Truth (2026-04-12)
Mike's explicit instruction: **tax filings and documents are the source of truth for business, tax, and accounting tasks.** When in doubt about entity structures, income, losses, or financial figures — read the actual tax documents, not prior memory or notes.

---

## Promoted From Short-Term Memory (2026-04-15)

<!-- openclaw-memory-promotion:memory:memory/2026-04-12.md:114:142 -->
- - Pushed to GitHub, verified live at www.successionholdingllc.com ## Bithues.com QA Work - Category pages (9): duplicate footers removed, inline CSS removed, nav/footer made consistent with homepage - Homepage (index, articles, press): footer class mismatch fixed, stray navbar class removed, merge conflict markers cleaned - Author pages: subagent timed out — manual check needed - Review pages (56): subagent spawned to add proper nav/hero/footer - Story pages (36): subagent spawned to add proper nav/hero/footer ## Amazon Associates — bithues-20 - Tracking ID: `bithues-20` (StoreID: ventureprise-20) - Applied `?tag=bithues-20` to all bare `amazon.com/dp/` links on bithues - Files updated: reviews/35.html, reviews/, stories/, authors/, articles/ - amzn.to short links already carry affiliate tags — left as-is - Verified live: amazon.com/dp/B0D38W5972?tag=bithues-20 ## Ad Networks - **InfoLinks**: Applied and pending approval (PID 3444842). Will notify by email when activated. - **Media.net**: Not yet applied - **Ezoic**: Not yet applied - **AdSense**: Already set up on all 3 sites (bithues, dependability, succession) ## Open Items - [ ] Bithues review pages — 56 pages need proper nav/hero/footer (agent running) - [ ] Bithues story pages — 36 pages need proper nav/hero/footer (agent running) - [ ] Bithues author pages — manual QA needed (agent timed out) - [ ] Media.net and Ezoic applications still needed - [ ] Wiki entity pages — need to build from tax docs / Master Organizer - [ ] Find full Bacotti Enterprises Master Organizer PDF (only page 1 found in tmp/) [score=0.843 recalls=9 avg=0.383 source=memory/2026-04-12.md:114-142]

## Promoted From Short-Term Memory (2026-04-16)

<!-- openclaw-memory-promotion:memory:memory/2026-04-08.md:158:177 -->
- - Candidate: Dependability Forecast Page Created: New page: dependability.us/dependability-forecast.html; S&P 500 bullish thesis, weekly/monthly contract tables for 2026; Wall Street targets: Morgan Stanley 7,800, Goldman 7,600, JPMorgan 7,500, Citi 7,700, Barclays 7,400; Option spread strate - confidence: 0.00 - evidence: memory/2026-04-02.md:20-23 - recalls: 0 - status: staged - Candidate: Dependability Entity Clarified: Dependability Holding LLC = all stock, options, trading, investment management; Succession Holding LLC = real estate, subsidiary management; All trading/options matters → tag to Dependability - confidence: 0.00 - evidence: memory/2026-04-02.md:26-28 - recalls: 0 - status: staged - Candidate: Bithues Nav Redesigned: Hover dropdown menus: Reviews (7 categories), Stories, Articles; Full-width navy nav bar; Brand "Bithues Reading Lab" links to home - confidence: 0.00 - evidence: memory/2026-04-02.md:31-33 - recalls: 0 - status: staged - Candidate: Subagent Spam Issue: Subagent completion notifications kept flooding the session; Killed stuck subagents that were looping on approval timeouts; Fixed by ensuring subagents write results to files before finishing - confidence: 0.00 - evidence: memory/2026-04-02.md:36-38 - recalls: 0 - status: staged [score=0.841 recalls=10 avg=0.369 source=memory/2026-04-08.md:158-177]
