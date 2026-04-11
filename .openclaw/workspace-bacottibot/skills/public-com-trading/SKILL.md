---
name: public-com-trading
description: Query real-time stock and options quotes, account balances, and positions via the Public.com API. Use when Mike asks about his trading account balance, portfolio positions, a specific stock or options price, or needs to look up a ticker quote on Public.com. Trigger phrases: "public.com", "Public.com account", "stock quote", "options quote", "account balance", "trading positions", "AAPL quote", "option chain".
---

# Public.com Trading Skill

Query Mike Bacotti's Public.com brokerage account (5OS76342) for real-time quotes, options chains, Greeks, and account data.

## Quick Start


> **⚠️ NEVER invent account numbers, token values, or API responses.** If the API fails or returns an error, report the actual error rather than guessing what the balance or position "should" be.
```bash
# Stock quote
./scripts/get-quote.sh AAPL

# Options quote (underlying symbol + expiration date)
./scripts/get-quote.sh AAPL 2026-04-18

# Account info (balances + positions)
./scripts/get-account.sh
```

## Authentication

The API uses a two-step Bearer token auth:

1. **Auth endpoint**: `POST https://api.public.com/userapiauthservice/personal/access-tokens`
2. Exchange secret key → access token (valid up to 24h)
3. Use access token as `Authorization: Bearer <token>` header for all data calls

Credentials are stored in `~/.openclaw/credentials/public.txt` (format: `secret_key=<key>`).

## Available Scripts

| Script | What it does |
|--------|-------------|
| `scripts/get-quote.sh` | Real-time stock or options quote |
| `scripts/get-account.sh` | Account balances and open positions |

## Available References

| File | Contents |
|------|----------|
| `references/api-guide.md` | Full API endpoint reference with request/response shapes |

## Error Handling

- **Expired token (401)**: Script re-authenticates automatically and retries once
- **Network timeout**: Curl timeout of 15s; script exits with clear error
- **Invalid symbol**: API returns 400 or empty results; script reports "Symbol not found"
- **Missing argument**: Script shows usage help

## Account IDs

- **Brokerage**: `5OS76342` (MARGIN, LEVEL_2 options)
- **Savings**: `2OF49173` (HIGH_YIELD savings)
