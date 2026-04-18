# SKILL.md — robotics-deploy

## Purpose

Deploy and update the Exabytes robotics team dashboard to Cloudflare Pages.

---

## Team Info

- **Team:** Exabytes | **Number:** 603E | **Org:** RIZE Robotics
- **Dashboard:** https://exabytes.pages.dev
- **Source file:** `memory/robotics-dashboard.html`
- **Deploy folder:** `websites/exabytes/`

---

## Deploy Command

```bash
cp memory/robotics-dashboard.html websites/exabytes/index.html && wrangler pages deploy websites/exabytes --project-name=exabytes
```

Or from workspace root:

```bash
cp memory/robotics-dashboard.html websites/exabytes/index.html && cd websites/exabytes && wrangler pages deploy . --project-name=exabytes
```

---

## First-Time Setup (already done)

1. `wrangler login` — authenticated with Cloudflare OAuth
2. `wrangler pages project create exabytes --production-branch main`
3. First deploy: `wrangler pages deploy websites/exabytes --project-name=exabytes`

**URL:** https://exabytes.pages.dev

---

## Prerequisites

- Wrangler CLI installed: `npm install -g wrangler`
- Cloudflare account authenticated: `wrangler login`
- Internet connection (deployment is to Cloudflare edge)

---

## When to Deploy

- After Mike confirms any corrections to the dashboard are final
- When competition results change or new awards are earned
- Before sharing the link with anyone externally

---

## Deployment Flow

1. Mike makes corrections to `memory/robotics-dashboard.html`
2. Copy updated HTML to deploy folder
3. Run deploy command
4. Confirm live URL responds with `curl -s -o /dev/null -w "%{http_code}" https://exabytes.pages.dev` → should return 200
5. Update `memory/robotics-exabytes.md` with last deploy date if needed