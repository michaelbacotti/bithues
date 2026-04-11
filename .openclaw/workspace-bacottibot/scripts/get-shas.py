#!/usr/bin/env python3
import urllib.request, json

TOKEN = "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"
REPO = "michaelbacotti/bithues"

articles = [
    "best-books-spring-2026.html",
    "best-sci-fi-2026.html",
    "books-for-dad-gift-guide.html",
    "best-books-summer-2026.html",
    "fantasy-for-beginners.html",
    "horror-for-beginners.html",
    "romance-for-beginners.html",
    "thriller-mystery-guide.html",
    "kids-reading-guide.html",
    "how-to-read-more-books.html",
    "how-we-review-books.html",
    "little-mike-series.html",
    "memoir-biography-guide.html",
    "quantum-physics-beginners.html",
    "reading-challenge-2026.html",
    "speed-reading-basics.html",
    "shadow-work-guide.html",
    "why-read-outside-your-genre.html",
    "books-change-how-you-think.html",
    "books-like-physics-of-time.html",
    "books-like-project-hail-mary.html",
    "hopepunk-beginners-guide.html",
    "business-leadership-guide.html",
]

for article in articles:
    url = f"https://api.github.com/repos/{REPO}/contents/articles/{article}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req) as resp:
            d = json.loads(resp.read())
            print(f'    "{article}": "{d["sha"]}",')
    except Exception as e:
        print(f'    # {article}: ERROR {e}')
