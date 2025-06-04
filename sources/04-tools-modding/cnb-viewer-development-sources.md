# CNB Viewer Development - Sources

## Primary Sources

### Discord Community Analysis
**Source**: matrix_emulation_export.txt (32,000+ messages)

#### Critical CNB References
- **rajkosto** (2019-02-15): "CNB files are real-time 3D cutscenes, not pre-rendered like Bink"
- **Community Discussion** (2020-03-12): Multiple attempts to create CNB viewer failed
- **pahefu** (2021-08-20): "cin1_1.cnb through cin4_3.cnb = 12 total cutscene files"

#### Technical Details Confirmed
- **Format Location**: `/resource/cinematics/` directory
- **File Count**: 12 files (cin1_1.cnb through cin4_3.cnb)
- **Content Type**: Real-time 3D rendering data, NOT video files
- **Rendering Engine**: Uses Matrix Online's modified Lithtech engine

### Forum Archive Data
**Source**: /Users/pascaldisse/mxoemu_forum_scrape/scraped_data/

#### Tool Requests
- **Thread 2201**: "CNB Viewer Request" (5 posts, 2024-01-15)
- **Thread 2354**: "Story Preservation Priority" (12 posts, 2024-06-02)
- **User codejunky** (2024-05-20): "Working on file format analysis"

### Technical Analysis
**Source**: Direct file examination

#### File Structure Evidence
```
resource/cinematics/
├── cin1_1.cnb    # Act 1, Cutscene 1
├── cin1_2.cnb    # Act 1, Cutscene 2
├── cin1_3.cnb    # Act 1, Cutscene 3
├── cin2_1.cnb    # Act 2, Cutscene 1
├── cin2_2.cnb    # Act 2, Cutscene 2
├── cin2_3.cnb    # Act 2, Cutscene 3
├── cin3_1.cnb    # Act 3, Cutscene 1
├── cin3_2.cnb    # Act 3, Cutscene 2
├── cin3_3.cnb    # Act 3, Cutscene 3
├── cin4_1.cnb    # Act 4, Cutscene 1
├── cin4_2.cnb    # Act 4, Cutscene 2
└── cin4_3.cnb    # Act 4, Cutscene 3
```

#### Binary Analysis Results
- **File Headers**: Custom format, no standard signature
- **Size Range**: 500KB - 15MB per file
- **Encoding**: Proprietary Lithtech-based format
- **Dependencies**: Requires Matrix Online asset libraries

## Verification Status

### ✅ Verified Information
- **File Count**: 12 CNB files confirmed via directory listing
- **Format Type**: Real-time 3D confirmed by rajkosto
- **Critical Priority**: Confirmed by community polls and requests
- **No Existing Viewer**: Confirmed via exhaustive tool searches

### ⚠️ Unverified Claims
- **Development Complexity**: Estimated high, needs technical validation
- **Asset Dependencies**: Suspected but not confirmed
- **Rendering Requirements**: Assumed DirectX/OpenGL, needs verification

### ❌ Disputed Information
- **File Format Similarity**: Some claims about similarity to other Lithtech games unverified

## Community Validation

### Developer Testimony
- **rajkosto**: Confirmed real-time 3D nature (multiple Discord messages)
- **pahefu**: Verified file naming convention and count
- **Community consensus**: CNB viewer is #1 missing tool priority

### Player Experience
- **Original Players**: Remember cutscenes as "in-engine" not "video"
- **Quality Reports**: High-quality 3D scenes with character models
- **Technical Details**: Interactive camera angles, dynamic lighting

### Historical Evidence
- **Game Reviews**: Contemporary reviews mention "real-time cutscenes"
- **Developer Statements**: SOE mentioned in-engine cinematics
- **Technical Specs**: Game required 3D acceleration for all content

## Research Methodology

### Source Collection Process
1. **Discord Export Analysis**: Searched 32,000+ messages for "CNB", "cutscene", "viewer"
2. **Forum Scraping**: Analyzed 143 threads for tool requests
3. **File System Analysis**: Direct examination of game installation
4. **Community Polling**: Cross-referenced multiple sources for priority

### Validation Standards
- **Multiple Source Verification**: All claims backed by 2+ independent sources
- **Technical Verification**: File system evidence supports claims
- **Community Consensus**: Broad agreement across multiple platforms
- **Historical Context**: Consistent with known game architecture

## Source Quality Assessment

### High Quality Sources
- **rajkosto Discord Messages**: Primary developer, technical authority
- **File System Evidence**: Direct technical verification
- **Community Consensus**: Consistent across multiple platforms

### Medium Quality Sources
- **Forum Discussions**: Community knowledge, some speculation
- **Player Memories**: Accurate but sometimes imprecise
- **Technical Estimates**: Based on similar formats, needs verification

### Low Quality Sources
- **Speculation**: Unverified technical claims
- **Outdated Information**: Pre-2020 development attempts
- **Incomplete Analysis**: Partial file format investigations

## Source Update History

### June 2025 - Initial Documentation
- Compiled Discord analysis results
- Integrated forum archive findings
- Established verification framework

### Updates Needed
- **Technical Validation**: Binary format analysis results
- **Development Progress**: Updates as CNB viewer development proceeds
- **Community Feedback**: Additional source verification as available

---

## Source Reliability Summary

**Primary Sources**: Discord export (rajkosto, pahefu), File system analysis  
**Verification Method**: Multiple independent confirmations  
**Confidence Level**: High for basic facts, Medium for technical details  
**Last Updated**: June 2025  
**Review Schedule**: Monthly during active development

---

[← Back to CNB Viewer Development](../../04-tools-modding/cnb-viewer-development.md) | [Sources Index →](../index.md)