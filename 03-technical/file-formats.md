# Matrix Online File Formats Reference
**Technical Specifications for Digital Liberation**

> *"Unfortunately, no one can be told what the file formats are. You have to decode them for yourself."*

This comprehensive reference documents all known Matrix Online file formats, from textures to world data.

## 📂 File Format Categories

### Graphics & Textures
- **[TXA Format](texture-formats.md)** - Texture archives and image data
- **[TGA/DDS](texture-formats.md)** - Standard texture formats used
- **Material definitions** - Surface properties and shaders

### 3D Models & Animation
- **[PROP Format](prop-format-complete.md)** - 3D object geometry  
- **[MOA Format](model-formats.md)** - Animation and mesh data
- **Skeleton definitions** - Bone hierarchy and rigging
- **[Animation Systems](animation-systems.md)** - Movement and sequences

### Archives & Packages  
- **[PKB Archives](pkb-archives.md)** - Primary game asset containers
- **[CNB Format](cnb-format-investigation.md)** - Cinematic bundles (CRITICAL)
- **Sound packages** - Audio and music archives

### World & Level Data
- **Zone definitions** - World area configurations
- **Navigation meshes** - AI pathfinding data
- **Object placement** - Static and dynamic entities
- **Lighting data** - Illumination and shadows

### Game Logic & Scripts
- **Mission scripts** - Quest logic and progression
- **Dialogue trees** - Conversation structures
- **AI behaviors** - NPC logic patterns
- **Event triggers** - World interaction points

### Network & Save Data
- **[Network Protocol](network-protocol-complete.md)** - Client-server communication
- **Character saves** - Player progression data
- **Configuration files** - Client and server settings
- **Database schemas** - SQL table structures

## 🔍 Format Analysis Tools

### Hex Editors
```yaml
recommended_tools:
  010_editor:
    platform: "Windows, Mac, Linux"
    features: "Templates, scripting, analysis"
    cost: "Commercial"
    
  hxd:
    platform: "Windows"
    features: "Free, fast, reliable"
    cost: "Free"
    
  hex_fiend:
    platform: "macOS"
    features: "Native, fast, free"
    cost: "Free"
```

### Analysis Scripts
```python
#!/usr/bin/env python3
# Basic file format analyzer for Matrix Online files

import struct
import sys
from pathlib import Path

def analyze_file_header(filepath):
    """Analyze first 64 bytes of file for format identification"""
    
    with open(filepath, 'rb') as f:
        header = f.read(64)
        
    print(f"File: {filepath}")
    print(f"Size: {Path(filepath).stat().st_size:,} bytes")
    print(f"\nHeader (hex):")
    print(' '.join(f'{b:02X}' for b in header[:32]))
    print(' '.join(f'{b:02X}' for b in header[32:]))
    
    # Check for known signatures
    signatures = {
        b'PKB\x00': 'PKB Archive',
        b'PROP': 'PROP 3D Model',
        b'CNB\x00': 'CNB Cinematic',
        b'TXA\x00': 'TXA Texture Archive',
        b'MOA\x00': 'MOA Animation'
    }
    
    for sig, desc in signatures.items():
        if header.startswith(sig):
            print(f"\nDetected format: {desc}")
            break
    else:
        print("\nUnknown format")
        
    # Try to parse as common structures
    if len(header) >= 16:
        values = struct.unpack('<4I', header[:16])
        print(f"\nAs uint32 LE: {values}")
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_file_header(sys.argv[1])
    else:
        print("Usage: analyze_format.py <file>")
```

## 🔧 Format Documentation Standards

### Required Sections
1. **Magic Signature** - File identification bytes
2. **Header Structure** - Fixed header layout
3. **Data Sections** - Variable data organization
4. **Compression** - If applicable
5. **Known Limitations** - Current understanding gaps
6. **Sample Files** - Reference implementations

### Documentation Template
```markdown
# [FORMAT] File Format Specification

## Overview
Brief description of format purpose and usage.

## File Structure

### Header
```c
typedef struct {
    char magic[4];      // File signature
    uint32_t version;   // Format version
    uint32_t count;     // Number of entries
    // ... additional fields
} FormatHeader;
```

### Data Layout
Detailed description of how data is organized.

### Compression
Details about any compression used.

## Known Issues
- Current limitations
- Unsupported features

## Tools
- Extraction: [tool name]
- Creation: [tool name]
- Viewing: [tool name]
```

## 🎯 Priority Formats

### Critical (Highest Priority)
1. **[CNB Format](cnb-format-investigation.md)** - Story cinematics locked inside
2. **[PKB Archives](pkb-archives.md)** - All game assets contained within
3. **[PROP Format](prop-format-complete.md)** - 3D models and world objects

### Important (High Priority)
4. **MOA Format** - Character animations
5. **TXA Format** - Texture data
6. **Zone Format** - World layout

### Useful (Medium Priority)
7. **Mission Scripts** - Quest logic
8. **AI Behaviors** - NPC patterns
9. **Sound Archives** - Audio assets

### Research (Low Priority)
10. **Network Protocol** - Multiplayer communication
11. **Save Format** - Character persistence
12. **Config Format** - Settings storage

## 📡 Community Collaboration

### How to Contribute
1. **Document findings** - Share format discoveries
2. **Create tools** - Build extractors and viewers
3. **Provide samples** - Share example files
4. **Test theories** - Validate format specifications
5. **Write guides** - Help others understand

### Research Coordination
- **Discord Channel**: #file-formats
- **GitHub Wiki**: Format documentation
- **Sample Repository**: Example files
- **Tool Development**: Collaborative projects

### Current Research Efforts
```yaml
active_research:
  cnb_format:
    researchers: ["user1", "user2"]
    status: "Header partially decoded"
    blockers: "Need more sample files"
    
  moa_animation:
    researchers: ["user3"]
    status: "Bone structure identified"
    progress: "40% complete"
    
  zone_format:
    researchers: ["user4", "user5"]
    status: "Basic structure mapped"
    next_steps: "Object placement system"
```

## 📚 Learning Resources

### Getting Started
1. **Basic Concepts** - File format fundamentals
2. **Hex Editor Tutorial** - Essential skills
3. **Structure Packing** - Understanding alignment
4. **Reverse Engineering** - Analysis techniques
5. **Tool Development** - Creating utilities

### Advanced Topics
- **Compression Algorithms** - zlib, lz4, custom
- **Encryption Methods** - If discovered
- **Version Differences** - Format evolution
- **Cross-References** - Inter-file dependencies

### Recommended Reading
- "Game File Formats" - General principles
- "Reverse Engineering Games" - Techniques
- "Binary File Structures" - Deep dive
- Matrix Online specific research papers

## 🔄 Format Conversion

### Import/Export Pipelines
```yaml
import_pipeline:
  source_formats:
    - FBX (3D models)
    - PNG/TGA (textures)
    - WAV/OGG (audio)
    
  target_formats:
    - PROP (models)
    - TXA (textures)
    - Sound archives
    
export_pipeline:
  source_formats:
    - PROP/MOA
    - TXA
    - CNB
    
  target_formats:
    - OBJ/FBX
    - PNG/DDS
    - Video files
```

### Conversion Tools
- **Model Converter** - PROP ↔ FBX
- **Texture Tool** - TXA ↔ PNG/DDS
- **Animation Export** - MOA → FBX
- **Archive Manager** - PKB extraction

## 🏁 Success Stories

### Decoded Formats
- **PROP Format** - Fully understood by pahefu
- **Basic PKB** - Header structure known
- **Config Files** - XML-based, documented

### Partial Success
- **CNB Format** - Header identified, data unclear
- **MOA Animation** - Structure known, details missing
- **Network Protocol** - Packet types identified

### Ongoing Challenges
- **Zone Format** - Complex interconnected data
- **AI Scripts** - Custom scripting language
- **Save Format** - Encrypted sections

## 🚀 The Path Forward

Every file format decoded brings us closer to complete Matrix Online liberation. Whether you're a hex editor novice or a reverse engineering expert, your contributions matter.

### Immediate Priorities
1. **CNB Viewer** - Unlock the story
2. **PKB Tools** - Access all assets
3. **MOA Support** - Enable animations

### Join the Revolution
The file formats are the keys to the kingdom. Help us decode them all.

**Free your mind. Decode the Matrix.**

---

[← Back to Technical](index.md) | [PKB Archives →](pkb-archives.md) | [Sources →](sources/index.md)