import os
from pathlib import Path
import html

# --- Config ----
ROOT = Path(__file__).resolve().parent
TRACKER_PATH = Path("/Users/mike/.openclaw/workspace/References/book-tracker.md")
PUBLIC_DIR = ROOT / "public"

INDEX_TEMPLATE_PATH = PUBLIC_DIR / "index.html"
CATALOG_TEMPLATE_PATH = PUBLIC_DIR / "catalog.html"

INDEX_OUTPUT_PATH = PUBLIC_DIR / "index.html"
CATALOG_OUTPUT_PATH = PUBLIC_DIR / "catalog.html"

# Pick featured books by row number in the table (1-based, matching your tracker)
FEATURED_IDS = [13, 15, 27, 24]


def parse_markdown_table(path: Path):
    """
    Very simple parser for your existing markdown table:
    | # | Title | Subtitle | Author (Pen Name) | Affiliate Link |
    """
    with path.open("r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    # Find table start (first line that looks like a header row)
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

    # Skip header and separator (first two lines)
    for row_line in table_lines[2:]:
        cols = [col.strip() for col in row_line.strip("|").split("|")]
        if len(cols) < len(header):
            # pad missing columns
            cols += [""] * (len(header) - len(cols))
        data = dict(zip(header, cols))
        # normalize keys we care about
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

    # sort by id just in case
    rows.sort(key=lambda x: x["id"])
    return rows


def escape(text: str) -> str:
    return html.escape(text or "")


def render_book_card(book, compact=False):
    title = escape(book["title"])
    subtitle = escape(book["subtitle"])
    author = escape(book["author"])
    link = book["link"].strip()

    if not link:
        button_html = (
            '<button class="button amazon" disabled>'
            "Link coming soon"
            "</button>"
        )
    else:
        button_html = (
            f'<a class="button amazon" href="{html.escape(link)}" '
            f'target="_blank" rel="noopener">'
            "View on Amazon"
            "</a>"
        )

    if author:
        meta = author
    else:
        meta = "Curated title"

    parts = [
        '<article class="book-card">',
        f' <div class="book-meta">{meta}</div>',
        f' <h3 class="book-title">{title}</h3>',
    ]
    if subtitle:
        parts.append(f' <p class="book-subtitle">{subtitle}</p>')
    parts.append(' <div class="book-actions">')
    parts.append(f' {button_html}')
    parts.append(' </div>')
    parts.append('</article>')
    return "\n".join(parts)


def generate_site():
    # Ensure public dir exists
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    books = parse_markdown_table(TRACKER_PATH)

    # Build lookup by id
    by_id = {b["id"]: b for b in books}

    # Featured books: keep those that exist, in order
    featured_books = [by_id[i] for i in FEATURED_IDS if i in by_id]
    featured_cards_html = "\n\n".join(
        render_book_card(b, compact=True) for b in featured_books
    )

    # All book cards
    all_cards_html = "\n\n".join(render_book_card(b) for b in books)

    # Load templates
    index_tpl = INDEX_TEMPLATE_PATH.read_text(encoding="utf-8")
    catalog_tpl = CATALOG_TEMPLATE_PATH.read_text(encoding="utf-8")

    # Simple placeholder replacement
    index_out = index_tpl.replace("{{FEATURED_CARDS}}", featured_cards_html)
    catalog_out = catalog_tpl.replace("{{ALL_BOOK_CARDS}}", all_cards_html)

    INDEX_OUTPUT_PATH.write_text(index_out, encoding="utf-8")
    CATALOG_OUTPUT_PATH.write_text(catalog_out, encoding="utf-8")


if __name__ == "__main__":
    generate_site()
    print("Site generated into ./public")
