#!/usr/bin/env python3
"""Convert a category page from old navy/gold style to Goodreads-style Lora + Source Sans 3."""

import re
import sys

def convert_category(html: str, category_name: str, page_title: str, meta_desc: str, book_count: int, sub: str) -> str:

    # ---- Remove old Google Fonts link ----
    html = re.sub(r'<link[^>]+googleapis\.com/css2\?[^>]*>\s*', '', html)

    # ---- Add Lora + Source Sans 3 right after <head> ----
    new_fonts = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Source+Sans+3:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
    )
    html = re.sub(r'(</head>)', new_fonts + r'\n\1', html, count=1)

    # ---- Stylesheet: ../css/main.css → css/main.css ----
    html = re.sub(r'<link rel=["\']stylesheet["\'] href=["\']\.\./(css/main\.css)["\']',
                  r'<link rel="stylesheet" href="\1"', html)

    # ---- Remove ALL inline <style> blocks ----
    html = re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)

    # ---- Remove Google tag (gtag) scripts ----
    html = re.sub(r'<!-- Google tag \(gtag\.js\) -->.*?<script>\s*window\.dataLayer.*?</script>',
                  '', html, flags=re.DOTALL)
    html = re.sub(r'<script async src="https://www\.googletagmanager\.com/gtag.*?</script>',
                  '', html, flags=re.DOTALL)

    # ---- Title ----
    html = re.sub(r'<title>.*?</title>', f'<title>{page_title}</title>', html)

    # ---- Meta description ----
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{meta_desc}">', html)

    # ---- Nav: replace old nav with Goodreads-style nav ----
    new_nav = '''<nav class="nav">
  <div class="nav-inner">
    <a href="index.html" class="nav-brand">Bithues</a>
    <div class="nav-links">
      <div class="nav-dropdown">
        <a href="catalog.html" class="nav-link nav-link--dropdown">Books</a>
        <div class="nav-dropdown-content">
          <a href="catalog.html" class="nav-dropdown-item">All Books</a>
          <a href="book-tracker.html" class="nav-dropdown-item">Book Tracker</a>
          <a href="category/self-help.html" class="nav-dropdown-item">Self-Help</a>
          <a href="category/science-fiction.html" class="nav-dropdown-item">Sci-Fi</a>
          <a href="category/fantasy.html" class="nav-dropdown-item">Fantasy</a>
          <a href="category/nonfiction.html" class="nav-dropdown-item">Nonfiction</a>
          <a href="category/thriller.html" class="nav-dropdown-item">Thriller</a>
          <a href="category/biography.html" class="nav-dropdown-item">Biography</a>
          <a href="category/business.html" class="nav-dropdown-item">Business</a>
        </div>
      </div>
      <div class="nav-dropdown">
        <a href="catalog.html" class="nav-link nav-link--dropdown">Reviews</a>
        <div class="nav-dropdown-content">
          <a href="catalog.html" class="nav-dropdown-item">All Reviews</a>
          <a href="category/self-help.html" class="nav-dropdown-item">By Genre</a>
          <a href="authors.html" class="nav-dropdown-item">By Author</a>
        </div>
      </div>
      <div class="nav-dropdown">
        <a href="articles.html" class="nav-link nav-link--dropdown">Articles</a>
        <div class="nav-dropdown-content">
          <a href="articles.html" class="nav-dropdown-item">Reading Guides</a>
          <a href="articles.html" class="nav-dropdown-item">Best Lists</a>
        </div>
      </div>
      <a href="authors.html" class="nav-link">Authors</a>
      <a href="about.html" class="nav-link">About</a>
    </div>
  </div>
</nav>'''

    html = re.sub(r'<nav>.*?</nav>', new_nav, html, flags=re.DOTALL)

    # ---- Hero → page-header ----
    old_hero = re.search(
        r'<section class="(hero|pillar-hero)"[^>]*>.*?</section>',
        html, re.DOTALL
    )
    if old_hero:
        hero_html = old_hero.group(0)
        h1_match = re.search(r'<h1>([^<]+)</h1>', hero_html)
        h1_text = h1_match.group(1) if h1_match else category_name.capitalize()
        sub_match = re.search(r'<p class="hero-sub">([^<]+)</p>', hero_html)
        sub_text = sub_match.group(1) if sub_match else meta_desc
        badge_match = re.search(r'<span class="hero-badge">([^<]+)</span>', hero_html)
        badge_text = badge_match.group(1) if badge_match else f"{book_count} books"

        new_header = f'''<div class="container">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="index.html">Home</a>
    <span class="breadcrumb-sep">›</span>
    <a href="catalog.html">Books</a>
    <span class="breadcrumb-sep">›</span>
    <span class="current">{h1_text}</span>
  </nav>
</div>

<div class="container">
  <div class="page-header">
    <p class="page-header__eyebrow">{badge_text}</p>
    <h1 class="page-header__title">{h1_text}</h1>
    <p class="page-header__desc">{sub_text}</p>
  </div>
</div>'''
        html = html.replace(hero_html, new_header)

    # ---- Remove old divider ----
    html = re.sub(
        r'<div style="height:1px;background:linear-gradient\(to right,transparent,rgba\(200,169,110\.\.3\),transparent\);max-width:1100px;margin:0 auto;"></div>',
        '', html
    )

    # ---- section tags that wrap cards → container div ----
    html = re.sub(r'<section class="section">', '<div class="container"><section class="books-section">', html)
    html = re.sub(r'</section>\s*</main>', '</section></div></main>', html)

    # ---- Fix review-tag → genre-chip ----
    html = re.sub(r'<span class="review-tag">', '<span class="genre-chip">', html)

    # ---- newsletter section: clean ----
    old_newsletter = re.search(
        r'<div class="newsletter-section"[^>]*>.*?</div>\s*</section>',
        html, re.DOTALL
    )
    if old_newsletter:
        new_newsletter = '''<div class="container">
  <div class="newsletter-section">
    <h3>📬 Get the weekly shortlist</h3>
    <p>One email, Friday mornings. The 2–3 best new books we reviewed that week, plus one curated reading list. No fluff.</p>
    <form class="newsletter-form" action="#" method="post">
      <input type="email" placeholder="your@email.com" required>
      <button type="submit" class="btn btn--primary">Subscribe</button>
    </form>
    <p class="form-note">Join 1,200+ readers. Unsubscribe anytime.</p>
  </div>
</div>'''
        html = html.replace(old_newsletter.group(0), new_newsletter)

    # ---- Remove inline AdSense <ins> elements ----
    html = re.sub(r'\s*<ins class="adsbygoogle".*?</script>', '', html, flags=re.DOTALL)

    # ---- Footer ----
    old_footer = re.search(r'<footer>.*?</footer>', html, re.DOTALL)
    if old_footer:
        new_footer = '''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <p class="footer-brand">Bithues</p>
        <p class="footer-tagline">Curated book reviews and reading recommendations for curious minds.</p>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Explore</p>
        <ul class="footer-links">
          <li><a href="catalog.html">All Reviews</a></li>
          <li><a href="articles.html">Reading Guides</a></li>
          <li><a href="category/adventure.html">Browse by Genre</a></li>
          <li><a href="authors.html">Authors</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Company</p>
        <ul class="footer-links">
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="press.html">Press</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Legal</p>
        <ul class="footer-links">
          <li><a href="privacy.html">Privacy Policy</li>
          <li><a href="affiliate-disclosure.html">Affiliate Disclosure</a></li>
          <li><a href="editorial-policy.html">Editorial Policy</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© <span id="year"></span> Bithues Reading Lab · All rights reserved</p>
    </div>
  </div>
</footer>
<script>document.getElementById("year").textContent = new Date().getFullYear();</script>'''
        html = html.replace(old_footer.group(0), new_footer)

    # ---- Back to top button ----
    if 'back-to-top' not in html:
        html = re.sub(
            r'</body>',
            '<button class="back-to-top" onclick="window.scrollTo({top:0,behavior:\'smooth\'})">↑</button>\n'
            '<script>\n'
            'window.onscroll=function(){document.querySelector(".back-to-top").classList.toggle("visible",window.scrollY>300);};\n'
            '</script>\n</body>',
            html
        )

    return html


if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2]
    category = sys.argv[3]
    title = sys.argv[4]
    meta_desc = sys.argv[5]
    book_count = sys.argv[6]
    sub = sys.argv[7] if len(sys.argv) > 7 else meta_desc

    with open(src) as f:
        html = f.read()

    result = convert_category(html, category, title, meta_desc, book_count, sub)

    with open(dst, 'w') as f:
        f.write(result)

    print(f"Converted: {src} → {dst}")