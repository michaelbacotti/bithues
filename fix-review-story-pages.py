#!/usr/bin/env python3
"""
Fix review and story HTML pages to match dna-ancestry article structure.

Target structure:
  <nav>...</nav>
  <section class="hero">  <- generic site hero (inserted)
  <header class="hero">   <- specific page hero (already present)
  <div class="chips">     <- category chips
  <section class="section">
    <article class="review"> or <article class="story">
      ...content...
    </article>
  </section>
  <section class="share-section">
    <h3>Share this article/story</h3>
    <div class="share-buttons">...</div>
  </section>
  <footer>...</footer>
"""

import sys
import os
from html.parser import HTMLParser

BASE = '/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues'

class HTMLFixer(HTMLParser):
    def __init__(self, dir_name, file_name):
        super().__init__()
        self.dir_name = dir_name
        self.file_name = file_name
        self.path = os.path.join(BASE, dir_name, file_name)
        
        with open(self.path, 'r', encoding='utf-8', errors='replace') as f:
            self.orig_html = f.read()
        
        self.result_parts = []
        self.tag_stack = []  # stack of open tags
        self.phase = 'nav'   # nav -> hero -> article_body -> share -> footer
        self.inject_generic_hero = False
        self.generic_hero_injected = False
        self.injected_share_section = False
        self.in_section_wrapper = False
        self.seen_article_close = False
        self.skip_tags = set()  # tags to skip entirely
        
        # Detect what kind of section this is
        if 'Reviews' in self.orig_html and 'Articles' not in self.orig_html:
            self.section_label = 'Reviews'
        elif 'Stories' in self.orig_html:
            self.section_label = 'Stories'
        else:
            self.section_label = dir_name.capitalize()
        
        # Extract title for generic hero
        import re
        m = re.search(r'<title>([^<]+)\s+–\s+Bithues\s+Reading\s+Lab</title>', self.orig_html)
        if m:
            self.page_title = m.group(1)
        else:
            self.page_title = file_name.replace('.html', '').replace('-', ' ').title()
        
        self.item_type = 'article' if dir_name == 'reviews' else 'story'
    
    def make_generic_hero(self):
        return (
            '<section class="hero">\n'
            f'    <div class="hero-eyebrow">Bithues Reading Lab — {self.section_label}</div>\n'
            f'    <h1>{self.page_title} — Bithues Reading Lab</h1>\n'
            f'    <p>Explore our curated insights and guides on this topic.</p>\n'
            f'  </section>\n\n'
        )
    
    def make_share_section(self):
        return (
            '        <section class="share-section">\n'
            f'            <h3>Share this {self.item_type}</h3>\n'
            '            <div class="share-buttons">\n'
            '                <button class="share-btn" onclick="shareTwitter()">𝕏 Twitter</button>\n'
            '                <button class="share-btn" onclick="shareFacebook()">📘 Facebook</button>\n'
            '                <button class="share-btn" onclick="shareLinkedIn()">💼 LinkedIn</button>\n'
            '            </div>\n'
            '        </section>\n'
        )
    
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            return
        
        attrs_dict = dict(attrs)
        attrs_str = ''.join(f' {k}="{v}"' for k, v in attrs)
        cls = attrs_dict.get('class', '')
        
        # Inject generic hero before first hero (section or header)
        if not self.generic_hero_injected and tag in ('section', 'header') and 'hero' in cls:
            self.result_parts.append(self.make_generic_hero())
            self.generic_hero_injected = True
            self.inject_generic_hero = True
        
        # Phase management
        if self.phase == 'nav' and tag == 'nav':
            self.phase = 'nav'
        
        # Convert content-wrapper div with gradient style -> skip (we add section wrapper)
        if tag == 'div' and cls == 'content-wrapper' and 'style' in attrs_dict:
            if 'linear-gradient' in attrs_dict.get('style', ''):
                self.skip_tags.add('div')  # skip this div and its close
                return
        
        # Track entering article.review or article.story
        if tag == 'article' and ('review' in cls or 'story' in cls):
            if not self.in_section_wrapper and self.phase == 'article_body':
                self.result_parts.append('  <section class="section">\n')
                self.in_section_wrapper = True
            self.phase = 'article_open'
        
        # Detect bare <article> in stories (no class)
        if tag == 'article' and not cls:
            if not self.in_section_wrapper:
                self.result_parts.append('  <section class="section">\n')
                self.in_section_wrapper = True
            self.result_parts.append(f'<article class="story"{attrs_str}>')
            self.phase = 'article_open'
            return
        
        # Track leaving article tag
        if tag == 'article':
            self.tag_stack.append(('article', cls))
        else:
            self.tag_stack.append((tag, cls))
        
        if self.phase == 'article_open' and tag not in ('article',):
            pass  # fall through
        
        self.result_parts.append(f'<{tag}{attrs_str}>')
    
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_tags.discard(tag)
            return
        
        if not self.tag_stack or self.tag_stack[-1][0] != tag:
            # Malformed HTML, just append
            self.result_parts.append(f'</{tag}>')
            return
        
        self.tag_stack.pop()
        
        # Close article -> inject </section> after </article>
        if tag == 'article' and not self.seen_article_close:
            cls = self.tag_stack[-1][1] if self.tag_stack else '' if self.tag_stack else ''
            self.result_parts.append('</article>')
            if self.in_section_wrapper:
                self.result_parts.append('  </section>')
                self.in_section_wrapper = False
            self.seen_article_close = True
            self.phase = 'share'
            return
        
        # Convert <div class="share-section"> to <section class="share-section">
        if tag == 'div' and self.phase == 'share' and not self.injected_share_section:
            # Check if this was the share-section div opener
            if len(self.result_parts) > 0:
                last = self.result_parts[-1]
                if 'share-section' in last:
                    # Remove the opening div from result (already added as section)
                    self.result_parts.pop()
                    self.result_parts.append(self.make_share_section())
                    self.injected_share_section = True
                    return
        
        # Skip <div class="share-section"> close tag
        if tag == 'div' and self.phase == 'share':
            # Check if it's the close of share-section div we already handled
            return
        
        self.result_parts.append(f'</{tag}>')
    
    def handle_data(self, data):
        self.result_parts.append(data)
    
    def fix(self):
        # Override the parser to handle unclosed tags properly
        self.result_parts = []
        self.tag_stack = []
        self.skip_tags = set()
        self.phase = 'nav'
        self.in_section_wrapper = False
        self.seen_article_close = False
        self.generic_hero_injected = False
        self.injected_share_section = False
        self.inject_generic_hero = False
        
        # Check if share section already exists as <section>
        has_share_section = '<section class="share-section"' in self.orig_html
        
        # Parse the original HTML
        try:
            self.feed(self.orig_html)
        except Exception as e:
            print(f"  PARSE ERROR: {e}", file=sys.stderr)
            return None
        
        result = ''.join(self.result_parts)
        
        # Verify
        has_gen = 'Bithues Reading Lab — ' in result and self.section_label in result
        has_sec = '<section class="section">' in result
        
        # If share section missing and we didn't inject, try inserting before footer
        if not has_share_section and not self.injected_share_section:
            if '<footer' in result:
                share = self.make_share_section()
                result = result.replace('<footer', share + '<footer', 1)
                self.injected_share_section = True
        
        if has_gen and has_sec:
            return result
        elif result == self.orig_html:
            return 'ok'
        else:
            return f'skip(gen={has_gen} sec={has_sec})'


def process_dir(dir_name):
    dir_path = os.path.join(BASE, dir_name)
    os.chdir(dir_path)
    
    files = [f for f in os.listdir('.') if f.endswith('.html') and 'fix' not in f.lower()]
    fixed = ok = errors = 0
    
    for f in sorted(files):
        fixer = HTMLFixer(dir_name, f)
        result = fixer.fix()
        
        if result is None:
            errors += 1
            print(f"  ERROR {dir_name}/{f}", file=sys.stderr)
        elif result == 'ok':
            ok += 1
        elif result.startswith('skip'):
            ok += 1
            print(f"  SKIP {dir_name}/{f}: {result}")
        else:
            with open(fixer.path, 'w', encoding='utf-8') as out_f:
                out_f.write(result)
            fixed += 1
            print(f"  FIXED {dir_name}/{f}")
    
    print(f"{dir_name}: {fixed} fixed, {ok} ok/skipped, {errors} errors")
    return fixed, ok, errors


rf, rk, re = process_dir('reviews')
sf, sk, se = process_dir('stories')
print(f"\nTOTAL: reviews({rf} fixed) stories({sf} fixed)")
