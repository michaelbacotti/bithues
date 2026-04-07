# OptionStrat Integration Guide

OptionStrat (`optionstrat.com`) is the primary web-based tool for visualizing, building, and analyzing options strategies. It provides P/L diagrams, breakeven calculations, Greeks estimates, and probability of profit for any multi-leg strategy.

---

## Platform Overview

### Main Sections
- **Strategy Builder** — `https://optionstrat.com/build` — Custom multi-leg builder
- **Strategy List** — `https://optionstrat.com/strategies` — Pre-built strategies with calculators
- **Options Calculator** — `https://optionstrat.com/calculator` — Single-leg analysis
- **Tutorials** — `https://optionstrat.com/tutorials` — How-to guides
- **Saved Trades** — `https://optionstrat.com/saved` — Saved strategy URLs for tracking

---

## Strategy Builder (`optionstrat.com/build`)

The strategy builder is the core tool. You construct multi-leg positions by adding individual option legs and viewing the combined P/L diagram in real time.

### How to Use

1. **Go to:** `https://optionstrat.com/build`
2. **Enter underlying symbol** (e.g., AAPL, SPY, QQQ)
3. **Add legs** by clicking "Add Leg" and configuring:
   - Buy or Sell
   - Call or Put
   - Strike price (or select from chain)
   - Expiration date
   - Quantity (default: 1 contract = 100 shares)
4. **View P/L diagram** — updates live as you configure
5. **Save / Share** — click Save to store to your account, or copy the URL to share

### Strategy Builder Parameters Explained

| Parameter | What it Means |
|-----------|--------------|
| **Symbol** | Underlying stock or index ticker |
| **Buy/Sell** | Long (buy) or Short (sell) the leg |
| **Call/Put** | Option type |
| **Strike** | The price at which the option can be exercised |
| **Expiration** | The date the option expires |
| **Quantity** | Number of contracts (1 contract = 100 shares) |
| **Bid/Ask/Last** | Market prices shown — use ask for buying, bid for selling |
| **Leg Weight** | Relative weight for ratio spreads (e.g., 2:1) |
| **Price** | Manual price override if needed |

### P/L Diagram

The P/L diagram shows your profit/loss at expiration (Y-axis) at any underlying price (X-axis).

**Reading the P/L diagram:**
- X-axis: Stock price at expiration
- Y-axis: Profit (green/positive) or loss (red/negative)
- **Dark line:** P/L at expiration
- **Lighter line:** P/L today (degrades as time passes)
- **Vertical dotted lines:** Strike prices
- **Horizontal dotted line:** $0 (breakeven)
- **Shaded region:** Profit zone (green) vs loss zone (red)

**Interactive features:**
- Hover over any point to see exact P/L at that price
- Adjust underlying price slider to see current P/L vs expiration P/L
- Toggle between "at expiration" and "today" views

---

## Key Statistics Panel

After building a strategy, OptionStrat shows key metrics:

| Stat | What it Means |
|------|--------------|
| **Max Profit** | Maximum possible profit (may be unlimited for some strategies) |
| **Max Loss** | Maximum possible loss (or "unlimited") |
| **Breakeven** | Stock price(s) where you neither profit nor lose at expiration |
| **Chance of Profit** | Probability of P/L > $0 at expiration |
| **Chance of Max Profit** | Probability of achieving maximum profit |
| **Risk/Reward Ratio** | Max loss divided by max profit |
| **Net Debit/Credit** | Total cost (debit) or proceeds (credit) for the position |
| **IV (Implied Volatility)** | Current IV of the underlying, used for probability calculations |
| **Delta** | Net delta of the position |
| **Gamma** | Net gamma of the position |
| **Theta** | Net theta of the position |
| **Vega** | Net vega of the position |
| **Days to Expiration (DTE)** | Days remaining until the shortest leg expires |
| **Days to Expiration (far leg)** | For calendar/diagonal spreads |

---

## Pre-Built Strategy URLs

These are direct links to each strategy on OptionStrat. Click to open in the strategy builder.

### Vertical Spreads

| Strategy | URL |
|----------|-----|
| Bull Call Spread | `https://optionstrat.com/build/bull-call-spread` |
| Bear Put Spread | `https://optionstrat.com/build/bear-put-spread` |
| Bull Put Spread | `https://optionstrat.com/build/bull-put-spread` |
| Bear Call Spread | `https://optionstrat.com/build/bear-call-spread` |

### Butterfly / Broken Wing

| Strategy | URL |
|----------|-----|
| Long Call Butterfly | `https://optionstrat.com/build/long-call-butterfly` |
| Short Call Butterfly | `https://optionstrat.com/build/short-call-butterfly` |
| Long Put Butterfly | `https://optionstrat.com/build/long-put-butterfly` |
| Short Put Butterfly | `https://optionstrat.com/build/short-put-butterfly` |
| Broken Wing Butterfly | `https://optionstrat.com/build/broken-wing-butterfly` |

### Iron Condors

| Strategy | URL |
|----------|-----|
| Iron Condor | `https://optionstrat.com/build/iron-condor` |
| Broken Wing Iron Condor | `https://optionstrat.com/build/broken-wing-iron-condor` |
| Iron Butterfly | `https://optionstrat.com/build/iron-butterfly` |

### Calendar / Diagonal

| Strategy | URL |
|----------|-----|
| Calendar Spread | `https://optionstrat.com/build/calendar-spread` |
| Diagonal Spread | `https://optionstrat.com/build/diagonal-spread` |
| Double Diagonal | `https://optionstrat.com/build/double-diagonal` |

### Other Strategies

| Strategy | URL |
|----------|-----|
| Long Straddle | `https://optionstrat.com/build/long-straddle` |
| Short Straddle | `https://optionstrat.com/build/short-straddle` |
| Long Strangle | `https://optionstrat.com/build/long-strangle` |
| Short Strangle | `https://optionstrat.com/build/short-strangle` |
| Collar | `https://optionstrat.com/build/collar` |
| Protective Put | `https://optionstrat.com/build/protective-put` |
| Covered Call | `https://optionstrat.com/build/covered-call` |
| Jelly Roll | `https://optionstrat.com/build/jelly-roll` |
| Ratio Spread | `https://optionstrat.com/build/ratio-spread` |

### Full Strategy List
All strategies: `https://optionstrat.com/strategies`

---

## Strategy-Specific URL Parameters

OptionStrat supports URL parameters for direct links with pre-filled strikes. Example:

```
https://optionstrat.com/build?symbol=SPY&legs[]=type%3Dbuy%26strike%3D450%26expiration%3D2024-12-20%26type%3Dsell%26strike%3D460
```

This can be generated by building a strategy and copying the URL from the browser.

**To share a strategy:**
1. Build the position in the builder
2. Click "Share" in the top right
3. Copy the URL — anyone can view the exact position with current prices

---

## Using OptionStrat for Greeks Analysis

### To See Greeks for a Position:
1. Build the position
2. Look at the **Greeks Panel** on the right side
3. It shows: Delta, Gamma, Theta, Vega for the entire position

### To Stress-Test Greeks:
Use the **Price slider** to see how Greeks change as the underlying moves:
- Watch delta approach 1.00 (call) or -1.00 (put) as price increases
- Watch gamma spike and theta burn intensify near ATM

### Implied Volatility Impact:
1. Enter the **IV** manually if OptionStrat doesn't auto-populate it
2. Use the IV input to see how P/L changes with IV moves
3. Important for iron condors and credit spreads (IV crush scenarios)

---

## Tips and Tricks

### 1. Compare Two Strategies
Open two browser tabs with different strategies and compare max profit/loss side by side.

### 2. Save Trades for Tracking
Click "Save" on any strategy. Saved trades appear in your dashboard and can be tracked over time with live P/L updates.

### 3. Adjust Any Parameter
Click any strike, expiration, or price to edit it. The P/L diagram updates instantly.

### 4. View "Today" vs "At Expiration"
Toggle between current P/L (accounting for time remaining) and expiration P/L to understand theta's effect on your position.

### 5. Customize the X-Axis Range
Drag the price range slider to zoom in/out on the profit zone for precision.

### 6. Probability Overlay
OptionStrat overlays a probability distribution curve on the P/L chart showing the likelihood of the stock being at each price at expiration (based on IV).

---

## Limitations

- **Data is indicative only** — prices may be slightly delayed
- **Greeks are model-based** — calculated from IV, time, and underlying price; actual assignment/exercise may differ
- **No live trading execution** — OptionStrat is a visualization tool, not a broker
- **Free tier** has limited features; premium offers more advanced analytics

---

## Quick Workflow for Analysis

1. Identify the strategy the user wants to analyze
2. Open the appropriate OptionStrat URL from the table above
3. Input the current underlying price, IV, and specific strikes
4. Review: Max profit/loss, breakeven, chance of profit, Greek profile
5. Share the URL with the user for visual reference
6. Interpret the Greeks and explain how theta/vega will affect the position over time

---

## External Resources
- **OptionStrat Home:** `https://optionstrat.com`
- **Strategy Builder:** `https://optionstrat.com/build`
- **All Strategies:** `https://optionstrat.com/strategies`
- **Options Builder Tutorial:** `https://optionstrat.com/tutorials/options-builder`
- **Blog Tutorial:** `https://optionstrat.com/blog/optionstrat-strategy-builder-tutorial-how-to-calculate-options-profit`
