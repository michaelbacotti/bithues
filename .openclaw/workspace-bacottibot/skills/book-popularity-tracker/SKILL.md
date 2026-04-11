# book-popularity-tracker Skill

Track daily popularity metrics (ratings, reviews, rank) for all 64 books in `References/book-tracker.md`.

---

## 📋 Book Data Source

**⚠️ NEVER invent book ASINs, titles, or author names.** Always read `References/book-tracker.md` first. If a book's ASIN is not in that file, say "I don't have that book in my tracker" rather than guessing.

Read `References/book-tracker.md` for the full list of 64 books. For each book, extract:
- **Title**
- **Author / Pen Name**
- **Amazon ASIN** (from tracker — construct URL as `https://www.amazon.com/dp/{ASIN}`)
- **Google Books ID** (search by title+author if not known)

---

## 📅 Daily Tracking Process

### Step 1: Check Each Book's Popularity

For each of the 64 books, scrape/publicly fetch:
1. **Amazon Product Page** — `https://www.amazon.com/dp/{ASIN}`
   - Star rating (e.g., "4.2 out of 5 stars")
   - Number of ratings (e.g., "1,234 ratings")
   - Best Sellers Rank (BSR) if available
   - Recent reviews count
2. **Google Books** — `https://books.google.com/books?q={title}+{author}`
   - Star rating
   - Number of ratings

> Use `web_fetch` for lightweight scraping, or `browser` for JavaScript-rendered pages.

### Step 2: Log Data

Create file: `memory/book-popularity-YYYY-MM-DD.md`

```markdown
# Book Popularity Tracker — YYYY-MM-DD

## Summary
- Books checked: 63
- New reviews detected: N
- Rating changes >0.2 stars: N
- Significant rank changes: N

## Detailed Data

| # | Title | Author | Amazon Rating | Amazon # Ratings | Amazon BSR | Google Rating | Google # Ratings | Notes |
|---|-------|--------|---------------|-------------------|------------|---------------|-------------------|-------|
| 1 | ... | ... | 4.5 | 120 | 45,000 | 4.3 | 89 | |
...
```

### Step 3: Compare with Previous Day

Read `memory/book-popularity-YYYY-MM-DD.md` (yesterday's file if exists).

Compare for each book:
- **Star rating delta** — alert if |change| > 0.2
- **Review count delta** — alert if any new reviews
- **BSR delta** — alert if rank changed by >5,000 positions

### Step 4: Alert on Notable Changes

If any of the following detected, write alert to top of today's log AND notify Mike:

1. **New review appeared** — new review count > previous
2. **Rating changed by > 0.2 stars** — up or down
3. **Significant BSR change** — moved >5,000 positions in either direction
4. **New book detected** — a book not in previous tracker
5. **Book no longer available** — product page returns 404/unavailable

**Alert format:**
```markdown
## 🚨 Alert — YYYY-MM-DD

- **[BOOK TITLE]** by [AUTHOR]: Rating changed from X.X → Y.Y (delta: ±Z.Z)
- **[BOOK TITLE]** by [AUTHOR]: New reviews (+N = total N)
- **[BOOK TITLE]** by [AUTHOR]: BSR changed from #X → #Y (moved Z positions)
```

Send alert to Mike (main session) via final response or log to `memory/YYYY-MM-DD-alerts.md`.

---

## 📊 Weekly Summary

Every 7 days, generate a `memory/book-popularity-WEEKLY.md` comparing the week's data — trend lines for top movers (biggest rating changes, most reviews gained, biggest rank improvements).

---

## 🔧 Tools

- **`web_fetch`** — lightweight page scraping for ratings/rank
- **`browser`** — for Amazon pages that require JS rendering
- **`web_search`** — lookup Google Books IDs if not in tracker

---

## ⏰ Cron Setup

Daily cron job — run every morning (e.g., 8:00 AM ET):

```
sessionTarget: "isolated"
payload.kind: "agentTurn"
message: "Run the book-popularity-tracker skill. Check all 64 books in References/book-tracker.md. Log to memory/book-popularity-YYYY-MM-DD.md. Compare with yesterday. Alert on notable changes (new reviews, rating delta >0.2, BSR delta >5000). Report summary to main session."
```

---

## 📁 File Structure

```
memory/
  book-popularity-YYYY-MM-DD.md      # Daily snapshot
  book-popularity-YYYY-MM-DD-alerts.md  # Alert-only days
  book-popularity-WEEKLY.md          # Weekly summary
```

---

*Skill: book-popularity-tracker v1.0*
