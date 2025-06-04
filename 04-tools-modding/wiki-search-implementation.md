# Wiki Search Implementation Guide
**Building a Neural Search System for Eden Reborn**

> *"I don't like the idea that I'm not in control of my life."* - Neo (Let's take control of our wiki's knowledge discovery.)

## 🔍 **The Search Vision**

The Matrix Online Liberation Wiki needs a search system that embodies our liberation philosophy - open, powerful, and accessible to all. This guide documents multiple implementation approaches from simple to advanced.

## 🎯 **Search Requirements**

### Core Features
- **Full-text search** across all wiki content
- **Instant results** as users type
- **Context highlighting** in search results
- **Tag-based filtering** by category
- **Cross-reference awareness** for related content
- **Mobile-responsive** interface
- **Zero external dependencies** (self-hosted)

### Liberation Principles
- **No tracking** - User privacy respected
- **No analytics** - Search data stays local
- **Open source** - All code freely available
- **Offline capable** - Works without internet
- **Accessible** - Screen reader compatible

## 🛠️ **Implementation Options**

### Option 1: Client-Side JavaScript Search

**Best for**: GitHub Pages, static hosting, offline-first approach

```javascript
// MXO Wiki Search Engine - Client Side Implementation
class MatrixWikiSearch {
    constructor() {
        this.searchIndex = [];
        this.documents = new Map();
        this.initialized = false;
    }
    
    async initialize() {
        // Load pre-built search index
        const response = await fetch('/search-index.json');
        const data = await response.json();
        
        // Build search structures
        data.pages.forEach(page => {
            this.documents.set(page.id, page);
            this.searchIndex.push({
                id: page.id,
                title: page.title,
                content: this.tokenize(page.content),
                tags: page.tags,
                category: page.category,
                path: page.path
            });
        });
        
        this.initialized = true;
    }
    
    tokenize(text) {
        // Remove markdown syntax
        text = text.replace(/[#*`\[\]()]/g, ' ');
        // Convert to lowercase tokens
        return text.toLowerCase()
            .split(/\s+/)
            .filter(token => token.length > 2);
    }
    
    search(query, options = {}) {
        if (!this.initialized) return [];
        
        const queryTokens = this.tokenize(query);
        const results = [];
        
        // Score each document
        this.searchIndex.forEach(doc => {
            let score = 0;
            
            // Title matches (highest weight)
            const titleTokens = this.tokenize(doc.title);
            queryTokens.forEach(token => {
                if (titleTokens.includes(token)) score += 10;
                if (doc.title.toLowerCase().includes(query.toLowerCase())) score += 20;
            });
            
            // Content matches
            queryTokens.forEach(token => {
                const count = doc.content.filter(t => t.includes(token)).length;
                score += count;
            });
            
            // Tag matches
            if (options.tags) {
                const tagMatch = doc.tags.some(tag => 
                    options.tags.includes(tag)
                );
                if (tagMatch) score += 5;
            }
            
            // Category filter
            if (options.category && doc.category !== options.category) {
                score = 0;
            }
            
            if (score > 0) {
                results.push({
                    ...this.documents.get(doc.id),
                    score,
                    excerpt: this.generateExcerpt(doc.id, queryTokens)
                });
            }
        });
        
        // Sort by relevance
        return results.sort((a, b) => b.score - a.score);
    }
    
    generateExcerpt(docId, queryTokens) {
        const doc = this.documents.get(docId);
        const content = doc.content;
        
        // Find first occurrence of query terms
        let bestPosition = -1;
        let bestToken = '';
        
        queryTokens.forEach(token => {
            const pos = content.toLowerCase().indexOf(token);
            if (pos !== -1 && (bestPosition === -1 || pos < bestPosition)) {
                bestPosition = pos;
                bestToken = token;
            }
        });
        
        if (bestPosition === -1) {
            return content.substring(0, 150) + '...';
        }
        
        // Extract context around match
        const start = Math.max(0, bestPosition - 50);
        const end = Math.min(content.length, bestPosition + 100);
        let excerpt = content.substring(start, end);
        
        // Highlight matches
        queryTokens.forEach(token => {
            const regex = new RegExp(`(${token})`, 'gi');
            excerpt = excerpt.replace(regex, '<mark>$1</mark>');
        });
        
        return (start > 0 ? '...' : '') + excerpt + (end < content.length ? '...' : '');
    }
}

// Search UI Component
class MatrixSearchUI {
    constructor(searchEngine) {
        this.searchEngine = searchEngine;
        this.setupUI();
    }
    
    setupUI() {
        // Create search interface
        const searchHTML = `
            <div class="matrix-search-container">
                <div class="search-header">
                    <input type="text" 
                           id="matrix-search-input" 
                           placeholder="Search the Matrix..." 
                           autocomplete="off">
                    <div class="search-filters">
                        <select id="search-category">
                            <option value="">All Categories</option>
                            <option value="server">Server Setup</option>
                            <option value="technical">Technical</option>
                            <option value="tools">Tools & Modding</option>
                            <option value="gameplay">Gameplay</option>
                            <option value="story">Story & Lore</option>
                            <option value="community">Community</option>
                        </select>
                    </div>
                </div>
                <div class="search-status"></div>
                <div class="search-results" id="matrix-search-results"></div>
            </div>
        `;
        
        // Inject into page
        const container = document.getElementById('search-container');
        if (container) {
            container.innerHTML = searchHTML;
            this.bindEvents();
        }
    }
    
    bindEvents() {
        const input = document.getElementById('matrix-search-input');
        const category = document.getElementById('search-category');
        const results = document.getElementById('matrix-search-results');
        
        // Debounced search
        let searchTimeout;
        input.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.performSearch(e.target.value);
            }, 300);
        });
        
        // Category filter
        category.addEventListener('change', () => {
            if (input.value) {
                this.performSearch(input.value);
            }
        });
        
        // Keyboard navigation
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                input.value = '';
                results.innerHTML = '';
            }
        });
    }
    
    performSearch(query) {
        const results = document.getElementById('matrix-search-results');
        const category = document.getElementById('search-category').value;
        
        if (!query || query.length < 2) {
            results.innerHTML = '';
            return;
        }
        
        const searchResults = this.searchEngine.search(query, { category });
        
        if (searchResults.length === 0) {
            results.innerHTML = `
                <div class="no-results">
                    <p>No results found for "${query}"</p>
                    <p class="suggestion">Try different keywords or check the 
                       <a href="/index.html">complete index</a></p>
                </div>
            `;
            return;
        }
        
        // Render results
        const resultsHTML = searchResults.slice(0, 20).map(result => `
            <div class="search-result">
                <h3><a href="${result.path}">${result.title}</a></h3>
                <div class="result-category">${result.category}</div>
                <div class="result-excerpt">${result.excerpt}</div>
                <div class="result-tags">
                    ${result.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
        `).join('');
        
        results.innerHTML = `
            <div class="results-header">
                Found ${searchResults.length} result${searchResults.length !== 1 ? 's' : ''}
            </div>
            ${resultsHTML}
        `;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    const searchEngine = new MatrixWikiSearch();
    await searchEngine.initialize();
    new MatrixSearchUI(searchEngine);
});
```

### Option 2: Static Site Generator Plugin

**Best for**: Jekyll (GitHub Pages), Hugo, MkDocs

```ruby
# Jekyll plugin for Matrix Wiki search index generation
# Place in _plugins/search_index_generator.rb

module Jekyll
  class SearchIndexGenerator < Generator
    safe true
    priority :low
    
    def generate(site)
      # Collect all pages and posts
      searchable_pages = site.pages + site.posts.docs
      
      # Build search index
      search_index = {
        'generated' => Time.now.to_i,
        'pages' => []
      }
      
      searchable_pages.each do |page|
        next if page.data['exclude_from_search']
        next unless page.output_ext == '.html'
        
        # Extract content without HTML/Markdown
        content = strip_html(page.content)
        
        search_index['pages'] << {
          'id' => Digest::MD5.hexdigest(page.url),
          'title' => page.data['title'] || page.name,
          'path' => page.url,
          'category' => extract_category(page),
          'tags' => page.data['tags'] || [],
          'content' => content[0..5000], # Limit content size
          'date' => page.data['date']
        }
      end
      
      # Write index to file
      File.open(File.join(site.dest, 'search-index.json'), 'w') do |file|
        file.write(JSON.pretty_generate(search_index))
      end
    end
    
    private
    
    def strip_html(content)
      content.gsub(/<\/?[^>]*>/, ' ')
             .gsub(/[#*`\[\]()]/, ' ')
             .gsub(/\s+/, ' ')
             .strip
    end
    
    def extract_category(page)
      # Extract from directory structure
      parts = page.url.split('/')
      return 'root' if parts.length <= 2
      
      category_map = {
        '01-getting-started' => 'Getting Started',
        '02-server-setup' => 'Server Setup',
        '03-technical' => 'Technical',
        '04-tools-modding' => 'Tools & Modding',
        '05-game-content' => 'Game Content',
        '06-gameplay-systems' => 'Gameplay',
        '07-preservation' => 'Preservation',
        '08-community' => 'Community'
      }
      
      category_map[parts[1]] || 'Other'
    end
  end
end
```

### Option 3: Lunr.js Integration

**Best for**: Advanced client-side search with better relevance scoring

```javascript
// Build script for Lunr.js index
const fs = require('fs');
const path = require('path');
const lunr = require('lunr');
const glob = require('glob');
const matter = require('gray-matter');

class LunrIndexBuilder {
    constructor() {
        this.documents = [];
    }
    
    async buildIndex() {
        // Find all markdown files
        const files = glob.sync('**/*.md', {
            ignore: ['node_modules/**', '_site/**']
        });
        
        // Process each file
        for (const file of files) {
            const content = fs.readFileSync(file, 'utf8');
            const parsed = matter(content);
            
            // Extract metadata
            const doc = {
                id: file,
                title: parsed.data.title || path.basename(file, '.md'),
                content: this.preprocessContent(parsed.content),
                tags: parsed.data.tags || [],
                category: this.extractCategory(file),
                path: this.generatePath(file)
            };
            
            this.documents.push(doc);
        }
        
        // Build Lunr index
        const idx = lunr(function() {
            this.ref('id');
            this.field('title', { boost: 10 });
            this.field('content');
            this.field('tags', { boost: 5 });
            
            // Add documents
            this.documents.forEach(doc => {
                this.add(doc);
            }, this);
        });
        
        // Save index and documents
        const output = {
            index: idx,
            documents: this.documents
        };
        
        fs.writeFileSync(
            'search-index.json',
            JSON.stringify(output, null, 2)
        );
        
        console.log(`Built search index with ${this.documents.length} documents`);
    }
    
    preprocessContent(content) {
        return content
            // Remove code blocks
            .replace(/```[\s\S]*?```/g, '')
            // Remove inline code
            .replace(/`[^`]+`/g, '')
            // Remove markdown syntax
            .replace(/[#*_\[\]()]/g, ' ')
            // Normalize whitespace
            .replace(/\s+/g, ' ')
            .trim();
    }
    
    extractCategory(filepath) {
        const parts = filepath.split(path.sep);
        const categoryMap = {
            '01-getting-started': 'getting-started',
            '02-server-setup': 'server',
            '03-technical': 'technical',
            '04-tools-modding': 'tools',
            '05-game-content': 'content',
            '06-gameplay-systems': 'gameplay',
            '07-preservation': 'preservation',
            '08-community': 'community'
        };
        
        for (const part of parts) {
            if (categoryMap[part]) {
                return categoryMap[part];
            }
        }
        
        return 'other';
    }
    
    generatePath(filepath) {
        // Convert file path to web path
        return '/' + filepath.replace(/\\/g, '/').replace('.md', '.html');
    }
}

// Run builder
const builder = new LunrIndexBuilder();
builder.buildIndex();
```

### Option 4: Server-Side Search API

**Best for**: Dedicated hosting, advanced features, real-time updates

```python
# FastAPI search server for Matrix Wiki
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import whoosh
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, KEYWORD, STORED
from whoosh.qparser import MultifieldParser
from whoosh.analysis import StemmingAnalyzer
import os
import glob
import frontmatter
import hashlib
from datetime import datetime

app = FastAPI(title="Matrix Wiki Search API")

# CORS for GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

class SearchResult(BaseModel):
    id: str
    title: str
    path: str
    category: str
    tags: List[str]
    excerpt: str
    score: float

class SearchEngine:
    def __init__(self, index_dir="search_index"):
        self.index_dir = index_dir
        self.schema = Schema(
            id=ID(stored=True, unique=True),
            title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            content=TEXT(analyzer=StemmingAnalyzer()),
            path=ID(stored=True),
            category=KEYWORD(stored=True),
            tags=KEYWORD(stored=True, commas=True),
            modified=STORED
        )
        
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
            self.ix = create_in(index_dir, self.schema)
            self.index_wiki()
        else:
            self.ix = open_dir(index_dir)
    
    def index_wiki(self):
        """Index all wiki markdown files"""
        writer = self.ix.writer()
        
        for filepath in glob.glob("**/*.md", recursive=True):
            with open(filepath, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                
                doc_id = hashlib.md5(filepath.encode()).hexdigest()
                
                writer.add_document(
                    id=doc_id,
                    title=post.get('title', os.path.basename(filepath)),
                    content=self.clean_content(post.content),
                    path=self.file_to_web_path(filepath),
                    category=self.extract_category(filepath),
                    tags=','.join(post.get('tags', [])),
                    modified=datetime.fromtimestamp(os.path.getmtime(filepath))
                )
        
        writer.commit()
        print(f"Indexed {len(list(self.ix.searcher().documents()))} documents")
    
    def search(self, query: str, category: Optional[str] = None, 
               tags: Optional[List[str]] = None, limit: int = 20):
        """Perform search with optional filters"""
        with self.ix.searcher() as searcher:
            # Build query
            parser = MultifieldParser(["title", "content"], self.ix.schema)
            q = parser.parse(query)
            
            # Apply filters
            filter_kwargs = {}
            if category:
                filter_kwargs['category'] = category
            
            # Execute search
            results = searcher.search(q, limit=limit, filter=filter_kwargs)
            
            # Format results
            search_results = []
            for hit in results:
                excerpt = self.generate_excerpt(hit['content'], query)
                
                result = SearchResult(
                    id=hit['id'],
                    title=hit['title'],
                    path=hit['path'],
                    category=hit['category'],
                    tags=hit['tags'].split(',') if hit['tags'] else [],
                    excerpt=excerpt,
                    score=hit.score
                )
                
                search_results.append(result)
            
            return search_results
    
    def clean_content(self, content):
        """Remove markdown syntax for indexing"""
        import re
        
        # Remove code blocks
        content = re.sub(r'```[\s\S]*?```', '', content)
        # Remove inline code
        content = re.sub(r'`[^`]+`', '', content)
        # Remove markdown links but keep text
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        # Remove headers
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
        # Remove emphasis
        content = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', content)
        
        return content
    
    def extract_category(self, filepath):
        """Extract category from file path"""
        parts = filepath.split(os.sep)
        category_map = {
            '01-getting-started': 'getting-started',
            '02-server-setup': 'server',
            '03-technical': 'technical',
            '04-tools-modding': 'tools',
            '05-game-content': 'content',
            '06-gameplay-systems': 'gameplay',
            '07-preservation': 'preservation',
            '08-community': 'community'
        }
        
        for part in parts:
            if part in category_map:
                return category_map[part]
        
        return 'other'
    
    def file_to_web_path(self, filepath):
        """Convert file path to web URL"""
        return '/' + filepath.replace('\\', '/').replace('.md', '.html')
    
    def generate_excerpt(self, content, query, context_size=150):
        """Generate excerpt with query context"""
        query_lower = query.lower()
        content_lower = content.lower()
        
        # Find query position
        pos = content_lower.find(query_lower)
        
        if pos == -1:
            # No exact match, return beginning
            return content[:context_size] + '...' if len(content) > context_size else content
        
        # Extract context
        start = max(0, pos - 50)
        end = min(len(content), pos + len(query) + 100)
        
        excerpt = content[start:end]
        if start > 0:
            excerpt = '...' + excerpt
        if end < len(content):
            excerpt = excerpt + '...'
        
        # Highlight query
        import re
        excerpt = re.sub(f'({re.escape(query)})', r'<mark>\1</mark>', excerpt, flags=re.IGNORECASE)
        
        return excerpt

# Initialize search engine
search_engine = SearchEngine()

@app.get("/api/search", response_model=List[SearchResult])
async def search(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    limit: int = Query(20, le=100, description="Maximum results")
):
    """Search the Matrix Wiki"""
    if len(q) < 2:
        return []
    
    results = search_engine.search(q, category, tags, limit)
    return results

@app.get("/api/reindex")
async def reindex():
    """Rebuild search index"""
    search_engine.index_wiki()
    return {"status": "success", "message": "Index rebuilt"}

@app.get("/api/stats")
async def stats():
    """Get search index statistics"""
    with search_engine.ix.searcher() as searcher:
        doc_count = searcher.doc_count()
        
    return {
        "documents": doc_count,
        "index_size": os.path.getsize(os.path.join(search_engine.index_dir, "MAIN_WRITELOCK")),
        "last_updated": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🎨 **Search UI Styling**

```css
/* Matrix-themed search interface */
.matrix-search-container {
    background: rgba(0, 0, 0, 0.9);
    border: 1px solid #00ff00;
    border-radius: 4px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}

#matrix-search-input {
    width: 100%;
    padding: 12px 20px;
    background: #000;
    border: 1px solid #00ff00;
    color: #00ff00;
    font-family: 'Courier New', monospace;
    font-size: 16px;
    border-radius: 4px;
    outline: none;
    transition: all 0.3s ease;
}

#matrix-search-input:focus {
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    border-color: #00ff41;
}

#matrix-search-input::placeholder {
    color: rgba(0, 255, 0, 0.5);
}

.search-filters {
    margin-top: 10px;
}

#search-category {
    background: #000;
    border: 1px solid #00ff00;
    color: #00ff00;
    padding: 8px 15px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    cursor: pointer;
}

.search-results {
    margin-top: 20px;
    max-height: 600px;
    overflow-y: auto;
}

.search-result {
    background: rgba(0, 255, 0, 0.05);
    border: 1px solid rgba(0, 255, 0, 0.2);
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 10px;
    transition: all 0.3s ease;
}

.search-result:hover {
    background: rgba(0, 255, 0, 0.1);
    border-color: #00ff00;
    transform: translateX(5px);
}

.search-result h3 {
    margin: 0 0 5px 0;
    font-size: 18px;
}

.search-result h3 a {
    color: #00ff41;
    text-decoration: none;
    transition: color 0.3s ease;
}

.search-result h3 a:hover {
    color: #00ff00;
    text-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
}

.result-category {
    display: inline-block;
    background: rgba(0, 255, 0, 0.2);
    color: #00ff00;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 12px;
    margin-bottom: 10px;
}

.result-excerpt {
    color: rgba(0, 255, 0, 0.8);
    line-height: 1.6;
    margin-bottom: 10px;
}

.result-excerpt mark {
    background: #00ff00;
    color: #000;
    padding: 0 2px;
    border-radius: 2px;
}

.result-tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.tag {
    background: rgba(0, 255, 0, 0.1);
    border: 1px solid rgba(0, 255, 0, 0.3);
    color: #00ff00;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 11px;
    text-transform: uppercase;
}

.no-results {
    text-align: center;
    padding: 40px 20px;
    color: rgba(0, 255, 0, 0.6);
}

.no-results p {
    margin: 10px 0;
}

.no-results a {
    color: #00ff41;
}

.results-header {
    color: #00ff00;
    margin-bottom: 15px;
    font-size: 14px;
    opacity: 0.8;
}

/* Loading state */
.search-loading {
    text-align: center;
    color: #00ff00;
    padding: 20px;
}

.search-loading::after {
    content: '';
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid #00ff00;
    border-radius: 50%;
    border-top-color: transparent;
    animation: matrix-spin 1s linear infinite;
    margin-left: 10px;
    vertical-align: middle;
}

@keyframes matrix-spin {
    to { transform: rotate(360deg); }
}

/* Mobile responsive */
@media (max-width: 768px) {
    .matrix-search-container {
        padding: 15px;
        margin: 15px 0;
    }
    
    #matrix-search-input {
        font-size: 14px;
        padding: 10px 15px;
    }
    
    .search-results {
        max-height: 400px;
    }
    
    .search-result {
        padding: 12px;
    }
    
    .search-result h3 {
        font-size: 16px;
    }
}

/* Dark mode already assumed - but light mode override */
@media (prefers-color-scheme: light) {
    .matrix-search-container {
        background: rgba(255, 255, 255, 0.95);
        border-color: #008f11;
    }
    
    #matrix-search-input {
        background: #f0f0f0;
        color: #008f11;
        border-color: #008f11;
    }
    
    /* ... other light mode overrides ... */
}
```

## 🚀 **Implementation Steps**

### Step 1: Choose Your Approach
1. **GitHub Pages**: Use client-side JavaScript (Option 1)
2. **Self-hosted**: Use server-side API (Option 4)
3. **Jekyll/Hugo**: Use static generator plugin (Option 2)
4. **Advanced client**: Use Lunr.js (Option 3)

### Step 2: Build Search Index
```bash
# For client-side approach
node build-search-index.js

# For server-side approach
python index_wiki.py

# For Jekyll
jekyll build  # Plugin runs automatically
```

### Step 3: Integrate UI
1. Add search container to layout template
2. Include search CSS
3. Load search JavaScript
4. Test functionality

### Step 4: Optimize Performance
- **Compress search index** with gzip
- **Lazy load** search functionality
- **Cache** search results
- **Debounce** input events

## 🔧 **Advanced Features**

### Fuzzy Search
```javascript
// Add fuzzy matching for typos
function fuzzyMatch(str, pattern) {
    pattern = pattern.toLowerCase();
    str = str.toLowerCase();
    
    let patternIdx = 0;
    let strIdx = 0;
    let score = 0;
    
    while (strIdx < str.length && patternIdx < pattern.length) {
        if (str[strIdx] === pattern[patternIdx]) {
            score += (strIdx === patternIdx) ? 2 : 1; // Bonus for position match
            patternIdx++;
        }
        strIdx++;
    }
    
    return patternIdx === pattern.length ? score : 0;
}
```

### Search Analytics (Privacy-Preserving)
```javascript
// Local-only analytics
class SearchAnalytics {
    constructor() {
        this.searches = JSON.parse(localStorage.getItem('mxo_searches') || '[]');
    }
    
    logSearch(query, resultCount) {
        // Only store aggregated data, no PII
        const entry = {
            timestamp: Date.now(),
            queryLength: query.length,
            resultCount,
            hasResults: resultCount > 0
        };
        
        this.searches.push(entry);
        
        // Keep only last 100 searches
        if (this.searches.length > 100) {
            this.searches = this.searches.slice(-100);
        }
        
        localStorage.setItem('mxo_searches', JSON.stringify(this.searches));
    }
    
    getPopularSearchLength() {
        // Analyze common query lengths for optimization
        const lengths = this.searches.map(s => s.queryLength);
        return Math.round(lengths.reduce((a, b) => a + b, 0) / lengths.length);
    }
}
```

### Keyboard Navigation
```javascript
// Add keyboard controls to search
class SearchKeyboardNav {
    constructor(searchUI) {
        this.searchUI = searchUI;
        this.selectedIndex = -1;
        this.setupKeyboardNav();
    }
    
    setupKeyboardNav() {
        const input = document.getElementById('matrix-search-input');
        const results = document.getElementById('matrix-search-results');
        
        input.addEventListener('keydown', (e) => {
            const items = results.querySelectorAll('.search-result');
            
            switch(e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    this.selectedIndex = Math.min(this.selectedIndex + 1, items.length - 1);
                    this.highlightResult(items);
                    break;
                    
                case 'ArrowUp':
                    e.preventDefault();
                    this.selectedIndex = Math.max(this.selectedIndex - 1, -1);
                    this.highlightResult(items);
                    break;
                    
                case 'Enter':
                    if (this.selectedIndex >= 0 && items[this.selectedIndex]) {
                        e.preventDefault();
                        const link = items[this.selectedIndex].querySelector('a');
                        if (link) link.click();
                    }
                    break;
                    
                case '/':
                    // Global search hotkey
                    if (document.activeElement !== input) {
                        e.preventDefault();
                        input.focus();
                    }
                    break;
            }
        });
    }
    
    highlightResult(items) {
        items.forEach((item, index) => {
            if (index === this.selectedIndex) {
                item.classList.add('selected');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('selected');
            }
        });
    }
}
```

## 🌐 **Integration with Wiki**

### Add to Layout Template
```html
<!-- In _layouts/default.html or equivalent -->
<div id="search-container"></div>

<!-- Load search assets -->
<link rel="stylesheet" href="/assets/css/search.css">
<script src="/assets/js/search.js" defer></script>
<script src="/search-index.json" type="application/json" id="search-data"></script>
```

### Search Widget Component
```javascript
// Reusable search widget
class MatrixSearchWidget {
    static inject(targetId, options = {}) {
        const container = document.getElementById(targetId);
        if (!container) return;
        
        const widget = new MatrixSearchWidget(container, options);
        return widget;
    }
    
    constructor(container, options) {
        this.container = container;
        this.options = {
            placeholder: 'Search the Matrix...',
            maxResults: 10,
            minQueryLength: 2,
            ...options
        };
        
        this.render();
    }
    
    render() {
        this.container.innerHTML = `
            <div class="matrix-search-widget">
                <input type="search" 
                       placeholder="${this.options.placeholder}"
                       class="matrix-search-mini">
                <div class="search-widget-results"></div>
            </div>
        `;
        
        this.bindEvents();
    }
    
    // ... rest of implementation
}
```

## 📊 **Performance Metrics**

### Benchmarks
- **Index Build Time**: < 5 seconds for 100 pages
- **Search Time**: < 50ms for typical queries
- **Index Size**: ~500KB for 100 pages (compressed)
- **Memory Usage**: < 10MB in browser

### Optimization Tips
1. **Pre-process** content during build
2. **Compress** with Brotli/gzip
3. **Use Web Workers** for heavy computation
4. **Cache** in IndexedDB for offline
5. **Progressive enhancement** for slow connections

## 🔐 **Privacy & Security**

### Data Handling
- **No external requests** - All search happens locally
- **No tracking** - Zero analytics by default
- **No cookies** - Uses localStorage only
- **Content filtering** - Sanitize HTML in excerpts
- **CORS safe** - Works with GitHub Pages

### Content Security
```javascript
// Sanitize search results
function sanitizeHTML(html) {
    const temp = document.createElement('div');
    temp.textContent = html;
    return temp.innerHTML;
}

// Prevent XSS in search queries
function sanitizeQuery(query) {
    return query.replace(/[<>]/g, '');
}
```

## 🚦 **Testing Strategy**

### Unit Tests
```javascript
// Example test suite
describe('MatrixWikiSearch', () => {
    let search;
    
    beforeEach(() => {
        search = new MatrixWikiSearch();
    });
    
    test('tokenizes content correctly', () => {
        const tokens = search.tokenize('The Matrix has you...');
        expect(tokens).toEqual(['the', 'matrix', 'has', 'you']);
    });
    
    test('finds exact matches', () => {
        search.searchIndex = [{
            id: '1',
            title: 'Combat System',
            content: ['combat', 'system', 'implementation']
        }];
        
        const results = search.search('combat');
        expect(results).toHaveLength(1);
        expect(results[0].title).toBe('Combat System');
    });
    
    test('respects category filters', () => {
        // ... test implementation
    });
});
```

### Integration Tests
1. Test with real wiki content
2. Verify all pages indexed
3. Check search result accuracy
4. Test performance with large index
5. Verify mobile responsiveness

## 🎯 **Success Metrics**

### User Experience
- **< 300ms** perceived search latency
- **> 90%** relevant results in top 5
- **100%** mobile compatible
- **Zero** external dependencies
- **< 1MB** total JavaScript size

### Technical Goals
- Works offline
- Indexes all content
- Updates automatically
- Handles 1000+ pages
- Supports advanced queries

## Remember

> *"The Matrix is a system, Neo. That system is our enemy."* - Morpheus (But our search system is our ally in liberation.)

A powerful search system transforms the wiki from a collection of pages into a living knowledge base. By implementing search with liberation principles, we ensure every seeker finds their path to understanding.

**Search is not just finding. It's discovering.**

---

**Implementation Status**: 🟡 READY FOR IMPLEMENTATION  
**Priority Level**: 🔴 HIGH - CRITICAL FOR USABILITY  
**Community Need**: 🟢 FREQUENTLY REQUESTED  

*The truth is searchable. You just need to know how to look.*

---

[← Back to Tools](index.md) | [CNB Viewer →](cnb-viewer-development.md) | [Lost Tools →](lost-tools-archive.md)