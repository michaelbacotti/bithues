---
name: x-social-manager
description: Daily X (Twitter) engagement management for @SpaceCat_SC001. Use when: (1) Mike asks to post, reply, like, or engage on X, (2) setting up X engagement cron/daily tasks, (3) promoting Little Mike books, (4) finding posts to reply to, (5) quote-posting old content. Workflow: browser-based X engagement using the openclaw browser profile. No API calls needed — X API credits are exhausted.
---

# X Social Manager

Daily engagement workflow for @SpaceCat_SC001 using browser automation.

## ⚠️ Critical Rules

1. **Never say Mike is the author of Little Mike books** — his SON writes them
2. **No links in replies** — spammy, X algorithm penalizes links
3. **Soft sell only** — mention @LittleMikeReads, never Amazon/website links in replies
4. **Put links in bio/pinned post only** — not in individual replies
5. **Use browser profile: `openclaw`** — not the user profile

## Topics That Work (Mike's Interests)

| Topic | Engagement |
|-------|------------|
| Physics/quantum mechanics | ✅ Best (38-1555 views) |
| Finance/markets/investing | ✅ Good |
| Technology/AI | ✅ Good |
| Geopolitics | ✅ Okay |
| Space/science | ✅ Good |
| Book promo (standalone) | ❌ Almost no traction |

## Account Info

- **Profile:** https://x.com/SpaceCat_SC001
- **Browser:** openclaw profile
- **Little Mike account:** @LittleMikeReads (dormant, promote this)
- **Little Mike website:** https://littlemikebooks.com
- **Little Mike Amazon:** https://amzn.to/4sZxujl

## Engagement Workflow

1. **Find posts** → Browser search on x.com for relevant topics
2. **Pick 2-3 posts** → Best fit: asking questions, seeking recommendations, discussions
3. **Draft reply** → Natural, helpful, no links, mention @LittleMikeReads when on-topic
4. **Post reply** → Browser compose/reply
5. **Like the post** → After replying

## Reply Templates

### Book-adjacent posts
> "Little Mike books are a fun series for kids — beach adventures, learning to fly, building robots. Perfect for sparking curiosity! @LittleMikeReads has more 🐱✈️🏖️"

### Science/physics posts
> "This is exactly why physics class should've been this interesting. Block universe theory is wild — every moment existing all at once like pages in a book."

### Finance/markets posts
> "The hedging dynamics here are fascinating. Oil companies locking in multi-year margin protection while traders fight over short-term price direction."

### General engagement
> "Great point — following for more like this."
> "This is the kind of content worth bookmarking."

## Quote-Posting Old High-Performers

Mike's pinned post ("If you're fascinated by biology, quantum mechanics, and technology...") has 1,555 views and is evergreen. Quote it with fresh commentary to re-promote.

URL: https://x.com/SpaceCat_SC001/status/1873380012881224074

## Daily Search Queries

Rotate through these:
```
"children's books recommendations"
"#BookTwitter"
"quantum mechanics"
"block universe"
"time dilation GPS"
"stock market analysis"
"oil futures hedging"
"AI technology"
"#SciFi"
"new book recommendations"
```

## Cron Job Setup

For a daily engagement cron:
- Browser search for 2-3 relevant posts
- Draft replies (manual approval via message before posting)
- Post replies, then like

Use cron for exact timing (e.g., 9 AM daily). See references/cron-setup.md for cron configuration.

## References

- [Engagement Rules](references/engagement-rules.md) — detailed do's and don'ts
- [Cron Setup](references/cron-setup.md) — daily cron configuration
