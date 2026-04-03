// Enhanced Site Search with relevance scoring, fuzzy matching, and suggestions

const siteData = {
    "books": [
        {
            "title": "Shadow Work Journal for Women",
            "author": "Luna Sage",
            "url": "reviews/23.html",
            "desc": "A beginner-friendly 90-day journal with warm prompts for emotional healing.",
            "keywords": "a beginner-friendly 90-day journal with warm prompts for emotional healing."
        },
        {
            "title": "Time Investing",
            "author": "H Harvey",
            "url": "reviews/35.html",
            "desc": "A self-help guide showing how to prioritize yourself and your time. Strategies for investing in yourself.",
            "keywords": "a self-help guide showing how to prioritize yourself and your time. strategies for investing in your"
        },
        {
            "title": "The Shadow Within",
            "author": "Elena Maris",
            "url": "reviews/9.html",
            "desc": "Instead of treating reactions as defects, learn to treat them as information\u2014and respond differently in everyday life.",
            "keywords": "instead of treating reactions as defects, learn to treat them as information\u2014and respond differently"
        },
        {
            "title": "Microbiology ABC&#x27;s",
            "author": "Michael Bacotti",
            "url": "reviews/19.html",
            "desc": "From amoebas to zooplankton, each letter highlights a microbe or cell structure with colorful illustrations.",
            "keywords": "from amoebas to zooplankton, each letter highlights a microbe or cell structure with colorful illust"
        },
        {
            "title": "Living with a Moving Planet",
            "author": "J. T. Hartley",
            "url": "reviews/5.html",
            "desc": "Drawing on deep-time climate records and archaeology, this book shows how humans have adapted to changing baselines for tens of thousands of years.",
            "keywords": "drawing on deep-time climate records and archaeology, this book shows how humans have adapted to cha"
        },
        {
            "title": "Physics of Insight",
            "author": "Quantum Chronos",
            "url": "reviews/15.html",
            "desc": "What if genius isn&#x27;t rare\u2014it&#x27;s hidden inside every mind, waiting for the right switch?",
            "keywords": "what if genius isn&#x27;t rare\u2014it&#x27;s hidden inside every mind, waiting for the right switch?"
        },
        {
            "title": "The Power of Changing Your Mind",
            "author": "Evan R. A. Cole",
            "url": "reviews/the-power-of-changing-your-mind.html",
            "desc": "A practical guide to intellectual humility and how it improves decisions, relationships, and everyday life.",
            "keywords": "a practical guide to intellectual humility and how it improves decisions, relationships, and everyda"
        },
        {
            "title": "Otom\u00ed",
            "author": "E. J. Mar\u00edn",
            "url": "reviews/14.html",
            "desc": "Through the eyes of a young ritual apprentice, follow one drought-stricken year in an Otom\u00ed village.",
            "keywords": "through the eyes of a young ritual apprentice, follow one drought-stricken year in an otom\u00ed village."
        },
        {
            "title": "The Confluence Doctrine",
            "author": "Alaric Wynn",
            "url": "reviews/4.html",
            "desc": "In a world where suffering has been designed out, Orren Myal hears something that doesn&#x27;t fit\u2014a sense of &#x27;full, but unfinished.&#x27; What i",
            "keywords": "in a world where suffering has been designed out, orren myal hears something that doesn&#x27;t fit\u2014a"
        },
        {
            "title": "Quantum Soul Echoes",
            "author": "Quantum Chronos",
            "url": "reviews/18.html",
            "desc": "What if consciousness is what spacetime remembers? Two models synthesized in this rigorous exploration.",
            "keywords": "what if consciousness is what spacetime remembers? two models synthesized in this rigorous explorati"
        },
        {
            "title": "The Power of Changing Your Mind",
            "author": "Evan R. Cole",
            "url": "reviews/8.html",
            "desc": "In a culture that rewards confidence, this book shows how intellectual humility is actually a competitive edge.",
            "keywords": "in a culture that rewards confidence, this book shows how intellectual humility is actually a compet"
        },
        {
            "title": "Little Mike: Builds a Robot",
            "author": "Michael Jr",
            "url": "reviews/34.html",
            "desc": "Little Mike, John, and May build robots\u2014but they keep falling apart. Through teamwork, they create a robot that tells stories.",
            "keywords": "little mike, john, and may build robots\u2014but they keep falling apart. through teamwork, they create a"
        },
        {
            "title": "Mindful Memory",
            "author": "D. E. Harlan",
            "url": "reviews/22.html",
            "desc": "Empowering retirees with science-backed exercises like memory palaces and timeline mapping.",
            "keywords": "empowering retirees with science-backed exercises like memory palaces and timeline mapping."
        },
        {
            "title": "Little Mike: Learns to Fly",
            "author": "Michael Jr",
            "url": "reviews/29.html",
            "desc": "Little Mike dreams of flying. With friends John and May, he meets Pilot Thomas who teaches the wonders of airplanes.",
            "keywords": "little mike dreams of flying. with friends john and may, he meets pilot thomas who teaches the wonde"
        },
        {
            "title": "The Richmond Cipher",
            "author": "E. Maris",
            "url": "reviews/the-richmond-cipher.html",
            "desc": "A historical thriller that weaves cryptography, Civil War intrigue, and a family secret into a page-turning mystery.",
            "keywords": "a historical thriller that weaves cryptography, civil war intrigue, and a family secret into a page-"
        },
        {
            "title": "Red Horizon: Lunar Launch",
            "author": "M. A. Hale",
            "url": "reviews/3.html",
            "desc": "Commander Marcus Hale must launch the Eos Ark to deliver 250 young colonists to Mars. But UAP hover above the horizon\u2014humanity is raising children und",
            "keywords": "commander marcus hale must launch the eos ark to deliver 250 young colonists to mars. but uap hover "
        },
        {
            "title": "Symbiont Bloom",
            "author": "Elowen Tidebloom",
            "url": "reviews/13.html",
            "desc": "On volcanic isles of Lumengrove, dawn arrives through living leaf-glass. When the island&#x27;s pulse skips, a family must unravel a systems puzzle.",
            "keywords": "on volcanic isles of lumengrove, dawn arrives through living leaf-glass. when the island&#x27;s puls"
        },
        {
            "title": "Blood Ember",
            "author": "Jorak Veldt",
            "url": "reviews/25.html",
            "desc": "Three parts trace how survival habits harden into protocol, law, and chant. From fire to spear to echo.",
            "keywords": "three parts trace how survival habits harden into protocol, law, and chant. from fire to spear to ec"
        },
        {
            "title": "Mythical Menagerie",
            "author": "E. Marlowe",
            "url": "reviews/33.html",
            "desc": "A thrilling journey through cultures exploring mythical creatures. Discover how dragons and shape-shifters shaped cultural identities.",
            "keywords": "a thrilling journey through cultures exploring mythical creatures. discover how dragons and shape-sh"
        },
        {
            "title": "Living with a Moving Planet",
            "author": "J. T. Hartley",
            "url": "reviews/living-with-a-moving-planet.html",
            "desc": "A hopeful, practical guide to adapting to climate change through personal resilience and systemic thinking.",
            "keywords": "a hopeful, practical guide to adapting to climate change through personal resilience and systemic th"
        },
        {
            "title": "American Journeys",
            "author": "C. Everett",
            "url": "reviews/32.html",
            "desc": "For those moving to or visiting the US\u2014or anyone eager to enhance English through immersive content.",
            "keywords": "for those moving to or visiting the us\u2014or anyone eager to enhance english through immersive content."
        },
        {
            "title": "Rules of Survival",
            "author": "Jorak Veldt",
            "url": "reviews/24.html",
            "desc": "Roughly one million years ago, a boy learns the band&#x27;s rules\u2014water order, ember law, watch\u2014and pays for them in skin.",
            "keywords": "roughly one million years ago, a boy learns the band&#x27;s rules\u2014water order, ember law, watch\u2014and "
        },
        {
            "title": "Resonance Drift",
            "author": "R. Zyrion",
            "url": "reviews/12.html",
            "desc": "In Eden Prime&#x27;s biolum spires, harmony hums\u2014until a family detects a pulse that defies the weave.",
            "keywords": "in eden prime&#x27;s biolum spires, harmony hums\u2014until a family detects a pulse that defies the weav"
        },
        {
            "title": "The Richmond Cipher",
            "author": "E. Maris",
            "url": "reviews/2.html",
            "desc": "In Confederate Richmond, 1863, Mary carries secrets in her memory as she moves through the Executive Mansion. Every word she hears becomes intelligenc",
            "keywords": "in confederate richmond, 1863, mary carries secrets in her memory as she moves through the executive"
        },
        {
            "title": "The Quiet Hours",
            "author": "Elara Moss",
            "url": "reviews/28.html",
            "desc": "Gentle bedtime stories celebrating simple joys\u2014perfect for children seeking comfort.",
            "keywords": "gentle bedtime stories celebrating simple joys\u2014perfect for children seeking comfort."
        },
        {
            "title": "Disclosure 2026",
            "author": "Marcus Reeve",
            "url": "reviews/11.html",
            "desc": "From viral smartphone footage to White House landings, this book analyzes 18 pathways to alien disclosure\u2014each rated for plausibility based on decades",
            "keywords": "from viral smartphone footage to white house landings, this book analyzes 18 pathways to alien discl"
        },
        {
            "title": "The Dawn of Civilization",
            "author": "T. Stone",
            "url": "reviews/1.html",
            "desc": "When a brutal winter kills his father, sixteen-year-old Koda watches Uluk take up the leader&#x27;s staff and hold their small tribe together. As bear",
            "keywords": "when a brutal winter kills his father, sixteen-year-old koda watches uluk take up the leader&#x27;s "
        },
        {
            "title": "The Shadow Within",
            "author": "Elena Maris",
            "url": "reviews/the-shadow-within.html",
            "desc": "A practical, grounded guide to shadow work that avoids mysticism while acknowledging psychological depth.",
            "keywords": "a practical, grounded guide to shadow work that avoids mysticism while acknowledging psychological d"
        },
        {
            "title": "Echoes of Transcendence",
            "author": "L Everwood",
            "url": "reviews/31.html",
            "desc": "Where boundaries of reality blur, seekers embark on a transformative journey. Guided by ancient prophecies, they unveil mysteries.",
            "keywords": "where boundaries of reality blur, seekers embark on a transformative journey. guided by ancient prop"
        },
        {
            "title": "Little Mike: Fun at the Beach",
            "author": "Michael Jr",
            "url": "reviews/27.html",
            "desc": "Join Little Mike and his friends as they build an awe-inspiring sand castle.",
            "keywords": "join little mike and his friends as they build an awe-inspiring sand castle."
        },
        {
            "title": "The Orchardist: Harvest",
            "author": "Kate E Brennan",
            "url": "reviews/26.html",
            "desc": "Diane Kessler falls from a ladder\u2014in that moment, she doesn&#x27;t come back. A story of near-death experience.",
            "keywords": "diane kessler falls from a ladder\u2014in that moment, she doesn&#x27;t come back. a story of near-death "
        },
        {
            "title": "Discovering Washington DC",
            "author": "Evelyn Carter",
            "url": "reviews/30.html",
            "desc": "Beyond the monuments\u2014a guide to the real DC. Stroll Georgetown&#x27;s cobblestones, tap your feet to jazz, taste a half-smoke.",
            "keywords": "beyond the monuments\u2014a guide to the real dc. stroll georgetown&#x27;s cobblestones, tap your feet to"
        },
        {
            "title": "Echoes of Aetheris",
            "author": "Aetheri Codex",
            "url": "reviews/10.html",
            "desc": "Nine thousand years before history, a wounded alien ship falls onto a frozen steppe. The first hybrid is born.",
            "keywords": "nine thousand years before history, a wounded alien ship falls onto a frozen steppe. the first hybri"
        },
        {
            "title": "The Burning Song",
            "author": "Rowan Ashcroft",
            "url": "reviews/21.html",
            "desc": "When a cave lion marks Aken, the leader makes a choice that breaks every rule: he sends scouts to the coastal strangers.",
            "keywords": "when a cave lion marks aken, the leader makes a choice that breaks every rule: he sends scouts to th"
        },
        {
            "title": "Consciousness in Higher Dimensional Spacetime",
            "author": "Quantum Chronos",
            "url": "reviews/17.html",
            "desc": "What if consciousness doesn&#x27;t exist in the same spacetime as the body? A radical extension of Einstein&#x27;s relativity into the domain of mind.",
            "keywords": "what if consciousness doesn&#x27;t exist in the same spacetime as the body? a radical extension of e"
        },
        {
            "title": "Veiled Presence",
            "author": "E.C. Stroud",
            "url": "reviews/7.html",
            "desc": "In Veiled Presence: Questions on Earth's Silent Neighbors, researcher E. C. Stroud walks carefully through the modern UAP/UFO record\u2014not to proclaim a",
            "keywords": "in veiled presence: questions on earth's silent neighbors, researcher e. c. stroud walks carefully t"
        },
        {
            "title": "Beyond the Veil",
            "author": "D. E. Harlan",
            "url": "reviews/6.html",
            "desc": "A careful tour of evidence around what happens when we die, drawing on NDE research, quantum physics, and philosophy.",
            "keywords": "a careful tour of evidence around what happens when we die, drawing on nde research, quantum physics"
        },
        {
            "title": "The Physics of Time",
            "author": "Quantum Chronos",
            "url": "reviews/16.html",
            "desc": "A groundbreaking exploration: what if the universe is a block of spacetime containing all moments, yet consciousness navigates through it?",
            "keywords": "a groundbreaking exploration: what if the universe is a block of spacetime containing all moments, y"
        },
        {
            "title": "Red Horizon: Lunar Launch",
            "author": "M. A. Hale",
            "url": "reviews/red-horizon-lunar-launch.html",
            "desc": "A near-future lunar colony faces sabotage and political intrigue in this fast-paced sci-fi thriller.",
            "keywords": "a near-future lunar colony faces sabotage and political intrigue in this fast-paced sci-fi thriller."
        },
        {
            "title": "You Tell the Story",
            "author": "Ellie Sunwood",
            "url": "reviews/20.html",
            "desc": "A draw-and-write storybook where children look at pictures, then write and draw their own stories.",
            "keywords": "a draw-and-write storybook where children look at pictures, then write and draw their own stories."
        }
    ],
    "stories": [
        {
            "title": "The Ember Song",
            "url": "stories/23.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Last Gift",
            "url": "stories/35.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Humble Mind",
            "url": "stories/9.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Question",
            "url": "stories/19.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "Echoes of the Designed",
            "url": "stories/5.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Last Song",
            "url": "stories/15.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Door Between Worlds",
            "url": "stories/14.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Ones Who Wait",
            "url": "stories/4.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Forgotten Minute",
            "url": "stories/18.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "They Walk Among Us",
            "url": "stories/8.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The First Word",
            "url": "stories/34.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Last Arena",
            "url": "stories/22.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Echoes Return",
            "url": "stories/29.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "What the Silence Knew",
            "url": "stories/3.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Borrowed Life",
            "url": "stories/13.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "Fun at the Beach",
            "url": "stories/25.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Time Auction",
            "url": "stories/33.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "Builds a Robot",
            "url": "stories/32.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Harvest",
            "url": "stories/24.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Disclosure",
            "url": "stories/12.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Last Winter",
            "url": "stories/2.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "City of Wonders",
            "url": "stories/28.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Forbidden Library",
            "url": "stories/11.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Last Signal",
            "url": "stories/1.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Mythical Search",
            "url": "stories/31.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "Learns to Fly",
            "url": "stories/27.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Quiet Town",
            "url": "stories/26.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "American Voices",
            "url": "stories/30.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Other Side",
            "url": "stories/10.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Shadow Garden",
            "url": "stories/21.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "Blood Ties",
            "url": "stories/17.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Space Between",
            "url": "stories/7.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Last Garden",
            "url": "stories/6.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "Rules of the Game",
            "url": "stories/16.html",
            "desc": "",
            "keywords": ""
        },
        {
            "title": "The Sound Between Stars",
            "url": "stories/20.html",
            "desc": "",
            "keywords": ""
        }
    ],
    "articles": []
};

// Popular searches for empty state
const popularSearches = [
    { query: "science fiction", label: "Sci-Fi" },
    { query: "fantasy", label: "Fantasy" },
    { query: "mystery", label: "Mystery" },
    { query: "thriller", label: "Thriller" },
    { query: "nonfiction", label: "Nonfiction" },
    { query: "self-help", label: "Self-Help" }
];

let searchModal = null;
let searchInput = null;
let searchResults = null;
let debounceTimer = null;

function initSearch() {
    if (document.getElementById('searchModal')) return;
    
    const modal = document.createElement('div');
    modal.id = 'searchModal';
    modal.className = 'search-modal';
    modal.style.cssText = 'display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:10000;overflow-y:auto;padding:1rem;';
    
    modal.innerHTML = `
        <div class="search-container" style="max-width:650px;margin:2rem auto;background:var(--surface);border-radius:16px;padding:1.5rem;box-shadow:0 20px 60px rgba(0,0,0,0.5);">
            <div class="search-header" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
                <h2 style="font-size:1.25rem;">🔍 Search</h2>
                <button onclick="closeSearch()" style="background:none;border:none;font-size:1.5rem;cursor:pointer;color:var(--text-dim);padding:0.5rem;">✕</button>
            </div>
            <div class="search-input-wrapper" style="position:relative;margin-bottom:1rem;">
                <input type="text" id="searchInput" placeholder="Search books, stories, articles..." 
                    style="width:100%;padding:1rem 1rem 1rem 2.5rem;font-size:1.1rem;border:2px solid var(--border);border-radius:12px;background:var(--bg);color:var(--text);outline:none;transition:border-color 0.2s;"
                    onfocus="this.style.borderColor='var(--accent)'"
                    onblur="this.style.borderColor='var(--border)'">
                <span style="position:absolute;left:1rem;top:50%;transform:translateY(-50%);color:var(--text-dim);font-size:1rem;">🔎</span>
                <kbd style="position:absolute;right:1rem;top:50%;transform:translateY(-50%);background:var(--surface);padding:0.2rem 0.5rem;border-radius:4px;font-size:0.75rem;color:var(--text-dim);border:1px solid var(--border);">ESC</kbd>
            </div>
            <div id="searchResults" class="search-results" style="max-height:60vh;overflow-y:auto;"></div>
        </div>
    `;
    document.body.appendChild(modal);

    searchModal = modal;
    searchInput = document.getElementById('searchInput');
    searchResults = document.getElementById('searchResults');
    
    searchInput.addEventListener('input', handleSearch);
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeSearch();
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeSearch();
    });
    
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            openSearch();
        }
    });
}

function openSearch() {
    initSearch();
    searchModal.style.display = 'block';
    searchInput.focus();
    showPopularSearches();
}

function closeSearch() {
    if (searchModal) {
        searchModal.style.display = 'none';
    }
}

function showPopularSearches() {
    let html = '<div style="padding:1rem;"><p style="color:var(--text-dim);margin-bottom:1rem;">Popular searches:</p>';
    html += '<div style="display:flex;flex-wrap:wrap;gap:0.5rem;">';
    popularSearches.forEach(ps => {
        html += `<button onclick="searchInput.value='${ps.query}';handleSearch()" style="background:var(--bg);border:1px solid var(--border);border-radius:20px;padding:0.5rem 1rem;cursor:pointer;color:var(--text);font-size:0.9rem;">${ps.label}</button>`;
    });
    html += '</div></div>';
    searchResults.innerHTML = html;
}

function handleSearch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        const query = searchInput.value.toLowerCase().trim();
        if (query.length < 2) {
            showPopularSearches();
            return;
        }
        performSearch(query);
    }, 150);
}

function performSearch(query) {
    const allData = [...siteData.books, ...siteData.stories, ...siteData.articles];
    
    const results = allData.map(item => {
        const titleMatch = item.title.toLowerCase().includes(query);
        const descMatch = item.desc && item.desc.toLowerCase().includes(query);
        const keywordsMatch = item.keywords && item.keywords.toLowerCase().includes(query);
        const authorMatch = item.author && item.author.toLowerCase().includes(query);
        
        let score = 0;
        if (titleMatch) score += 10;
        if (descMatch) score += 5;
        if (keywordsMatch) score += 3;
        if (authorMatch) score += 5;
        
        return { ...item, score };
    }).filter(item => item.score > 0)
      .sort((a, b) => b.score - a.score);
    
    displayResults(results, query);
}

function highlightMatch(text, query) {
    if (!query) return text;
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark style="background:var(--accent);color:white;padding:0 0.2rem;border-radius:2px;">$1</mark>');
}

function displayResults(results, query) {
    if (results.length === 0) {
        searchResults.innerHTML = '<div style="padding:2rem;text-align:center;color:var(--text-dim);">No results found. Try different keywords.</div>';
        return;
    }
    
    const books = results.filter(r => r.url && r.url.startsWith('reviews/'));
    const stories = results.filter(r => r.url && r.url.startsWith('stories/'));
    const articles = results.filter(r => r.url && !r.url.startsWith('reviews/') && !r.url.startsWith('stories/'));
    
    let html = '';
    
    if (books.length > 0) {
        html += '<div style="margin-bottom:1.5rem;"><h4 style="color:var(--accent);font-size:0.85rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.75rem;">📚 Books</h4>';
        books.forEach(book => {
            html += `<a href="${book.url}" style="display:block;padding:0.75rem;margin-bottom:0.5rem;background:var(--bg);border-radius:8px;text-decoration:none;color:var(--text);transition:transform 0.2s;" onmouseover="this.style.transform='translateX(4px)'">
                <div style="font-weight:600;font-size:1rem;">${highlightMatch(book.title, query)}${book.author ? ' <span style="color:var(--text-dim);font-weight:normal;">by ' + book.author + '</span>' : ''}</div>
                <div style="color:var(--text-dim);font-size:0.85rem;margin-top:0.25rem;">${book.desc.substring(0, 80)}...</div>
            </a>`;
        });
        html += '</div>';
    }
    
    if (stories.length > 0) {
        html += '<div style="margin-bottom:1.5rem;"><h4 style="color:var(--accent);font-size:0.85rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.75rem;">📖 Stories</h4>';
        stories.forEach(story => {
            html += `<a href="${story.url}" style="display:block;padding:0.75rem;margin-bottom:0.5rem;background:var(--bg);border-radius:8px;text-decoration:none;color:var(--text);" onmouseover="this.style.transform='translateX(4px)'">
                <div style="font-weight:600;font-size:1rem;">${highlightMatch(story.title, query)}</div>
                <div style="color:var(--text-dim);font-size:0.85rem;margin-top:0.25rem;">${story.desc.substring(0, 80)}...</div>
            </a>`;
        });
        html += '</div>';
    }
    
    if (articles.length > 0) {
        html += '<div><h4 style="color:var(--accent);font-size:0.85rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.75rem;">📰 Articles</h4>';
        articles.forEach(article => {
            html += `<a href="${article.url}" style="display:block;padding:0.75rem;margin-bottom:0.5rem;background:var(--bg);border-radius:8px;text-decoration:none;color:var(--text);" onmouseover="this.style.transform='translateX(4px)'">
                <div style="font-weight:600;font-size:1rem;">${highlightMatch(article.title, query)}</div>
            </a>`;
        });
        html += '</div>';
    }
    
    searchResults.innerHTML = html;
}

function addSearchButton() {
    const navDiv = document.querySelector('nav > div');
    if (navDiv && !document.querySelector('.search-btn')) {
        const searchBtn = document.createElement('button');
        searchBtn.className = 'search-btn';
        searchBtn.innerHTML = '🔍';
        searchBtn.title = 'Search (Ctrl+K)';
        searchBtn.style.cssText = 'background:none;border:none;font-size:1rem;cursor:pointer;color:var(--text-dim);padding:0 0.5rem;margin-left:0.5rem;';
        searchBtn.onclick = openSearch;
        navDiv.appendChild(searchBtn);
    }
}

document.addEventListener('DOMContentLoaded', addSearchButton);
