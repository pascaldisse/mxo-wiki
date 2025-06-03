# CNB Viewer Development Guide
**Building the Key to Liberation**

> *"The Matrix cannot tell you who you are."* - But CNB files can tell us what happened.

## 🎯 Mission: Decode the Cinematics

This guide provides a comprehensive roadmap for developing a CNB viewer - the most critical tool needed for Matrix Online preservation. We combine technical analysis, community knowledge, and the Neoologist approach to crack this format.

## Current Understanding

### What We Know for Certain
- **Location**: `/resource/cinematics/` directory
- **Files**: 12 total (cin1_1.cnb through cin4_3.cnb)
- **Type**: Real-time 3D cinematics, not pre-rendered video
- **Integration**: Uses player's RSI (avatar) in scenes
- **Engine**: Lithtech-based rendering system

### Technical Observations
From binary analysis of CNB files:
```
00000000: 434E 4220 0100 0000 | CNB .....  (Magic: "CNB ")
00000008: 3412 0000 2C01 0000 | File size, Scene count?
00000010: References to .ltb files (Lithtech Binary)
Various offsets pointing to .txa textures
```

## Development Approach

### Phase 1: Format Analysis (Current Priority)

#### 1.1 Header Structure Investigation
```python
# cnb_analyzer.py - Starting point
import struct

class CNBAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = open(filepath, 'rb').read()
        
    def analyze_header(self):
        # Check magic number
        magic = self.data[0:4]
        if magic == b'CNB ':
            print("Valid CNB file detected")
            
        # Parse potential header
        version = struct.unpack('<I', self.data[4:8])[0]
        file_size = struct.unpack('<I', self.data[8:12])[0]
        
        print(f"Version: {version}")
        print(f"File Size: {file_size}")
        
    def find_references(self):
        # Search for known extensions
        extensions = [b'.ltb', b'.txa', b'.wav', b'.dtx']
        for ext in extensions:
            offset = 0
            while True:
                pos = self.data.find(ext, offset)
                if pos == -1:
                    break
                # Backtrack to find filename
                start = pos
                while start > 0 and self.data[start-1] > 32:
                    start -= 1
                filename = self.data[start:pos+4].decode('ascii', errors='ignore')
                print(f"Found reference: {filename}")
                offset = pos + 1
```

#### 1.2 Compression Detection
```python
def detect_compression(data):
    # Check for zlib signature
    if data[0:2] == b'\x78\x9c':
        return "zlib"
    # Check for LZ4
    elif data[0:4] == b'\x04\x22\x4d\x18':
        return "lz4"
    # Check for custom Lithtech compression
    elif data[0:4] == b'LITH':
        return "lithtech_custom"
    return "unknown"
```

### Phase 2: Structure Mapping

#### 2.1 Scene Graph Hypothesis
Based on Lithtech engine knowledge:
```c
struct CNBHeader {
    char magic[4];      // "CNB "
    uint32_t version;   
    uint32_t file_size;
    uint32_t scene_count;
    uint32_t offset_table; // Points to scene locations
};

struct CNBScene {
    uint32_t id;
    uint32_t duration_ms;
    uint32_t camera_track_offset;
    uint32_t model_count;
    uint32_t animation_offset;
    uint32_t audio_trigger_offset;
};

struct CameraTrack {
    uint32_t keyframe_count;
    struct {
        float time;
        float position[3];
        float rotation[4]; // Quaternion
        float fov;
    } keyframes[];
};
```

#### 2.2 Resource Reference System
```python
class ResourceMapper:
    def __init__(self, cnb_data):
        self.references = {}
        self.parse_references(cnb_data)
        
    def parse_references(self, data):
        # Map internal IDs to external files
        # Models: .ltb files
        # Textures: .txa files
        # Sounds: .wav files
        pass
        
    def resolve_path(self, ref_id):
        # Convert ID to actual file path
        # Check PKB archives for resources
        pass
```

### Phase 3: Rendering Pipeline

#### 3.1 Minimal Viewer Implementation
```python
# cnb_viewer.py - Basic viewer structure
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class CNBViewer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.setup_gl()
        
    def setup_gl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, 800/600, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        
    def load_cnb(self, filepath):
        # Parse CNB file
        # Load referenced models
        # Setup animation tracks
        # Prepare audio triggers
        pass
        
    def render_frame(self, time_ms):
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Update camera position
        self.update_camera(time_ms)
        
        # Render models with animations
        for model in self.models:
            model.render(time_ms)
            
        # Trigger audio if needed
        self.check_audio_triggers(time_ms)
        
        pygame.display.flip()
```

#### 3.2 Model Loading Integration
```python
class LTBModelLoader:
    """Load Lithtech Binary models referenced by CNB"""
    
    def load(self, filepath):
        # Open LTB file from PKB archive
        # Parse model structure
        # Extract mesh data
        # Load animations
        # Return renderable object
        pass
```

### Phase 4: Advanced Features

#### 4.1 Player Avatar Integration
```python
class RSIIntegration:
    """Replace placeholder with player's avatar"""
    
    def __init__(self, player_rsi_data):
        self.rsi = player_rsi_data
        
    def replace_placeholder(self, scene, placeholder_id):
        # Find placeholder model in scene
        # Replace with player's RSI
        # Adjust animations for body type
        # Maintain original motion data
        pass
```

#### 4.2 Export Functionality
```python
class CNBExporter:
    """Export CNB to standard formats"""
    
    def to_video(self, cnb, output_path, fps=30):
        # Render each frame
        # Encode to video (MP4/AVI)
        # Include audio track
        pass
        
    def to_collada(self, cnb, output_path):
        # Export 3D scene data
        # Convert to COLLADA format
        # Preserve animations
        pass
```

## Community Collaboration Framework

### GitHub Repository Structure
```
mxo-cnb-viewer/
├── docs/
│   ├── format_spec.md      # Evolving format documentation
│   ├── findings.md         # Research discoveries
│   └── contributors.md     # Honor roll
├── src/
│   ├── analyzer/          # Format analysis tools
│   ├── parser/            # CNB parsing library
│   ├── viewer/            # Rendering implementation
│   └── exporter/          # Export utilities
├── samples/
│   ├── headers/           # CNB header dumps
│   └── tests/             # Test files
└── tools/
    ├── hex_patterns.py    # Pattern search tools
    └── compare_cnb.py     # File comparison
```

### Research Coordination

#### Discord Channel Structure
- **#cnb-research** - General discussion
- **#cnb-findings** - Breakthrough announcements
- **#cnb-dev** - Development coordination
- **#cnb-testing** - Tool testing results

#### Documentation Standards
```markdown
# CNB Research Finding #XXX
**Date**: 2025-06-04
**Researcher**: [Your name]
**File Analyzed**: cin1_1.cnb
**Offset**: 0x1234

## Discovery
[What you found]

## Evidence
[Hex dump or screenshot]

## Interpretation
[What you think it means]

## Next Steps
[What to investigate next]
```

## Technical Challenges & Solutions

### Challenge 1: Unknown Compression
**Problem**: Data appears compressed but algorithm unknown  
**Solutions**:
1. Try all standard algorithms (zlib, lz4, lzma)
2. Check Lithtech engine source for clues
3. Pattern match against known compressed data
4. Brute force small sections

### Challenge 2: Resource References
**Problem**: CNB references external files we can't locate  
**Solutions**:
1. Map references to PKB archive contents
2. Create placeholder resources for testing
3. Extract all game assets for cross-reference
4. Build resource dependency graph

### Challenge 3: Animation Format
**Problem**: Animation data structure unknown  
**Solutions**:
1. Compare with Lithtech .ltb animation format
2. Identify keyframe patterns
3. Test with simple movements first
4. Reverse engineer from motion patterns

## Success Metrics

### Milestone 1: Header Decoded ✓
- Magic number identified
- Basic structure mapped
- File sections located

### Milestone 2: First Frame Rendered
- Static scene visible
- Models loaded correctly
- Camera positioned properly

### Milestone 3: Animation Playback
- Camera movement working
- Model animations playing
- Timing synchronized

### Milestone 4: Full Playback
- Complete cinematic plays
- Audio synchronized
- Player avatar integrated

### Milestone 5: Public Release
- Stable viewer available
- Export features working
- Documentation complete

## Call to Action

### For Reverse Engineers
1. **Download** CNB files from game client
2. **Analyze** with hex editor (HxD, ImHex)
3. **Document** ALL findings, even "failures"
4. **Share** discoveries immediately

### For Developers
1. **Fork** the repository (when created)
2. **Implement** analysis tools
3. **Test** parsing approaches
4. **Collaborate** on Discord

### For Testers
1. **Try** every build released
2. **Report** crashes with details
3. **Suggest** UI improvements
4. **Celebrate** progress

## Resources & References

### Essential Tools
- **HxD / ImHex** - Hex editors
- **IDA Pro / Ghidra** - Disassemblers
- **Python** - Rapid prototyping
- **OpenGL/DirectX** - Rendering

### Lithtech Knowledge
- NOLF2 modding community (similar engine)
- Lithtech engine documentation
- LTB model format specifications
- Jupiter Engine references

### Related Formats
- Bink video (for comparison)
- COLLADA (for export)
- glTF (modern alternative)
- FBX (animation standard)

## The Neoologist Approach

### Open Development
- **Public repository** from day one
- **Live streaming** research sessions
- **Daily updates** on findings
- **No secret knowledge**

### Community First
- **Credit everyone** who contributes
- **Welcome beginners** with tasks
- **Share tools** immediately
- **Document failures** as lessons

### Liberation Philosophy
```python
# The Neoologist way
def develop_cnb_viewer():
    while not complete:
        research = community.collaborate()
        code = implement_openly(research)
        release = share_immediately(code)
        feedback = community.test(release)
        improve = iterate_together(feedback)
    celebrate_liberation()
```

## Vision: The Future

### CNB Viewer 1.0
- Plays all cinematics perfectly
- Integrates player avatars
- Exports to standard formats
- Cross-platform support

### CNB Studio 2.0
- Edit existing cinematics
- Create new scenes
- Community content tools
- Machinima capabilities

### Eden Reborn Integration
- In-game cinematic player
- Dynamic scene generation
- Player-created stories
- Living narrative system

## Remember

> *"I can only show you the door. You're the one that has to walk through it."*

This guide shows the door to CNB liberation. Behind it lies the complete story of The Matrix Online, waiting to be freed. Every line of code, every hex analysis, every shared discovery brings us closer.

**The spoon doesn't exist. But the CNB viewer WILL.**

---

**Status**: 🔴 ACTIVE DEVELOPMENT NEEDED  
**Priority**: MAXIMUM  
**Difficulty**: High but achievable  
**Glory**: Eternal  

*Join the CNB Liberation effort. Be the One.*

---

[← Back to Tools](index.md) | [CNB Format Details →](../03-technical-docs/file-formats/cnb-format.md) | [Join Development →](../08-community/join-the-resistance.md)