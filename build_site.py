import os
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent
TRACKER_PATH = Path("/Users/mike/.openclaw/workspace/References/book-tracker.md")

INDEX_TEMPLATE = ROOT / "index.html"
CATALOG_TEMPLATE = ROOT / "catalog.html"

FEATURED_IDS = [13, 15, 27, 24]

DESCRIPTIONS = {
    1: "When a brutal winter kills his father, sixteen-year-old Koda watches Uluk take up the leader's staff. As bears, bandits, and a bronze-armed warlord close in, Koda and his friends fight to turn a wandering tribe into a walled village.",
    2: "In Richmond, 1863, Mary listens as generals speak freely, certain no one below the stairs can understand. Every word she carries becomes a weapon in this tense spy thriller inspired by the real Elizabeth Van Lew network.",
    3: "Commander Marcus Hale must launch the Eos Ark to deliver 250 young colonists to Mars. But UAP hover above the horizon—humanity is raising children under the scrutiny of an unknown intelligence.",
    4: "In a world where suffering has been designed out, Orren hears something that doesn't fit—a sense of 'full, but unfinished.' A luminous exploration of what life is for when everything is already okay.",
    5: "Drawing on deep-time climate records and archaeology, this book shows how humans have adapted to changing baselines for tens of thousands of years—and what we can learn for living with a changing planet.",
    6: "A careful tour of evidence around what happens when we die, drawing on NDE research, quantum physics, and philosophy. Neither dogmatic nor dismissive—this is for anyone willing to think deeply about mystery.",
    7: "A transformative journey of self-discovery as seekers venture into realms where echoes of destiny reverberate. Courage, illumination, and the boundless pursuit of truth.",
    8: "In a culture that rewards confidence, this book shows how intellectual humility is a competitive edge. Learn the 'update loop' to turn mistakes into better models.",
    9: "Instead of treating reactions as defects, learn to treat them as information—and respond differently. A trauma-informed, Jungian approach to shadow work that emphasizes grounding and safety.",
    10: "Nine thousand years before history, a wounded alien ship falls onto a frozen steppe. The first hybrid is born in this atmospheric story of ancient aliens done seriously.",
    11: "From viral smartphone footage to White House landings, this book analyzes 18 pathways to alien disclosure—each rated for plausibility based on decades of testimony.",
    12: "In Eden Prime's biolum spires, harmony hums—until a family detects a pulse that defies the weave. A cozy hopepunk novella where stewardship triumphs through kinship.",
    13: "On volcanic isles of Lumengrove, dawn arrives through living leaf-glass. When the island's pulse skips, a family must unravel a systems puzzle—no villains, only a paradise nudging caretakers to pay attention.",
    14: "Through the eyes of a young ritual apprentice, follow one drought-stricken year in an Otomí village, drawing on archaeology and cosmology to reconstruct ancient life.",
    15: "What if genius isn't rare—it's hidden inside every mind, waiting for the right switch? A disciplined exploration of the 'savant switch' and mind's untapped architecture.",
    16: "A groundbreaking exploration: what if the universe is a block of spacetime containing all moments, yet consciousness navigates through it, actualizing possibility into experience?",
    17: "What if consciousness doesn't exist in the same spacetime as the body? A radical extension of Einstein's relativity into the domain of mind.",
    18: "What if consciousness is what spacetime remembers? Two models synthesized in this rigorous exploration of what happens to awareness when biological machinery shuts down.",
    19: "From amoebas to zooplankton, each letter highlights a microbe or cell structure. Colorful illustrations explain what cells are and how our immune cells fight back.",
    20: "A draw-and-write storybook where children look at pictures, then write and draw their own stories. Perfect for ages 4-8, screen-free creativity.",
    21: "When a cave lion marks Aken, the leader makes a choice that breaks every rule: he sends scouts to the coastal strangers. A story about learning when to lean on others.",
    22: "Empowering retirees with science-backed exercises like memory palaces and timeline mapping. Thought experiments reframed for personal wisdom.",
    23: "A beginner-friendly 90-day journal with warm prompts for emotional healing. From awareness to inner child work to integration—emerging confident and free.",
    24: "Roughly one million years ago, a boy learns the band's rules—water order, ember law, watch—and pays for them in skin. Grounded in archaeological inference.",
    25: "Three parts trace how survival habits harden into protocol, law, and chant. From fire to spear to echo—how technology becomes culture.",
    26: "Diane Kessler falls from a ladder—in that moment, she doesn't come back. A story of near-death experience and a larger world.",
    27: "Join Little Mike and his friends as they build an awe-inspiring sand castle. Vibrant illustrations and a positive message of teamwork.",
    28: "Gentle bedtime stories celebrating simple joys—perfect for children seeking comfort and adults craving peace. Lantern-lit cabins and moonlit gardens.",
    29: "Little Mike dreams of flying. With friends John and May, he meets Pilot Thomas who teaches the wonders of airplanes. A high-flying adventure.",
    30: "Beyond the monuments—a guide to the real DC. Stroll Georgetown's cobblestones, tap your feet to jazz, taste a half-smoke at Ben's.",
    31: "Where boundaries of reality blur, seekers embark on a transformative journey. Guided by ancient prophecies, they unveil mysteries of existence.",
    32: "For those moving to or visiting the US—or anyone eager to enhance English through immersive content. Discover American customs from Native wisdom to immigration.",
    33: "A thrilling journey through cultures exploring mythical creatures. Discover how dragons and shape-shifters have shaped cultural identities.",
    34: "Little Mike, John, and May build robots—but they keep falling apart. Through teamwork, they create a robot that tells stories and dances.",
    35: "A self-help guide showing how to prioritize yourself and your time. Strategies for investing in yourself instead of spending precious time away.",
}

WHO_WOULD_ENJOY = {
    1: "Fans of gritty historical adventures, tribal survival stories, and early-civilization settings.",
    2: "Readers of Kristin Hannah, James McBride, and Anthony Doerr. Fans of Civil War fiction and espionage.",
    3: "Fans of realistic Mars/Moon fiction who want competent characters and hopeful space opera.",
    4: "Fans of Ursula K. Le Guin, Becky Chambers, and meditative explorations of consciousness.",
    5: "Anyone tired of doom and denial who wants a grounded, hopeful way to think about climate.",
    6: "Readers who've stared at the night sky wondering. Anyone asking big questions about death.",
    7: "Readers who enjoy transformative journeys exploring consciousness and reality.",
    8: "Leaders, investors, and anyone who wants better decisions and fewer pointless fights.",
    9: "People who know their patterns but struggle to change reactions. Jungian psychology fans.",
    10: "Readers who enjoy ancient aliens without camp, evolutionary what-ifs, and atmospheric fiction.",
    11: "UFO disclosure enthusiasts, preppers, and anyone asking 'what if?'",
    12: "Fans of Becky Chambers and Martha Wells—serene sci-fi where community matters.",
    13: "Readers who love eco-worldbuilding and stories where people do the right thing.",
    14: "Bernard Cornwell fans and lovers of indigenous historical fiction.",
    15: "Readers who loved The Physics of Time and want more on consciousness.",
    16: "Physicists, philosophers, and curious minds willing to think radically.",
    17: "Anyone fascinated by consciousness foundations and physics meets neuroscience.",
    18: "Readers of Penrose and Hameroff—those who demand rigor and wonder.",
    19: "Curious kids who ask about germs. Parents seeking screen-free STEM learning.",
    20: "Children 4-8 and parents looking for creative, screen-free activities.",
    21: "Readers who love character-driven stories and authentic historical fiction.",
    22: "Retirees seeking to sharpen cognition. Anyone building emotional resilience.",
    23: "Women 25-45 feeling stuck in anxiety or people-pleasing.",
    24: "Fans of deep-time settings and anthropologically grounded survival fiction.",
    25: "Readers who like deep-time settings and stories of how culture forms.",
    26: "Readers who enjoy literary fiction with spiritual themes.",
    27: "Children 3-8 and parents who enjoy wholesome illustrated books.",
    28: "Children needing comfort and adults who need peaceful escape.",
    29: "Children 3-8 fascinated by planes. Parents wanting positive values.",
    30: "Tourists, history hounds, and anyone planning a DC visit.",
    31: "Readers who enjoy transformative fiction and self-discovery.",
    32: "ESL learners, immigrants, and anyone curious about American culture.",
    33: "Mythology enthusiasts and readers who enjoy cultural explorations.",
    34: "Children 3-8 and families who enjoy teamwork stories.",
    35: "Anyone feeling time-slippage and wanting to prioritize what matters.",
}

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

def get_category(book_id):
    return CATEGORIES.get(book_id, "Books")

def render_book_card(book):
    book_id = book["id"]
    title = html.escape(book["title"] or "")
    subtitle = html.escape(book["subtitle"] or "")
    author = html.escape(book["author"] or "Bithues")
    category = get_category(book_id)
    description = html.escape(DESCRIPTIONS.get(book_id, ""))
    
    return f'''<a href="book/{book_id}.html" class="book-card">
 <div class="card-category">{category}</div>
 <h3 class="card-title">{title}</h3>
 <p class="card-subtitle">{subtitle}</p>
 <p class="card-author">by {author}</p>
 <p class="card-desc">{description}</p>
</a>'''

def render_detail_page(book):
    book_id = book["id"]
    title = html.escape(book["title"] or "")
    subtitle = html.escape(book["subtitle"] or "")
    author = html.escape(book["author"] or "Bithues")
    link = book["link"].strip()
    category = get_category(book_id)
    description = DESCRIPTIONS.get(book_id, "")
    who_enjoys = WHO_WOULD_ENJOY.get(book_id, "")
    
    if link:
        amazon_btn = f'<a class="btn-buy" href="{html.escape(link)}" target="_blank" rel="noopener">Buy on Amazon</a>'
    else:
        amazon_btn = '<span class="btn-buy disabled">Coming Soon</span>'
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <title>{title} - Bithues Reading Lab</title>
 <meta name="viewport" content="width=device-width, initial-scale=1">
 <meta name="description" content="{title} - {description[:150]}">
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
    <a href="../catalog.html" class="back-link">← Back to Catalog</a>
    <div class="detail-content">
     <span class="detail-category">{category}</span>
     <h1 class="detail-title">{title}</h1>
     <p class="detail-subtitle">{subtitle}</p>
     <p class="detail-author">by {author}</p>
     <div class="detail-description">
      <h2>About this book</h2>
      <p>{description}</p>
     </div>
     <div class="detail-who">
      <h2>Who would enjoy this</h2>
      <p>{who_enjoys}</p>
     </div>
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
    
    featured_books = [by_id[i] for i in FEATURED_IDS if i in by_id]
    featured_cards = "\n ".join(render_book_card(b) for b in featured_books)
    all_cards = "\n ".join(render_book_card(b) for b in books)
    
    index_tpl = INDEX_TEMPLATE.read_text(encoding="utf-8")
    catalog_tpl = CATALOG_TEMPLATE.read_text(encoding="utf-8")
    
    index_out = index_tpl.replace("{{FEATURED_CARDS}}", featured_cards)
    catalog_out = catalog_tpl.replace("{{ALL_BOOK_CARDS}}", all_cards).replace("{{BOOK_COUNT}}", str(len(books)))
    
    INDEX_TEMPLATE.write_text(index_out, encoding="utf-8")
    CATALOG_TEMPLATE.write_text(catalog_out, encoding="utf-8")
    
    books_dir = ROOT / "book"
    books_dir.mkdir(exist_ok=True)
    
    for book in books:
        detail_html = render_detail_page(book)
        (books_dir / f"{book['id']}.html").write_text(detail_html, encoding="utf-8")
    
    print(f"Generated: index.html, catalog.html, {len(books)} detail pages")

if __name__ == "__main__":
    generate_site()