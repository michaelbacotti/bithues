# Data Sources for Options Analysis

Since we do not have a live trading API connected, we rely on a combination of web search and free developer APIs for options data. This guide covers the best available options and their limitations.

---

## Overview of Options

| Source | Data Quality | Real-Time | Greeks | Cost |
|--------|-------------|-----------|--------|------|
| Tradier API | Full market depth | Yes (streaming) | Yes | Free developer tier + brokerage |
| Web Search | Indicative, delayed | No | No | Free |
| OptionStrat | Indicative, delayed | No | Yes (model-based) | Free tier / Premium |
| TastyTrade | Educational | No | Yes (model-based) | Free |
| CBOE | Index/VIX data | Delayed | No | Free |
| Brokerage Platforms | Full | Yes | Yes | Commission-based |

---

## Tradier API (Recommended)

Tradier is the recommended data source for programmatic options data. They offer a free developer sandbox and live trading API.

### Why Tradier?
- **Free developer tier** — sandbox for testing without real money
- **Full options chain** — all strikes, expirations, open interest, volume
- **Greeks included** — delta, gamma, theta, vega, rho for each option
- **Real-time quotes** — streaming market data
- **Python and Node.js SDKs** — easy to integrate

### Getting Started with Tradier

**Step 1: Sign Up for a Developer Account**
1. Go to: `https://docs.tradier.com/docs/getting-started`
2. Create a free developer account at: `https://account.tradier.com/register`
3. Get your API access token from the dashboard

**Step 2: Developer Sandbox**
- Sandbox endpoint: `https://sandbox.tradier.com`
- Use the sandbox token for testing
- Sandbox simulates real market conditions without real money

**Step 3: Enable Live Trading (Optional)**
- To trade with real money, open a Tradier brokerage account
- Link your developer account to enable live trading
- Commission: $0 per trade (Pro plan) with competitive options pricing

**Step 4: Install SDK**
```bash
# Python
pip install tradier

# Node.js
npm install tradier
```

**Step 5: Basic Python Example**
```python
from tradier import Tradier

# Initialize with your token
client = Tradier(token='YOUR_ACCESS_TOKEN', account_id='YOUR_ACCOUNT_ID')

# Get option chain for a symbol
chains = client.options.chains('AAPL')
print(chains)

# Get a quote
quote = client.market.quote('AAPL')
print(quote)

# Get Greeks for a specific option
option = client.options.chains('AAPL', strike=150, expiration='2024-12-20')
print(option.delta, option.gamma, option.theta, option.vega)
```

**Step 6: Get Historical Data**
```python
# Historical OHLCV for options or underlying
history = client.market.history(
    symbol='AAPL',
    interval='daily',
    start='2024-01-01',
    end='2024-12-31'
)
```

### Tradier API Key Setup

**Get your credentials:**
1. Sign up at: `https://account.tradier.com`
2. Go to: Settings → API Access
3. Copy your **Account ID** and **Access Token**

**Environment variables (recommended):**
```bash
export TRADIER_TOKEN="your_token_here"
export TRADIER_ACCOUNT_ID="your_account_id"
```

Store these in your environment or in `~/.openclaw/workspace-bacottibot/.env` for local use.

---

## Web Search (No-API Approach)

When an API isn't available, web search provides delayed, indicative data.

### What Web Search Can Tell You
- Current stock price (delayed ~15 min)
- Approximate IV rank / percentile
- Recent news and earnings dates
- General market sentiment

### What Web Search Cannot Tell You
- Real-time Greeks
- Real-time option prices (only rough estimates)
- Implied volatility for specific strikes
- Probability of profit calculations

### How to Use It
Use web search to quickly get:
1. Current underlying price
2. Earnings date and expected move
3. Current IV compared to historical IV
4. General market conditions

Then use OptionStrat with manual price/IV entry for P/L diagrams and Greeks.

---

## OptionStrat (Manual Entry)

**Best for:** Strategy visualization without any API setup.

**How to use:**
1. Go to `https://optionstrat.com/build`
2. Enter the underlying symbol
3. Manually enter the current stock price
4. Select strikes and expirations
5. OptionStrat calculates Greeks based on your inputs

**Limitation:** Prices are indicative, not live. Enter bid/ask/mid estimates from your brokerage or web search.

---

## TastyTrade (`tastylive.com`)

**Best for:** Educational content, Greek behavior explanations, strategy selection.

### What TastyTrade Offers
- **Education:** Deep dives into Greek behavior, strategy selection, probability of profit
- **Strategy tools:** P/L calculators similar to OptionStrat
- **Market data:** Delayed quotes, IV metrics
- **Webinars and courses:** Free options education

### Limitations
- No live trading execution
- Greeks are model-based (similar limitations to OptionStrat)
- Best used for learning, not live trading

### Key TastyTrade Resources
- Greeks education: Search "The Greeks" on `tastylive.com`
- Strategy search: Browse by market outlook, volatility, directional bias
- Probability of profit: Built into all strategy tools

---

## CBOE (Chicago Board Options Exchange)

**Best for:** Index data, VIX, market-wide volatility metrics.

### What CBOE Offers
- **VIX Index** — real-time fear/volatility gauge
- **S&P 500 options data** — LEAPS, weeklys, SPX
- **Historical volatility data** — for IV comparison
- **Weekly index options** — 0DTE SPX strategies

### Key CBOE Resources
- **VIX:** `https://www.cboexchange.com/indexdata`
- **CBOE Volatility Index:** `https://www.cboe.com/tradable_products/vix/`
- **SPX Options:** `https://www.cboe.com/tradable_products/sp_500/spx_options/`
- **0DTE Options:** `https://www.cboe.com/us0dte/`

### Using VIX for IV Context
- VIX ≈ market's expected 30-day volatility
- If a stock's IV is above VIX, it's relatively high volatility
- If a stock's IV is below its own historical average, it may be a good time to sell premium

---

## Brokerage Platforms

If you have a brokerage account, most major brokers offer:
- Thinkorswim (TD Ameritrade) — Free, full platform, excellent Greeks
- tastytrade platform — Free, designed for options
- Interactive Brokers — API available for programmatic access
- Webull — Free platform, limited API

**Recommendation:** If you plan to trade options, a dedicated brokerage platform is the most reliable data source.

---

## Recommended Stack for This Skill

| Task | Tool |
|------|------|
| Quick price check | Web search |
| Strategy visualization | OptionStrat (`optionstrat.com/build`) |
| Full Greek data | Tradier API (sandbox or live) |
| Education / learning | TastyTrade (`tastylive.com`) |
| Index/IV context | CBOE |
| Live trading (when ready) | Tradier brokerage + API |

---

## Setting Up Tradier (Step by Step)

### 1. Create Developer Account
```
https://account.tradier.com/register
```
Choose "Developer" account type (free).

### 2. Access the Developer Dashboard
```
https://docs.tradier.com
```
Your access token is found in your account dashboard.

### 3. Test the API
```bash
# Get market status
curl -X GET "https://sandbox.tradier.com/v1/markets/status" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get a quote
curl -X GET "https://sandbox.tradier.com/v1/markets/quotes?symbols=AAPL" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Get Option Chains
```bash
curl -X GET "https://sandbox.tradier.com/v1/options/lookup/AAPL" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. Install Python SDK
```bash
pip install tradier
```

### 6. Set Environment Variables
```bash
# In your shell profile (~/.zshrc, ~/.bashrc)
export TRADIER_TOKEN="your_sandbox_token"
export TRADIER_ACCOUNT_ID="your_account_id"
```

### 7. Query Options in Python
```python
from tradier import Tradier
import os

client = Tradier(
    token=os.environ.get('TRADIER_TOKEN'),
    account_id=os.environ.get('TRADIER_ACCOUNT_ID')
)

# Get full option chain
chains = client.options.chains('AAPL')
print(chains)

# Get specific expiration
expirations = client.options.expirations('AAPL')
print(expirations)

# Get quote with Greeks
quotes = client.market.quotes(['AAPL241220C00150000'])  # specific option symbol
print(quotes.delta, quotes.gamma, quotes.theta, quotes.vega)
```

---

## Data Freshness Guide

| Data Type | Acceptable Freshness | Source |
|-----------|---------------------|--------|
| Current stock price | Real-time or <15 min delayed | Any |
| IV Rank / Percentile | End of day (good enough) | CBOE, your broker |
| Option prices | Real-time preferred | Broker or Tradier |
| Greeks | Real-time preferred | Tradier API, OptionStrat |
| VIX / Index data | 15 min delayed OK | CBOE |
| Earnings date | Static (known in advance) | Web search |
| Historical volatility | End of day | CBOE, Tradier |

---

## Important Caveats

1. **Web search data is always delayed** — never use it for live trading decisions
2. **Greeks from OptionStrat are estimates** — based on entered IV, may differ from actual
3. **IV crush is real** — after earnings, long options lose value from IV collapse even if the stock moves in your favor
4. **Probability of profit is model-based** — assumes returns follow a log-normal distribution; real-world events can cause outsized moves outside the modeled range
5. **Assignment and exercise risk** — American-style options can be exercised at any time before expiration; deep ITM options near expiration carry early exercise risk
6. **Weekly options have extreme gamma** — 0DTE and weekly options are extremely sensitive to small moves in the underlying
