#!/usr/bin/env python3
"""Generate author pages from review data"""
import re
import os

reviews_dir = "/Users/mike/.openclaw/workspace/Website/bithues-reading-lab/reviews"
authors_dir = "/Users/mike/.openclaw/workspace/Website/bithues-reading-lab/authors"

# Template for author page
template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="AUTHOR_NAME - Books reviewed on Bithues Reading Lab. AUTHOR_COUNT books reviewed.">
    <meta property="og:title" content="AUTHOR_NAME | Bithues Reading Lab">
    <meta property="og:description" content="Books by AUTHOR_NAME reviewed on Bithues Reading Lab">
    <meta property="og:type" content="profile">
    <meta property="og:url" content="https://bithues.com/authors/AUTHOR_SLUG.html">
    <title>AUTHOR_NAME | Bithues Reading Lab</title>
    <script>
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
    </script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg: #0a0a0f; --surface: #12121a; --border: #2a2a3a;
            --text: #e8e8f0; --text-dim: #7a7a90; --accent: #7c3aed;
        }
        [data-theme="light"] {
            --bg: #f5f5f5; --surface: #ffffff; --border: #e0e0e0;
            --text: #1a1a1a; --text-dim: #666666;
        }
        body { font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; }
        .container { max-width: 800px; margin: 0 auto; padding: 0 1.5rem; }
        header { padding: 2rem 0; border-bottom: 1px solid var(--border); }
        nav { display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; flex-wrap: wrap; gap: 1rem; }
        .logo { font-size: 1.5rem; font-weight: 700; color: var(--text); text-decoration: none; }
        .logo span { color: var(--accent); }
        nav a { color: var(--text-dim); text-decoration: none; margin-left: 1.5rem; }
        
        .author-header { padding: 3rem 0; text-align: center; }
        .author-header h1 { font-size: 2.5rem; margin-bottom: 1rem; }
        .author-header p { color: var(--text-dim); font-size: 1.1rem; }
        
        .books-section { padding: 2rem 0; }
        .books-section h2 { font-size: 1.5rem; margin-bottom: 2rem; }
        
        .book-card { padding: 1.5rem; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 1.5rem; }
        .book-card h3 { font-size: 1.25rem; margin-bottom: 0.5rem; }
        .book-card h3 a { color: var(--text); text-decoration: none; }
        .book-card h3 a:hover { color: var(--accent); }
        .book-card .tldr { color: var(--text-dim); margin-bottom: 1rem; }
        .book-card .meta { display: flex; gap: 1rem; font-size: 0.9rem; color: var(--text-dim); }
        
        footer { padding: 2rem 0; text-align: center; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.85rem; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <nav>
                <a href="../index.html" class="logo">Bithues<span> Reading Lab</span></a>
                <div>
                    <a href="../index.html">Home</a>
                    <a href="../catalog.html">Catalog</a>
                    <a href="../articles.html">Articles</a>
                    <a href="../stories.html">Stories</a>
                    <a href="../about.html">About</a>
                    <button class="theme-toggle" onclick="toggleTheme()" style="background:none;border:1px solid var(--border);border-radius:20px;padding:0.5rem 1rem;cursor:pointer;color:var(--text-dim)">🌙</button>
                </div>
            </nav>
        </header>

        <section class="author-header">
            <h1>AUTHOR_NAME</h1>
            <p>BOOK_COUNT books reviewed</p>
        </section>

        <section class="books-section">
            <h2>Books by AUTHOR_NAME</h2>
            
BOOKS_LIST
        </section>

        <footer>
            <p>© <span id="year"></span> Bithues Reading Lab</p>
        </footer>
    </div>

    <script>
        function toggleTheme() {
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            const next = current === 'light' ? 'dark' : 'light';
            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
        }
        document.getElementById('year').textContent = new Date().getFullYear();
    </script>
</body>
</html>'''

def slugify(text):
    """Convert text to URL-friendly slug"""
    import unicodedata
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.lower().strip('-')

def extract_author_book(file_path):
    """Extract author and book title from review"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'<title>([^–]+)–([^|]+)', content)
    if not title_match:
        return None, None
    
    book_title = title_match.group(1).strip()
    author = title_match.group(2).strip()
    
    # Extract TLDR
    tldr_match = re.search(r'<p class="tldr">([^<]+)', content)
    tldr = tldr_match.group(1).strip() if tldr_match else ""
    
    return author, {'title': book_title, 'tldr': tldr, 'url': os.path.basename(file_path)}

# Collect all authors and their books
authors = {}

print("Scanning reviews for author information...")

files = sorted([f for f in os.listdir(reviews_dir) if f.endswith('.html') and f != 'index.html'])

for file in files:
    file_path = os.path.join(reviews_dir, file)
    if os.path.isfile(file_path):
        author, book = extract_author_book(file_path)
        if author and book:
            if author not in authors:
                authors[author] = []
            authors[author].append(book)

print(f"Found {len(authors)} unique authors")

# Generate author pages
print("\nGenerating author pages...")

for author, books in sorted(authors.items()):
    author_slug = slugify(author)
    
    # Build books list HTML
    books_html = ""
    for book in books:
        books_html += f'''            <div class="book-card">
                <h3><a href="../reviews/{book['url']}">{book['title']}</a></h3>
                <p class="tldr">{book['tldr']}</p>
                <div class="meta">
                    <a href="../reviews/{book['url']}">Read Review →</a>
                </div>
            </div>
'''
    
    # Fill template
    page = template.replace('AUTHOR_NAME', author)
    page = page.replace('AUTHOR_SLUG', author_slug)
    page = page.replace('AUTHOR_COUNT', str(len(books)))
    page = page.replace('BOOK_COUNT', str(len(books)))
    page = page.replace('BOOKS_LIST', books_html)
    
    # Write file
    output_path = os.path.join(authors_dir, f"{author_slug}.html")
    with open(output_path, 'w') as f:
        f.write(page)
    
    print(f"  Created: {author_slug}.html ({len(books)} books)")

print("\nDone! Author pages created:")
print(f"  Directory: {authors_dir}")
print(f"  Total pages: {len(authors)}")
