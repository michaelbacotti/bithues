#!/usr/bin/env node
/**
 * migrate-all.js — Migrate all bithues-work content to blog-bithues format
 */
const fs = require('fs');
const path = require('path');

const WORK = path.join(__dirname, '..', 'bithues-work');
const BLOG = __dirname;
const POSTS = path.join(BLOG, 'posts');
const CONTENT = path.join(BLOG, 'content');

// Ensure directories exist
[POSTS, CONTENT].forEach(d => {
  if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
});

// ─── Helpers ────────────────────────────────────────────────────────────────

function slugify(str) {
  return str.toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

function getText(el, regex) {
  const m = el.match(regex);
  return m ? m[1].trim() : '';
}

function extractProse(html) {
  // Find the .review-prose, .story-prose, or .article-body div and extract <p> tags
  const proseMatch = html.match(/<(?:div|p)[^>]*class="[^"]*prose[^"]*"[^>]*>([\s\S]*?)<\/div>/i)
    || html.match(/<(?:div)[^>]*class="[^"]*(?:review-body|story-body|article-body)[^"]*"[^>]*>([\s\S]*?)<\/div>/i)
    || html.match(/<div[^>]*>(<p>[\s\S]*?)<\/div>/i);
  
  if (!proseMatch) {
    // Fallback: extract all <p> tags
    const paras = [];
    const re = /<p[^>]*>([\s\S]*?)<\/p>/gi;
    let m;
    while ((m = re.exec(html)) !== null && paras.length < 20) {
      paras.push(m[1]);
    }
    return paras.join('\n');
  }
  
  const prose = proseMatch[1];
  const paras = [];
  const re = /<p[^>]*>([\s\S]*?)<\/p>/gi;
  let m;
  while ((m = re.exec(prose)) !== null) {
    paras.push(m[1]);
  }
  return paras.join('\n');
}

function cleanHtml(str) {
  return str
    .replace(/<![\s\S]*?-->/g, '')
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/\s+/g, ' ')
    .replace(/&#8217;/g, "'")
    .replace(/&#8216;/g, "'")
    .replace(/&#8220;/g, '"')
    .replace(/&#8221;/g, '"')
    .replace(/&#8230;/g, '…')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/<[^>]+>/g, '')
    .trim();
}

function truncate(str, len = 200) {
  const clean = cleanHtml(str);
  if (clean.length <= len) return clean;
  return clean.substring(0, len).replace(/\s+\S*$/, '') + '…';
}

// Cover gradient by genre
const GRADIENTS = {
  'Adventure': 'linear-gradient(135deg, #1a3a5c 0%, #0f2540 100%)',
  'Historical Fiction': 'linear-gradient(135deg, #2d5a4a 0%, #1a3028 100%)',
  'Literary Fiction': 'linear-gradient(135deg, #5a2d4a 0%, #3a1a28 100%)',
  'Sci-Fi': 'linear-gradient(135deg, #2d3a5a 0%, #1a2040 100%)',
  'Science Fiction': 'linear-gradient(135deg, #2d3a5a 0%, #1a2040 100%)',
  'Thriller': 'linear-gradient(135deg, #5a2d2d 0%, #3a1a1a 100%)',
  'Fantasy': 'linear-gradient(135deg, #3a2d5a 0%, #24103f 100%)',
  'Self-Help': 'linear-gradient(135deg, #4a5a2d 0%, #2a3a1a 100%)',
  "Children's Books": 'linear-gradient(135deg, #5a4a2d 0%, #3a2a1a 100%)',
  'default': 'linear-gradient(135deg, #3a3a3a 0%, #1a1a1a 100%)',
};

function getGradient(genre) {
  return GRADIENTS[genre] || GRADIENTS.default;
}

// ─── Parse Reviews ────────────────────────────────────────────────────────────

function parseReview(dirPath, dirName) {
  const filePath = path.join(dirPath, 'index.html');
  if (!fs.existsSync(filePath)) return null;
  const html = fs.readFileSync(filePath, 'utf8');
  
  const title = getText(html, /<h1[^>]*style="[^"]*">([^<]+)<\/h1>/)
    || getText(html, /<title>([^<]+ \|)/);
  
  const author = getText(html, /href="\/authors"[^>]*>([^<]+)<\/a>/)
    || getText(html, /Author[^<]*<[^>]+>([^<]+)<\/a>/);
  
  const genreMatch = html.match(/<span[^>]*class="[^"]*shelf-item[^"]*"[^>]*>([^<]+)<\/span>/);
  const genre = genreMatch ? genreMatch[1].trim() : 'Fiction';
  
  const starsMatch = html.match(/[★☆]+/);
  const stars = starsMatch ? starsMatch[0] : '★★★';
  
  // Date: look for the date in meta
  const dateMatch = html.match(/(\w+ \d+, \d{4})/);
  const date = dateMatch ? dateMatch[1] : '2026-01-01';
  
  const prose = extractProse(html);
  const excerpt = truncate(prose);
  
  return {
    type: 'book-review',
    title: title.replace(/ \| Bithues.*$/, '').trim(),
    author: author || 'Unknown',
    genre,
    stars,
    date,
    excerpt,
    content: prose,
    slug: slugify(title),
    coverGradient: getGradient(genre),
  };
}

// ─── Parse Stories ───────────────────────────────────────────────────────────

function parseStory(dirPath, dirName) {
  const filePath = path.join(dirPath, 'index.html');
  if (!fs.existsSync(filePath)) return null;
  const html = fs.readFileSync(filePath, 'utf8');
  
  const title = getText(html, /<h1[^>]*style="[^"]*">([^<]+)<\/h1>/)
    || getText(html, /<title>([^<]+ \|)/);
  
  // Stories don't always have author - they might be original
  const author = getText(html, /href="\/authors"[^>]*>([^<]+)<\/a>/) || 'Original Work';
  
  const genreMatch = html.match(/<span[^>]*class="[^"]*shelf-item[^"]*"[^>]*>([^<]+)<\/span>/);
  const genre = genreMatch ? genreMatch[1].trim() : 'Literary Fiction';
  
  const dateMatch = html.match(/(\w+ \d+, \d{4})/);
  const date = dateMatch ? dateMatch[1] : '2026-01-01';
  
  const prose = extractProse(html);
  const excerpt = truncate(prose);
  
  return {
    type: 'short-story',
    title: title.replace(/ \| Bithues.*$/, '').trim(),
    author,
    genre,
    stars: '',
    date,
    excerpt,
    content: prose,
    slug: slugify(title),
    coverGradient: getGradient('Literary Fiction'),
  };
}

// ─── Parse Articles ──────────────────────────────────────────────────────────

function parseArticle(dirPath, dirName) {
  const filePath = path.join(dirPath, 'index.html');
  if (!fs.existsSync(filePath)) return null;
  const html = fs.readFileSync(filePath, 'utf8');
  
  const title = getText(html, /<h1[^>]*style="[^"]*">([^<]+)<\/h1>/)
    || getText(html, /<title>([^<]+ \|)/);
  
  const author = getText(html, /href="\/authors"[^>]*>([^<]+)<\/a>/) || 'Bithues';
  
  // Article topics from sidebar chips
  const topicMatch = html.match(/href="\/topics\/[^"]+"[^>]*class="genre-chip"[^>]*>([^<]+)<\/a>/);
  const genre = topicMatch ? topicMatch[1].trim() : 'Book Lists';
  
  const dateMatch = html.match(/(\w+ \d+, \d{4})/);
  const date = dateMatch ? dateMatch[1] : '2026-01-01';
  
  // Look for article body
  const articleBodyMatch = html.match(/<div[^>]*class="[^"]*article-body[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
  let prose = '';
  if (articleBodyMatch) {
    const body = articleBodyMatch[1];
    const paras = [];
    const re = /<p[^>]*>([\s\S]*?)<\/p>/gi;
    let m;
    while ((m = re.exec(body)) !== null) {
      paras.push(m[1]);
    }
    prose = paras.join('\n');
  } else {
    prose = extractProse(html);
  }
  
  const excerpt = truncate(prose, 200);
  
  return {
    type: 'article',
    title: title.replace(/ \| Bithues.*$/, '').trim(),
    author,
    genre,
    stars: '',
    date,
    excerpt,
    content: prose,
    slug: slugify(title),
    coverGradient: getGradient(genre),
  };
}

// ─── Parse Authors ────────────────────────────────────────────────────────────

function parseAuthor(dirPath, dirName) {
  const filePath = path.join(dirPath, 'index.html');
  if (!fs.existsSync(filePath)) return null;
  const html = fs.readFileSync(filePath, 'utf8');
  
  const name = getText(html, /<h1[^>]*style="[^"]*">([^<]+)<\/h1>/)
    || getText(html, /<title>([^<]+ \|)/);
  
  const bioMatch = html.match(/<div[^>]*class="[^"]*author-bio[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
  const bio = bioMatch ? bioMatch[1] : '';
  
  return {
    type: 'author-profile',
    title: (name || dirName).replace(/ \| Bithues.*$/, '').trim(),
    author: name || dirName,
    genre: 'Author',
    stars: '',
    date: '',
    excerpt: truncate(bio, 200),
    content: bio,
    slug: dirName,
    coverGradient: getGradient('Literary Fiction'),
  };
}

// ─── Build post HTML ──────────────────────────────────────────────────────────

function buildPostHtml(post) {
  const tagClass = {
    'book-review': 'tag--review',
    'short-story': 'tag--story',
    'article': 'tag--article',
    'author-profile': 'tag--genre',
  }[post.type] || 'tag--article';
  
  const tagLabel = {
    'book-review': 'Book Review',
    'short-story': 'Short Story',
    'article': 'Article',
    'author-profile': 'Author',
  }[post.type] || 'Article';
  
  const starsHtml = post.stars
    ? `<div class="post-rating"><span class="stars">${post.stars}</span><span class="rating-text">Book Rating</span></div>` 
    : '';
  
  // Convert content paragraphs to HTML
  const contentHtml = post.content
    .split('\n')
    .filter(p => p.trim())
    .map(p => `<p>${p}</p>`)
    .join('\n');
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${post.title} — Bithues</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>

  <nav class="nav">
    <div class="nav-inner">
      <a href="../index.html" class="nav-logo">Bithues</a>
      <div class="nav-links">
        <a href="../index.html" class="nav-link">Feed</a>
        <a href="../browse.html" class="nav-link">Browse</a>
        <a href="../about.html" class="nav-link">About</a>
      </div>
    </div>
  </nav>

  ${post.type === 'book-review' ? `
  <div class="post-hero" style="background:${post.coverGradient};padding:48px 24px;text-align:center;">
    <div class="post-hero-inner" style="max-width:640px;margin:0 auto;">
      <span class="tag ${tagClass}" style="margin-bottom:12px;display:inline-block;">${tagLabel}</span>
      <h1 class="post-title post-title--cover">${post.title}</h1>
      <p class="post-byline" style="color:rgba(255,255,255,0.8);margin-top:8px;">by ${post.author}</p>
    </div>
  </div>` : `
  <header class="post-header">
    <div class="post-header-inner">
      <div class="post-meta-top">
        <span class="tag ${tagClass}">${tagLabel}</span>
        <span class="post-date">${post.date}</span>
      </div>
      <h1 class="post-title">${post.title}</h1>
      <p class="post-byline">by ${post.author}</p>
    </div>
  </header>`}

  <article class="post-body">
    ${starsHtml}
    <p class="post-lead">${post.excerpt}</p>
    ${contentHtml}
  </article>

  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">Bithues</div>
      <nav class="footer-nav">
        <a href="../index.html">Feed</a>
        <a href="../browse.html">Browse</a>
        <a href="../about.html">About</a>
      </nav>
      <p class="footer-copy">&copy; 2026 Bithues. All rights reserved.</p>
    </div>
  </footer>

</body>
</html>`;
}

// ─── Main ────────────────────────────────────────────────────────────────────

const stats = { reviews: 0, stories: 0, articles: 0, authors: 0, errors: [] };

// --- Reviews ---
const reviewsDir = path.join(WORK, 'reviews');
if (fs.existsSync(reviewsDir)) {
  fs.readdirSync(reviewsDir).forEach(dir => {
    const dirPath = path.join(reviewsDir, dir);
    if (!fs.statSync(dirPath).isDirectory()) return;
    try {
      const post = parseReview(dirPath, dir);
      if (!post || !post.title) { stats.errors.push(`review ${dir}: no title`); return; }
      const slug = post.slug || `review-${dir}`;
      fs.writeFileSync(path.join(CONTENT, `${slug}.html`), buildPostHtml(post));
      stats.reviews++;
      process.stdout.write(`R`);
    } catch (e) {
      stats.errors.push(`review ${dir}: ${e.message}`);
    }
  });
}

// --- Stories (directories) ---
const storiesDir = path.join(WORK, 'stories');
if (fs.existsSync(storiesDir)) {
  fs.readdirSync(storiesDir).forEach(item => {
    const dirPath = path.join(storiesDir, item);
    if (!fs.statSync(dirPath).isDirectory()) return;
    try {
      const post = parseStory(dirPath, item);
      if (!post || !post.title) { stats.errors.push(`story ${item}: no title`); return; }
      const slug = post.slug || item;
      fs.writeFileSync(path.join(CONTENT, `${slug}.html`), buildPostHtml(post));
      stats.stories++;
      process.stdout.write(`S`);
    } catch (e) {
      stats.errors.push(`story ${item}: ${e.message}`);
    }
  });
}

// --- Articles ---
const articlesDir = path.join(WORK, 'articles');
if (fs.existsSync(articlesDir)) {
  fs.readdirSync(articlesDir).forEach(dir => {
    const dirPath = path.join(articlesDir, dir);
    if (!fs.statSync(dirPath).isDirectory()) return;
    try {
      const post = parseArticle(dirPath, dir);
      if (!post || !post.title) { stats.errors.push(`article ${dir}: no title`); return; }
      const slug = post.slug || dir;
      fs.writeFileSync(path.join(CONTENT, `${slug}.html`), buildPostHtml(post));
      stats.articles++;
      process.stdout.write(`A`);
    } catch (e) {
      stats.errors.push(`article ${dir}: ${e.message}`);
    }
  });
}

// --- Authors ---
const authorsDir = path.join(WORK, 'authors');
if (fs.existsSync(authorsDir)) {
  fs.readdirSync(authorsDir).forEach(dir => {
    const dirPath = path.join(authorsDir, dir);
    if (!fs.statSync(dirPath).isDirectory()) return;
    try {
      const post = parseAuthor(dirPath, dir);
      if (!post || !post.title) { stats.errors.push(`author ${dir}: no title`); return; }
      const slug = post.slug || dir;
      fs.writeFileSync(path.join(CONTENT, `author-${slug}.html`), buildPostHtml(post));
      stats.authors++;
      process.stdout.write(`a`);
    } catch (e) {
      stats.errors.push(`author ${dir}: ${e.message}`);
    }
  });
}

console.log('\n\nMigration complete!');
console.log(`  Reviews: ${stats.reviews}`);
console.log(`  Stories: ${stats.stories}`);
console.log(`  Articles: ${stats.articles}`);
console.log(`  Authors: ${stats.authors}`);
console.log(`  Errors: ${stats.errors.length}`);
if (stats.errors.length) {
  stats.errors.slice(0, 10).forEach(e => console.log(`  - ${e}`));
}
