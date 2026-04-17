# Bithues Reviews — Redirect Plan

GitHub Pages does not support `.htaccess` or server-side 301 redirects. The fix implemented here uses HTML `<meta http-equiv="refresh">` redirects in the old numeric URL files, pointing them to the named (canonical) URL files.

---

## Redirect Table

| From (redirect) | To (canonical) | Notes |
|---|---|---|
| `reviews/1.html` | `reviews/1_new.html` | Named version kept; numeric URL redirects |
| `reviews/2.html` | `reviews/the-richmond-cipher.html` | Named version kept; numeric URL redirects |
| `reviews/3.html` | `reviews/red-horizon-lunar-launch.html` | Named version kept; numeric URL redirects |
| `reviews/9.html` | `reviews/the-shadow-within.html` | Named version kept; numeric URL redirects |
| `reviews/14.html` | `reviews/otomi.html` | Named version kept; numeric URL redirects |
| `reviews/36.html` | `reviews/perfection-cycle.html` | Named version kept; numeric URL redirects |

---

## Implementation

Each redirect file (e.g., `reviews/1.html`) contains only this minimal HTML:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Redirecting...</title>
  <meta http-equiv="refresh" content="0;url=reviews/the-richmond-cipher.html" />
  <link rel="canonical" href="reviews/the-richmond-cipher.html" />
</head>
<body>
  <p>Redirecting to <a href="reviews/the-richmond-cipher.html">the-richmond-cipher.html</a>...</p>
</body>
</html>
```

## Status

- [x] `reviews/1.html` → redirects to `reviews/1_new.html`
- [x] `reviews/2.html` → redirects to `reviews/the-richmond-cipher.html`
- [x] `reviews/3.html` → redirects to `reviews/red-horizon-lunar-launch.html`
- [x] `reviews/9.html` → redirects to `reviews/the-shadow-within.html`
- [x] `reviews/14.html` → redirects to `reviews/otomi.html`
- [x] `reviews/36.html` → redirects to `reviews/perfection-cycle.html`
