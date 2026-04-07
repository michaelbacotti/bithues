# SKILL.md — kb-dependability-holding

## What it does
Expert skill for Dependability Holding LLC — trading activities, Schwab brokerage account, P/L tracking, distributions to Bacotti Inc., and tax filing (Form 1065).

## When to use
- Questions about Dependability, DP&L, trading account, Schwab
- P/L tracking or distribution calculations
- Tax considerations for the trading entity
- Wash-sale loss carryforward status

## When NOT to use
- For general business entity overview (use kb-entity-overview)
- For tax preparation details (use kb-tax-preparation)
- For trading strategy (use options-pro)

## Inputs
- Entity info: `dependability-holding-llc/entity-info.md`
- P/L tracker: `dependability_pl_tracker.csv` or `pl_tracker.py`
- Tax documents in reference folders

## Outputs
- Current account status and YTD performance
- Distribution calculations per operating agreement
- Tax asset status (wash-sale carryforward)
- Action items for record-keeping

## Cost / Risk notes
No external calls. Read-only reference to workspace files.
