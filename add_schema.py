#!/usr/bin/env python3
"""Add Schema.org JSON-LD to review pages"""
import re
import os
import json

reviews_dir = "/Users/mike/.openclaw/workspace/Website/bithues-reading-lab/reviews"

def extract_book_info(file_path):
    """Extract book info from review page"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract title (between <title> and </title>)
    title_match = re.search(r'<title>([^–]+)–([^|]+)', content)
    if not title_match:
        return None
    
    book_title = title_match.group(1).strip()
    author = title_match.group(2).strip()
    
    # Extract description/TLDR
    tldr_match = re.search(r'<p class="tldr">([^<]+)', content)
    tldr = tldr_match.group(1).strip() if tldr_match else ""
    
    # Extract rating (if any)
    rating_match = re.search(r'(\d+)\s*stars?', content, re.IGNORECASE)
    rating = int(rating_match.group(1)) if rating_match else None
    
    # Extract Amazon link
    amazon_match = re.search(r'href="(https://amzn\.to/[^"]+)', content)
    amazon_link = amazon_match.group(1) if amazon_match else None
    
    # Extract review body for word count
    content_match = re.search(r'<div class="review-content">(.+?)</div>', content, re.DOTALL)
    review_text = content_match.group(1) if content_match else ""
    word_count = len(review_text.split())
    
    # Extract date
    date_match = re.search(r'published.*?(\w+\s+\d+,\s+\d{4})', content, re.IGNORECASE)
    date_published = date_match.group(1) if date_match else None
    
    return {
        'title': book_title,
        'author': author,
        'description': tldr,
        'rating': rating,
        'amazon_link': amazon_link,
        'word_count': word_count,
        'date_published': date_published
    }

def create_schema(book_info, file_name):
    """Create JSON-LD schema"""
    # Determine schema type
    if 'fiction' in book_info.get('description', '').lower() or 'fantasy' in book_info.get('description', '').lower():
        schema_type = "Book"
    else:
        schema_type = "Book"
    
    schema = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": book_info['title'],
        "author": {
            "@type": "Person",
            "name": book_info['author']
        },
        "description": book_info['description'],
        "url": f"https://bithues.com/reviews/{file_name}",
    }
    
    if book_info.get('rating'):
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": book_info['rating'],
            "bestRating": 5,
            "worstRating": 1,
            "ratingCount": 1
        }
    
    if book_info.get('amazon_link'):
        schema["offers"] = {
            "@type": "Offer",
            "url": book_info['amazon_link'],
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock"
        }
    
    return json.dumps(schema, indent=2)

def add_schema_to_file(file_path):
    """Add Schema.org markup to a review file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Skip if already has schema
    if 'application/ld+json' in content:
        print(f"  Skipping {os.path.basename(file_path)} - already has schema")
        return
    
    book_info = extract_book_info(file_path)
    if not book_info:
        print(f"  Error parsing {os.path.basename(file_path)}")
        return
    
    file_name = os.path.basename(file_path)
    schema_json = create_schema(book_info, file_name)
    
    # Find where to insert (before </head>)
    schema_tag = f'\n    <script type="application/ld+json">\n{schema_json}\n    </script>'
    
    # Insert before </head>
    new_content = content.replace('</head>', schema_tag + '\n</head>')
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"  Added schema to {file_name}")

# Process all review HTML files
print("Adding Schema.org markup to review pages...")

files = sorted([f for f in os.listdir(reviews_dir) if f.endswith('.html') and f != 'index.html'])

for file in files:
    file_path = os.path.join(reviews_dir, file)
    if os.path.isfile(file_path):
        add_schema_to_file(file_path)

print("Done!")
