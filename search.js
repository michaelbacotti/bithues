// Site Search Functionality
// Searches through books, articles, and stories

const siteData = {
    books: [{"title": "Shadow Work Journal for Women", "author": "Luna Sage", "category": "Book", "url": "reviews/23.html", "keywords": "A beginner-friendly 90-day journal with warm prompts for emotional healing."}, {"title": "Time Investing", "author": "H Harvey", "category": "Book", "url": "reviews/35.html", "keywords": "A self-help guide showing how to prioritize yourself and your time. Strategies for investing in your"}, {"title": "The Shadow Within", "author": "Elena Maris", "category": "Book", "url": "reviews/9.html", "keywords": "Instead of treating reactions as defects, learn to treat them as information—and respond differently"}, {"title": "Microbiology ABC&#x27;s", "author": "Michael Bacotti", "category": "Book", "url": "reviews/19.html", "keywords": "From amoebas to zooplankton, each letter highlights a microbe or cell structure with colorful illust"}, {"title": "Living with a Moving Planet", "author": "J. T. Hartley", "category": "Book", "url": "reviews/5.html", "keywords": "Drawing on deep-time climate records and archaeology, this book shows how humans have adapted to cha"}, {"title": "Physics of Insight", "author": "Quantum Chronos", "category": "Book", "url": "reviews/15.html", "keywords": "What if genius isn&#x27;t rare—it&#x27;s hidden inside every mind, waiting for the right switch?"}, {"title": "The Power of Changing Your Mind", "author": "Evan R. A. Cole", "category": "Book", "url": "reviews/the-power-of-changing-your-mind.html", "keywords": "A practical guide to intellectual humility and how it improves decisions, relationships, and everyda"}, {"title": "Otomí", "author": "E. J. Marín", "category": "Book", "url": "reviews/14.html", "keywords": "Through the eyes of a young ritual apprentice, follow one drought-stricken year in an Otomí village."}, {"title": "The Confluence Doctrine", "author": "Alaric Wynn", "category": "Book", "url": "reviews/4.html", "keywords": "In a world where suffering has been designed out, Orren Myal hears something that doesn&#x27;t fit—a"}, {"title": "The Confluence Doctrine | Bithues Reading Lab</title>\n    <style>\n        * { margin: 0; padding: 0; box-sizing: border-box; }\n        [data-theme=\"light\"] { --bg: #f5f5f5; --surface: #ffffff; --border: #e0e0e0; --text: #1a1a1a; --text-dim: #666666; } :root { --bg: #0a0a0f; --surface: #12121a; --border: #2a2a3a; --text: #e8e8f0; --text-dim: #7a7a90; --accent: #7c3aed; }\n        body { transition: background 0.3s, color 0.3s; font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; }\n        .container { max-width: 700px; margin: 0 auto; padding: 0 1.5rem; }\n        header, footer { padding: 2rem 0; border-bottom: 1px solid var(--border); text-align: center; }\n        nav { padding: 1rem 0; }\n        .logo { font-size: 1.25rem; font-weight: 700; color: var(--text); text-decoration: none; }\n        .logo span { color: var(--accent); }\n        .nav-links { margin-top: 1rem; }\n        .nav-links a { color: var(--text-dim); text-decoration: none; font-size: 0.9rem; margin: 0 0.75rem; }\n        .review { padding: 3rem 0; }\n        .back-link { display: inline-block; margin-bottom: 2rem; color: var(--accent); text-decoration: none; font-size: 0.9rem; }\n        h1 { font-size: 1.75rem; margin-bottom: 0.5rem; }\n        .author { color: var(--text-dim); font-size: 1.1rem; margin-bottom: 1.5rem; }\n        .tldr { font-size: 1.15rem; margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid var(--border); }\n        h2 { font-size: 1.25rem; margin-bottom: 1rem; }\n        ul { list-style: none; margin-bottom: 2rem; }\n        li { padding: 0.75rem 0; border-bottom: 1px solid var(--border); }\n        .who, .verdict, .affiliate { padding: 1.5rem; background: var(--surface); border-radius: 8px; border: 1px solid var(--border); margin-bottom: 1.5rem; }\n        .affiliate { border-color: var(--accent); text-align: center; }\n        .affiliate p { color: var(--text-dim); margin-bottom: 1rem; }\n        .affiliate a { display: inline-block; padding: 0.75rem 1.5rem; background: var(--accent); color: white; text-decoration: none; border-radius: 6px; }\n    .similar-books { padding: 2rem 0; border-top: 1px solid var(--border); margin-top: 2rem; }\n.similar-books h2 { font-size: 1.5rem; margin-bottom: 1.5rem; }\n.similar-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }\n.similar-card { padding: 1rem; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; }\n.similar-card h3 { font-size: 1rem; margin-bottom: 0.3rem; }\n.similar-card h3 a { color: var(--text); text-decoration: none; }\n.similar-card h3 a:hover { color: var(--accent); }\n.similar-card .author { color: var(--text-dim); font-size: 0.85rem; }\n</style>\n\n    <script type=\"application/ld+json\">\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"Book\",\n  \"name\": \"The Confluence Doctrine | Bithues Reading ...,
    articles: [{"title": "The Ember Song", "url": "stories/23.html", "keywords": ""}, {"title": "The Last Gift", "url": "stories/35.html", "keywords": ""}, {"title": "The Humble Mind", "url": "stories/9.html", "keywords": ""}, {"title": "The Question", "url": "stories/19.html", "keywords": ""}, {"title": "Echoes of the Designed", "url": "stories/5.html", "keywords": ""}, {"title": "The Last Song", "url": "stories/15.html", "keywords": ""}, {"title": "The Door Between Worlds", "url": "stories/14.html", "keywords": ""}, {"title": "The Ones Who Wait", "url": "stories/4.html", "keywords": ""}, {"title": "The Forgotten Minute", "url": "stories/18.html", "keywords": ""}, {"title": "They Walk Among Us", "url": "stories/8.html", "keywords": ""}, {"title": "The First Word", "url": "stories/34.html", "keywords": ""}, {"title": "The Last Arena", "url": "stories/22.html", "keywords": ""}, {"title": "The Echoes Return", "url": "stories/29.html", "keywords": ""}, {"title": "What the Silence Knew", "url": "stories/3.html", "keywords": ""}, {"title": "The Borrowed Life", "url": "stories/13.html", "keywords": ""}, {"title": "Fun at the Beach", "url": "stories/25.html", "keywords": ""}, {"title": "The Time Auction", "url": "stories/33.html", "keywords": ""}, {"title": "Builds a Robot", "url": "stories/32.html", "keywords": ""}, {"title": "The Harvest", "url": "stories/24.html", "keywords": ""}, {"title": "The Disclosure", "url": "stories/12.html", "keywords": ""}, {"title": "The Last Winter", "url": "stories/2.html", "keywords": ""}, {"title": "City of Wonders", "url": "stories/28.html", "keywords": ""}, {"title": "The Forbidden Library", "url": "stories/11.html", "keywords": ""}, {"title": "The Last Signal", "url": "stories/1.html", "keywords": ""}, {"title": "The Mythical Search", "url": "stories/31.html", "keywords": ""}, {"title": "Learns to Fly", "url": "stories/27.html", "keywords": ""}, {"title": "The Quiet Town", "url": "stories/26.html", "keywords": ""}, {"title": "American Voices", "url": "stories/30.html", "keywords": ""}, {"title": "The Other Side", "url": "stories/10.html", "keywords": ""}, {"title": "The Shadow Garden", "url": "stories/21.html", "keywords": ""}, {"title": "Blood Ties", "url": "stories/17.html", "keywords": ""}, {"title": "The Space Between", "url": "stories/7.html", "keywords": ""}, {"title": "The Last Garden", "url": "stories/6.html", "keywords": ""}, {"title": "Rules of the Game", "url": "stories/16.html", "keywords": ""}, {"title": "The Sound Between Stars", "url": "stories/20.html", "keywords": ""}]...,
    stories: [
        { title: "The Last Signal", url: "stories/1.html", keywords: "sci-fi space adventure" },
        { title: "Echoes of Tomorrow", url: "stories/2.html", keywords: "time travel sci-fi" },
        { title: "The Shadow Garden", url: "stories/3.html", keywords: "mystery thriller" },
    ]
};

// Add more stories from search-index.json
siteData.stories = [{"title": "The Ember Song", "url": "stories/23.html", "keywords": ""}, {"title": "The Last Gift", "url": "stories/35.html", "keywords": ""}, {"title": "The Humble Mind", "url": "stories/9.html", "keywords": ""}, {"title": "The Question", "url": "stories/19.html", "keywords": ""}, {"title": "Echoes of the Designed", "url": "stories/5.html", "keywords": ""}, {"title": "The Last Song", "url": "stories/15.html", "keywords": ""}, {"title": "The Door Between Worlds", "url": "stories/14.html", "keywords": ""}, {"title": "The Ones Who Wait", "url": "stories/4.html", "keywords": ""}, {"title": "The Forgotten Minute", "url": "stories/18.html", "keywords": ""}, {"title": "They Walk Among Us", "url": "stories/8.html", "keywords": ""}, {"title": "The First Word", "url": "stories/34.html", "keywords": ""}, {"title": "The Last Arena", "url": "stories/22.html", "keywords": ""}, {"title": "The Echoes Return", "url": "stories/29.html", "keywords": ""}, {"title": "What the Silence Knew", "url": "stories/3.html", "keywords": ""}, {"title": "The Borrowed Life", "url": "stories/13.html", "keywords": ""}, {"title": "Fun at the Beach", "url": "stories/25.html", "keywords": ""}, {"title": "The Time Auction", "url": "stories/33.html", "keywords": ""}, {"title": "Builds a Robot", "url": "stories/32.html", "keywords": ""}, {"title": "The Harvest", "url": "stories/24.html", "keywords": ""}, {"title": "The Disclosure", "url": "stories/12.html", "keywords": ""}, {"title": "The Last Winter", "url": "stories/2.html", "keywords": ""}, {"title": "City of Wonders", "url": "stories/28.html", "keywords": ""}, {"title": "The Forbidden Library", "url": "stories/11.html", "keywords": ""}, {"title": "The Last Signal", "url": "stories/1.html", "keywords": ""}, {"title": "The Mythical Search", "url": "stories/31.html", "keywords": ""}, {"title": "Learns to Fly", "url": "stories/27.html", "keywords": ""}, {"title": "The Quiet Town", "url": "stories/26.html", "keywords": ""}, {"title": "American Voices", "url": "stories/30.html", "keywords": ""}, {"title": "The Other Side", "url": "stories/10.html", "keywords": ""}, {"title": "The Shadow Garden", "url": "stories/21.html", "keywords": ""}, {"title": "Blood Ties", "url": "stories/17.html", "keywords": ""}, {"title": "The Space Between", "url": "stories/7.html", "keywords": ""}, {"title": "The Last Garden", "url": "stories/6.html", "keywords": ""}, {"title": "Rules of the Game", "url": "stories/16.html", "keywords": ""}, {"title": "The Sound Between Stars", "url": "stories/20.html", "keywords": ""}];

let searchModal = null;
let searchInput = null;
let searchResults = null;

function initSearch() {
    if (!document.getElementById('searchModal')) {
        const modal = document.createElement('div');
        modal.id = 'searchModal';
        modal.className = 'search-modal';
        modal.style.cssText = 'display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:1000;overflow-y:auto;';
        modal.innerHTML = `
            <div class="search-container" style="max-width:600px;margin:50px auto;padding:2rem;background:var(--surface);border-radius:12px;">
                <div class="search-header" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">
                    <h2 style="font-size:1.5rem;">🔍 Search Books, Stories & Articles</h2>
                    <button onclick="closeSearch()" style="background:none;border:none;font-size:1.5rem;cursor:pointer;color:var(--text-dim);">&times;</button>
                </div>
                <input type="text" id="searchInput" placeholder="Try: 'space books' or 'fantasy adventure'..." 
                    style="width:100%;padding:1rem;font-size:1rem;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text);margin-bottom:1rem;">
                <div id="searchResults" class="search-results" style="max-height:400px;overflow-y:auto;"></div>
            </div>
        `;
        document.body.appendChild(modal);
        
        searchInput = document.getElementById('searchInput');
        searchResults = document.getElementById('searchResults');
        
        searchInput.addEventListener('input', performSearch);
    }
    
    document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            openSearch();
        }
        if (e.key === 'Escape') {
            closeSearch();
        }
    });
}

function openSearch() {
    initSearch();
    const modal = document.getElementById('searchModal');
    modal.style.display = 'block';
    document.getElementById('searchInput').focus();
    document.body.style.overflow = 'hidden';
}

function closeSearch() {
    const modal = document.getElementById('searchModal');
    if (modal) {
        modal.style.display = 'none';
    }
    document.body.style.overflow = '';
}

function performSearch() {
    const query = searchInput.value.toLowerCase().trim();
    const resultsDiv = document.getElementById('searchResults');
    
    if (query.length < 2) {
        resultsDiv.innerHTML = '<p style="color:var(--text-dim);padding:1rem;">Type at least 2 characters to search... <br><small style="color:var(--accent);">Try: "space", "fantasy", "thriller"</small></p>';
        return;
    }
    
    let results = { books: [], articles: [], stories: [] };
    
    // Search books (fuzzy match)
    siteData.books.forEach(book => {
        const searchText = (book.title + ' ' + book.author + ' ' + (book.keywords || '')).toLowerCase();
        if (searchText.includes(query) || fuzzyMatch(query, searchText)) {
            results.books.push(book);
        }
    });
    
    // Search articles
    siteData.articles.forEach(article => {
        const searchText = (article.title + ' ' + (article.keywords || '')).toLowerCase();
        if (searchText.includes(query) || fuzzyMatch(query, searchText)) {
            results.articles.push(article);
        }
    });
    
    // Search stories
    if (siteData.stories) {
        siteData.stories.forEach(story => {
            const searchText = (story.title + ' ' + (story.keywords || '')).toLowerCase();
            if (searchText.includes(query) || fuzzyMatch(query, searchText)) {
                results.stories.push(story);
            }
        });
    }
    
    // Render results
    let html = '';
    
    if (results.books.length === 0 && results.articles.length === 0 && results.stories.length === 0) {
        html = '<p style="color:var(--text-dim);padding:1rem;">No results found. Try different keywords.</p>';
    }
    
    if (results.books.length > 0) {
        html += '<h3 style="font-size:1rem;margin:1rem 0 0.5rem;color:var(--accent);">📚 Books (' + results.books.length + ')</h3>';
        results.books.slice(0, 5).forEach(book => {
            html += `<a href="${book.url}" style="display:block;padding:0.75rem;border-bottom:1px solid var(--border);text-decoration:none;color:var(--text);">
                <strong>${book.title}</strong>
                <span style="color:var(--text-dim);font-size:0.85rem;"> by ${book.author}</span>
            </a>`;
        });
    }
    
    if (results.stories && results.stories.length > 0) {
        html += '<h3 style="font-size:1rem;margin:1rem 0 0.5rem;color:var(--accent);">📖 Stories (' + results.stories.length + ')</h3>';
        results.stories.slice(0, 5).forEach(story => {
            html += `<a href="${story.url}" style="display:block;padding:0.75rem;border-bottom:1px solid var(--border);text-decoration:none;color:var(--text);">
                <strong>${story.title}</strong>
            </a>`;
        });
    }
    
    if (results.articles.length > 0) {
        html += '<h3 style="font-size:1rem;margin:1rem 0 0.5rem;color:var(--accent);">📰 Articles (' + results.articles.length + ')</h3>';
        results.articles.slice(0, 5).forEach(article => {
            html += `<a href="${article.url}" style="display:block;padding:0.75rem;border-bottom:1px solid var(--border);text-decoration:none;color:var(--text);">
                <strong>${article.title}</strong>
            </a>`;
        });
    }
    
    resultsDiv.innerHTML = html;
}

function fuzzyMatch(query, text) {
    // Simple fuzzy matching - checks if all chars appear in order
    let queryIdx = 0;
    for (let i = 0; i < text.length && queryIdx < query.length; i++) {
        if (text[i] === query[queryIdx]) {
            queryIdx++;
        }
    }
    return queryIdx === query.length;
}

function addSearchButton() {
    const navDiv = document.querySelector('nav > div');
    if (navDiv && !document.querySelector('.search-btn')) {
        const searchBtn = document.createElement('button');
        searchBtn.className = 'search-btn';
        searchBtn.innerHTML = '🔍';
        searchBtn.title = 'Search (Ctrl+K)';
        searchBtn.style.cssText = 'background:none;border:none;font-size:1rem;cursor:pointer;color:var(--text-dim);padding:0 0.5rem;';
        searchBtn.onclick = openSearch;
        navDiv.insertBefore(searchBtn, navDiv.firstChild);
    }
}

document.addEventListener('DOMContentLoaded', addSearchButton);
