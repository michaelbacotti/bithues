// Site Search Functionality
// Searches through books and articles

const siteData = {
    books: [
        { title: "The Dawn of Civilization", author: "T. Stone", category: "Fiction", url: "reviews/1.html", keywords: "prehistoric tribal survival ancient" },
        { title: "The Richmond Cipher", author: "Jonathan Richmond", category: "Fiction", url: "reviews/2.html", keywords: "mystery cipher codes" },
        { title: "Red Horizon: Lunar Launch", author: "Michael H. Martin", category: "Fiction", url: "reviews/3.html", keywords: "space moon sci-fi" },
        { title: "The Confluence Doctrine", author: "E.C. Stroud", category: "Nonfiction", url: "reviews/4.html", keywords: "spirituality consciousness" },
        { title: "Living with a Moving Planet", author: "David W. R. H.", category: "Nonfiction", url: "reviews/5.html", keywords: "earth nature environment" },
        { title: "Beyond the Veil", author: "E.C. Stroud", category: "Fiction", url: "reviews/6.html", keywords: "spiritual fiction intuition" },
        { title: "Veiled Presence", author: "E.C. Stroud", category: "Nonfiction", url: "reviews/7.html", keywords: "intuition awareness mindfulness" },
        { title: "The Power of Changing Your Mind", author: "Jane Smith", category: "Nonfiction", url: "reviews/8.html", keywords: "mindset psychology change" },
        { title: "The Shadow Within", author: "Luna Meridian", category: "Fiction", url: "reviews/9.html", keywords: "dark fantasy shadow" },
        { title: "Echoes of Aetheris", author: "Marcus Chen", category: "Fiction", url: "reviews/10.html", keywords: "fantasy epic magic" },
        { title: "Disclosure 2026", author: "Unknown", category: "Nonfiction", url: "reviews/11.html", keywords: "aliens ufo disclosure" },
        { title: "Resonance Drift", author: "Sarah Webb", category: "Fiction", url: "reviews/12.html", keywords: "sci-fi space physics" },
        { title: "Symbiont Bloom", author: "Dr. Alex Kim", category: "Fiction", url: "reviews/13.html", keywords: "aliens biology sci-fi" },
        { title: "Otomí", author: "Maria Santos", category: "Fiction", url: "reviews/14.html", keywords: "mexico magical realism" },
        { title: "Physics of Insight", author: "Dr. James Chen", category: "Nonfiction", url: "reviews/15.html", keywords: "physics science" },
        { title: "The Physics of Time", author: "David Park", category: "Nonfiction", url: "reviews/16.html", keywords: "time physics quantum" },
        { title: "Consciousness in Higher Dimensional Spacetime", author: "Dr. Emily Wu", category: "Nonfiction", url: "reviews/17.html", keywords: "consciousness dimensions physics" },
        { title: "Quantum Soul Echoes", author: "Michael Torres", category: "Nonfiction", url: "reviews/18.html", keywords: "quantum spirituality soul" },
        { title: "Microbiology ABC's", author: "Dr. Lisa Park", category: "Nonfiction", url: "reviews/19.html", keywords: "science microbiology kids" },
        { title: "You Tell the Story", author: "Rachel Green", category: "Nonfiction", url: "reviews/20.html", keywords: "storytelling writing narrative" },
        { title: "The Burning Song", author: "Aria Storm", category: "Fiction", url: "reviews/21.html", keywords: "fantasy epic fire" },
        { title: "Mindful Memory", author: "Dr. Sarah Lee", category: "Nonfiction", url: "reviews/22.html", keywords: "memory mindfulness psychology" },
        { title: "Shadow Work Journal for Women", author: "Elena Moon", category: "Nonfiction", url: "reviews/23.html", keywords: "journal self-help shadow work" },
        { title: "Rules of Survival", author: "Jack Carter", category: "Fiction", url: "reviews/24.html", keywords: "thriller survival action" },
        { title: "Blood Ember", author: "Vera Blackwood", category: "Fiction", url: "reviews/25.html", keywords: "fantasy dark vampire" }
    ],
    articles: [
        { title: "Best Sci-Fi Books 2026", url: "articles/best-sci-fi-2026.html", keywords: "sci-fi science fiction recommendations 2026" },
        { title: "Hopepunk Beginner's Guide", url: "articles/hopepunk-beginners-guide.html", keywords: "hopepunk genre optimistic" },
        { title: "How to Read More Books", url: "articles/how-to-read-more-books.html", keywords: "reading tips speed" },
        { title: "Speed Reading Basics", url: "articles/speed-reading-basics.html", keywords: "speed reading tips" },
        { title: "Read More This Year", url: "articles/read-more-this-year.html", keywords: "reading goals new year" },
        { title: "Why Indie Authors Are Rising", url: "articles/why-indie-authors-rising.html", keywords: "indie authors self-publish" },
        { title: "Meet Indie Authors", url: "articles/meet-indie-authors.html", keywords: "indie authors interviews" },
        { title: "How We Review Books", url: "articles/how-we-review-books.html", keywords: "reviews methodology" },
        { title: "Books for Dad Gift Guide", url: "articles/books-for-dad-gift-guide.html", keywords: "gifts father dad" },
        { title: "Quantum Physics Beginners", url: "articles/quantum-physics-beginners-guide.html", keywords: "quantum physics science" },
        { title: "Best Books Spring 2026", url: "articles/best-books-spring-2026.html", keywords: "spring reading recommendations" },
        { title: "Best Books Summer 2026", url: "articles/best-books-summer-2026.html", keywords: "summer reading recommendations" },
        { title: "Reading Challenge 2026", url: "articles/reading-challenge-2026.html", keywords: "reading challenge goals" },
        { title: "Books Like The Physics of Time", url: "articles/books-like-physics-of-time.html", keywords: "physics time recommendations" },
        { title: "Books Like Project Hail Mary", url: "articles/books-like-project-hail-mary.html", keywords: "sci-fi space recommendations" },
        { title: "Why Read Outside Your Genre", url: "articles/why-read-outside-your-genre.html", keywords: "genre reading advice" },
        { title: "Fantasy for Beginners", url: "articles/fantasy-for-beginners.html", keywords: "fantasy guide入门" },
        { title: "Thriller and Mystery Guide", url: "articles/thriller-mystery-guide.html", keywords: "thriller mystery suspense" },
        { title: "Horror for Beginners", url: "articles/horror-for-beginners.html", keywords: "horror scary fear" },
        { title: "Romance for Beginners", url: "articles/romance-for-beginners.html", keywords: "romance love relationship" },
        { title: "Memoir and Biography Guide", url: "articles/memoir-biography-guide.html", keywords: "memoir biography life" },
        { title: "Business and Leadership Guide", url: "articles/business-leadership-guide.html", keywords: "business leadership management" }
    ]
};

let searchModal = null;
let searchInput = null;
let searchResults = null;

function initSearch() {
    // Create modal if it doesn't exist
    if (!document.getElementById('searchModal')) {
        const modal = document.createElement('div');
        modal.id = 'searchModal';
        modal.className = 'search-modal';
        modal.style.cssText = 'display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:1000;overflow-y:auto;';
        modal.innerHTML = `
            <div class="search-container" style="max-width:600px;margin:50px auto;padding:2rem;background:var(--surface);border-radius:12px;">
                <div class="search-header" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">
                    <h2 style="font-size:1.5rem;">Search Books & Articles</h2>
                    <button onclick="closeSearch()" style="background:none;border:none;font-size:1.5rem;cursor:pointer;color:var(--text-dim);">&times;</button>
                </div>
                <input type="text" id="searchInput" placeholder="Search for books, articles, authors..." 
                    style="width:100%;padding:1rem;font-size:1rem;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text);margin-bottom:1rem;">
                <div id="searchResults" class="search-results"></div>
            </div>
        `;
        document.body.appendChild(modal);
        
        searchInput = document.getElementById('searchInput');
        searchResults = document.getElementById('searchResults');
        
        searchInput.addEventListener('input', performSearch);
    }
    
    // Add keyboard shortcut (Cmd/Ctrl + K)
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
        resultsDiv.innerHTML = '<p style="color:var(--text-dim);">Type at least 2 characters to search...</p>';
        return;
    }
    
    let results = { books: [], articles: [] };
    
    // Search books
    siteData.books.forEach(book => {
        const searchText = (book.title + ' ' + book.author + ' ' + book.keywords).toLowerCase();
        if (searchText.includes(query)) {
            results.books.push(book);
        }
    });
    
    // Search articles
    siteData.articles.forEach(article => {
        const searchText = (article.title + ' ' + article.keywords).toLowerCase();
        if (searchText.includes(query)) {
            results.articles.push(article);
        }
    });
    
    // Render results
    let html = '';
    
    if (results.books.length === 0 && results.articles.length === 0) {
        html = '<p style="color:var(--text-dim);">No results found. Try different keywords.</p>';
    }
    
    if (results.books.length > 0) {
        html += '<h3 style="font-size:1rem;margin:1rem 0 0.5rem;color:var(--accent);">Books (' + results.books.length + ')</h3>';
        results.books.forEach(book => {
            html += `<a href="${book.url}" class="search-result-item" style="display:block;padding:0.75rem;border-bottom:1px solid var(--border);text-decoration:none;color:var(--text);">
                <strong>${book.title}</strong>
                <span style="color:var(--text-dim);font-size:0.85rem;"> by ${book.author}</span>
                <span style="color:var(--accent);font-size:0.75rem;margin-left:0.5rem;">${book.category}</span>
            </a>`;
        });
    }
    
    if (results.articles.length > 0) {
        html += '<h3 style="font-size:1rem;margin:1rem 0 0.5rem;color:var(--accent);">Articles (' + results.articles.length + ')</h3>';
        results.articles.forEach(article => {
            html += `<a href="${article.url}" class="search-result-item" style="display:block;padding:0.75rem;border-bottom:1px solid var(--border);text-decoration:none;color:var(--text);">
                <strong>${article.title}</strong>
            </a>`;
        });
    }
    
    resultsDiv.innerHTML = html;
}

// Add search button to nav
function addSearchButton() {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks && !document.querySelector('.search-btn')) {
        const searchBtn = document.createElement('button');
        searchBtn.className = 'search-btn';
        searchBtn.innerHTML = '🔍';
        searchBtn.title = 'Search (Ctrl+K)';
        searchBtn.style.cssText = 'background:none;border:none;font-size:1rem;cursor:pointer;color:var(--text-dim);padding:0 0.5rem;';
        searchBtn.onclick = openSearch;
        navLinks.insertBefore(searchBtn, navLinks.firstChild);
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', addSearchButton);
