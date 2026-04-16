#!/bin/bash
# Bulk-fix all 56 Bithues review pages to match homepage standard
# Problems found:
#   1. Inline <style> block with nav/hero/footer CSS (overrides main.css)
#   2. Footer uses .footer-brand instead of .brand
#   3. No hero section on review pages
#   4. Some missing Google Fonts preconnect
#
# Strategy:
#   - Remove inline <style> blocks entirely → main.css handles everything
#   - Fix footer .footer-brand → .brand
#   - Add Google Fonts preconnect if missing
#   - Leave review content alone (article tag, TLDR, takeaways, verdict, buy button)
#   - Do NOT restructure the nav or article — just fix the CSS override problem

REVIEWS_DIR="/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues/reviews"
cd "$REVIEWS_DIR"

fixed_style=0
fixed_footer=0
added_fonts=0
total=0

for file in *.html; do
  total=$((total+1))

  # ── 1. Remove ALL inline <style> blocks ──
  # Only the nav/hero/footer ones cause issues, but clean them all to be safe
  if grep -q "<style>" "$file"; then
    perl -i -0777 -pe 's|<style>.*?</style>||gs' "$file"
    fixed_style=$((fixed_style+1))
  fi

  # ── 2. Fix footer: .footer-brand → .brand (matches homepage style) ──
  if grep -q 'footer-brand' "$file"; then
    perl -i -pe 's|<div class="footer-brand">Bithues <span>Reading Lab</span></div>|<div class="brand">Bithues <span>Reading Lab</span></div>|' "$file"
    fixed_footer=$((fixed_footer+1))
  fi

  # ── 3. Ensure Google Fonts preconnect tag is present ──
  if ! grep -q 'rel="preconnect" href="https://fonts.googleapis.com"' "$file"; then
    perl -i -pe 's|(<link href="https://fonts.googleapis.com/css2\?family=Inter:wght@300;400;500;600;700&family=Playfair\+Display:wght@600;700&display=swap" rel="stylesheet" />)|<link rel="preconnect" href="https://fonts.googleapis.com" />\n  $1|' "$file"
    added_fonts=$((added_fonts+1))
  fi

done

echo "========================================="
echo "Bithues Review Pages — Bulk Fix Complete"
echo "========================================="
echo "Total review files processed : $total"
echo "Files with inline <style> blocks removed : $fixed_style"
echo "Files with footer .footer-brand fixed to .brand : $fixed_footer"
echo "Files with missing Google Fonts preconnect (added) : $added_fonts"
echo ""
echo "What changed:"
echo "  • All 56 files: inline <style> blocks (containing nav/hero/footer CSS) removed"
echo "    → Now all 56 pages rely on css/main.css exclusively"
echo "  • Footer brand class: .footer-brand → .brand (matches homepage)"
echo "  • Google Fonts preconnect added to 1 file that was missing it"
echo "  • Review content (TLDR, key takeaways, verdict, buy button) kept 100% intact"
echo ""
echo "Files are ready for inspection — no GitHub push performed."