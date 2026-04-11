# CONTENT_AUDIT.md — Bithues Reading Lab

## Reviews Section

**reviews/index.html** lists: 35 reviews (1–35, no gaps)

**Files in reviews/ directory:**
- Numbered: 1.html through 36.html (36 files) ✅
- Extra: aetheri-codex.html, beyond-the-veil.html, index.html, living-with-a-moving-planet.html, otomi.html, quantum-soul-echoes.html, red-horizon-lunar-launch.html, the-confluence-doctrine.html, the-power-of-changing-your-mind.html, the-richmond-cipher.html, the-shadow-within.html, three-seas.html, veiled-presence.html (13 extra non-numbered files)

**MISMATCH:** 35 listed but 36 numbered files exist. Review 36 (which one?) is in filesystem but not listed in index. The numbered files don't directly correspond to the 35 listed reviews.

**Author links in reviews/index.html:**
- `href="../authors/s.html"` — used for T. Stone (review 1), E. Maris (review 2), and possibly others. This filename doesn't match any file in the authors directory.
- **Missing author pages:** "Bithues" (review 7) — no author page link exists
- The short filename `s.html` doesn't exist in the authors directory. Should be `t-stone.html` and `e-maris.html`

**Extra review files not listed in index:**
- `three-seas.html` (Maritime epic — appears on homepage "Men of the Three Seas" with Amazon link)
- `otomi.html` → maps to review 14 (Otomí by E. J. Marín)
- `veiled-presence.html` → maps to review 7 (Veiled Presence by Bithues)
- `the-richmond-cipher.html` → review 2
- `red-horizon-lunar-launch.html` → review 3
- `the-confluence-doctrine.html` → review 4
- `living-with-a-moving-planet.html` → review 5
- `beyond-the-veil.html` → review 6
- `the-power-of-changing-your-mind.html` → review 8
- `the-shadow-within.html` → review 9
- `aetheri-codex.html` → review 10 (Echoes of Aetheris by Aetheri Codex)
- `quantum-soul-echoes.html` → review 18

---

## Stories Section

**stories.html** lists: 36 stories in JavaScript array (1–36, no gaps)

**Files in stories/ directory:** 1.html through 36.html (36 files) ✅

All 36 stories present, no gaps.

---

## Articles Section

**articles.html** lists: 32 article cards in HTML (some appear truncated)

**Files in articles/ directory:** 34 .html files + 2 .md files

.md files (should not be in production):
- `hopepunk-fiction-guide.md`
- `mind-bending-books.md`

**Missing links from articles.html cards:**
- Articles.html has `<a href="articles/dna-ancestry-historical-fiction.html">` — but only `dna-ancestry-historical-fiction.html` (33 chars) exists; need to verify exact filename

**Article files confirmed present:**
- best-books-spring-2026.html ✅
- quantum-physics-beginners.html ✅
- hopepunk-fiction.html ✅

---

## Authors Section

**authors.html** lists: 24 author cards

**Files in authors/ directory:** 32 .html files + 1 template.html

**Extra author files (not in authors.html listing):**
- `e-j-marín.html` — E. J. Marín (writes Otomí, mentioned in reviews but not in author grid)
- `evan-r-a-cole.html` — duplicate of evan-r-cole.html? Or alternate name?
- `j-e-mercer.html`
- `leander-vassos.html`
- `michael-jr.html` — Michael Jr. (Little Mike books)
- `michael-bacotti.html` — Michael Bacotti (Microbiology ABC's)
- `template.html` — template file left in production

**Author listing includes:** quantum-chronos (4 books), but the reviews show reviews 15, 16, 17, 18 all by Quantum Chronos

---

## Category Pages

**Files in category/ directory:** 19 .html files (self-help, sci-fi, fantasy, etc.) + template.html

**template.html** left in production in category/ directory.

---

## Summary of Content Issues

| Category | Issue | Severity |
|----------|-------|----------|
| Reviews | `href="../authors/s.html"` broken — should point to specific author files | HIGH |
| Reviews | Review 7 "Veiled Presence" by Bithues — no author page | MEDIUM |
| Authors | 6 author files exist but not in authors.html grid | MEDIUM |
| Articles | 2 .md files in production (not HTML) | MEDIUM |
| Category | template.html left in production | LOW |
| Authors | template.html left in production | LOW |
| Reviews/Authors | Multiple duplicate footers on authors.html, reviews/index.html, articles.html | LOW |
| Articles | Some article cards appear truncated in articles.html | LOW |

---

## CSS Path Issues (Link Audit Finding)

- **reviews/1.html** uses `<link rel="stylesheet" href="/css/main.css">` (absolute path with leading slash) — works on bithues.com root but may not work in subdirectories
- **stories/1.html** uses `<link rel="stylesheet" href="/css/main.css">` (same issue)
- **articles/best-books-spring-2026.html** uses `<link rel="stylesheet" href="/css/main.css">` (same issue)
- Other pages use `href="css/main.css"` (correct relative path)

This is a path mismatch: some subpage files use absolute `/css/main.css` while being in a subdirectory. The homepage and most pages use relative `css/main.css`. This would cause CSS to fail to load on those specific pages.