# Link Pattern Examples
**Real Examples from the Wiki**

> *"Do not try and bend the spoon. That's impossible. Instead, only try to realize the truth."* - Consistent patterns ARE possible.

## ✅ Good Examples to Follow

### 1. Perfect Footer Navigation
From `cnb-viewer-development.md`:
```markdown
---

[← Back to Tools](index.md) | [CNB Format Details →](../03-technical/cnb-format.md) | [Join Development →](../08-community/join-the-resistance.md)
```
**Why it's good:**
- Clear directional flow
- Descriptive link text
- Related topics linked
- Mobile-friendly length

### 2. Excellent Hub Pattern
From root `index.md`:
```markdown
### 02 - Server Setup & Configuration
5. **[Server Setup Hub](02-server-setup/index.md)**
   - *Complete guide to running MXO servers*
   - Choose your server type
   - Step-by-step configuration
```
**Why it's good:**
- Bold title link
- Italicized description
- Bullet points for features
- Clear hierarchy

### 3. Great External Link
From `hardline-dreams-setup.md`:
```markdown
**Repository**: https://github.com/hdneo/mxo-hd
```
**Why it's good:**
- Label explains link type
- Full URL visible
- Clean formatting

### 4. Perfect CTA Section
From `cnb-format.md`:
```markdown
### 🚨 URGENT: We Need You

#### For Reverse Engineers
- This is the holy grail
- Glory awaits the decoder
- Full community support
- Document EVERYTHING
```
**Why it's good:**
- Emoji draws attention
- Clear audience targeting
- Action-oriented language
- Specific next steps

### 5. Ideal Quick Links
From root `index.md`:
```markdown
### 🧭 Essential Navigation
- **[Home](Home.md)** - Main landing page
- **[Getting Started](01-getting-started/index.md)** - New user guide
- **[Server Setup](02-server-setup/index.md)** - Run your own server
- **[Community](08-community/index.md)** - Get involved
```
**Why it's good:**
- Emoji section marker
- Consistent format
- Brief descriptions
- Logical grouping

## ❌ Patterns to Avoid

### 1. Inconsistent Navigation
```markdown
[< Back to Server Setup](index.md) | [Home](/Home.md) | [Next: Client Config >](client.md)
```
**Problems:**
- Wrong arrow style `<` instead of `←`
- Inconsistent labels ("Back to" vs just "Next:")
- Absolute path `/Home.md`

### 2. Poor Hub Links
```markdown
- Server Setup - see 02-server-setup/index.md
- technical documentation is in /03-technical/
- Tools: 04-tools-modding/index.md (incomplete)
```
**Problems:**
- Not actual links
- Inconsistent capitalization
- Mixed path styles
- Editorial comments in links

### 3. Unclear External Links
```markdown
Download the tool [here](https://example.com/download)
Check [this link](https://github.com/user/repo) for more info
```
**Problems:**
- Vague link text ("here", "this link")
- No indication it's external
- No context about destination

### 4. Overwhelming Navigation
```markdown
[← Previous: Advanced Server Configuration for MXOEmu Reality 2.0](very-long-previous-page-name.md) | [🏠 Home Page of the Matrix Online Eden Reborn Wiki](../index.md) | [Next: Complete Client Patching Guide for All Versions →](another-very-long-page-name.md)
```
**Problems:**
- Too long for mobile
- Unnecessary words
- Breaks on small screens

### 5. Missing Context
```markdown
See [here](../03-technical/cnb-format.md).
Check out [the guide](guide.md).
[Link](page.md)
```
**Problems:**
- No descriptive text
- Reader must click to understand
- Poor accessibility

## 🔄 Before & After

### Navigation Footer
**Before:**
```markdown
[Go back](previous.md) / [Index](index.md) / [Continue](next.md)
```

**After:**
```markdown
---

[← Setup Overview](previous.md) | [🏠 Server Hub](index.md) | [Database Config →](next.md)
```

### External Link
**Before:**
```markdown
GitHub: https://github.com/hdneo/mxo-hd
```

**After:**
```markdown
**Repository**: [Hardline Dreams (mxo-hd)](https://github.com/hdneo/mxo-hd)
```

### Hub Entry
**Before:**
```markdown
Technical Documentation - technical stuff about MXO
```

**After:**
```markdown
### 03 - Technical Documentation
10. **[Technical Deep Dives](03-technical/index.md)**
    - *Advanced technical analysis*
    - Server architecture documentation
    - Implementation guides
```

### Call to Action
**Before:**
```markdown
If you want to help, join us.
```

**After:**
```markdown
## 🚀 Join the Liberation

**[→ Start Contributing Today](../08-community/contributing-guide.md)**

Your skills are needed:
- Developers: Build the tools
- Writers: Document the journey
- Testers: Validate the work
- Dreamers: Imagine the future
```

## 📏 Quick Reference Rules

### Always
- ✅ Use `←` and `→` for arrows
- ✅ Include `🏠` for home links
- ✅ Bold important links with `**[text]**`
- ✅ Add descriptions after hub links
- ✅ Mark external links clearly

### Never
- ❌ Use `<` or `>` for arrows
- ❌ Create links longer than ~40 chars
- ❌ Use vague text like "here" or "this"
- ❌ Mix relative and absolute paths
- ❌ Forget mobile users

## 🎯 The Perfect Page Footer

```markdown
---

📚 [View Sources](../sources/current-page-sources.md)

[← Previous Topic](previous.md) | [🏠 Home](../index.md) | [Next Topic →](next.md)
```

This is the gold standard. Use it everywhere.

---

📚 [Standardization Guide](link-standardization-guide.md) | [Implementation Checklist](link-standardization-checklist.md)

[← Link Standards](link-standardization-guide.md) | [🏠 Community](index.md) | [Start Implementing →](link-standardization-checklist.md)