#!/usr/bin/env node
/**
 * generate-pages.js — Build index, browse, and post pages from migrated content
 */
const fs = require('fs');
const path = require('path');

const BLOG = path.join(__dirname);
const CONTENT = path.join(BLOG, 'content');
const PAGES = BLOG; // index.html, browse.html live here

// ─── Load all posts ─────────────────────────────────────────────────────────

function loadPosts() {
  const files = fs.readdirSync(CONTENT).filter(f => f.endsWith('.html'));
  const posts = [];
  
  files.forEach(file => {
    const html = fs.readFileSync(path.join(CONTENT, file), 'utf8');
    
    const titleMatch = html.match(/<title>([^<]+) — Bithues<\/title>/);
    const typeMatch = html.match(/class="tag (tag--[^"]+)"/);
    const dateMatch = html.match(/class="post-date">([^<]+)<\/span>/);
    const excerptMatch = html.match(/class="post-lead">([^<]+)<\/p>/);
    const genreMatch = html.match(/class="card-genre">([^<]+)<\/span>/);
    const authorMatch = html.match(/class="post-byline">by ([^<]+)<\/p>/);
    const starsMatch = html.match(/class="stars">([^<]+)<\/span>/);
    
    const title = titleMatch ? titleMatch[1] : file.replace('.html', '');
    const typeClass = typeMatch ? typeMatch[1] : 'tag--article';
    const type = typeClass.replace('tag--', '');
    const date = dateMatch ? dateMatch[1] : '';
    const excerpt = excerptMatch ? excerptMatch[1] : '';
    const genre = genreMatch ? genreMatch[1] : '';
    const author = authorMatch ? authorMatch[1] : '';
    const stars = starsMatch ? starsMatch[1] : '';
    const slug = file;
    
    posts.push({ title, type, typeClass, date, excerpt, genre, author, stars, slug });
  });
  
  return posts;
}

// Sort by date (newest first)
function sortByDate(posts) {
  return posts.sort((a, b) => {
    if (!a.date && !b.date) return 0;
    if (!a.date) return 1;
    if (!b.date) return -1;
    const da = new Date(a.date), db = new Date(b.date);
    return db - da;
  });
}

// ─── Card HTML ────────────────────────────────────────────────────────────────

function feedCard(post) {
  const coverGradients = {
    'Adventure': '#1a3a5c',
    'Historical Fiction': '#2d5a4a',
    'Literary Fiction': '#5a2d4a',
    'Sci-Fi': '#2d3a5a',
    'Science Fiction': '#2d3a5a',
    'Thriller': '#5a2d2d',
    'Fantasy': '#3a2d5a',
    'Self-Help': '#4a5a2d',
    "Children's Books": '#5a4a2d',
  };
  const bg = coverGradients[post.genre] || '#3a3a3a';
  
  if (post.type === 'review') {
    return `      <!-- Review -->
      <article class="card card--review">
        <div class="card-cover" style="background: linear-gradient(135deg, ${bg} 0%, ${bg}88 100%);">
          <span class="card-cover-title">${post.title}</span>
        </div>
        <div class="card-body">
          <div class="card-meta-top">
            <span class="tag tag--review">Book Review</span>
            <span class="card-date">${post.date}</span>
          </div>
          <h2 class="card-title"><a href="content/${post.slug}">${post.title}</a></h2>
          <p class="card-excerpt">${post.excerpt}${post.stars ? ` <strong>${post.stars}</strong>` : ''}</p>
          <div class="card-footer">
            <span class="card-genre">${post.genre}</span>
            <span class="card-author">${post.author}</span>
          </div>
        </div>
      </article>
`;
  } else if (post.type === 'story') {
    return `      <!-- Story -->
      <article class="card card--story">
        <div class="card-meta-top">
          <span class="tag tag--story">Short Story</span>
          <span class="card-date">${post.date}</span>
        </div>
        <h2 class="card-title"><a href="content/${post.slug}">${post.title}</a></h2>
        <p class="card-excerpt">${post.excerpt}</p>
        <div class="card-footer">
          <span class="card-genre">${post.genre}</span>
          <span class="card-read-time">${post.readTime || '8 min read'}</span>
        </div>
      </article>
`;
  } else {
    return `      <!-- Article -->
      <article class="card card--article">
        <div class="card-meta-top">
          <span class="tag tag--article">Article</span>
          <span class="card-date">${post.date}</span>
        </div>
        <h2 class="card-title"><a href="content/${post.slug}">${post.title}</a></h2>
        <p class="card-excerpt">${post.excerpt}</p>
        <div class="card-footer">
          <span class="card-genre">${post.genre}</span>
          <span class="card-read-time">${post.readTime || '10 min read'}</span>
        </div>
      </article>
`;
  }
}

function gridCard(post) {
  const coverGradients = {
    'Adventure': '#1a3a5c',
    'Historical Fiction': '#2d5a4a',
    'Literary Fiction': '#5a2d4a',
    'Sci-Fi': '#2d3a5a',
    'Science Fiction': '#2d3a5a',
    'Thriller': '#5a2d2d',
    'Fantasy': '#3a2d5a',
    'Self-Help': '#4a5a2d',
    "Children's Books": '#5a4a2d',
  };
  const bg = coverGradients[post.genre] || '#3a3a3a';
  const genreSlug = post.genre.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  
  if (post.type === 'review') {
    return `      <article class="grid-card card--review" data-type="review" data-genre="${genreSlug}">
        <div class="card-cover" style="background: linear-gradient(135deg, ${bg} 0%, ${bg}88 100%);">
          <span class="card-cover-title">${post.title}</span>
        </div>
        <div class="card-body">
          <div class="card-meta-top">
            <span class="tag tag--review">Review</span>
            <span class="card-date">${post.date}</span>
          </div>
          <h3 class="card-title"><a href="content/${post.slug}">${post.title}</a></h3>
          <p class="card-author">by ${post.author}</p>
          <p class="card-excerpt">${post.excerpt}${post.stars ? ` ${post.stars}` : ''}</p>
          <div class="card-footer">
            <span class="card-genre">${post.genre}</span>
          </div>
        </div>
      </article>
`;
  } else if (post.type === 'story') {
    return `      <article class="grid-card card--story" data-type="story" data-genre="${genreSlug}">
        <div class="card-meta-top">
          <span class="tag tag--story">Story</span>
          <span class="card-date">${post.date}</span>
        </div>
        <h3 class="card-title"><a href="content/${post.slug}">${post.title}</a></h3>
        <p class="card-excerpt">${post.excerpt}</p>
        <div class="card-footer">
          <span class="card-genre">${post.genre}</span>
        </div>
      </article>
`;
  } else {
    return `      <article class="grid-card card--article" data-type="article" data-genre="${genreSlug}">
        <div class="card-meta-top">
          <span class="tag tag--article">Article</span>
          <span class="card-date">${post.date}</span>
        </div>
        <h3 class="card-title"><a href="content/${post.slug}">${post.title}</a></h3>
        <p class="card-excerpt">${post.excerpt}</p>
        <div class="card-footer">
          <span class="card-genre">${post.genre}</span>
        </div>
      </article>
`;
  }
}

// ─── Build index.html ───────────────────────────────────────────────────────

function buildIndex(posts) {
  const latest = posts.slice(0, 20);
  const cards = latest.map(feedCard).join('\n\n');
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bithues — A Book Blog</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>

  <nav class="nav">
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">Bithues</a>
      <div class="nav-links">
        <a href="index.html" class="nav-link active">Feed</a>
        <a href="browse.html" class="nav-link">Browse</a>
        <a href="about.html" class="nav-link">About</a>
      </div>
    </div>
  </nav>

  <header class="hero">
    <div class="hero-inner">
      <h1 class="hero-title">Bithues</h1>
      <p class="hero-tagline">A book blog about fiction, ideas, and the worlds between the pages. Reviews, reading lists, articles, and original short fiction.</p>
    </div>
  </header>

  <main class="main">
    <div class="feed">

${cards}

    </div>
  </main>

  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">Bithues</div>
      <nav class="footer-nav">
        <a href="index.html">Feed</a>
        <a href="browse.html">Browse</a>
        <a href="about.html">About</a>
      </nav>
      <p class="footer-copy">&copy; 2026 Bithues. All rights reserved.</p>
    </div>
  </footer>

</body>
</html>`;
}

// ─── Build browse.html ───────────────────────────────────────────────────────

function buildBrowse(posts) {
  const cards = posts.map(gridCard).join('\n\n');
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Browse — Bithues</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>

  <nav class="nav">
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">Bithues</a>
      <div class="nav-links">
        <a href="index.html" class="nav-link">Feed</a>
        <a href="browse.html" class="nav-link active">Browse</a>
        <a href="about.html" class="nav-link">About</a>
      </div>
    </div>
  </nav>

  <header class="browse-header">
    <div class="browse-header-inner">
      <h1 class="browse-title">Browse</h1>
      <p class="browse-subtitle">All content — sorted, filtered, waiting to be found.</p>
    </div>
  </header>

  <section class="filters">
    <div class="filters-inner">
      <div class="filter-group">
        <span class="filter-label">Type:</span>
        <button class="filter-btn active" data-filter="all">All</button>
        <button class="filter-btn" data-filter="review">Book Reviews</button>
        <button class="filter-btn" data-filter="article">Articles</button>
        <button class="filter-btn" data-filter="story">Short Stories</button>
      </div>
    </div>
  </section>

  <main class="main">
    <div class="grid">

${cards}

    </div>
  </main>

  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">Bithues</div>
      <nav class="footer-nav">
        <a href="index.html">Feed</a>
        <a href="browse.html">Browse</a>
        <a href="about.html">About</a>
      </nav>
      <p class="footer-copy">&copy; 2026 Bithues. All rights reserved.</p>
    </div>
  </footer>

  <script>
    const typeBtns = document.querySelectorAll('[data-filter]');
    typeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cards = document.querySelectorAll('.grid-card');
        cards.forEach(card => {
          const type = card.dataset.type;
          const genre = card.dataset.genre;
          if (filter === 'all' || type === filter || genre === filter) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  </script>

</body>
</html>`;
}

// ─── Main ───────────────────────────────────────────────────────────────────

const posts = sortByDate(loadPosts());
console.log(`Loaded ${posts.length} posts`);

fs.writeFileSync(path.join(PAGES, 'index.html'), buildIndex(posts));
console.log('Wrote index.html');

fs.writeFileSync(path.join(PAGES, 'browse.html'), buildBrowse(posts));
console.log('Wrote browse.html');

// Stats
const byType = { review: 0, story: 0, article: 0, author: 0 };
posts.forEach(p => {
  if (p.type === 'review') byType.review++;
  else if (p.type === 'story') byType.story++;
  else if (p.type === 'article') byType.article++;
  else byType.author++;
});
console.log(`Stats: ${byType.review} reviews, ${byType.story} stories, ${byType.article} articles, ${byType.author} authors`);
