# Strategy Encyclopedia — Complete Options Strategies Reference

## Table of Contents
1. [Vertical Spreads](#vertical-spreads)
2. [Butterfly / Broken Wing](#butterfly--broken-wing)
3. [Iron Condors](#iron-condors)
4. [Calendar / Diagonal Spreads](#calendar--diagonal-spreads)
5. [Other Strategies](#other-strategies)

---

## Vertical Spreads

### Bull Call Spread

**What it is:** Buy a call option at a lower strike, sell a call option at a higher strike (same expiration).

| Attribute | Value |
|-----------|-------|
| Direction | Bullish |
| Debit/Credit | Debit (you pay) |
| Max Profit | Width of strikes − Net Debit |
| Max Loss | Net Debit paid |
| Breakeven | Lower Strike + Net Debit |
| When to Use | Moderately bullish outlook, want defined risk, reduced cost vs. buying naked call |
| Greek Profile | Long delta, short gamma, short theta, short vega |

**Example:**
- Stock at $100
- Buy $95 call for $7.00, Sell $105 call for $2.50
- Net Debit: $4.50
- Max Profit: $105 − $95 − $4.50 = $5.50 (if stock > $105 at expiry)
- Max Loss: $4.50 (if stock < $95 at expiry)
- Breakeven: $95 + $4.50 = $99.50

**Greeks:**
- Net Delta: Positive (bullish directional exposure)
- Net Gamma: Negative (short gamma on the upper strike)
- Net Theta: Negative (you pay theta on the long leg; short call helps slightly)
- Net Vega: Negative (net buyer of premium, but also net seller of upside calls)

---

### Bear Put Spread

**What it is:** Buy a put option at a higher strike, sell a put option at a lower strike (same expiration).

| Attribute | Value |
|-----------|-------|
| Direction | Bearish |
| Debit/Credit | Debit (you pay) |
| Max Profit | Width of strikes − Net Debit |
| Max Loss | Net Debit paid |
| Breakeven | Higher Strike − Net Debit |
| When to Use | Moderately bearish outlook, want defined risk, reduced cost vs. buying naked put |
| Greek Profile | Long delta (negative), short gamma, short theta, short vega |

**Example:**
- Stock at $100
- Buy $105 put for $7.00, Sell $95 put for $2.50
- Net Debit: $4.50
- Max Profit: $105 − $95 − $4.50 = $5.50 (if stock < $95 at expiry)
- Max Loss: $4.50 (if stock > $105 at expiry)
- Breakeven: $105 − $4.50 = $100.50

---

### Bull Put Spread

**What it is:** Sell a put option at a higher strike, buy a put option at a lower strike (same expiration). Also called a "cash-secured put spread."

| Attribute | Value |
|-----------|-------|
| Direction | Moderately Bullish / Neutral |
| Debit/Credit | Credit (you receive) |
| Max Profit | Net Credit received |
| Max Loss | Width of strikes − Net Credit |
| Breakeven | Higher Strike − Net Credit |
| When to Use | Expect stock to stay above the short strike; collecting premium on a pullback |
| Greek Profile | Short put delta, short vega, short theta (you collect) |

**Example:**
- Stock at $100
- Sell $95 put for $3.00, Buy $90 put for $1.50
- Net Credit: $1.50
- Max Profit: $1.50 (if stock > $95 at expiry)
- Max Loss: $95 − $90 − $1.50 = $3.50 (if stock < $90 at expiry)
- Breakeven: $95 − $1.50 = $93.50

---

### Bear Call Spread

**What it is:** Sell a call option at a lower strike, buy a call option at a higher strike (same expiration).

| Attribute | Value |
|-----------|-------|
| Direction | Moderately Bearish / Neutral |
| Debit/Credit | Credit (you receive) |
| Max Profit | Net Credit received |
| Max Loss | Width of strikes − Net Credit |
| Breakeven | Lower Strike + Net Credit |
| When to Use | Expect stock to stay below the short strike; collecting premium on a rally |
| Greek Profile | Short call delta, short vega, short theta (you collect) |

**Example:**
- Stock at $100
- Sell $95 call for $7.00, Buy $105 call for $2.50
- Net Credit: $4.50
- Max Profit: $4.50 (if stock < $95 at expiry)
- Max Loss: $105 − $95 − $4.50 = $5.50 (if stock > $105 at expiry)
- Breakeven: $95 + $4.50 = $99.50

---

## Butterfly / Broken Wing

### Long Call Butterfly

**What it is:** Buy 1 ATM call, Sell 2 OTM calls at higher strikes, Buy 1 ITM call at an even higher strike. All same expiration. Wings are equidistant from the middle (short) strike.

| Attribute | Value |
|-----------|-------|
| Direction | Neutral (target: middle strike) |
| Debit/Credit | Debit (you pay) |
| Max Profit | Width of outer strikes − Net Debit |
| Max Loss | Net Debit paid |
| Breakeven | Lower Wing + Net Debit AND Upper Wing − Net Debit |
| When to Use | Expect stock to stay near the middle (short) strike at expiration |
| Greek Profile | Short gamma (all short strikes), short theta near wings |

**Structure (wings = $5 wide typically):**
```
Example: Stock at $100
Buy 1 $100 call  (ATM)
Sell 2 $105 calls (OTM, 5 pts above)
Buy 1 $110 call  (ITM, 10 pts above)
Net Debit: $X
```
**Max Profit occurs** if stock closes exactly at the middle strike ($105 in this example).

### Short Call Butterfly

**What it is:** Opposite of Long Call Butterfly. Sell 1 ATM call, Buy 2 OTM calls, Sell 1 ITM call. Collect credit, max profit at wings.

| Attribute | Value |
|-----------|-------|
| Direction | Neutral (target: wings) |
| Debit/Credit | Credit (you receive) |
| Max Profit | Net Credit received |
| Max Loss | Width of outer strikes − Net Credit |
| Breakeven | Middle Strike ± Net Credit |

---

### Put Broken Wing (PBBW) — Call Version

**What it is:** A butterfly where the lower wing is not equidistant from the middle strike. You skip the lowest strike entirely, making the position asymmetric.

**Setup:**
- Sell 1 ATM put
- Buy 1 OTM put (higher strike) — standard wing
- Buy 1 far-OTM put (much lower strike) — but you skip the intermediate strikes

**Or Call version:**
- Stock at $100
- Sell 1 $100 call (ATM)
- Buy 1 $105 call (OTM, 5 pts up)
- Buy 1 $90 put (far ITM, 10 pts down — not $95, skipping a strike)

| Attribute | Value |
|-----------|-------|
| Direction | Directional bias (unbalanced) |
| Debit/Credit | Usually a small credit or debit |
| Max Profit | Defined, asymmetric |
| Max Loss | Defined on one side |
| When to Use | When you have a directional bias but want to reduce cost / define risk on the opposing side |

**Key advantage:** Can be entered for a credit or very small debit while defining risk on one side.

---

### Call Broken Wing

**What it is:** A broken wing butterfly skewed to the upside. Similar to the put broken wing but structured with calls.

**Example:**
- Stock at $100
- Sell 1 $100 call (ATM)
- Buy 1 $115 call (far OTM, 15 pts up — wider wing)
- Buy 1 $95 call (ITM, 5 pts down)

The upper wing ($115) is wider than the lower wing ($100 - $95 = $5), creating an asymmetric risk/reward profile with bullish bias.

---

## Iron Condors

### Iron Condor

**What it is:** Combine a bull put spread (sell lower-strike put, buy even lower put) with a bear call spread (sell higher-strike call, buy even higher call). The stock can move within a range and you profit.

| Attribute | Value |
|-----------|-------|
| Direction | Neutral (range-bound) |
| Debit/Credit | Credit (you receive) |
| Max Profit | Net Credit received |
| Max Loss | Sum of both wing widths − Net Credit |
| Breakeven (downside) | Lower Short Strike − Net Credit |
| Breakeven (upside) | Upper Short Strike + Net Credit |
| When to Use | Expect stock to stay within a range; collect premium in a choppy market |
| Greek Profile | Short vega (net short volatility), short theta (you collect decay) |

**Structure:**
```
Stock at $100
Bull Put Spread:    Sell $95 put / Buy $90 put
Bear Call Spread:   Sell $105 call / Buy $110 call
Both spreads = $5 wide each = $10 total width max loss
```

**Example:**
- Sell $95 put for $3.00, Buy $90 put for $1.00 → Credit: $2.00
- Sell $105 call for $3.00, Buy $110 call for $1.00 → Credit: $2.00
- Total Net Credit: $4.00
- Max Profit: $4.00 (if stock between $95 and $105 at expiry)
- Max Loss: $10 − $4 = $6 (if stock below $90 or above $110 at expiry)
- Downside Breakeven: $95 − $4.00 = $91.00
- Upside Breakeven: $105 + $4.00 = $109.00

---

### Broken Wing Iron Condor

**What it is:** An iron condor where one side's short strike is farther from the protective leg than the other side, creating an asymmetric position.

**Example:**
- Stock at $100
- Sell $95 put / Buy $90 put — standard $5 put spread
- Sell $110 call / Buy $115 call — $5 wide call spread

OR make the upside wider:
- Sell $95 put / Buy $90 put — standard
- Sell $110 call / Buy $120 call — $10 wide call spread (broken wing on top)

| Attribute | Value |
|-----------|-------|
| Direction | Directional bias on one side |
| Debit/Credit | Credit (typically larger than standard IC) |
| Max Profit | Net Credit |
| Max Loss | Asymmetric — larger on the broken wing side |
| When to Use | When you have a directional bias but want to collect premium with defined risk |

The side with the wider spread carries more risk but can generate more credit.

---

## Calendar / Diagonal Spreads

### Calendar Spread

**What it is:** Sell a near-term option and buy a longer-dated option at the **same strike** (calls or puts).

| Attribute | Value |
|-----------|-------|
| Direction | Neutral (strike-specific) |
| Debit/Credit | Debit (you pay — longer-dated costs more than near-term brings in) |
| Max Profit | Occurs when stock is near the strike at near-term expiration |
| Max Loss | Net Debit paid |
| Breakeven | Complex — depends on IV term structure |
| When to Use | Expect low volatility in the near term; time decay accelerates on near-term option |
| Greek Profile | Short theta (near-term decays faster than long-term), short vega on net |

**Mechanics:**
- Near-term option decays rapidly (high theta burn)
- Long-term option decays slowly
- The difference in decay rates = your profit
- Risk: Stock moves significantly away from strike before near-term expires

**Example:**
- Stock at $100
- Sell 30-day $100 call for $3.00
- Buy 60-day $100 call for $5.00
- Net Debit: $2.00
- Profit if stock stays near $100 at 30-day expiry (you keep the $3 from the short call)

---

### Diagonal Spread

**What it is:** Buy a longer-dated option at one strike and sell a near-term option at a **different strike**. Combines time decay benefit with directional bias.

**Classic Diagonal (Poor Man's Covered Call):**
- Buy longer-dated ATM or slightly ITM call
- Sell near-term OTM call (same underlying)
- Benefits from directional move while collecting premium

| Attribute | Value |
|-----------|-------|
| Direction | Directional bias (bullish or bearish) |
| Debit/Credit | Debit (but cheaper than a naked long call) |
| Max Profit | Complex — near-term strike + decay benefit |
| Max Loss | Net Debit paid |
| Breakeven | At or near the long call strike minus net debit |
| When to Use | When you want directional exposure but also want to offset cost with premium collection |

**Key difference from Calendar:**
- Calendar: Same strike, different expirations
- Diagonal: Different strike AND different expirations

**Greek Profile:**
- Long delta (directional bias based on strike selection)
- Short theta (near-term decay works for you)
- Short vega (you are net short near-term IV, net long far-term IV)

### Double Diagonal

**What it is:** Sell a near-term strangle (OTM call + OTM put) and buy a longer-dated strangle at **wider strikes**.

| Attribute | Value |
|-----------|-------|
| Direction | Neutral with wide range expectation |
| Debit/Credit | Debit |
| Max Profit | Wide range — benefits from IV differential between near and far terms |
| Max Loss | Net Debit paid |
| When to Use | Similar to iron condor but with longer-dated protection, better for longer-term views |

---

## Other Strategies

### Long Straddle

**What it is:** Buy 1 ATM call AND buy 1 ATM put at the same strike, same expiration.

| Attribute | Value |
|-----------|-------|
| Direction | Volatility (direction agnostic) |
| Debit/Credit | Debit |
| Max Profit | Unlimited (on either side) |
| Max Loss | Net Debit paid (both options expire worthless) |
| Breakeven (upside) | Strike + Net Debit |
| Breakeven (downside) | Strike − Net Debit |
| When to Use | Before binary events (earnings, FDA decisions, major announcements) where you expect a big move but aren't sure which direction |
| Greek Profile | Long delta (net zero at entry), long gamma, long vega, negative theta |

**Risk:** IV crush after the event can cause loss even if the stock moves (if IV collapses).

---

### Long Strangle

**What it is:** Buy 1 OTM call AND buy 1 OTM put at different strikes, same expiration. Cheaper than a straddle but requires a larger move to profit.

| Attribute | Value |
|-----------|-------|
| Direction | Volatility (direction agnostic) |
| Debit/Credit | Debit |
| Max Profit | Unlimited (on either side) |
| Max Loss | Net Debit paid |
| Breakeven (upside) | Call Strike + Net Debit |
| Breakeven (downside) | Put Strike − Net Debit |
| When to Use | Same as straddle but when you want lower cost (and expect a larger move) |
| Greek Profile | Long gamma, long vega, negative theta; cheaper than straddle, but wider breakevens |

---

### Ratio Spread

**What it is:** Buy X options at one strike and sell more options (2X, 3X) at a different strike. Unequal long/short leg count.

**Example: 1:2 Call Ratio Spread**
- Buy 1 ATM call
- Sell 2 OTM calls at a higher strike
- Net credit (or small debit)

| Attribute | Value |
|-----------|-------|
| Direction | Slightly bullish (call ratio) or bearish (put ratio) |
| Debit/Credit | Often a credit, but can be a small debit |
| Max Profit | Width of spread − Net Cost (if stock stays below short strike) |
| Max Loss | Potentially unlimited on the naked side if stock rises past short strikes |
| When to Use | When you want to collect premium with a moderately directional view |
| Greek Profile | Short delta on naked side, short vega, short theta; naked wings create unbounded risk |

⚠️ **Warning:** Ratio spreads with naked short legs have unbounded risk on the naked side. Use with caution.

---

### Jelly Roll

**What it is:** Combine a long call calendar spread with a long put calendar spread at the **same strike**. Both calendars are at-the-money.

| Attribute | Value |
|-----------|-------|
| Direction | Arbitrage / mispricing play |
| Debit/Credit | Usually a small credit (exploits minor mispricing) |
| Max Profit | Small — it's an arbitrage play |
| Max Loss | Defined |
| When to Use | When near-term put-call parity is violated (rare in liquid markets) |
| Greek Profile | Short gamma, short theta (near-term premium decays) |

**Structure:**
- Long call calendar (buy far-dated call, sell near-term call)
- Long put calendar (buy far-dated put, sell near-term put)
- Both at same strike, netting to a small credit

---

## Strategy Comparison Matrix

| Strategy | Debit/Credit | Max Profit | Max Loss | Best Market Condition |
|----------|-------------|------------|----------|----------------------|
| Bull Call Spread | Debit | Defined | Defined | Moderately bullish |
| Bear Put Spread | Debit | Defined | Defined | Moderately bearish |
| Bull Put Spread | Credit | Defined | Defined | Neutral/slightly bullish |
| Bear Call Spread | Credit | Defined | Defined | Neutral/slightly bearish |
| Long Call Butterfly | Debit | Defined | Defined | Neutral, stay at middle strike |
| Short Call Butterfly | Credit | Defined | Defined | Neutral, stay at wings |
| Put Broken Wing | Debit/Credit | Asymmetric | Asymmetric | Directional bias |
| Iron Condor | Credit | Defined | Defined | Range-bound |
| Broken Wing Iron Condor | Credit | Asymmetric | Asymmetric | Directional bias |
| Calendar Spread | Debit | Strike-dependent | Defined | Low vol, near-term decay |
| Diagonal Spread | Debit | Directional | Defined | Directional with premium collection |
| Double Diagonal | Debit | Wide range | Defined | Wide range, IV differential |
| Long Straddle | Debit | Unlimited | Defined | Big move expected (binary event) |
| Long Strangle | Debit | Unlimited | Defined | Big move expected, lower cost |
| Ratio Spread | Credit/Debit | Defined | Unbounded | Moderately directional |
| Jelly Roll | Credit | Small | Defined | Arbitrage opportunity |

---

## Choosing the Right Strategy

### By Outlook

| Outlook | Strategies |
|---------|-----------|
| Strongly bullish | Buy call, bull call spread |
| Moderately bullish | Bull call spread, bull put spread (credit) |
| Neutral / range-bound | Iron condor, short straddle, calendar spread |
| Moderately bearish | Bear put spread, bear call spread (credit) |
| Strongly bearish | Buy put, bear put spread |
| Volatility spike (earnings/event) | Long straddle, long strangle |
| IV crush expected | Short straddle, iron condor, credit spreads |
| Time decay advantage | Sell premium (credit spreads, covered calls) |

### By Risk Tolerance

| Risk Level | Strategies |
|-----------|-----------|
| Defined risk (max loss known) | All spreads, butterflies, iron condors |
| Undefined risk (naked legs) | Naked calls/puts, ratio spreads with naked wings |
| Low cost / lottery tickets | Long straddles/strangles, far OTM options |
| Income generation | Credit spreads, covered calls, cash-secured puts |

---

## External Resources
- **OptionStrat strategies list:** `https://optionstrat.com/strategies`
- **TastyTrade strategy explanations:** `https://tastylive.com/concepts-strategies`
- **OptionsPlaybook:** `https://www.optionsplaybook.com/`
