# Matrix Online Wiki Link Validation Report

## Executive Summary

**Date:** June 4, 2025  
**Total Wiki Health Score:** 86% (581 working links out of 669 total)

### Key Metrics
- **Total markdown files scanned:** 124
- **Total internal links found:** 669
- **Working links:** 581
- **Broken links:** 88 (all are .md file references)
- **Broken directories:** 0

## Critical Issues Found

### 1. Sources Directory Structure Problem
The `sources/index.md` file contains **24 broken links** - the highest concentration in the wiki. This appears to be a systematic issue where source files are expected but don't exist.

**Pattern:** Links to non-existent `-sources.md` files:
- `01-getting-started/timeline-liberation-complete-sources.md`
- `02-server-setup/mxoemu-setup-sources.md`
- etc.

### 2. Missing Cross-Reference Files
Several important files are referenced but don't exist:
- `pkb-tools.md` (2 references)
- `pkb-archive-investigation.md` (2 references)
- `gm-commands.md`
- `custom-content.md`
- `mission-examples.md`
- `mission-creator.md`

### 3. Incorrect Relative Path Navigation
Many broken links use incorrect relative paths:
- `../sources/` references from main content directories
- `../06-file-formats/index.md` (directory doesn't exist)
- `../07-story-lore/` (directory doesn't exist)

## Top 10 Most Broken Links

1. **pkb-tools.md** (2 occurrences)
2. **pkb-archive-investigation.md** (2 occurrences)
3. texture-archive.md
4. submit-story.md
5. server-security-hardening.md
6. screenshot-guide.md
7. pkb-research.md
8. performance-monitoring.md
9. network-protocol.md
10. navigation-tools.md

## Files with Most Broken Links

1. **sources/index.md** - 24 broken links
2. **02-server-setup/mxoemu-setup.md** - 3 broken links
3. **08-community/github-workflow-contribution-framework.md** - 2 broken links
4. **08-community/event-planning-templates.md** - 2 broken links
5. **06-gameplay-systems/character-development-complete.md** - 2 broken links

## Recommended Actions (Priority Order)

### Immediate Actions (High Priority)

1. **Remove or restructure the sources directory**
   - Either create all missing source files OR
   - Remove the sources directory and update all references

2. **Create critical missing files:**
   ```
   - 02-server-setup/gm-commands.md
   - 02-server-setup/custom-content.md
   - 04-tools-modding/pkb-tools.md
   - 05-game-content/mission-examples.md
   - 05-game-content/mission-creator.md
   ```

3. **Fix directory structure mismatches:**
   - Rename or create missing directories like `06-file-formats`, `07-story-lore`
   - Update all references to match actual directory structure

### Medium Priority

4. **Update relative path references**
   - Fix all `../sources/` references
   - Correct paths that go up then down unnecessarily

5. **Create placeholder files for less critical missing content:**
   - navigation-tools.md
   - screenshot-guide.md
   - texture-archive.md
   - character-profiles.md

### Low Priority

6. **Consolidate duplicate references**
   - Merge similar content (e.g., pkb-related files)
   - Create canonical locations for commonly referenced topics

## Link Categories Breakdown

### By Target Type
- **Missing configuration/admin files:** 8
- **Missing tool documentation:** 15
- **Missing content/story files:** 12
- **Missing source reference files:** 24
- **Incorrect path navigation:** 29

### By Source Directory
- Most broken links originate from:
  - `/sources/` (24)
  - `/02-server-setup/` (11)
  - `/05-game-content/` (16)
  - `/04-tools-modding/` (9)

## Conclusion

The wiki has an 86% link health score, which is good but has room for improvement. The main issues are:

1. A systematic problem with the sources directory structure
2. Missing key documentation files for tools and server administration
3. Inconsistent directory naming and structure

Addressing these issues in priority order will significantly improve wiki navigation and user experience. Start with removing/fixing the sources directory, then create the critical missing files, and finally clean up the directory structure inconsistencies.