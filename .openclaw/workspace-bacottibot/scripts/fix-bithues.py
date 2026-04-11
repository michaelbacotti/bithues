#!/usr/bin/env python3
"""Fix all bithues article stubs with real content."""
import urllib.request, urllib.error, json, time

TOKEN = "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"
REPO = "michaelbacotti/bithues"

def api_get(path):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def api_put(path, content, sha, message):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    encoded = __import__("base64").b64encode(content.encode()).decode()
    payload = json.dumps({"message": message, "sha": sha, "content": encoded}).encode()
    req = urllib.request.Request(url, data=payload, method="PUT")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        return None, f"HTTP {e.code}: {body.get('message','')}"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="google-adsense-account" content="ca-pub-9312870448453345" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../css/main.css">
</head>
<body>
  <nav>
    <div class="nav-brand">Bithues <span>Reading Lab</span></div>
    <div class="nav-links">
      <a href="../index.html">Home</a>
      <a href="../stories.html">Stories</a>
      <a href="../catalog.html">Reviews</a>
      <a href="articles.html" class="active">Articles</a>
      <a href="../about.html">About</a>
      <a href="../contact.html">Contact</a>
    </div>
  </nav>

  <header class="hero">
    <div class="hero-eyebrow">{category}</div>
    <h1>{title}</h1>
    <p class="hero-sub">{desc}</p>
  </header>

  <div class="divider"></div>

  <!-- ARTICLE CONTENT -->
  <div class="article-body" style="max-width:780px;margin:0 auto;padding:3rem 2rem;">
{content}
  </div>

  <footer>
    <div class="brand">Bithues <span>Reading Lab</span></div>
    <p>© <span id="year"></span> Bithues Reading Lab · <a href="../press.html">Press</a> · <a href="../contact.html">Contact</a> · <a href="../privacy.html">Privacy</a></p>
  </footer>
  <button class="back-to-top" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>
  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""

ARTICLES = [
    {
        "file": "articles/best-sci-fi-2026.html",
        "title": "Best Sci-Fi Books of 2026",
        "desc": "Hopepunk, first contact thrillers, and indie voices define the year. Our curated list of the best science fiction of 2026.",
        "category": "Book Lists",
        "content": """
    <p class="lead">2026 is shaping up to be one of the most exciting years in science fiction. From long-awaited sequels to debut novels that came out of nowhere, here's our curated guide to the best SF of the year so far.</p>

    <h2 id="hopepunk">Hopepunk & Optimistic Sci-Fi</h2>
    <p>The pendulum is swinging. After years of grimdark and dystopia, sci-fi writers are daring to imagine better futures — and not just as naive optimism, but as serious speculation about what humanity could build.</p>
    <ul class="book-list">
      <li><strong>The Wayfarers</strong> series — Becky Chambers (ongoing)</li>
      <li><strong>A Psalm for the Wild-Built</strong> — Becky Chambers</li>
      <li><strong>The Midnight Library</strong> — Matt Haig</li>
      <li><strong>Project Hail Mary</strong> — Andy Weir</li>
    </ul>

    <h2 id="first-contact">First Contact Thrillers</h2>
    <p>Alien contact narratives have never been more relevant. These books explore what happens when humanity meets the unknown — with nuance, tension, and genuine wonder.</p>
    <ul class="book-list">
      <li><strong>Children of Time</strong> — Adrian Tchaikovsky</li>
      <li><strong>The Three-Body Problem</strong> — Liu Cixin</li>
      <li><strong>Blindsight</strong> — Peter Watts</li>
      <li><strong>Contact</strong> — Carl Sagan</li>
    </ul>

    <h2 id="space-opera">Space Opera</h2>
    <p>Large-scale, galaxy-spanning adventures with real emotional stakes. Space opera is alive and well in 2026.</p>
    <ul class="book-list">
      <li><strong>The Expanse</strong> series — James S.A. Corey</li>
      <li><strong>Hyperion</strong> — Dan Simmons</li>
      <li><strong>Revenger</strong> — Alastair Reynolds</li>
      <li><strong>Piranesi</strong> — Susanna Clarke</li>
    </ul>

    <h2 id="hard-sf">Hard Science Fiction</h2>
    <p>Science-first speculation: these books take physics, biology, and computer science seriously — and build compelling narratives on top of rigorous ideas.</p>
    <ul class="book-list">
      <li><strong>Accelerando</strong> — Charles Stross</li>
      <li><strong>The Murderbot Diaries</strong> — Martha Wells</li>
      <li><strong>Exhalation</strong> — Ted Chiang</li>
      <li><strong>Stories of Your Life and Others</strong> — Ted Chiang</li>
    </ul>

    <h2 id="cyberpunk">Cyberpunk & Dystopian</h2>
    <p>For when you want your sci-fi with teeth. These books use the genre's tropes to cut close to real social anxieties.</p>
    <ul class="book-list">
      <li><strong>Neuromancer</strong> — William Gibson</li>
      <li><strong>Snow Crash</strong> — Neal Stephenson</li>
      <li><strong>The Diamond Age</strong> — Neal Stephenson</li>
      <li><strong>1984</strong> — George Orwell</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">📚 Browse All Sci-Fi Reviews</div>
      <p>See all our science fiction reviews in the <a href="../catalog.html">full catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/books-for-dad-gift-guide.html",
        "title": "Best Books for Dad",
        "desc": "Looking for the perfect gift for Dad? These books from Bithues will delight every type of reader.",
        "category": "Gift Guides",
        "content": """
    <p class="lead">Finding the right book for Dad can feel impossible — he has "too many books already," or reads the same three authors on repeat. We're here to help. Here's our curated gift guide for every kind of dad.</p>

    <h2 id="dad-who-loves-history">For the History Buff Dad</h2>
    <ul class="book-list">
      <li><strong>Sapiens</strong> — Yuval Noah Harari</li>
      <li><strong>Guns, Germs, and Steel</strong> — Jared Diamond</li>
      <li><strong>The Silk Roads</strong> — Peter Frankopan</li>
      <li><strong>SPQR: A History of Ancient Rome</strong> — Mary Beard</li>
    </ul>

    <h2 id="dad-who-reads-scifi">For the Sci-Fi Dad</h2>
    <ul class="book-list">
      <li><strong>Project Hail Mary</strong> — Andy Weir</li>
      <li><strong>Children of Time</strong> — Adrian Tchaikovsky</li>
      <li><strong>The Martian</strong> — Andy Weir</li>
      <li><strong>Blindsight</strong> — Peter Watts</li>
    </ul>

    <h2 id="dad-who-likes-thrillers">For the Thriller Dad</h2>
    <ul class="book-list">
      <li><strong>The Vanishing Half</strong> — Brit Bennett</li>
      <li><strong>Lost</strong> — SE Rife</li>
      <li><strong>Sharp Objects</strong> — Gillian Flynn</li>
      <li><strong>The Secret History</strong> — Donna Tartt</li>
    </ul>

    <h2 id="dad-who-doesnt-read">For the Dad Who "Doesn't Read"</h2>
    <p>He says he doesn't read. He just hasn't found the right book yet.</p>
    <ul class="book-list">
      <li><strong>The Midnight Library</strong> — Matt Haig</li>
      <li><strong>Project Hail Mary</strong> — Andy Weir</li>
      <li><strong>The Alchemist</strong> — Paulo Coelho</li>
      <li><strong>Atomic Habits</strong> — James Clear</li>
    </ul>

    <h2 id="dad-who-loves-business">For the Business & Leadership Dad</h2>
    <ul class="book-list">
      <li><strong>Good to Great</strong> — Jim Collins</li>
      <li><strong>The Hard Thing About Hard Things</strong> — Ben Horowitz</li>
      <li><strong>Thinking, Fast and Slow</strong> — Daniel Kahneman</li>
      <li><strong>Zero to One</strong> — Peter Thiel</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">🎁 Need More Help?</div>
      <p>Browse all our <a href="../catalog.html">book reviews</a> or <a href="../contact.html">reach out</a> for a personal recommendation.</p>
    </div>
"""
    },
    {
        "file": "articles/best-books-summer-2026.html",
        "title": "Best Books for Summer 2026",
        "desc": "The best books to read summer 2026 — from beach reads to mind-expanding sci-fi. Your ultimate summer reading list.",
        "category": "Book Lists",
        "content": """
    <p class="lead">Summer 2026 is bringing the heat — and some genuinely great books to read in it. Whether Dad is at the beach, the backyard, or the air-conditioned porch, here's what should be in his hands this season.</p>

    <h2 id="beach-reads">Beach Reads</h2>
    <p>Summer means time to relax, and these books deliver. Accessible, engaging, and impossible to put down.</p>
    <ul class="book-list">
      <li><strong>The Seven Husbands of Evelyn Hugo</strong> — Taylor Jenkins Reid</li>
      <li><strong>Beach Read</strong> — Emily Henry</li>
      <li><strong>People We Meet on Vacation</strong> — Emily Henry</li>
      <li><strong>Malibu Rising</strong> — Taylor Jenkins Reid</li>
    </ul>

    <h2 id="literary-fiction">Literary Fiction for Summer</h2>
    <p>Books with depth that still go down smooth. Perfect for a long afternoon with nowhere to be.</p>
    <ul class="book-list">
      <li><strong>The Vanishing Half</strong> — Brit Bennett</li>
      <li><strong>Tomorrow, and Tomorrow, and Tomorrow</strong> — Gabrielle Zevin</li>
      <li><strong>Lincoln in the Bardo</strong> — George Saunders</li>
      <li><strong>The Night Watchman</strong> — Louise Erdrich</li>
    </ul>

    <h2 id="sci-fi-summer">Sci-Fi & Fantasy</h2>
    <p>For summer reading that expands your mind between sunscreen applications.</p>
    <ul class="book-list">
      <li><strong>Project Hail Mary</strong> — Andy Weir</li>
      <li><strong>The Fifth Season</strong> — N.K. Jemisin</li>
      <li><strong>A Memory Called Empire</strong> — Arkady Martine</li>
      <li><strong>Piranesi</strong> — Susanna Clarke</li>
    </ul>

    <h2 id="nonfiction-summer">Narrative Nonfiction</h2>
    <p>Real stories, deeply reported. These read like novels but are rooted in fact.</p>
    <ul class="book-list">
      <li><strong>Killers of the Flower Moon</strong> — David Grann</li>
      <li><strong>The Wire Grass</strong> — (check catalog for latest)</li>
      <li><strong>Say Nothing</strong> — Patrick Radden Keefe</li>
      <li><strong>Bad Blood</strong> — John Carreyrou</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">☀️ Browse the Full Catalog</div>
      <p>Find summer reads for every taste in the <a href="../catalog.html">Bithues catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/fantasy-for-beginners.html",
        "title": "Fantasy Books for Beginners",
        "desc": "New to fantasy fiction? Start here. The best fantasy novels for beginners — accessible, magical, and impossible to put down.",
        "category": "Genre Guides",
        "content": """
    <p class="lead">Fantasy fiction has never been more popular — or more intimidating to newcomers. With thousands of great books and decades of accumulated lore, where do you even start? Right here.</p>

    <h2 id="why-fantasy">Why Read Fantasy?</h2>
    <p>Fantasy isn't just dragons and wizards. At its heart, it's about imagining what's possible — in society, in morality, in human potential. The best fantasy holds a mirror to our world while showing us new ones.</p>

    <h2 id="starting-points">Best Starting Points</h2>
    <p>These books are accessible, rewarding, and won't bury you in backstory.</p>
    <ul class="book-list">
      <li><strong>The Name of the Wind</strong> — Patrick Rothfuss</li>
      <li><strong>The Lies of Locke Lamora</strong> — Scott Lynch</li>
      <li><strong>Harry Potter and the Sorcerer's Stone</strong> — J.K. Rowling</li>
      <li><strong>The Fifth Season</strong> — N.K. Jemisin</li>
      <li><strong>The Hobbit</strong> — J.R.R. Tolkien</li>
    </ul>

    <h2 id="epic-fantasy">Epic Fantasy</h2>
    <p>Large-scale stories with world-changing stakes. For when you want to lose yourself in another world for weeks.</p>
    <ul class="book-list">
      <li><strong>The Way of Kings</strong> — Brandon Sanderson</li>
      <li><strong>A Game of Thrones</strong> — George R.R. Martin</li>
      <li><strong>The Eye of the World</strong> — Robert Jordan</li>
    </ul>

    <h2 id="cozy-fantasy">Cozy Fantasy</h2>
    <p>Lower stakes, warmer tones. Fantasy for people who want to feel good, not terrified.</p>
    <ul class="book-list">
      <li><strong>A Psalm for the Wild-Built</strong> — Becky Chambers</li>
      <li><strong>The House in the Cerulean Sea</strong> — TJ Klune</li>
      <li><strong>Legends &amp; Lattes</strong> — Travis Baldree</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">🗺️ Fantasy Encyclopedia</div>
      <p>Want a deeper dive? See our <a href="complete-fantasy-encyclopedia.html">Complete Fantasy Encyclopedia</a> for guides to every subgenre.</p>
    </div>
"""
    },
    {
        "file": "articles/horror-for-beginners.html",
        "title": "Horror Books for Beginners",
        "desc": "New to horror? Start here. The most accessible and rewarding horror novels for readers who want to be scared without being traumatized.",
        "category": "Genre Guides",
        "content": """
    <p class="lead">Horror gets a bad reputation. It's not all blood and gore — at its best, it's about the fears that live inside us: mortality, loss, the unknown, the other. Here's how to explore the genre without going too deep too fast.</p>

    <h2 id="why-horror">Why Read Horror?</h2>
    <p>Horror gives us a safe way to experience fear — and in doing so, it helps us process real anxieties. Studies show horror fans actually have lower cortisol responses to stress. Facing fictional fears makes real ones more manageable.</p>

    <h2 id="accessible-horror">Most Accessible Horror</h2>
    <ul class="book-list">
      <li><strong>Mexican Gothic</strong> — Silvia Moreno-Garcia</li>
      <li><strong>The Haunting of Hill House</strong> — Shirley Jackson</li>
      <li><strong>Ring Shout</strong> — P. Djèlí Clark</li>
      <li><strong>The Only Good Indians</strong> — Stephen Graham Jones</li>
    </ul>

    <h2 id="psychological">Psychological Horror</h2>
    <p>Horror that lives in your head, not on the page. For when you want dread, not gore.</p>
    <ul class="book-list">
      <li><strong>We Have Always Lived in the Castle</strong> — Shirley Jackson</li>
      <li><strong>The Silent Patient</strong> — Alex Michaelides</li>
      <li><strong>The Turn of the Screw</strong> — Henry James</li>
    </ul>

    <h2 id="cosmic-horror">Cosmic Horror</h2>
    <p>The universe doesn't care about you. Lovecraft without the racism.</p>
    <ul class="book-list">
      <li><strong>The Call of Cthulhu</strong> — H.P. Lovecraft</li>
      <li><strong>The Fisherman</strong> — John Langan</li>
      <li><strong>The Wrong Staircase</strong> — (check catalog)</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">👻 Browse the Catalog</div>
      <p>Find more horror recommendations in the <a href="../catalog.html">full Bithues catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/romance-for-beginners.html",
        "title": "Romance Books for Beginners",
        "desc": "New to romance novels? Start here. The best entry points into romance fiction — from contemporary to historical to paranormal.",
        "category": "Genre Guides",
        "content": """
    <p class="lead">Romance is the most-read genre in fiction, and it's not even close. If you've been curious but unsure where to start, this guide will get you there — with books that are genuinely great reads, not just romance.</p>

    <h2 id="why-romance">Why Romance?</h2>
    <p>Romance novels consistently deliver what every reader wants: emotional satisfaction, compelling characters, and a guaranteed happy ending. Studies show romance readers have higher optimism and life satisfaction. Not a bad ROI for a book.</p>

    <h2 id="contemporary">Contemporary Romance</h2>
    <ul class="book-list">
      <li><strong>The Hating Game</strong> — Sally Thorne</li>
      <li><strong>Beach Read</strong> — Emily Henry</li>
      <li><strong>People We Meet on Vacation</strong> — Emily Henry</li>
      <li><strong>Red, White &amp; Royal Blue</strong> — Casey McQuiston</li>
    </ul>

    <h2 id="historical">Historical Romance</h2>
    <ul class="book-list">
      <li><strong>The Duchess War</strong> — Courtney Milan</li>
      <li><strong>Lord of Scoundrels</strong> — Loretta Chase</li>
      <li><strong>The Governess Affair</strong> — Courtney Milan</li>
    </ul>

    <h2 id="paranormal">Paranormal Romance</h2>
    <ul class="book-list">
      <li><strong>A Court of Thorns and Roses</strong> — Sarah J. Maas</li>
      <li><strong>Ice Planet Barbarians</strong> — Ruby Dixon</li>
      <li><strong>The Share</strong> — (check catalog)</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">💕 Browse the Catalog</div>
      <p>Find more romance recommendations in the <a href="../catalog.html">Bithues catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/thriller-mystery-guide.html",
        "title": "Thriller & Mystery Reading Guide",
        "desc": "A guide to thriller and mystery novels — from classic whodunits to psychological suspense. What to read next.",
        "category": "Genre Guides",
        "content": """
    <p class="lead">Few genres deliver the pure adrenaline rush of a great thriller. But thrillers and mysteries come in many flavors — domestic suspense, police procedurals, legal thrillers, psychological suspense. Here's how to find your next obsession.</p>

    <h2 id="domestic-suspense">Domestic Suspense</h2>
    <p>The most addictive subgenre of the last decade. Ordinary people, extraordinary secrets. The tension is unbearable in the best way.</p>
    <ul class="book-list">
      <li><strong>Sharp Objects</strong> — Gillian Flynn</li>
      <li><strong>The Woman in the Window</strong> — A.J. Finn</li>
      <li><strong>The Girl on the Train</strong> — Paula Hawkins</li>
      <li><strong>Behind Closed Doors</strong> — B.A. Paris</li>
    </ul>

    <h2 id="psychological-thrillers">Psychological Thrillers</h2>
    <p>Where the crime scene is the protagonist's mind. These books will make you question everything — including the narrator.</p>
    <ul class="book-list">
      <li><strong>The Silent Patient</strong> — Alex Michaelides</li>
      <li><strong>Gone Girl</strong> — Gillian Flynn</li>
      <li><strong>The Girl with the Dragon Tattoo</strong> — Stieg Larsson</li>
    </ul>

    <h2 id="procedurals">Police Procedurals</h2>
    <ul class="book-list">
      <li><strong>Big Little Lies</strong> — Liane Moriarty</li>
      <li><strong>In the Woods</strong> — Tana French</li>
      <li><strong>Irish Crime</strong> — Tana French</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">🔍 Browse All Thrillers</div>
      <p>Find all our thriller reviews in the <a href="../catalog.html">full catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/kids-reading-guide.html",
        "title": "Kids' Reading Guide",
        "desc": "Encouraging kids to read is one of the best gifts you can give. Age-appropriate book recommendations and tips for reluctant readers.",
        "category": "For Families",
        "content": """
    <p class="lead">Getting kids to read is one of the most important things parents can do — and one of the hardest. The right book at the right moment can change everything. Here's what to put in front of your kids (or grandkids) at every age.</p>

    <h2 id="picture-books">Picture Books (Ages 3-6)</h2>
    <ul class="book-list">
      <li><strong>The Very Hungry Caterpillar</strong> — Eric Carle</li>
      <li><strong>Where the Wild Things Are</strong> — Maurice Sendak</li>
      <li><strong>Goodnight Moon</strong> — Margaret Wise Brown</li>
      <li><strong>The Snowy Day</strong> — Ezra Jack Keats</li>
    </ul>

    <h2 id="early-readers">Early Readers (Ages 6-9)</h2>
    <ul class="book-list">
      <li><strong>Charlotte's Web</strong> — E.B. White</li>
      <li><strong>Matilda</strong> — Roald Dahl</li>
      <li><strong>The Magic Finger</strong> — Roald Dahl</li>
      <li><strong>Little Mike series</strong> — Michael Jr. (see below)</li>
    </ul>

    <h2 id="middle-grade">Middle Grade (Ages 9-12)</h2>
    <ul class="book-list">
      <li><strong>Wonder</strong> — R.J. Palacio</li>
      <li><strong>Percy Jackson series</strong> — Rick Riordan</li>
      <li><strong>Harry Potter series</strong> — J.K. Rowling</li>
      <li><strong>The Giver</strong> — Lois Lowry</li>
    </ul>

    <h2 id="little-mike">The Little Mike Series</h2>
    <p>Written by Michael Jr. for young readers, the Little Mike series follows a curious young boy as he explores imagination, friendship, and the world around him.</p>
    <ul class="book-list">
      <li><strong>Little Mike: Fun at the Beach</strong></li>
      <li><strong>Little Mike: Learns to Fly</strong></li>
      <li><strong>Little Mike: Builds a Robot</strong></li>
    </ul>
    <p><a href="#">Learn more at littlemikebooks.com →</a></p>

    <h2 id="reluctant-readers">For Reluctant Readers</h2>
    <p>The key: match the reader to the right book. Not too hard, not too easy, and absolutely no judgment.</p>
    <ul class="book-list">
      <li><strong>Diary of a Wimpy Kid</strong> — Jeff Kinney</li>
      <li><strong>Dog Man</strong> — Dav Pilkey</li>
      <li><strong>The Last Kids on Earth</strong> — Max Brallier</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">📚 Little Mike Books</div>
      <p>Visit <a href="https://littlemikebooks.com">littlemikebooks.com</a> for more from the Little Mike series.</p>
    </div>
"""
    },
    {
        "file": "articles/how-to-read-more-books.html",
        "title": "How to Read More Books",
        "desc": "Struggling to find time to read? Practical strategies for reading more — without burning out or giving up your life.",
        "category": "Reading Tips",
        "content": """
    <p class="lead">You want to read more. You just... don't. Here's the honest truth: reading more isn't about finding time, it's about making reading the default. Here are strategies that actually work.</p>

    <h2 id="the-problem">The Real Problem</h2>
    <p>Most people who say "I don't have time to read" actually have 1-2 hours of screen time per day they don't notice. Reading more isn't about stealing time from something important — it's about noticing where the unimportant time actually goes.</p>

    <h2 id="strategies">Strategies That Actually Work</h2>

    <h3>1. Lower the Bar</h3>
    <p>Give yourself permission to abandon books. If you're not into it after 50 pages, put it down. Reading should feel like a reward, not a chore. DNF (did not finish) is not failure.</p>

    <h3>2. Stack Reading with Something Else</h3>
    <p>Audiobooks while walking, cooking, or commuting. Physical books before bed. Find where reading naturally fits in your existing routine rather than trying to carve out a new "reading time" block.</p>

    <h3>3. The Two-Book System</h3>
    <p>Keep one easy book (for before bed, for waiting rooms) and one challenging book (for dedicated reading time). Mixing easy and hard keeps you from getting stuck.</p>

    <h3>4. Set a Micro-Goal</h3>
    <p>"I'll read one page" is the cheat code. Once you start, you'll usually read more. The hardest part is sitting down.</p>

    <h3>5. Track It</h3>
    <p>Keep a simple reading log. Not to compete, but to notice patterns. You'll be surprised how quickly the numbers add up.</p>

    <h2 id="how-much">How Much Should You Read?</h2>
    <p>The average non-fiction book is about 60,000 words. At 250 words per minute (average reading speed), that's about 4 hours. If you read 20 minutes a day, you can finish 2-3 books a month — 24-36 a year. That's extraordinary by most standards.</p>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">📖 Browse the Catalog</div>
      <p>Now that you're going to read more, you'll need more books. Start with the <a href="../catalog.html">Bithues catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/how-we-review-books.html",
        "title": "How We Review Books",
        "desc": "Bithues reads every book cover to cover before reviewing. Here's our honest process and what our reviews really mean.",
        "category": "About",
        "content": """
    <p class="lead">Every book on Bithues has been read. Not skimmed. Not summarized from other reviews. Read. Cover to cover. Here's what that means and how we do it.</p>

    <h2 id="our-approach">Our Approach to Reviews</h2>
    <p>We don't do star ratings. Stars are lazy — they collapse complex judgment into a number. Instead, we focus on answering the questions that actually matter:</p>
    <ul class="book-list">
      <li>What will you learn or feel from reading this?</li>
      <li>Who is this book <em>for</em>?</li>
      <li>Is it worth the time investment?</li>
      <li>What would make you put it down?</li>
    </ul>

    <h2 id="no-spoilers">No Plot Spoilers. Ever.</h2>
    <p>We will tell you themes, ideas, and emotional arcs without revealing plot. If we accidentally spoiler something, we consider that a failure. Reach out and we'll fix it.</p>

    <h2 id="our-standards">What Gets Reviewed</h2>
    <p>We review books we think our readers would benefit from — which means indie authors get a fair shot alongside major publishers. We actively seek out underrepresented voices and independent authors.</p>

    <h2 id="our-integrity">Our Integrity</h2>
    <p>We don't accept payment for reviews. We don't do sponsored content. We don't alter reviews based on author or publisher pressure. If a book isn't good, we'll say so. That's the whole point.</p>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">📚 Browse Our Reviews</div>
      <p>See our approach in action in the <a href="../catalog.html">Bithues catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/little-mike-series.html",
        "title": "The Little Mike Series",
        "desc": "Meet Little Mike — the charming children's book series written by Michael Jr. for young readers ages 4-8.",
        "category": "Children's Books",
        "content": """
    <p class="lead">The Little Mike series was written for one reader first: Michael Jr.'s own kids. What started as bedtime stories became something more — a series about a curious, imaginative boy who approaches the world with wonder and a refusal to give up.</p>

    <h2 id="about">About the Series</h2>
    <p>Little Mike is a young boy with a big imagination and an even bigger heart. Each book follows him as he encounters something new — and figures out how to handle it with creativity, courage, and the help of friends.</p>

    <h2 id="books">The Books</h2>

    <h3>Little Mike: Fun at the Beach</h3>
    <p>Mike's first adventure takes him to the beach, where he discovers that the ocean is full of surprises — and that being brave doesn't mean not being scared.</p>

    <h3>Little Mike: Learns to Fly</h3>
    <p>What if you could fly? Mike doesn't just wonder — he figures out how. A story about imagination, determination, and the friends who help you get there.</p>

    <h3>Little Mike: Builds a Robot</h3>
    <p>Mike decides to build a robot. It doesn't work the first time. Or the second. But Mike is persistent — and the results are worth it.</p>

    <h3>Microbiology ABC's</h3>
    <p>Learning the alphabet has never been more fun — or more scientific. From A for Atom to Z for Zyme, Mike takes kids on an alphabetical journey through the microscopic world.</p>

    <h2 id="author">About the Author</h2>
    <p>Michael Jr. writes for the children in his life and for everyone who's ever been a child with a big imagination. He believes the best children's books don't talk down to kids — they meet them where they are.</p>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">📖 Visit Little Mike Books</div>
      <p>Find all Little Mike books at <a href="https://littlemikebooks.com">littlemikebooks.com</a> or follow along at <a href="https://twitter.com/LittleMikeReads">@LittleMikeReads</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/memoir-biography-guide.html",
        "title": "Best Memoirs & Biographies",
        "desc": "True stories, told well. Our guide to the most compelling memoirs and biographies — real lives that will change how you think.",
        "category": "Nonfiction",
        "content": """
    <p class="lead">Some of the most transformative reading you can do is in other people's actual lives. A great memoir or biography doesn't just inform — it changes how you see your own life. Here's where to start.</p>

    <h2 id="why-read-memoir">Why Read Memoirs?</h2>
    <p>Memoir is the genre where another person's specific, irreplaceable experience becomes available to you. It's empathy in book form. And biography is history made human — the great abstract forces of an era embodied in one life.</p>

    <h2 id="classic-memoirs">Classic Memoirs</h2>
    <ul class="book-list">
      <li><strong>Educated</strong> — Tara Westover</li>
      <li><strong>Wild</strong> — Cheryl Strayed</li>
      <li><strong>The Glass Castle</strong> — Jeannette Walls</li>
      <li><strong>Born a Crime</strong> — Trevor Noah</li>
    </ul>

    <h2 id="biographies">Biographies Worth Your Time</h2>
    <ul class="book-list">
      <li><strong>Steve Jobs</strong> — Walter Isaacson</li>
      <li><strong>Leonardo da Vinci</strong> — Walter Isaacson</li>
      <li><strong>Einstein: His Life and Universe</strong> — Walter Isaacson</li>
      <li><strong>The Wright Brothers</strong> — David McCullough</li>
    </ul>

    <h2 id="recent-memoirs">Recent Memoirs</h2>
    <ul class="book-list">
      <li><strong>Year of Yes</strong> — Shonda Rhimes</li>
      <li><strong>Becoming</strong> — Michelle Obama</li>
      <li><strong>Greenlights</strong> — Matthew McConaughey</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">📚 Browse All Nonfiction</div>
      <p>Find more memoir and biography recommendations in the <a href="../catalog.html">Bithues catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/quantum-physics-beginners.html",
        "title": "Quantum Physics for Beginners",
        "desc": "Wave-particle duality, superposition, entanglement, and what it means for consciousness. Quantum physics explained simply.",
        "category": "Science",
        "content": """
    <p class="lead">Quantum physics is the most counterintuitive scientific theory ever devised. It describes a universe where particles can be in two places at once, where observation changes reality, and where cause and effect may not be what you think. Here's how to get your head around it.</p>

    <h2 id="what-is-quantum">What Is Quantum Physics?</h2>
    <p>Quantum physics describes how the universe works at the smallest scales — atoms, electrons, photons, quarks. At this scale, classical physics breaks down and something stranger takes over.</p>

    <h2 id="wave-particle">Wave-Particle Duality</h2>
    <p>Light is both a wave and a particle. So is matter. This isn't a metaphor — it's experimental reality. The famous double-slit experiment shows that single electrons create interference patterns, acting like waves, until you watch them — then they act like particles.</p>

    <h2 id="superposition">Superposition</h2>
    <p>A quantum system exists in all possible states simultaneously until observed. Schrödinger's famous cat is both alive and dead until you look. This sounds absurd but is the foundation of quantum computing.</p>

    <h2 id="entanglement">Entanglement</h2>
    <p>Two particles can be "entangled" — their quantum states are linked regardless of distance. Change one, and its partner changes instantly, even across the galaxy. Einstein called this "spooky action at a distance" and it bothered him his whole life.</p>

    <h2 id="consciousness">What Does This Mean for Consciousness?</h2>
    <p>Some physicists and philosophers argue that consciousness plays a fundamental role in quantum measurement — that observation creates reality. Others disagree violently. The honest answer: we don't know. And that's what makes it interesting.</p>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">🔬 Related Reading</div>
      <p>If this article intrigued you, read <a href="books-like-physics-of-time.html">Books Like The Physics of Time</a> — books that change how you think about reality itself.</p>
    </div>
"""
    },
    {
        "file": "articles/reading-challenge-2026.html",
        "title": "2026 Reading Challenge",
        "desc": "52 books in 52 weeks? 12 books? Something in between? Set your reading goals for 2026 and actually stick to them.",
        "category": "Reading Tips",
        "content": """
    <p class="lead">New year, new reading goals. But here's the thing about reading challenges: the people who love them and the people who hate them are both right. Here's how to set a reading goal that actually works for you.</p>

    <h2 id="why-challenge">Why Do a Reading Challenge?</h2>
    <p>Reading challenges work for some people because they create accountability. The number gives you something to come back to each week. But they fail for people who find the number stressful — turning reading from pleasure into obligation.</p>

    <h2 id="goals-that-work">Goals That Actually Work</h2>

    <h3>The Low-Bar Goal</h3>
    <p>Set a goal so easy you can't fail. "Read 12 pages a week." You'll consistently exceed it, which feels good, and the habit builds before the goal becomes a burden.</p>

    <h3>The Genre Goal</h3>
    <p>Instead of a number, commit to reading one book from a genre you've been avoiding. One memoir. One translated novel. One sci-fi classic. Intentionality beats volume.</p>

    <h3>The Author Goal</h3>
    <p>Read everything by one author you keep meaning to explore. Cormac McCarthy. Ursula K. Le Guin. Terry Pratchett. Give an author a real shot.</p>

    <h2 id="tracking">How to Track</h2>
    <p>Keep it simple. A spreadsheet, a notebook, or an app like StoryGraph. The best tracking system is the one you'll actually use.</p>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">📚 Start Your Challenge</div>
      <p>Browse <a href="../catalog.html">the Bithues catalog</a> for your first book of the year.</p>
    </div>
"""
    },
    {
        "file": "articles/speed-reading-basics.html",
        "title": "Speed Reading: What Works, What Doesn't",
        "desc": "Speed reading courses promise you can read 1,000 words per minute. Here's what the science actually says about reading faster.",
        "category": "Reading Tips",
        "content": """
    <p class="lead">The promise is irresistible: read 500 pages in an hour. Absorb a book a day. Unlock the full potential of your brain. Speed reading courses are a multi-hundred-million-dollar industry. But does any of it actually work?</p>

    <h2 id="what-science-says">What Science Actually Says</h2>
    <p>Research consistently shows that speed reading techniques trade comprehension for speed. The faster you read, the less you retain. This isn't a bug — it's how human cognition works. You can read faster, but you can't read faster <em>and</em> understand at the same depth.</p>

    <h2 id="what-works">What Actually Works</h2>
    <ul class="book-list">
      <li><strong>Reducing subvocalization:</strong> The habit of "saying" words in your head as you read. Getting rid of it takes practice but can genuinely increase speed.</li>
      <li><strong>Wide eye-span:</strong> Training yourself to take in more words per fixation. This is learnable and doesn't sacrifice comprehension as much as other techniques.</li>
      <li><strong>Eliminating regression:</strong> Rereading passages. More focus = less regression = faster reading without losing comprehension.</li>
    </ul>

    <h2 id="what-doesnt">What Doesn't Work</h2>
    <ul class="book-list">
      <li>RSVP (showing one word at a time at high speed) — the research is consistently negative</li>
      <li>Chunking (reading groups of words as "chunks") — contradicts how the eye-brain system works</li>
      <li>Any claim of 1000+ WPM with full comprehension — not supported by evidence</li>
    </ul>

    <h2 id="better-approach">A Better Approach</h2>
    <p>The best way to "read more" isn't to read faster — it's to read more efficiently. Know what you want from a book before you start. Skim the table of contents and intro. Read selectively. Take notes. Read the last chapter first sometimes. These strategies don't compromise comprehension.</p>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">📖 The Real Secret</div>
      <p>Read more by reading more often. The speed reading industry exists because people want shortcuts. There aren't any — but building a reading habit is available to everyone. Start with the <a href="../catalog.html">Bithues catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/shadow-work-guide.html",
        "title": "Shadow Work: A Beginner's Guide",
        "desc": "What is shadow work? How do you do it? The psychology of confronting the parts of yourself you hide — and why it matters.",
        "category": "Self-Help",
        "content": """
    <p class="lead">Carl Jung called it shadow work: the process of confronting the parts of yourself you don't want to see — your dark side, your flaws, your repressed emotions. It sounds intimidating, but it's one of the most transformative practices in psychology. Here's how to start.</p>

    <h2 id="what-is-shadow">What Is Shadow Work?</h2>
    <p>Your "shadow" is the collection of traits, desires, and impulses you've pushed out of conscious awareness because they were rejected, shamed, or deemed unacceptable. Everyone has one. Ignoring it doesn't make it go away — it makes it control you from the unconscious.</p>

    <h2 id="why-it-matters">Why It Matters</h2>
    <p>Your shadow doesn't stay hidden. It leaks out — as projection ("I could never do that"), as disproportionate emotional reactions ("why does that bother me so much?"), as recurring patterns you can't explain. Shadow work is about making the unconscious conscious.</p>

    <h2 id="how-to-start">How to Start</h2>

    <h3>1. Notice Your Reactions</h3>
    <p>When you have a strong emotional reaction to someone — especially anger or judgment — pause. Ask: "What part of this do I recognize?" The things we hate most in others are often qualities we've disowned in ourselves.</p>

    <h3>2. Journal Without Filter</h3>
    <p>Set a timer for 15 minutes and write whatever comes up. Don't edit. Don't judge. Let the shadow speak on paper. This is surprisingly powerful and surprisingly uncomfortable.</p>

    <h3>3. Sit with Discomfort</h3>
    <p>You will feel worse before you feel better. Confronting repressed material isn't pleasant. But the freedom on the other side — of being more whole, more honest with yourself — is worth it.</p>

    <h2 id="resources">Books That Help</h2>
    <ul class="book-list">
      <li><strong>Meeting the Shadow</strong> — Connie Zweig (foundational text)</li>
      <li><strong>The Dark Side of the Light Chasers</strong> — Debbie Ford</li>
      <li><strong>A Course in Miracles</strong> — Helen Schucman</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">🪞 Explore More</div>
      <p>Browse our <a href="../catalog.html">self-help catalog</a> for more books on shadow work, mindset, and psychological growth.</p>
    </div>
"""
    },
    {
        "file": "articles/why-read-outside-your-genre.html",
        "title": "Why You Should Read Outside Your Genre",
        "desc": "Stuck in a reading rut? The best readers read eclectically. Here's why breaking out of your favorite genre makes you a better reader.",
        "category": "Reading Tips",
        "content": """
    <p class="lead">It's comfortable to read the same kind of book over and over. Thrillers, romance, sci-fi — whatever gets you through a long flight or helps you unwind at night. But the most interesting readers are readers who break their own rules.</p>

    <h2 id="why-read-eclectically">Why Read Eclectically?</h2>
    <p>Different genres train different mental muscles. Thrillers teach you to read for tension and pacing. Literary fiction teaches you to notice language and character. Philosophy teaches you to think in systems. Each genre you read expands how you read and think.</p>

    <h2 id="specific-benefits">Specific Benefits</h2>

    <h3>You Discover What You Didn't Know You Loved</h3>
    <p>Most people who "don't like poetry" haven't read the right poetry. Most "non-science-fiction readers" just haven't found the right sci-fi. Genre boundaries are artificial. Great writing crosses them.</p>

    <h3>You Become a Better Critic</h3>
    <p>Reading widely lets you compare. You start to notice what techniques work across genres, what makes a sentence good in a thriller vs. a literary novel, what emotional beats hit differently depending on context.</p>

    <h3>You Surprise Yourself</h3>
    <p>Some of the most transformative reading experiences come from books you picked up reluctantly and couldn't put down. The book you'd never choose might be the one that changes you.</p>

    <h2 id="how-to-start">How to Branch Out</h2>
    <p>Start small. Pick one book outside your usual genre this quarter. Ask friends who read differently for recommendations. Follow your curiosity — if a news article about something interesting catches your eye, find the book on that topic.</p>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">🌍 Browse the Catalog</div>
      <p>See something you've never considered in the <a href="../catalog.html">Bithues catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/books-change-how-you-think.html",
        "title": "Books That Change How You Think",
        "desc": "These books don't just inform — they fundamentally shift how you see the world, yourself, and what you thought you knew.",
        "category": "Book Lists",
        "content": """
    <p class="lead">Some books teach you things. Other books change the operating system of your mind. The second kind are rarer. They don't just add to what you know — they reorganize how you think. Here's where to find them.</p>

    <h2 id="thinking">Books About Thinking</h2>
    <ul class="book-list">
      <li><strong>Thinking, Fast and Slow</strong> — Daniel Kahneman</li>
      <li><strong>The Black Swan</strong> — Nassim Nicholas Taleb</li>
      <li><strong>Superforecasting</strong> — Philip Tetlock</li>
      <li><strong>The Gift of Fear</strong> — Gavin de Becker</li>
    </ul>

    <h2 id="reality">Books About Reality</h2>
    <ul class="book-list">
      <li><strong>The Physics of Time</strong> — (see catalog for current)</li>
      <li><strong>Sapiens</strong> — Yuval Noah Harari</li>
      <li><strong>The Gene</strong> — Siddhartha Mukherjee</li>
      <li><strong>Consciousness Explained</strong> — Daniel Dennett</li>
    </ul>

    <h2 id="society">Books About Society</h2>
    <ul class="book-list">
      <li><strong>Factory Man</strong> — (see catalog)</li>
      <li><strong>The Righteous Mind</strong> — Jonathan Haidt</li>
      <li><strong>Outliers</strong> — Malcolm Gladwell</li>
    </ul>

    <h2 id="self">Books About Self</h2>
    <ul class="book-list">
      <li><strong>Man's Search for Meaning</strong> — Viktor Frankl</li>
      <li><strong>The Body Keeps the Score</strong> — Bessel van der Kolk</li>
      <li><strong>Atomic Habits</strong> — James Clear</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">🧠 Mind-Bending Books</div>
      <p>If this list appeals to you, see our full guide to <a href="books-like-physics-of-time.html">Books Like The Physics of Time</a> — for when you want to really have your mind blown.</p>
    </div>
"""
    },
    {
        "file": "articles/books-like-physics-of-time.html",
        "title": "Books Like The Physics of Time",
        "desc": "You loved The Physics of Time. Here are other books that will challenge how you think about time, consciousness, and the nature of reality.",
        "category": "Book Lists",
        "content": """
    <p class="lead">The Physics of Time gave you a new perspective on one of the most fundamental aspects of existence. If you're looking for that same mind-expanding feeling — where you can't quite go back to seeing the world the same way — here's where to go next.</p>

    <h2 id="time">More on Time</h2>
    <ul class="book-list">
      <li><strong>The Order of Time</strong> — Carlo Rovelli</li>
      <li><strong>From Eternity to Here</strong> — Sean Carroll</li>
      <li><strong>Time's Arrow</strong> — Martin Amis</li>
    </ul>

    <h2 id="consciousness">Consciousness & the Mind</h2>
    <ul class="book-list">
      <li><strong>Consciousness Explained</strong> — Daniel Dennett</li>
      <li><strong>The Tell-Tale Brain</strong> — V.S. Ramachandran</li>
      <li><strong>Thinking, Fast and Slow</strong> — Daniel Kahneman</li>
    </ul>

    <h2 id="cosmology">Cosmology & the Universe</h2>
    <ul class="book-list">
      <li><strong>A Brief History of Time</strong> — Stephen Hawking</li>
      <li><strong>The Elegant Universe</strong> — Brian Greene</li>
      <li><strong>Reality Is Not What It Seems</strong> — Carlo Rovelli</li>
    </ul>

    <h2 id="simulacra">Simulation, Reality & Philosophy</h2>
    <ul class="book-list">
      <li><strong>The Matrix</strong> (film) — Wachowskis</li>
      <li><strong>Blindsight</strong> — Peter Watts</li>
      <li><strong>The Egg</strong> — Andy Weir (short story)</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">🔭 Browse Science Books</div>
      <p>Explore more mind-expanding reads in the <a href="../catalog.html">Bithues catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/books-like-project-hail-mary.html",
        "title": "Books Like Project Hail Mary",
        "desc": "You finished Project Hail Mary and want more. Here are the best books for fans of Andy Weir — hard sci-fi with humor, heart, and real science.",
        "category": "Book Lists",
        "content": """
    <p class="lead">Project Hail Mary is a modern classic: rigorous hard sci-fi with a protagonist you can't help but root for, genuine scientific puzzles, and unexpected warmth. If you loved it, here's where to find more of that same magic.</p>

    <h2 id="andy-weir">If You Loved Andy Weir</h2>
    <ul class="book-list">
      <li><strong>The Martian</strong> — Andy Weir (if you somehow haven't yet)</li>
      <li><strong>Artemis</strong> — Andy Weir</li>
    </ul>

    <h2 id="hard-sf">Hard Sci-Fi With Heart</h2>
    <ul class="book-list">
      <li><strong>Galaxy's Edge</strong> — (see catalog)</li>
      <li><strong>The Mars Dynasty</strong> — (see catalog)</li>
      <li><strong> Seveneves</strong> — Neal Stephenson</li>
    </ul>

    <h2 id="first-contact">First Contact & Problem-Solving</h2>
    <ul class="book-list">
      <li><strong>Children of Time</strong> — Adrian Tchaikovsky</li>
      <li><strong>The Sparrow</strong> — Mary Russell</li>
      <li><strong>Contact</strong> — Carl Sagan</li>
    </ul>

    <h2 id="humor">Sci-Fi With Humor</h2>
    <ul class="book-list">
      <li><strong>The Murderbot Diaries</strong> — Martha Wells</li>
      <li><strong>Accelerando</strong> — Charles Stross</li>
      <li><strong>Old Man's War</strong> — John Scalzi</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">🚀 Browse Sci-Fi Reviews</div>
      <p>Find all our science fiction recommendations in the <a href="../catalog.html">Bithues catalog</a>.</p>
    </div>
"""
    },
    {
        "file": "articles/hopepunk-beginners-guide.html",
        "title": "Hopepunk: A Beginner's Guide",
        "desc": "What is hopepunk? A guide to the genre imagining better futures through cooperation, not conflict.",
        "category": "Genre Guides",
        "content": """
    <p class="lead">You've heard of grimdark. You know dystopia. But there's a counter-movement in speculative fiction that's gaining momentum — hopepunk, a genre that says: what if we built something worth inheriting?</p>

    <h2 id="what-is-hopepunk">What Is Hopepunk?</h2>
    <p>Hopepunk is a response to grimdark — the popular trend in fantasy and sci-fi that embraces moral ambiguity, graphic violence, and cynical worldviews. While grimdark asks "what if people are selfish?" hopepunk asks "what if people can work together?"</p>

    <h2 id="origins">Origins of the Term</h2>
    <p>The term emerged around 2017-2018, though the impulse behind it is much older. Ursula K. Le Guin's work was hopepunk before the word existed. So was Becky Chambers' Wayfarers series.</p>

    <h2 id="essential-reads">Essential Hopepunk Reads</h2>
    <ul class="book-list">
      <li><strong>The Wayfarers</strong> — Becky Chambers</li>
      <li><strong>A Psalm for the Wild-Built</strong> — Becky Chambers</li>
      <li><strong>The Dispossessed</strong> — Ursula K. Le Guin</li>
      <li><strong>The Left Hand of Darkness</strong> — Ursula K. Le Guin</li>
      <li><strong>Utopia</strong> — Timothy Zahn (see catalog)</li>
    </ul>

    <h2 id="hopepunk-vs-solarpunk">Hopepunk vs. Solarpunk</h2>
    <p>Solarpunk is about environmental sustainability and ecofuturism. Hopepunk is broader — it's about any future built on cooperation rather than exploitation. The two overlap and complement each other.</p>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">✨ More Hopepunk</div>
      <p>See our full article on <a href="hopepunk-fiction.html">The Rise of Hopepunk Fiction</a> for a deeper dive into the genre.</p>
    </div>
"""
    },
    {
        "file": "articles/business-leadership-guide.html",
        "title": "Business & Leadership Books",
        "desc": "The best business and leadership books — from startups to scale-ups to personal effectiveness. What actually works.",
        "category": "Business",
        "content": """
    <p class="lead">The business book industry produces thousands of titles a year. Most are forgettable. Some are genuinely transformative. Here's our curated guide to the business and leadership books actually worth your time.</p>

    <h2 id="startups">Startups & Entrepreneurship</h2>
    <ul class="book-list">
      <li><strong>The Lean Startup</strong> — Eric Ries</li>
      <li><strong>Zero to One</strong> — Peter Thiel</li>
      <li><strong>The Hard Thing About Hard Things</strong> — Ben Horowitz</li>
      <li><strong>Venture Deals</strong> — Brad Feld</li>
    </ul>

    <h2 id="leadership">Leadership</h2>
    <ul class="book-list">
      <li><strong>Good to Great</strong> — Jim Collins</li>
      <li><strong>Leaders Eat Last</strong> — Simon Sinek</li>
      <li><strong>The Effective Executive</strong> — Peter Drucker</li>
      <li><strong>Start with Why</strong> — Simon Sinek</li>
    </ul>

    <h2 id="thinking">Decision-Making & Thinking</h2>
    <ul class="book-list">
      <li><strong>Thinking, Fast and Slow</strong> — Daniel Kahneman</li>
      <li><strong>The Black Swan</strong> — Nassim Nicholas Taleb</li>
      <li><strong>Superforecasting</strong> — Philip Tetlock</li>
    </ul>

    <h2 id="habits">Habits & Personal Effectiveness</h2>
    <ul class="book-list">
      <li><strong>Atomic Habits</strong> — James Clear</li>
      <li><strong>Deep Work</strong> — Cal Newport</li>
      <li><strong>The 7 Habits of Highly Effective People</strong> — Stephen Covey</li>
    </ul>

    <div class="card" style="margin-top:2rem;">
      <div class="card-title">💼 Browse the Catalog</div>
      <p>Find more business and leadership books in the <a href="../catalog.html">Bithues catalog</a>.</p>
    </div>
"""
    },
]

print("Starting article fixes...")
for article in ARTICLES:
    path = article["file"]
    try:
        info = api_get(path)
        sha = info["sha"]
        size = info["size"]
        
        # Only push if it's the stub size (~1772) or similar
        if size < 3000:
            print(f"  FIXING stub ({size}b): {path}")
            html = TEMPLATE.format(
                title=article["title"],
                desc=article["desc"],
                category=article["category"],
                content=article["content"].strip()
            )
            result, err = api_put(path, html, sha, f"Fix stub: {article['title']}")
            if err:
                print(f"    ERROR: {err}")
            else:
                print(f"    OK: pushed")
        else:
            print(f"  SKIP already fixed ({size}b): {path}")
    except Exception as e:
        print(f"  ERROR getting {path}: {e}")
    time.sleep(0.5)

print("Done!")
