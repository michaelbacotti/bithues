# Book Popularity Tracker — Cron Setup

## 📋 To Create the Daily Cron Job

Run this command to set up a daily cron at 8:00 AM ET:

```bash
openclaw cron add \
  --name "book-popularity-tracker" \
  --schedule "0 8 * * *" \
  --session-target "isolated" \
  --message "Run the book-popularity-tracker skill. Check all 63 books in References/book-tracker.md. Log to memory/book-popularity-YYYY-MM-DD.md. Compare with yesterday. Alert on notable changes (new reviews, rating delta >0.2, BSR delta >5000). Report summary to main session." \
  --model "minimax/MiniMax-M2.7"
```

## ⚙️ Cron Parameters

| Parameter | Value |
|-----------|-------|
| **Name** | `book-popularity-tracker` |
| **Schedule** | `0 8 * * *` (8:00 AM daily, America/New_York timezone) |
| **sessionTarget** | `isolated` |
| **payload.kind** | `agentTurn` |
| **payload.message** | `"Run the book-popularity-tracker skill. Check all 63 books in References/book-tracker.md. Log to memory/book-popularity-YYYY-MM-DD.md. Compare with yesterday. Alert on notable changes (new reviews, rating delta >0.2, BSR delta >5000). Report summary to main session."` |
| **Model** | `minimax/MiniMax-M2.7` |

## ✅ Verify Cron Created

```bash
openclaw cron list
```

## 🛑 Remove Cron (if needed)

```bash
openclaw cron remove --name "book-popularity-tracker"
```

---

*Created: 2026-04-04*
