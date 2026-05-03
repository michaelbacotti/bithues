#!/usr/bin/env python3
"""Fix review genres based on actual content analysis."""
import os

# Genre corrections based on content analysis
GENRE_FIXES = {
    "1": "Adventure",
    "2": "Historical Fiction",
    "3": "Science Fiction",
    "4": "Fiction",   # "life's task within harmony" - philosophical fiction
    "5": "Nonfiction",
    "6": "Nonfiction",
    "7": "Nonfiction",
    "8": "Nonfiction",
    "9": "Self-Help",
    "10": "Science Fiction",
    "11": "Science Fiction",
    "12": "Science Fiction",
    "13": "Science Fiction",
    "14": "Historical Fiction",
    "15": "Science",
    "16": "Science",
    "17": "Science",
    "18": "Science",
    "19": "Children",
    "20": "Children",
    "21": "Adventure",
    "22": "Nonfiction",
    "23": "Self-Help",
    "24": "Adventure",
    "25": "Adventure",
    "26": "Literary",
    "27": "Children",
    "28": "Children",
    "29": "Children",
    "30": "Nonfiction",
    "31": "Fiction",   # "seekers embark on a transformative journey" - speculative fiction
    "32": "Nonfiction",
    "33": "Nonfiction",
    "34": "Children",
    "35": "Self-Help",
    "36": "Nonfiction",
    "37": "Science Fiction",
    # Slug-named reviews
    "aetheri-codex": "Science Fiction",
    "beyond-the-veil": "Science Fiction",
    "cords-of-empire": "Fantasy",
    "first-contact-diary": "Science Fiction",
    "home-for-anya": "Romance",
    "horizonte-rojo": "Science Fiction",
    "living-with-a-moving-planet": "Nonfiction",
    "men-of-three-seas": "Historical Fiction",
    "otomi": "Historical Fiction",
    "perfection-cycle": "Nonfiction",
    "probability-of-light": "Science Fiction",
    "quantum-soul-echoes": "Science",
    "red-horizon-lunar-launch": "Science Fiction",
    "the-blueprint": "Science Fiction",
    "the-confluence-doctrine": "Science Fiction",
    "the-martian": "Science Fiction",
    "the-power-of-changing-your-mind": "Self-Help",
    "the-richmond-cipher": "Historical Fiction",
    "the-shadow-within": "Self-Help",
    "three-seas": "Historical Fiction",
    "veiled-presence": "Nonfiction",
    "virus-childrens-story": "Children",
    "xaltocan": "Historical Fiction",
}

REVIEWS_DIR = "/Users/mike/.openclaw/workspace-bacottibot/bithues-hugo/content/reviews"
count = 0
for filename, genre in GENRE_FIXES.items():
    path = os.path.join(REVIEWS_DIR, f"{filename}.md")
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
        
        # Replace genre in frontmatter
        import re
        # Handle quoted or unquoted genre values
        new_content = re.sub(
            r'^genre:.*$',
            f'genre: "{genre}"',
            content,
            count=1,
            flags=re.MULTILINE
        )
        
        if new_content != content:
            with open(path, 'w') as f:
                f.write(new_content)
            count += 1
            print(f"Fixed: {filename}.md → {genre}")

print(f"\nTotal fixed: {count}")