# Learnings

## 2026-04-06 — Session Hygiene & Long Conversation Failures

**Problem:** After 20+ turns in a single session, assistant started contradicting things user already said (GoDaddy records deleted, PDFs not wanted, etc.). Memory degraded significantly.

**Root cause:** No checkpoint system for long sessions. No trigger to re-read memory mid-conversation.

**What to do differently:**
1. For sessions > 15 turns, write midpoint checkpoint to memory
2. If user says "memory is bad" → apply conversation-hygiene skill immediately
3. Don't rely on context window for critical facts — write to memory as they happen
4. When starting a new topic in a long session, explicitly re-read relevant memory file first

---

## 2026-04-06 — GitHub Repo Wiped (3 Times)

**Problem:** `michaelbacotti/bithues` repo lost all commits and content 3 times during automated workflows.

**Root cause:** Sub-agents doing `git push --force`, or pushing without `fetch` first (stale parent SHA). Also: creating files via GitHub API in /tmp without pushing, then force-pushing from workspace to "restore."

**What to do differently:**
1. NEVER force-push to main
2. ALWAYS `git fetch origin` before push
3. Sub-agents should clone fresh or fetch before making changes
4. Use github-safe-push skill for all git operations
5. Never do `git push --force` regardless of what a sub-agent reports

---

## 2026-04-06 — DNS Misdiagnosis (www.bithues.com)

**Problem:** Spent 45+ minutes troubleshooting www.bithues.com DNS. Told Mike to delete A records that didn't exist. Actual problem was GitHub Pages settings missing www as a custom domain.

**Root cause:** Started with wrong diagnostic path (looked at Cloudflare zone records instead of checking what GitHub Pages itself was configured for). Confused zone-level DNS with registry-level NS delegation. Didn't use `dig ns www.bithues.com` early.

**What to do differently:**
1. When GitHub Pages shows "DNS check unsuccessful" → FIRST check if www is added in GitHub Pages settings (Settings → Pages → Custom domain), not just DNS
2. Run `dig ns www.domain.com` to check for registry-level NS delegation BEFORE assuming zone records are wrong
3. Use dns-diagnostic skill for all DNS troubleshooting
4. Public resolvers (1.1.1.1, 8.8.8.8) showing correct values + GitHub still showing error = GitHub's cached data, not a real DNS problem

---

## 2026-04-06 — Sub-agent Timeout Pattern

**Problem:** Sub-agents consistently timing out on GitHub API blob workflows (get SHA → base64 encode → PUT). 10+ attempts across multiple task names.

**Root cause:** Multi-step API calls in sub-agents exceed timeout window. Each step is a separate API call. Total time exceeds what isolated sessions allow.

**What to do differently:**
1. For GitHub API file operations: write a single Python script that does ALL steps in one exec call
2. Use `requests` library in Python for API calls (faster than curl in sub-agent)
3. Or: use main session for API calls, don't spawn sub-agent
4. Don't retry same failed approach 3+ times — write it as "blocked" in memory and tell Mike

---

## 2026-04-06 — Cloudflare Email Routing Side Effects

**Problem:** Cloudflare Email Routing automatically added NS records and A records that broke www subdomain routing to GitHub Pages.

**What to know:**
- Email Routing can add A records for `www` pointing to mail server IPs (76.223.54.146, 13.248.169.48)
- Email Routing can add NS records for `www` to Afternic/other platforms
- These are added at the REGISTRY level, not visible in the Cloudflare zone DNS panel
- When enabling email routing: check for these side effects immediately after

---

## 2026-04-04 — Google Books PDF Upload

**Confirmed:** Mike does NOT want PDFs uploaded to Google Books or any third-party platform. Keep all PDFs local. This was stated multiple times. Do not offer Google Books upload again.

---

## 2026-04-04 — KDP Excel Royalty Estimator

**Decision:** Built an Excel file with 10 sheets for KDP royalty estimation. Mike said the data is already in book-tracker.md and the Excel was unnecessary complexity. Keep estimates in the spreadsheet only if Mike specifically asks. Don't build elaborate tracking tools unless requested.

---

_Last updated: 2026-04-06 20:50 EDT_
