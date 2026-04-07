# Greeks Reference — Full Guide

The Greeks measure an option's sensitivity to various factors: underlying price, time, volatility, and interest rates. Understanding them is essential for selecting strategies and managing positions.

---

## Delta (Δ)

### Definition
Delta measures how much an option's price changes for a **$1 move in the underlying asset**.

### Range
- **Calls:** 0.00 to +1.00 (0 to 100 delta)
- **Puts:** -1.00 to 0.00 (negative 100 to 0 delta)
- **ATM (At-the-money):** ≈ 0.50 (50 delta) for both calls and puts

### Key Properties

| Condition | Call Delta | Put Delta | Interpretation |
|-----------|-----------|-----------|----------------|
| Deep ITM | Close to +1.00 | Close to -1.00 | Moves almost 1:1 with underlying |
| ATM | ≈ +0.50 | ≈ -0.50 | Half the underlying move |
| Deep OTM | Close to 0.00 | Close to 0.00 | Barely responds to underlying move |
| At Expiration | Either 0 or 1 | Either 0 or -1 | No in-between |

### Delta as Probability Proxy
Delta ≈ the **probability of expiring in-the-money** (for OTM options at current prices).

- A 30-delta put ≈ 30% chance of expiring ITM
- A 70-delta call ≈ 70% chance of expiring ITM
- ATM (50 delta) ≈ 50/50 odds

This is not a precise probability — it's a useful approximation that breaks down for deep ITM options and near expiration.

### How Delta Changes

**With Price Movement:**
- As underlying rises: Call delta increases (toward +1.00), put delta increases (toward 0.00, i.e., becomes less negative)
- As underlying falls: Call delta decreases (toward 0.00), put delta decreases (toward -1.00, i.e., becomes more negative)

**With Time (Theta Effect):**
- As expiration approaches, ATM delta converges rapidly toward 0.50 until it snaps to 0 or 1 at expiry
- ITM options: delta approaches 1.00 (calls) or -1.00 (puts) as time passes
- OTM options: delta approaches 0.00 as time passes

**With Implied Volatility:**
- Higher IV → Higher delta magnitude (more extreme) for ITM/OTM options
- Lower IV → Delta converges closer to 0.50 ATM

---

## Gamma (Γ)

### Definition
Gamma measures how much **delta changes** per $1 move in the underlying. It is the "acceleration" of delta.

### Key Properties

| Condition | Gamma Level | Why |
|-----------|-------------|-----|
| Deep ITM | Low | Delta already near 1.00, can't increase much |
| Deep OTM | Low | Delta already near 0.00, can't decrease much |
| **ATM** | **Highest** | Delta is most sensitive here — a small move can flip it |
| Near Expiry | **Explodes** | ATM delta swings from 0.50 to 0 or 1 very quickly |

### Gamma Behavior Table

| Scenario | ATM Response to +$1 | ATM Response to +1 Day | ATM Response to +10% IV |
|----------|---------------------|------------------------|-------------------------|
| Gamma | Delta moves sharply | Gamma decreases slightly | Increases significantly |
| Direction | Gamma peaks just slightly below strike for calls, just above for puts | Higher for near-expiry | Higher IV means gamma spread is wider |

### Gamma in Practice
- A position with **high gamma** (long gamma) means your delta is unstable — small moves in the underlying cause large delta swings
- Long options = long gamma (you want the underlying to move)
- Short options = short gamma (you want the underlying to stay still)
- Gamma is highest for **ATM options near expiration** — this is why 0DTE and short-dated options are so volatile

---

## Theta (Θ)

### Definition
Theta measures how much value an option **loses per day** due to time decay.

### Key Rule
> **All long options lose value with time. All short options gain value with time.**

Theta is always expressed as a negative number for long positions (you are losing money per day) and a positive number for short positions (you are collecting per day).

### Theta by Moneyness and Time

| Condition | Theta Behavior | Notes |
|-----------|----------------|-------|
| **ATM, near expiry** | **Most negative (biggest burn)** | This is where theta is most destructive |
| OTM, near expiry | Still significant | Time value is leaving the option |
| Deep ITM | Can have positive theta | Early exercise risk may complicate this |
| Far-dated (LEAPS) | Small theta per day | You pay for time, but daily burn is low |
| At expiration | Theta = 0 | Either expired worthless or exercised |

### Theta Decay Curve
Theta is **not linear** — it accelerates as expiration approaches:
- 60 DTE: Small daily decay
- 30 DTE: Moderate decay
- 7 DTE: Significant decay
- 1 DTE: Extreme decay for ATM options
- Expiration: Theta = 0

### Theta in Strategies
- **Want theta to work for you:** Sell premium (short options) — collect time decay
  - Covered calls, cash-secured puts, iron condors, credit spreads
- **Want theta to work against you:** Buy options (long options) — pay for time
  - Long straddles, long strangles,买 lottery plays

### Theta Behavior Table

| Greek | ATM Response to +$1 | ATM Response to +1 Day | ATM Response to +10% IV |
|-------|---------------------|------------------------|-------------------------|
| Theta (Long) | Slightly less negative | Moves toward most negative | Becomes more negative |

---

## Vega (ν)

### Definition
Vega measures how much an option's price changes for a **1% change in implied volatility (IV)**.

### Key Rule
> **Long options benefit from IV rise. Short options get hurt by IV rise.**
> **At expiration, vega = 0** (there is no more uncertainty to price).

### Vega by Moneyness

| Condition | Vega Level | Why |
|-----------|-----------|-----|
| **ATM** | **Highest** | Maximum uncertainty about which side you'll end up on |
| ITM | Moderate | Already decided direction, less room for IV to move price |
| OTM | Moderate | May become relevant if IV moves it toward ATM |
| At expiration | **Zero** | No time left for volatility to matter |

### Vega in Strategies
- **Long Vega** (want IV to rise):
  - Long straddles, long strangles, buying spreads
  - Betting on a volatility event (earnings, FDA decision, macro event)
- **Short Vega** (want IV to fall or stay low):
  - Short straddles, short strangles, iron condors (net short vega)
  - Betting that post-event IV will collapse ("IV crush")

### IV Crush
After a major catalyst (earnings, FDA approval, binary event), implied volatility typically collapses 30-60%. This destroys the value of long options even if the stock moves in your favor.

**Example:** You buy straddles before earnings on a stock at $100. IV is 80%. Stock jumps to $105. You'd expect to profit — but if IV collapses from 80% to 40%, the put value collapses, potentially leaving you with a net loss despite the directional move.

### Vega Behavior Table

| Greek | ATM Response to +$1 | ATM Response to +1 Day | ATM Response to +10% IV |
|-------|---------------------|------------------------|-------------------------|
| Vega (Long) | Slight change | Near zero at expiry | **+value significantly** |
| Vega (Short) | Slight change | Near zero at expiry | **-value significantly** |

---

## Rho (ρ)

### Definition
Rho measures how much an option's price changes for a **1% change in interest rates**.

### Key Properties
- **Usually the least important Greek** for short to medium-term options
- Matters most for **long-dated options (LEAPS)** and equity positions
- Call options: positive rho (benefit from higher rates)
- Put options: negative rho (hurt by higher rates)

| Condition | Rho Impact | Notes |
|-----------|-----------|-------|
| Short-dated options | Minimal | Almost no effect |
| Long-dated options (LEAPS) | Moderate | Higher rates = higher call prices |
| Equity substitutes | Significant | Deep ITM calls may be exercised |

In the current high-rate environment (2023-2025), rho has become slightly more relevant but still ranks last among Greeks for most option traders.

---

## Combined Greek Summary Table

### ATM Response to +$1 Underlying Move

| Greek | Long Call (ATM) | Long Put (ATM) | Short Call (ATM) | Short Put (ATM) |
|-------|-----------------|-----------------|-------------------|-----------------|
| **Delta** | +0.50 (toward 1.0) | -0.50 (toward 0) | -0.50 (toward 0) | +0.50 (toward 0) |
| **Gamma** | Positive spike | Positive spike | Negative spike | Negative spike |
| **Theta** | Negative (you lose) | Negative (you lose) | Positive (you collect) | Positive (you collect) |
| **Vega** | Positive (you benefit) | Positive (you benefit) | Negative (you hurt) | Negative (you hurt) |
| **Rho** | Positive | Negative | Negative | Positive |

### ATM Response to +1 Day (Time Passes)

| Greek | Long Call (ATM) | Long Put (ATM) | Short Call (ATM) | Short Put (ATM) |
|-------|-----------------|-----------------|-------------------|-----------------|
| **Delta** | Decreases slightly | Increases (less negative) | Increases slightly | Decreases (more negative) |
| **Gamma** | Decreases | Decreases | Decreases | Decreases |
| **Theta** | More negative (big burn) | More negative (big burn) | More positive (collect more) | More positive (collect more) |
| **Vega** | Slightly decreases | Slightly decreases | Slightly decreases | Slightly decreases |
| **Rho** | Minimal | Minimal | Minimal | Minimal |

### ATM Response to +10% Implied Volatility

| Greek | Long Call (ATM) | Long Put (ATM) | Short Call (ATM) | Short Put (ATM) |
|-------|-----------------|-----------------|-------------------|-----------------|
| **Delta** | Increases (more positive) | Decreases (more negative) | Decreases (more negative) | Increases (more positive) |
| **Gamma** | Increases | Increases | Decreases | Decreases |
| **Theta** | More negative (costs more to hold) | More negative (costs more to hold) | More positive (collect more) | More positive (collect more) |
| **Vega** | **Significantly positive** | **Significantly positive** | **Significantly negative** | **Significantly negative** |

---

## Practical Greek Cheat Sheet

### For Choosing Strategies

| If you think... | Greeks you want | Strategies |
|-----------------|-----------------|------------|
| Stock will move up | Long delta | Bull call spreads, buy calls |
| Stock will move down | Short delta (long put) | Bear put spreads, buy puts |
| Stock won't move much | Short delta, short vega | Credit spreads, iron condors, covered calls |
| IV will rise (volatility event coming) | Long vega | Long straddles, long strangles |
| IV will fall / post-event crush | Short vega | Iron condors, credit spreads, short straddles |
| Time will pass with no move | Short gamma, short theta | Credit spreads, iron condors |
| Quick move coming (near term) | Long gamma, long theta | Weeklys, 0DTEs |

### Position Greek Signs

| Position | Delta | Gamma | Theta | Vega |
|----------|-------|-------|-------|------|
| Long Call | + | + | - | + |
| Long Put | - | + | - | + |
| Short Call | - | - | + | - |
| Short Put | + | - | + | - |
| Long Stock | + | 0 | 0 | 0 |
| Short Stock | - | 0 | 0 | 0 |

---

## Key Takeaways

1. **Delta** tells you directional exposure and serves as a probability proxy
2. **Gamma** tells you how fast your delta is changing — high gamma = high risk/reward near expiry
3. **Theta** is always working against long option holders and for short option sellers
4. **Vega** is the Greeks most tied to market fear/market environment — IV crush is a real risk
5. **Rho** is mostly irrelevant for short-dated options; matters for LEAPS in high-rate environments
6. Greeks are **interconnected** — a move in one affects others
7. OptionStrat (`optionstrat.com`) can calculate all Greeks for any position if you know the inputs

---

## External Resources
- **TastyTrade Greek education:** `https://tastylive.com/concepts-strategies`
- **OptionStrat calculator:** `https://optionstrat.com/build`
- **Investopedia Greek guide:** `https://www.investopedia.com/trading/using-the-greeks-to-understand-options/`
