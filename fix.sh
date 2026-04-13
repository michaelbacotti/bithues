#!/bin/bash
# Fix review and story pages to match dna-ancestry structure
# Bash + sed approach

BASE="/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues"
cd "$BASE"

fix_reviews() {
    echo "=== Fixing reviews ==="
    for f in reviews/*.html; do
        fname=$(basename "$f")
        if [[ "$fname" == *"fix"* ]]; then continue; fi
        
        cp "$f" "/tmp/backup_$fname"
        
        # 1. Insert generic hero after </nav> (only if not already present)
        if ! grep -q "Bithues Reading Lab — Reviews" "$f"; then
            sed -i '' '/<\/nav>/{
                r /dev/stdin
            }' "$f" << 'INNER'
  <section class="hero">
    <div class="hero-eyebrow">Bithues Reading Lab — Reviews</div>
    <h1>REVIEW_PLACEHOLDER — Bithues Reading Lab</h1>
    <p>Explore our curated insights and guides on this topic.</p>
  </section>

INNER
        fi
        
        # 2. Wrap <article class="review"> with <section class="section">
        # This is complex with sed - use perl for this step
        perl -i -pe '
            if (/<article\s+class\s*=\s*["\x27]review["\x27]/ && !$wrapped++) {
                $_ = "  <section class=\"section\">\n$_";
            }
            if (/<\/article>/ && $wrapped && !$closed++) {
                $_ = $_ . "\n  </section>";
            }
        ' "$f"
        
        # 3. Convert <div class="share-section"> to <section class="share-section"> (if <section class="share-section"> not already present)
        if ! grep -q '<section class="share-section">' "$f"; then
            sed -i '' 's/<div class="share-section">/<section class="share-section">/g' "$f"
            sed -i '' 's/Share this article/Share this article/g' "$f"
            # Close the section (replace the closing </div> that follows share buttons)
            # This is tricky - only replace </div> after share buttons
            perl -i -pe '
                if (/share-btn/ .. /<\/div>\s*$/ && /<\/div>\s*$/) {
                    $_ = "" unless /share-btn/;
                }
            ' "$f"
        fi
        
        echo "  Processed reviews/$fname"
    done
}

# Can't run multi-line bash functions with backgrounding
# Let's do this in Python instead but simpler

python3 - << 'PYEOF'
import os

BASE = '/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues'
os.chdir(BASE)

def process_file(path, dir_name):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    orig = html
    
    # Determine section label
    sec = 'Reviews' if dir_name == 'reviews' else 'Stories'
    
    # Extract title
    import re
    m = re.search(r'<title>([^<]+)\s+[–-]\s+Bithues', html)
    title = m.group(1) if m else dir_name
    
    # Generic hero
    gen_hero = (
        '  <section class="hero">\n'
        f'    <div class="hero-eyebrow">Bithues Reading Lab — {sec}</div>\n'
        f'    <h1>{title} — Bithues Reading Lab</h1>\n'
        f'    <p>Explore our curated insights and guides on this topic.</p>\n'
        f'  </section>\n\n'
    )
    
    item = 'article' if dir_name == 'reviews' else 'story'
    share = (
        '        <section class="share-section">\n'
        f'            <h3>Share this {item}</h3>\n'
        '            <div class="share-buttons">\n'
        '                <button class="share-btn" onclick="shareTwitter()">𝕏 Twitter</button>\n'
        '                <button class="share-btn" onclick="shareFacebook()">📘 Facebook</button>\n'
        '                <button class="share-btn" onclick="shareLinkedIn()">💼 LinkedIn</button>\n'
        '            </div>\n'
        '        </section>\n'
    )
    
    changed = False
    
    # 1. Inject generic hero after </nav>
    if 'Bithues Reading Lab — ' + sec not in html:
        html = re.sub(r'(</nav>\n)', r'\1' + gen_hero, html, count=1)
        changed = True
    
    # 2. Wrap <article class="review/story"> with <section class="section">
    if '<section class="section">' not in html:
        # Find <article class="review"> and insert section opening before it
        html = re.sub(
            r'(<article\s+class=["\']?(?:review|story)["\']?>)',
            r'  <section class="section">\n\1',
            html, count=1
        )
        # Find </article> followed by share/footer and insert </section> after it
        html = re.sub(
            r'(</article>)(\s*(?:<div\s+class=["\']share|<!--\s*──\s*FOOTER|<footer))',
            r'\1\n  </section>\2',
            html, count=1
        )
        changed = True
    
    # 3. Convert <div class="share-section"> to <section class="share-section">
    if '<div class="share-section">' in html and '<section class="share-section">' not in html:
        # Replace opening div with section
        html = re.sub(r'<div\s+class=["\']share-section["\']>', 
                      '<section class="share-section">', html)
        # Remove the closing </div> for share-section (it's now a section, needs </section>)
        # But we need to be careful not to remove other </div>s
        # Replace the specific </div> that closes share-section with </section>
        html = re.sub(
            r'(<button\s+class=["\']share-btn["\']>.*?</div>)(\s*</div>)',
            r'\1\n        </section>',
            html, count=1
        )
        changed = True
    
    # 4. Add share section before footer if missing
    if '<section class="share-section">' not in html:
        html = re.sub(r'(<footer)', share + r'\1', html, count=1)
        changed = True
    
    has_gen = 'Bithues Reading Lab — ' + sec in html
    has_sec = '<section class="section">' in html
    
    if has_gen and has_sec and changed and html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return 'fixed', has_gen, has_sec
    elif html == orig:
        return 'ok', has_gen, has_sec
    else:
        return f'skip(gen={has_gen} sec={has_sec})', has_gen, has_sec

for dir_name in ['reviews', 'stories']:
    path = BASE + '/' + dir_name
    os.chdir(path)
    files = [f for f in os.listdir('.') if f.endswith('.html') and 'fix' not in f.lower()]
    fixed = ok = err = 0
    for fname in sorted(files):
        full = path + '/' + fname
        try:
            res, g, s = process_file(full, dir_name)
            if res == 'fixed':
                print(f'  FIXED {dir_name}/{fname}')
                fixed += 1
            elif res == 'ok':
                ok += 1
            else:
                print(f'  SKIP {dir_name}/{fname}: {res}')
                ok += 1
        except Exception as e:
            print(f'  ERROR {dir_name}/{fname}: {e}')
            err += 1
    print(f'{dir_name}: {fixed} fixed, {ok} ok, {err} errors')
PYEOF
