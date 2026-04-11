# LINKS_FIXED.md — Bithues Reading Lab

## Critical Issues Found

### 1. CSS Path Inconsistency — CRITICAL (CSS not loading on some pages)

**Files with absolute `/css/main.css` (broken in subdirectories):**
- reviews/1.html → `/css/main.css` ❌
- reviews/2.html through review 9 — likely same
- stories/1.html → `/css/main.css` ❌
- stories/2.html through stories/9 — likely same
- articles/best-books-spring-2026.html → `/css/main.css` ❌
- articles/hopepunk-fiction.html → `/css/main.css` ❌
- articles/quantum-physics-beginners.html → `/css/main.css` ❌
- articles/hopepunk-beginners-guide.html → likely same
- articles/best-sci-fi-2026.html → likely same
- articles/aliens-disclosure-2026.html → likely same
- Other article files in the same subdirectory batch — likely same

**Files with correct relative `css/main.css`:**
- index.html → `css/main.css` ✅
- reviews/11.html → `css/main.css` ✅
- reviews/10.html → `css/main.css` ✅
- reviews/20.html → `css/main.css` ✅
- stories/10.html → `css/main.css` ✅
- stories/20.html → `css/main.css` ✅
- authors/evan-r-cole.html → `css/main.css` ✅
- authors/michael-bacotti.html → `css/main.css` ✅
- category/self-help.html → `css/main.css` ✅

**Fix:** Change `/css/main.css` to `css/main.css` in all affected files.

---

### 2. Broken Author Link in reviews/index.html — CRITICAL

**Problem:** `href="../authors/s.html"` used for T. Stone, E. Maris, and likely more
- `s.html` does not exist in authors/ directory
- Should be specific per-author pages: `t-stone.html`, `e-maris.html`, etc.

**Fix:** Update author links in reviews/index.html to point to correct filenames.

---

### 3. Review 7 "Veiled Presence" by Bithues — No Author Link

**Problem:** The author "Bithues" has no link to an author page.
**Fix:** Either create authors/bithues.html OR verify this is intentional.

---

### 4. Extra .md Files in Production — articles/ — MEDIUM

- `articles/hopepunk-fiction-guide.md` — not an HTML page, shouldn't be in production
- `articles/mind-bending-books.md` — not an HTML page, shouldn't be in production

**Fix:** Delete these files or rename to .html if content is missing.

---

### 5. Template Files Left in Production — MEDIUM

- `authors/template.html`
- `category/template.html`

**Fix:** Delete these template files.

---

### 6. Duplicate Footer Blocks — LOW

- reviews/index.html has 2 footer blocks
- articles.html has 2 footer blocks  
- authors.html has 4 footer blocks (multiple inline footers + bottom footers)

**Fix:** Remove duplicate footer blocks, keep only one per page.

---

### 7. Missing Author Files (Not Linked from authors.html)

The following author files exist but aren't in the authors.html grid:
- `e-j-marín.html` — E. J. Marín (Otomí, review 14)
- `michael-jr.html` — Michael Jr. (Little Mike books, reviews 27, 29, 34)
- `michael-bacotti.html` — Michael Bacotti (Microbiology ABC's, review 19)
- `evan-r-a-cole.html` — possible duplicate/alternate
- `j-e-mercer.html`
- `leander-vassos.html`

**Fix:** Either add these authors to authors.html grid, or confirm they're intentionally excluded.

---

## Summary of Fixes to Make

1. **Update CSS paths** in all files using `/css/main.css` → `css/main.css` (estimated ~50+ files)
2. **Fix author links** in reviews/index.html
3. **Delete** articles/hopepunk-fiction-guide.md, articles/mind-bending-books.md
4. **Delete** authors/template.html, category/template.html
5. **Remove duplicate footers** from reviews/index.html, articles.html, authors.html
6. **Verify/fix** missing author pages (Bithues author)