#!/usr/bin/env python3
"""Process all book pages - add Schema.org JSON-LD."""
import subprocess, json, base64, re, sys, os

TOKEN = os.environ.get("GH_TOKEN", "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")
REPO = "michaelbacotti/bithues"

TRACKER = {
    1:  {"title": "The Dawn of Civilization", "subtitle": "A Story of a Prehistoric Tribe's Struggle for Survival", "author": "T. Stone", "asin": "4sYlT3t"},
    2:  {"title": "The Richmond Cipher", "subtitle": "", "author": "E. Maris", "asin": "4snAwxv"},
    3:  {"title": "Red Horizon: Lunar Launch", "subtitle": "", "author": "M. A. Hale", "asin": "40NsrpN"},
    4:  {"title": "The Confluence Doctrine", "subtitle": "", "author": "Alaric Wynn", "asin": "3Pm0iUi"},
    5:  {"title": "Living with a Moving Planet", "subtitle": "Deep Time, Human Adaptation, and a Positive Climate Future", "author": "J. T. Hartley", "asin": "4lHbruZ"},
    6:  {"title": "Beyond the Veil", "subtitle": "Quantum Speculations on Consciousness, Death, and the Universe", "author": "D. E. Harlan", "asin": "480RlWP"},
    7:  {"title": "Veiled Presence", "subtitle": "Questions on Earth's Silent Neighbors", "author": "E. C. Stroud", "asin": "4bAAv3z"},
    8:  {"title": "The Power of Changing Your Mind", "subtitle": "How Intellectual Humility Improves Decisions, Relationships, and Everyday Life", "author": "Evan R. Cole", "asin": "3PieMVj"},
    9:  {"title": "The Shadow Within", "subtitle": "A Practical Guide to Safe, Realistic Shadow Work in Everyday Life", "author": "Elena Maris", "asin": "4d19yHb"},
    10: {"title": "Echoes of Aetheris", "subtitle": "", "author": "Aetheri Codex", "asin": "4rN0KIS"},
    11: {"title": "Disclosure 2026", "subtitle": "18 Rated Scenarios for Alien First Contact", "author": "Marcus Reeve", "asin": "47hGhV8"},
    12: {"title": "Resonance Drift", "subtitle": "A Hopepunk Signal", "author": "R. Zyrion", "asin": "3Pe2EEO"},
    13: {"title": "Symbiont Bloom", "subtitle": "Verdant Nexus #1", "author": "Elowen Tidebloom", "asin": "47W0PTa"},
    14: {"title": "Otomí", "subtitle": "A Historical Narrative of Land, Ritual, and Continuity", "author": "E. J. Marín", "asin": "41jPyIE"},
    15: {"title": "Physics of Insight", "subtitle": "Awakening the Savant Within", "author": "Quantum Chronos", "asin": "B0GRW79ZM7"},
    16: {"title": "The Physics of Time", "subtitle": "A Creative Exploration of Consciousness, Spacetime, and the Nature of Temporal Experience", "author": "Quantum Chronos", "asin": "3NCAWRA"},
    17: {"title": "Consciousness in Higher Dimensional Spacetime", "subtitle": "A Dual-Dimensional Theory of Mind and Body", "author": "Quantum Chronos", "asin": "4siK2lz"},
    18: {"title": "Quantum Soul Echoes", "subtitle": "Consciousness as Particle and Spacetime Imprint", "author": "Quantum Chronos", "asin": "3Pl8NPu"},
    19: {"title": "Microbiology ABC's", "subtitle": "Tiny Cells and Microbes from A to Z", "author": "Michael Bacotti", "asin": "4cZlh9l"},
    20: {"title": "You Tell the Story", "subtitle": "Everyday Adventures", "author": "Ellie Sunwood", "asin": "4smIZAW"},
    21: {"title": "The Burning Song", "subtitle": "", "author": "Rowan Ashcroft", "asin": "4uDlo0F"},
    22: {"title": "Mindful Memory", "subtitle": "Thought Experiments and Memory Mapping to Strengthen Your Brain", "author": "D. E. Harlan", "asin": "4smJrz8"},
    23: {"title": "Shadow Work Journal for Women", "subtitle": "90-Day Guided Prompts to Heal Your Inner Child and Embrace Emotional Freedom", "author": "Luna Sage", "asin": "3NCBFlM"},
    24: {"title": "Rules of Survival", "subtitle": "Fire, Hunger, and the First Name", "author": "Jorak Veldt", "asin": "3NvIPZ6"},
    25: {"title": "Blood Ember", "subtitle": "Chants of the First", "author": "Jorak Veldt", "asin": "4bLjVwK"},
    26: {"title": "The Orchardist: Harvest", "subtitle": "", "author": "Kate E Brennan", "asin": "4rOcr1Z"},
    27: {"title": "Little Mike: Fun at the Beach", "subtitle": "", "author": "Michael Jr", "asin": "40JEYKU"},
    28: {"title": "The Quiet Hours", "subtitle": "", "author": "Elara Moss", "asin": "3NOtEKA"},
    29: {"title": "Little Mike: Learns to Fly", "subtitle": "", "author": "Michael Jr", "asin": "4dzhtvy"},
    30: {"title": "Discovering Washington DC", "subtitle": "A Comprehensive Guide for All Ages", "author": "Evelyn Carter", "asin": "3Pl9LeA"},
    31: {"title": "Echoes of Transcendence", "subtitle": "", "author": "L Everwood", "asin": "4rOlOyl"},
    32: {"title": "American Journeys", "subtitle": "Exploring Language and American Culture", "author": "C. Everett", "asin": "4cUyAb0"},
    33: {"title": "Mythical Menagerie", "subtitle": "A Journey Across Cultures and Creatures", "author": "E. Marlowe", "asin": "47W2rwc"},
    34: {"title": "Little Mike: Builds a Robot", "subtitle": "", "author": "Michael Jr", "asin": "4svSTRa"},
    35: {"title": "Time Investing", "subtitle": "A Self-Help Guide to Valuing Your Own Time", "author": "H Harvey", "asin": "4sSWsAl"},
}

def gh_api(path):
    env = os.environ.copy()
    env["GH_TOKEN"] = TOKEN
    r = subprocess.run(["gh", "api", f"repos/{REPO}/contents/{path}"],
                      capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise Exception(f"API error {r.returncode}: {r.stderr}")
    return json.loads(r.stdout)

def gh_update(path, content, sha, msg):
    encoded = base64.b64encode(content.encode()).decode()
    env = os.environ.copy()
    env["GH_TOKEN"] = TOKEN
    p = subprocess.run(
        ["gh", "api", "-X", "PUT", f"repos/{REPO}/contents/{path}",
         "-f", f"message={msg}", "-f", f"content={encoded}", "-f", f"sha={sha}"],
        capture_output=True, text=True, env=env
    )
    if p.returncode != 0:
        raise Exception(f"PUT error: {p.stderr}")

def build_jsonld(n, title, author):
    asin = TRACKER[n]["asin"]
    obj = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": title,
        "author": {"@type": "Person", "name": author},
        "url": f"https://amzn.to/{asin}",
        "bookEdition": "eBook",
        "bookFormat": "https://schema.org/EBook",
        "publisher": {"@type": "Organization", "name": "Threshold Publishing"}
    }
    return json.dumps(obj, indent=2)

def process_one(n):
    path = f"book/{n}.html"
    info = TRACKER[n]
    
    # Fetch current content
    data = gh_api(path)
    sha = data["sha"]
    content = base64.b64decode(data["content"]).decode("utf-8")
    
    # Extract title from page (use tracker if not found)
    m = re.search(r'<title>([^<]+)</title>', content)
    page_title = m.group(1).strip() if m else info["title"]
    
    # Extract author from page
    m = re.search(r'class="detail-author">([^<]+)</p>', content)
    if m:
        author = m.group(1).strip()
        if author.startswith("by "):
            author = author[3:]
    else:
        author = info["author"]
    
    # Build new title
    new_title = f"{info['title']} by {author} | Bithues Reading Lab"
    
    # Build JSON-LD
    jsonld = build_jsonld(n, info["title"], author)
    script_tag = f'\n<script type="application/ld+json">\n{jsonld}\n</script>\n'
    
    # Check for existing JSON-LD
    has_jsonld = '<script type="application/ld+json"' in content
    
    # Insert before </head>
    new_content = content.replace('</head>', script_tag + '</head>')
    
    # Update title if needed
    if page_title != new_title:
        new_content = re.sub(r'<title>[^<]+</title>', f'<title>{new_title}</title>', new_content)
    
    msg = f"Add Schema.org JSON-LD to book {n}: {info['title']}"
    gh_update(path, new_content, sha, msg)
    
    status = "updated" if not has_jsonld else "replaced existing"
    print(f"Book {n}: {info['title']} - {status}")
    return True, None

def main():
    print(f"Processing 35 book pages...")
    for n in range(1, 36):
        try:
            success, err = process_one(n)
            if not success:
                print(f"Book {n}: ERROR - {err}")
        except Exception as e:
            print(f"Book {n}: EXCEPTION - {e}")

if __name__ == "__main__":
    main()
