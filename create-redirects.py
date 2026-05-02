#!/usr/bin/env python3
"""Create HTML redirect files for old legacy URLs."""
import os

REDIRECTS = [
    # Reviews: numeric.html → /reviews/N/
    ("reviews/1.html", "/reviews/1/"),
    ("reviews/2.html", "/reviews/2/"),
    ("reviews/3.html", "/reviews/3/"),
    ("reviews/4.html", "/reviews/4/"),
    ("reviews/5.html", "/reviews/5/"),
    ("reviews/6.html", "/reviews/6/"),
    ("reviews/7.html", "/reviews/7/"),
    ("reviews/8.html", "/reviews/8/"),
    ("reviews/9.html", "/reviews/9/"),
    ("reviews/10.html", "/reviews/10/"),
    ("reviews/11.html", "/reviews/11/"),
    ("reviews/12.html", "/reviews/12/"),
    ("reviews/13.html", "/reviews/13/"),
    ("reviews/14.html", "/reviews/14/"),
    ("reviews/15.html", "/reviews/15/"),
    ("reviews/16.html", "/reviews/16/"),
    ("reviews/17.html", "/reviews/17/"),
    ("reviews/18.html", "/reviews/18/"),
    ("reviews/19.html", "/reviews/19/"),
    ("reviews/20.html", "/reviews/20/"),
    ("reviews/21.html", "/reviews/21/"),
    ("reviews/22.html", "/reviews/22/"),
    ("reviews/23.html", "/reviews/23/"),
    ("reviews/24.html", "/reviews/24/"),
    ("reviews/25.html", "/reviews/25/"),
    ("reviews/26.html", "/reviews/26/"),
    ("reviews/27.html", "/reviews/27/"),
    ("reviews/28.html", "/reviews/28/"),
    ("reviews/29.html", "/reviews/29/"),
    ("reviews/30.html", "/reviews/30/"),
    ("reviews/31.html", "/reviews/31/"),
    ("reviews/32.html", "/reviews/32/"),
    ("reviews/33.html", "/reviews/33/"),
    ("reviews/34.html", "/reviews/34/"),
    ("reviews/35.html", "/reviews/35/"),
    ("reviews/36.html", "/reviews/36/"),
    ("reviews/37.html", "/reviews/37/"),
    # Stories: numeric.html → /stories/slug/
    ("stories/1.html", "/stories/the-last-signal/"),
    ("stories/2.html", "/stories/the-last-winter/"),
    ("stories/3.html", "/stories/what-the-silence-knew/"),
    ("stories/4.html", "/stories/the-listen/"),
    ("stories/5.html", "/stories/before-the-streetlights-came-on/"),
    ("stories/6.html", "/stories/the-last-garden/"),
    ("stories/7.html", "/stories/the-space-between/"),
    ("stories/8.html", "/stories/they-walk-among-us/"),
    ("stories/9.html", "/stories/the-humble-mind/"),
    ("stories/10.html", "/stories/the-other-side/"),
    ("stories/11.html", "/stories/the-forbidden-library/"),
    ("stories/12.html", "/stories/the-disclosure/"),
    ("stories/13.html", "/stories/the-borrowed-life/"),
    ("stories/14.html", "/stories/the-door-between-worlds/"),
    ("stories/15.html", "/stories/the-last-song/"),
    ("stories/16.html", "/stories/rules-of-the-game/"),
    ("stories/17.html", "/stories/blood-ties/"),
    ("stories/18.html", "/stories/the-forgotten-minute/"),
    ("stories/19.html", "/stories/the-question/"),
    ("stories/20.html", "/stories/the-sound-between-stars/"),
    ("stories/21.html", "/stories/the-shadow-garden/"),
    ("stories/22.html", "/stories/the-last-arena/"),
    ("stories/23.html", "/stories/the-ember-song/"),
    ("stories/24.html", "/stories/the-harvest/"),
    ("stories/25.html", "/stories/oliver-and-the-ocean/"),
    ("stories/26.html", "/stories/the-quiet-town/"),
    ("stories/27.html", "/stories/jaspers-flight/"),
    ("stories/28.html", "/stories/city-of-wonders/"),
    ("stories/29.html", "/stories/the-echoes-return/"),
    ("stories/30.html", "/stories/american-voices/"),
    ("stories/31.html", "/stories/the-cartographer-of-sea-serpents/"),
    ("stories/32.html", "/stories/you-did-this-yourself/"),
    ("stories/33.html", "/stories/the-time-auction/"),
    ("stories/34.html", "/stories/mabi/"),
    ("stories/35.html", "/stories/the-last-gift/"),
    ("stories/36.html", "/stories/ice-memory/"),
    # Genre category: category/FOLDER.html → /genres/FOLDER/
    ("category/adventure.html", "/genres/adventure/"),
    ("category/biography.html", "/genres/biography/"),
    ("category/business.html", "/genres/business/"),
    ("category/children.html", "/genres/children/"),
    ("category/cultural.html", "/genres/cultural/"),
    ("category/dystopian.html", "/genres/dystopian/"),
    ("category/fantasy.html", "/genres/fantasy/"),
    ("category/fiction.html", "/genres/fiction/"),
    ("category/historical-fiction.html", "/genres/historical-fiction/"),
    ("category/literary.html", "/genres/literary/"),
    ("category/mystery.html", "/genres/mystery/"),
    ("category/mythology.html", "/genres/mythology/"),
    ("category/nonfiction.html", "/genres/nonfiction/"),
    ("category/romance.html", "/genres/romance/"),
    ("category/science-fiction.html", "/genres/science-fiction/"),
    ("category/science.html", "/genres/science/"),
    ("category/self-help.html", "/genres/self-help/"),
    ("category/spiritual.html", "/genres/spiritual/"),
    ("category/thriller.html", "/genres/thriller/"),
    # Root genre files
    ("adventure.html", "/genres/adventure/"),
    ("biography.html", "/genres/biography/"),
    ("business.html", "/genres/business/"),
    ("children.html", "/genres/children/"),
    ("cultural.html", "/genres/cultural/"),
    ("dystopian.html", "/genres/dystopian/"),
    ("fantasy.html", "/genres/fantasy/"),
    ("fiction.html", "/genres/fiction/"),
    ("historical-fiction.html", "/genres/historical-fiction/"),
    ("literary.html", "/genres/literary/"),
    ("mystery.html", "/genres/mystery/"),
    ("mythology.html", "/genres/mythology/"),
    ("nonfiction.html", "/genres/nonfiction/"),
    ("romance.html", "/genres/romance/"),
    ("science-fiction.html", "/genres/science-fiction/"),
    ("science.html", "/genres/science/"),
    ("self-help.html", "/genres/self-help/"),
    ("spiritual.html", "/genres/spiritual/"),
    ("thriller.html", "/genres/thriller/"),
    # Best list flat files
    ("best-apocalyptic-fiction.html", "/best-list/best-apocalyptic-fiction/"),
    ("best-biography-books.html", "/best-list/best-biography-books/"),
    ("best-books-about-friendship.html", "/best-list/best-books-about-friendship/"),
    ("best-books-about-grief.html", "/best-list/best-books-about-grief/"),
    ("best-books-about-money.html", "/best-list/best-books-about-money/"),
    ("best-books-about-productivity.html", "/best-list/best-books-about-productivity/"),
    ("best-books-for-anxious-people.html", "/best-list/best-books-for-anxious-people/"),
    ("best-books-for-couples.html", "/best-list/best-books-for-couples/"),
    ("best-books-for-dad.html", "/best-list/best-books-for-dad/"),
    ("best-books-for-entrepreneurs.html", "/best-list/best-books-for-entrepreneurs/"),
    ("best-books-for-men.html", "/best-list/best-books-for-men/"),
    ("best-fantasy-books.html", "/best-list/best-fantasy-books/"),
    ("best-historical-fiction.html", "/best-list/best-historical-fiction/"),
    ("best-sci-fi-books.html", "/best-list/best-sci-fi-books/"),
    ("best-self-help-books.html", "/best-list/best-self-help-books/"),
    ("best-space-opera-books.html", "/best-list/best-space-opera-books/"),
    ("best-thriller-books.html", "/best-list/best-thriller-books/"),
    ("best-time-travel-books.html", "/best-list/best-time-travel-books/"),
    # Books-like flat files
    ("books-like-1984.html", "/books-like/books-like-1984/"),
    ("books-like-atomic-habits.html", "/books-like/books-like-atomic-habits/"),
    ("books-like-dark-matter.html", "/books-like/books-like-dark-matter/"),
    ("books-like-dune.html", "/books-like/books-like-dune/"),
    ("books-like-foundation.html", "/books-like/books-like-foundation/"),
    ("books-like-hyperion.html", "/books-like/books-like-hyperion/"),
    ("books-like-project-hail-mary.html", "/books-like/books-like-project-hail-mary/"),
    ("books-like-psychology-of-money.html", "/books-like/books-like-psychology-of-money/"),
    ("books-like-sci-fi-beginners.html", "/books-like/books-like-sci-fi-beginners/"),
    ("books-like-the-martian.html", "/books-like/books-like-the-martian/"),
    ("books-like-the-midnight-library.html", "/books-like/books-like-the-midnight-library/"),
    ("books-like-the-name-of-the-wind.html", "/books-like/books-like-the-name-of-the-wind/"),
    # Section index pages
    ("articles.html", "/articles/"),
    ("authors.html", "/authors/"),
    ("stories.html", "/stories/"),
    ("book-tracker.html", "/book-tracker/"),
    ("reading-lists.html", "/reading-lists/"),
    # Policy pages
    ("editorial-policy.html", "/privacy.html"),
    ("affiliate-disclosure.html", "/privacy.html"),
    ("reviewer-bio.html", "/about.html"),
    ("contact.html", "/about.html"),
    ("press.html", "/about.html"),
]

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Redirecting...</title>
  <link rel="canonical" href="{url}">
  <meta http-equiv="refresh" content="0; url={url}">
</head>
<body>
  <p>Redirecting to <a href="{url}">{url}</a></p>
</body>
</html>'''

count = 0
for src, dst in REDIRECTS:
    dir_path = os.path.dirname(src)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    path = src  # already has .html extension
    
    # Only create if not already a real Hugo page
    if os.path.exists(path):
        # Check if it has Hugo meta tag (real Hugo page)
        with open(path, 'r') as f:
            content = f.read(200)
        if 'meta name="generator" content="Hugo' in content:
            # It's a real Hugo page, skip creating redirect
            continue
    
    with open(path, 'w') as f:
        f.write(TEMPLATE.format(url=dst))
    count += 1

print(f"Created {count} redirect files")