# STYLE_SPEC.md — Bithues Reading Lab

## Reference: Homepage (index.html) = Source of Truth

The homepage at `index.html` (and the linked `css/main.css`) is the canonical reference for all styling. Subpages must match.

---

## CSS Custom Properties (from `:root` in css/main.css)

```css
:root {
    --navy:       #0a1628;
    --navy-mid:   #132240;
    --navy-light: #1e3358;
    --gold:       #c8a96e;
    --gold-light: #e2c99a;
    --white:      #ffffff;
    --off-white:  #f5f6f8;
    --gray-light: #e8eaed;
    --gray-mid:   #8a94a6;
    --green:      #2e9e6b;
    --red:        #c94b4b;
    --text-dark:  #1a1f2e;
    --text-body:  #3a4157;
    --shadow:     0 2px 12px rgba(10,22,40,.12);
}
```

---

## Google Fonts

Both imported in `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet" />
```

Font stack:
- Headings: `'Playfair Display', serif`
- Body: `'Inter', system-ui, sans-serif`

---

## Nav HTML Structure (exact markup)

```html
<nav>
  <a href="index.html" class="nav-brand">Bithues <span>Reading Lab</span></a>
  <div class="nav-links">
    <div class="nav-item"><a href="index.html" class="active">Home</a></div>
    <div class="nav-item">
      <a href="catalog.html">Reviews ▾</a>
      <div class="dropdown">
        <a href="catalog.html">All Reviews</a>
        <a href="category/self-help.html">Self-Help</a>
        <a href="category/science-fiction.html">Sci-Fi</a>
        <a href="category/fantasy.html">Fantasy</a>
        <a href="category/nonfiction.html">Nonfiction</a>
        <a href="category/thriller.html">Thriller</a>
        <a href="category/biography.html">Biography</a>
        <a href="category/business.html">Business</a>
      </div>
    </div>
    <div class="nav-item">
      <a href="stories.html">Stories ▾</a>
      <div class="dropdown">
        <a href="stories.html">All Stories</a>
      </div>
    </div>
    <div class="nav-item">
      <a href="articles.html">Articles ▾</a>
      <div class="dropdown">
        <a href="articles.html">All Articles</a>
      </div>
    </div>
    <div class="nav-item"><a href="about.html">About</a></div>
    <div class="nav-item"><a href="contact.html">Contact</a></div>
  </div>
</nav>
```

### Nav CSS (inline style block)
- `nav`: `background: var(--navy)`, sticky, `height: 64px`, `border-bottom: 2px solid var(--gold)`
- `.nav-brand`: Playfair Display, white with gold `<span>`, `text-decoration: none`
- `.nav-links`: `display: flex; align-items: center; gap: 0`
- `.nav-item`: `position: relative`
- `.nav-item > a`: `color: var(--gray-mid)`, `height: 64px`, border-bottom transparent → gold on hover/active
- `.dropdown`: absolute, hidden by default, shown on hover, `background: var(--navy-mid)`, `border-top: 2px solid var(--gold)`
- Dropdown links: `color: var(--gray-mid)`, hover turns `color: var(--gold)` with `background: var(--navy-light)`

---

## Hero Section

```css
.hero {
  background: linear-gradient(160deg, var(--navy) 0%, var(--navy-mid) 60%, #1a3a6a 100%);
  color: var(--white);
  padding: 5rem 2rem 4rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}
/* Subtle grid pattern overlay */
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,...") repeat;
  pointer-events: none;
}
.hero-eyebrow {
  font-size: .8rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 1rem;
  font-weight: 600;
}
.hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.2rem, 5vw, 3.6rem);
  line-height: 1.15;
  margin-bottom: 1.2rem;
  color: var(--white);
}
.hero h1 em { font-style: normal; color: var(--gold); }
.hero p { font-size: 1.1rem; color: rgba(255,255,255,.75); max-width: 640px; margin: 0 auto; }
```

---

## Footer HTML Structure

```html
<footer>
  <div class="footer-brand">Bithues <span>Reading Lab</span></div>
  <p>© <span id="year"></span> Bithues Reading Lab · <a href="press.html">Press</a> · <a href="contact.html">Contact</a> · <a href="privacy.html">Privacy</a></p>
</footer>
<button class="back-to-top" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>
<script>
  window.onscroll = function() {
    document.querySelector('.back-to-top').classList.toggle('visible', window.scrollY > 300);
  };
  document.getElementById('year').textContent = new Date().getFullYear();
</script>
```

### Footer CSS
- `background: var(--navy)`, `color: rgba(255,255,255,.5)`, `padding: 2.5rem 2rem`, centered, `border-top: 2px solid var(--gold)`
- `.footer-brand`: Playfair Display, white with gold `<span>`

---

## Cards Grid

```css
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  max-width: 1100px;
  margin: 0 auto;
}
.card {
  background: var(--white);
  border: 1px solid var(--gray-light);
  border-top: 3px solid var(--gold);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: var(--shadow);
}
.card h3 { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: var(--navy); margin-bottom: .5rem; }
.card h3 a { color: var(--navy); text-decoration: none; }
.card h3 a:hover { color: var(--gold); }
.card .review-tag { background: var(--navy); color: var(--gold); padding: .15rem .5rem; border-radius: 4px; font-size: .7rem; font-weight: 600; }
```

---

## Button / Chip Styles

```css
.chips { padding: 2rem 2rem 0; text-align: center; }
.chips a {
  display: inline-block;
  padding: .4rem 1rem;
  border: 1.5px solid var(--gold);
  border-radius: 20px;
  color: var(--gold);
  text-decoration: none;
  font-size: .8rem;
  font-weight: 500;
  margin: .25rem;
  transition: all .2s;
}
.chips a:hover { background: var(--gold); color: var(--navy); }
```

---

## Back to Top Button

```css
.back-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 44px;
  height: 44px;
  background: var(--gold);
  color: var(--navy);
  border: none;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  display: none;
  align-items: center;
  justify-content: center;
  transition: opacity .3s;
  z-index: 50;
}
.back-to-top.visible { display: flex; }
```

---

## Sections

```css
.section { padding: 3rem 2rem; }
.section-alt { background: var(--white); }
.section-title { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: var(--navy); margin-bottom: .5rem; text-align: center; }
.section-sub { color: var(--gray-mid); text-align: center; margin-bottom: 2rem; }
```

---

## Newsletter Section

```css
.newsletter-section {
  background: linear-gradient(135deg, var(--navy-mid), var(--navy-light));
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  max-width: 700px;
  margin: 0 auto;
  border: 1px solid rgba(200,169,110,.3);
}
.newsletter-section h3 { font-family: 'Playfair Display', serif; color: var(--white); font-size: 1.6rem; margin-bottom: 1rem; }
.newsletter-section p { color: rgba(255,255,255,.7); margin-bottom: 1.5rem; font-size: .95rem; }
```

---

## Key Differences: Homepage vs Subpages

The homepage (`index.html`) has:
- ✅ Complete inline `<style>` block with all nav/hero/footer styles
- ✅ Google Fonts link
- ✅ `css/main.css` stylesheet link
- ✅ Correct `<nav>` with dropdown menus
- ✅ Hero section with correct structure
- ✅ Footer with `footer-brand` class

Some subpages (reviews/index.html, stories.html, articles.html) have:
- ✅ Google Fonts link
- ✅ `css/main.css` stylesheet link
- ✅ Correct nav structure with inline styles
- ✅ Footer (some have duplicate footers — bug)

Authors page:
- ❌ Different nav structure (uses `navbar` class + different markup)
- ❌ Missing inline style block with nav styles
- ❌ Has a second completely different nav inside the page body

---

## Files Needing Style Updates

| File | Needs Nav Fix | Needs Footer Fix | Notes |
|------|-------------|-----------------|-------|
| reviews/index.html | ✅ Has inline styles | ⚠️ Duplicate footers | OK nav, has inline style block |
| stories.html | ✅ Has inline styles | ✅ OK | Has inline style block |
| articles.html | ✅ Has inline styles | ⚠️ Duplicate footers | Has inline style block |
| authors.html | ❌ Missing inline nav styles | ⚠️ Duplicate footers | Has two separate navs in body |
| reviews/1-35.html | 🔲 Need to check | 🔲 Need to check | Individual review pages |
| stories/1-36.html | 🔲 Need to check | 🔲 Need to check | Individual story pages |
| articles/*.html | 🔲 Need to check | 🔲 Need to check | Individual article pages |
| authors/*.html | 🔲 Need to check | 🔲 Need to check | Individual author pages |
| category/*.html | 🔲 Need to check | 🔲 Need to check | Category pages |
