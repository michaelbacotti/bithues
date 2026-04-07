# SKILL.md — dependability-pl

## What it does
Tracks Dependability Holding monthly Net P/L and calculates Bacotti Inc.'s monthly distributions (GP Fee + 20% Profit Share) per the operating agreement.

## When to use
- User says "P/L [Month] $[amount]" or "Dependability made $[amount] [Month]"
- User asks for "YTD", "year to date", or "show 2026"
- Monthly distribution calculations needed

## When NOT to use
- For tax filing (use kb-tax-preparation)
- For entity overview (use kb-entity-overview or business-manager)
- For trading decisions (use options-pro)

## Inputs
- Monthly P/L amounts via CLI (pl_tracker.py add, show, print)
- CSV file: `dependability_pl_tracker.csv`

## Outputs
- CSV updates with monthly entries
- Response tables showing GP Fee ($1,000/month), Profit Share (20% after carryforward), and Total to Bacotti Inc.

## Cost / Risk notes
No external calls. Read/write to workspace CSV file. Formula: GP_Fee + max(0, (Net_P/L - Carry_In) × 20%).
