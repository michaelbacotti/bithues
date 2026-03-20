import os
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent
TRACKER_PATH = Path("/Users/mike/.openclaw/workspace/References/book-tracker.md")

INDEX_TEMPLATE_PATH = ROOT / "index.html"
CATALOG_TEMPLATE_PATH = ROOT / "catalog.html"

FEATURED_IDS = [13, 15, 27, 24]

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

def render_book_card(book):
    title = html.escape(book["title"] or "")
    subtitle = html.escape(book["subtitle"] or "")
    author = html.escape(book["author"] or "Curated title")
    link = book["link"].strip()

    button = f'<a class="button amazon" href="{html.escape(link)}" target="_blank" rel="noopener">View on Amazon</a>' if link else '<span class="button amazon" style="opacity:0.5;cursor:default;">Coming Soon</span>'

    subtitle_html = f'<p class="book-subtitle">{subtitle}</p>' if subtitle else ""

    return f'''<article class="book-card">
 <div class="book-header">
 <span class="book-author">{author}</span>
 <h3 class="book-title">{title}</h3>
 </div>
 {subtitle_html}
 <div class="book-footer">{button}</div>
</article>'''

def generate_site():
    books = parse_markdown_table(TRACKER_PATH)
    by_id = {b["id"]: b for b in books}

    featured_books = [by_id[i] for i in FEATURED_IDS if i in by_id]
    featured_cards = "\n ".join(render_book_card(b) for b in featured_books)
    all_cards = "\n ".join(render_book_card(b) for b in books)

    # Load templates
    index_tpl = INDEX_TEMPLATE_PATH.read_text(encoding="utf-8")
    catalog_tpl = CATALOG_TEMPLATE_PATH.read_text(encoding="utf-8")

    # Replace placeholders
    index_out = index_tpl.replace("{{FEATURED_CARDS}}", featured_cards)
    catalog_out = catalog_tpl.replace("{{ALL_BOOK_CARDS}}", all_cards).replace("{{BOOK_COUNT}}", str(len(books)))

    INDEX_TEMPLATE_PATH.write_text(index_out, encoding="utf-8")
    CATALOG_TEMPLATE_PATH.write_text(catalog_out, encoding="utf-8")
    print(f"Generated site with {len(books)} books")

if __name__ == "__main__":
    generate_site()