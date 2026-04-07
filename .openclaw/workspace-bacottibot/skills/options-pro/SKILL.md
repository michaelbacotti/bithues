# SKILL.md — options-pro

## What it does
Provides stock market analysis, options trading strategy, portfolio analysis, and Greek interpretation for the Bacotti family office and Dependability Holding LLC.

## When to use

**Trigger phrases / contexts:**
- User asks about any specific trade, strategy, or option structure
- User mentions: "options", "spreads", "iron condor", "butterfly", "straddle", "strangle", " Greeks", "delta", "gamma", "theta", "vega", "rho"
- User asks about a particular stock's option chain or implied volatility (IV)
- User wants to analyze or compare option strategies
- User asks about a specific underlying (SPX, QQQ, AAPL, TSLA, etc.)
- User asks "what's the max loss on this spread?" or "what's the breakeven?"
- User wants Greeks interpreted for an existing position
- User asks about earnings plays, dividend risk, early assignment
- User wants to know about probability of expiring ITM/OTM
- User asks about calendar or diagonal spreads
- User mentions: "poor man's covered call", "diagonal", "ratio spread", "jelly roll"
- User wants to backtest or evaluate an options position

**NOT for:**
- Non-trading entity questions (use the relevant entity skill)
- Tax filing or regulatory advice (defer to qualified professionals)
- Broker-specific execution (no trading execution capability)

---

## Greek Quick Reference

### Greek Behavior at ATM (At-The-Money) — 50 Delta

| Greek | +$1 Underlying | +1 Day (Theta Decay) | +10% IV | -10% IV |
|-------|---------------|----------------------|---------|---------|
| **Delta (Call)** | +0.50 → moves toward 1.0 | Decreases slightly | Increases | Decreases |
| **Delta (Put)** | -0.50 → moves toward -1.0 | Decreases (less negative) | Increases (more negative) | Decreases (less negative) |
| **Gamma** | Jumps higher near ATM | Highest near expiry ATM | Higher | Higher |
| **Theta** | Slightly changes | Most negative at ATM/near-expiry | Increases debit cost | Decreases debit cost |
| **Vega** | Slightly changes | Near zero at expiry | Positive for long options | Negative for long options |
| **Rho** | Minimal | Minimal | Minimal | Minimal |

### Greek Definitions at a Glance

- **Delta (Δ):** How much the option price changes per $1 move in the underlying.
  - Calls: 0.00 to +1.00 | Puts: -1.00 to 0.00 | ATM ≈ 0.50
  - Also ≈ probability of expiring ITM for OTM options
- **Gamma (Γ):** Rate of change of delta per $1 move in the underlying.
  - Highest ATM, explodes near expiration
- **Theta (Θ):** Time decay — how much value the option loses per day.
  - Always negative for long options, positive for short options
  - ATM near expiry = theta burn is maximum
- **Vega (ν):** Sensitivity to a 1% change in implied volatility (IV).
  - Long options benefit from IV rise, short options get hurt
  - ATM options have highest vega
  - At expiration, vega = 0
- **Rho (ρ):** Sensitivity to interest rate changes (usually minor).
  - Matters most for long-dated options (LEAPS)

---

## Strategy Quick Reference

### Vertical Spreads

| Strategy | Direction | Debit/Credit | Max Profit | Max Loss | Greek Bias |
|----------|-----------|--------------|------------|----------|------------|
| Bull Call Spread | Bullish | Debit | Width − Net Debit | Net Debit paid | Long delta, short gamma/theta |
| Bear Put Spread | Bearish | Debit | Width − Net Debit | Net Debit paid | Long delta (negative), short gamma |
| Bull Put Spread | Bullish | Credit | Net Credit received | Width − Net Credit | Short put delta, short vega |
| Bear Call Spread | Bearish | Credit | Net Credit received | Width − Net Credit | Short call delta, short vega |

### Butterfly / Broken Wing

| Strategy | Direction | Debit/Credit | Max Profit | Max Loss |
|----------|-----------|--------------|------------|----------|
| Long Call Butterfly | Neutral | Debit | Width − Net Debit | Net Debit paid |
| Short Call Butterfly | Neutral | Credit | Net Credit received | Width − Net Credit |
| Put Broken Wing (PBBW) | Directional bias | Debit/Credit | Asymmetric | Defined one side |
| Call Broken Wing | Directional bias | Debit/Credit | Asymmetric | Defined one side |

### Iron Condors

| Strategy | Direction | Debit/Credit | Max Profit | Max Loss |
|----------|-----------|--------------|------------|----------|
| Iron Condor | Neutral/range | Credit | Net Credit | Width − Net Credit |
| Broken Wing Iron Condor | Directional bias | Credit | Asymmetric | Defined, wider one side |

### Calendar / Diagonal

| Strategy | Direction | Debit/Credit | Key Feature |
|----------|-----------|--------------|-------------|
| Calendar Spread | Neutral | Debit | Same strike, different expirations |
| Diagonal Spread | Directional | Debit | Different strike + different expiration |
| Double Diagonal | Neutral/wide | Debit | Near-term strangle, far-term wider strangle |

### Other Strategies

| Strategy | Direction | Debit/Credit | Max Profit | Max Loss |
|----------|-----------|--------------|------------|----------|
| Long Straddle | Volatility | Debit | Unlimited | Net Debit |
| Long Strangle | Volatility | Debit | Unlimited | Net Debit |
| Ratio Spread | Directional | Variable | Width − Net Cost | Net Debit or unbounded |
| Jelly Roll | Arbitrage | Credit | Small | Defined |

---

## Data Sources

### Real-Time / API (Recommended)
- **Tradier** — Free developer sandbox + live trading API. Recommended for programmatic options data.
  - Docs: `https://docs.tradier.com`
  - Streaming quotes, options chains, Greeks, historical data
  - Setup: See `references/data-sources.md`

### Web-Based (No API Required)
- **OptionStrat** (`optionstrat.com`) — Strategy builder + P/L diagrams. Use for visualizing any spread.
  - All strategies: `https://optionstrat.com/strategies`
  - Build custom: `https://optionstrat.com/build`
- **TastyTrade** (`tastylive.com`) — Education, Greek behavior tutorials, strategy selection.
- **CBOE** (`cboexchange.com`) — Index data, VIX, implied volatility metrics.
- **Investopedia** — Greek definitions and strategy explanations (educational).

### Limitations
- Web search gives **delayed, indicative** data — not suitable for live trading
- Web search **cannot return real-time Greeks** (delta, gamma, theta, vega, rho)
- For Greeks, use OptionStrat (manual entry) or Tradier API

---

## Workflow

1. **Identify the question** — What is the user trying to do?
2. **Fetch data** — Use web search for current prices/IV or open OptionStrat directly
3. **Analyze** — Apply Greek logic (which Greeks favor or hurt the position)
4. **Recommend** — Specific strikes, expiry, width, max profit/loss, breakeven
5. **Warn** — Assignment risk, early exercise, IV crush, correlation risk

---

## Risk Notes
- Options involve substantial risk. Not suitable for all investors.
- This skill provides **analysis only** — no execution capability.
- Always confirm trade details with the user before any specific recommendation.
- Tax consequences of options transactions can be complex; consult a tax professional.
- Past performance does not guarantee future results.

---

## Related Files
- `references/greeks.md` — Full Greek reference with detailed behavior tables
- `references/strategies.md` — Complete strategy encyclopedia
- `references/optionstrat.md` — OptionStrat platform guide
- `references/data-sources.md` — Real-time data setup (Tradier API)
