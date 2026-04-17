# Forecast Page — Canonical Good Version

**Git SHA:** `d2082fe75967b6b74d79cd743a0d58b8b6e6aebc`
**Source file:** `websites/bithues/Website/dependability-us/dependability-forecast.html`
**Live URL:** `https://www.dependability.us/dependability-forecast.html`
**Reference copy:** `Reference_Files/good-forecast-template-d2082fe.html`
**Visual reference (14 screenshots):** `Reference_Files/forecast-screenshots/`

---

## What This Version Contains

### Hero Section
- **Badge:** `📈 FLAT PRE-MARKET — April 15, 2026 | All-Time Highs in Reach`
- **S&P 500 Close:** 6,944 (pre-market / Tuesday close)
- **VIX:** 18.35 (elevated)
- **SPY:** $694.46 (Tuesday close)
- **QQQ:** $637.40 (Tuesday close)
- Hero has full gradient navy background with SVG pattern overlay

### Key Takeaways Block (navy box)
Three bullet points in gold arrows:
1. S&P at ~6,944 (all-time high territory)
2. VIX 18.35 (elevated, credit spreads preferred)
3. Bull call spreads and bull put spreads both referenced

### Market Commentary Section
Full paragraph + sub-sections:
- **What Changed Today** — Iran diplomacy progress, 10-day Nasdaq win streak
- **VIX and Volatility Regime** — elevated, declining, de-escalation regime
- **Preferred Strategy Framework** — Bull Put Spreads + Bull Call Spreads for 3 DTE Apr 18

### S&P 500 Sector Performance Table (THE KEY DIFFERENTATOR)
All 14 sectors: XLK, XLF, XLV, XLI, XLC, XLY, XLP, XLB, XLE, XLU, XME, XLRE, XHB, XSW
Each with:
- Daily % change (color-coded green/red)
- Weekly % change
- S&P weight
- Notes column with market rationale

### Option Trade Ideas Section
Two trade setups:
1. **Bull Call Spread** — Buy ATM $695 / Sell OTM $700, Apr 18 expiry
2. **Bull Put Spread** — Sell $695 / Buy $690, Apr 18 expiry
Each with full rationale, max profit/loss, probability of profit

### Support & Resistance Levels
Table with resistance, support, 50-day MA, VIX regime

### FAQ Section

### About the Research Team + Related Research blocks

---

## Structure Rules (Never Break These)

1. **This page MUST have the full 14-sector table** — this is the signature content
2. **Inline CSS in `<head>`** — not external CSS file for this page
3. **Self-contained** — all styles embedded, no external dependencies except fonts/adsense
4. **Hero has SVG pattern overlay** — `data:image/svg+xml,...` background pattern
5. **Sector table uses `<thead>` + `<tbody>`** — proper table structure
6. **Gold accent color** (`#c8a96e`) used for highlights and borders
7. **navy background** (`#0a1628`) for the hero and takeaway boxes
8. **Two trade ideas minimum** — Bull Call Spread + Bull Put Spread
9. **Use `afdea8c` as canonical git reference** — this is the LAST good commit

---

## How to Restore This Version

```bash
cd /Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/dependability-us/
git show d2082fe:dependability-forecast.html > dependability-forecast.html
git add dependability-forecast.html
git commit -m "Restore canonical forecast page (d2082fe)"
git push
```

---

## What Changed vs Earlier Versions

| Version | Date | Key Difference |
|---------|------|----------------|
| `d2082fe` | Apr 15 morning | Full 14-sector table, inline CSS, self-contained |
| `3664a25` | Apr 15 morning | S&P 6,944/VIX 18.35, same sector table but different opening |
| `64da0ca` | Apr 13 | VIX 21.27, bearish context, Iran blockade |
| `caf4cde` | Apr 12 | Iran blockade, Hormuz strait, oil spike |

**d2082fe is the canonical "good" version.**

---

## Lessons Learned

- Don't incrementally patch this page — if broken, restore from `d208fe` and re-apply date/trade changes
- The sector table is the signature content — never strip it out
- The inline CSS approach (self-contained) prevents `css/main.css` vs `css/style.css` confusion
- This page is 1,260 lines of self-contained HTML — treat it as a design document, not a template
