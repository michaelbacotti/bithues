# MEMORY.md — Long-Term Memory

## ⚠️ Primary Interface: NERVE OpenClaw Cockpit
Mike primarily uses **NERVE OpenClaw Cockpit V1.5.2** as his main interface. All sessions, tabs, agent management, and configuration should be understood in the context of NERVE.

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
| **Personal** | `memory/personal.md` | Mike's background, family, Little Mike books, X/social |

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

---

## ⚠️ Critical Constraints

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

## Pending Tasks (from 2026-04-06)

1. **www.bithues.com GitHub Pages** — GitHub still showing warning; DNS is correct, just needs GitHub to re-verify
2. **Goodreads books** — claim all 35 books for Threshold Publishing author profile (need pseudonyms approved first)
3. **Push browser-workarounds skill** to GitHub (exec blocked)
4. **Enable Google Calendar API** at console.developers.google.com (for gog)
5. **Comet browser CDP test** — run with `--remote-debugging-port=9222` to see if it supports Chrome DevTools Protocol

---

_Last updated: 2026-04-06 20:45 EDT_
