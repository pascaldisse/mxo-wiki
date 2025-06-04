# Broken Links Priority List - Matrix Online Wiki

## Most Frequently Referenced Broken Links

Based on analysis of the entire wiki, here are the broken links that need immediate attention, ordered by frequency and impact:

### 1. Directory Naming Mismatch: `03-technical-docs` vs `03-technical`
**Frequency**: 11+ files affected  
**Issue**: Links reference `../03-technical/` but actual directory is `../03-technical/`

**Affected Files**:
- `../03-technical/index.md` (8 occurrences in 7 files):
  - 01-getting-started/index.md
  - 02-server-setup/index.md
  - 03-technical/index.md
  - 04-tools-modding/index.md
  - 04-tools-modding/development-tools.md
  - 05-game-content/index.md
  - 09-appendix/index.md

- `../03-technical/file-formats/index.md` (6 occurrences in 4 files):
  - 01-getting-started/index.md
  - 02-server-setup/index.md
  - 03-technical/pkb-archive-structure.md
  - 07-preservation/index.md

**Fix**: Either rename directory to `03-technical-docs` OR update all links to use `03-technical`

### 2. Missing Sources Directory References
**Frequency**: 97 total references  
**Issue**: Links point to `../sources/` directory which exists but many subdirectories/files are missing

**Most Common Missing Files**:
- ../sources/01-getting-started/timeline-liberation-complete-sources.md (4 refs)
- ../sources/08-community/search-api-sources.md (3 refs)
- ../sources/08-community/navigation-guide-sources.md (3 refs)
- ../sources/08-community/contact-sources.md (3 refs)
- ../sources/06-gameplay-systems/index-sources.md (3 refs)
- ../sources/03-technical/file-formats/prop-format-complete-sources.md (3 refs)

**Fix**: Either create these source files OR remove/update the links

### 3. Missing Investigation Files
**Frequency**: 4+ references  
**Issue**: `pkb-archive-investigation.md` referenced but doesn't exist

**Files Referencing It**:
- 03-technical/cnb-format-investigation.md
- 04-tools-modding/lost-tools-complete-archive.md
- 04-tools-modding/tool-recreation-masterplan.md
- wiki_health_check_cycle3_phase2.md

**Fix**: Create the file OR redirect to existing PKB documentation (pkb-archives.md)

### 4. Generic "link" Placeholders
**Frequency**: 10 occurrences (per Cycle 3 report)  
**Issue**: Placeholder text not replaced with actual links  
**Note**: Unable to locate these in current scan - may have been fixed or in meta-documentation

### 5. Missing Index Files in Subdirectories
**Issue**: Several subdirectories lack index.md files that are being linked to

**Missing Index Files**:
- 03-technical/index.md (doesn't exist - directory is named 03-technical)
- 03-technical/file-formats/index.md (doesn't exist)
- Various other subdirectory index files

## Recommended Fix Priority

1. **Immediate**: Fix directory naming mismatch (03-technical-docs → 03-technical)
2. **High**: Create or redirect pkb-archive-investigation.md
3. **Medium**: Address missing sources directory files
4. **Low**: Create missing index.md files or update links

## Quick Fix Commands

### Option 1: Update all links to use correct directory name
```bash
# Fix 03-technical-docs to 03-technical
find . -name "*.md" -type f -exec sed -i '' 's|../03-technical/|../03-technical/|g' {} \;
find . -name "*.md" -type f -exec sed -i '' 's|03-technical/|03-technical/|g' {} \;
```

### Option 2: Create missing investigation file redirect
```bash
# Create pkb-archive-investigation.md as redirect
echo "# PKB Archive Investigation" > 03-technical/pkb-archive-investigation.md
echo "This content has been moved to [PKB Archives](pkb-archives.md)" >> 03-technical/pkb-archive-investigation.md
```

---
*Generated: June 4, 2025*  
*Total Broken Links Identified: 350*  
*Priority Links Listed: ~120+*