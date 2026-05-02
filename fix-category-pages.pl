#!/usr/bin/perl
use strict;
use warnings;

my $base = "/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues/category";

my %genre_intros = (
  fiction => <<'INTRO',
<p class="genre-intro">Fiction is the art of living other lives. When you open a novel, you don't just read words — you step inside someone else's skin, see through their eyes, feel their world. The best fiction doesn't escape reality; it deepens it, showing us corners of human experience we'd never reach on our own. Whether it's a centuries-past empire or a city that never sleeps, fiction gives us the maps we didn't know we needed.</p>
INTRO
  selfhelp => <<'INTRO',
<p class="genre-intro">Self-help is built on a simple, radical premise: you have the power to change your own life. Not tomorrow, not when the conditions are perfect — now. The genre cuts through noise and gets practical, offering frameworks for everything from managing anxiety to building wealth to thinking more clearly. The best books in this space don't preach; they equip, giving you mental models and habits you can actually use.</p>
INTRO
  'science-fiction' => <<'INTRO',
<p class="genre-intro">Science fiction is the literature of the possible — stories that begin with "what if" and follow the answer wherever it leads. From cyberpunk megacities to first-contact diplomacy, from quantum theories of consciousness to the ethics of artificial minds, sci-fi uses tomorrow's technology to explore today's deepest questions. It is the genre most responsible for making readers think about what kind of species we are becoming.</p>
INTRO
  fantasy => <<'INTRO',
<p class="genre-intro">Fantasy is the literature of wonder — where magic is real, ancient powers stir beneath the earth, and ordinary people discover they are capable of extraordinary things. But fantasy is never really about magic. It is about choice, sacrifice, the weight of power, and what we owe to people we love. The best fantasy builds worlds with the internal consistency of physics, then tells human stories against that epic backdrop.</p>
INTRO
  thriller => <<'INTRO',
<p class="genre-intro">A thriller demands one thing above all else: forward momentum. From the first page, something has gone wrong — or is about to. The protagonist is already in deep, or about to be. Every chapter ends on a hinge, and the reader has no choice but to swing that door open. The best thrillers use the format not for empty spectacle but to explore people under pressure, where character is forged or broken by circumstance.</p>
INTRO
  biography => <<'INTRO',
<p class="genre-intro">Biography is the genre where facts become stories without sacrificing truth. A great biography does more than chronicle events — it inhabits a life, tracing the internal logic of someone who made particular choices at particular moments. The reader comes away not just knowing more history but understanding it differently, feeling the weight of living inside a specific human mind and the era it navigated.</p>
INTRO
  business => <<'INTRO',
<p class="genre-intro">Business books are where abstract strategy meets daily reality. The best ones take ideas that sound simple — compounding, first principles, incentives — and show you how they play out in practice across decades of market history, startup culture, and the minds of exceptional founders. Read critically, this genre is one of the best investments you can make: a few hours with the right book can reframe how you think about money, work, and risk for years.</p>
INTRO
  mystery => <<'INTRO',
<p class="genre-intro">Mystery is the puzzle-solver's art — a genre where every detail is a potential clue and the reader who pays closest attention wins. But the best mysteries are more than intellectual games. They are, at their heart, moral stories: crimes that reveal something broken in the world, investigations that restore a kind of justice, and endings that linger because they don't just solve a case but illuminate a truth about human nature.</p>
INTRO
  adventure => <<'INTRO',
<p class="genre-intro">Adventure fiction is as old as storytelling itself — the call into the unknown, the hero who answers despite every reason not to. These are stories of movement and risk: crossing trackless wilderness, navigating hostile territory, making it out alive against the odds. The geography and the stakes are extreme, but the underlying story is deeply human: what we endure for the people we protect, and what we discover about ourselves when ordinary limits no longer apply.</p>
INTRO
  dystopian => <<'INTRO',
<p class="genre-intro">Dystopian fiction is warning literature dressed in the clothes of prediction. It builds worlds where a single wrong turn — a technological overreach, a political failure, a cultural collapse — has reshaped civilization into something unrecognizable. The dystopia is not the point. The point is the mirror: every terrible future on the page is a shadow cast by a present we still have the power to change. The genre earns its darkness by making us feel what we stand to lose.</p>
INTRO
  'historical-fiction' => <<'INTRO',
<p class="genre-intro">Historical fiction does something no documentary can: it makes the past feel inhabited. It asks not just "what happened?" but "what was it like to live inside that moment?" — to wear those clothes, speak those words, carry those fears. The best historical fiction earns its setting through rigorous research, then uses that research not for display but to create pressure: characters caught in historical forces they didn't choose, navigating change the way a swimmer navigates current.</p>
INTRO
  romance => <<'INTRO',
<p class="genre-intro">Romance is, at its core, the literature of hope — the insistence that human connection matters, that two people can meet in the middle of their各自的 complexity and choose each other anyway. The genre gets dismissed as lightweight because it centers relationship, but that focus is precisely what makes it demanding: writing desire and vulnerability and the slow accumulation of trust in a way that feels true is one of the hardest things in fiction. The best romance readers know this.</p>
INTRO
  mythology => <<'INTRO',
<p class="genre-intro">Mythology is where a culture goes to dream aloud. Ancient stories of gods and monsters, of heroes who walk between worlds, of floods and fires and the slow emergence of civilization from chaos — these are the templates from which all subsequent storytelling draws. Myth is not outdated: it is the deep structure of narrative itself. To read mythology is to understand the archetypes that show up in every bookstore and streaming platform today.</p>
INTRO
  literary => <<'INTRO',
<p class="genre-intro">Literary fiction is fiction that takes the craft of writing itself seriously — where the sentence is a unit of thought, not just a carrier of information. It is often slower than genre fiction, more interested in the interior life of its characters than in external plot mechanics, and more willing to sit with ambiguity and contradiction. But "literary" is not a seal of quality — it is a style, and like any style, it can be used brilliantly or badly. The best literary fiction makes you see language itself as a creative act.</p>
INTRO
  children => <<'INTRO',
<p class="genre-intro">Children's literature is where reading begins — and where the most important literary negotiations happen. A book for young readers has to earn attention on their terms, not adult ones: shorter attention spans, concrete thinking, emotional lives that haven't yet learned to hide behind irony. The best children's books are deceptively simple on the surface and quietly sophisticated underneath, teaching kids to imagine, to feel, and to think about others without ever making it feel like teaching. They are also, frequently, the best-written books on any shelf.</p>
INTRO
  cultural => <<'INTRO',
<p class="genre-intro">Cultural fiction opens doors that daily life keeps closed — novels and stories built from lives lived in different languages, under different skies, within different assumptions about family, faith, and freedom. These are books that ask you to suspend your own common sense and enter a different common world. The reader who finishes a cultural novel with genuine understanding has accomplished something that is rarer than it should be: they have genuinely imagined life in another place.</p>
INTRO
  spiritual => <<'INTRO',
<p class="genre-intro">Spiritual fiction navigates the inner terrain — not the geography of external reality but the landscape of consciousness, meaning, and the persistent human sense that there is more to existence than meets the eye. From consciousness-expanding thrillers to quiet contemplative novels, from stories of awakening in the modern world to myths of ancient wisdom traditions, this genre takes the invisible seriously without sacrificing intellectual honesty. The best spiritual fiction doesn't answer the big questions; it makes readers feel the questions more fully.</p>
INTRO
  science => <<'INTRO',
<p class="genre-intro">Science writing translates the most counterintuitive discoveries in human history into language that non-specialists can actually feel. The best science books don't just convey information — they recalibrate intuition. After reading the right book on thermodynamics, or the origins of the universe, or how consciousness emerges from matter, you look at the world differently. Science writing is philosophy that has been stress-tested against reality, and the results are often stranger and more beautiful than anything we could have invented.</p>
INTRO
);

my %book_cards = (
  fiction => [
    { title => "The Dawn of Civilization", author => "T. Stone", tldr => "A prehistoric tribe fights to survive in a world reshaped by catastrophe.", href => "../reviews/1.html" },
    { title => "The Richmond Cipher", author => "E. Maris", tldr => "Historical secrets buried in a centuries-old code.", href => "../reviews/the-richmond-cipher.html" },
    { title => "Disclosure 2026", author => "Marcus Reeve", tldr => "Eighteen rated scenarios for alien first contact.", href => "../reviews/disclosure-2026.html" },
    { title => "The Virus: A Children's Story", author => "Michael Bacotti", tldr => "A children's story exploring science, fear, and resilience.", href => "../reviews/virus-childrens-story.html" },
  ],
  'science-fiction' => [
    { title => "Echoes of Aetheris", author => "Aetheri Codex", tldr => "A dying world, ancient AI, and one programmer's choice.", href => "../reviews/aetheri-codex.html" },
    { title => "Resonance Drift", author => "R. Zyrion", tldr => "In bioluminescent spires of Eden Prime, a family's discovery threatens everything.", href => "../reviews/resonance-drift.html" },
    { title => "Symbiont Bloom", author => "Elowen Tidebloom", tldr => "On volcanic Lumengrove, a family must solve a systems puzzle to save their home.", href => "../reviews/symbiont-bloom.html" },
    { title => "Quantum Soul Echoes", author => "Quantum Chronos", tldr => "Consciousness as particle and spacetime imprint — a dual-dimensional theory of mind and body.", href => "../reviews/quantum-soul-echoes.html" },
    { title => "Rules of Survival", author => "Jorak Veldt", tldr => "First names and a hostile world: survival is not a given.", href => "../reviews/rules-of-survival.html" },
    { title => "Consciousness in Higher Dimensional Spacetime", author => "Quantum Chronos", tldr => "A dual-dimensional theory of mind and body.", href => "../reviews/17.html" },
  ],
  fantasy => [
    { title => "The Quiet Hours", author => "Elara Moss", tldr => "Gentle bedtime stories celebrating simple joys — perfect for children seeking comfort.", href => "../reviews/the-quiet-hours.html" },
    { title => "Shadow Work Journal for Women", author => "Luna Sage", tldr => "A beginner-friendly 90-day journal with warm prompts for emotional healing.", href => "../reviews/shadow-work-journal.html" },
    { title => "Rules of Survival", author => "Jorak Veldt", tldr => "First names and a hostile world: survival is not a given.", href => "../reviews/rules-of-survival.html" },
    { title => "Symbiont Bloom", author => "Elowen Tidebloom", tldr => "On volcanic Lumengrove, a family must solve a systems puzzle.", href => "../reviews/symbiont-bloom.html" },
    { title => "Blood Ember", author => "Jorak Veldt", tldr => "The first fire brings the first cost.", href => "../reviews/blood-ember.html" },
  ],
  'self-help' => [
    { title => "The Power of Changing Your Mind", author => "Evan R. Cole", tldr => "How intellectual humility improves decisions, relationships, and everyday life.", href => "../reviews/the-power-of-changing-your-mind.html" },
    { title => "The Shadow Within", author => "Elena Maris", tldr => "A practical guide to shadow work for everyday life.", href => "../reviews/the-shadow-within.html" },
    { title => "Time Investing", author => "H Harvey", tldr => "A self-help guide to valuing your own time.", href => "../reviews/35.html" },
    { title => "Mindful Memory", author => "D. E. Harlan", tldr => "Thought experiments and memory mapping to strengthen your brain.", href => "../reviews/mindful-memory.html" },
    { title => "Beyond the Veil", author => "D. E. Harlan", tldr => "Quantum speculations on consciousness, death, and the universe.", href => "../reviews/beyond-the-veil.html" },
  ],
  nonfiction => [
    { title => "Living with a Moving Planet", author => "J. T. Hartley", tldr => "Deep time, human adaptation, and a positive climate future.", href => "../reviews/living-with-a-moving-planet.html" },
    { title => "Mindful Memory", author => "D. E. Harlan", tldr => "Thought experiments and memory mapping to strengthen your brain.", href => "../reviews/mindful-memory.html" },
    { title => "Physics of Insight", author => "Quantum Chronos", tldr => "Awakening the savant within.", href => "../reviews/physics-of-insight.html" },
    { title => "The Physics of Time", author => "Quantum Chronos", tldr => "Consciousness, spacetime, and the nature of temporal experience.", href => "../reviews/the-physics-of-time.html" },
    { title => "Discovering Washington DC", author => "Evelyn Carter", tldr => "A comprehensive guide for all ages.", href => "../reviews/discovering-washington-dc.html" },
    { title => "Echoes of Transcendence", author => "L Everwood", tldr => "Poetry, meaning, and the search for transcendence.", href => "../reviews/echoes-of-transcendence.html" },
    { title => "American Journeys", author => "C. Everett", tldr => "Exploring language and American culture.", href => "../reviews/american-journeys.html" },
  ],
  thriller => [
    { title => "The Confluence Doctrine", author => "Alaric Wynn", tldr => "A framework for understanding how trends converge to create opportunities.", href => "../reviews/the-confluence-doctrine.html" },
    { title => "Disclosure 2026", author => "Marcus Reeve", tldr => "Eighteen rated scenarios for alien first contact.", href => "../reviews/disclosure-2026.html" },
  ],
  biography => [
    { title => "Mythical Menagerie", author => "E. Marlowe", tldr => "A journey across cultures and the creatures that inhabit human imagination.", href => "../reviews/mythical-menagerie.html" },
    { title => "The Orchardist: Harvest", author => "Kate E Brennan", tldr => "Small-town roots, complicated harvests.", href => "../reviews/the-orchardist-harvest.html" },
  ],
  business => [
    { title => "The Power of Changing Your Mind", author => "Evan R. Cole", tldr => "How intellectual humility improves decisions, relationships, and everyday life.", href => "../reviews/the-power-of-changing-your-mind.html" },
    { title => "The Confluence Doctrine", author => "Alaric Wynn", tldr => "A framework for understanding how trends converge to create opportunities.", href => "../reviews/the-confluence-doctrine.html" },
    { title => "Time Investing", author => "H Harvey", tldr => "A self-help guide to valuing your own time.", href => "../reviews/35.html" },
  ],
  adventure => [
    { title => "Rules of Survival", author => "Jorak Veldt", tldr => "First names and a hostile world: survival is not a given.", href => "../reviews/rules-of-survival.html" },
    { title => "Blood Ember", author => "Jorak Veldt", tldr => "The first fire brings the first cost.", href => "../reviews/blood-ember.html" },
    { title => "Red Horizon: Lunar Launch", author => "M. A. Hale", tldr => "A lunar mission, a sabotage, and the astronauts caught in the middle.", href => "../reviews/red-horizon-lunar-launch.html" },
  ],
  dystopian => [
    { title => "Disclosure 2026", author => "Marcus Reeve", tldr => "Eighteen rated scenarios for alien first contact.", href => "../reviews/disclosure-2026.html" },
    { title => "Resonance Drift", author => "R. Zyrion", tldr => "In bioluminescent spires of Eden Prime, harmony hums — until it doesn't.", href => "../reviews/resonance-drift.html" },
  ],
  'historical-fiction' => [
    { title => "The Richmond Cipher", author => "E. Maris", tldr => "Historical secrets buried in a centuries-old code.", href => "../reviews/the-richmond-cipher.html" },
    { title => "Otomí", author => "E. J. Marín", tldr => "A historical narrative of land, ritual, and continuity.", href => "../reviews/otomi.html" },
    { title => "Horizonte Rojo: Lanzamiento Lunar", author => "M. A. Hale", tldr => "Una historia de la primera base lunar y sus secretos.", href => "../reviews/horizonte-rojo.html" },
    { title => "The Dawn of Civilization", author => "T. Stone", tldr => "A prehistoric tribe fights to survive in a world reshaped by catastrophe.", href => "../reviews/1.html" },
  ],
  romance => [
    { title => "A Home for Anya", author => "Lena Ashfield", tldr => "A small-town romance about finding home where you least expect it.", href => "../reviews/home-for-anya.html" },
  ],
  mythology => [
    { title => "Mythical Menagerie", author => "E. Marlowe", tldr => "A journey across cultures and the creatures that inhabit human imagination.", href => "../reviews/mythical-menagerie.html" },
    { title => "Echoes of Aetheris", author => "Aetheri Codex", tldr => "A dying world, ancient AI, and one programmer's choice.", href => "../reviews/aetheri-codex.html" },
  ],
  literary => [
    { title => "The Quiet Hours", author => "Elara Moss", tldr => "Gentle bedtime stories celebrating simple joys.", href => "../reviews/the-quiet-hours.html" },
    { title => "The Virus: A Children's Story", author => "Michael Bacotti", tldr => "A children's story exploring science, fear, and resilience.", href => "../reviews/virus-childrens-story.html" },
  ],
  children => [
    { title => "Little Mike: Fun at the Beach", author => "Michael Jr.", tldr => "A children's adventure at the beach — fun, gentle, and perfect for bedtime.", href => "../reviews/little-mike-beach.html" },
    { title => "Little Mike: Learns to Fly", author => "Michael Jr.", tldr => "Mike learns to fly — with imagination, determination, and a little help from friends.", href => "../reviews/little-mike-fly.html" },
    { title => "Little Mike: Builds a Robot", author => "Michael Jr.", tldr => "Mike builds a robot from scraps, curiosity, and a lot of heart.", href => "../reviews/little-mike-robot.html" },
    { title => "Microbiology ABC's", author => "Michael Bacotti", tldr => "Tiny cells and microbes from A to Z — science for kids.", href => "../reviews/microbiology-abcs.html" },
    { title => "The Virus: A Children's Story", author => "Michael Bacotti", tldr => "A children's story exploring science, fear, and resilience.", href => "../reviews/virus-childrens-story.html" },
  ],
  cultural => [
    { title => "American Journeys", author => "C. Everett", tldr => "Exploring language and American culture.", href => "../reviews/american-journeys.html" },
    { title => "Otomí", author => "E. J. Marín", tldr => "A historical narrative of land, ritual, and continuity.", href => "../reviews/otomi.html" },
  ],
  spiritual => [
    { title => "Beyond the Veil", author => "D. E. Harlan", tldr => "Quantum speculations on consciousness, death, and the universe.", href => "../reviews/beyond-the-veil.html" },
    { title => "Quantum Soul Echoes", author => "Quantum Chronos", tldr => "Consciousness as particle and spacetime imprint.", href => "../reviews/quantum-soul-echoes.html" },
    { title => "The Physics of Time", author => "Quantum Chronos", tldr => "Consciousness, spacetime, and the nature of temporal experience.", href => "../reviews/the-physics-of-time.html" },
  ],
  science => [
    { title => "Physics of Insight", author => "Quantum Chronos", tldr => "Awakening the savant within.", href => "../reviews/physics-of-insight.html" },
    { title => "The Physics of Time", author => "Quantum Chronos", tldr => "Consciousness, spacetime, and the nature of temporal experience.", href => "../reviews/the-physics-of-time.html" },
    { title => "Consciousness in Higher Dimensional Spacetime", author => "Quantum Chronos", tldr => "A dual-dimensional theory of mind and body.", href => "../reviews/17.html" },
    { title => "Microbiology ABC's", author => "Michael Bacotti", tldr => "Tiny cells and microbes from A to Z.", href => "../reviews/microbiology-abcs.html" },
  ],
);

for my $cat (keys %genre_intros) {
  my $path = "$base/$cat.html";
  next unless -f $path;
  
  my $intro = $genre_intros{$cat};
  my $cards = $book_cards{$cat} // [];
  
  open(my $fh, '<', $path) or die "Cannot read $path: $!";
  my $content = do { local $/; <$fh> };
  close($fh);
  
  my $intro_html = qq(<div class="genre-intro">\n$intro</div>\n);
  my $books_html = "";
  for my $book (@$cards) {
    $books_html .= qq(<div class="book-card">\n);
    $books_html .= qq(<h3><a href="$book->{href}">$book->{title}</a></h3>\n);
    $books_html .= qq(<p class="author">by $book->{author}</p>\n);
    $books_html .= qq(<p class="tldr">$book->{tldr}</p>\n);
    $books_html .= qq(<a href="$book->{href}" class="read-more">Read Review →</a>\n);
    $books_html .= qq(</div>\n);
  }
  my $grid_html = qq(<section class="book-grid">\n$books_html</section>\n);
  my $intro_html = qq(<div class="genre-intro">\n$intro</div>\n);

  if ($content =~ m|<section class="book-grid">.*?</section>|s) {
    $content =~ s|(<section class="book-grid">.*?</section>)|$grid_html|s;
  }
  if ($content !~ /genre-intro/) {
    $content =~ s|(<div class="chips"[^>]*>.*?</div>\s*)|$1\n$intro_html\n$grid_html|s;
  }
  
  open(my $fh, '>', $path) or die "Cannot write $path: $!";
  print $fh $content;
  close($fh);
  
  print "Processed: $cat.html\n";
}

print "Done.\n";
