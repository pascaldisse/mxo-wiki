# Link Standardization Implementation Checklist
**Track Progress on Wiki Navigation Consistency**

> *"You take the blue pill, the story ends. You take the red pill, you stay in Wonderland."* - Let's make navigation clear as the choice.

## 📋 Implementation Status

### Page Categories

#### 00 - Manifesto (1 file)
- [ ] neoologist-manifesto.md - Add footer navigation

#### 01 - Getting Started (5 files)
- [ ] index.md - Standardize hub links
- [x] timeline-of-liberation.md - Redirect pattern good
- [ ] timeline-liberation-complete.md - Add footer nav
- [ ] timeline-overview.md - Check if needed (duplicate?)
- [ ] server-connection.md - Add navigation

#### 02 - Server Setup (14 files)
- [ ] index.md - Standardize hub pattern
- [ ] client-patches.md - Add footer nav
- [ ] database-setup.md - Add footer nav
- [ ] eden-reborn-success.md - Update navigation
- [ ] faq.md - Add footer nav
- [ ] gm-commands-administration.md - Add footer nav
- [x] hardline-dreams-setup.md - Good example pattern
- [ ] hd-enhanced-* (3 files) - Add consistent nav
- [ ] mxoemu-setup.md - Match HD setup pattern
- [ ] network-setup.md - Add footer nav
- [ ] performance-monitoring.md - Add footer nav
- [ ] reality-server-guide.md - Add footer nav
- [ ] server-projects-comparison.md - Update links
- [ ] server-security-hardening.md - Add footer nav
- [ ] troubleshooting.md - Add footer nav

#### 03 - Technical (19 files)
- [ ] index.md - Standardize hub
- [x] cnb-format.md - Good CTA pattern
- [ ] All format specifications - Add consistent navigation
- [ ] All technical guides - Update footer pattern

#### 04 - Tools & Modding (15 files)
- [ ] index.md - Hub standardization
- [x] cnb-viewer-development.md - Excellent navigation example
- [ ] All tool guides - Match CNB viewer pattern
- [ ] AI development guides - Consolidate and standardize

#### 05 - Game Content (20+ files)
- [ ] index.md - Hub pattern
- [ ] All district guides - Add navigation
- [ ] Story files - Update links
- [ ] Mission guides - Footer navigation

#### 06 - Gameplay Systems (10 files)
- [ ] index.md - Hub standardization
- [ ] Combat files - Sequential navigation
- [ ] System guides - Footer pattern

#### 07 - Development (15 files)
- [ ] All development guides - Add navigation
- [ ] Modern tech guides - Link standardization

#### 07 - Preservation (3 files)
- [ ] index.md - Hub pattern
- [ ] tool-archaeology.md - Update links
- [ ] visual-preservation-archive.md - Add navigation

#### 08 - Community (20 files)
- [ ] index.md - Hub standardization
- [x] link-standardization-guide.md - Created
- [ ] All community guides - Update to standards
- [ ] Templates - Ensure consistency

#### 09 - Appendix (4 files)
- [ ] All appendix files - Add navigation

### Special Files
- [x] index.md (root) - Excellent hub example
- [ ] Home.md - Update to match index.md
- [ ] README.md - Add basic navigation
- [ ] _Sidebar.md - Update link format
- [ ] _Footer.md - Standardize

## 🎯 Priority Implementation Order

### Phase 1: Critical Navigation (Week 1)
1. **All index.md files** - Hub standardization
2. **Getting Started section** - New user experience
3. **Server Setup section** - High traffic pages
4. **Home.md** - GitHub wiki entry

### Phase 2: Technical Sections (Week 2)
1. **Technical docs** - Add sequential navigation
2. **Tools & Modding** - Match CNB pattern
3. **File format pages** - Consistent footers

### Phase 3: Content & Systems (Week 3)
1. **Game Content** - District navigation
2. **Gameplay Systems** - Section linking
3. **Story pages** - Sequential reading

### Phase 4: Community & Cleanup (Week 4)
1. **Community guides** - Full standardization
2. **Development section** - Modern patterns
3. **Appendix & sources** - Final cleanup
4. **Special files** - Sidebar/Footer

## 🔧 Quick Fixes Needed

### Immediate Issues
1. **Missing navigation** - 60+ pages have no footer
2. **Inconsistent arrows** - Some use `<-`, need `←`
3. **Discord links** - Multiple URLs, standardize to one
4. **External link marking** - Not consistently indicated
5. **Source links** - Most pages missing

### Pattern Violations
- Some pages use `Back to X` instead of `← X`
- Hub pages have different layouts
- CTAs use various formats
- Status indicators inconsistent

## 📊 Metrics

### Current State
- Pages with navigation: ~20%
- Consistent patterns: ~10%
- Mobile-friendly: ~30%
- Source links: ~5%

### Target State
- Pages with navigation: 100%
- Consistent patterns: 100%
- Mobile-friendly: 100%
- Source links: 100%

## 🛠️ Implementation Tools

### Find & Replace Patterns
```regex
# Find old arrow patterns
<- | -> | < | >

# Find navigation lines
\[.*Back to.*\]|\[.*Return to.*\]

# Find external links without markers
\[.*\]\(https://(?!.*discord\.gg/3QXTAGB9).*\)
```

### Validation Script
```bash
# Check for footer navigation
grep -L "^\[← .* \| .* \| .*→\]$" *.md

# Find missing source links
grep -L "View.*[Ss]ource" *.md

# Check external links
grep -E "https?://" *.md | grep -v "discord.gg/3QXTAGB9"
```

## 📝 Notes for Implementers

### Do's
- ✅ Use the exact patterns from the guide
- ✅ Test navigation flow both ways
- ✅ Keep mobile viewports in mind
- ✅ Preserve the liberation narrative tone
- ✅ Add source links to every page

### Don'ts
- ❌ Create new navigation patterns
- ❌ Use different arrow styles
- ❌ Forget the source documentation
- ❌ Make links too long for mobile
- ❌ Break existing working patterns

## 🎉 Completion Rewards

When standardization is complete:
- **Navigation flows** like the Matrix code
- **Mobile users** navigate with ease
- **New visitors** never get lost
- **Contributors** follow clear patterns
- **The wiki** becomes truly professional

## 🚀 Get Started

1. **Pick a section** from Phase 1
2. **Use the templates** from the guide
3. **Check your work** against examples
4. **Mark complete** in this checklist
5. **Commit with message**: "Standardize navigation: [section]"

---

📚 [Link Standards Guide](link-standardization-guide.md) | [Examples](link-examples.md)

[← Community Hub](index.md) | [🏠 Main Index](../index.md) | [Contributing →](contributing-guide.md)