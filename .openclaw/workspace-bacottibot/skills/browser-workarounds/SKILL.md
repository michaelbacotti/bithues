---
name: browser-workarounds
description: Patterns for overcoming common browser automation obstacles — cookie banners, Cloudflare challenges, React buttons, session loss, and dynamic content. Use when normal browser.snapshot/act calls fail or return unexpected elements.
---

# browser-workarounds

## When to Use This Skill

Your normal browser calls are failing or returning nothing useful. Specifically:
- Cookie consent banners blocking interactions
- Cloudflare/JavaScript challenges preventing page access
- Buttons with no detectable selectors (React/Vue shadow DOM, dynamic IDs)
- Session/auth state lost between navigations
- Forms that silently reject or ignore input
- Sites that detect and block automation

---

## Priority Order of Fixes

### 1. Cookie Consent Banners (Onetrust, etc.)

Cloudflare and most sites use Onetrust cookie banners. The close button is often buried in a shadow DOM or dynamically rendered.

```javascript
// Try these in order — stop at the first that works:
document.getElementById('onetrust-accept-btn-handler')?.click();
document.querySelector('.onetrust-pc-dark-filter')?.remove();
document.querySelector('[aria-label="Accept all cookies"]')?.click();
document.querySelector('#cookieLawInfoAllowCookieBTN')?.click();
// Onetrust close (found in wild):
var btns = document.querySelectorAll('button');
for (var i=0; i<btns.length; i++) {
  var t = btns[i].textContent.trim();
  if (t.includes('Accept') || t.includes('Agree') || t.includes('Allow')) {
    btns[i].click(); break;
  }
}
```

**Or via browser evaluation:**
```
browser(action=act, fn=(function() { var b = document.getElementById('onetrust-accept-btn-handler'); if(b) b.click(); return b ? 'clicked' : 'not found'; })(), kind=evaluate)
```

### 2. Stubborn Buttons (React/Vue/No Selectors)

When `snapshot` shows a button but `act` can't find it by ref — use JavaScript evaluation to find and click by text content:

```javascript
// Click by button text
var btns = document.querySelectorAll('button, a, [role="button"]');
for (var i=0; i<btns.length; i++) {
  var t = btns[i].textContent.trim();
  if (t.includes('Add Pseudonym') || t.includes('Add record') || t.includes('Save')) {
    btns[i].click(); break;
  }
}
```

**Via evaluate:**
```
browser(action=act, fn=(function() { var btns=document.querySelectorAll('button'); for(var i=0;i<btns.length;i++){if(btns[i].textContent.includes('TARGET_TEXT')){btns[i].click();return'clicked: '+btns[i].textContent;}}return'not found';})(), kind=evaluate)
```

**Via direct JS click:**
```
browser(action=act, fn=(function() { document.querySelector('button[class*="submit"]').click(); })(), kind=evaluate)
```

### 3. Modal/Dialog Detection

Always check for modals before interacting with a page:

```javascript
var modals = document.querySelectorAll('[role=dialog], .modal, .slide-out, .Toastify');
if (modals.length > 0) {
  var inner = Array.from(modals).map(function(m) { return m.textContent.trim().slice(0,200); });
  return 'MODALS: ' + JSON.stringify(inner);
}
```

### 4. React/Vue Shadow DOM

When elements exist but have no stable attributes:

```javascript
// Find all buttons and log their text + rough position
var btns = document.querySelectorAll('*');
var found = [];
for (var i=0; i<btns.length; i++) {
  var t = btns[i].textContent.trim();
  if (t.length > 2 && t.length < 100) {
    var r = btns[i].getBoundingClientRect();
    if (r.width > 0 && r.height > 0) {
      found.push({text: t.slice(0,50), x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)});
    }
  }
}
return JSON.stringify(found.slice(0, 50));
```

### 5. Session/Auth Loss (Cloudflare, Login Walls)

**Prevention:**
- Always navigate to login-dependent sites FIRST before doing anything else
- If Cloudflare challenge appears, wait with `page.waitForLoadState('networkidle')`
- For sites that lose session mid-session: do all auth-gated actions in one continuous session

**Cloudflare detection:**
```javascript
var body = document.body.innerText;
if (body.includes('Checking your browser') || body.includes('Cloudflare')) {
  return 'CLOUDFLARE_CHALLENGE';
}
```

### 6. Forms That Ignore Input

When `fill` or `type` don't trigger React state:
```javascript
// Dispatch native input event after setting value
var input = document.querySelector('input[name="EMAIL"]');
input.value = 'test@example.com';
input.dispatchEvent(new Event('input', { bubbles: true }));
input.dispatchEvent(new Event('change', { bubbles: true }));
```

### 7. Drag-and-Drop or Complex Interactions

```javascript
// Simulate drag
var src = document.querySelector('[draggable="true"]');
var tgt = document.querySelector('.drop-zone');
var dt = { effectAllowed: 'all', dropEffect: 'none', data: {} };
var dragStart = src.dispatchEvent(new DragEvent('dragstart', dt));
// ... simplified — prefer clicking via keyboard/menu if available
```

### 8. Handling iFrames

```javascript
// Access iframe content
var iframe = document.querySelector('iframe[name="oauth"]');
if (iframe) {
  var iwin = iframe.contentWindow;
  var idoc = iframe.contentDocument || iframe.contentWindow.document;
  return idoc.body.innerText.slice(0, 500);
}
```

---

## Site-Specific Notes

### Cloudflare DNS Dashboard (dash.cloudflare.com)
- Cookie banner (Onetrust) appears on almost every page load
- Close it FIRST before any navigation
- Session expires quickly — do DNS operations in one session without navigating away
- If you get "Verify you are human" → need to wait or use external auth

### Google AdSense (adsense.google.com)
- Cookie warning can be dismissed
- Site status sometimes lags — "Not found" may clear in 24-48hrs
- No manual verify button in the UI — need to wait for crawler

### Amazon/KDP (author.amazon.com, kdp.amazon.com)
- React-rendered buttons with no stable IDs
- Pseudonym management: "Add Pseudonym" button at bottom of /profile page
- Use JS evaluation to find and click by text
- Sessions can expire mid-session

### Goodreads (goodreads.com)
- Dynamic content loaded via JS
- Cookie banners common
- Author claim process: search by author name, click "Claim" on each book
- "Claim this author" link is separate from individual book claiming

---

## What NOT to Try to Automate

- **File upload dialogs** — must be done manually (browser can't inject file paths into OS dialogs)
- **CAPTCHA** — skip entirely
- **SMS/Phone 2FA** — requires human
- **Google OAuth consent screens** — navigate to the consent URL with parameters already set
- **Sites with aggressive bot detection** (some banking sites) — may never work reliably

---

## Debugging Tips

1. **Snapshot vs Evaluate** — `snapshot` shows rendered DOM, `evaluate` runs JS and can find invisible elements
2. **Check for iframes** — some login forms live in hidden iframes
3. **Log ALL buttons** when stuck:
   ```javascript
   var btns = document.querySelectorAll('button');
   return Array.from(btns).map(b => b.textContent.trim() + '|' + b.className).join('\n');
   ```
4. **Screenshot** when `screenshot` tool fails, try `canvas(action=snapshot)` for a different capture method
5. **Take a break** — some anti-bot detections clear after a few minutes

---

## Pattern: Multi-Step Recovery

When a site blocks you mid-task:

```
1. Stop all navigation
2. Check for modal/challenge (rule 3 above)
3. If challenge → wait 10s, then re-navigate to the target page
4. If still blocked → do the specific action manually and report to user
5. Document the block pattern in this skill for future reference
```
