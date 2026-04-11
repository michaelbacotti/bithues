#!/usr/bin/env python3
"""
Add Schema.org JSON-LD to all book pages on bithues.com (michaelbacotti/bithues)
"""

import subprocess
import json
import re
import base64

TOKEN = "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"
REPO = "michaelbacotti/bithues"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.raw+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Book tracker data: number -> (title, subtitle, author, formats, asin_or_shortcode)
# ASIN is extracted from amzn.to shortcode via the book's Amazon page
# Format: number (in tracker) -> {title, subtitle, author, asin, isbn, pages, rating, reviews}
TRACKER = {
    1:  {"title": "The Dawn of Civilization", "subtitle": "A Story of a Prehistoric Tribe's Struggle for Survival", "author": "T. Stone", "asin": "4sYlT3t", "isbn": None, "pages": None, "rating": None, "reviews": None},
    2:  {"title": "The Richmond Cipher", "subtitle": "", "author": "E. Maris", "asin": "4snAwxv", "isbn": None, "pages": None, "rating": None, "reviews": None},
    3:  {"title": "Red Horizon: Lunar Launch", "subtitle": "", "author": "M. A. Hale", "asin": "40NsrpN", "isbn": None, "pages": None, "rating": None, "reviews": None},
    4:  {"title": "The Confluence Doctrine", "subtitle": "", "author": "Alaric Wynn", "asin": "3Pm0iUi", "isbn": None, "pages": None, "rating": None, "reviews": None},
    5:  {"title": "Living with a Moving Planet", "subtitle": "Deep Time, Human Adaptation, and a Positive Climate Future", "author": "J. T. Hartley", "asin": "4lHbruZ", "isbn": None, "pages": None, "rating": None, "reviews": None},
    6:  {"title": "Beyond the Veil", "subtitle": "Quantum Speculations on Consciousness, Death, and the Universe", "author": "D. E. Harlan", "asin": "480RlWP", "isbn": None, "pages": None, "rating": None, "reviews": None},
    7:  {"title": "Veiled Presence", "subtitle": "Questions on Earth's Silent Neighbors", "author": "E. C. Stroud", "asin": "4bAAv3z", "isbn": None, "pages": None, "rating": None, "reviews": None},
    8:  {"title": "The Power of Changing Your Mind", "subtitle": "How Intellectual Humility Improves Decisions, Relationships, and Everyday Life", "author": "Evan R. Cole", "asin": "3PieMVj", "isbn": None, "pages": None, "rating": None, "reviews": None},
    9:  {"title": "The Shadow Within", "subtitle": "A Practical Guide to Safe, Realistic Shadow Work in Everyday Life", "author": "Elena Maris", "asin": "4d19yHb", "isbn": None, "pages": None, "rating": None, "reviews": None},
    10: {"title": "Echoes of Aetheris", "subtitle": "", "author": "Aetheri Codex", "asin": "4rN0KIS", "isbn": None, "pages": None, "rating": None, "reviews": None},
    11: {"title": "Disclosure 2026", "subtitle": "18 Rated Scenarios for Alien First Contact", "author": "Marcus Reeve", "asin": "47hGhV8", "isbn": None, "pages": None, "rating": None, "reviews": None},
    12: {"title": "Resonance Drift", "subtitle": "A Hopepunk Signal", "author": "R. Zyrion", "asin": "3Pe2EEO", "isbn": None, "pages": None, "rating": None, "reviews": None},
    13: {"title": "Symbiont Bloom", "subtitle": "Verdant Nexus #1", "author": "Elowen Tidebloom", "asin": "47W0PTa", "isbn": None, "pages": None, "rating": None, "reviews": None},
    14: {"title": "Otomí", "subtitle": "A Historical Narrative of Land, Ritual, and Continuity", "author": "E. J. Marín", "asin": "41jPyIE", "isbn": None, "pages": None, "rating": None, "reviews": None},
    15: {"title": "Physics of Insight", "subtitle": "Awakening the Savant Within", "author": "Quantum Chronos", "asin": "B0GRW79ZM7", "isbn": None, "pages": None, "rating": None, "reviews": None},
    16: {"title": "The Physics of Time", "subtitle": "A Creative Exploration of Consciousness, Spacetime, and the Nature of Temporal Experience", "author": "Quantum Chronos", "asin": "3NCAWRA", "isbn": None, "pages": None, "rating": None, "reviews": None},
    17: {"title": "Consciousness in Higher Dimensional Spacetime", "subtitle": "A Dual-Dimensional Theory of Mind and Body", "author": "Quantum Chronos", "asin": "4siK2lz", "isbn": None, "pages": None, "rating": None, "reviews": None},
    18: {"title": "Quantum Soul Echoes", "subtitle": "Consciousness as Particle and Spacetime Imprint", "author": "Quantum Chronos", "asin": "3Pl8NPu", "isbn": None, "pages": None, "rating": None, "reviews": None},
    19: {"title": "Microbiology ABC's", "subtitle": "Tiny Cells and Microbes from A to Z", "author": "Michael Bacotti", "asin": "4cZlh9l", "isbn": None, "pages": None, "rating": None, "reviews": None},
    20: {"title": "You Tell the Story", "subtitle": "Everyday Adventures", "author": "Ellie Sunwood", "asin": "4smIZAW", "isbn": None, "pages": None, "rating": None, "reviews": None},
    21: {"title": "The Burning Song", "subtitle": "", "author": "Rowan Ashcroft", "asin": "4uDlo0F", "isbn": None, "pages": None, "rating": None, "reviews": None},
    22: {"title": "Mindful Memory", "subtitle": "Thought Experiments and Memory Mapping to Strengthen Your Brain", "author": "D. E. Harlan", "asin": "4smJrz8", "isbn": None, "pages": None, "rating": None, "reviews": None},
    23: {"title": "Shadow Work Journal for Women", "subtitle": "90-Day Guided Prompts to Heal Your Inner Child and Embrace Emotional Freedom", "author": "Luna Sage", "asin": "3NCBFlM", "isbn": None, "pages": None, "rating": None, "reviews": None},
    24: {"title": "Rules of Survival", "subtitle": "Fire, Hunger, and the First Name", "author": "Jorak Veldt", "asin": "3NvIPZ6", "isbn": None, "pages": None, "rating": None, "reviews": None},
    25: {"title": "Blood Ember", "subtitle": "Chants of the First", "author": "Jorak Veldt", "asin": "4bLjVwK", "isbn": None, "pages": None, "rating": None, "reviews": None},
    26: {"title": "The Orchardist: Harvest", "subtitle": "", "author": "Kate E Brennan", "asin": "4rOcr1Z", "isbn": None, "pages": None, "rating": None, "reviews": None},
    27: {"title": "Little Mike: Fun at the Beach", "subtitle": "", "author": "Michael Jr", "asin": "40JEYKU", "isbn": None, "pages": None, "rating": None, "reviews": None},
    28: {"title": "The Quiet Hours", "subtitle": "", "author": "Elara Moss", "asin": "3NOtEKA", "isbn": None, "pages": None, "rating": None, "reviews": None},
    29: {"title": "Little Mike: Learns to Fly", "subtitle": "", "author": "Michael Jr", "asin": "4dzhtvy", "isbn": None, "pages": None, "rating": None, "reviews": None},
    30: {"title": "Discovering Washington DC", "subtitle": "A Comprehensive Guide for All Ages", "author": "Evelyn Carter", "asin": "3Pl9LeA", "isbn": None, "pages": None, "rating": None, "reviews": None},
    31: {"title": "Echoes of Transcendence", "subtitle": "", "author": "L Everwood", "asin": "4rOlOyl", "isbn": None, "pages": None, "rating": None, "reviews": None},
    32: {"title": "American Journeys", "subtitle": "Exploring Language and American Culture", "author": "C. Everett", "asin": "4cUyAb0", "isbn": None, "pages": None, "rating": None, "reviews": None},
    33: {"title": "Mythical Menagerie", "subtitle": "A Journey Across Cultures and Creatures", "author": "E. Marlowe", "asin": "47W2rwc", "isbn": None, "pages": None, "rating": None, "reviews": None},
    34: {"title": "Little Mike: Builds a Robot", "subtitle": "", "author": "Michael Jr", "asin": "4svSTRa", "isbn": None, "pages": None, "rating": None, "reviews": None},
    35: {"title": "Time Investing", "subtitle": "A Self-Help Guide to Valuing Your Own Time", "author": "H Harvey", "asin": "4sSWsAl", "isbn": None, "pages": None, "rating": None, "reviews": None},
}

def gh_raw(path):
    """Fetch raw file content from GitHub."""
    result = subprocess.run(
        ["gh", "api", "-H", "Accept: application/vnd.github.raw+json",
         f"repos/{REPO}/contents/{path}"],
        capture_output=True, text=True,
        env={**__import__('os').environ, "GH_TOKEN": TOKEN}
    )
    if result.returncode != 0:
        raise Exception(f"Failed to fetch {path}: {result.stderr}")
    return result.stdout

def gh_get_sha(path):
    """Get SHA of a file for updates."""
    result = subprocess.run(
        ["gh", "api",
         f"repos/{REPO}/contents/{path}",
         "--jq", ".sha"],
        capture_output=True, text=True,
        env={**__import__('os').environ, "GH_TOKEN": TOKEN}
    )
    if result.returncode != 0:
        raise Exception(f"Failed to get SHA for {path}: {result.stderr}")
    return result.stdout.strip()

def gh_update_file(path, content, sha, message):
    """Update a file on GitHub via API."""
    encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')
    data = json.dumps({
        "message": message,
        "content": encoded,
        "sha": sha
    })
    result = subprocess.run(
        ["gh", "api", "-X", "PUT",
         f"repos/{REPO}/contents/{path}",
         "-f", f"input={data}"],
        capture_output=True, text=True,
        env={**__import__('os').environ, "GH_TOKEN": TOKEN}
    )
    if result.returncode != 0:
        raise Exception(f"Failed to update {path}: {result.stderr}")
    return result.stdout

def extract_from_html(html, book_num):
    """Extract title, author, category from HTML page."""
    # Title
    title_match = re.search(r'<title>([^<]+)</title>', html)
    title = title_match.group(1).strip() if title_match else TRACKER[book_num]["title"]
    
    # Category (eyebrow)
    cat_match = re.search(r'<div class="hero-eyebrow">([^<]+)</div>', html)
    category = cat_match.group(1).strip() if cat_match else "Fiction"
    
    # Subtitle
    sub_match = re.search(r'class="detail-subtitle">([^<]+)</p>', html)
    subtitle = sub_match.group(1).strip() if sub_match else ""
    
    # Author
    author_match = re.search(r'class="detail-author">([^<]+)</p>', html)
    if author_match:
        author_text = author_match.group(1).strip()
        # Remove "by " prefix
        if author_text.startswith("by "):
            author_text = author_text[3:]
        author = author_text
    else:
        author = TRACKER[book_num]["author"]
    
    return title, subtitle, author, category

def build_jsonld(book_num, title, subtitle, author, category):
    """Build the Schema.org JSON-LD block."""
    info = TRACKER[book_num]
    asin = info["asin"]
    
    # Amazon URL - use short code as-is (amzn.to/asin format)
    if asin:
        amazon_url = f"https://amzn.to/{asin}"
    else:
        amazon_url = None
    
    # Build sameAs (Goodreads placeholder - we'll omit if we don't have a Goodreads ID)
    same_as = None
    
    # ISBN
    isbn = info.get("isbn")
    
    # Pages
    pages = info.get("pages")
    
    # Rating
    rating = info.get("rating")
    reviews = info.get("reviews")
    
    # Determine book format - ebook by default for these pages
    book_format = "https://schema.org/EBook"
    book_edition = "eBook"
    
    obj = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": title,
        "author": {
            "@type": "Person",
            "name": author
        },
        "url": amazon_url,
        "bookEdition": book_edition,
        "bookFormat": book_format,
        "publisher": {
            "@type": "Organization",
            "name": "Threshold Publishing"
        }
    }
    
    if subtitle:
        obj["alternateName"] = subtitle
    
    if isbn:
        obj["isbn"] = isbn
    
    if pages:
        obj["numberOfPages"] = pages
    
    if rating and reviews:
        obj["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(rating),
            "reviewCount": str(reviews)
        }
    
    if same_as:
        obj["sameAs"] = same_as
    
    return json.dumps(obj, indent=2)

def process_book(book_num):
    """Process a single book page: fetch, modify, push back."""
    path = f"book/{book_num}.html"
    print(f"\n--- Processing book {book_num}: {path} ---")
    
    # Fetch raw content
    html = gh_raw(path)
    print(f"  Fetched {len(html)} chars")
    
    # Extract page info
    title, subtitle, author, category = extract_from_html(html, book_num)
    print(f"  Title: {title}")
    print(f"  Subtitle: {subtitle}")
    print(f"  Author: {author}")
    print(f"  Category: {category}")
    
    # Build JSON-LD
    jsonld = build_jsonld(book_num, title, subtitle, author, category)
    print(f"  JSON-LD: {jsonld[:100]}...")
    
    # Check if already has JSON-LD
    if '<script type="application/ld+json"' in html:
        print(f"  ⚠️  Already has JSON-LD, replacing...")
    
    # Build the script tag
    script_tag = f'\n<script type="application/ld+json">\n{jsonld}\n</script>\n'
    
    # Find </head> and insert before it
    if '</head>' in html:
        new_html = html.replace('</head>', script_tag + '</head>')
        print(f"  Inserted JSON-LD before </head>")
    else:
        print(f"  ❌ ERROR: Could not find </head> in HTML!")
        return False, "No </head> found"
    
    # Check if title needs updating
    current_title_match = re.search(r'<title>([^<]+)</title>', html)
    if current_title_match:
        current_title = current_title_match.group(1).strip()
        desired_title = f"{title} by {author} | Bithues Reading Lab"
        if current_title != desired_title:
            new_html = re.sub(r'<title>[^<]+</title>', f'<title>{desired_title}</title>', new_html)
            print(f"  Updated title: '{current_title}' -> '{desired_title}'")
    
    # Get SHA for update
    sha = gh_get_sha(path)
    print(f"  SHA: {sha[:8]}...")
    
    # Push update
    message = f"Add Schema.org JSON-LD to book {book_num}: {title}"
    try:
        gh_update_file(path, new_html, sha, message)
        print(f"  ✅ Pushed successfully")
        return True, None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False, str(e)

def main():
    print("=" * 60)
    print("Adding Schema.org JSON-LD to bithues.com book pages")
    print("=" * 60)
    
    results = []
    for book_num in range(1, 36):
        success, error = process_book(book_num)
        results.append((book_num, success, error))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    success_count = sum(1 for _, s, _ in results if s)
    error_count = sum(1 for _, s, _ in results if not s)
    
    print(f"Total processed: {len(results)}")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")
    
    if error_count > 0:
        print("\nErrors:")
        for num, success, error in results:
            if not success:
                print(f"  Book {num}: {error}")
    
    return results

if __name__ == "__main__":
    main()
