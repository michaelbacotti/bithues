#!/usr/bin/env python3
import os
from pathlib import Path
import html as html_module

ROOT = Path(__file__).resolve().parent
TRACKER_PATH = Path("/Users/mike/.openclaw/workspace/References/book-tracker.md")

# Full review data for all 35 books
REVIEWS = {
    1: {
        "title": "The Dawn of Civilization", "author": "T. Stone", "subtitle": "A Story of a Prehistoric Tribe's Struggle for Survival",
        "tldr": "When a brutal winter kills his father, sixteen-year-old Koda watches Uluk take up the leader's staff and hold their small tribe together. As bears, bandits, and a bronze-armed warlord close in, Koda and his friends fight to turn a wandering tribe into a walled village that can survive.",
        "takeaways": ["Survival in harsh prehistoric times required trust, cooperation, and learning when to lean on others", "Leadership isn't about strength—it's about making hard choices for the group's survival", "The line between friend and foe blurs when survival is at stake", "Building something lasting requires breaking old rules and forming new alliances"],
        "who": "Fans of gritty historical adventures, tribal survival stories, and early-civilization settings. Readers who like light romance woven into war, politics, and found family.",
        "verdict": "A grounded, visceral tale of prehistoric survival that feels authentically ancient. The world-building is meticulous and the characters are memorable."
    },
    2: {
        "title": "The Richmond Cipher", "author": "E. Maris", "subtitle": "",
        "tldr": "In Confederate Richmond, 1863, Mary carries secrets in her memory as she moves through the Executive Mansion. Every word she hears becomes intelligence in this tense spy thriller.",
        "takeaways": ["The invisible labor of enslaved people included risking everything for the Union cause", "Intelligence networks often relied on those society refused to notice", "Courage sometimes looks like obedience"],
        "who": "Readers of Kristin Hannah, James McBride, and Anthony Doerr. Fans of Civil War fiction and espionage thrillers.",
        "verdict": "A tense, intimate portrait of espionage behind Confederate lines. The perspective is fresh and the tension never lets up."
    },
    3: {
        "title": "Red Horizon: Lunar Launch", "author": "M. A. Hale", "subtitle": "",
        "tldr": "Commander Marcus Hale must launch the Eos Ark to deliver 250 young colonists to Mars. But UAP hover above the horizon—humanity is raising children under the scrutiny of an unknown intelligence.",
        "takeaways": ["Space colonization requires long-term thinking that most societies struggle to embrace", "The math of survival on another planet is brutal—every person matters", "UAP presence adds an unsettling layer of cosmic oversight"],
        "who": "Fans of realistic Mars and Moon fiction who want competent characters and hopeful space opera.",
        "verdict": "A grounded, hopeful space-colony saga that takes the science seriously."
    },
    4: {
        "title": "The Confluence Doctrine", "author": "Alaric Wynn", "subtitle": "",
        "tldr": "In a world where suffering has been designed out, Orren Myal hears something that doesn't fit—a sense of 'full, but unfinished.' What is life's task within harmony?",
        "takeaways": ["When basic needs are met, humans still seek meaning and purpose", "Contentment and restlessness can coexist", "The greatest questions often have no enemies to fight"],
        "who": "Fans of Ursula K. Le Guin, Becky Chambers, and meditative explorations of consciousness.",
        "verdict": "A quiet, luminous philosophical novel that asks what happens after we've solved all our problems."
    },
    5: {
        "title": "Living with a Moving Planet", "author": "J. T. Hartley", "subtitle": "Deep Time, Human Adaptation, and a Positive Climate Future",
        "tldr": "Drawing on deep-time climate records and archaeology, this book shows how humans have adapted to changing baselines for tens of thousands of years.",
        "takeaways": ["Climate has always changed—human adaptation is the story, not the exception", "Institutions fail but people move, improvise, and rebuild", "Hope requires understanding, not denial or panic"],
        "who": "Anyone tired of doom and denial who wants a grounded, hopeful way to think about climate change.",
        "verdict": "A clear-eyed, non-tribal guide that reframes the climate conversation toward practical adaptation."
    },
    6: {
        "title": "Beyond the Veil", "author": "D. E. Harlan", "subtitle": "Quantum Speculations on Consciousness, Death, and the Universe",
        "tldr": "A careful tour of evidence around what happens when we die, drawing on NDE research, quantum physics, and philosophy.",
        "takeaways": ["Near-death experiences share remarkable similarities across cultures", "The hard problem of consciousness may resist material explanation", "Many-worlds and quantum theories offer intriguing possibilities"],
        "who": "Readers who've stared at the night sky wondering. Anyone asking big questions about death.",
        "verdict": "Neither dogmatic nor dismissive—this is for anyone willing to sit with uncertainty."
    },
    7: {
        "title": "Veiled Presence", "author": "", "subtitle": "",
        "tldr": "A transformative journey of self-discovery as seekers venture into realms where echoes of destiny reverberate.",
        "takeaways": ["Destiny often reveals itself through unexpected paths", "Courage and transformation go hand in hand"],
        "who": "Readers who enjoy transformative journeys exploring consciousness and reality.",
        "verdict": "An engaging exploration of self-discovery with mystical undertones."
    },
    8: {
        "title": "The Power of Changing Your Mind", "author": "Evan R. Cole", "subtitle": "How Intellectual Humility Improves Decisions, Relationships, and Everyday Life",
        "tldr": "In a culture that rewards confidence, this book shows how intellectual humility is actually a competitive edge.",
        "takeaways": ["New facts rarely change minds—understanding why matters more", "The 'update loop' helps turn mistakes into better models", "Changing your mind is maintenance, not confession"],
        "who": "Leaders, investors, and anyone who wants better decisions and fewer pointless fights.",
        "verdict": "Practical, actionable advice for becoming more updateable in a polarized world."
    },
    9: {
        "title": "The Shadow Within", "author": "Elena Maris", "subtitle": "A Practical Guide to Safe, Realistic Shadow Work in Everyday Life",
        "tldr": "Instead of treating reactions as defects, learn to treat them as information—and respond differently in everyday life.",
        "takeaways": ["Shadow work is about integration, not elimination", "The Observe → Explore → Integrate method provides a safe framework", "Grounding and safety matter more than dramatic breakthroughs"],
        "who": "People who describe their patterns but struggle to change reactions. Jungian psychology fans.",
        "verdict": "A trauma-informed, practical approach to shadow work that respects your nervous system."
    },
    10: {
        "title": "Echoes of Aetheris", "author": "Aetheri Codex", "subtitle": "",
        "tldr": "Nine thousand years before history, a wounded alien ship falls onto a frozen steppe. The first hybrid is born.",
        "takeaways": ["Ancient aliens done seriously—not campy, but plausibly speculative", "The origin of human traits may have extraterrestrial roots", "Hybridization could explain sudden leaps in human capability"],
        "who": "Readers who enjoy ancient aliens without the camp, evolutionary what-ifs.",
        "verdict": "An atmospheric, grounded take on ancient astronaut theory."
    },
    11: {
        "title": "Disclosure 2026", "author": "Marcus Reeve", "subtitle": "18 Rated Scenarios for Alien First Contact",
        "tldr": "From viral smartphone footage to White House landings, this book analyzes 18 pathways to alien disclosure—each rated for plausibility based on decades of testimony.",
        "takeaways": ["Disclosure isn't a single event—it's a spectrum of possibilities", "Government secrecy has legitimate national security dimensions", "The Drake equation suggests we're likely not alone"],
        "who": "UFO disclosure enthusiasts, preppers, and anyone asking 'what if?'",
        "verdict": "A thorough, balanced analysis of one of humanity's most profound potential pivots."
    },
    12: {
        "title": "Resonance Drift", "author": "R. Zyrion", "subtitle": "A Hopepunk Signal",
        "tldr": "In Eden Prime's biolum spires, harmony hums—until a family detects a pulse that defies the weave.",
        "takeaways": ["Hopepunk is about building better worlds, not just hoping for them", "Stewardship of place creates deep belonging", "Cozy settings can hold profound themes"],
        "who": "Fans of Becky Chambers and Martha Wells—serene sci-fi where community matters.",
        "verdict": "A comforting hug of a novella that proves optimism is a valid literary stance."
    },
    13: {
        "title": "Symbiont Bloom", "author": "Elowen Tidebloom", "subtitle": "Verdant Nexus #1",
        "tldr": "On volcanic isles of Lumengrove, dawn arrives through living leaf-glass. When the island's pulse skips, a family must unravel a systems puzzle.",
        "takeaways": ["Eco-worldbuilding shows how organisms and environments co-create reality", "Paying attention to patterns reveals deeper truths", "No villains—only Paradise nudging caretakers to pay attention"],
        "who": "Readers who love eco-worldbuilding and stories where people do the right thing.",
        "verdict": "A lush, thoughtful start to a series that treats ecology as spiritual practice."
    },
    14: {
        "title": "Otomí", "author": "E. J. Marín", "subtitle": "A Historical Narrative of Land, Ritual, and Continuity",
        "tldr": "Through the eyes of a young ritual apprentice, follow one drought-stricken year in an Otomí village.",
        "takeaways": ["Indigenous knowledge holds ecological wisdom accumulated over millennia", "Ritual connects communities to land and each other", "Historical fiction can recover erased perspectives"],
        "who": "Bernard Cornwell fans and lovers of indigenous historical fiction.",
        "verdict": "A respectful, immersive reconstruction of ancient life."
    },
    15: {
        "title": "Physics of Insight", "author": "Quantum Chronos", "subtitle": "Awakening the Savant Within",
        "tldr": "What if genius isn't rare—it's hidden inside every mind, waiting for the right switch?",
        "takeaways": ["Savant skills exist on a spectrum in everyone", "The 'savant switch' can be triggered by various conditions", "Understanding cognitive limits expands what we attempt"],
        "who": "Readers who loved The Physics of Time and want more on consciousness.",
        "verdict": "A disciplined exploration of mind's untapped architecture."
    },
    16: {
        "title": "The Physics of Time", "author": "Quantum Chronos", "subtitle": "A Creative Exploration of Consciousness, Spacetime, and the Nature of Temporal Experience",
        "tldr": "A groundbreaking exploration: what if the universe is a block of spacetime containing all moments, yet consciousness navigates through it?",
        "takeaways": ["Block universe theory suggests past, present, and future coexist", "Consciousness may 'actualize' possibilities into experience", "Time flow may be an illusion—yet experience is real"],
        "who": "Physicists, philosophers, and curious minds willing to think radically.",
        "verdict": "A mind-expanding tour de force that leaves you rethinking reality."
    },
    17: {
        "title": "Consciousness in Higher Dimensional Spacetime", "author": "Quantum Chronos", "subtitle": "A Dual-Dimensional Theory of Mind and Body",
        "tldr": "What if consciousness doesn't exist in the same spacetime as the body? A radical extension of Einstein's relativity into the domain of mind.",
        "takeaways": ["Consciousness may exist in a different dimensional space than physical matter", "The hard problem may require new mathematics to solve", "Awareness could be non-local in ways physics is only beginning to explore"],
        "who": "Anyone fascinated by consciousness foundations and physics meets neuroscience.",
        "verdict": "Speculative but rigorous—an intellectual adventure."
    },
    18: {
        "title": "Quantum Soul Echoes", "author": "Quantum Chronos", "subtitle": "Consciousness as Particle and Spacetime Imprint",
        "tldr": "What if consciousness is what spacetime remembers? Two models synthesized in this rigorous exploration.",
        "takeaways": ["Consciousness may leave traces in spacetime itself", "Quantum coherence could persist beyond biological death", "The 'soul' concept gains unexpected scientific footing"],
        "who": "Readers of Penrose and Hameroff—those who demand rigor and wonder.",
        "verdict": "A synthesis that bridges physics, philosophy, and spirituality."
    },
    19: {
        "title": "Microbiology ABC's", "author": "Michael Bacotti", "subtitle": "Tiny Cells and Microbes from A to Z",
        "tldr": "From amoebas to zooplankton, each letter highlights a microbe or cell structure with colorful illustrations.",
        "takeaways": ["The microbial world is more diverse than all other life combined", "Our immune cells are specialized warriors defending us daily", "Microbes are partners, not just pathogens"],
        "who": "Curious kids who ask about germs. Parents seeking screen-free STEM learning.",
        "verdict": "A colorful, accessible introduction to the invisible world."
    },
    20: {
        "title": "You Tell the Story", "author": "Ellie Sunwood", "subtitle": "Everyday Adventures",
        "tldr": "A draw-and-write storybook where children look at pictures, then write and draw their own stories.",
        "takeaways": ["Creative writing builds confidence and communication skills", "Open-ended prompts encourage imagination", "Screen-free activities develop focus and creativity"],
        "who": "Children 4-8 and parents looking for creative, screen-free activities.",
        "verdict": "A blank canvas for young imaginations to fill."
    },
    21: {
        "title": "The Burning Song", "author": "Rowan Ashcroft", "subtitle": "",
        "tldr": "When a cave lion marks Aken, the leader makes a choice that breaks every rule: he sends scouts to the coastal strangers.",
        "takeaways": ["Trust between tribes required enormous vulnerability", "Leadership sometimes means breaking tradition to save your people", "The courage to reach out defines human progress"],
        "who": "Readers who love character-driven stories and authentic historical fiction.",
        "verdict": "A powerful story about the moment one people decided to trust another."
    },
    22: {
        "title": "Mindful Memory", "author": "D. E. Harlan", "subtitle": "Thought Experiments and Memory Mapping to Strengthen Your Brain",
        "tldr": "Empowering retirees with science-backed exercises like memory palaces and timeline mapping.",
        "takeaways": ["Memory palaces have 2,500 years of evidence behind them", "Neuroplasticity means brains can change at any age", "Active recall beats passive review for retention"],
        "who": "Retirees seeking to sharpen cognition. Anyone building emotional resilience.",
        "verdict": "Practical tools backed by neuroscience, accessible to anyone."
    },
    23: {
        "title": "Shadow Work Journal for Women", "author": "Luna Sage", "subtitle": "90-Day Guided Prompts to Heal Your Inner Child and Embrace Emotional Freedom",
        "tldr": "A beginner-friendly 90-day journal with warm prompts for emotional healing.",
        "takeaways": ["Inner child work helps reparent your younger self", "Awareness is the first step—action completes the journey", "Journaling creates a record of growth over time"],
        "who": "Women 25-45 feeling stuck in anxiety or people-pleasing.",
        "verdict": "A gentle, structured path to emotional freedom."
    },
    24: {
        "title": "Rules of Survival", "author": "Jorak Veldt", "subtitle": "Fire, Hunger, and the First Name",
        "tldr": "Roughly one million years ago, a boy learns the band's rules—water order, ember law, watch—and pays for them in skin.",
        "takeaways": ["Survival rules are learned through pain and repetition", "Early humans lived with constant danger but strong community", "The gap between childhood and adulthood was terrifyingly short"],
        "who": "Fans of deep-time settings and anthropologically grounded survival fiction.",
        "verdict": "A visceral, unflinching look at prehistoric childhood."
    },
    25: {
        "title": "Blood Ember", "author": "Jorak Veldt", "subtitle": "Chants of the First",
        "tldr": "Three parts trace how survival habits harden into protocol, law, and chant. From fire to spear to echo.",
        "takeaways": ["Ritual may have evolved from survival necessity", "Chants served practical purposes before artistic ones", "Culture is technology made social"],
        "who": "Readers who like deep-time settings and stories of how culture forms.",
        "verdict": "A thought-provoking exploration of civilization's roots."
    },
    26: {
        "title": "The Orchardist: Harvest", "author": "Kate E Brennan", "subtitle": "",
        "tldr": "Diane Kessler falls from a ladder—in that moment, she doesn't come back. A story of near-death experience.",
        "takeaways": ["Near-death experiences often transform how people see life", "The boundary between this world and 'after' may be thinner than we think", "Coming back changes you irreversibly"],
        "who": "Readers who enjoy literary fiction with spiritual themes.",
        "verdict": "A tender, haunting exploration of what lies beyond."
    },
    27: {
        "title": "Little Mike: Fun at the Beach", "author": "Michael Jr", "subtitle": "",
        "tldr": "Join Little Mike and his friends as they build an awe-inspiring sand castle.",
        "takeaways": ["Teamwork makes dreams bigger", "Creativity thrives in play", "Every child can be a hero"],
        "who": "Children 3-8 and parents who enjoy wholesome illustrated books.",
        "verdict": "A cheerful, positive story about friendship and creativity."
    },
    28: {
        "title": "The Quiet Hours", "author": "Elara Moss", "subtitle": "",
        "tldr": "Gentle bedtime stories celebrating simple joys—perfect for children seeking comfort.",
        "takeaways": ["Peaceful endings help children process the day", "Simple pleasures are worth celebrating", "Bedtime can be a sacred ritual"],
        "who": "Children needing comfort and adults who need peaceful escape.",
        "verdict": "A calming collection that lulls and comforts."
    },
    29: {
        "title": "Little Mike: Learns to Fly", "author": "Michael Jr", "subtitle": "",
        "tldr": "Little Mike dreams of flying. With friends John and May, he meets Pilot Thomas who teaches the wonders of airplanes.",
        "takeaways": ["Dreams are worth pursuing", "Mentors appear in unexpected places", "Courage means trying even when it's scary"],
        "who": "Children 3-8 fascinated by planes. Parents wanting positive values.",
        "verdict": "An inspiring story about following your dreams."
    },
    30: {
        "title": "Discovering Washington DC", "author": "Evelyn Carter", "subtitle": "A Comprehensive Guide for All Ages",
        "tldr": "Beyond the monuments—a guide to the real DC. Stroll Georgetown's cobblestones, tap your feet to jazz, taste a half-smoke.",
        "takeaways": ["DC is more than museums and monuments", "Neighborhoods have distinct personalities", "Local favorites reveal a city's soul"],
        "who": "Tourists, history hounds, and anyone planning a DC visit.",
        "verdict": "The insider's guide to Washington that official tourism misses."
    },
    31: {
        "title": "Echoes of Transcendence", "author": "L Everwood", "subtitle": "",
        "tldr": "Where boundaries of reality blur, seekers embark on a transformative journey. Guided by ancient prophecies, they unveil mysteries.",
        "takeaways": ["Transformation requires stepping into the unknown", "Ancient wisdom may hold keys to modern awakening", "The journey inward is as real as any external adventure"],
        "who": "Readers who enjoy transformative fiction and self-discovery.",
        "verdict": "A mystical journey through realms of possibility."
    },
    32: {
        "title": "American Journeys", "author": "C. Everett", "subtitle": "Exploring Language and American Culture",
        "tldr": "For those moving to or visiting the US—or anyone eager to enhance English through immersive content.",
        "takeaways": ["Language and culture are inseparable", "Immersion accelerates learning", "American diversity is its greatest strength"],
        "who": "ESL learners, immigrants, and anyone curious about American culture.",
        "verdict": "A cultural companion for the American journey."
    },
    33: {
        "title": "Mythical Menagerie", "author": "E. Marlowe", "subtitle": "A Journey Across Cultures and Creatures",
        "tldr": "A thrilling journey through cultures exploring mythical creatures. Discover how dragons and shape-shifters shaped cultural identities.",
        "takeaways": ["Every culture creates creatures that reflect its values", "Myths encode collective wisdom", "The same creature means different things across cultures"],
        "who": "Mythology enthusiasts and readers who enjoy cultural explorations.",
        "verdict": "A fascinating tour of humanity's imaginary bestiary."
    },
    34: {
        "title": "Little Mike: Builds a Robot", "author": "Michael Jr", "subtitle": "",
        "tldr": "Little Mike, John, and May build robots—but they keep falling apart. Through teamwork, they create a robot that tells stories.",
        "takeaways": ["Failure is part of invention", "Teamwork beats individual genius", "Persistence pays off"],
        "who": "Children 3-8 and families who enjoy teamwork stories.",
        "verdict": "A fun, empowering story about never giving up."
    },
    35: {
        "title": "Time Investing", "author": "H Harvey", "subtitle": "A Self-Help Guide to Valuing Your Own Time",
        "tldr": "A self-help guide showing how to prioritize yourself and your time. Strategies for investing in yourself.",
        "takeaways": ["Time is your most precious resource—spend it intentionally", "Saying no to others is saying yes to yourself", "Self-investment compounds over time"],
        "who": "Anyone feeling time-slippage and wanting to prioritize what matters.",
        "verdict": "Practical wisdom for reclaiming your most valuable asset."
    },
}

def parse_tracker():
    with open(TRACKER_PATH) as f:
        lines = [l.rstrip() for l in f]
    books = []
    in_table = False
    for line in lines:
        if line.startswith("| #"):
            in_table = True
            continue
        if in_table and line.startswith("|"):
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) >= 5 and cols[0].isdigit():
                books.append({"id": int(cols[0]), "title": cols[1], "author": cols[3], "link": cols[4]})
    return books

def generate_homepage():
    books = parse_tracker()
    cards = ""
    for b in books[:6]:
        r = REVIEWS.get(b["id"], {"tldr": "A curated title from Bithues Reading Lab.", "author": b["author"]})
        cards += f'''<div class="review-card">
            <h3><a href="reviews/{b['id']}.html">{html_module.escape(b['title'])}</a></h3>
            <p class="author">by {html_module.escape(r.get('author', b['author']) or 'Bithues')}</p>
            <p class="tldr">{r['tldr'][:150]}...</p>
        </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bithues Reading Lab | Curated Book Reviews</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ --bg: #0a0a0f; --surface: #12121a; --border: #2a2a3a; --text: #e8e8f0; --text-dim: #7a7a90; --accent: #7c3aed; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; min-height: 100vh; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 0 1.5rem; }}
        header {{ padding: 2rem 0; border-bottom: 1px solid var(--border); }}
        nav {{ display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; }}
        .logo {{ font-size: 1.5rem; font-weight: 700; color: var(--text); text-decoration: none; }}
        .logo span {{ color: var(--accent); }}
        .nav-links a {{ color: var(--text-dim); text-decoration: none; font-size: 0.9rem; margin-left: 1.5rem; }}
        .nav-links a:hover, .nav-links a.active {{ color: var(--text); }}
        .hero {{ padding: 3rem 0; text-align: center; }}
        .hero h1 {{ font-size: 2.5rem; margin-bottom: 1rem; }}
        .hero p {{ color: var(--text-dim); font-size: 1.1rem; max-width: 500px; margin: 0 auto 2rem; }}
        .featured {{ padding: 2rem 0; }}
        .featured h2 {{ font-size: 1.25rem; margin-bottom: 1.5rem; }}
        .review-card {{ padding: 1.5rem; background: var(--surface); border-radius: 8px; border: 1px solid var(--border); margin-bottom: 1rem; }}
        .review-card h3 {{ font-size: 1.25rem; margin-bottom: 0.5rem; }}
        .review-card h3 a {{ color: var(--text); text-decoration: none; }}
        .review-card h3 a:hover {{ color: var(--accent); }}
        .review-card .author {{ color: var(--text-dim); font-size: 0.9rem; margin-bottom: 0.75rem; }}
        .review-card .tldr {{ color: var(--text-dim); font-size: 0.95rem; }}
        .all-reviews {{ text-align: center; padding: 2rem 0; }}
        .all-reviews a {{ display: inline-block; padding: 0.75rem 1.5rem; background: var(--accent); color: white; text-decoration: none; border-radius: 6px; }}
        footer {{ padding: 2rem 0; text-align: center; border-top: 1px solid var(--border); }}
        footer p {{ color: var(--text-dim); font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <nav>
                <a href="index.html" class="logo">Bithues<span> Reading Lab</span></a>
                <div class="nav-links">
                    <a href="index.html" class="active">Home</a>
                    <a href="reviews/index.html">Reviews</a>
                    <a href="catalog.html">Catalog</a>
                    <a href="articles.html">Articles</a>
                </div>
            </nav>
        </header>
        <section class="hero">
            <h1>Curated book reviews that change how you think</h1>
            <p>Bithues Reading Lab is a curated book review hub for indie authors, solopreneurs, and anyone who wants signal-dense reading.</p>
        </section>
        <section class="featured">
            <h2>Featured Reviews</h2>
            {cards}
        </section>
        <section class="all-reviews">
            <a href="reviews/index.html">View all {len(books)} reviews →</a>
        </section>
        <footer>
            <p>© <span id="year"></span> Bithues Reading Lab</p>
        </footer>
    </div>
    <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>'''
    (ROOT / "index.html").write_text(html)

def generate_review(book_id, book_info):
    r = REVIEWS.get(book_id, {"title": book_info["title"], "author": book_info["author"], "tldr": "A curated title from Bithues Reading Lab.", "takeaways": [], "who": "Readers interested in this genre.", "verdict": "A thought-provoking read."})
    
    title = r.get("title", book_info["title"])
    author = r.get("author", book_info["author"])
    tldr = r.get("tldr", "")
    takeaways = r.get("takeaways", [])
    who = r.get("who", "")
    verdict = r.get("verdict", "")
    link = book_info["link"].strip()
    
    takeaways_html = "".join(f"<li>{html_module.escape(t)}</li>" for t in takeaways)
    
    if link:
        affiliate = f'<div class="affiliate"><p>As an Amazon Associate, we earn from qualifying purchases.</p><a href="{html_module.escape(link)}" target="_blank" rel="noopener">Buy on Amazon</a></div>'
    else:
        affiliate = ""
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_module.escape(title)} – {html_module.escape(author)} | Bithues Reading Lab</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ bg: #0a0a0f; surface: #12121a; border: #2a2a3a; text: #e8e8f0; text-dim: #7a7a90; accent: #7c3aed; accent-dim: #5b21b6; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #0a0a0f; color: #e8e8f0; line-height: 1.7; min-height: 100vh; }}
        .container {{ max-width: 700px; margin: 0 auto; padding: 0 1.5rem; }}
        header {{ padding: 2rem 0; border-bottom: 1px solid #2a2a3a; }}
        nav {{ display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; }}
        .logo {{ font-size: 1.25rem; font-weight: 700; color: #e8e8f0; text-decoration: none; }}
        .logo span {{ color: #7c3aed; }}
        .nav-links a {{ color: #7a7a90; text-decoration: none; font-size: 0.9rem; margin-left: 1.5rem; }}
        .nav-links a:hover {{ color: #e8e8f0; }}
        .review {{ padding: 3rem 0; }}
        .back-link {{ display: inline-block; margin-bottom: 2rem; color: #7c3aed; text-decoration: none; font-size: 0.9rem; }}
        h1 {{ font-size: 1.75rem; margin-bottom: 0.5rem; line-height: 1.3; }}
        .author {{ color: #7a7a90; font-size: 1.1rem; margin-bottom: 1.5rem; }}
        .tldr {{ font-size: 1.15rem; line-height: 1.7; margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid #2a2a3a; }}
        .takeaways h2 {{ font-size: 1.25rem; margin-bottom: 1rem; }}
        .takeaways ul {{ list-style: none; margin-bottom: 2rem; }}
        .takeaways li {{ padding: 0.75rem 0; border-bottom: 1px solid #2a2a3a; }}
        .takeaways li:last-child {{ border-bottom: none; }}
        .who {{ margin-bottom: 2rem; padding: 1.5rem; background: #12121a; border-radius: 8px; border: 1px solid #2a2a3a; }}
        .who strong {{ color: #7c3aed; }}
        .verdict {{ margin-bottom: 2rem; padding: 1.5rem; background: #12121a; border-radius: 8px; border: 1px solid #2a2a3a; }}
        .affiliate {{ padding: 1.5rem; background: #12121a; border-radius: 8px; border: 1px solid #7c3aed; text-align: center; }}
        .affiliate p {{ margin-bottom: 1rem; color: #7a7a90; }}
        .affiliate a {{ display: inline-block; padding: 0.75rem 1.5rem; background: #7c3aed; color: white; text-decoration: none; border-radius: 6px; font-weight: 500; }}
        footer {{ padding: 2rem 0; text-align: center; border-top: 1px solid #2a2a3a; }}
        footer p {{ color: #7a7a90; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <nav>
                <a href="../index.html" class="logo">Bithues<span> Reading Lab</span></a>
                <div class="nav-links">
                    <a href="../index.html">Home</a>
                    <a href="index.html">Reviews</a>
                    <a href="../catalog.html">Catalog</a>
                    <a href="../articles.html">Articles</a>
                </div>
            </nav>
        </header>
        <article class="review">
            <a href="index.html" class="back-link">← Back to Reviews</a>
            <h1>{html_module.escape(title)}</h1>
            <p class="author">by {html_module.escape(author)}</p>
            <p class="tldr">{html_module.escape(tldr)}</p>
            <div class="takeaways">
                <h2>Key Takeaways</h2>
                <ul>{takeaways_html}</ul>
            </div>
            <div class="who">
                <strong>Who would enjoy this:</strong><br>{html_module.escape(who)}
            </div>
            <div class="verdict">
                <strong>Verdict:</strong> {html_module.escape(verdict)}
            </div>
            {affiliate}
        </article>
        <footer>
            <p>© <span id="year"></span> Bithues Reading Lab</p>
        </footer>
    </div>
    <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>'''
    return html

def main():
    books = parse_tracker()
    
    # Generate homepage
    generate_homepage()
    
    # Generate reviews index
    reviews_list = "".join(f'''<div class="review-card">
        <h3><a href="{b['id']}.html">{html_module.escape(b['title'])}</a></h3>
        <p class="author">by {html_module.escape(b['author'] or 'Bithues')}</p>
        <p class="tldr">{html_module.escape(REVIEWS.get(b['id'], {}).get('tldr', 'A curated title from Bithues Reading Lab.')[:150])}...</p>
    </div>''' for b in books)
    
    reviews_index = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Reviews – Bithues Reading Lab</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #0a0a0f; color: #e8e8f0; line-height: 1.7; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 0 1.5rem; }}
        header {{ padding: 2rem 0; border-bottom: 1px solid #2a2a3a; }}
        nav {{ display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; }}
        .logo {{ font-size: 1.5rem; font-weight: 700; color: #e8e8f0; text-decoration: none; }}
        .logo span {{ color: #7c3aed; }}
        .nav-links a {{ color: #7a7a90; text-decoration: none; font-size: 0.9rem; margin-left: 1.5rem; }}
        .nav-links a:hover, .nav-links a.active {{ color: #e8e8f0; }}
        .page-header {{ padding: 3rem 0; }}
        .page-header h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        .page-header p {{ color: #7a7a90; }}
        .review-card {{ padding: 1.5rem; background: #12121a; border-radius: 8px; border: 1px solid #2a2a3a; margin-bottom: 1rem; }}
        .review-card h3 {{ font-size: 1.25rem; margin-bottom: 0.5rem; }}
        .review-card h3 a {{ color: #e8e8f0; text-decoration: none; }}
        .review-card h3 a:hover {{ color: #7c3aed; }}
        .review-card .author {{ color: #7a7a90; font-size: 0.9rem; margin-bottom: 0.75rem; }}
        .review-card .tldr {{ color: #7a7a90; font-size: 0.95rem; }}
        footer {{ padding: 2rem 0; text-align: center; border-top: 1px solid #2a2a3a; }}
        footer p {{ color: #7a7a90; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <nav>
                <a href="../index.html" class="logo">Bithues<span> Reading Lab</span></a>
                <div class="nav-links">
                    <a href="../index.html">Home</a>
                    <a href="index.html" class="active">Reviews</a>
                    <a href="../catalog.html">Catalog</a>
                    <a href="../articles.html">Articles</a>
                </div>
            </nav>
        </header>
        <section class="page-header">
            <h1>All Reviews</h1>
            <p>{len(books)} books reviewed</p>
        </section>
        {reviews_list}
        <footer>
            <p>© <span id="year"></span> Bithues Reading Lab</p>
        </footer>
    </div>
    <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>'''
    
    reviews_dir = ROOT / "reviews"
    reviews_dir.mkdir(exist_ok=True)
    (reviews_dir / "index.html").write_text(reviews_index)
    
    # Generate individual review pages
    for b in books:
        html = generate_review(b["id"], b)
        (reviews_dir / f"{b['id']}.html").write_text(html)
    
    print(f"Generated: index.html, reviews/index.html, {len(books)} review pages")

if __name__ == "__main__":
    main()