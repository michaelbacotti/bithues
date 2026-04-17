#!/usr/bin/env python3
import os
import re
import glob

REVIEWS_DIR = "/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues/reviews"

# Files that already have good unique meta descriptions
GOOD_DESCRIPTIONS = {
    "21.html": "Twenty thousand years ago, survival meant knowing who to trust. A powerful historical fiction about a community that learned to stop surviving alone.",
    "first-contact-diary.html": "First contact stories tend to go one of two directions: military thriller or diplomatic drama. First Contact Diary does neither, and that restraint is what makes it compelling.",
    "home-for-anya.html": "A small-town romance that executes a familiar premise—woman returns to hometown, rediscovers herself, finds unexpected love—with enough care and specificity to rise above convention.",
    "horizonte-rojo.html": "A Spanish-language sci-fi novel told from the perspective of the Mexican engineering team building lunar colony infrastructure—the people who make everything else possible.",
    "men-of-three-seas.html": "An epic historical voyage across three eras—Stone Age, Bronze Age, and Iron Age—that traces how survival habits become protocol, and protocol becomes culture.",
    "otomi.html": "Through the eyes of a young ritual apprentice, follow one drought-stricken year in an Otomí village. Historical fiction rooted in deep cultural knowledge and narrative instinct.",
    "perfection-cycle.html": "A bold synthesis of biology, cosmology, and philosophy arguing the universe is not a finished machine but a rough draft—and that destruction is its most powerful editing tool.",
    "probability-of-light.html": "What if consciousness is what spacetime remembers? A rigorous exploration of how physics and subjective experience might finally point to the same answer.",
    "virus-childrens-story.html": "A children's story about the immune system's battle against a virus, told with enough scientific honesty to teach while it entertains.",
    "three-seas.html": "An epic historical voyage across the Stone Age, Bronze Age, and Iron Age. For fans of sweeping, researched historical fiction that traces civilization's long formation.",
}

def extract_title_and_author(title_tag):
    """Extract book title and author from existing title tag like 'The Dawn of Civilization – T. Stone | Bithues Reading Lab'"""
    match = re.match(r'^(.+?)\s*[-–]\s*(.+?)\s*[|]', title_tag)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None, None

def extract_h1_content(html):
    """Get first h1 text content"""
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    if match:
        return match.group(1).strip()
    return None

def extract_tldr_paragraph(html):
    """Extract first paragraph after h1 that looks like a review summary"""
    # Find content between h1 and affiliate link
    body_match = re.search(r'<article[^>]*>.*?<p[^>]*>(.+?)</p>', html, re.DOTALL)
    if body_match:
        text = body_match.group(1)
        # Clean HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:300]
    return None

def get_meta_description_fallback(h1_text, author):
    """Generate meta description based on book title and author"""
    return f"Read our review of {h1_text} by {author}. Find out if this book is worth your time on Bithues Reading Lab."

def make_schema(book_title, author, review_body):
    """Create BookReview schema JSON-LD"""
    # Truncate review body to ~200 chars
    body = review_body[:250] if review_body else f"Read our full review of {book_title} by {author} on Bithues Reading Lab."
    escaped_title = book_title.replace('"', '\\"')
    escaped_author = author.replace('"', '\\"')
    escaped_body = body.replace('"', '\\"')
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BookReview",
  "name": "{escaped_title}",
  "reviewBody": "{escaped_body}",
  "reviewRating": {{"@type": "Rating", "ratingValue": "4", "bestRating": "5"}},
  "author": {{"@type": "Person", "name": "{escaped_author}"}},
  "itemReviewed": {{"@type": "Book", "name": "{escaped_title}", "author": {{"@type": "Person", "name": "{escaped_author}"}}}},
  "publisher": {{"@type": "Organization", "name": "Bithues Reading Lab"}}
}}
</script>'''

def process_file(filepath):
    filename = os.path.basename(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file already has BookReview schema (skip if already done)
    if '"@type": "BookReview"' in content:
        print(f"SKIP {filename}: BookReview schema already present")
        return False
    
    # Extract h1 content
    h1_text = extract_h1_content(content)
    if not h1_text:
        print(f"SKIP {filename}: Could not find h1")
        return False
    
    # Clean h1 text (remove author suffix if present)
    h1_clean = re.sub(r'\s*[-–]\s*.+$', '', h1_text).strip()
    
    # Extract author from h1 if present
    author_match = re.search(r'[-–]\s*(.+?)$', h1_text)
    if author_match:
        author = author_match.group(1).strip()
    else:
        # Try to get from existing title tag
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if title_match:
            _, author = extract_title_and_author(title_match.group(1))
            if not author:
                author = "Unknown Author"
        else:
            author = "Unknown Author"
    
    # Get existing title tag
    title_match = re.search(r'<title>([^<]+)</title>', content)
    if title_match:
        existing_title = title_match.group(1)
        book_title_from_title, author_from_title = extract_title_and_author(existing_title)
        if book_title_from_title:
            h1_clean = book_title_from_title
        if author_from_title:
            author = author_from_title
    
    # Get review body for schema
    review_body = extract_tldr_paragraph(content)
    
    # Create new title (format: "[Book Title] Review | Bithues Reading Lab")
    new_title = f"{h1_clean} Review | Bithues Reading Lab"
    
    # Get meta description - use existing good ones or generate from tldr
    if filename in GOOD_DESCRIPTIONS:
        new_description = GOOD_DESCRIPTIONS[filename]
    else:
        # Try to extract from first paragraph of review
        # Find the first review paragraph (after h1 class=header)
        para_match = re.search(r'<p[^>]*>([A-Z][^<]{50,300}?)</p>', content)
        if para_match:
            desc = para_match.group(1)
            desc = re.sub(r'<[^>]+>', '', desc)
            desc = re.sub(r'\s+', ' ', desc).strip()
            # Truncate to ~160 chars
            if len(desc) > 160:
                desc = desc[:157] + '...'
            new_description = desc
        else:
            new_description = f"Read our review of {h1_clean} by {author}. Find out if this book is worth your time."
    
    # Create BookReview schema
    schema = make_schema(h1_clean, author, review_body)
    
    # Update title tag
    content = re.sub(r'<title>[^<]+</title>', f'<title>{new_title}</title>', content)
    
    # Update meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{new_description}">',
        content
    )
    
    # Add BookReview schema before </head>
    content = content.replace('</head>', schema + '\n</head>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"UPDATED {filename}: {new_title}")
    return True

def main():
    files = sorted(glob.glob(os.path.join(REVIEWS_DIR, "*.html")))
    
    # Skip index.html and 1_new.html
    skip_files = {"index.html", "1_new.html"}
    
    count = 0
    for filepath in files:
        filename = os.path.basename(filepath)
        if filename in skip_files:
            continue
        if process_file(filepath):
            count += 1
    
    print(f"\nDone. Updated {count} files.")

if __name__ == "__main__":
    main()