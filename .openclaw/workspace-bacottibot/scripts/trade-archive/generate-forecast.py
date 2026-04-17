#!/usr/bin/env python3
"""
Generate dependability-forecast.html from forecast.json data.
Produces the FULL inline-CSS canonical page — all 14 sectors, all sections.

Usage: python3 generate-forecast.py [output_path]
Template is embedded below; edit the TEMPLATE constant to change page structure.
"""
import json, sys, os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.join(SCRIPT_DIR, 'data', 'forecast.json')
DEFAULT_OUTPUT = '/tmp/forecast-generated.html'
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'data', 'forecast-canonical-template.html')

# ── Canonical template ────────────────────────────────────────────────────────
# This is the full canonical page. All dynamic values are {{PLACEHOLDER}} markers.
# Edit here to change page structure. Never change generate_forecast() to produce
# a simpler/alternative structure — the goal is always this full page.
TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="canonical" href="https://www.dependability.us/dependability-forecast.html" />
  <title>S&P 500 Forecast 2026 — Bullish Case for American Growth | Dependability Holdings</title>
  <meta name="google-adsense-account" content="ca-pub-9312870448453345" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet" />
  <style>
    :root {
      --navy:       #0a1628;
      --navy-mid:   #132240;
      --navy-light: #1e3358;
      --gold:       #c8a96e;
      --gold-light: #e2c99a;
      --white:      #ffffff;
      --off-white:  #f5f6f8;
      --gray-light: #e8eaed;
      --gray-mid:   #8a94a6;
      --green:      #2e9e6b;
      --red:        #c94b4b;
      --text-dark:  #1a1f2e;
      --text-body:  #3a4157;
      --shadow:     0 2px 12px rgba(10,22,40,.12);
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Inter', system-ui, sans-serif;
      background: var(--off-white);
      color: var(--text-body);
      line-height: 1.6;
    }
    nav {
      background: var(--navy);
      padding: 0 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 64px;
      position: sticky;
      top: 0;
      z-index: 100;
      border-bottom: 2px solid var(--gold);
    }
    .nav-brand {
      font-family: 'Playfair Display', serif;
      font-size: 1.2rem;
      color: var(--white);
      letter-spacing: .03em;
      text-decoration: none;
    }
    .nav-brand span { color: var(--gold); }
    .nav-links { display: flex; gap: 2rem; }
    .nav-links a {
      color: var(--gray-mid);
      text-decoration: none;
      font-size: .875rem;
      font-weight: 500;
      transition: color .2s;
    }
    .nav-links a:hover { color: var(--gold); }
    .hero {
      background: linear-gradient(160deg, var(--navy) 0%, var(--navy-mid) 60%, #1a3a6a 100%);
      color: var(--white);
      padding: 5rem 2rem 4rem;
      text-align: center;
      position: relative;
      overflow: hidden;
    }
    .hero::before {
      content: '';
      position: absolute;
      inset: 0;
      background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
      pointer-events: none;
    }
    .hero-eyebrow {
      font-size: .8rem;
      letter-spacing: .18em;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 1rem;
      font-weight: 600;
    }
    .hero h1 {
      font-family: 'Playfair Display', serif;
      font-size: clamp(2.2rem, 5vw, 3.6rem);
      line-height: 1.15;
      margin-bottom: 1.2rem;
      color: var(--white);
    }
    .hero h1 em { font-style: normal; color: var(--gold-light); }
    .hero-sub {
      font-size: 1.1rem;
      color: rgba(255,255,255,.65);
      max-width: 620px;
      margin: 0 auto 2.5rem;
      font-weight: 300;
    }
    .hero-stats {
      display: flex;
      justify-content: center;
      gap: 3rem;
      flex-wrap: wrap;
      margin-top: 2rem;
    }
    .hero-stat { text-align: center; }
    .hero-stat-value {
      font-size: 2.4rem;
      font-weight: 700;
      color: var(--gold-light);
      line-height: 1;
    }
    .hero-stat-label {
      font-size: .78rem;
      color: rgba(255,255,255,.5);
      text-transform: uppercase;
      letter-spacing: .1em;
      margin-top: .4rem;
    }
    .hero-badge {
      display: inline-block;
      background: rgba(200,169,110,.15);
      border: 1px solid rgba(200,169,110,.35);
      color: var(--gold);
      font-size: .8rem;
      padding: .35rem .9rem;
      border-radius: 50px;
      margin-bottom: 1.5rem;
      letter-spacing: .04em;
    }
    .section { padding: 4rem 2rem; max-width: 1100px; margin: 0 auto; }
    .section-title {
      font-family: 'Playfair Display', serif;
      font-size: 1.9rem;
      color: var(--navy);
      margin-bottom: .4rem;
    }
    .section-sub {
      color: var(--gray-mid);
      font-size: .95rem;
      margin-bottom: 2.5rem;
    }
    .divider {
      height: 1px;
      background: linear-gradient(to right, transparent, var(--gold), transparent);
      max-width: 1100px;
      margin: 0 auto;
    }
    .table-wrap { overflow-x: auto; border-radius: 12px; box-shadow: var(--shadow); }
    table { width: 100%; border-collapse: collapse; background: var(--white); font-size: .9rem; }
    thead { background: var(--navy); }
    thead th {
      color: var(--white);
      font-weight: 600;
      text-align: left;
      padding: .85rem 1.1rem;
      font-size: .82rem;
      letter-spacing: .06em;
      text-transform: uppercase;
    }
    thead th:first-child { border-radius: 12px 0 0 0; }
    thead th:last-child { border-radius: 0 12px 0 0; }
    tbody tr:nth-child(even) { background: var(--off-white); }
    tbody tr:hover { background: rgba(200,169,110,.08); }
    td {
      padding: .75rem 1.1rem;
      border-bottom: 1px solid var(--gray-light);
      color: var(--text-dark);
    }
    td strong { color: var(--green); }
    tr:last-child td { border-bottom: none; }
    .tier-badge {
      display: inline-block;
      padding: .2rem .6rem;
      border-radius: 4px;
      font-size: .75rem;
      font-weight: 700;
      letter-spacing: .05em;
      text-transform: uppercase;
    }
    .tier-bull  { background: rgba(46,158,107,.12); color: #1e7e52; }
    .tier-bear  { background: rgba(201,75,75,.1);  color: #a33535; }
    .tier-base  { background: rgba(200,169,110,.15); color: #8a6e3e; }
    .thesis-section { background: var(--navy); color: var(--white); padding: 4rem 2rem; }
    .thesis-inner { max-width: 1100px; margin: 0 auto; }
    .thesis-section .section-title { color: var(--white); }
    .thesis-section .section-sub { color: rgba(255,255,255,.55); }
    .thesis-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1.5rem;
      margin-top: 0;
    }
    .thesis-card {
      background: var(--navy-light);
      border-radius: 12px;
      padding: 1.75rem;
      border-left: 3px solid var(--gold);
    }
    .thesis-card h3 {
      color: var(--gold-light);
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: .6rem;
    }
    .thesis-card p { color: rgba(255,255,255,.7); font-size: .9rem; line-height: 1.65; }
    .thesis-card ul {
      list-style: none;
      margin-top: .75rem;
      display: flex;
      flex-direction: column;
      gap: .4rem;
    }
    .thesis-card li {
      color: rgba(255,255,255,.65);
      font-size: .875rem;
      padding-left: 1.1rem;
      position: relative;
    }
    .thesis-card li::before {
      content: '▸';
      position: absolute;
      left: 0;
      color: var(--gold);
    }
    .levels-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.5rem;
    }
    @media (max-width: 680px) { .levels-grid { grid-template-columns: 1fr; } }
    .level-col { background: var(--white); border-radius: 12px; overflow: hidden; box-shadow: var(--shadow); }
    .level-header {
      padding: .9rem 1.25rem;
      font-weight: 700;
      font-size: .85rem;
      letter-spacing: .08em;
      text-transform: uppercase;
      text-align: center;
    }
    .level-header.bull  { background: var(--green);  color: var(--white); }
    .level-header.base  { background: var(--navy);   color: var(--white); }
    .level-header.bear  { background: var(--red);    color: var(--white); }
    .level-body { padding: 1.5rem; }
    .level-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: .6rem 0;
      border-bottom: 1px solid var(--gray-light);
      font-size: .9rem;
    }
    .level-item:last-child { border-bottom: none; }
    .level-item-label { color: var(--gray-mid); }
    .level-item-value { font-weight: 700; color: var(--text-dark); }
    .context-section { background: var(--off-white); }
    .context-split {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
    }
    @media (max-width: 680px) { .context-split { grid-template-columns: 1fr; } }
    .context-panel {
      background: var(--white);
      border-radius: 12px;
      padding: 2rem;
      box-shadow: var(--shadow);
    }
    .context-panel h3 {
      font-size: 1.1rem;
      font-weight: 700;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: .5rem;
    }
    .context-panel.us h3  { color: var(--green); }
    .context-panel.risk h3 { color: var(--red); }
    .context-panel ul {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: .6rem;
    }
    .context-panel li {
      font-size: .9rem;
      padding-left: 1.1rem;
      position: relative;
      color: var(--text-body);
    }
    .context-panel li::before { content: '–'; position: absolute; left: 0; color: var(--gray-mid); }
    .strategy-section { background: var(--navy); }
    .strategy-inner { max-width: 1100px; margin: 0 auto; }
    .strategy-section .section-title { color: var(--white); }
    .strategy-section .section-sub { color: rgba(255,255,255,.55); }
    .strategy-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.25rem;
    }
    .strategy-card {
      background: var(--navy-light);
      border-radius: 10px;
      padding: 1.4rem;
    }
    .strategy-card h4 {
      color: var(--gold-light);
      font-size: .9rem;
      font-weight: 700;
      margin-bottom: .5rem;
      text-transform: uppercase;
      letter-spacing: .05em;
    }
    .strategy-card p { color: rgba(255,255,255,.65); font-size: .875rem; line-height: 1.6; }
    .strategy-card .pro { color: #5fca9a; font-size: .8rem; margin-top: .5rem; }
    .strategy-card .con { color: #e08080; font-size: .8rem; margin-top: .25rem; }
    .disclaimer {
      background: var(--navy);
      color: rgba(255,255,255,.4);
      font-size: .78rem;
      line-height: 1.7;
      padding: 2.5rem 2rem;
      text-align: center;
    }
    .disclaimer-inner { max-width: 760px; margin: 0 auto; }
    footer {
      background: var(--navy);
      border-top: 1px solid rgba(200,169,110,.2);
      padding: 1.25rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: .5rem;
    }
    footer .brand { font-family: 'Playfair Display', serif; font-size: 1rem; color: var(--white); }
    footer .brand span { color: var(--gold); }
    footer p { font-size: .78rem; color: rgba(255,255,255,.3); }
    [id] { scroll-margin-top: 72px; }
    .trade-disclaimer {
      margin-top: 1.5rem;
      padding: 1rem;
      background: rgba(200,169,110,.08);
      border: 1px solid rgba(200,169,110,.2);
      border-radius: 8px;
      font-size: .82rem;
      color: rgba(255,255,255,.5);
      line-height: 1.6;
    }
    .trade-disclaimer strong { color: rgba(255,255,255,.7); }
  </style>
</head>
<body>
  <nav>
    <a href="index.html" class="nav-brand">Dependability <span>Holdings</span> LLC</a>
    <div class="nav-links">
      <a href="#weekly">Weekly</a>
      <a href="#monthly">Monthly</a>
      <a href="#thesis">Thesis</a>
      <a href="#levels">Levels</a>
      <a href="#global">Global</a>
      <a href="#strategy">Strategy</a>
    </div>
  </nav>

  <header class="hero">
    <div class="hero-eyebrow">Dependability Holdings LLC — Research</div>
    <h1>S&P 500 Forecast <em>2026</em><br>Bullish Case for American Growth</h1>
    <p class="hero-sub">A disciplined, research-driven overview of the key fundamental, technical, and geopolitical forces shaping the S&P 500 in 2026 — with actionable option expiry schedules.</p>
    <div class="hero-badge">{{BADGE}}</div>
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="hero-stat-value">{{SP500}}</div>
        <div class="hero-stat-label"><a href="https://www.spglobal.com/spdji/en/indices/equity/sp-500/" target="_blank" rel="noopener" style="color:rgba(255,255,255,.5);">S&P 500</a> Close</div>
        <div class="hero-stat-label">{{SP500_DATE}}</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-value">{{SPY}}</div>
        <div class="hero-stat-label">SPY Live</div>
        <div class="hero-stat-label">{{SPY_DATE}}</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-value">{{VIX}}</div>
        <div class="hero-stat-label">VIX</div>
        <div class="hero-stat-label">{{VIX_REGIME}}</div>
      </div>
      <div class="hero-stat">
        <div class="hero-stat-value">{{QQQ}}</div>
        <div class="hero-stat-label">QQQ</div>
        <div class="hero-stat-label">{{QQQ_DATE}}</div>
      </div>
    </div>
  </header>

  <div style="max-width:900px;margin:1rem auto;font-size:.85rem;color:#64748b;padding:0 2rem;">
    <p><strong>Author:</strong> Dependability Holdings Research Team &nbsp;|&nbsp; <strong>Updated:</strong> {{UPDATED_DATE}} &nbsp;|&nbsp; <a href="about-strategy.html" style="color:var(--gold);">About our methodology →</a></p>
  </div>

  <div style="background:#f8fafc;border-left:4px solid #f59e0b;padding:1rem 1.25rem;margin:1.5rem auto;max-width:900px;border-radius:4px;font-size:.85rem;color:#64748b;line-height:1.6;">
    <strong>Disclaimer:</strong> This is educational research, not investment advice. Options trading involves significant risk of loss. All information is for informational purposes only. Not affiliated with or endorsed by any broker. Past performance does not indicate future results.
  </div>

  <div class="divider"></div>

  <div class="divider"></div>
  <div style="background:var(--navy);color:white;border-radius:12px;padding:1.5rem 2rem;margin:2rem auto;max-width:900px;">
    <h2 style="color:var(--gold);font-family:'Playfair Display',serif;margin-bottom:1rem;font-size:1.3rem;">Key Takeaways — {{UPDATED_DATE}}</h2>
    <ul style="list-style:none;padding:0;margin:0;display:grid;gap:0.6rem;">
      <li style="display:flex;gap:0.5rem;"><span style="color:var(--gold);">→</span> <a href="https://www.spglobal.com/spdji/en/indices/equity/sp-500/" target="_blank" rel="noopener" style="color:rgba(255,255,255,.85);font-weight:600;">S&P 500</a> {{T1}}</li>
      <li style="display:flex;gap:0.5rem;"><span style="color:var(--gold);">→</span> <a href="https://www.cboe.com/" target="_blank" rel="noopener" style="color:rgba(255,255,255,.85);font-weight:600;">VIX</a> {{T2}}</li>
      <li style="display:flex;gap:0.5rem;"><span style="color:var(--gold);">→</span> {{T3}}</li>
    </ul>
    <p style="margin-top:1rem;font-size:.85rem;color:rgba(255,255,255,.6);">⚠️ Risk: VIX {{VIX}} ({{VIX_REGIME}}) — defined-risk spreads preferred over naked positions. {{RISK_NOTE}}</p>
  </div>

  <section class="section" id="geopolitical-alert" style="background:#fff3cd;border-left:5px solid #c8a96e;border-radius:12px;padding:2rem;max-width:1100px;margin:0 auto 2rem;">
    <div style="font-size:.75rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#2e7d32;margin-bottom:.5rem;">{{BADGE}}</div>
    <h2 style="font-family:'Playfair Display',serif;font-size:1.5rem;color:var(--navy);margin-bottom:.75rem;">S&P 500 {{GEOPOLITICAL_SUBTITLE}}</h2>
    <h3 style="font-size:.95rem;color:var(--navy);margin-bottom:.5rem;">Market Digesting Tuesday's Historic Rally</h3>
    <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;margin-bottom:.75rem;"><strong>As of {{DOW}} {{UPDATED_DATE}} ({{TIME_ET}} ET)</strong>, US equity futures are little changed after <strong>SPY closed at {{SPY}} ({{SPY_CHANGE}})</strong> on Tuesday — pushing the <a href="https://www.spglobal.com/spdji/en/indices/equity/sp-500/" target="_blank" rel="noopener" style="color:var(--navy);font-weight:600;">S&P 500</a> to <strong>~{{SP500}}</strong>, an all-time high and within striking distance of the {{RESISTANCE_1}} round number. The Nasdaq led with a {{QQQ_CHANGE}} gain and has now extended its win streak to {{STREAK}} — a remarkable show of momentum. Pre-market {{DOW}} is flat as traders pause before the next Iran diplomacy headlines.</p>
    <h3 style="font-size:.95rem;color:var(--navy);margin-bottom:.5rem;">US-Iran Talks: Market Pricing {{CEASEFIRE_ODDS}} Odds of Formal Negotiations</h3>
    <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;margin-bottom:.75rem;"><strong>VIX is holding at {{VIX}}</strong> — {{VIX_REGIME}} but declining from Tuesday's close. The IV backdrop remains supportive for credit spread strategies as the market views Iran escalation risk as fading. WTI crude has sold off ~7% on ceasefire optimism, adding tailwind to equities. Trump confirmed Iran wants to negotiate; the Hormuz blockade remains technically active but the market is clearly looking past it toward a diplomatic resolution.</p>
    <h3 style="font-size:.95rem;color:var(--navy);margin-bottom:.5rem;">Key Levels — SPY and S&P 500</h3>
    <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;margin-bottom:0;">Resistance: <strong>{{RESISTANCE_1}} (psychological), {{RESISTANCE_2}} (all-time high)</strong>. Support: <strong>{{SP500}} (Tuesday close), {{RESISTANCE_2}}</strong>.</p>
  </section>

  <section class="section" id="weekly-outlook">
    <div class="section-title">S&P 500 Forecast: What to Watch This Week</div>
    <h3 style="font-size:1.05rem;color:var(--navy);margin-bottom:.5rem;">Market Snapshot — {{DOW}} {{UPDATED_DATE}}</h3>
    <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;margin-bottom:.75rem;">It is <strong>{{DOW}}, {{UPDATED_DATE}} ({{TIME_ET}} ET)</strong>. {{COMMENTARY_INTRO}}</p>
    <h3 style="font-size:1.05rem;color:var(--navy);margin-bottom:.5rem;">VIX, Oil, and De-Escalation Trade in Force</h3>
    <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;margin-bottom:.75rem;">{{COMMENTARY_VIX}}</p>
    <h3 style="font-size:1.05rem;color:var(--navy);margin-bottom:.5rem;">Key Levels and Preferred Strategies</h3>
    <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;margin-bottom:0;">Resistance: <strong>{{RESISTANCE_1}}</strong> (psychological), <strong>{{RESISTANCE_2}}</strong> (all-time high area). Support: <strong>{{SP500}}</strong> (Tuesday close), <strong>{{RESISTANCE_2}}</strong>. With VIX at {{VIX}} ({{VIX_REGIME}}), credit spreads remain the preferred instrument. Bull Put Spreads collect premium while betting on continued calm; Bull Call Spreads provide leveraged upside without paying full outright call premium. {{EXPIRY_NOTE}}</p>
  </section>

  <section class="section" id="sector-performance" style="background:#f8f9fa;">
    <div style="max-width:1100px;margin:0 auto;">
      <h2 style="font-family:"'Playfair Display'",serif;font-size:1.6rem;color:#0a1628;text-align:center;margin-bottom:0.5rem;">S&P 500 Sector Performance — {{UPDATED_DATE}}</h2>
      <p style="text-align:center;color:#666;font-size:0.82rem;margin-bottom:2rem;">Daily and weekly performance. Source: S&P 500 sector SPDRs. For informational purposes only.</p>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-size:0.85rem;min-width:700px;">
          <thead>
            <tr style="background:#0a1628;color:#fff;">
              <th style="padding:0.6rem 0.75rem;text-align:left;font-weight:600;border-bottom:2px solid #3ecf8e;">Sector ETF</th>
              <th style="padding:0.6rem 0.75rem;text-align:center;font-weight:600;border-bottom:2px solid #3ecf8e;">Daily %</th>
              <th style="padding:0.6rem 0.75rem;text-align:center;font-weight:600;border-bottom:2px solid #3ecf8e;">Weekly %</th>
              <th style="padding:0.6rem 0.75rem;text-align:left;font-weight:600;border-bottom:2px solid #3ecf8e;">S&P Weight</th>
              <th style="padding:0.6rem 0.75rem;text-align:left;font-weight:600;border-bottom:2px solid #3ecf8e;">Notes</th>
            </tr>
          </thead>
          <tbody>{{SECTOR_ROWS}}</tbody>
        </table>
      </div>
      <p style="text-align:center;color:#94a3b8;font-size:0.75rem;margin-top:1rem;">* Weights are approximate S&P 500 sector allocations as of Q1 2026. Performance figures are illustrative. Data: S&P sector SPDRs.</p>
    </div>
  </section>

  <section class="section" id="trade-ideas">
    <div class="section-title">Option Trade Ideas for Today — {{UPDATED_DATE}}</div>
    <p style="margin:.25rem 0 .75rem;font-size:.85rem;color:var(--gray-mid);">📋 Previous ideas: <a href="trade-archive.html" style="color:var(--gold);">View trade archive</a></p>
    <p style="font-size:.8rem;color:#94a3b8;margin:.5rem 0;">📘 Educational example only — not investment advice.</p>
    <h3 style="font-size:1rem;color:var(--navy);margin-bottom:.5rem;">Market Regime and Direction</h3>
    <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;margin-bottom:.75rem;">Market regime: Risk-On / Bullish (<a href="https://www.spglobal.com/spdji/en/indices/equity/sp-500/" target="_blank" rel="noopener" style="color:var(--navy);font-weight:600;">S&P 500</a> at all-time high ~{{SP500}} + Nasdaq {{QQQ_CHANGE}} with {{STREAK}} + VIX {{VIX}} = {{VIX_REGIME}} but declining). Direction: Bullish — SPY {{SPY}}, firmly in all-time-high territory. De-escalation odds {{CEASEFIRE_ODDS}}. Pre-market {{DOW}} as market digests momentum.</p>
    <h3 style="font-size:1rem;color:var(--navy);margin-bottom:.5rem;">Trade Setup — {{TRADE_EXPIRY}} ({{TRADE_DTE}})</h3>
    <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;margin-bottom:.75rem;">Expiration: nearest weekly ({{TRADE_EXPIRY}}, <strong>{{TRADE_DTE}}</strong>). SPY {{SPY}}. Resistance at <strong>{{RESISTANCE_1}}</strong> (psychological), <strong>{{RESISTANCE_2}}</strong> (all-time high). <strong>Preferred vehicles: Bull Call Spread (debit) and Bull Put Spread (credit)</strong> — VIX {{VIX}} ({{VIX_REGIME}}, {{VIX}}-20) makes selling premium still attractive. {{TRADE_SETUP_NOTE}}</p>
    <p style="font-size:.8rem;color:#94a3b8;margin:.5rem 0;">📘 Educational examples only — not investment advice. Verify all pricing with your broker.</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th></th><th>Trade 1</th><th>Trade 2</th></tr>
        </thead>
        <tbody>{{TRADE_ROWS}}</tbody>
      </table>
    </div>
    <p class="trade-disclaimer">⚠️ All spreads are for educational purposes only. Options trading involves significant risk. {{TRADE_DISCLAIMER}}</p>
  </section>

  <section class="section" id="weekly">
    <div class="section-title">XSP / SPX Weekly Options — 2026</div>
    <div class="section-sub">Mini-SPX (XSP) and SPX Weeklys expire every Monday, Wednesday, and Friday. Dates below show weekly cycles for the remainder of 2026 (sample Mon / Wed / Fri).</div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>Month</th><th>Monday</th><th>Wednesday</th><th>Friday</th><th>Notes</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>April 2026</strong></td><td>Apr 6, 13, 20, 27</td><td>Apr 1, 8, 15, 22, 29</td><td>Apr 3, 10, 17*, 24</td><td><span class="tier-badge tier-base">Apr 17 = Monthly OPEX</span></td></tr>
          <tr><td><strong>May 2026</strong></td><td>May 4, 11, 18, 25</td><td>May 6, 13*, 20, 27</td><td>May 1, 8, 15*, 22, 29</td><td><span class="tier-badge tier-base">May 15 = Monthly OPEX</span></td></tr>
          <tr><td><strong>June 2026</strong></td><td>Jun 1, 8, 15, 22, 29</td><td>Jun 3, 10, 17*, 24</td><td>Jun 5, 12, 19*, 26</td><td><span class="tier-badge tier-bull">Jun 19 = Quarterly OPEX</span></td></tr>
          <tr><td><strong>July 2026</strong></td><td>Jul 6, 13, 20, 27</td><td>Jul 1, 8, 15*, 22, 29</td><td>Jul 3, 10, 17*, 24, 31</td><td><span class="tier-badge tier-base">Jul 17 = Monthly OPEX</span></td></tr>
          <tr><td><strong>August 2026</strong></td><td>Aug 3, 10, 17, 24, 31</td><td>Aug 5, 12, 19, 26</td><td>Aug 7, 14, 21*, 28</td><td><span class="tier-badge tier-base">Aug 21 = Monthly OPEX</span></td></tr>
          <tr><td><strong>September 2026</strong></td><td>Sep 7, 14, 21, 28</td><td>Sep 2, 9, 16, 23, 30</td><td>Sep 4, 11, 18*, 25</td><td><span class="tier-badge tier-bull">Sep 18 = Quarterly OPEX</span></td></tr>
          <tr><td><strong>October 2026</strong></td><td>Oct 5, 12, 19, 26</td><td>Oct 7, 14, 21, 28</td><td>Oct 2, 9, 16*, 23, 30</td><td><span class="tier-badge tier-base">Oct 16 = Monthly OPEX</span></td></tr>
          <tr><td><strong>November 2026</strong></td><td>Nov 2, 9, 16, 23, 30</td><td>Nov 4, 11, 18, 25</td><td>Nov 6, 13, 20*, 27</td><td><span class="tier-badge tier-base">Nov 20 = Monthly OPEX</span></td></tr>
          <tr><td><strong>December 2026</strong></td><td>Dec 7, 14, 21, 28</td><td>Dec 2, 9, 16, 23, 30</td><td>Dec 4, 11, 18*, 25</td><td><span class="tier-badge tier-bull">Dec 18 = Quarterly OPEX</span></td></tr>
        </tbody>
      </table>
    </div>
    <p style="font-size:.8rem;color:var(--gray-mid);margin-top:.75rem;">* Monthly/quarterly OPEX dates override weekly expirations on those specific days. XSP is the mini-SPX (1/10th notional) with European-style cash settlement. SPX Weeklys are PM-settled. Verify holiday-adjusted dates via the <a href="https://www.cboe.com/" target="_blank" rel="noopener" style="color:var(--navy);font-weight:600;">CBOE</a>/OCC calendars.</p>
  </section>

  <div class="divider"></div>

  <section class="section" id="monthly">
    <div class="section-title">Monthly SPX Expirations — 2026</div>
    <div class="section-sub">Standard monthly SPX options expire on the third Friday of each month (European-style, cash-settled at PM close). Remaining 2026 monthly expiries with Wall Street price targets and key context.</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>Expiration</th><th>Date</th><th>Day</th><th>Type</th><th>Bullish Target Zone</th><th>Key Drivers</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>June 2026</strong></td><td>Jun 19, 2026</td><td>Friday</td><td><span class="tier-badge tier-bull">Quarterly OPEX</span></td><td><strong>6,900 – 7,200</strong></td><td>Q2 earnings, Iran blockade resolution, tax legislation</td></tr>
          <tr><td><strong>July 2026</strong></td><td>Jul 17, 2026</td><td>Friday</td><td><span class="tier-badge tier-base">Monthly</span></td><td><strong>7,000 – 7,300</strong></td><td>AI earnings season, Fed signaling, energy prices</td></tr>
          <tr><td><strong>August 2026</strong></td><td>Aug 21, 2026</td><td>Friday</td><td><span class="tier-badge tier-base">Monthly</span></td><td><strong>7,100 – 7,400</strong></td><td>Summer rally seasonality, earnings momentum</td></tr>
          <tr><td><strong>September 2026</strong></td><td>Sep 18, 2026</td><td>Friday</td><td><span class="tier-badge tier-bull">Quarterly OPEX</span></td><td><strong>7,200 – 7,500</strong></td><td>Q3 resolution, mid-year GDP check, Fed path clear</td></tr>
          <tr><td><strong>October 2026</strong></td><td>Oct 16, 2026</td><td>Friday</td><td><span class="tier-badge tier-base">Monthly</span></td><td><strong>7,300 – 7,600</strong></td><td>Q4 seasonal strength, full-year earnings growth</td></tr>
          <tr><td><strong>November 2026</strong></td><td>Nov 20, 2026</td><td>Friday</td><td><span class="tier-badge tier-base">Monthly</span></td><td><strong>7,400 – 7,700</strong></td><td>Year-end momentum, portfolio repositioning</td></tr>
          <tr><td><strong>December 2026</strong></td><td>Dec 18, 2026</td><td>Friday</td><td><span class="tier-badge tier-bull">Quarterly OPEX</span></td><td><strong>7,500 – 7,800</strong></td><td>Morgan Stanley target; Q4 earnings closeout</td></tr>
        </tbody>
      </table>
    </div>
    <p style="font-size:.8rem;color:var(--gray-mid);margin-top:.75rem;">* Target zones are directional estimates based on Wall Street consensus ranges and the Dependability Holdings internal base case. Not a guarantee of price.</p>
  </section>

  <div class="divider"></div>

  <section class="thesis-section" id="thesis">
    <div class="thesis-inner">
      <div class="section-title">The Bullish Thesis — 5 Pillars</div>
      <div class="section-sub">Five interconnected forces supporting continued S&P 500 appreciation through 2026.</div>
      <div class="thesis-grid">
        <div class="thesis-card">
          <h3>1. Tax Cuts &amp; Deregulation</h3>
          <p>The Trump administration's 2025–2026 agenda centers on extending and expanding the 2017 Tax Cuts and Jobs Act. Corporate tax rate preservation and further business-friendly deregulation are expected to boost S&P 500 earnings per share by 5–10%.</p>
          <ul>
            <li>Corporate tax extension = direct EPS uplift</li>
           li>Financial &amp; energy deregulation = margin expansion</li>
            <li>Regulatory rollback lowers compliance costs</li>
          </ul>
        </div>
        <div class="thesis-card">
          <h3>2. Iran Conflict — De-escalation in Progress</h3>
          <p>The US-Iran Hormuz blockade is <strong>technically still in effect</strong> as of {{UPDATED_DATE}} — but diplomatic off-ramps are opening on both sides. The market is now pricing {{CEASEFIRE_ODDS}} of formal US-Iran negotiations. WTI crude has pulled back from $104 to ~$97–98 on ceasefire hopes. SPY closed at {{SPY}} Tuesday — firmly in all-time-high territory — and the relief rally has fully reversed the initial blockade spike.</p>
          <p style="color:rgba(255,255,255,.7);font-size:.9rem;line-height:1.65;margin-top:.75rem;">The Strait of Hormuz carries 20–25% of global daily oil supply, so any confirmed ceasefire would be a significant tailwind for equities and a headwind for energy prices.</p>
          <ul>
            <li>Diplomatic off-ramp: Trump says Iran wants to make a deal — market pricing {{CEASEFIRE_ODDS}} of formal talks</li>
            <li>SPY closed at {{SPY}} ({{SPY_CHANGE}}), S&P at all-time high ~{{SP500}}</li>
            <li>WTI crude steady near $97–98 on ceasefire expectations</li>
            <li>VIX dropped from 21.27 (high stress) to {{VIX}} ({{VIX_REGIME}}, near-normal) — IV draining</li>
            <li>Resistance: {{RESISTANCE_1}} (psychological); Support: {{SP500}} (Tuesday close), {{RESISTANCE_2}} (all-time high)</li>
          </ul>
        </div>
        <div class="thesis-card">
          <h3>3. Energy Independence &amp; US Production</h3>
          <p>US oil and gas production at record highs. American energy self-sufficiency buffers against global supply shocks and keeps domestic energy prices lower than peer nations.</p>
          <ul>
            <li>Record US output reduces import dependency</li>
            <li>Lower input costs for manufacturers</li>
            <li>Energy sector earnings = S&P tailwind</li>
          </ul>
        </div>
        <div class="thesis-card">
          <h3>4. AI-Driven Productivity Gains</h3>
          <p>Continued enterprise AI adoption is driving margin expansion across tech, financials, and healthcare. Massive capex in AI infrastructure continues to lift the broader supply chain.</p>
          <ul>
            <li>~30% of S&P 500 market cap = tech/AI exposure</li>
            <li>Productivity gains offset labor cost inflation</li>
            <li>Global AI investment cycle remains in early innings</li>
          </ul>
        </div>
        <div class="thesis-card">
          <h3>5. Favorable Historical Context</h3>
          <p>Republican administrations with tax-cut agendas (Reagan, Trump 1.0) have historically produced strong equity market performance. The current policy mix closely parallels the Trump 1.0 era that delivered +67% in S&P 500 over four years.</p>
          <ul>
            <li>Trump 1.0: S&P +67% (2017–2021)</li>
            <li>Reagan era: S&P +228% (1981–1989)</li>
            <li>Post-election S&P +3.6% (Nov 2024–Jan 2025)</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <section class="section" id="levels">
    <div class="section-title">SPY Support and Resistance — Current Trading Levels</div>
    <div class="section-sub">Current price ~{{SP500}}. Support, resistance, and Wall Street year-end targets across three scenarios.</div>
    <div class="levels-grid">
      <div class="level-col">
        <div class="level-header bull">🐂 Bull Case</div>
        <div class="level-body">
          <div class="level-item"><span class="level-item-label">All-time high</span><span class="level-item-value">~{{SP500}}</span></div>
          <div class="level-item"><span class="level-item-label">Break resistance</span><span class="level-item-value">{{RESISTANCE_1}}</span></div>
          <div class="level-item"><span class="level-item-label">Goldman base target</span><span class="level-item-value">7,600</span></div>
          <div class="level-item"><span class="level-item-label">Morgan Stanley target</span><span class="level-item-value">7,800</span></div>
          <div class="level-item"><span class="level-item-label">Citi target</span><span class="level-item-value">7,700</span></div>
          <div class="level-item"><span class="level-item-label">Upside from current</span><span class="level-item-value" style="color:var(--green)">+9–12%</span></div>
        </div>
      </div>
      <div class="level-col">
        <div class="level-header base">◉ Base Case</div>
        <div class="level-body">
          <div class="level-item"><span class="level-item-label">Current price</span><span class="level-item-value">{{SP500}}</span></div>
          <div class="level-item"><span class="level-item-label">JPMorgan target</span><span class="level-item-value">7,500</span></div>
          <div class="level-item"><span class="level-item-label">Barclays target</span><span class="level-item-value">7,400</span></div>
          <div class="level-item"><span class="level-item-label">Wells Fargo target</span><span class="level-item-value">7,500</span></div>
          <div class="level-item"><span class="level-item-label">Avg. Wall Street target</span><span class="level-item-value">~7,450</span></div>
          <div class="level-item"><span class="level-item-label">Base case upside</span><span class="level-item-value" style="color:var(--navy)">+7–8%</span></div>
        </div>
      </div>
      <div class="level-col">
        <div class="level-header bear">🐻 Bear Case</div>
        <div class="level-body">
          <div class="level-item"><span class="level-item-label">Near-term support</span><span class="level-item-value">6,150</span></div>
          <div class="level-item"><span class="level-item-label">JPMorgan floor</span><span class="level-item-value">6,000</span></div>
          <div class="level-item"><span class="level-item-label">Goldman moderate</span><span class="level-item-value">6,300</span></div>
          <div class="level-item"><span class="level-item-label">Goldman severe</span><span class="level-item-value">5,400</span></div>
          <div class="level-item"><span class="level-item-label">Bear case trigger</span><span class="level-item-value">Iran war escalation</span></div>
          <div class="level-item"><span class="level-item-label">Bear case downside</span><span class="level-item-value" style="color:var(--red)">−9–18%</span></div>
        </div>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <section class="section context-section" id="global">
    <div class="section-title">Why US Markets Outperform: Economic Strengths vs. Global Headwinds</div>
    <div class="section-sub">How American economic strengths (via <a href="https://fred.stlouisfed.org/" target="_blank" rel="noopener" style="color:var(--navy);font-weight:600;">FRED</a> data) contrast with structural headwinds facing Europe and China.</div>
    <div class="context-split">
      <div class="context-panel us">
        <h3>🇺🇸 United States — Relative Strength</h3>
        <ul>
          <li>GDP growth positive; labor market remains resilient</li>
          <li>AI investment cycle driving productivity gains</li>
          <li>Record US oil production provides energy cost advantage</li>
          <li>Tax and regulatory environment favors business expansion</li>
          <li>Dollar strength attracts foreign capital into equities</li>
          <li>Tariff framework with China reduces worst-case escalation risk</li>
          <li>Wall Street consensus still constructive on full-year 2026 earnings</li>
        </ul>
      </div>
      <div class="context-panel risk">
        <h3>🌍 EU &amp; China — Structural Headwinds</h3>
        <ul>
          <li><strong>China:</strong> 2026 GDP target 4.5–5% — lowest since early 1990s</li>
          <li><strong>China:</strong> Record $1.2T trade surplus in 2025 masks domestic weakness</li>
          <li><strong>Germany:</strong> Years of stagnation; structural reform stalled</li>
          <li><strong>France:</strong> Debt ratio deteriorating; political instability</li>
          <li><strong>Italy:</strong> Sovereign refinancing costs elevated</li>
          <li><strong>EU:</strong> As long as Germany underperforms, EU faces severe collective headwinds</li>
          <li><strong>EU:</strong> Financial crisis risk flagged by multiple analysts for 2026</li>
        </ul>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <section class="strategy-section" id="strategy">
    <div class="strategy-inner">
      <div class="section-title">Option Strategy Notes — Capitalizing on the Bullish Thesis</div>
      <p style="font-size:.8rem;color:#94a3b8;margin-bottom:.5rem;">📘 Educational examples only — not investment advice. All strategies described involve risk of loss.</p>
      <div class="section-sub">Dependability Holding's preferred approaches for bullish S&P positioning. We almost always sell an option to offset time decay.</div>
      <div class="strategy-grid">
        <div class="strategy-card">
          <h4>📊 Bull Call Spread (Preferred)</h4>
          <p>Buy a call at a lower strike, sell a call at a higher strike. The short call offsets theta decay on the long call. Defined risk, defined max profit.</p>
          <p class="pro">✓ Theta works FOR you — short call decays faster</p>
          <p class="pro">✓ Lower cost than naked call</p>
          <p class="con">✗ Profit capped at short strike</p>
        </div>
        <div class="strategy-card">
          <h4>📈 Bull Put Spread</h4>
          <p>Sell a put at a higher strike, buy a put at a lower strike for protection. Collect premium while establishing bullish exposure. We often sell cash-secured puts at support levels.</p>
          <p class="pro">✓ Net credit = you get paid upfront</p>
          <p class="pro">✓ Short put offset by long put — defined risk</p>
          <p class="con">✗ Profit capped if price rises above short strike</p>
        </div>
        <div class="strategy-card">
          <h4>🔄 Diagonal Spread</h4>
          <p>Buy a longer-dated call (e.g., Dec 2026) and sell a shorter-dated call at a higher strike. Combines bullish directional with theta capture.</p>
          <p class="pro">✓ Long call has more time to work</p>
          <p class="pro">✓ Short call generates income to offset decay</p>
          <p class="con">✗ More complex to manage</p>
        </div>
        <div class="strategy-card">
          <h4>⚡ Ratio Spread (2:1)</h4>
          <p>Buy 2 calls at a lower strike, sell 1 call at a higher strike. The short call funds half the long calls, reducing net cost.</p>
          <p class="pro">✓ Reduced or zero net cost</p>
          <p class="pro">✓ Theta neutral to slightly positive</p>
          <p class="con">✗ Can lose more than 1:1 spreads if price falls</p>
        </div>
        <div class="strategy-card">
          <h4>🏦 Cash-Secured Put (CSP)</h4>
          <p>Sell puts at levels you'd be comfortable owning the underlying. Collect premium while waiting for entries at support.</p>
          <p class="pro">✓ Earn income while waiting to buy</p>
          <p class="pro">✓ Can roll or assign if called away</p>
          <p class="con">✗ Obligation to buy if assigned</p>
        </div>
        <div class="strategy-card">
          <h4>🛡️ Collar (Protective Put + Covered Call)</h4>
          <p>Own the underlying (SPY or SPX), sell a call above current price for income, buy a put below for protection.</p>
          <p class="pro">✓ Defined risk with limited upside cap</p>
          <p class="pro">✓ Both legs fight theta decay</p>
          <p class="con">✗ Surrenders upside above short strike</p>
        </div>
      </div>
      <p style="color:rgba(255,255,255,.35);font-size:.8rem;margin-top:1.75rem;text-align:center;">All strategies above involve selling options to offset theta decay. Pure long options (buying single calls or puts without selling) are generally avoided because time decay erodes directional bets over time.</p>
      <p style="color:rgba(255,255,255,.35);font-size:.8rem;margin-top:.75rem;text-align:center;">These strategies are educational. Options trading involves significant risk. Past performance does not guarantee future results. Consult a licensed options professional.</p>
    </div>
  </section>

  <div style="max-width:900px;margin:2rem auto;">
    <h2 style="font-family:'Playfair Display',serif;color:var(--navy);margin-bottom:1.5rem;font-size:1.6rem;">Frequently Asked Questions</h2>
    <div style="border-bottom:1px solid var(--gray-light);padding:1rem 0;">
      <h3 style="font-size:1rem;color:var(--navy);margin-bottom:0.5rem;">What does VIX measure?</h3>
      <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;">The <a href="https://www.cboe.com/" target="_blank" rel="noopener" style="color:var(--navy);font-weight:600;">CBOE</a> Volatility Index (VIX) measures the market's expectation of 30-day volatility in the <a href="https://www.spglobal.com/spdji/en/indices/equity/sp-500/" target="_blank" rel="noopener" style="color:var(--navy);font-weight:600;">S&P 500</a>. When VIX is elevated (above 20), it signals elevated fear and uncertainty — which typically favors defined-risk option strategies like spreads over naked positions.</p>
    </div>
    <div style="border-bottom:1px solid var(--gray-light);padding:1rem 0;">
      <h3 style="font-size:1rem;color:var(--navy);margin-bottom:0.5rem;">What is a bull put spread?</h3>
      <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;">A bull put spread is a defined-risk, income-generating options strategy. You sell a higher strike put and buy a lower strike put for protection. Your max profit is the net credit received. Max loss is the width of the spread minus the credit. It profits when the underlying rises or stays flat.</p>
    </div>
    <div style="border-bottom:1px solid var(--gray-light);padding:1rem 0;">
      <h3 style="font-size:1rem;color:var(--navy);margin-bottom:0.5rem;">What does DTE mean?</h3>
      <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;">Days to Expiration (DTE) is how many days remain until the options contract expires. Short-dated spreads (7–14 DTE) capture time decay quickly but require the trade to work fast. 30–45 DTE gives more room for the thesis to develop.</p>
    </div>
    <div style="border-bottom:1px solid var(--gray-light);padding:1rem 0;">
      <h3 style="font-size:1rem;color:var(--navy);margin-bottom:0.5rem;">What VIX level signals elevated volatility?</h3>
      <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;">A VIX above 20 is generally considered elevated — indicating heightened uncertainty. VIX between 15–20 suggests the market is aware of risks but not in panic mode. Below 15 typically reflects complacency. The current VIX of {{VIX}} ({{UPDATED_DATE}}) sits in the {{VIX_REGIME}} range, which is still attractive for premium-selling strategies.</p>
    </div>
    <div style="padding:1rem 0;">
      <h3 style="font-size:1rem;color:var(--navy);margin-bottom:0.5rem;">Is this investment advice?</h3>
      <p style="font-size:.9rem;color:var(--text-body);line-height:1.65;">No. All content on this site is educational research only. Options trading involves significant risk of loss. Nothing here is personalized investment advice. Consult a licensed financial advisor before trading.</p>
    </div>
  </div>

  <div style="background:var(--navy);color:white;border-radius:12px;padding:2rem;margin:2rem auto;max-width:900px;">
    <h3 style="color:var(--gold);margin-bottom:1rem;font-size:1.1rem;">About the Research Team</h3>
    <p style="font-size:.9rem;line-height:1.8;color:rgba(255,255,255,.8);margin-bottom:1rem;">Dependability Holdings publishes educational research on markets, options strategies, and wealth-building. Our research is built on publicly available market data, standard options theory, and disciplined risk management principles.</p>
    <p style="font-size:.85rem;color:rgba(255,255,255,.5);">Last updated: {{UPDATED_DATE}} · <a href="about-strategy.html" style="color:var(--gold);">About our methodology →</a> · <a href="trade-archive.html" style="color:var(--gold);">Trade Archive →</a></p>
  </div>

  <div style="background:#f8fafc;border-radius:10px;padding:1.5rem;margin:2rem auto;max-width:900px;">
    <h3 style="color:var(--navy);margin-bottom:1rem;">Related Research</h3>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;">
      <a href="options-basics.html" style="color:var(--navy);font-weight:600;">→ Options Basics</a>
      <a href="risk-management.html" style="color:var(--navy);font-weight:600;">→ Risk Management</a>
      <a href="covered-calls-guide.html" style="color:var(--navy);font-weight:600;">→ Covered Calls Guide</a>
      <a href="iron-condors-explained.html" style="color:var(--navy);font-weight:600;">→ Iron Condors</a>
      <a href="trade-archive.html" style="color:var(--navy);font-weight:600;">→ Trade Archive</a>
      <a href="weekly-market-recap.html" style="color:var(--navy);font-weight:600;">→ Weekly Recap</a>
    </div>
  </div>

  <div class="disclaimer">
    <div class="disclaimer-inner">
      <strong>Important Disclaimer — Please Read</strong><br />
      Dependability Holdings LLC is an investment holding company. This webpage is for informational and educational purposes only and does not constitute financial, investment, or legal advice.
      Dependability Holdings LLC is not a registered investment advisor. The information provided herein should not be construed as personalized investment advice, a recommendation to buy, sell, or hold any investment, or an offer or solicitation to buy or sell securities.
      <br /><br />
      All investments involve risk, including the potential loss of principal. The value of investments can fluctuate, and past performance may not be indicative of future results. The price targets, technical levels, and strategy notes presented represent research opinions, not predictions of future performance.
      <br /><br />
      Please consult with a qualified financial advisor, attorney, or tax professional before making any investment decisions. Any decisions you make based on information found on this page are made entirely at your own risk.
    </div>
  </div>

  <footer>
    <div class="brand">Dependability <span>Holdings</span> LLC</div>
    <p>© 2026 Dependability Holdings LLC. All rights reserved. | <a href="https://dependability.us" style="color:rgba(200,169,110,.6);text-decoration:none;">dependability.us</a></p>
  </footer>
</body>
</html>'''


# ── Sector table ─────────────────────────────────────────────────────────────
SECTORS = [
    ("XLK", "Technology", "sectorspdr.com/sectorspdr/sector-spdr/xlk", "+1.2%", "+2.8%", "~29%", "Led by semiconductors; AI infrastructure demand steady", False),
    ("XLF", "Financials",  "sectorspdr.com/sectorspdr/sector-spdr/xlf", "+0.8%", "+1.5%", "~13%",  "Banks steady; rate-cut optimism supporting financials", False),
    ("XLV", "Healthcare",  "sectorspdr.com/sectorspdr/sector-spdr/xlv", "+0.3%", "+0.7%", "~13%",  "Defensive lag; biotech component outperforming", False),
    ("XLI", "Industrials", "sectorspdr.com/sectorspdr/sector-spdr/xli", "+0.9%", "+2.1%", "~8.5%", "Infrastructure spending narrative; defense names strong", False),
    ("XLC", "Communication Svcs", "sectorspdr.com/sectorspdr/sector-spdr/xlc", "+1.4%", "+2.9%", "~8.5%", "Meta, Alphabet strength; ad revenue momentum", False),
    ("XLY", "Consumer Discretionary", "sectorspdr.com/sectorspdr/sector-spdr/xly", "+1.5%", "+3.2%", "~10.5%", "Tesla and Amazon outperforming; consumer spending resilient", False),
    ("XLP", "Consumer Staples", "sectorspdr.com/sectorspdr/sector-spdr/xlp", "+0.4%", "+0.9%", "~6%", "Defensive; steady but not leading the rally", False),
    ("XLB", "Materials",   "sectorspdr.com/sectorspdr/sector-spdr/xlb", "+0.7%", "+1.8%", "~2.5%", "Copper and steel steady; infrastructure theme supporting", False),
    ("XLE", "Energy",      "sectorspdr.com/sectorspdr/sector-spdr/xle", "-1.2%", "-2.5%", "~3.5%", "Oil down ~7% on Iran ceasefire expectations; biggest sector laggard", True),
    ("XLU", "Utilities",   "sectorspdr.com/sectorspdr/sector-spdr/xlu", "+0.2%", "+0.5%", "~2.5%", "Defensive; little movement; bond proxy behavior", False),
    ("XME", "Metals & Mining", "sectorspdr.com/sectorspdr/sector-spdr/xme", "+1.1%", "+2.4%", "~0.5%", "Silver and gold mining outperforming; tariff relief rally", False),
    ("XLRE","Real Estate", "sectorspdr.com/sectorspdr/sector-spdr/xlre", "+0.6%", "+1.2%", "~2.5%", "Rate-sensitivity weighing on RE; small bounce on rate optimism", False),
    ("XHB", "Homebuilders","sectorspdr.com/sectorspdr/sector-spdr/xhb", "+0.8%", "+1.6%", "~0.8%", "Mortgage rates stabilizing; housing demand still pressured", False),
    ("XSW", "Software & Services", "sectorspdr.com/sectorspdr/sector-spdr/xsw", "+1.7%", "+3.5%", "~4.5%", "Small/mid-cap software leaders; AI integration names strong", False),
]


def day_of_week():
    """Return current day name (e.g. 'Friday')."""
    return datetime.now().strftime('%A')


def vix_color(vix_str):
    """Return CSS color class for VIX value."""
    try:
        v = float(vix_str.split()[0])
    except (ValueError, IndexError):
        return "gold"
    if v > 25: return "red"
    if v > 18: return "gold"
    return "green"


def make_sector_rows(data):
    sectors = data.get('sectors', [])
    if not sectors:
        # Fallback to hardcoded SECTORS if JSON has no sector data
        sec_list = SECTORS
    else:
        sec_list = [(s['ticker'], s['name'], f"sectorspdr.com/sectorspdr/sector-spdr/{s['ticker'].lower()}",
                     s['daily'], s['weekly'], s['weight'], s['notes'], s.get('neg', False)) for s in sectors]
    rows = []
    for i, (ticker, name, url, daily, weekly, weight, notes, neg) in enumerate(sec_list):
        bg = "#fff" if i % 2 == 0 else "#f8f9fa"
        col = "#dc2626;font-weight:600" if neg else "#16a34a;font-weight:600"
        rows.append(
            f'<tr style="background:{bg};border-bottom:1px solid #e8eaed;">'
            f'<td style="padding:0.55rem 0.75rem;font-weight:600;color:#0a1628;">'
            f'<a href="https://www.{url}" target="_blank" rel="noopener" style="color:#0a1628;text-decoration:none;">{ticker}</a> — {name}</td>'
            f'<td style="padding:0.55rem 0.75rem;text-align:center;color:{col};">{daily}</td>'
            f'<td style="padding:0.55rem 0.75rem;text-align:center;color:{col};">{weekly}</td>'
            f'<td style="padding:0.55rem 0.75rem;color:#555;">{weight} of S&P</td>'
            f'<td style="padding:0.55rem 0.75rem;color:#555;">{notes}</td>'
            f'</tr>'
        )
    return '\n'.join(rows)


def make_trade_rows(data):
    """Build trade table rows from forecast.json active_trades."""
    active = data.get('active_trades', [])
    if not active:
        return '<tr><td colspan="3"><em>No active trades this week.</em></td></tr>'
    rows = []
    # Pad to 2 trades
    trades = (active + [{}] * 2)[:2]
    labels = ["Direction", "Strategy", "Underlying", "Leg 1 — Buy Call",
              "Leg 2 — Sell Call", "Leg 3 — Sell Put", "Leg 4 — Buy Put",
              "Short Strike", "Long Strike", "Net Debit/Credit",
              "Max Profit", "Max Loss", "Prob. of Profit",
              "Days to Expiration", "Why This Trade"]
    fields = [
        ["direction", "strategy", "underlying", "leg_buy", "leg_sell_call", "leg_sell_put", "leg_buy_put",
         "short_strike", "long_strike", "net_debit", "max_profit", "max_loss",
         "prob_profit", "dte", "rationale"],
    ]
    t1, t2 = trades[0], trades[1] if len(trades) > 1 else {}
    for label in labels:
        k = label.lower().replace(" — ", "_").replace(" ", "_").replace("-", "_").replace("leg_", "leg")
        v1 = trades[0].get(k, "—") if trades[0] else "—"
        v2 = trades[1].get(k, "—") if len(trades) > 1 and trades[1] else "—"
        rows.append(f'<tr><td><strong>{label}</strong></td><td>{v1}</td><td>{v2}</td></tr>')
    return '\n'.join(rows)


def generate_forecast(data):
    m    = data.get('market', {})
    out  = data.get('outlook', {})
    day  = day_of_week()
    now  = datetime.now().strftime('%B %d, %Y')

    sp500      = m.get('sp500', '—')
    spy        = m.get('spy', '—')
    spy_ch     = m.get('spy_change', '—')
    vix        = m.get('vix', '—')
    vix_regime = m.get('vix_regime', 'Elevated')
    qqq        = m.get('qqq', '—')
    qqq_ch     = m.get('qqq_change', '—')
    badge      = out.get('badge', 'NEUTRAL')
    tagline    = out.get('tagline', '')
    t1         = out.get('t1', f'S&P 500 at {sp500}')
    t2         = out.get('t2', f'VIX {vix} — {vix_regime}')
    t3         = out.get('t3', 'Bull put spreads and bull call spreads recommended')
    risk_note  = out.get('risk_note', 'Defined-risk spreads preferred over naked positions.')
    updated    = data.get('last_updated', now)
    expiry_note= out.get('expiry_note', f'Friday Apr 18 weekly expiry (3 DTE) — defined-risk bullish positions')
    trade_note = out.get('trade_setup_note', 'Both benefit from continued IV crush if geopolitical situation improves through expiry.')
    disclaimer = out.get('trade_disclaimer', 'Trade 1 (Bull Call Spread) and Trade 2 (Bull Put Spread) both expire Friday Apr 18 (3 DTE). The Hormuz blockade remains technically active — formal US-Iran talks have not yet been confirmed. Monitor Iran diplomacy headlines throughout the day. Confirm spread pricing before entering.')
    ceasefire  = out.get('ceasefire_odds', '~85%')
    streak      = out.get('nasdaq_streak', '10 straight days')
    geo_sub    = out.get('geopolitical_subtitle', 'Flat Pre-Market — All-Time Highs Within Reach')
    comm_intro = out.get('commentary_intro', f'The relief rally from Tuesday has put the S&P 500 firmly in all-time-high territory at ~{sp500}.')
    comm_vix   = out.get('commentary_vix', f'VIX is holding at {vix} ({vix_regime} zone, 15–20) — still elevated enough that premium-selling strategies benefit.')
    resistance1= out.get('resistance_1', '7,000')
    resistance2= out.get('resistance_2', '6,800')
    time_et    = out.get('time_et', '7:00 AM')

    # Hero badge
    hero_badge = f"📈 {badge} — {day} {updated}  |  {tagline}"

    # Build replacements dict
    rep = {
        '{{BADGE}}':                   hero_badge,
        '{{SP500}}':                   sp500,
        '{{SP500_DATE}}':              updated,
        '{{SPY}}':                     spy,
        '{{SPY_DATE}}':                updated,
        '{{SPY_CHANGE}}':              spy_ch,
        '{{VIX}}':                    vix,
        '{{VIX_REGIME}}':             vix_regime,
        '{{QQQ}}':                    qqq,
        '{{QQQ_DATE}}':               updated,
        '{{QQQ_CHANGE}}':             qqq_ch,
        '{{UPDATED_DATE}}':           updated,
        '{{T1}}':                     t1,
        '{{T2}}':                     t2,
        '{{T3}}':                     t3,
        '{{RISK_NOTE}}':               risk_note,
        '{{DOW}}':                    day,
        '{{TIME_ET}}':                time_et,
        '{{RESISTANCE_1}}':           resistance1,
        '{{RESISTANCE_2}}':           resistance2,
        '{{CEASEFIRE_ODDS}}':         ceasefire,
        '{{STREAK}}':                 streak,
        '{{GEOPOLITICAL_SUBTITLE}}':  geo_sub,
        '{{COMMENTARY_INTRO}}':       comm_intro,
        '{{COMMENTARY_VIX}}':         comm_vix,
        '{{EXPIRY_NOTE}}':            expiry_note,
        '{{TRADE_EXPIRY}}':           out.get('trade_expiry', 'Apr 18'),
        '{{TRADE_DTE}}':              out.get('trade_dte', '3 DTE'),
        '{{TRADE_SETUP_NOTE}}':       trade_note,
        '{{TRADE_DISCLAIMER}}':       disclaimer,
        '{{SECTOR_ROWS}}':            make_sector_rows(data),
        '{{TRADE_ROWS}}':             make_trade_rows(data),
    }

    html = TEMPLATE
    for k, v in rep.items():
        html = html.replace(k, v)

    return html


if __name__ == '__main__':
    output_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT
    with open(DEFAULT_DATA, 'r') as f:
        data = json.load(f)
    html = generate_forecast(data)
    with open(output_path, 'w') as f:
        f.write(html)
    trades = len(data.get('active_trades', []))
    print(f'Written: {output_path} ({len(html):,} chars, {trades} active trades)')
