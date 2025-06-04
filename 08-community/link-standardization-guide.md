# Wiki Link Standardization Guide
**Consistent Navigation for the Liberation**

> *"The Matrix is a system. That system has rules."* - Our wiki needs consistent patterns too.

## 🔍 Current Link Patterns Analysis

After analyzing the wiki, we've identified several link patterns in use. This guide establishes standards for each type to ensure consistency and mobile-friendly navigation.

## 📐 Link Pattern Standards

### 1. Navigation Links (Page Footer)

**Standard Pattern:**
```markdown
---

[← Previous Page](previous.md) | [🏠 Home](../index.md) | [Next Page →](next.md)
```

**Guidelines:**
- Use arrows with spaces: `← ` and ` →`
- Center separator: ` | ` (space-pipe-space)
- Home link includes house emoji: `🏠 Home`
- Keep on single line
- Place after horizontal rule `---`

**Mobile-Friendly Variant (for long titles):**
```markdown
---

[← Back](previous.md) | [🏠](../index.md) | [Next →](next.md)
```

### 2. Section Navigation (Within Categories)

**Standard Pattern:**
```markdown
## 🧭 Navigation

**In This Section:**
- 📋 [Current Page] - You are here
- [Previous Topic](previous.md) - Brief description
- [Next Topic](next.md) - Brief description

**Other Sections:**
- [🏠 Main Hub](../index.md)
- [📚 Related Section](../other-section/index.md)
```

### 3. External Links

**GitHub/Code Repositories:**
```markdown
**Repository**: [Project Name](https://github.com/user/repo)
**Source**: [HD GitHub](https://github.com/hdneo/mxo-hd)
```

**Discord Links:**
```markdown
**🔗 [Join us on Discord](https://discord.gg/3QXTAGB9)**
[Discord Community](https://discord.gg/3QXTAGB9) - Live discussions
```

**Other External:**
```markdown
[Tool Download](https://example.com) (External)
[Reference Doc](https://site.com) → External site
```

### 4. Cross-Reference Links

**In-Text References:**
```markdown
See [CNB Format](../03-technical/cnb-format.md) for technical details.
As documented in the [Timeline](../01-getting-started/timeline.md), this occurred in 2025.
For setup instructions, check the [Server Guide](../02-server-setup/index.md).
```

**Reference Lists:**
```markdown
### Related Topics
- **[File Formats](../03-technical/file-formats.md)** - Complete specifications
- **[Tool Development](../04-tools-modding/index.md)** - Build new tools
- **[Combat System](../06-gameplay-systems/combat/index.md)** - Implementation details
```

### 5. Source Documentation Links

**Standard Pattern:**
```markdown
## 📚 Sources & Evidence

📖 **[View Source Documentation](../sources/current-page-sources.md)**

This page is based on:
- Discord messages (2016-2025)
- Forum posts from mxoemu.info
- Community knowledge
- [Full source details →](../sources/current-page-sources.md)
```

### 6. Hub/Index Pages

**Category Links:**
```markdown
### 02 - Server Setup & Configuration
5. **[Server Setup Hub](02-server-setup/index.md)**
   - *Complete guide to running MXO servers*
   - Choose your server type
   - Step-by-step configuration
```

**Quick Navigation:**
```markdown
## 🎯 Quick Links
- **[Getting Started](01-getting-started/index.md)** → New? Start here
- **[Server Setup](02-server-setup/index.md)** → Run your server
- **[Technical Docs](03-technical/index.md)** → Deep dives
- **[Community](08-community/index.md)** → Get involved
```

### 7. Call-to-Action Links

**Standard CTAs:**
```markdown
## 🚀 Get Started
**[→ Begin Your Journey](../01-getting-started/index.md)**

## 💪 Take Action
**[Join the CNB Liberation Effort →](cnb-development.md)**

## 🤝 Connect
**[Find Your Crew on Discord →](https://discord.gg/3QXTAGB9)**
```

### 8. Status/Priority Indicators

**With Links:**
```markdown
**Status**: 🔴 [CRITICAL - Help Needed](../08-community/help-wanted.md)
**Priority**: ⚡ [Maximum Priority](priority-matrix.md)
**Progress**: 🟡 [In Development](development-status.md)
```

## 🎨 Emoji Usage Standards

### Navigation Emojis
- 🏠 Home/Main page
- 📚 Documentation/Sources
- 🧭 Navigation/Contents
- 🎯 Goals/Targets
- 🚀 Getting started/Action
- 💪 Call to action
- 🤝 Community/Collaboration
- 🔗 External links
- 📖 View more/Read
- ← → Directional navigation

### Status Emojis
- 🔴 Critical/Urgent
- 🟡 In Progress
- 🟢 Complete/Ready
- ⚡ High Priority
- 🚧 Under Construction
- ✅ Verified/Complete
- ❌ Not working/Missing
- ❓ Unknown/Needs research

## 📱 Mobile-Friendly Guidelines

1. **Keep link text short** on navigation bars
2. **Use line breaks** for long link lists
3. **Emoji + text** for visual recognition
4. **Touch-friendly spacing** between links
5. **Avoid long URLs** in text

## 🔄 Implementation Plan

### Phase 1: Navigation Links (High Priority)
1. Update all page footers to standard pattern
2. Add navigation to pages missing it
3. Ensure mobile-friendly variants where needed

### Phase 2: Hub Pages
1. Standardize all index.md files
2. Update quick link sections
3. Add emoji indicators

### Phase 3: Cross-References
1. Review in-text links
2. Standardize related topics sections
3. Add source documentation links

### Phase 4: External Links
1. Mark all external links clearly
2. Update Discord links to single URL
3. Add repository indicators

## 🛠️ Tools & Templates

### Page Footer Template
```markdown
---

📚 [View Sources](../sources/PAGENAME-sources.md)

[← Previous Topic](previous.md) | [🏠 Home](../index.md) | [Next Topic →](next.md)
```

### Quick Reference
```markdown
| Pattern | Usage | Example |
|---------|-------|---------|
| `[← Back]` | Previous page | `[← Server Setup](setup.md)` |
| `[→ Next]` | Next page | `[Client Config →](client.md)` |
| `[🏠 Home]` | Main index | `[🏠 Home](../index.md)` |
| `**[Link]**` | Emphasis | `**[Critical Doc](doc.md)**` |
| `[Link] →` | External | `[GitHub] → (url)` |
```

## 🌟 The Link Liberation Philosophy

Links are the neural pathways of our wiki. They should:
- **Guide** without confusion
- **Connect** related knowledge
- **Work** on all devices
- **Feel** consistent everywhere
- **Support** the liberation narrative

## 📝 Maintenance Notes

When adding new pages:
1. Use the templates above
2. Check link patterns match standards
3. Test on mobile viewport
4. Ensure bidirectional navigation
5. Update related page links

---

📚 [View Implementation Examples](link-examples.md)

[← Documentation Standards](documentation-standards.md) | [🏠 Community Hub](index.md) | [Contributing Guide →](contributing-guide.md)