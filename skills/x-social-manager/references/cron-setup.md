# X Daily Engagement Cron Setup

## Recommended Schedule

**Daily at 9:00 AM ET** — prime morning engagement window

## Cron Expression

```
0 9 * * * America/New_York
```

## Workflow Per Run

1. Browser search x.com for 2-3 relevant posts (rotate search queries)
2. Identify best-fit posts (asking questions, recommendations, discussions)
3. Draft replies (send to Mike for approval OR auto-post if pre-approved)
4. Post approved replies via browser
5. Like the target posts
6. Log results to memory/YYYY-MM-DD.md

## Search Query Rotation

Daily rotation to keep content fresh:

| Day | Primary Topic | Search Query |
|-----|--------------|--------------|
| Mon | Finance/markets | "stock market analysis" |
| Tue | Science/physics | "quantum mechanics" |
| Wed | Books/literature | "book recommendations" |
| Thu | Technology/AI | "artificial intelligence" |
| Fri | Science/space | "space exploration" |
| Sat | Personal finance | "investing tips" |
| Sun | Science/physics | "time dilation" |

## Pre-Approved Reply Templates

To enable auto-posting without per-approval:

### Template 1 (Book-related)
```
Little Mike books are a fun series for kids — beach adventures, learning to fly, building robots. Perfect for sparking curiosity! @LittleMikeReads has more 🐱✈️🏖️
```

### Template 2 (Science)
```
This is exactly why physics class should've been this interesting. Block universe theory is wild — every moment existing all at once like pages in a book.
```

### Template 3 (Finance)
```
The hedging dynamics here are fascinating. Oil companies locking in multi-year margin protection while traders fight over short-term price direction.
```

### Template 4 (General)
```
Great point — following for more like this.
```

## Manual Approval Mode

If Mike wants to review before posting, the cron should:
1. Find posts and draft replies
2. Send Mike a message with the drafts
3. Wait for approval before posting
4. Post and like after approval

## Tools Used

- Browser (openclaw profile) — all posting via x.com
- Memory files — log all posted replies
- xurl — only for auth verification, not posting (credits exhausted)

## Note on API

X API credits exhausted as of 2026-04-02. All engagement must go through browser at x.com using the openclaw browser profile.
