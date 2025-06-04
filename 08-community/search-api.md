# 🔍 Wiki Search API
**Advanced Content Discovery System**

> *"There is no spoon... but there is a search function."*

Technical documentation for the Eden Reborn wiki search and content discovery system. Enable advanced navigation and automated content analysis.

## 🎯 Search System Overview

### Current Implementation
- **GitHub Search** - Built-in repository search
- **File-Based Search** - Direct markdown content access
- **Manual Navigation** - Guided discovery paths
- **Link Validation** - Automated health checking

### Planned Enhancements
- **Full-Text Search** - Content-aware discovery
- **Topic Indexing** - Semantic content organization
- **API Endpoints** - Programmatic content access
- **Search Analytics** - Usage pattern tracking

## 🔧 Current Search Methods

### GitHub Native Search
**Built-in repository search functionality**

#### Basic Usage
```
Search Query Examples:
- "CNB viewer" - Find CNB-related content
- "server setup" - Locate installation guides
- "file:*.md pahefu" - Find mentions of pahefu
- "path:04-tools-modding" - Search within tools section
```

#### Advanced GitHub Search
```
Advanced Queries:
- org:codejunky language:markdown "combat system"
- repo:codejunky/mxo-wiki extension:md "database"
- path:sources/ "discord" NOT "forum"
- created:2024-12-01..2024-12-31 "tool development"
```

### File System Search
**Direct content access for development**

#### Command Line Tools
```bash
# Find files containing specific terms
grep -r "CNB viewer" wiki/ --include="*.md"

# Search for function names or technical terms
rg "PKB archives" wiki/ -t markdown

# Find broken links
grep -r "\.md)" wiki/ | grep -v "http"
```

#### Automated Validation
```bash
# Link validation script
find wiki/ -name "*.md" -exec grep -l "\[.*\](.*)" {} \;

# Content statistics
wc -w wiki/**/*.md | sort -n

# File organization analysis
find wiki/ -name "index.md" | wc -l
```

## 📡 API Design Specifications

### Planned API Endpoints

#### Content Search
```http
GET /api/v1/search
Parameters:
  - query: string (search terms)
  - section: string (limit to section)
  - type: string (content type filter)
  - limit: integer (result count)

Response:
{
  "results": [
    {
      "title": "CNB Viewer Development",
      "path": "04-tools-modding/cnb-viewer-development.md",
      "section": "Tools & Modding",
      "relevance": 0.95,
      "excerpt": "CNB files contain real-time 3D cutscenes...",
      "last_modified": "2024-12-01T10:00:00Z"
    }
  ],
  "total": 42,
  "query_time": 0.15
}
```

#### Content Statistics
```http
GET /api/v1/stats
Response:
{
  "pages": {
    "total": 85,
    "by_section": {
      "02-server-setup": 8,
      "04-tools-modding": 5,
      "03-technical-docs": 12
    }
  },
  "content": {
    "total_words": 45000,
    "average_page_length": 529,
    "longest_page": "combat-implementation-guide.md"
  },
  "links": {
    "total": 525,
    "internal": 476,
    "external": 49,
    "broken": 91
  }
}
```

#### Section Overview
```http
GET /api/v1/sections/{section_name}
Response:
{
  "name": "04-tools-modding",
  "title": "Tools & Modding",
  "description": "Tool development and modding resources",
  "pages": 5,
  "priority_items": [
    "CNB Viewer Development",
    "Lost Tools Archive"
  ],
  "status": "active_development",
  "last_updated": "2024-12-01T10:00:00Z"
}
```

### Search Index Structure

#### Document Schema
```json
{
  "id": "04-tools-modding/cnb-viewer-development",
  "title": "CNB Viewer Development",
  "section": "04-tools-modding",
  "content": "Full markdown content...",
  "headers": [
    "Development Roadmap",
    "Technical Requirements",
    "Getting Started"
  ],
  "tags": ["cnb", "viewer", "priority", "development"],
  "priority": "critical",
  "status": "in_progress",
  "contributors": ["community"],
  "word_count": 1250,
  "last_modified": "2024-12-01T10:00:00Z",
  "source_count": 5,
  "external_links": 3,
  "internal_links": 12
}
```

#### Search Weighting
```json
{
  "title": 3.0,
  "headers": 2.0,
  "priority_content": 1.5,
  "body_text": 1.0,
  "tags": 2.5,
  "filename": 1.8,
  "path": 1.2
}
```

## 🔍 Advanced Search Features

### Semantic Search
**Content-aware discovery beyond keyword matching**

#### Implementation Approach
- **Topic Modeling** - Identify content themes
- **Similarity Scoring** - Related content discovery
- **Concept Mapping** - Technical term relationships
- **Context Awareness** - Section-specific relevance

#### Search Categories
```
Technical Searches:
- "How to implement combat system" → Combat guides + Technical docs
- "PKB file extraction" → Tools + File format docs
- "Database setup issues" → Server setup + Troubleshooting

Community Searches:
- "How to contribute" → Community guides + Development workflow
- "Contact developers" → Contact info + Community channels
- "Project status" → Progress tracking + Task lists

Content Searches:
- "Matrix Online story" → Game content + Narrative preservation
- "Character information" → Story docs + Gameplay systems
- "Historical events" → Timeline + Community archives
```

### Faceted Search
**Multi-dimensional content filtering**

#### Available Facets
```json
{
  "section": [
    "manifesto", "getting-started", "server-setup",
    "technical-docs", "tools-modding", "game-content",
    "gameplay-systems", "preservation", "community"
  ],
  "priority": ["critical", "high", "medium", "low"],
  "status": ["complete", "in_progress", "planned"],
  "content_type": ["guide", "reference", "overview", "technical"],
  "difficulty": ["beginner", "intermediate", "advanced"],
  "last_updated": ["week", "month", "quarter", "year"]
}
```

#### Faceted Query Examples
```http
GET /api/v1/search?query=server&section=server-setup&priority=critical&status=complete
GET /api/v1/search?query=development&content_type=guide&difficulty=beginner
GET /api/v1/search?section=tools-modding&priority=critical&last_updated=week
```

## 📊 Search Analytics

### Usage Tracking
**Understanding how content is discovered**

#### Metrics Collected
- **Query Frequency** - Most searched terms
- **Result Relevance** - Click-through rates
- **Path Analysis** - How users navigate results
- **Content Gaps** - Searches with poor results

#### Popular Searches
```json
{
  "top_queries": [
    {"query": "CNB viewer", "count": 156, "satisfaction": 0.73},
    {"query": "server setup", "count": 142, "satisfaction": 0.89},
    {"query": "combat system", "count": 98, "satisfaction": 0.61},
    {"query": "tool development", "count": 87, "satisfaction": 0.75}
  ],
  "trending": [
    {"query": "eden reborn", "growth": 1.34},
    {"query": "database setup", "growth": 1.12}
  ]
}
```

### Content Discovery Patterns
```json
{
  "entry_points": {
    "search": 0.35,
    "direct_link": 0.28,
    "navigation": 0.22,
    "external_referral": 0.15
  },
  "user_journeys": [
    ["search", "04-tools-modding", "cnb-viewer-development"],
    ["index", "02-server-setup", "mxoemu-setup"],
    ["community", "contribute", "contact"]
  ]
}
```

## 🛠️ Implementation Roadmap

### Phase 1: Enhanced GitHub Search
**Immediate improvements using existing tools**

#### Features
- **Custom Search Operators** - Simplified query syntax
- **Search Result Templates** - Consistent result presentation
- **Quick Filters** - One-click section filtering
- **Search Shortcuts** - Bookmarkable search URLs

#### Timeline
- **Week 1**: Search operator documentation
- **Week 2**: Result template implementation
- **Week 3**: Filter interface development
- **Week 4**: Testing and refinement

### Phase 2: Index-Based Search
**Structured content indexing for better results**

#### Features
- **Content Indexing** - Full-text search database
- **Relevance Scoring** - Weighted result ranking
- **Auto-Suggestions** - Query completion and correction
- **Advanced Filtering** - Multi-dimensional facets

#### Timeline
- **Month 1**: Index structure design
- **Month 2**: Content processing pipeline
- **Month 3**: Search interface development
- **Month 4**: Integration and testing

### Phase 3: Intelligent Search
**AI-powered content discovery and recommendations**

#### Features
- **Semantic Understanding** - Intent-based search
- **Content Recommendations** - Related material suggestions
- **Personalization** - User-specific result ranking
- **Natural Language Queries** - Conversational search interface

#### Timeline
- **Quarter 1**: AI model training
- **Quarter 2**: Integration development
- **Quarter 3**: User testing and refinement
- **Quarter 4**: Production deployment

## 🔗 Integration Points

### Wiki Integration
**Search functionality embedded in wiki experience**

#### Search Interface Locations
- **Header Search Bar** - Global wiki search
- **Section Search** - Scoped to current section
- **Page Search** - Within-page content finding
- **Footer Search** - Alternative access point

#### Search Result Integration
- **Inline Results** - Search without leaving current page
- **Dedicated Search Pages** - Full search experience
- **Contextual Suggestions** - Related content recommendations
- **Search History** - Recent queries and results

### External Integration
**Search API for external tools and services**

#### Developer Access
- **REST API** - Standard HTTP interface
- **GraphQL** - Flexible query language
- **Webhooks** - Real-time content updates
- **SDK Libraries** - Language-specific implementations

#### Community Tools
- **Discord Bot** - Search wiki from Discord
- **Browser Extensions** - Enhanced navigation
- **Mobile Apps** - Native search interface
- **Developer Tools** - IDE integrations

## 📈 Success Metrics

### User Experience Metrics
- **Search Success Rate** - Percentage of successful searches
- **Average Query Time** - Speed of result delivery
- **Result Relevance** - User satisfaction with results
- **Navigation Efficiency** - Clicks to target content

### Content Discovery Metrics
- **Content Utilization** - Which pages are found via search
- **Dead Content Identification** - Pages never discovered
- **Popular Pathways** - Common search-to-content flows
- **Gap Analysis** - Searches with no good results

### Technical Performance
- **Search Latency** - Response time requirements
- **Index Freshness** - Content update lag time
- **System Reliability** - Search availability metrics
- **Scalability Measures** - Performance under load

---

## 🌟 Search Vision

The Eden Reborn wiki search system will be more than just finding content—it will be a gateway to knowledge discovery, community connection, and project contribution.

**Every search is a journey. Every result is a door to liberation.**

---

[← Back to Search Implementation](search-implementation.md) | [Navigation Guide →](navigation-guide.md) | [Community Hub →](index.md)

📚 [View Sources](../sources/08-community/search-api-sources.md)