# Broken Links Analysis - Matrix Online Wiki

## Summary Statistics
- **Total links checked**: 1,038
- **Broken links**: 220 (21.2%)
- **Files scanned**: 150

## Categorized Breakdown of Broken Links

### 1. Source Documentation Links (25 links)
These are "View Sources" or "Sources →" links pointing to non-existent files in the `/sources/` directory.

**Count**: 25 broken links
- Pattern: `../sources/[section]/[filename]-sources.md`
- Examples:
  - `../sources/01-getting-started/character-creation-sources.md`
  - `../sources/02-server-setup/advanced-admin-sources.md`
  - `../sources/03-technical/file-formats-sources.md`
  - `../sources/04-tools-modding/automation-scripts-sources.md`

**Fix Strategy**: Either:
- Create the missing source documentation files, OR
- Remove these "View Sources" links entirely (recommended if sources aren't available)

### 2. Cross-Reference Links (Missing Pages) (75 links)
Links to pages that should exist based on the content structure but don't.

**Count**: 75 broken links
- Character/story content: `character-profiles.md`, `mission-archive.md`, `characters.md`
- Game mechanics: `hidden-areas-guide.md`, `districts-map.md`, `faction-territories.md`
- Tools/development: `moa-tools.md`, `prop-tools.md`, `advanced-extraction-tools.md`
- Community: `contribute.md`, `contact.md`, `submit-story.md`
- Navigation: `navigation-tools.md`, `hardline-guide.md`, `awakening-paths.md`

**Fix Strategy**: 
- Create stub pages for critical missing content
- Redirect to existing similar content where applicable
- Remove links to planned but unimplemented features

### 3. Navigation Structure Issues (Wrong Paths) (45 links)
Links with incorrect relative paths, often missing `.md` extensions or wrong directory traversal.

**Count**: 45 broken links
- Sidebar/Footer navigation (missing `.md`):
  - `Home` → should be `Home.md`
  - `00-manifesto/neoologist-manifesto` → `00-manifesto/neoologist-manifesto.md`
  - `01-getting-started/index` → `01-getting-started/index.md`
- Wrong directory structure:
  - `../03-technical/file-formats/index.md` (directory doesn't exist)
  - `../07-story-lore/complete-storyline-documentation.md` (wrong path)
  - `../06-gameplay-systems/packet-analysis-guide.md` (file not there)

**Fix Strategy**:
- Add `.md` extensions to all wiki navigation links
- Fix directory paths to match actual structure
- Update relative paths to use correct traversal (`../` vs `../../`)

### 4. Code-Related False Positives (Lambda/Function Links) (25 links)
These are C++ lambda expressions or function parameters mistakenly parsed as Markdown links.

**Count**: 25 broken links
- Pattern: `[](parameter)` or `[text](parameter)`
- Examples:
  - `[](const auto& a, const auto& b)`
  - `[](Player& player)`
  - `[](ImGuiInputTextCallbackData* data)`
  - `[condition_name](context, **parameters)`
  - `[opcode](payload)`

**Fix Strategy**:
- Escape these in code blocks with proper markdown formatting
- Use backticks or code fences to prevent parsing as links
- Review all technical documentation for similar issues

### 5. Wiki Navigation Links (Sidebar/Footer) (50 links)
Links from `_Sidebar.md` and `_Footer.md` that don't match actual file structure.

**Count**: 50 broken links
- Missing top-level pages:
  - `Home`, `README`, `WIKI_PROGRESS`, `CLAUDE`
  - `sources/index`, `sources/README`
- Incorrect paths in navigation:
  - All sidebar links missing `.md` extension
  - Some using wrong directory names
- Template variables:
  - `{{ page.title }}`, `{{ page.url }}` (Jekyll/Liquid syntax)
  - `#{{ related_tag.name }}` (tag system not implemented)

**Fix Strategy**:
- Update `_Sidebar.md` and `_Footer.md` to use correct paths with `.md`
- Remove or implement template-based navigation
- Ensure all navigation targets exist

## Priority Recommendations

### Critical Fixes (High Priority)
1. **Fix all Sidebar/Footer navigation** (50 links) - These affect site-wide navigation
2. **Update path structures** (45 links) - Fix relative paths and add `.md` extensions
3. **Create essential missing pages** or remove links:
   - `character-creation.md` and `interface-guide.md` (getting started)
   - Core index pages for each section

### Medium Priority
1. **Handle code false positives** (25 links) - Wrap code properly in markdown
2. **Create stub pages** for important cross-references (districts, factions, tools)

### Low Priority  
1. **Remove source documentation links** (25 links) - Unless sources will be added
2. **Clean up speculative/future links** (ai-prompts, ethics guidelines, etc.)

## Implementation Script Suggestions

1. **Batch fix navigation links** - Add `.md` to all sidebar links
2. **Create stub generator** - Auto-create missing pages with basic templates
3. **Code block wrapper** - Find and fix lambda expressions in documentation
4. **Path validator** - Check all relative paths match actual file structure

Total fixes needed: ~170 (excluding code false positives which need manual review)