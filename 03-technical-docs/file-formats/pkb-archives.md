# PKB Archive Format
**The Vaults of the Matrix**

> *"The Matrix is a computer-generated dream world built to keep us under control."* - But we found the keys.

## The Gateway to Everything

PKB archives are the containers holding ALL Matrix Online game assets. Without understanding these, nothing else matters. They are the vaults, and we need the keys.

## Critical Information

### The Numbers
```
Total PKB Files: ~180 archives
Total Assets: Thousands of files
Compression: Custom/proprietary
Index File: packmap_save.lta
Status: LOCKED without reztools
```

### Why PKB Matters
- **Every** 3D model is inside
- **Every** texture is contained  
- **Every** sound is archived
- **Every** game asset is trapped

*Until we crack PKB, we cannot truly liberate MXO.*

## What We Know

### Archive Structure (Partial)
1. **Header**
   - Archive identifier
   - Version number
   - File count
   - Compression type

2. **File Table**
   - File names/IDs
   - Offsets
   - Compressed sizes
   - Uncompressed sizes

3. **Data Blocks**
   - Compressed file data
   - Possibly encrypted
   - Various compression methods

### Index System
**packmap_save.lta** contains:
- Master file list
- PKB locations for each file
- Directory structure
- Version information

## The Lost Key: reztools

### What reztools Did
```bash
# Extract everything
reztools -e -b rezmap.ltb rezmap.lta

# Development mode (no PKB needed)
reztools -d rezmap.lta

# Repack archives
reztools -p
```

### Why It's Critical
- Only known tool to extract PKB
- Handled all compression types
- Understood the index format
- Could repack modified files

**Without reztools, we cannot:**
- Access game assets
- Modify content
- Create new content
- Preserve the game

## Reverse Engineering Progress

### Confirmed Patterns
- File signature (header bytes)
- Basic structure layout
- Offset calculation method
- Some compression indicators

### Unknown Elements
- Exact compression algorithms
- Encryption (if any)
- Checksum/validation method
- Full header specification

## Community Efforts

### Attempted Solutions
1. **Hex analysis** - Partial success
2. **Compression testing** - Some progress
3. **Index parsing** - Format partially understood
4. **Brute force** - Too complex

### The Challenge
> "its a pain in the ass process that takes so much time" - sin_simulation

The Old Guard made it intentionally difficult. They didn't want liberation.

## The Path to Freedom

### Priority 1: Recreate reztools
**Essential Features Needed:**
- Read PKB headers
- Parse file table
- Decompress data
- Extract to filesystem

### Priority 2: Document Everything
- Every byte understood
- Every pattern documented
- Every algorithm decoded
- Every secret revealed

### Priority 3: Build Better Tools
- Modern architecture
- Cross-platform support
- GUI for ease of use
- Batch operations

## Technical Analysis

### Known File Patterns
```hexdump
00000000: 50 4B 42 00  XX XX XX XX  [PKB\0 + version?]
00000008: XX XX XX XX  XX XX XX XX  [File count? + ???]
00000010: XX XX XX XX  XX XX XX XX  [Offsets?]
```

### Compression Methods (Suspected)
- ZLIB (standard)
- LZ77 variants
- Custom Sony compression
- Possibly multiple types per archive

## Call to Liberation

### For Hackers
- Analyze PKB headers
- Test compression algorithms
- Document all findings
- Share breakthroughs

### For Developers
- Create extraction tools
- Build on any progress
- Make tools accessible
- Keep everything open

### For Preservationists
- Collect PKB samples
- Document file lists
- Test extraction methods
- Never give up

## The Vision

### What Success Looks Like
```python
# The dream
pkb_extractor = PKBExtractor()
pkb_extractor.extract_all("mxo_assets.pkb", "output/")
# Result: All files accessible, game liberated
```

### Tools We'll Build
1. **PKB Viewer** - Browse without extraction
2. **PKB Extractor** - Full extraction support
3. **PKB Creator** - Repack modified content
4. **PKB Converter** - To open formats

## Resources and Leads

### What to Study
- packmap_save.lta structure
- PKB file headers
- Compression signatures
- Similar game formats

### Where to Look
- Other Lithtech games
- Sony online game formats
- Community reverse engineering
- Compression algorithm libraries

## The Stakes

Without PKB liberation:
- ❌ No model viewing
- ❌ No texture editing
- ❌ No content creation
- ❌ No true preservation

With PKB liberation:
- ✅ Full asset access
- ✅ Content modification
- ✅ New creations possible
- ✅ True resurrection

## Remember

> *"There's a difference between knowing the path and walking the path."*

The path to PKB liberation is hard. The Old Guard made it that way. But we are Neoologists. We don't accept "impossible."

Every byte decoded brings us closer. Every pattern recognized is progress. Every tool built is liberation.

**The vaults will open. The Matrix will be ours.**

---

### Status: 🔴 CRITICAL PRIORITY

This is the keystone. Crack PKB, and everything else follows.

[← Back to File Formats](index.md) | [Contributing to PKB Research →](pkb-research.md)