#!/usr/bin/env python3
"""
Restructure category pages from old subcategory/amazon-cta/review-mini structure
to the proper Goodreads-style book-card grid layout.

Old body sections (after page-header, before footer):
  <section class="subcategory">...</section>  (multiple)
  <section class="books-like-block">...</section>
  <section class="internal-links">...</section>
  <section class="faq">...</section>
  <section class="newsletter-section">...</section>

New body:
  <div class="container">
    <section class="cards-section">
      <div class="section-header">
        <h2 class="section-title">All [Category] Books</h2>
      </div>
      <div class="cards-grid">
        <article class="book-card">...</article>  (one per review-mini)
        ...
      </div>
    </section>
    <hr class="section-divider">
    <section class="cards-section">
      <h2 class="section-title">Frequently Asked Questions</h2>
      <div class="faq-list">...</div>
    </section>
    <hr class="section-divider">
    <section class="newsletter-section">...</section>
  </div>
"""

import re, sys

def build_book_card(title, author, excerpt, review_url, genre_label):
    """Build a book-card HTML element."""
    # Pick a gradient based on genre
    gradients = {
        'Epic Fantasy': '#2d4a3e 0%, #1a3028 100%',
        'Grimdark': '#3d1f2b 0%, #251018 100%',
        'YA Fantasy': '#4a3d1f 0%, #302410 100%',
        'default': '#1a3d5c 0%, #0d2438 100%',
    }
    gradient = gradients.get(genre_label, gradients['default'])
    excerpt_esc = excerpt.replace('"', '&quot;') if excerpt else ''
    return f'''<article class="book-card">
  <div class="book-card__cover" style="background: linear-gradient(145deg, {gradient});">
    <span class="book-card__genre">{genre_label}</span>
  </div>
  <div class="book-card__body">
    <h3 class="book-card__title"><a href="{review_url}">{title}</a></h3>
    <p class="book-card__author">{author}</p>
    <p class="book-card__excerpt">{excerpt_esc}</p>
  </div>
</article>'''


def parse_review_mini(div_html):
    """Extract title, author, excerpt, url from a review-mini div."""
    title_m = re.search(r'<h4>([^<]+)</h4>', div_html)
    author_m = re.search(r'<span class="review-author">by ([^<]+)</span>', div_html)
    excerpt_m = re.search(r'<p>([^<]+(?:<[^>]+>[^<]*</[^>]+>)*[^<]*)</p>', div_html)
    # Find first non-link p tag for excerpt
    p_tags = re.findall(r'<p>(.*?)</p>', div_html, re.DOTALL)
    excerpt = ''
    for p in p_tags:
        if '<a href=' not in p:
            excerpt = re.sub(r'<[^>]+>', '', p).strip()
            break
    link_m = re.search(r"<a href='([^']+)'", div_html)
    title = title_m.group(1).strip() if title_m else 'Unknown'
    author = author_m.group(1).strip() if author_m else ''
    excerpt = excerpt.strip()
    url = link_m.group(1).strip() if link_m else '#'
    return title, f'by {author}' if author else '', excerpt, url


def parse_subcategory(section_html):
    """Extract subcategory name, description, and all review-minis."""
    header_m = re.search(r'<h2>([^<]+)</h2>', section_html)
    name = header_m.group(1).strip() if header_m else ''
    desc_m = re.search(r'<p class="subcategory-desc">([^<]+(?:<[^>]+>[^<]*</[^>]+>|[^<])*)</p>', section_html, re.DOTALL)
    # Better: find the subcategory-desc p and get all text
    desc_elem = re.search(r'<p class="subcategory-desc">(.*?)</p>', section_html, re.DOTALL)
    description = ''
    if desc_elem:
        description = re.sub(r'<[^>]+>', '', desc_elem.group(1)).strip()

    reviews = []
    for mini in re.findall(r'<div class="review-mini">(.*?)</div>\s*</div>', section_html, re.DOTALL):
        r = parse_review_mini('<div class="review-mini">' + mini + '</div>')
        reviews.append(r)
    return name, description, reviews


def restructure_category(body_html):
    """
    Given the body HTML (everything between nav and footer), extract
    subcategory data and rebuild with proper book-card grid.
    """
    # Extract all subcategory sections
    subcat_pattern = r'<section class="subcategory">(.*?)</section>\s*</section>'
    subcat_matches = list(re.finditer(subcat_pattern, body_html, re.DOTALL))

    if not subcat_matches:
        # Try alternate pattern
        subcat_pattern2 = r'<section class="subcategory">(.*?)</section>'
        subcat_matches = list(re.finditer(subcat_pattern2, body_html, re.DOTALL))

    all_books = []
    subcat_names = []

    for m in subcat_matches:
        section_text = m.group(0)
        name, desc, reviews = parse_subcategory(section_text)
        if name:
            subcat_names.append(name)
        for title, author, excerpt, url in reviews:
            all_books.append((name, title, author, excerpt, url))

    # Extract FAQ items
    faq_items = []
    faq_section = re.search(r'<section class="faq">(.*?)</section>\s*</section>', body_html, re.DOTALL)
    if faq_section:
        for item in re.findall(r'<div class="faq-item">(.*?)</div>\s*</div>', faq_section.group(1), re.DOTALL):
            q_m = re.search(r'<h3>([^<]+)</h3>', item)
            a_m = re.search(r'<p>(.*?)</p>', item, re.DOTALL)
            if q_m and a_m:
                q = q_m.group(1).strip()
                a = re.sub(r'<[^>]+>', '', a_m.group(1)).strip()
                faq_items.append((q, a))

    # Extract newsletter section
    newsletter_html = ''
    nl_match = re.search(r'<section class="newsletter-section">(.*?)</section>\s*</section>', body_html, re.DOTALL)
    if nl_match:
        newsletter_html = f'<section class="newsletter-section">{nl_match.group(1)}</section>'

    # Extract books-like block
    bl_items = []
    bl_match = re.search(r'<section class="books-like-block">(.*?)</section>\s*</section>', body_html, re.DOTALL)
    if bl_match:
        bl_text = bl_match.group(1)
        for link in re.findall(r'<a href="([^"]+)">([^<]+)</a>', bl_text):
            bl_items.append(link)

    # Build new body
    genre_label = subcat_names[0] if subcat_names else 'Book'

    # Build cards grid
    cards_html = ''
    for subcat, title, author, excerpt, url in all_books:
        cards_html += build_book_card(title, author, excerpt, url, subcat or genre_label) + '\n'

    # Build FAQ HTML
    faq_html = ''
    if faq_items:
        faq_html = '''<section class="cards-section">
      <h2 class="section-title">Frequently Asked Questions</h2>
      <div class="faq-list">
'''
        for q, a in faq_items:
            faq_html += f'''        <div class="faq-item">
          <h3>{q}</h3>
          <p>{a}</p>
        </div>
'''
        faq_html += '      </div>\n    </section>\n'

    # Build books-like HTML
    bl_html = ''
    if bl_items:
        bl_links = '\n'.join(f'          <a href="{u}">{t}</a>' for u, t in bl_items)
        bl_html = f'''<section class="cards-section">
      <h2 class="section-title">Books Like… Fantasy Deep Dives</h2>
      <div class="books-like-chips">
{bl_links}
      </div>
    </section>
'''

    new_body = f'''<div class="container">
    <section class="cards-section">
      <div class="section-header">
        <h2 class="section-title">All {genre_label} Books</h2>
      </div>
      <div class="cards-grid">
{cards_html}
      </div>
    </section>
    <hr class="section-divider">
{bl_html}
    <hr class="section-divider">
    {faq_html}
    <hr class="section-divider">
    {newsletter_html}
  </div>'''

    return new_body


if __name__ == '__main__':
    src = sys.argv[1]
    with open(src) as f:
        html = f.read()

    # Find the body content (between </nav> and <footer>)
    body_match = re.search(r'(</nav>)\s*(.*?)\s*(<footer)', html, re.DOTALL)
    if not body_match:
        print(f"ERROR: Could not find body boundary in {src}")
        sys.exit(1)

    old_body = body_match.group(2)
    new_body = restructure_category(old_body)

    # Reconstruct the full page
    new_html = html.replace(old_body, '\n' + new_body + '\n')

    with open(src, 'w') as f:
        f.write(new_html)

    print(f"Restructured: {src}")
