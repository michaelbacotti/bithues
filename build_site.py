import os
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent
TRACKER_PATH = Path("/Users/mike/.openclaw/workspace/References/book-tracker.md")

# Pages to generate
INDEX_TEMPLATE = ROOT / "index.html"
CATALOG_TEMPLATE = ROOT / "catalog.html"
DETAIL_TEMPLATE = ROOT / "book-detail.html"

FEATURED_IDS = [13, 15, 27, 24]

# Book descriptions (can expand later)
DESCRIPTIONS = {
    1: "A prehistoric tale of survival, leadership, and building the first settlement.",
    2: "A Civil War spy thriller set in Confederate Richmond.",
    3: "A space colony saga about humanity's future on Mars.",
    4: "A philosophical sci-fi about harmony and what it means to be truly alive.",
    5: "A deep-time look at climate change and human adaptation.",
    6: "Quantum speculations on consciousness, death, and what lies beyond.",
    7: "Exploring the boundaries of reality and self-discovery.",
    8: "How intellectual humility can improve your decisions and relationships.",
    9: "A practical guide to safe, realistic shadow work.",
    10: "Ancient aliens, evolutionary what-ifs, and cold clinical narration.",
    11: "18 rated scenarios for alien first contact.",
    12: "A cozy hopepunk novella about stewardship and defiant optimism.",
    13: "A solarpunk novel about family, community, and tending to a thriving world.",
    14: "Historical narrative of land, ritual, and continuity in ancient Mexico.",
    15: "Exploring the physics of insight and hidden cognition.",
    16: "A groundbreaking exploration of time and consciousness.",
    17: "A dual-dimensional theory of mind and body.",
    18: "Consciousness as particle and spacetime imprint.",
    19: "An A-Z guide to microbiology for kids.",
    20: "A draw-and-write storybook for children.",
    21: "A prehistoric fiction about trust, alliance, and survival.",
    22: "Thought experiments and memory mapping to strengthen your brain.",
    23: "90-day guided prompts for emotional healing.",
    24: "Rules of survival in prehistoric times.",
    25: "How a band's survival habits harden into protocol, law, and chant.",
    26: "A story of near-death experience and a larger world.",
    27: "Little Mike's fun adventure at the beach.",
    28: "Gentle bedtime stories for all ages.",
    29: "Little Mike learns to fly with Pilot Thomas.",
    30: "A comprehensive guide to Washington DC for all ages.",
    31: "A transformative journey of self-discovery.",
    32: "Exploring language and American culture.",
    33: "A journey across cultures and mythical creatures.",
    34: "Little Mike and friends build a robot together.",
    35: "A self-help guide to valuing your own time.",
}

# Categories (simple mapping)
CATEGORIES = {
    1: "Fiction", 2: "Fiction", 3: "Fiction", 4: "Fiction", 5: "Nonfiction",
    6: "Nonfiction", 7: "Fiction", 8: "Nonfiction", 9: "Nonfiction",
    10: "Fiction", 11: "Nonfiction", 12: "Fiction", 13: "Fiction",
    14: "Nonfiction", 15: "Nonfiction", 16: "Nonfiction", 17: "Nonfiction",
    18: "Nonfiction", 19: "Children", 20: "Children", 21: "Fiction",
    22: "Nonfiction", 23: "Nonfiction", 24: "Fiction", 25: "Fiction",
    26: "Fiction", 27: "Children", 28: "Children", 29: "Children",
    30: "Nonfiction", 31: "Fiction", 32: "Nonfiction", 33: "Nonfiction",
    34: "Children", 35: "Nonfiction",
}

def parse_markdown_table(path):
    with path.open("r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    table_lines = []
    in_table = False
    for line in lines:
        if line.strip().startswith("| #"):
            in_table = True
            table_lines.append(line)
            continue
        if in_table:
            if line.strip() == "" or not line.strip().startswith("|"):
                break
            table_lines.append(line)

    if len(table_lines) < 3:
        return []

    header = [col.strip() for col in table_lines[0].strip("|").split("|")]
    rows = []

    for row_line in table_lines[2:]:
        cols = [col.strip() for col in row_line.strip("|").split("|")]
        if len(cols) < len(header):
            cols += [""] * (len(header) - len(cols))
        data = dict(zip(header, cols))
        try:
            idx = int(data.get("#", "").strip())
        except ValueError:
            continue

        rows.append({
            "id": idx,
            "title": data.get("Title", ""),
            "subtitle": data.get("Subtitle", ""),
            "author": data.get("Author (Pen Name)", ""),
            "link": data.get("Affiliate Link", ""),
        })

    rows.sort(key=lambda x: x["id"])
    return rows

def get_description(book_id):
    return DESCRIPTIONS.get(book_id, "A curated title from Bithues Reading Lab.")

def get_category(book_id):
    return CATEGORIES.get(book_id, "Books")

def render_book_card(book, featured=False):
    book_id = book["id"]
    title = html.escape(book["title"] or "")
    subtitle = html.escape(book["subtitle"] or "")
    author = html.escape(book["author"] or "Bithues")
    link = book["link"].strip()
    category = get_category(book_id)
    description = get_description(book_id)
    
    # Amazon button
    if link:
        amazon_btn = f'<a class="btn-amazon" href="{html.escape(link)}" target="_blank" rel="noopener">Buy on Amazon →</a>'
    else:
        amazon_btn = '<span class="btn-amazon disabled">Coming Soon</span>'
    
    # Featured = bigger card
    card_class = "book-card featured-card" if featured else "book-card"
    
    return f'''<a href="book/{book_id}.html" class="{card_class}">
 <div class="card-category">{category}</div>
 <h3 class="card-title">{title}</h3>
 <p class="card-subtitle">{subtitle}</p>
 <p class="card-author">by {author}</p>
 <p class="card-desc">{description}</p>
 <div class="card-footer">{amazon_btn}</div>
</a>'''

def render_detail_page(book):
    book_id = book["id"]
    title = html.escape(book["title"] or "")
    subtitle = html.escape(book["subtitle"] or "")
    author = html.escape(book["author"] or "Bithues")
    link = book["link"].strip()
    category = get_category(book_id)
    description = get_description(book_id)
    
    if link:
        amazon_btn = f'<a class="btn-buy" href="{html.escape(link)}" target="_blank" rel="noopener">Buy on Amazon</a>'
    else:
        amazon_btn = '<span class="btn-buy disabled">Coming Soon</span>'
    
    # Back link
    back_link = f'<a href="../catalog.html" class="back-link">← Back to Catalog</a>'
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <title>{title} - Bithues Reading Lab</title>
 <meta name="viewport" content="width=device-width, initial-scale=1">
 <link rel="stylesheet" href="../styles.css">
</head>
<body>
 <header class="site-header">
  <div class="container header-inner">
   <a href="../index.html" class="brand">
    <span class="brand-mark">B</span>
    <span class="brand-text">Bithues Reading Lab</span>
   </a>
   <nav class="nav">
    <a href="../index.html">Home</a>
    <a href="../catalog.html" class="nav-active">Catalog</a>
   </nav>
  </div>
 </header>

 <main>
  <section class="detail-hero">
   <div class="container">
    {back_link}
    <div class="detail-content">
     <span class="detail-category">{category}</span>
     <h1 class="detail-title">{title}</h1>
     <p class="detail-subtitle">{subtitle}</p>
     <p class="detail-author">by {author}</p>
     <p class="detail-desc">{description}</p>
     <div class="detail-actions">{amazon_btn}</div>
    </div>
   </div>
  </section>
 </main>

 <footer class="site-footer">
  <div class="container footer-inner">
   <div class="footer-brand">Bithues Reading Lab</div>
   <div class="footer-links">
    <span>© <span id="year"></span> All rights reserved</span>
   </div>
  </div>
 </footer>

 <script>
  document.getElementById('year').textContent = new Date().getFullYear();
 </script>
</body>
</html>'''

def generate_site():
    books = parse_markdown_table(TRACKER_PATH)
    by_id = {b["id"]: b for b in books}
    
    # Featured books
    featured_books = [by_id[i] for i in FEATURED_IDS if i in by_id]
    featured_cards = "\n ".join(render_book_card(b, featured=True) for b in featured_books)
    
    # All cards
    all_cards = "\n ".join(render_book_card(b) for b in books)
    
    # Load templates
    index_tpl = INDEX_TEMPLATE.read_text(encoding="utf-8")
    catalog_tpl = CATALOG_TEMPLATE.read_text(encoding="utf-8")
    
    # Generate index and catalog
    index_out = index_tpl.replace("{{FEATURED_CARDS}}", featured_cards)
    catalog_out = catalog_tpl.replace("{{ALL_BOOK_CARDS}}", all_cards).replace("{{BOOK_COUNT}}", str(len(books)))
    
    INDEX_TEMPLATE.write_text(index_out, encoding="utf-8")
    CATALOG_TEMPLATE.write_text(catalog_out, encoding="utf-8")
    
    # Generate detail pages
    books_dir = ROOT / "book"
    books_dir.mkdir(exist_ok=True)
    
    for book in books:
        detail_html = render_detail_page(book)
        (books_dir / f"{book['id']}.html").write_text(detail_html, encoding="utf-8")
    
    print(f"Generated: index.html, catalog.html, {len(books)} detail pages")

if __name__ == "__main__":
    generate_site()