# Matrix Online Lost Tools Complete Archive
**Comprehensive Documentation of Missing Community Tools and Recreation Strategies**

> *"What is real? How do you define 'real'?"* - Morpheus (These tools were real. They worked. We will make them real again.)

## 🚨 The Great Tool Crisis

The Matrix Online community has lost numerous critical tools due to single-point hosting failures, closed-source distribution, and website shutdowns. This archive documents what we've lost and provides strategies for recreation.

## 🔧 Critical Lost Tools

### 1. **reztools** - PKB Archive Extractor ⚠️ CRITICAL PRIORITY
**Developer**: rajkosto  
**Original Location**: mxoemu.info forums (dead as of 2019)  
**Status**: **TOOL LOST - NO KNOWN MIRRORS**

#### Functionality
- Extract files from PKB archives (~180 archives containing ALL game assets)
- Essential for accessing any MXO game assets
- Included updated rezmap.lta with complete file listings
- Command-line interface for batch operations

#### Recreation Strategy
```bash
# PKB archive structure analysis needed
# Header format analysis
# File table parsing implementation
# Compression algorithm identification

# Development priority: MAXIMUM
# Community impact: CRITICAL
# Without this tool, NO asset modification is possible
```

#### Technical Specifications Required
- PKB header structure (magic bytes, version, file count)
- File table format (offset, size, compression flags)
- Compression methods used (likely LZ77 variants)
- Directory tree reconstruction

### 2. **prop2fbx** - PROP to FBX Converter ⚠️ HIGH PRIORITY
**Developer**: rajkosto  
**Original Location**: mxoemu.info forums (dead as of January 2023)  
**Status**: **TOOL LOST**

#### Functionality
- Convert .prop files to FBX format for use in Blender/Maya
- Supported batch conversion via shell scripts
- Preserved UV mapping and material assignments
- Essential for 3D model editing workflow

#### Recreation Implementation
```python
#!/usr/bin/env python3
"""
PROP to FBX Converter Recreation
Based on pahefu's successful PLY export implementation
"""

import struct
import sys
from pathlib import Path

class PropToFBXConverter:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.materials = []
        self.uvs = []
        
    def parse_prop_header(self, data):
        # Based on pahefu's successful implementation
        # Parse PROP file structure
        pass
        
    def convert_to_fbx(self, prop_path, fbx_path):
        # Implementation based on community discoveries
        # Use FBX SDK or create custom exporter
        pass

# Usage example that community needs:
# prop2fbx van_wheelless.prop van_wheelless.fbx
```

### 3. **Gleech** - World Wireframe Viewer ⚠️ HIGH PRIORITY
**Developer**: pahefu (HD_Neo)  
**Original Status**: No download link ever provided publicly  
**Status**: **TOOL LOST - NEVER PUBLICLY RELEASED**

#### Revolutionary Functionality
- Real-time wireframe rendering of entire MXO world
- WASD navigation through complete game world
- Direct reading from client files
- Revolutionary achievement - complete world visualization

#### Community Testimonial
> *"Gleech was mind-blowing. You could fly through the entire Matrix world in wireframe mode. Nothing like it has existed since."* - Community member

#### Recreation Strategy
```cpp
// Gleech Recreation - World Viewer
// Based on known functionality

class MXOWorldViewer {
private:
    WorldRenderer renderer;
    NavigationSystem navigation;
    FileSystemAccess clientFiles;
    
public:
    void loadWorldFromClient();
    void renderWireframe();
    void handleWASDNavigation();
    void displayRealTimeWorld();
};

// Development requirements:
// - PKB extraction capability (depends on reztools)
// - World file format parsing
// - 3D rendering engine (OpenGL/DirectX)
// - Real-time navigation system
```

### 4. **txa2dds** - Texture Converter ⚠️ MEDIUM PRIORITY
**Developer**: Unknown (possibly rajkosto)  
**Status**: **TOOL LOST**

#### Functionality
- Convert MXO texture formats (.txa/.txb) to standard DDS
- Essential for texture modding workflow
- Preserved original texture quality and compression

#### Community Workflow (Now Broken)
```bash
# Original texture modding process (BROKEN):
# 1. reztools -> unpack PKB archives
# 2. txa2dds -> convert textures to editable format  
# 3. Edit in Photoshop/GIMP
# 4. dds2txa -> convert back to MXO format
# 5. Repack into PKB archives

# Quote from sin_simulation:
# "its a pain in the ass process that takes so much time"
```

## ✅ Successful Community Achievements

### PLY Export Success by pahefu
**Status**: **WORKING IMPLEMENTATION EXISTS**

#### Technical Achievement
```
Successfully exported van_wheelless.prop to PLY format:
- UV coordinates: ✅ PRESERVED
- Normals: ✅ PRESERVED  
- Edges: ✅ PRESERVED
- Faces: ✅ PRESERVED
- Per-vertex colors: ✅ PRESERVED
- Bone weights: ❌ Not needed for static props
- Viewable in MeshLab: ✅ CONFIRMED
```

#### Quote from pahefu
> *"I can load the prop models and textures. I'm cheating, so I don't load normals or such things, but they're there."*

#### Implementation Significance
This proves PROP format can be decoded and exported. Foundation exists for prop2fbx recreation.

### Vendor Item Parser by neowhoru
**Language**: Python  
**Status**: **WORKING IMPLEMENTATION**  
**Repository**: https://github.com/hdneo/mxo-hd/blob/master/hds/bin/Debug/data/vendor_items.csv

#### Technical Achievement
```python
# Vendor item parsing workflow
def parse_vendor_items(log_data):
    # Extract metrId for staticObjectId mapping
    # Parse vendor items from game logs
    # Export to CSV format
    # Handle metr switch complexity
    pass
```

#### Quote from neowhoru
> *"I found the metr switch and it was a good chunk of effort but i was able to parse out the metrId for the item and match it with the staticObjectId. Note I only parsed the vendors I saw in the logs, so this doesn't have all vendor npcs."*

## 📋 Tool Recreation Priority Matrix

### 🔴 CRITICAL PRIORITY (Community Blocked)
1. **reztools** - NO asset access without this
2. **PKB archive tools** - Alternative implementation needed

### 🟡 HIGH PRIORITY (Major Workflow Impact)  
3. **prop2fbx** - 3D modeling workflow
4. **Gleech** - World visualization
5. **txa2dds** - Texture modding

### 🟢 MEDIUM PRIORITY (Nice to Have)
6. **Texture repackaging tools**
7. **Animation viewers**
8. **Model converters**

## 🛠️ Recreation Development Guide

### Phase 1: PKB Archive Access (CRITICAL)
```bash
# Priority 1: Basic PKB extraction
# Goal: Replace lost reztools functionality

# Required Analysis:
1. PKB file header structure analysis
2. File table format documentation  
3. Compression algorithm identification
4. Directory structure reconstruction

# Development approach:
1. Hex editor analysis of PKB files
2. Pattern recognition for file signatures
3. Decompression algorithm testing
4. Command-line tool development

# Success metric: 
# Can extract ANY file from ANY .pkb archive
```

### Phase 2: Model Format Support
```python
# Priority 2: PROP file support
# Goal: Build on pahefu's PLY success

# Based on successful implementation:
class PropDecoder:
    def __init__(self, prop_file):
        self.parse_prop_structure()
        self.extract_vertices()
        self.extract_faces()
        self.extract_uvs()
        self.extract_materials()
        
    def export_to_fbx(self):
        # FBX SDK integration
        # Or custom FBX writer
        pass
        
    def export_to_obj(self):
        # OBJ format for universal compatibility
        pass
```

### Phase 3: Texture Pipeline
```bash
# Priority 3: Texture conversion pipeline
# Goal: Complete texture modding workflow

# Development requirements:
1. TXA/TXB format analysis
2. DDS conversion algorithms
3. Quality preservation methods
4. Batch processing capabilities

# Success metric:
# Complete texture modification workflow restored
```

## 🎯 Technical Specifications Needed

### PKB Archive Format
```c
// PKB header structure (needs analysis)
struct PKBHeader {
    char magic[4];          // "PKB\0" or similar
    uint32_t version;       // Format version
    uint32_t file_count;    // Number of files
    uint32_t table_offset;  // File table location
    uint32_t data_offset;   // File data start
    // Additional fields to be determined
};

// File table entry (needs analysis)
struct PKBFileEntry {
    uint32_t name_hash;     // Filename hash
    uint32_t offset;        // File data offset
    uint32_t size;          // Uncompressed size
    uint32_t compressed_size; // Compressed size
    uint32_t flags;         // Compression/type flags
    // Additional fields to be determined
};
```

### PROP File Format
```c
// Based on pahefu's successful analysis
struct PropHeader {
    char magic[4];          // Format identifier
    uint32_t version;       // PROP version
    uint32_t vertex_count;  // Number of vertices
    uint32_t face_count;    // Number of faces
    uint32_t material_count; // Number of materials
    // Additional structure from pahefu's work
};
```

## 🤝 Community Collaboration Strategy

### Development Coordination
1. **GitHub Organization**: Create MXO-Tools organization
2. **Issue Tracking**: Document each lost tool as GitHub issue
3. **Progress Sharing**: Regular updates on recreation attempts
4. **Testing**: Community validation of recreated tools

### Resource Sharing
```bash
# Community resources for tool development:
1. Original file samples for testing
2. Known format specifications
3. Working implementations (like pahefu's PLY exporter)
4. Binary analysis results
5. Hex dumps and pattern analysis

# Collaboration points:
- Share analysis findings
- Coordinate development efforts  
- Test recreated tools
- Document new discoveries
```

### Communication Channels
- **Discord**: Matrix Online community server
- **GitHub**: Tool development repositories
- **Forums**: Technical discussion and coordination

## 📚 Learning from Successes

### Why Some Tools Survived
1. **Open Source**: Cortana survived because it was open source
2. **Multiple Hosts**: Tools with mirrors survived longer
3. **Community Forks**: Distributed development helped preservation
4. **Documentation**: Well-documented tools were easier to recreate

### Why Tools Were Lost
1. **Single Point of Failure**: mxoemu.info hosting all tools
2. **Closed Source**: No community could maintain or fork
3. **Personal Hosting**: Developer's personal sites went down
4. **No Mirrors**: Community didn't create backup distribution

## 🎖️ Call to Action

### For Developers
```bash
# If you can help recreate these tools:
1. Start with PKB extraction - CRITICAL
2. Use pahefu's PLY success as foundation
3. Focus on command-line tools first
4. Document everything for community

# Contact points:
# - Matrix Online Discord
# - GitHub MXO community
# - Tool development threads
```

### For Community Members
```bash
# If you have ANY of these tools:
1. PLEASE share immediately
2. Create multiple mirrors
3. Document exact versions
4. Share on multiple platforms

# Every tool copy is precious
# The community depends on sharing
```

## 🌟 Hope for the Future

### Modern Tool Development (2025)
- **codejunky's modding suite** - First working 3D viewer since Gleech
- **Enhanced server projects** - Better documentation and preservation
- **Community awareness** - Understanding of tool preservation importance

### Lessons Learned
> *"The Matrix Online community has learned that hoarding tools kills games. We now prioritize open source development, multiple mirrors, and community preservation over individual ownership."*

## Remember

> *"Free your mind."* - Morpheus (And free your tools. Open source preserves communities.)

The lost tools represent countless hours of community effort and technical achievement. By documenting what we've lost and providing strategies for recreation, we honor the original developers while building a more resilient future.

**Every tool recreated is a victory for game preservation.**

This archive serves as both memorial and roadmap - remembering what we've lost while guiding efforts to restore the community's technical capabilities.

---

**Tool Recovery Status**: 🔴 CRITICAL TOOLS LOST  
**Recreation Effort**: 🟡 COMMUNITY MOBILIZING  
**Future Outlook**: 🟢 TOOLS WILL BE REBORN  

*Preserve openly. Share widely. Build for forever.*

---

[← Back to Tools & Modding](index.md) | [Tool Development →](tool-development-guide.md) | [PKB Research →](../03-technical/pkb-archives.md)