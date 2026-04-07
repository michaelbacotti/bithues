#!/bin/bash
# Fix CSS paths and nav links in bithues articles/ and stories/ HTML files

TOKEN="$(cat ~/.openclaw/credentials/github.txt)"
REPO="michaelbacotti/bithues"
AUTH_HEADER="Authorization: Bearer $TOKEN"

ARTICLES=(
    "aliens-disclosure-2026.html" "best-books-spring-2026.html" "best-books-summer-2026.html"
    "best-sci-fi-2026.html" "books-change-how-you-think.html" "books-for-dad-gift-guide.html"
    "books-like-physics-of-time.html" "books-like-project-hail-mary.html"
    "business-leadership-guide.html" "complete-fantasy-encyclopedia.html"
    "fantasy-for-beginners.html" "hopepunk-beginners-guide.html" "hopepunk-fiction.html"
    "horror-for-beginners.html" "how-to-read-more-books.html" "how-we-review-books.html"
    "kids-reading-guide.html" "little-mike-series.html" "meet-indie-authors.html"
    "memoir-biography-guide.html" "quantum-physics-beginners-guide.html"
    "quantum-physics-beginners.html" "read-more-this-year.html" "reading-challenge-2026.html"
    "romance-for-beginners.html" "shadow-work-guide.html" "speed-reading-basics.html"
    "thriller-mystery-guide.html" "ultimate-sci-fi-guide.html" "why-indie-authors-rising.html"
    "why-read-outside-your-genre.html"
)

STORIES=(
    "1.html" "2.html" "3.html" "4.html" "5.html" "6.html" "7.html" "8.html" "9.html" "10.html"
    "11.html" "12.html" "13.html" "14.html" "15.html" "16.html" "17.html" "18.html" "19.html" "20.html"
    "21.html" "22.html" "23.html" "24.html" "25.html" "26.html" "27.html" "28.html" "29.html" "30.html"
    "31.html" "32.html" "33.html" "34.html" "35.html" "36.html"
)

fix_file() {
    local folder="$1"
    local filename="$2"
    local path="${folder}/${filename}"
    
    # Get sha and content
    local response
    response=$(curl -s -H "$AUTH_HEADER" \
        "https://api.github.com/repos/${REPO}/contents/${path}")
    
    local sha content
    sha=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])")
    content=$(echo "$response" | python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode('utf-8'))")
    
    # Apply fixes
    local fixed="$content"
    
    # Fix 1: CSS path
    fixed="${fixed//href=\"css\/main.css\"/href=\"..\/css\/main.css\"}"
    
    # Fix 2: Nav links
    fixed="${fixed//href=\"index.html\"/href=\"..\/index.html\"}"
    fixed="${fixed//href=\"stories.html\"/href=\"..\/stories.html\"}"
    fixed="${fixed//href=\"catalog.html\"/href=\"..\/catalog.html\"}"
    fixed="${fixed//href=\"articles.html\"/href=\"..\/articles.html\"}"
    fixed="${fixed//href=\"about.html\"/href=\"..\/about.html\"}"
    fixed="${fixed//href=\"contact.html\"/href=\"..\/contact.html\"}"
    
    # Check if changed
    if [[ "$content" == "$fixed" ]]; then
        echo "  SKIP $path (no changes)"
        return 0
    fi
    
    # Encode content for API
    local encoded
    encoded=$(echo "$fixed" | base64 | tr -d '\n')
    
    # Push update
    local result
    result=$(curl -s -H "$AUTH_HEADER" \
        -H "Content-Type: application/json" \
        -X PUT \
        -d "{\"message\":\"Fix CSS path and nav links in ${path}\",\"content\":\"${encoded}\",\"sha\":\"${sha}\"}" \
        "https://api.github.com/repos/${REPO}/contents/${path}")
    
    if echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if 'commit' in d else 1)" 2>/dev/null; then
        echo "  FIXED $path"
    else
        echo "  ERROR $path: $(echo "$result" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("message","?"))' 2>/dev/null || echo "unknown")"
    fi
}

export -f fix_file
export AUTH_HEADER REPO TOKEN

echo "=== Articles ==="
for f in "${ARTICLES[@]}"; do
    fix_file "articles" "$f"
done

echo ""
echo "=== Stories ==="
for f in "${STORIES[@]}"; do
    fix_file "stories" "$f"
done
