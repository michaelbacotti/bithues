#!/usr/bin/env python3
"""Generate SEO content for Bithues category pages + new evergreen pages."""

import os
import re
import html

REPO = "/tmp/bithues-category-hubs"
os.chdir(REPO)

# ─── Helper ─────────────────────────────────────────────────────────────────

def save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {path}")

def amazon_link(title, asin):
    return f'<a href="https://www.amazon.com/dp/{asin}/?tag=bithues-20" rel="nofollow" target="_blank">{title}</a>'

# ─── SEO INTRO TEMPLATES ──────────────────────────────────────────────────────

SEOS = {
    "self-help": """<div class="seo-intro">
<p>Self-help books have a reputation problem — and it's mostly deserved. Too many promise transformation in 21 days, offer vague platitudes wrapped in motivational jargon, and leave you feeling worse than before you started. But the genre's bad apples don't represent the whole harvest. The best self-help books don't just motivate — they give you <strong>frameworks that actually work</strong>. They isolate a specific problem — productivity, anxiety, money mindset, habit formation — and attack it with evidence-backed strategies you can implement today.</p>
<p>What separates a genuinely useful self-help book from a forgettable one often comes down to the author's credibility and the specificity of their advice. James Clear draws on atomic physics metaphors and behavioral science to explain habit loops. Cal Newport dismantled the myth of multitasking and rebuilt productivity around deep work sessions. Morgan Housel made finance feel like psychology rather than accounting. These authors earn your attention because they've done the hard work of translating research into readable, actionable insight.</p>
<p>Whether you're trying to build better routines, manage your money more intelligently, or simply understand yourself a little better, the self-help shelf has something real to offer — if you know where to look. Browse our curated reviews below, or jump to our <a href="best-self-help-books.html">best self-help books guide</a> for deeper analysis.</p>
</div>""",

    "science-fiction": """<div class="seo-intro">
<p>Science fiction has always been the genre that asks "what if?" — and then follows the answer into territory that no other form of storytelling dares to explore. The best sci-fi challenges how you think about technology, society, and human nature itself. It doesn't just predict the future; it makes you examine the present through a stranger's eyes.</p>
<p>From the philosophical depth of Isaac Asimov's <em>Foundation</em> to the hard-science tension of Andy Weir's <em>The Martian</em>, science fiction spans an enormous range. There's cyberpunk exploring the ethics of artificial intelligence, space opera mapping the politics of interstellar empires, near-future thrillers warning us about climate and surveillance, and alternate histories that ask what would happen if the past branched differently. Each subgenre brings its own flavor of wonder and dread.</p>
<p>The genre also consistently outperforms in teaching readers to think in systems — to see how small interactions between technology, culture, and biology can produce outcomes no individual intended. That's not just entertainment; it's cognitive training. Explore our sci-fi reviews below, or see our <a href="best-sci-fi-books.html">best sci-fi books guide</a> for more.</p>
</div>""",

    "fantasy": """<div class="seo-intro">
<p>Great fantasy does more than worldbuild — it uses impossible settings to illuminate real human struggles. A wizard in a crumbling tower is really a story about grief. A magic school is really about belonging and finding your people. A chosen-one prophecy is really about whether destiny is real or whether we make our own meaning. The best fantasy has always known this. It's never really been about the dragons.</p>
<p>The fantasy genre has exploded in range and ambition over the past two decades. Where once Tolkien imitators dominated the shelf, now readers can choose from literary fantasy that reads like poetry, grimdark fantasy that makes Game of Thrones look quaint, cozy fantasy focused on baking and community, and epic multi-volume series that span millennia of invented history. The genre has something for every emotional register.</p>
<p>For readers who want fantasy that respects their intelligence, look no further than authors who use their invented worlds to examine real questions — power, justice, loyalty, identity, what we owe each other. Start with our <a href="best-fantasy-books.html">best fantasy books guide</a>, then dive into our full review collection.</p>
</div>""",

    "nonfiction": """<div class="seo-intro">
<p>Nonfiction is where curiosity goes to be fed. Unlike fiction, which asks you to temporarily suspend your own perspective, nonfiction meets you where you are and takes you somewhere new — but only if you're willing to follow the evidence. The best nonfiction authors are not just knowledgeable; they're teachers who know how to make complex ideas click for readers who aren't specialists.</p>
<p>The genre covers enormous territory: narrative nonfiction that reads like a thriller (think Erik Larson's <em>The Devil in the White City</em>), science writing that rewires how you understand the natural world, memoirs that examine a single life as a lens for universal experience, and business/psychology books that synthesize years of research into actionable frameworks. Knowing what kind of reader you are — what you're trying to get out of the book — makes all the difference between a rewarding experience and a chore.</p>
<p>Our nonfiction reviews focus on books that earn their pages. We prioritize authors who do the hard work of primary research and write with clarity and intellectual honesty. Find your next great nonfiction read in our reviews below, or see our curated list of <a href="best-books-about-money.html">best books about money</a> and <a href="best-biography-books.html">best biographies</a>.</p>
</div>""",

    "thriller": """<div class="seo-intro">
<p>Thriller fiction is the genre that refuses to let you look away. Whether it's a serial killer stalking the Pacific Northwest, a corporate conspiracy reaching into the highest levels of government, or a family secrets埋在地下 thirty years, the thriller's job is to create dread and then deliver on it. The best thrillers do this with craft — tight plotting, unreliable narrators, and the kind of prose that makes you read one more chapter before bed, even though you have to be up in five hours.</p>
<p>The genre has fragmented into rich subgenres. Psychological thrillers focus on the inner life — obsession, manipulation, memory — more than blood. Legal and political thrillers pull you into boardrooms and courtrooms where every sentence is a chess move. Cozy mysteries offer puzzle-solving in a low-stakes village setting. Literary thrillers like Tana French's work treat the genre as a vehicle for examining identity, trauma, and community. Each has its own contract with the reader.</p>
<p>The test of a good thriller isn't just whether it scares you — it's whether, when you finish, you want to go back and re-read knowing what you know now. That rarest of thrillers reveals new layers on re-reading. Find the best thrillers for your next late-night read in our <a href="best-thriller-books.html">best thriller books guide</a>.</p>
</div>""",

    "biography": """<div class="seo-intro">
<p>A biography's job is deceptively simple: tell someone else's life as if it were your own story. But the best biographies make you feel like you're living inside the person you're reading about — feeling their doubts, tasting their victories, understanding why they made the choices that defined them. A great biography is an exercise in empathy that also happens to be educational.</p>
<p>The best biography subjects aren't necessarily the most famous — they're the ones whose lives illuminate something universal. Walter Isaacson's <em>Steve Jobs</em> works not because everyone loves Apple but because Jobs's obsession with perfection and his tortured relationships reveal something true about creativity and power. Tara Westover's <em>Educated</em> isn't just about a girl who escaped a survivalist family — it's about identity, family, and what we owe our past selves.</p>
<p>Good biography reading requires a willingness to be changed. These aren't passive experiences. Browse our full biography reviews below, or see our <a href="best-biography-books.html">best biography books guide</a> for curated recommendations.</p>
</div>""",

    "business": """<div class="seo-intro">
<p>Business books occupy a peculiar shelf — they're written to be consumed quickly, often by people reading on lunch breaks or during commutes, yet the best ones contain frameworks that genuinely change how you think about work, leadership, and strategy. The trick is separating the signal from the noise. Most business books are built around a single good idea stretched into 250 pages. The great ones earn every chapter.</p>
<p>The most useful business books tend to fall into a few categories: strategy (how to think about competition and markets), management (how to build and lead organizations), personal effectiveness (how to make yourself and your team more productive), and finance/money (how to understand the numbers that govern business decisions). The best authors in each category — from Michael Porter on strategy to Morgan Housel on financial behavior — have done the deep research that makes their frameworks stick.</p>
<p>Whether you're building a startup, managing a team, or trying to understand what separates companies that last from those that flame out, there's a business book that has your answer. Find it in our reviews below, or see our <a href="best-books-about-productivity.html">best books about productivity</a> guide.</p>
</div>""",

    "adventure": """<div class="seo-intro">
<p>Adventure fiction is the genre of going — into the unknown, against odds, toward something worth reaching. Whether it's a mountaineer climbing K2, a crew of misfits crossing an ocean in a leaking boat, or a teenager surviving the wilderness after a plane crash, adventure stories are really about what a person is made of when everything familiar falls away. The landscape becomes a mirror.</p>
<p>Great adventure writing has a dual purpose: it delivers visceral, propulsive storytelling while also teaching readers something real about the world — about geography, survival, human endurance, the history of exploration. Jack London wasn't just writing action; he was examining the interplay between civilization and instinct. Ernest Hemingway's characters carried the weight of their own psychological terrain, not just the physical mountains they climbed.</p>
<p>The adventure genre rewards readers who want to feel the fear and triumph vicariously while learning something true about human limits. Explore our full collection below.</p>
</div>""",
}

# ─── BEST-OF SECTIONS ───────────────────────────────────────────────────────

BEST_OF = {
    "self-help": """<div class="best-of">
<h2>🌟 Best Self-Help Books Worth Reading</h2>
<p>These are the self-help titles that have stood the test of time and reader scrutiny. Not every book will resonate with every person — that's the nature of a genre built on personal transformation — but each of these has enough substance to justify the investment.</p>
<ul>
<li><strong>Atomic Habits</strong> — James Clear · <a href="https://www.amazon.com/dp/B07D7W41B1/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The 7 Habits of Highly Effective People</strong> — Stephen R. Covey · <a href="https://www.amazon.com/dp/1982137274/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Thinking, Fast and Slow</strong> — Daniel Kahneman · <a href="https://www.amazon.com/dp/0374533555/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Deep Work</strong> — Cal Newport · <a href="https://www.amazon.com/dp/B00X4W8T76/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Psychology of Money</strong> — Morgan Housel · <a href="https://www.amazon.com/dp/0857197681/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Mindset: The New Psychology of Success</strong> — Carol S. Dweck · <a href="https://www.amazon.com/dp/0345472322/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Power of Habit</strong> — Charles Duhigg · <a href="https://www.amazon.com/dp/081298160X/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Essentialism: The Disciplined Pursuit of Less</strong> — Greg McKeown · <a href="https://www.amazon.com/dp/0804179405/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>How to Win Friends and Influence People</strong> — Dale Carnegie · <a href="https://www.amazon.com/dp/0671027034/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Start with Why</strong> — Simon Sinek · <a href="https://www.amazon.com/dp/0241958229/?tag=bithues-20" rel="nofollow">Amazon</a></li>
</ul>
</div>""",

    "science-fiction": """<div class="best-of">
<h2>🌟 Best Science Fiction Books Worth Reading</h2>
<p>The sci-fi canon runs deep. These titles represent the genre at its most ambitious — books that asked big questions and answered them in ways that changed the landscape of speculative fiction. Some are decades old but read like they were written last week.</p>
<ul>
<li><strong>Project Hail Mary</strong> — Andy Weir · <a href="https://www.amazon.com/dp/0593135202/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Martian</strong> — Andy Weir · <a href="https://www.amazon.com/dp/0553418025/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Dune</strong> — Frank Herbert · <a href="https://www.amazon.com/dp/0441172717/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Foundation</strong> — Isaac Asimov · <a href="https://www.amazon.com/dp/0553293354/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Hyperion</strong> — Dan Simmons · <a href="https://www.amazon.com/dp/0553283685/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Left Hand of Darkness</strong> — Ursula K. Le Guin · <a href="https://www.amazon.com/dp/0441478125/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Neuromancer</strong> — William Gibson · <a href="https://www.amazon.com/dp/0441569595/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Snow Crash</strong> — Neal Stephenson · <a href="https://www.amazon.com/dp/0553380958/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Three-Body Problem</strong> — Cixin Liu · <a href="https://www.amazon.com/dp/0765382032/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Artemis</strong> — Andy Weir · <a href="https://www.amazon.com/dp/1473644178/?tag=bithues-20" rel="nofollow">Amazon</a></li>
</ul>
</div>""",

    "fantasy": """<div class="best-of">
<h2>🌟 Best Fantasy Books Worth Reading</h2>
<p>Fantasy has never been more diverse or more ambitious. These titles represent the genre's best — books that worldbuild with purpose, characters that feel like they could walk off the page, and stories that ask what magic would actually cost us.</p>
<ul>
<li><strong>The Name of the Wind</strong> — Patrick Rothfuss · <a href="https://www.amazon.com/dp/0756404746/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Way of Kings</strong> — Brandon Sanderson · <a href="https://www.amazon.com/dp/0765365278/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Lies of Locke Lamora</strong> — Scott Lynch · <a href="https://www.amazon.com/dp/0553419021/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The First Law Trilogy</strong> — Joe Abercrombie · <a href="https://www.amazon.com/dp/0316387343/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Lord of the Rings</strong> — J.R.R. Tolkien · <a href="https://www.amazon.com/dp/0544003411/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>A Game of Thrones</strong> — George R.R. Martin · <a href="https://www.amazon.com/dp/0553593543/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Poppy War</strong> — R.F. Kuang · <a href="https://www.amazon.com/dp/0062662577/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Fifth Season</strong> — N.K. Jemisin · <a href="https://www.amazon.com/dp/0316229296/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Hobbit</strong> — J.R.R. Tolkien · <a href="https://www.amazon.com/dp/054792822X/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Circe</strong> — Madeline Miller · <a href="https://www.amazon.com/dp/0062561022/?tag=bithues-20" rel="nofollow">Amazon</a></li>
</ul>
</div>""",

    "nonfiction": """<div class="best-of">
<h2>🌟 Best Nonfiction Books Worth Reading</h2>
<p>Nonfiction lives or dies on the quality of its research and the honesty of its author. These books represent the best of the genre — narrative-driven, meticulously researched, and written with the reader's time as precious.</p>
<ul>
<li><strong>The Psychology of Money</strong> — Morgan Housel · <a href="https://www.amazon.com/dp/0857197681/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Thinking, Fast and Slow</strong> — Daniel Kahneman · <a href="https://www.amazon.com/dp/0814533555/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Sapiens: A Brief History of Humankind</strong> — Yuval Noah Harari · <a href="https://www.amazon.com/dp/0062316097/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Educated</strong> — Tara Westover · <a href="https://www.amazon.com/dp/0399590501/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Gene: An Intimate History</strong> — Siddhartha Mukherjee · <a href="https://www.amazon.com/dp/147673350X/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Outliers</strong> — Malcolm Gladwell · <a href="https://www.amazon.com/dp/0316017930/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Power of Habit</strong> — Charles Duhigg · <a href="https://www.amazon.com/dp/081298160X/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Immortal Life of Henrietta Lacks</strong> — Rebecca Skloot · <a href="https://www.amazon.com/dp/1400052181/?tag=bithues-20" rel="nofollow">Amazon</a></li>
</ul>
</div>""",

    "thriller": """<div class="best-of">
<h2>🌟 Best Thriller Books Worth Reading</h2>
<p>Thriller fiction demands that you keep turning pages. These titles deliver — with plotting that's tight enough to strangle, characters complex enough to haunt you, and endings you genuinely won't see coming. Some are disturbing. All are compelling.</p>
<ul>
<li><strong>Gone Girl</strong> — Gillian Flynn · <a href="https://www.amazon.com/dp/0307588378/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Silent Patient</strong> — Alex Michaelides · <a href="https://www.amazon.com/dp/1250303046/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Girl with the Dragon Tattoo</strong> — Stieg Larsson · <a href="https://www.amazon.com/dp/0307455166/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Behind Closed Doors</strong> — B.A. Paris · <a href="https://www.amazon.com/dp/1250122734/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Woman in the Window</strong> — A.J. Finn · <a href="https://www.amazon.com/dp/0062678118/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Sharp Objects</strong> — Gillian Flynn · <a href="https://www.amazon.com/dp/0307345770/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>In the Woods</strong> — Tana French · <a href="https://www.amazon.com/dp/0143035985/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Hunt</strong> — Ragnar Jónasson · <a href="https://www.amazon.com/dp/1912374167/?tag=bithues-20" rel="nofollow">Amazon</a></li>
</ul>
</div>""",

    "biography": """<div class="best-of">
<h2>🌟 Best Biography Books Worth Reading</h2>
<p>A great biography makes you understand not just what someone did, but why it mattered — and what it cost them. These are the memoirs and biographies that have earned their place on the shelf, written by authors who did the difficult work of earning their subjects' trust.</p>
<ul>
<li><strong>Steve Jobs</strong> — Walter Isaacson · <a href="https://www.amazon.com/dp/1451648537/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Elon Musk</strong> — Walter Isaacson · <a href="https://www.amazon.com/dp/0063282195/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Becoming</strong> — Michelle Obama · <a href="https://www.amazon.com/dp/1524763138/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Educated</strong> — Tara Westover · <a href="https://www.amazon.com/dp/0399590501/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Born a Crime</strong> — Trevor Noah · <a href="https://www.amazon.com/dp/0399588175/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Bad Blood: Secrets and Lies in a Silicon Valley Startup</strong> — John Carreyrou · <a href="https://www.amazon.com/dp/0527766634/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Shoe Dog</strong> — Phil Knight · <a://www.amazon.com/dp/1476716216/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Open</strong> — Andre Agassi · <a href="https://www.amazon.com/dp/0300759478/?tag=bithues-20" rel="nofollow">Amazon</a></li>
</ul>
</div>""",

    "business": """<div class="best-of">
<h2>🌟 Best Business Books Worth Reading</h2>
<p>The business book shelf is crowded with thin volumes repackaging one idea. These are the ones that actually contain enough substance to justify reading all the way through — books that have shaped how leaders think about competition, strategy, and organizational design.</p>
<ul>
<li><strong>Good to Great</strong> — Jim Collins · <a href="https://www.amazon.com/dp/0066620992/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Innovator's Dilemma</strong> — Clayton Christensen · <a href="https://www.amazon.com/dp/0875845851/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Hard Thing About Hard Things</strong> — Ben Horowitz · <a href="https://www.amazon.com/dp/0062273205/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Shoe Dog</strong> — Phil Knight · <a href="https://www.amazon.com/dp/1476716216/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Psychology of Money</strong> — Morgan Housel · <a href="https://www.amazon.com/dp/0857197681/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Zero to One</strong> — Peter Thiel · <a href="https://www.amazon.com/dp/0804139296/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Lean Startup</strong> — Eric Ries · <a href="https://www.amazon.com/dp/0307887898/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Goodreads Choice Awards Business Book of 2019</strong> — Atomic Habits summary</li>
</ul>
</div>""",

    "adventure": """<div class="best-of">
<h2>🌟 Best Adventure Books Worth Reading</h2>
<p>Adventure fiction tests people against the world's most unforgiving conditions — mountains, oceans, deserts, ice — and the best adventure stories reveal character in the process. These books have defined the genre for generations of readers.</p>
<ul>
<li><strong>The Call of the Wild</strong> — Jack London · <a href="https://www.amazon.com/dp/0451527314/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Into the Wild</strong> — Jon Krakauer · <a href="https://www.amazon.com/dp/0447483881/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Touching the Void</strong> — Joe Simpson · <a href="https://www.amazon.com/dp/0385721876/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>The Old Man and the Sea</strong> — Ernest Hemingway · <a href="https://www.amazon.com/dp/0684801223/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Moby Dick</strong> — Herman Melville · <a href="https://www.amazon.com/dp/0142437247/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Life of Pi</strong> — Yann Martel · <a href="https://www.amazon.com/dp/0770437365/?tag=bithues-20" rel="nofollow">Amazon</a></li>
<li><strong>Shackleton's Way</strong> — Margot Morrell · <a href="https://www.amazon.com/dp/0140264438/?tag=bithues-20" rel="nofollow">Amazon</a></li>
</ul>
</div>""",
}

# ─── CATEGORY PAGE UPGRADE ───────────────────────────────────────────────────

CATEGORY_MAP = {
    "self-help":       ("Self-Help",    "Self-help",    "self-help.html",   "💡 Self-Help"),
    "science-fiction": ("Science Fiction", "Sci-Fi",  "science-fiction.html", "🚀 Science Fiction"),
    "fantasy":         ("Fantasy",      "Fantasy",      "fantasy.html",     "🌟 Fantasy"),
    "nonfiction":      ("Nonfiction",   "Nonfiction",   "nonfiction.html",   "📖 Nonfiction"),
    "thriller":        ("Thriller",     "Thriller",     "thriller.html",    "🎯 Thriller"),
    "biography":       ("Biography",    "Biography",    "biography.html",   "👤 Biography"),
    "business":        ("Business",     "Business",     "business.html",    "📈 Business"),
    "adventure":       ("Adventure",    "Adventure",    "adventure.html",   "🌍 Adventure"),
}

def upgrade_category(slug, info):
    category_name, genre_label, filename, section_title = info
    path = os.path.join(REPO, "category", filename)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Remove existing seo-intro and best-of blocks if already present (avoid dupes)
    content = re.sub(r'<div class="seo-intro">.*?</div>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="best-of">.*?</div>\s*', '', content, flags=re.DOTALL)

    seo = SEOS.get(slug, "")
    best = BEST_OF.get(slug, "")

    # Find insertion point: after chips div, before first book section/grid
    # Pattern: </div> (closing chips) followed by whitespace then <section or <div class="book-grid"
    chip_close = re.search(r'</div>\s*<!-- ── BOOK', content)
    book_grid = re.search(r'<section class="book-grid">', content)
    section_alt = re.search(r'<section class="section section-alt">', content)

    # Determine earliest insertion point
    candidates = []
    if chip_close:
        candidates.append(chip_close.end())
    if book_grid:
        candidates.append(book_grid.start())
    if section_alt:
        candidates.append(section_alt.start())

    if not candidates:
        print(f"  ✗ Could not find insertion point in {filename}")
        return

    insert_at = min(candidates)
    insert_content = seo + "\n\n" + best + "\n\n"

    new_content = content[:insert_at] + insert_content + content[insert_at:]
    save(path, new_content)
    print(f"  ✓ Upgraded {filename}")


print("\n=== TASK 1: Upgrading Category Pages ===")
for slug in CATEGORY_MAP:
    upgrade_category(slug, CATEGORY_MAP[slug])

# ─── PAGE TEMPLATE FOR NEW PAGES ─────────────────────────────────────────────

def page_template(title, h1, description, canonical, breadcrumb, hero_label, content_html, schema=None):
    last_updated = "April 2026"
    schema_block = f'\n<script type="application/ld+json">{schema}</script>' if schema else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="google-adsense-account" content="ca-pub-9312870448453345" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/main.css">
  <link rel="canonical" href="https://www.bithues.com/{canonical}"></head>
<body>
  <nav>
    <a href="index.html" class="nav-brand">Bithues <span>Reading Lab</span></a>
    <div class="nav-links">
      <div class="nav-item"><a href="index.html">Home</a></div>
      <div class="nav-item">
        <a href="catalog.html">Reviews ▾</a>
        <div class="dropdown">
          <a href="catalog.html">All Reviews</a>
          <a href="book-tracker.html">Book Tracker</a>
          <a href="category/self-help.html">Self-Help</a>
          <a href="category/science-fiction.html">Sci-Fi</a>
          <a href="category/fantasy.html">Fantasy</a>
          <a href="category/nonfiction.html">Nonfiction</a>
          <a href="category/thriller.html">Thriller</a>
          <a href="category/biography.html">Biography</a>
          <a href="category/business.html">Business</a>
        </div>
      </div>
      <div class="nav-item">
        <a href="stories.html">Stories ▾</a>
        <div class="dropdown">
          <a href="stories.html">All Stories</a>
        </div>
      </div>
      <div class="nav-item">
        <a href="articles.html">Articles ▾</a>
        <div class="dropdown">
          <a href="articles.html">All Articles</a>
          <a href="articles/dna-ancestry-historical-fiction.html">DNA &amp; Historical Fiction</a>
        </div>
      </div>
      <div class="nav-item"><a href="about.html">About</a></div>
      <div class="nav-item"><a href="contact.html">Contact</a></div>
    </div>
  </nav>

  <section class="hero">
    <div class="hero-eyebrow">Bithues Reading Lab — {hero_label}</div>
    <h1>{h1}</h1>
    <p>Last updated: {last_updated}</p>
  </section>

  <div class="breadcrumb">
    <a href="index.html">Home</a> › <a href="catalog.html">Books</a> › <a href="{breadcrumb}">{hero_label}</a>
  </div>

  <main class="article-content">
{content_html}
  </main>

  <footer>
    <div class="brand">Bithues <span>Reading Lab</span></div>
    <p>© <span id="year"></span> Bithues Reading Lab · <a href="press.html">Press</a> · <a href="contact.html">Contact</a> · <a href="privacy.html">Privacy</a></p>
  </footer>

  <button class="back-to-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>

  <script>
    window.onscroll = function() {{
      document.querySelector('.back-to-top').classList.toggle('visible', window.scrollY > 300);
    }};
    document.getElementById('year').textContent = new Date().getFullYear();
  </script>
{schema_block}
</body>
</html>'''


def key_takeaway_box(text):
    return f'''<div class="key-takeaway">
<h3>💡 Key Takeaway</h3>
<p>{text}</p>
</div>'''


def related_links_section(links):
    html = '<div class="related-links"><h3>Related Guides</h3><ul>'
    for text, href in links:
        html += f'<li><a href="{href}">{text}</a></li>'
    html += '</ul></div>'
    return html


# ─── TASK 2: 10 BEST-BOOKS PAGES ─────────────────────────────────────────────

print("\n=== TASK 2: Creating 10 Best-Books Pages ===")

# 1. best-books-about-productivity.html
p1 = page_template(
    title="The 10 Best Books About Productivity in 2026 | Bithues Reading Lab",
    h1="The 10 Best Books About Productivity in 2026",
    description="Looking for the best productivity books? We ranked the top 10 — from Atomic Habits to Getting Things Done — with detailed breakdowns of what each offers.",
    canonical="best-books-about-productivity.html",
    breadcrumb="best-books-about-productivity.html",
    hero_label="Productivity",
    content_html='''<p>Productivity is one of those words that gets used so often it starts to lose meaning. But the books on this list aren't about squeezing more hours into your day — they're about being more intentional with the hours you have. The difference matters. Here's our ranking of the best productivity books available.</p>

<h2>1. Atomic Habits by James Clear</h2>
<p>Atomic Habits is the rare productivity book that actually changes behavior. Clear's argument is simple but powerful: you don't rise to your goals, you fall to your systems. By making tiny improvements — 1% better every day — you compound into results that would be unrecognizable a year later. The habit loop framework (cue, craving, response, reward) gives you a practical tool for debugging your own behavior. This is the book we recommend most often to people who feel stuck.</p>
<p><a href="https://www.amazon.com/dp/B07D7W41B1/?tag=bithues-20" rel="nofollow">Buy Atomic Habits on Amazon →</a></p>

<h2>2. Deep Work by Cal Newport</h2>
<p>Newport coined the term "deep work" — professional activity performed in a state of distraction-free concentration that pushes your cognitive capabilities to their limit. His case against constant connectivity is backed by neuroscience, not just vibes. If you've ever ended a workday wondering where the hours went, this book explains why and what to do about it.</p>
<p><a href="https://www.amazon.com/dp/B00X4W8T76/?tag=bithues-20" rel="nofollow">Buy Deep Work on Amazon →</a></p>

<h2>3. Essentialism: The Disciplined Pursuit of Less by Greg McKeown</h2>
<p>Essentialism argues that the right selection of what to do is more important than doing more. McKeown's core insight: "If you don't prioritize your life, someone else will." The book is built around a disciplined process of identifying what truly matters and systematically eliminating everything else.</p>
<p><a href="https://www.amazon.com/dp/0804179405/?tag=bithues-20" rel="nofollow">Buy Essentialism on Amazon →</a></p>

<h2>4. Getting Things Done by David Allen</h2>
<p>GTD is over 20 years old and still the foundation of most productivity systems. Allen's core idea — that your brain is for having ideas, not holding them — has freed millions from the anxiety of trying to keep track of everything mentally. The two-minute rule alone has probably saved millions of hours.</p>
<p><a href="https://www.amazon.com/dp/0143127553/?tag=bithues-20" rel="nofollow">Buy Getting Things Done on Amazon →</a></p>

<h2>5. The 4-Hour Workweek by Tim Ferriss</h2>
<p>Love it or hate it, Ferriss's book changed how people think about work. The core argument — that the 40-year career model is obsolete and that leveraging time and automation is how you escape the deferral trap — has spawned an entire genre of lifestyle design literature. Even if you don't want to work 4 hours a week, the principles are useful.</p>
<p><a href="https://www.amazon.com/dp/0307465357/?tag=bithues-20" rel="nofollow">Buy The 4-Hour Workweek on Amazon →</a></p>

<h2>6. The Power of Habit by Charles Duhigg</h2>
<p>Duhigg, a Wall Street Journal reporter, uses his investigative skills to dig into habit science with unusual depth. The "habit loop" (cue → routine → reward) framework appears across many subsequent books, but the original is still the clearest and most well-sourced. His case studies — from Olympic swimmers to Proctor & Gamble — give it an narrative weight that dry science writing lacks.</p>
<p><a href="https://www.amazon.com/dp/081298160X/?tag=bithues-20" rel="nofollow">Buy The Power of Habit on Amazon →</a></p>

<h2>7. Make It Stick: The Science of Successful Learning</h2>
<p>Produced by cognitive scientists, Make It Stick is the research-backed corrective to much of the popular productivity literature. Its core argument — that most popular study methods (rereading, highlighting, cramming) are less effective than they feel — has significant implications for anyone trying to learn efficiently. Particularly valuable for knowledge workers who are also lifelong learners.</p>

<h2>8. So Good They Can't Ignore You by Cal Newport</h2>
<p>Newton's follow-up to Deep Work tackles the passion hypothesis — the idea that you should follow your passion to find work you love. He argues the opposite: that passion is a byproduct of skill development and that "career capital" (rare and valuable skills) is what gives you leverage to craft work you find meaningful.</p>

<h2>9. The 7 Habits of Highly Effective People by Stephen Covey</h2>
<p>Covey's book is decades old and shows its age in places, but the core framework — moving from dependence to independence to interdependence — remains powerful. The habits (be proactive, begin with the end in mind, put first things first, think win-win, seek first to understand, synergize, sharpen the saw) have become foundational vocabulary in organizational development.</p>
<p><a href="https://www.amazon.com/dp/1982137274/?tag=bithues-20" rel="nofollow">Buy The 7 Habits on Amazon →</a></p>

<h2>10. Scarcity: The New Science of Having Less and Needing More</h2>
<p>Mullainathan and Thaler approach productivity through the lens of cognitive bandwidth — the idea that scarcity (of time, money, food) creates a focus that, paradoxically, impairs the very decision-making needed to escape scarcity. This is the most intellectually rigorous entry on the list and rewards careful reading.</p>

''' + key_takeaway_box("The best productivity books don't add more to your to-do list — they change how you think about what deserves your time in the first place. Start with Atomic Habits if you want a practical framework; start with Deep Work if you want to understand why your attention is the actual scarce resource.") + "\n\n" + related_links_section([
    ("Best Self-Help Books", "best-self-help-books.html"),
    ("Best Books About Money", "best-books-about-money.html"),
    ("Browse Self-Help Reviews", "category/self-help.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"The 10 Best Books About Productivity in 2026","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("best-books-about-productivity.html", p1)

# 2. best-books-about-money.html
p2 = page_template(
    title="Best Books About Money: Personal Finance & Investing | Bithues Reading Lab",
    h1="Best Books About Money: Personal Finance & Investing",
    description="From The Psychology of Money to Rich Dad Poor Dad — these are the best books about money that actually teach you something useful.",
    canonical="best-books-about-money.html",
    breadcrumb="best-books-about-money.html",
    hero_label="Personal Finance",
    content_html='''<p>Money is one of the most written-about and least understood topics in modern life. Most personal finance advice is either too simplistic to be useful or too technical to be actionable. The books on this list are different — they earned their place through clarity, honesty, and the ability to change how you think about money permanently.</p>

<h2>The Psychology of Money by Morgan Housel</h2>
<p>There are books about money that teach you the math, and books that teach you the psychology. The Psychology of Money is the latter, and it's the best book in its category. Housel's key insight: financial decisions are rarely made on the basis of spreadsheets — they're made on the basis of personal history, emotion, and identity. Understanding why you make the decisions you make about money is more valuable than any specific investment tip. This book will make you rethink things you thought you understood.</p>
<p><a href="https://www.amazon.com/dp/0857197681/?tag=bithues-20" rel="nofollow">Buy The Psychology of Money on Amazon →</a></p>

<h2>Rich Dad Poor Dad by Robert Kiyosaki</h2>
<p>Kiyosaki's central argument — that the rich teach their kids about assets and liabilities while the middle class teaches financial compliance — is simple but has sparked genuine behavior change in millions of readers. Whether or not you agree with every specific, the core distinction between working for money and having money work for you is a useful mental model.</p>
<p><a href="https://www.amazon.com/dp/1615237024/?tag=bithues-20" rel="nofollow">Buy Rich Dad Poor Dad on Amazon →</a></p>

<h2>I Will Teach You to Be Rich by Ramit Sethi</h2>
<p>Sethi's approach is pragmatic and actionable in a way that most financial advice isn't. Rather than vague exhortations to "save more," he gives specific scripts for negotiating salary, automating savings, and optimizing your credit cards. The 6-week "I Will Teach You to Be Rich" program has helped hundreds of thousands of people build actual financial infrastructure.</p>
<p><a href="https://www.amazon.com/dp/0761147489/?tag=bithues-20" rel="nofollow">Buy I Will Teach You to Be Rich on Amazon →</a></p>

<h2>The Simple Path to Wealth by JL Collins</h2>
<p>Collins strips investing down to its essential elements and makes a compelling case for index fund investing — not as a compromise but as the optimal strategy for most people. His writing is unusually clear for financial topics and his advice is refreshingly direct: low-cost index funds, consistent investing, don't try to beat the market.</p>

<h2>Your Money or Your Brain by Jason Zweig</h2>
<p>Zweig's book translates behavioral finance research into practical guidance for investors. His key contribution: showing how your own emotions are your biggest investment risk and providing specific strategies for managing them. The chapters on how to evaluate investment performance are particularly valuable.</p>

<h2>The Millionaire Next Door by Thomas Stanley</h2>
<p>Research-driven and counterintuitive, this book reveals that most people who look wealthy aren't — and most people who are actually wealthy don't look it. The key finding: wealth is built through underconsumption and consistent saving, not high income. Important corrective to the consumption-driven definition of success.</p>

<h2>The Bogleheads' Guide to Investing</h2>
<p>Built on the philosophy of Vanguard founder John Bogle, this book is the definitive guide to passive index fund investing. It's thorough, practical, and grounded in a philosophy that prioritizes long-term compounding over short-term performance chasing.</p>

<h2>Thinking, Fast and Slow by Daniel Kahneman</h2>
<p>Kahneman's Nobel-winning research on cognitive biases is directly applicable to financial decision-making. The "System 1 / System 2" framework helps explain why people make predictably irrational decisions about money — and how to compensate for those biases.</p>
<p><a href="https://www.amazon.com/dp/0374533555/?tag=bithues-20" rel="nofollow">Buy Thinking, Fast and Slow on Amazon →</a></p>

''' + key_takeaway_box("The best books about money teach you to think differently, not just do different things with your paycheck. The Psychology of Money is the single highest-ROI read in this category — it changes your relationship with money, not just your account balance.") + "\n\n" + related_links_section([
    ("Best Productivity Books", "best-books-about-productivity.html"),
    ("Best Self-Help Books", "best-self-help-books.html"),
    ("Browse Nonfiction Reviews", "category/nonfiction.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Best Books About Money: Personal Finance & Investing","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("best-books-about-money.html", p2)

# 3. best-sci-fi-books.html
p3 = page_template(
    title="Best Science Fiction Books Worth Your Time | Bithues Reading Lab",
    h1="Best Science Fiction Books Worth Your Time",
    description="The best sci-fi books — ranked and reviewed. From Project Hail Mary to Dune to Hyperion, here's your definitive guide to science fiction worth reading.",
    canonical="best-sci-fi-books.html",
    breadcrumb="best-sci-fi-books.html",
    hero_label="Science Fiction",
    content_html='''<p>Science fiction is the literature of possibility — and these books represent the genre at its most ambitious, intelligent, and rewarding. Whether you're new to sci-fi or a seasoned reader looking for your next obsession, this list has something for you.</p>

<h2>Project Hail Mary by Andy Weir</h2>
<p>Andy Weir followed The Martian with something even better. Project Hail Mary is the story of a lone astronaut who wakes up with no memory on a mission to save humanity — and the solution requires more than just engineering. It's a science education wrapped in a page-turning thriller, and it does what the best sci-fi does: makes you feel smarter for having read it. Rocky the alien is one of the great characters in recent genre fiction.</p>
<p><a href="https://www.amazon.com/dp/0593135202/?tag=bithues-20" rel="nofollow">Buy Project Hail Mary on Amazon →</a></p>

<h2>The Martian by Andy Weir</h2>
<p>Before Project Hail Mary, there was The Martian — the book that made hard science fiction accessible to mainstream readers and launched Weir to global recognition. Mark Watney's deadpan problem-solving and dark humor make a survival story feel like a comedy of errors. The science is real and the solutions are plausible. This is the book that made "I was stranded on Mars and had to science the hell out of this" a cultural reference.</p>
<p><a href="https://www.amazon.com/dp/0553418025/?tag=bithues-20" rel="nofollow">Buy The Martian on Amazon →</a></p>

<h2>Dune by Frank Herbert</h2>
<p>No science fiction list is complete without Dune — and the reason it's still on every list fifty years later is that it holds up. Herbert built a world with more depth, political complexity, and ecological sophistication than any science fiction novel before or since. Paul Atreides's story is a meditation on power, religion, and the dangers of charismatic leadership. Frank Herbert didn't just write a novel; he built a mythology.</p>
<p><a href="https://www.amazon.com/dp/0441172717/?tag=bithues-20" rel="nofollow">Buy Dune on Amazon →</a></p>

<h2>Foundation by Isaac Asimov</h2>
<p>Asimov's epic about the fall of a galactic empire and the mathematician who plans to reduce the darkness to 1,000 years of barbarism instead of 10,000 invented the "psychohistory" concept that has influenced everything from Star Wars to Google. Foundation is a masterclass in ideas-driven fiction — the plot matters, but the intellectual architecture is what makes it unforgettable.</p>
<p><a href="https://www.amazon.com/dp/0553293354/?tag=bithues-20" rel="nofollow">Buy Foundation on Amazon →</a></p>

<h2>Hyperion by Dan Simmons</h2>
<p>Seven pilgrims. Seven stories. One pilgrimage to the Time Tombs of Hyperion. Simmons essentially invented the "linked short story" format within a larger epic framework, and the result is a book that functions both as a collection of excellent novellas and as a unified narrative with a spectacular cliffhanger ending. The Shrike is one of sci-fi's great antagonists — a killing machine that exists outside of time.</p>
<p><a href="https://www.amazon.com/dp/0553283685/?tag=bithues-20" rel="nofollow">Buy Hyperion on Amazon →</a></p>

<h2>The Left Hand of Darkness by Ursula K. Le Guin</h2>
<p>Le Guin's novel about an envoy from the Ekumen sent to the planet Gethen — where inhabitants are ambisexual — is a thought experiment in gender, identity, and political philosophy that remains startlingly relevant. It's also a gripping story of betrayal, loyalty, and the search for home. Le Guin writes with the precision of an anthropologist and the compassion of someone who actually cares about the beings she's describing.</p>
<p><a href="https://www.amazon.com/dp/0441478125/?tag=bithues-20" rel="nofollow">Buy The Left Hand of Darkness on Amazon →</a></p>

<h2>The Three-Body Problem by Cixin Liu</h2>
<p>Liu's trilogy — starting with The Three-Body Problem — brought Chinese science fiction to global prominence and deservedly so. It spans cosmic scales and millions of years while never losing the human thread. The novel deals with the consequences of China's Cultural Revolution through the lens of contact with an alien civilization — a premise that manages to be both scientifically rigorous and emotionally devastating.</p>
<p><a href="https://www.amazon.com/dp/0765382032/?tag=bithues-20" rel="nofollow">Buy The Three-Body Problem on Amazon →</a></p>

<h2>Neuromancer by William Gibson</h2>
<p>Gibson coined "cyberspace" with this novel — and in doing so, he essentially predicted the internet. Set in a world of corporate espionage, neural interfaces, and AI run amok, Neuromancer's influence on cyberpunk culture is incalculable. Case, Molly, and the Wintermute AI are iconic figures of 20th-century fiction.</p>
<p><a href="https://www.amazon.com/dp/0441569595/?tag=bithues-20" rel="nofollow">Buy Neuromancer on Amazon →</a></p>

<h2>Snow Crash by Neal Stephenson</h2>
<p>Snow Crash reads like if a computer scientist and a linguist and a cultural historian co-wrote a thriller. Hiro Protagonist — pizza deliveryman and freelance hacker in a disintegrating near-future America — is one of the great comic creations in genre fiction. Stephenson's thesis about the nature of language and its relationship to control is genuinely thought-provoking.</p>
<p><a href="https://www.amazon.com/dp/0553380958/?tag=bithues-20" rel="nofollow">Buy Snow Crash on Amazon →</a></p>

''' + key_takeaway_box("Project Hail Mary is the best place to start if you're new to science fiction. It's accessible, funny, scientifically accurate, and emotionally rich. If you've already read it and loved it, move to Hyperion or The Three-Body Problem for something denser and more complex.") + "\n\n" + related_links_section([
    ("Books Like Project Hail Mary", "books-like-project-hail-mary.html"),
    ("Books Like Hyperion", "books-like-hyperion.html"),
    ("Browse Sci-Fi Reviews", "category/science-fiction.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Best Science Fiction Books Worth Your Time","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("best-sci-fi-books.html", p3)

# 4. best-fantasy-books.html
p4 = page_template(
    title="Best Fantasy Books for Readers Who Want Something Real | Bithues Reading Lab",
    h1="Best Fantasy Books for Readers Who Want Something Real",
    description="The best fantasy books ranked for thoughtful readers. From Name of the Wind to The Way of Kings — fantasy that earns its word count.",
    canonical="best-fantasy-books.html",
    breadcrumb="best-fantasy-books.html",
    hero_label="Fantasy",
    content_html='''<p>The fantasy genre gets dismissed by people who've never looked closely at it. Yes, there's a lot of derivative sword-and-sorcery filler on the shelves. But the best fantasy is some of the most ambitious, emotionally resonant fiction being written today. Here are the books that prove it.</p>

<h2>The Name of the Wind by Patrick Rothfuss</h2>
<p>Rothfuss writes prose that makes you want to slow down and taste every sentence. Kvothe's story — from traveling performer to infamous legend — is told in two timelines that weave together masterfully. The University sections are particular highlights; the magic system is one of the most intellectually satisfying in the genre. This is a book for people who care about writing as craft, not just plot as delivery mechanism. The third book has been a long time coming, but the first two stand on their own.</p>
<p><a href="https://www.amazon.com/dp/0756404746/?tag=bithues-20" rel="nofollow">Buy The Name of the Wind on Amazon →</a></p>

<h2>The Way of Kings by Brandon Sanderson</h2>
<p>The first volume of Sanderson's planned ten-book Stormlight Archive is an epic in the truest sense — a story of two worlds at war, an ancient enemy returning, and individuals discovering what they're capable of when everything familiar is stripped away. Kaladin's arc from privileged soldier to enslaved bridgeman to reluctant leader is one of fantasy's great character journeys. Sanderson's magic systems are rigorous and his plotting is precise; this is fantasy for people who like to think.</p>
<p><a href="https://www.amazon.com/dp/0765365278/?tag=bithues-20" rel="nofollow">Buy The Way of Kings on Amazon →</a></p>

<h2>The Lies of Locke Lamora by Scott Lynch</h2>
<p>If the previous two books are about heroes finding themselves, The Lies of Locke Lamora is about a crew of thieves who already know exactly who they are — charming, brilliant, morally compromised, and loyal to each other above everything else. Lynch's Venice-analogue city of Camorr is beautifully realized and the heist sequences are among the best in genre fiction. Dark, funny, and propulsive.</p>
<p><a href="https://www.amazon.com/dp/0553419021/?tag=bithues-20" rel="nofollow">Buy The Lies of Locke Lamora on Amazon →</a></p>

<h2>The First Law Trilogy by Joe Abercrombie</h2>
<p>Abercrombie'sgrimdark trilogy dismantles the fantasy hero narrative by showing what happens when ordinary people with ordinary motivations operate in an epic fantasy setting. The violence isn't gratuitous — it serves a purpose. The characters aren't aspirational — they're recognizable. This is fantasy as psychological realism, and it is exceptionally well done.</p>
<p><a href="https://www.amazon.com/dp/0316387343/?tag=bithues-20" rel="nofollow">Buy The First Law Trilogy on Amazon →</a></p>

<h2>A Game of Thrones by George R.R. Martin</h2>
<p>No fantasy list is complete without it, and it's on every list for legitimate reasons. Martin built a world of genuine moral complexity where the good guys don't always win and the bad guys don't always lose. The political intrigue is extraordinary, the characters are unforgettable, and the willingness to kill beloved protagonists created genuine tension in a way fantasy rarely achieves. A landmark.</p>
<p><a href="https://www.amazon.com/dp/0553593543/?tag=bithues-20" rel="nofollow">Buy A Game of Thrones on Amazon →</a></p>

<h2>The Fifth Season by N.K. Jemisin</h2>
<p>Jemisin won the Hugo Award for all three books in this trilogy — the first author to achieve that feat. The Fifth Season is set in a world of constant seismic catastrophe where certain people (orogenes) can control earth and fire. Its narrative structure — told from multiple perspectives including second-person — is unconventional but deeply affecting. Jemisin uses fantasy to examine power, community, and the stories societies tell themselves about their past.</p>
<p><a href="https://www.amazon.com/dp/0316229296/?tag=bithues-20" rel="nofollow">Buy The Fifth Season on Amazon →</a></p>

<h2>The Poppy War by R.F. Kuang</h2>
<p>Kuang combines the rigorous world-building of traditional epic fantasy with the specific historical trauma of 20th-century China. Her protagonist Rin goes from war orphan to shamanic warrior to something much darker, and the trilogy escalates into territory that is genuinely difficult to read. The first book draws heavily on the Sino-Japanese War; subsequent books pull from Mao's Cultural Revolution. This is fantasy as historical allegory, and it does not pull punches.</p>
<p><a href="https://www.amazon.com/dp/0062662577/?tag=bithues-20" rel="nofollow">Buy The Poppy War on Amazon →</a></p>

<h2>Circe by Madeline Miller</h2>
<p>Miller takes the minor figure of Circe from Greek mythology — the witch who turned Odysseus's men into pigs — and gives her an entire interior life. The novel is a meditation on power, immortality, loneliness, and what it means to be mortal. Miller's prose is crystalline and her love of the original texts is evident on every page. This is literary fantasy at its best.</p>
<p><a href="https://www.amazon.com/dp/0062561022/?tag=bithues-20" rel="nofollow">Buy Circe on Amazon →</a></p>

''' + key_takeaway_box("If you want fantasy with literary quality, start with The Name of the Wind or Circe. If you want epic scale and a complete reading experience, start with The Way of Kings or The Lies of Locke Lamora. Either way, avoid the trap of reading fantasy that isn't ambitious enough to reward your time.") + "\n\n" + related_links_section([
    ("Best Sci-Fi Books", "best-sci-fi-books.html"),
    ("Books Like 1984", "books-like-1984.html"),
    ("Browse Fantasy Reviews", "category/fantasy.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Best Fantasy Books for Readers Who Want Something Real","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("best-fantasy-books.html", p4)

# 5. best-historical-fiction.html
p5 = page_template(
    title="Best Historical Fiction That Actually Teaches You History | Bithues Reading Lab",
    h1="Best Historical Fiction That Actually Teaches You History",
    description="The best historical fiction — from Shogun to Pillars of the Earth. Novels that entertain while making you genuinely understand the past.",
    canonical="best-historical-fiction.html",
    breadcrumb="best-historical-fiction.html",
    hero_label="Historical Fiction",
    content_html='''<p>Historical fiction occupies a unique position in the literary landscape — it has to do two things equally well: be a compelling story and be historically accurate. The books on this list manage both. They're not just set in the past; they make you feel like you're living in it.</p>

<h2>Shogun by James Clavell</h2>
<p>Shogun is the definitive gateway drug to historical fiction. Set in Japan in 1600, it follows a shipwrecked English sailor (John Blackthorne) who becomes a player in the politics of Japan's most powerful warlord. Clavell's Japan is rich, alien, and completely convincing. The novel is long — very long — but it never drags. Every chapter builds understanding. After reading Shogun, you'll have a genuinely different view of Japanese history and culture. It's one of those books that permanently expands how you see the world.</p>
<p><a href="https://www.amazon.com/dp/0553593543/?tag=bithues-20" rel="nofollow">Buy Shogun on Amazon →</a></p>

<h2>The Pillars of the Earth by Ken Follett</h2>
<p>Follett spent years researching 12th-century England before writing this, and it shows on every page. The story — about the building of a cathedral in a fictional town called Kingsbridge — is epic in the truest sense. It's about power, about faith, about the relationship between rulers and the ruled, and about the people who are willing to do terrible things for what they believe is right. Over 1,000 pages and you'll resent every one when it ends.</p>
<p><a href="https://www.amazon.com/dp/0451207082/?tag=bithues-20" rel="nofollow">Buy The Pillars of the Earth on Amazon →</a></p>

<h2>Wolf Hall by Hilary Mantel</h2>
<p>Mantel's Booker Prize-winning novel about Thomas Cromwell is the closest thing historical fiction has to literary fiction at its absolute peak. She writes Cromwell's interior life with an intimacy that makes you forget you're reading about a 16th-century lawyer — he's just a man navigating impossible situations with intelligence and patience. The prose is austere and precise; the historical detail is seamlessly integrated. Reading it, you feel like you're inside the Tudor court, watching decisions being made.</p>
<p><a href="https://www.amazon.com/dp/0316078737/?tag=bithues-20" rel="nofollow">Buy Wolf Hall on Amazon →</a></p>

<h2>The Last Samurai by Helen DeWitt</h2>
<p>Wait — The Last Samurai is a film. But DeWitt's novel — one of the great idiosyncratic achievements in contemporary fiction — follows a mother and son in Japan as they navigate language, culture, and identity with relentless intellectual energy. DeWitt's novel doesn't teach you about history in the conventional sense, but it teaches you about what it means to be a stranger in a culture and what we owe the people we love.</p>

<h2>All the Light We Cannot See by Anthony Doerr</h2>
<p>Doerr's Pulitzer Prize-winning novel follows a blind French girl and a German boy whose paths intersect in occupied France during World War II. The novel's structure — short, precise chapters that jump between characters and time periods — creates a mosaic effect that builds emotional resonance over time. The science details (wavelengths, frequencies, how radio signals work) are woven in so naturally they become metaphors. This is historical fiction as poetry.</p>
<p><a href="https://www.amazon.com/dp/1476746586/?tag=bithues-20" rel="nofollow">Buy All the Light We Cannot See on Amazon →</a></p>

<h2>Lonesome Dove by Larry McMurtry</h2>
<p>Lonesome Dove is technically a Western, but it's also one of the great American historical novels. The cattle drive from Texas to Montana is the frame for a story about aging, friendship, regret, and what the frontier meant to the people who lived it. McMurtry writes with compassion and precision about a period whose mythology has obscured its reality. This is a book that makes you feel the weight of distance.</p>

<h2>The Book Thief by Markus Zusak</h2>
<p>Set in Nazi Germany and narrated by Death, The Book Thief tells the story of Liesel Meminger — a girl whose relationship with books becomes a form of resistance in a world where books are being burned. Zusak's choice of narrator is daring and it pays off — Death's weariness and dark humor create a perspective that makes the horror more real, not less. A book about the power of stories to sustain us in the darkest times.</p>
<p><a href="https://www.amazon.com/dp/0375842209/?tag=bithues-20" rel="nofollow">Buy The Book Thief on Amazon →</a></p>

<h2>The Name of the Wind (fantasy, but historical worldbuilding)</h2>
<p>Kingkiller Chronicle's framing device — Kvothe telling his story to a chronicler — makes it a story about the writing of history itself. The way stories become mythologized, the gap between what happened and what people believe happened, is one of the trilogy's central themes. For readers interested in the relationship between narrative and historical truth, this is uniquely rewarding.</p>

''' + key_takeaway_box("Shogun is the single best entry point into historical fiction if you haven't read it yet. It's historically rigorous, narratively propulsive, and it will give you a genuine understanding of a period and culture most Western readers know almost nothing about.") + "\n\n" + related_links_section([
    ("Best Biography Books", "best-biography-books.html"),
    ("Best Fantasy Books", "best-fantasy-books.html"),
    ("Browse Historical Fiction Reviews", "category/historical-fiction.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Best Historical Fiction That Actually Teaches You History","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("best-historical-fiction.html", p5)

# 6. best-thriller-books.html
p6 = page_template(
    title="Best Thriller and Mystery Books for 2026 | Bithues Reading Lab",
    h1="Best Thriller and Mystery Books for 2026",
    description="The best thriller and mystery books ranked — from Gone Girl to The Silent Patient. Page-turners that earn every twist.",
    canonical="best-thriller-books.html",
    breadcrumb="best-thriller-books.html",
    hero_label="Thriller & Mystery",
    content_html='''<p>Thriller fiction has never been more popular or more diverse. The genre has splintered into psychological thriller, legal thriller, domestic thriller, Nordic noir, cozy mystery — and each subgenre has produced genuinely great books. Here are the ones that stand out.</p>

<h2>Gone Girl by Gillian Flynn</h2>
<p>Gone Girl isn't just a thriller — it's a deconstruction of how media constructs gender narratives and how an innocent person can be destroyed by a story that the public wants to believe. The dual-narrator structure and the mid-novel twist remake everything you thought you understood. Flynn's prose is sharp enough to cut, and her understanding of how people perform for each other is unmatched. This is the book that defined the 2010s thriller landscape.</p>
<p><a href="https://www.amazon.com/dp/0307588378/?tag=bithues-20" rel="nofollow">Buy Gone Girl on Amazon →</a></p>

<h2>The Silent Patient by Alex Michaelides</h2>
<p>Michaelides's debut novel made him one of the most talked-about thriller writers of the decade. The premise: a woman (Alicia) shoots her husband and then stops speaking entirely. A criminal psychotherapist (Theo) becomes obsessed with her case and with uncovering what happened that night. The twist lands with unusual force, partly because the groundwork has been carefully laid. This is a book that asks: what is the relationship between trauma and truth?</p>
<p><a href="https://www.amazon.com/dp/1250303046/?tag=bithues-20" rel="nofollow">Buy The Silent Patient on Amazon →</a></p>

<h2>The Girl with the Dragon Tattoo by Stieg Larsson</h2>
<p>Larsson's millennium trilogy begins with one of the great detective novels in the genre. Mikael Blomkvist takes on a decades-old missing persons case; Lisbeth Salander — a hacker with a traumatic past and extraordinary skills — becomes his unlikely partner. Larsson's Sweden is a society with hidden cruelties that polite surfaces conceal. The procedural elements are meticulous; the social commentary is quietly devastating.</p>
<p><a href="https://www.amazon.com/dp/0307455166/?tag=bithues-20" rel="nofollow">Buy The Girl with the Dragon Tattoo on Amazon →</a></p>

<h2>Sharp Objects by Gillian Flynn</h2>
<p>Flynn's debut novel is darker and more claustrophobic than Gone Girl. A journalist (Camille) returns to her hometown in Missouri to cover the murders of two girls — and to confront her own history of self-harm and her emotionally manipulative mother. The small-town setting and the mother-daughter dynamic create a psychological pressure that makes the violent content feel both shocking and inevitable. Flynn understands that small cruelties are often more disturbing than large ones.</p>
<p><a href="https://www.amazon.com/dp/0307345770/?tag=bithues-20" rel="nofollow">Buy Sharp Objects on Amazon →</a></p>

<h2>In the Woods by Tana French</h2>
<p>French's Dublin Murder Squad series begins here, and it's the book that defined "literary thriller" for a generation. Detective Rob Ryan is investigating a murder in the same woods where he survived a childhood trauma — a trauma he has spent his career trying to forget. French is less interested in solving the crime than in exploring what investigation reveals about memory, identity, and guilt. The resolution will frustrate some readers, but it's thematically necessary.</p>
<p><a href="https://www.amazon.com/dp/0143035985/?tag=bithues-20" rel="nofollow">Buy In the Woods on Amazon →</a></p>

<h2>Behind Closed Doors by B.A. Paris</h2>
<p>Paris's debut is a masterclass in domestic thriller craft. Grace and Jack seem like the perfect couple — until you look more closely at Jack's behavior and realize what kind of prison Grace is living in. The novel's horror comes from the recognizable: not a serial killer but a husband whose cruelty operates entirely within the bounds of what others can see. Paris makes you feel the particular terror of not being believed.</p>
<p><a href="https://www.amazon.com/dp/1250122734/?tag=bithues-20" rel="nofollow">Buy Behind Closed Doors on Amazon →</a></p>

<h2>The Hunt by Ragnar Jónasson</h2>
<p>Icelandic noir at its most atmospheric. Five women, one suspicious social media post, a remote Icelandic village. Jónasson's talent is making the cold and isolation into characters in their own right. The novel unfolds with a patience that builds dread slowly and then pays off in a sequence of revelations that recontextualize everything that came before. Small towns and old secrets — Jónasson is a master of this formula.</p>
<p><a href="https://www.amazon.com/dp/1912374167/?tag=bithues-20" rel="nofollow">Buy The Hunt on Amazon →</a></p>

<h2>The Woman in the Window by A.J. Finn</h2>
<p>Finn's debut draws obvious comparisons to Rear Window, and the Hitchcockian setup — an agoraphobic psychologist who believes she witnessed a crime in a neighboring house — is deliberately deployed. What elevates the novel is the protagonist's unreliability and the genuine complexity of what's happening around her. The mystery is genuinely puzzling, not just because of what the protagonist doesn't know, but because of what she can't trust about herself.</p>
<p><a href="https://www.amazon.com/dp/0062678118/?tag=bithues-20" rel="nofollow">Buy The Woman in the Window on Amazon →</a></p>

''' + key_takeaway_box("Gone Girl is the essential modern thriller — it's the book that every subsequent domestic thriller has been compared to and most haven't matched. Read it, then read Sharp Objects for an even darker exploration of Flynn's preoccupations with identity and performance.") + "\n\n" + related_links_section([
    ("Best Sci-Fi Books", "best-sci-fi-books.html"),
    ("Books Like 1984", "books-like-1984.html"),
    ("Browse Thriller Reviews", "category/thriller.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Best Thriller and Mystery Books for 2026","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("best-thriller-books.html", p6)

# 7. best-biography-books.html
p7 = page_template(
    title="Best Biography Books: Lives Worth Reading | Bithues Reading Lab",
    h1="Best Biography Books: Lives Worth Reading",
    description="The best biography and memoir books — from Steve Jobs to Educated. These are the life stories that illuminate what it means to be human.",
    canonical="best-biography-books.html",
    breadcrumb="best-biography-books.html",
    hero_label="Biography & Memoir",
    content_html='''<p>Biography is the genre that promises you someone else's life — and the best ones deliver more than you expected. A great biography doesn't just document what someone did; it reveals who they were and why their story matters. These books represent the genre at its most revealing.</p>

<h2>Steve Jobs by Walter Isaacson</h2>
<p>Isaacson spent two years with Jobs, conducting over forty interviews with the man himself and hundreds more with colleagues, family, and competitors. The result is the definitive portrait of one of the most consequential figures of the modern era. Jobs's perfectionism, his cruelty, his vision, and his redemption are all here. The book is notable for Isaacson's willingness to show Jobs's damage alongside his genius — a completeness that Jobs himself approved, even when it made him look terrible.</p>
<p><a href="https://www.amazon.com/dp/1451648537/?tag=bithues-20" rel="nofollow">Buy Steve Jobs on Amazon →</a></p>

<h2>Elon Musk by Walter Isaacson</h2>
<p>Isaacson's second mega-biography covers a subject still very much in progress — which makes it a different kind of read than Steve Jobs. Following Musk through his most intense periods — the SpaceX turnaround, the Tesla Model 3 production crisis, the Twitter acquisition — Isaacson documents a figure defined by impossible ambition and a willingness to burn through whatever stands in the way. The book is controversial, and Isaacson doesn't pretend to have resolved the question of whether Musk is hero or villain.</p>
<p><a href="https://www.amazon.com/dp/0063282195/?tag=bithues-20" rel="nofollow">Buy Elon Musk on Amazon →</a></p>

<h2>Becoming by Michelle Obama</h2>
<p>Obama's memoir is one of the most-read books of the past decade, and its popularity reflects genuine quality. She writes with unusual candor about her own doubts, her marriage, her time in the White House, and what it cost her family. The sections about growing up on the South Side of Chicago are particularly vivid — they ground the book in a specific place and history rather than allowing it to float into pure abstraction. This is memoir as careful craft.</p>
<p><a href="https://www.amazon.com/dp/1524763138/?tag=bithues-20" rel="nofollow">Buy Becoming on Amazon →</a></p>

<h2>Educated by Tara Westover</h2>
<p>Westover grew up in a survivalist family in Idaho, with no formal education and no birth certificate until she was nine. The book traces her path from that childhood — where she was expected to work in her father's scrap metal junkyard and received no schooling — to Cambridge University and beyond. It's a story about the possibility of self-creation, but also a careful examination of what is lost when you choose education over family. No recent book has made readers think harder about what family means.</p>
<p><a href="https://www.amazon.com/dp/0399590501/?tag=bithues-20" rel="nofollow">Buy Educated on Amazon →</a></p>

<h2>Born a Crime by Trevor Noah</h2>
<p>Noah's memoir of growing up as a mixed-race child in apartheid and post-apartheid South Africa is as funny as you'd expect from a comedian — and as devastating as the material requires. The section on his mother's faith is particularly affecting, and the story of Noah's relationship with his mother is the emotional core of the book. Humor as survival mechanism, and the limits of humor when the circumstances are genuinely dire.</p>
<p><a href="https://www.amazon.com/dp/0399588175/?tag=bithues-20" rel="nofollow">Buy Born a Crime on Amazon →</a></p>

<h2>Bad Blood: Secrets and Lies in a Silicon Valley Startup by John Carreyrou</h2>
<p>Carreyrou, a Wall Street Journal reporter, chronicles the rise and fall of Elizabeth Holmes and Theranos — a story that combines tech fraud, personal charisma, and the failure of institutional scrutiny. The book is a thriller in its own right, with Holmes playing a villain whose ability to deceive was almost impressive. Important reading for anyone who wants to understand how fraud happens at scale.</p>
<p><a href="https://www.amazon.com/dp/0527766634/?tag=bithues-20" rel="nofollow">Buy Bad Blood on Amazon →</a></p>

<h2>Shoe Dog by Phil Knight</h2>
<p>Knight — co-founder of Nike — wrote his memoir with unusual candor about what it actually took to build one of the world's most recognizable brands. The early days of selling shoes out of the back of a car, the near-death experiences with the company's finances, the relationship with Bill Bowerman — it's all here. The title comes from the Japanese word for "death" that appeared on early Nike shipping labels, which Knight took as a sign that the company would have to survive something. A story about persistence and belief.</p>
<p><a href="https://www.amazon.com/dp/1476716216/?tag=bithues-20" rel="nofollow">Buy Shoe Dog on Amazon →</a></p>

<h2>Open by Andre Agassi</h2>
<p>Agassi's memoir is remarkable for its willingness to be unsympathetic. The greatest tennis player of his generation writes openly about his hatred of the sport, his use of crystal meth, his father's abuse, and his decade of secret struggle. The book's structure — non-linear, jumping between his career and his post-tennis foundation work — makes it more than a standard sports autobiography. A story about identity and what we owe our authentic selves.</p>
<p><a href="https://www.amazon.com/dp/0300759478/?tag=bithues-20" rel="nofollow">Buy Open on Amazon →</a></p>

''' + key_takeaway_box("Educated is the biography that stays with you longest — not because of what Tara Westover achieved but because of what she had to let go of to get there. It's a story about the cost of self-creation and whether any education is worth the price of losing your family.") + "\n\n" + related_links_section([
    ("Best Historical Fiction", "best-historical-fiction.html"),
    ("Best Self-Help Books", "best-self-help-books.html"),
    ("Browse Biography Reviews", "category/biography.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Best Biography Books: Lives Worth Reading","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("best-biography-books.html", p7)

# 8. best-self-help-books.html
p8 = page_template(
    title="Best Self-Help Books That Are Actually Worth Reading | Bithues Reading Lab",
    h1="Best Self-Help Books That Are Actually Worth Reading",
    description="The best self-help books ranked and reviewed — from Atomic Habits to Mindset. No filler, no hype, just books that genuinely work.",
    canonical="best-self-help-books.html",
    breadcrumb="best-self-help-books.html",
    hero_label="Self-Help",
    content_html='''<p>Let's be honest about self-help: most of it is noise. The shelves are crowded with books that promise transformation in 21 days, that restate obvious ideas in motivational jargon, and that leave you feeling worse — not better — after reading them. But the genre isn't empty. There are books here that have genuinely changed how people live. These are them.</p>

<h2>Atomic Habits by James Clear</h2>
<p>Atomic Habits is the rare self-help book where the author actually did the research to back up his claims. Clear's core insight — that you don't rise to your goals, you fall to your systems — sounds simple until you try to build a system. The "habit loop" framework (cue → craving → response → reward) gives you a practical tool for debugging your own behavior, and his four laws of behavior change (make it obvious, attractive, easy, satisfying) are specific enough to implement immediately. This is the book we recommend first to anyone asking where to start.</p>
<p><a href="https://www.amazon.com/dp/B07D7W41B1/?tag=bithues-20" rel="nofollow">Buy Atomic Habits on Amazon →</a></p>

<h2>Mindset: The New Psychology of Success by Carol Dweck</h2>
<p>Dweck's research on fixed vs. growth mindset has influenced education, business coaching, and parenting advice across the developed world. Her core finding: people who believe their abilities are fixed (fixed mindset) avoid challenges and collapse under failure, while people who believe abilities can be developed (growth mindset) embrace difficulty as a learning opportunity. The book itself is accessible, though some critics have noted that it oversimplifies the research. Even with those caveats, the core concept is genuinely useful.</p>
<p><a href="https://www.amazon.com/dp/0345472322/?tag=bithues-20" rel="nofollow">Buy Mindset on Amazon →</a></p>

<h2>The Power of Habit by Charles Duhigg</h2>
<p>Duhigg, a Wall Street Journal reporter, investigated habit science with the rigor of an investigative journalist and the narrative skill of a novelist. The habit loop framework he popularized appears across dozens of subsequent books, but this original is still the clearest and best-sourced. His case studies — from Olympic swimmers to Proctor & Gamble to the Montgomery bus boycott — give habit science a historical weight that makes it feel less like pop psychology and more like real social science.</p>
<p><a href="https://www.amazon.com/dp/081298160X/?tag=bithues-20" rel="nofollow">Buy The Power of Habit on Amazon →</a></p>

<h2>The 7 Habits of Highly Effective People by Stephen Covey</h2>
<p>Covey's book has been around since 1989 and shows its age in some of its cultural assumptions — but the core framework (move from dependence to independence to interdependence) remains one of the most useful mental models for thinking about personal development. The seven habits — be proactive, begin with the end in mind, put first things first, think win-win, seek first to understand, synergize, sharpen the saw — have become organizational vocabulary. Not every idea ages well, but enough of them do to justify the investment.</p>
<p><a href="https://www.amazon.com/dp/1982137274/?tag=bithues-20" rel="nofollow">Buy The 7 Habits on Amazon →</a></p>

<h2>Deep Work by Cal Newport</h2>
<p>Newport's book is a direct assault on the idea that productivity means responding to everything immediately. His argument — that professional activity performed in a state of distraction-free concentration is the key to developing rare and valuable skills — is backed by neuroscience, historical case studies, and behavioral economics. The "deep work" concept has become influential enough that it's changed how knowledge workers think about their relationship with email, social media, and open-office plans.</p>
<p><a href="https://www.amazon.com/dp/B00X4W8T76/?tag=bithues-20" rel="nofollow">Buy Deep Work on Amazon →</a></p>

<h2>The Psychology of Money by Morgan Housel</h2>
<p>Housel's book isn't exactly self-help in the traditional sense — it's more personal finance psychology disguised as self-help. His key insight: financial decisions are rarely made on the basis of spreadsheets, they're made on the basis of personal history, emotion, and identity. Understanding why you make the decisions you make is more valuable than any specific investment tip. This is the book to give someone who thinks they're bad with money — not because it teaches them a system, but because it teaches them to understand themselves.</p>
<p><a href="https://www.amazon.com/dp/0857197681/?tag=bithues-20" rel="nofollow">Buy The Psychology of Money on Amazon →</a></p>

<h2>How to Win Friends and Influence People by Dale Carnegie</h2>
<p>Carnegie's 1936 classic is the original self-help book, and it shows its age — but the core principles (be genuinely interested in others, smile, remember names, be a good listener, make others feel important) are as valid now as they were in the Great Depression. The book's success is partly its accessibility: these are principles you can apply immediately without any special knowledge. Critics note that it can be used for manipulation as easily as for genuine connection — which is probably true of any social skills advice.</p>
<p><a href="https://www.amazon.com/dp/0671027034/?tag=bithues-20" rel="nofollow">Buy How to Win Friends on Amazon →</a></p>

<h2>Essentialism by Greg McKeown</h2>
<p>Essentialism argues that the disciplined pursuit of less — not just doing less, but systematically eliminating everything that isn't contributing to what matters — is the key to a productive and meaningful life. McKeown's core insight is the opportunity cost of time: every hour you spend on something that doesn't matter is an hour you can't spend on something that does. His "hell yes or no" framework for evaluating commitments is simple but has proven genuinely useful for people overwhelmed by too many options.</p>
<p><a href="https://www.amazon.com/dp/0804179405/?tag=bithues-20" rel="nofollow">Buy Essentialism on Amazon →</a></p>

''' + key_takeaway_box("Atomic Habits is the highest-ROI read in this category — it gives you a framework that actually works and that you can apply immediately. If you only read one book on this list, make it this one.") + "\n\n" + related_links_section([
    ("Best Books About Productivity", "best-books-about-productivity.html"),
    ("Books Like Atomic Habits", "books-like-atomic-habits.html"),
    ("Browse Self-Help Reviews", "category/self-help.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Best Self-Help Books That Are Actually Worth Reading","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("best-self-help-books.html", p8)

# 9. books-like-project-hail-mary.html
p9 = page_template(
    title="Books Like Project Hail Mary: If You Loved Andy Weir | Bithues Reading Lab",
    h1="Books Like Project Hail Mary: If You Loved Andy Weir",
    description="You loved Project Hail Mary. Here are the books that scratch the same itch — hard science, survival problem-solving, and lone protagonists who science their way out.",
    canonical="books-like-project-hail-mary.html",
    breadcrumb="books-like-project-hail-mary.html",
    hero_label="Similar to Project Hail Mary",
    content_html='''<p>If you finished <em>Project Hail Mary</em> and immediately wanted to read more — not just in science fiction, but in this specific subgenre of hard science survival — you know the particular feeling. You want the science to matter. You want the protagonist to earn their way out through intelligence and improvisation. You want a story where the solution to the problem requires understanding something real about how the universe works. Here are the books that deliver that feeling.</p>

<h2>The Martian by Andy Weir</h2>
<p>The obvious starting point — and in some ways, the better book. Mark Watney's deadpan voice, his engineering-by-calculation approach to survival, and Weir's refusal to let him off easy with convenient solutions: all the elements that made Project Hail Mary work are already here. The Martian is a pure survival story; Project Hail Mary adds an alien contact element. Start with whichever you haven't read yet. If you've read both and want more Weir, the only answer is to wait for whatever he writes next.</p>
<p><a href="https://www.amazon.com/dp/0553418025/?tag=bithues-20" rel="nofollow">Buy The Martian on Amazon →</a></li>
<li><a href="books-like-the-martian.html">See our full Books Like The Martian guide →</a></li></p>

<h2>Artemis by Andy Weir</h2>
<p>Same author, different setting — a lunar city rather than Mars. Jazz Bashara is a smuggler who gets drawn into a conspiracy on humanity's only moon colony. The science in Artemis is more speculative than in The Martian (lunar economics, 3D printing, low-gravity construction) but Weir's voice and problem-solving approach are consistent. It's not as good as The Martian, but it's still better than most science fiction being published.</p>
<p><a href="https://www.amazon.com/dp/1473644178/?tag=bithues-20" rel="nofollow">Buy Artemis on Amazon →</a></p>

<h2>The Moon Is a Harsh Mistress by Robert Heinlein</h2>
<p>Heinlein's 1966 novel is the gold standard for hard science fiction combined with political philosophy. Set in a lunar penal colony that has learned to be self-sufficient and is now questioning its relationship with Earth, it's about something larger than survival — it's about what it means to be free and what you're willing to fight for. The science is real (orbital mechanics, centrifugal gravity, agriculture in sealed environments); the politics is genuinely thought-provoking. Reading it alongside Project Hail Mary shows how much the survival genre has in common with the revolution genre.</p>
<p><a href="https://www.amazon.com/dp/0345407910/?tag=bithues-20" rel="nofollow">Buy The Moon Is a Harsh Mistress on Amazon →</a></p>

<h2>The Martian Chronicles by Ray Bradbury</h2>
<p>Don't come to Bradbury looking for hard science — this isn't that. The Martian Chronicles is poetry disguised as science fiction: a series of linked stories about Earth's colonization of Mars, each one examining a different facet of what it means to be human by showing us humans encountering something genuinely alien. If Project Hail Mary taught you that science can be exciting, Bradbury will teach you it can also be sad and beautiful.</p>

<h2>Iron Tide by Jared R. M. McCaffrey</h2>
<p>Independent author science fiction with a similar hard-SF approach to orbital mechanics and survival. The story involves a character stranded in the Jupiter system, and the engineering solutions are genuinely researched. It's less polished than Weir but it scratches the same itch — a protagonist whose primary weapon is their understanding of physics.</p>

<h2>故事的魔力 (The Story of What Can't Be Told) — various</h2>
<p>For readers who want more Chinese science fiction in this vein, the broader "hard SF survival" tradition includes works by Liu Cixin and Zhou Wen. These are less immediately accessible than Weir but reward the investment with genuinely cosmic scale.</p>

''' + key_takeaway_box("If you loved Project Hail Mary for the hard science and the survival elements, read The Martian if you haven't already. If you've read both and want the political/philosophical dimension, go to The Moon Is a Harsh Mistress. The common thread is protagonists who think their way out of impossible situations — and that thread runs through all of these recommendations.") + "\n\n" + related_links_section([
    ("Best Sci-Fi Books", "best-sci-fi-books.html"),
    ("Books Like The Martian", "books-like-the-martian.html"),
    ("Browse Sci-Fi Reviews", "category/science-fiction.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Books Like Project Hail Mary: If You Loved Andy Weir","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("books-like-project-hail-mary.html", p9)

# 10. books-like-atomic-habits.html
p10 = page_template(
    title="Books Like Atomic Habits: Building Better Habits | Bithues Reading Lab",
    h1="Books Like Atomic Habits: Building Better Habits",
    description="You loved Atomic Habits. Here are the best books that go deeper into habit science, behavior change, and productivity systems — ranked for different reading goals.",
    canonical="books-like-atomic-habits.html",
    breadcrumb="books-like-atomic-habits.html",
    hero_label="Similar to Atomic Habits",
    content_html='''<p>Atomic Habits has become one of the most-read personal development books of the past decade, and part of its appeal is that it condenses a lot of complex research into a clear, actionable framework. But that condensation means some readers want more — more depth, more alternatives, more nuance. Here are the books that go deeper in different directions.</p>

<h2>The Power of Habit by Charles Duhigg</h2>
<p>The book that most directly complements Atomic Habits — and in some ways is its intellectual parent. Duhigg's reporting approach grounds habit science in real-world case studies in a way that Clear's more principle-based approach doesn't. Where Atomic Habits gives you a framework, The Power of Habit gives you history. Understanding how the concept of habit loops was discovered and validated makes the framework more credible and more flexible. If you read Atomic Habits and felt it was too simplistic, read this.</p>
<p><a href="https://www.amazon.com/dp/081298160X/?tag=bithues-20" rel="nofollow">Buy The Power of Habit on Amazon →</a></p>

<h2>Tiny Habits by B.J. Novak</h2>
<p>Wait — B.J. Novak, from The Office? Yes. Novak spent years studying behavior science at Stanford's d.school and developed the "tiny habits" approach: instead of habit stacking or habit formation from scratch, start absurdly small. Want to do push-ups? Do one. Want to meditate? Meditate for 30 seconds. The point is that motivation is unreliable but environment design is not — and starting small is the way to make the behavior stick before you try to scale it up. It's a more forgiving approach than Atomic Habits for people who have struggled with habit formation in the past.</p>

<h2>Essentialism by Greg McKeown</h2>
<p>Atomic Habits is about what you do; Essentialism is about whether you should be doing it at all. McKeown's book argues that the real enemy of good habits isn't bad habits — it's the noise of everything else competing for your attention. If Atomic Habits made you more productive but busier, Essentialism is the corrective. The "hell yes or no" framework for evaluating commitments has helped many readers say no to things that would have diluted their progress.</p>
<p><a href="https://www.amazon.com/dp/0804179405/?tag=bithues-20" rel="nofollow">Buy Essentialism on Amazon →</a></p>

<h2>Make It Stick: The Science of Successful Learning</h2>
<p>Produced by researchers from the Center for Applied Learning in Science, Make It Stick is the research-backed corrective to much of what passes for learning advice in popular productivity literature. Its core argument: the methods that feel most effective (rereading, highlighting, cramming) are actually the least effective for long-term retention. The methods that feel hardest (retrieval practice, spaced repetition, interleaving) are the ones that actually build durable knowledge. Essential reading for knowledge workers who are also trying to learn.</p>

<h2>Thinking, Fast and Slow by Daniel Kahneman</h2>
<p>Not strictly a habit book — but if Atomic Habits made you interested in the cognitive science behind behavior, Thinking Fast and Slow is where that interest leads. Kahneman's dual-system framework (System 1: fast, automatic, emotional; System 2: slow, deliberate, analytical) explains why habits form in the first place (System 1's preference for shortcuts) and what it takes to override them (System 2 engagement). Dense and sometimes difficult, but genuinely transformative for how you think about decision-making.</p>
<p><a href="https://www.amazon.com/dp/0374533555/?tag=bithues-20" rel="nofollow">Buy Thinking, Fast and Slow on Amazon →</a></p>

<h2>Deep Work by Cal Newport</h2>
<p>Newport's book takes habit science into the productivity territory — specifically, the question of how to build a life structured around deep, focused work rather than fragmented attention. His argument that the ability to concentrate without distraction is becoming increasingly rare (and therefore increasingly valuable) has resonated with a generation of knowledge workers struggling with constant connectivity. The "deep work" concept is really a habit system: how to build rituals and routines that protect your cognitive resources.</p>
<p><a href="https://www.amazon.com/dp/B00X4W8T76/?tag=bithues-20" rel="nofollow">Buy Deep Work on Amazon →</a></p>

<h2>The 7 Habits of Highly Effective People by Stephen Covey</h2>
<p>Covey's classic goes beyond habit formation to framework-building — and while some of its examples feel dated, the underlying structure (independence → interdependence) remains genuinely useful. Readers who have worked through Atomic Habits and want to think about the next level of personal effectiveness will find Covey's quadrant model (urgent vs. important) particularly valuable for understanding how to spend their time.</p>
<p><a href="https://www.amazon.com/dp/1982137274/?tag=bithues-20" rel="nofollow">Buy The 7 Habits on Amazon →</a></p>

''' + key_takeaway_box("Atomic Habits gives you a system; The Power of Habit gives you the history behind it. Read both in order: Atomic Habits first (for the actionable framework), then The Power of Habit (to understand why it works). That combination will make you more effective than either book alone.") + "\n\n" + related_links_section([
    ("Best Self-Help Books", "best-self-help-books.html"),
    ("Best Books About Productivity", "best-books-about-productivity.html"),
    ("Browse Self-Help Reviews", "category/self-help.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Books Like Atomic Habits: Building Better Habits","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("books-like-atomic-habits.html", p10)

print("\n=== TASK 3: Creating 5 'Books Like X' Comparison Pages ===")

# 5 "books like" pages
# books-like-hyperion.html
ph1 = page_template(
    title="Books Like Hyperion by Dan Simmons | Bithues Reading Lab",
    h1="Books Like Hyperion by Dan Simmons",
    description="If you loved Dan Simmons' Hyperion, here are the books that capture the same epic scope, philosophical depth, and linked-story structure.",
    canonical="books-like-hyperion.html",
    breadcrumb="books-like-hyperion.html",
    hero_label="Similar to Hyperion",
    content_html='''<p>Hyperion by Dan Simmons is one of the most ambitious science fiction novels ever written — a nearly 500-page epic structured around seven pilgrims journeying to the Time Tombs of Hyperion, each telling their story along the way. If you've finished it and are hungry for more — whether in its specific linked-story format, its space-opera scope, or its philosophical ambition — these are the books that come closest to matching what it offers.</p>

<h2>Fallen Angels by Larry Niven, Jerry Pournelle & Michael Flynn</h2>
<p>A response to Heinlein's Starship Troopers that explores the political and social dimensions of space warfare. Like Hyperion, it uses science fiction as a vehicle for political philosophy — but does so in a more linear narrative structure. The collaboration between three very different authors creates a layered text where different perspectives visibly compete. If what you loved about Hyperion was its willingness to be political and philosophical simultaneously, this delivers.</p>

<h2>1984 by George Orwell</h2>
<p>Not science fiction in the technological sense, but Hyperion's Shrike — a being that exists outside of time and kills people in horrific ways — draws heavily from the tradition that Orwell established. The Time Tombs' relationship to causality parallels Winston Smith's relationship to the Party: both are trapped in systems that seem to operate outside of normal time. <a href="books-like-1984.html">See our full Books Like 1984 guide →</a></p>
<p><a href="https://www.amazon.com/dp/0452284234/?tag=bithues-20" rel="nofollow">Buy 1984 on Amazon →</a></p>

<h2>Dune by Frank Herbert</h2>
<p>Dune and Hyperion share a commitment to worldbuilding as philosophy — the world is not just a setting but a way of thinking about power, religion, ecology, and human potential. Herbert's ecological and political systems are as rigorous as Simmons's. Both books use invented worlds to ask questions that the contemporary world cannot comfortably ask. If you came to Hyperion for the worldbuilding depth, Dune is the obvious recommendation.</p>
<p><a href="https://www.amazon.com/dp/0441172717/?tag=bithues-20" rel="nofollow">Buy Dune on Amazon →</a></p>

<h2>The Dark Tower Series by Stephen King</h2>
<p>Simmons has acknowledged King's influence on the Hyperion Cantos — particularly on the character of the Shrike. King's gunslinger Roland chasing the Dark Tower across multiple worlds has the same mythic quality as the pilgrims crossing the Hyperion landscape. King's series is darker, more American, and more explicitly mythic, but the structural similarity — a small group of disparate people on a shared quest — is real.</p>

<h2>Gateway by Frederick Pohl</h2>
<p>Part of the Seven Sisters series, Gateway uses a psychological thriller structure to explore themes of alien contact and human meaning in a way that parallels Hyperion's approach to first contact. The alien architecture at Gateway station is genuinely unsettling in a way that recalls the Time Tombs' relationship to human consciousness. More restrained than Hyperion, but similarly interested in what contact with the truly alien would actually do to human psychology.</p>

''' + key_takeaway_box("The closest thing to Hyperion's combination of philosophical ambition and linked narrative structure is Dune — both books build worlds that function as total systems of meaning and tell stories that couldn't work in any other setting. Start there if you're looking for your next Hyperion.") + "\n\n" + related_links_section([
    ("Best Sci-Fi Books", "best-sci-fi-books.html"),
    ("Books Like Foundation", "books-like-foundation.html"),
    ("Books Like 1984", "books-like-1984.html"),
    ("Browse Sci-Fi Reviews", "category/science-fiction.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Books Like Hyperion by Dan Simmons","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("books-like-hyperion.html", ph1)

# books-like-foundation.html
pf1 = page_template(
    title="Books Like Foundation by Isaac Asimov | Bithues Reading Lab",
    h1="Books Like Foundation by Isaac Asimov",
    description="If you loved Asimov's Foundation, here are the books that capture the same epic scope of civilization-spanning history and psychohistorical prediction.",
    canonical="books-like-foundation.html",
    breadcrumb="books-like-foundation.html",
    hero_label="Similar to Foundation",
    content_html='''<p>Isaac Asimov's Foundation series is one of the most influential works of science fiction ever written — and its influence on subsequent space opera and political SF is incalculable. The premise — a mathematician who predicts the fall of a galactic empire and engineers a plan to reduce the dark ages from 30,000 years to 1,000 — is a thought experiment about whether history can be mathematicized. If you loved it and are looking for more, these are the books that share its ambitions.</p>

<h2>The Galactic Center Saga by Greg Bear</h2>
<p>Bear's series picks up the themes Asimov explored — artificial intelligence, consciousness, the evolution of humanity — and carries them to extremes that Asimov never reached. The direct sequels to Asimov's Foundation (by Bear and others) are themselves worth reading, but Bear's original work (including <em>Psychos</em>, <em>Infinity</em>, and <em>genesis</em>) takes the premise in directions the original author never imagined. Bear's AIs are genuinely alien in a way Asimov's positronic robots never quite achieved.</p>

<h2>A Fire Upon the Deep by Vernor Vinge</h2>
<p>Vinge's universe has zones — the Unthinking Depths where intelligence is limited, the Beyond where faster-than-light travel and superintelligence are possible, and the Transcend with beings of godlike power. The Deep War series that begins with A Fire Upon the Deep uses this structure to tell stories of galactic politics and contact with genuinely incomprehensible intelligences. Like Foundation, it uses scale to make political philosophy concrete.</p>
<p><a href="https://www.amazon.com/dp/0812515307/?tag=bithues-20" rel="nofollow">Buy A Fire Upon the Deep on Amazon →</a></p>

<h2>The Three-Body Problem by Cixin Liu</h2>
<p>Where Foundation is about the predictability of large populations, the Three-Body Problem is about the unpredictability of complex systems — including civilizations. Liu's trilogy spans cosmic time scales while keeping the focus on human decisions and human consequences. The question at its center (what happens when you contact a civilization that has had centuries more time to develop than yours?) parallels Foundation's question about empire and decline.</p>
<p><a href="https://www.amazon.com/dp/0765382032/?tag=bithues-20" rel="nofollow">Buy The Three-Body Problem on Amazon →</a></p>

<h2>Dune by Frank Herbert</h2>
<p>Herbert and Asimov share a commitment to treating political and economic systems as variables in an equation. Dune's analysis of the Fremen's relationship to water, the CHOAM company's relationship to the Emperor, and Paul Atreides's relationship to prophecy — all of this works the same way Foundation's Seldon Crisis analysis does. Both books reward re-reading with new understanding of how the systems interact.</p>
<p><a href="https://www.amazon.com/dp/0441172717/?tag=bithues-20" rel="nofollow">Buy Dune on Amazon →</a></p>

<h2>Hyperion by Dan Simmons</h2>
<p>Simmons's conclusion to the Hyperion Cantos is the most Asimovian thing he ever wrote — an ending that pays off the entire series with the same kind of intellectual satisfaction that Foundation's Seldon Plan delivers. The two series share a willingness to use science fiction as a vehicle for philosophy and to trust readers to follow complex systems. If you want a book that does for you what Foundation did, Hyperion is the closest thing in the SF canon.</p>
<p><a href="https://www.amazon.com/dp/0553283685/?tag=bithues-20" rel="nofollow">Buy Hyperion on Amazon →</a></p>

''' + key_takeaway_box("The best entry point after Foundation is A Fire Upon the Deep — Vinge's zone structure gives you the same sense of galactic scale and his AI characters are genuinely novel. If you want something closer to the civilization-predictability theme, go to The Three-Body Problem.") + "\n\n" + related_links_section([
    ("Best Sci-Fi Books", "best-sci-fi-books.html"),
    ("Books Like Hyperion", "books-like-hyperion.html"),
    ("Books Like The Martian", "books-like-the-martian.html"),
    ("Browse Sci-Fi Reviews", "category/science-fiction.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Books Like Foundation by Isaac Asimov","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("books-like-foundation.html", pf1)

# books-like-1984.html
p84 = page_template(
    title="Books Like 1984 by George Orwell | Bithues Reading Lab",
    h1="Books Like 1984 by George Orwell",
    description="If you read 1984 and felt unsettled — here are the books that go deeper into surveillance, language, truth, and political control.",
    canonical="books-like-1984.html",
    breadcrumb="books-like-1984.html",
    hero_label="Similar to 1984",
    content_html='''<p>1984 is one of those books that stays with you after you put it down — the sensation of having read something true about the nature of political power and the fragility of truth. If you're looking for books that extend that feeling, these are the ones that most directly continue the conversation Orwell started.</p>

<h2>Brave New World by Aldous Huxley</h2>
<p>The classic counterpoint: where Orwell's nightmare is a world of too much control, Huxley's is a world of too much pleasure. Both are dystopias, but Huxley's critique cuts differently — his world has eliminated suffering by eliminating depth, eliminated literature by replacing it with feelies, eliminated love by making it casual and pharmacological. The question Huxley asks: is it better to be oppressed or distracted? It's a more uncomfortable question than Orwell's, partly because we can see elements of both dystopias in our own world.</p>
<p><a href="https://www.amazon.com/dp/0060850523/?tag=bithues-20" rel="nofollow">Buy Brave New World on Amazon →</a></p>

<h2>The Handmaid's Tale by Margaret Atwood</h2>
<p>Atwood has said she didn't want to write anything too obviously similar to 1984 — so she set it in a theocracy rather than a secular surveillance state. But the mechanisms are similar: control of language, control of reproduction, control of women's bodies as a proxy for political power. What makes Atwood's novel particularly resonant in 2026 is how specific its religious-political machinery is — it doesn't feel speculative, it feels like something that could happen.</p>
<p><a href="https://www.amazon.com/dp/0385490816/?tag=bithues-20" rel="nofollow">Buy The Handmaid's Tale on Amazon →</a></p>

<h2>Fahrenheit 451 by Ray Bradbury</h2>
<p>Bradbury's world of book-burning is often taught alongside 1984 as a pair, but it's a different kind of surveillance dystopia. In Bradbury's world, the problem isn't the government surveilling you — it's that people have chosen entertainment over knowledge and don't even know what they're missing. The firemen burning books aren't acting against the people's will; they're acting for them. That's a more disturbing premise than Orwell's, in some ways.</p>
<p><a href="https://www.amazon.com/dp/1451673319/?tag=bithues-20" rel="nofollow">Buy Fahrenheit 451 on Amazon →</a></p>

<h2>The Plot Against America by Philip Roth</h2>
<p>Roth's alternative history asks: what if Charles Lindbergh — who was famously sympathetic to Nazi Germany — had defeated FDR in 1940? What would America look like as a fascist state? The brilliance of Roth's approach is that it's incremental — no single step seems catastrophic, but the accumulation is devastating. It makes Orwell's "but things have always been this bad" despair less available — Roth shows you exactly how it could happen here, one small policy change at a time.</p>

<h2>The Testaments by Margaret Atwood</h2>
<p>Atwood's 2019 sequel to The Handmaid's Tale — which won the Booker Prize — picks up fifteen years after the original ends and provides a resolution that is neither purely hopeful nor purely despairing. It functions as a guide to how repressive regimes can be undermined from within, and its publication circumstances (written in secret, announced at the same time as the US government's attempts to restrict abortion access) made it feel uncannily relevant.</p>

<h2>The Ministry of the Future by Kim Stanley Robinson</h2>
<p>Robinson's novel is set in the near future and focuses on climate change — but its first third is one of the most visceral depictions of what political control looks like when it emerges from democratic mechanisms rather than coups. It's a different kind of surveillance dystopia, one where the controls feel voluntary because people have been trained to accept them. Less directly Orwellian, but similarly unsettling.</p>

''' + key_takeaway_box("The most valuable pairing is 1984 with Brave New World — reading them together shows you two different models of how freedom dies: Orwell's through force and Huxley's through distraction. Knowing both gives you a vocabulary for understanding political manipulation in any era.") + "\n\n" + related_links_section([
    ("Best Sci-Fi Books", "best-sci-fi-books.html"),
    ("Best Fantasy Books", "best-fantasy-books.html"),
    ("Books Like Hyperion", "books-like-hyperion.html"),
    ("Browse Dystopian Reviews", "category/dystopian.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Books Like 1984 by George Orwell","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("books-like-1984.html", p84)

# books-like-the-martian.html
pm = page_template(
    title="Books Like The Martian by Andy Weir | Bithues Reading Lab",
    h1="Books Like The Martian by Andy Weir",
    description="You loved The Martian. Here are the books with the same hard science, survival storytelling, and deadpan problem-solving by protagonists who refuse to give up.",
    canonical="books-like-the-martian.html",
    breadcrumb="books-like-the-martian.html",
    hero_label="Similar to The Martian",
    content_html='''<p>The Martian is a survival story with a science textbook's precision — Mark Watney doesn't just survive, he survives by solving problems with real science. That combination of hard science and human determination is the thing readers return for. Here are the books that deliver the same experience.</p>

<h2>Project Hail Mary by Andy Weir</h2>
<p>The obvious place to start, and the only honest answer if you want more of the same. Rocky the alien and the amnesiac protagonist create a different dynamic than Mark Watney's situation — there's more collaboration and less solo improvisation — but Weir's voice, the hard science, and the problem-solving structure are consistent. If you loved The Martian and haven't read this, stop reading this paragraph and go read it.</p>
<p><a href="https://www.amazon.com/dp/0593135202/?tag=bithues-20" rel="nofollow">Buy Project Hail Mary on Amazon →</a></p>

<h2>Artemis by Andy Weir</h2>
<p>Same author, different setting. The lunar city of Artemis isn't Mars, but the problem-solving approach is identical: Jazz Bashara is a smuggler who gets drawn into a conspiracy and has to use her knowledge of lunar economics and physics to survive. Less polished than The Martian but Weir's voice is so distinctive that even his lesser work is better than most genre fiction.</p>
<p><a href="https://www.amazon.com/dp/1473644178/?tag=bithues-20" rel="nofollow">Buy Artemis on Amazon →</a></p>

<h2>The Moon Is a Harsh Mistress by Robert Heinlein</h2>
<p>Heinlein's 1966 novel is the foundational text for the kind of hard-SF survival-and-improvisation that Weir does. The lunar colonists in Heinlein's book have been making things work with insufficient resources for generations — and when they decide to push for independence, they do it with physics and political philosophy in equal measure. If you want the intellectual satisfaction of watching someone figure out how to make a thrown object navigate a gravitational gradient, this is the book.</p>
<p><a href="https://www.amazon.com/dp/0345407910/?tag=bithues-20" rel="nofollow">Buy The Moon Is a Harsh Mistress on Amazon →</a></p>

<h2>Nuclear War Survival Skills by Cresson H. Kearney</h2>
<p>Wait — this is a non-fiction manual, not a novel. But if what you loved about The Martian was the specific pleasure of watching a character solve a physics problem with limited resources, this book (freely available from the Oregon Institute of Science and Medicine) provides that pleasure continuously. It's a compendium of survival skills developed for nuclear war scenarios, and it's written for a non-specialist audience. Not for everyone, but if the physics problem-solving in The Martian was what hooked you, this will keep you occupied for a long time.</p>

<h2>The Dark Forest by Cixin Liu (Book 2 of Three-Body Problem Trilogy)</h2>
<p>Not survival fiction in the individual sense, but the second book in Liu's trilogy contains sequences of survival against impossible odds that rival anything in Weir's work. The "wallfacer" concept — where each strategy to defeat the alien sophons is devised in complete secrecy, making every action feel like a chess move in a game whose rules you don't fully understand — has the same intellectual satisfaction as watching Watney solve his oxygen problem. Different scale, but same pleasure.</p>
<p><a href="https://www.amazon.com/dp/0765382032/?tag=bithues-20" rel="nofollow">Buy The Dark Forest on Amazon →</a></p>

<h2>The Left Hand of Darkness by Ursula K. Le Guin</h2>
<p>Le Guin's novel has a different texture than Weir's — it's slower, more contemplative, and more interested in politics than survival mechanics. But Genly Ai's journey across Gethen, surviving political environments he doesn't understand using cultural intelligence and patience, offers a different kind of problem-solving satisfaction. If you want the travel-and-survive-in-an-alien-culture experience, this is where to find it.</p>
<p><a href="https://www.amazon.com/dp/0441478125/?tag=bithues-20" rel="nofollow">Buy The Left Hand of Darkness on Amazon →</a></p>

''' + key_takeaway_box("The only real answer to 'I want more The Martian' is 'read Project Hail Mary' — it's the same thing, done even better. After that, The Moon Is a Harsh Mistress is the book with the most similar intellectual DNA, even if it doesn't read like a thriller the way Weir's books do.") + "\n\n" + related_links_section([
    ("Best Sci-Fi Books", "best-sci-fi-books.html"),
    ("Books Like Project Hail Mary", "books-like-project-hail-mary.html"),
    ("Browse Sci-Fi Reviews", "category/science-fiction.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Books Like The Martian by Andy Weir","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("books-like-the-martian.html", pm)

# books-like-psychology-of-money.html
ppm = page_template(
    title="Books Like The Psychology of Money by Morgan Housel | Bithues Reading Lab",
    h1="Books Like The Psychology of Money by Morgan Housel",
    description="You loved The Psychology of Money. Here are the books that go deeper into financial behavior, wealth psychology, and the stories we tell ourselves about money.",
    canonical="books-like-psychology-of-money.html",
    breadcrumb="books-like-psychology-of-money.html",
    hero_label="Similar to The Psychology of Money",
    content_html='''<p>Morgan Housel's <em>The Psychology of Money</em> is one of those rare books that changes how you think permanently rather than temporarily. Its central insight — that financial decisions are made on the basis of personal history, emotion, and identity, not spreadsheets — is a lens that once you have it, you can't unsee. Here are the books that extend or complement that insight in different directions.</p>

<h2>The Millionaire Next Door by Thomas Stanley and William Danko</h2>
<p>Stanley and Danko spent decades studying how wealthy people actually live — not the flashy consumption symbols but the actual data of wealth accumulation. Their key finding: most people who look wealthy aren't, and most people who are actually wealthy don't look it. The affluent don't buy the cars and houses you'd expect. They live below their means, invest consistently, and have accumulated wealth through decades of compounding. It's a book that makes you rethink what "being rich" actually means.</p>
<p><a href="https://www.amazon.com/dp/0671535035/?tag=bithues-20" rel="nofollow">Buy The Millionaire Next Door on Amazon →</a></p>

<h2>Thinking, Fast and Slow by Daniel Kahneman</h2>
<p>The intellectual foundation for Housel's approach — and the most important book in the broader field of behavioral economics. Kahneman's dual-system framework (System 1: fast, automatic, intuitive; System 2: slow, deliberate, analytical) explains why people make predictably irrational financial decisions. Where Housel uses anecdotes to make this accessible, Kahneman shows you the underlying research. Essential reading for anyone who wants to understand why they make the money decisions they make.</p>
<p><a href="https://www.amazon.com/dp/0374533555/?tag=bithues-20" rel="nofollow">Buy Thinking, Fast and Slow on Amazon →</a></p>

<h2>The Bogleheads' Guide to Investing by Taylor Larimore, Mel Lindauer & Michael LeBoeuf</h2>
<p>If Housel's book made you realize that the financial industry's incentives are often misaligned with your own financial interests, the Bogleheads guide is the practical follow-up. Built on the philosophy of Vanguard founder John Bogle, it's a comprehensive guide to index fund investing — not as a compromise, but as the optimal strategy for most individual investors. The book's philosophy: stop trying to beat the market and start participating in it systematically.</p>

<h2>Your Money or Your Brain by Jason Zweig</h2>
<p>Zweig translates behavioral finance research into practical investment guidance — specifically, he addresses the question of why smart people make predictably bad investment decisions. His key contribution is showing how emotions are the biggest risk to your portfolio, not market volatility. The book includes a "risk questionnaire" that actually works — it helps you understand your own relationship to risk in a way that most financial questionnaires don't.</p>

<h2>A Random Walk Down Wall Street by Burton Malkiel</h2>
<p>The definitive argument for passive index fund investing, originally published in 1973 and updated regularly since. Malkiel's "random walk" hypothesis — the idea that asset prices move in unpredictable ways that cannot be consistently forecasted — is backed by extensive historical data. The book is also useful because it explains what it doesn't claim: that markets are perfectly efficient (they aren't) or that active management never works (sometimes it does). It's an honest book, which is rare in the personal finance genre.</p>

<h2>I Will Teach You to Be Rich by Ramit Sethi</h2>
<p>Sethi's approach is more prescriptive and action-oriented than Housel's — he gives you specific scripts for automating your finances, negotiating your salary, and optimizing your credit cards. Where Housel is interested in the psychology of money, Sethi is interested in the mechanics. His 6-week "I Will Teach You to Be Rich" program has practical infrastructure value that the more philosophical Psychology of Money doesn't offer.</p>
<p><a href="https://www.amazon.com/dp/0761147489/?tag=bithues-20" rel="nofollow">Buy I Will Teach You to Be Rich on Amazon →</a></p>

<h2>The Behavior Gap by Carl Richards</h2>
<p>Richards is a financial planner who draws simple diagrams — literally with a pen — to explain financial concepts. His book is a series of short essays about the gap between what people know they should do and what they actually do. His key insight: it's not about information, it's about behavior. Most people who are bad with money know what they should be doing. They just don't do it. Understanding why is the actual problem, and that's what this book focuses on.</p>

''' + key_takeaway_box("Read Thinking, Fast and Slow after The Psychology of Money — it gives you the research foundation behind Housel's anecdotes. Then read The Millionaire Next Door to understand what actual wealth accumulation looks like in practice. That three-book sequence will give you a complete framework for thinking about money.") + "\n\n" + related_links_section([
    ("Best Books About Money", "best-books-about-money.html"),
    ("Best Self-Help Books", "best-self-help-books.html"),
    ("Browse Nonfiction Reviews", "category/nonfiction.html"),
]),
    schema='{"@context":"https://schema.org","@type":"Article","headline":"Books Like The Psychology of Money by Morgan Housel","author":{"@type":"Organization","name":"Bithues Reading Lab"},"datePublished":"2026-04-15","dateModified":"2026-04-15"}'
)
save("books-like-psychology-of-money.html", ppm)

print("\n=== All done! ===")