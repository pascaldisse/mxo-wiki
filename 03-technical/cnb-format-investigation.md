# CNB Format Investigation and Viewer Development Guide
**The Holy Grail of Matrix Online Preservation: Real-Time Cinematic Bundles**

> *"I can only show you the door. You're the one that has to walk through it."* - Morpheus (This guide shows you the door to CNB format liberation.)

## 🎬 **The CNB Crisis: Our #1 Priority**

CNB (Cinematic Bundle) files contain the **most important content** in The Matrix Online - the complete story told through real-time 3D cinematics. **NO VIEWER EXISTS** for these files, making story preservation our highest priority challenge.

### 💀 **What We're Losing**
```yaml
lost_content:
  story_missions: "Complete Matrix Online storyline"
  character_development: "All major plot developments"
  faction_storylines: "Zion, Machine, Merovingian narratives"
  player_integration: "Your avatar appearing in cutscenes"
  original_vision: "How the story was meant to be experienced"
  
  files_at_risk:
    location: "resource/cinematics/"
    file_count: 12
    naming_pattern: "cin1_1.cnb through cin4_3.cnb"
    structure: "4 acts, ~3 scenes each"
    size_range: "Large files containing complete 3D scenes"
```

## 🔍 **CNB Format Analysis**

### File Structure Discovery
```yaml
cnb_file_locations:
  base_directory: "resource/cinematics/"
  discovered_files:
    act_1:
      - "cin1_1.cnb"  # Act 1, Scene 1
      - "cin1_2.cnb"  # Act 1, Scene 2  
      - "cin1_3.cnb"  # Act 1, Scene 3
    act_2:
      - "cin2_1.cnb"  # Act 2, Scene 1
      - "cin2_2.cnb"  # Act 2, Scene 2
      - "cin2_3.cnb"  # Act 2, Scene 3
    act_3:
      - "cin3_1.cnb"  # Act 3, Scene 1
      - "cin3_2.cnb"  # Act 3, Scene 2
      - "cin3_3.cnb"  # Act 3, Scene 3
    act_4:
      - "cin4_1.cnb"  # Act 4, Scene 1
      - "cin4_2.cnb"  # Act 4, Scene 2
      - "cin4_3.cnb"  # Act 4, Scene 3
```

### CNB vs Bink Comparison
```yaml
format_comparison:
  cnb_files:
    type: "Real-time 3D cinematics"
    engine_integration: "Native Lithtech engine"
    player_avatar: "Your character appears in scenes"
    interactivity: "Dynamic, context-aware"
    quality: "Full game resolution"
    uniqueness: "Every playthrough different"
    
  bink_files:
    type: "Pre-rendered video (.bik)"
    engine_integration: "Video player overlay"
    player_avatar: "Generic characters only"
    interactivity: "Static playback"
    quality: "Compressed video"
    uniqueness: "Identical every time"
```

## 🛠️ **CNB Investigation Strategy**

### Phase 1: File Format Analysis
```python
#!/usr/bin/env python3
"""
CNB Format Investigation Tool
First step: Understanding the file structure
"""

import struct
import os
from pathlib import Path

class CNBInvestigator:
    def __init__(self, cnb_file_path):
        self.cnb_path = Path(cnb_file_path)
        self.header_data = None
        self.sections = []
        
    def analyze_cnb_header(self):
        """Analyze CNB file header structure"""
        
        with open(self.cnb_path, 'rb') as f:
            # Read first 1024 bytes for analysis
            header_data = f.read(1024)
            
            # Look for magic signatures
            magic_candidates = []
            for i in range(0, 100, 4):
                magic = header_data[i:i+4]
                if all(32 <= b <= 126 for b in magic):  # Printable ASCII
                    magic_candidates.append((i, magic.decode('ascii')))
                    
            print(f"Magic signature candidates in {self.cnb_path.name}:")
            for offset, magic in magic_candidates:
                print(f"  Offset {offset:04X}: '{magic}'")
                
            # Look for common patterns
            self.find_common_patterns(header_data)
            
    def find_common_patterns(self, data):
        """Look for patterns that might indicate structure"""
        
        # Look for section markers
        patterns_to_find = [
            b'CNB\x00',      # CNB null-terminated
            b'CINEMATIC',    # Cinematic marker
            b'SCENE',        # Scene marker
            b'ANIM',         # Animation marker
            b'CAMERA',       # Camera data
            b'AUDIO',        # Audio data
            b'MODEL',        # Model references
            b'PROP',         # Prop references
            b'\xFF\xFF\xFF\xFF',  # Common section terminator
        ]
        
        print(f"\nPattern search results:")
        for pattern in patterns_to_find:
            offset = data.find(pattern)
            if offset != -1:
                print(f"  Found '{pattern}' at offset {offset:04X}")
                
    def extract_metadata(self):
        """Extract basic metadata from CNB file"""
        
        file_size = os.path.getsize(self.cnb_path)
        
        with open(self.cnb_path, 'rb') as f:
            # Read potential header
            potential_header = f.read(64)
            
            # Try to parse as various structures
            metadata = {
                'file_size': file_size,
                'header_hex': potential_header.hex()[:128],  # First 64 bytes as hex
                'potential_version': None,
                'potential_section_count': None
            }
            
            # Look for version numbers (common at offsets 4, 8, 12)
            for offset in [4, 8, 12, 16]:
                if offset + 4 <= len(potential_header):
                    value = struct.unpack('<I', potential_header[offset:offset+4])[0]
                    if 1 <= value <= 100:  # Reasonable version range
                        metadata[f'version_candidate_{offset}'] = value
                        
            return metadata

def investigate_all_cnb_files(cinematics_directory):
    """Investigate all CNB files in the cinematics directory"""
    
    cnb_files = list(Path(cinematics_directory).glob("cin*.cnb"))
    
    if not cnb_files:
        print(f"No CNB files found in {cinematics_directory}")
        print("Make sure you've extracted files from PKB archives first")
        return
        
    print(f"Found {len(cnb_files)} CNB files to investigate:")
    
    results = {}
    for cnb_file in sorted(cnb_files):
        print(f"\n{'='*60}")
        print(f"Investigating: {cnb_file.name}")
        print(f"{'='*60}")
        
        investigator = CNBInvestigator(cnb_file)
        investigator.analyze_cnb_header()
        
        metadata = investigator.extract_metadata()
        results[cnb_file.name] = metadata
        
        print(f"\nFile metadata:")
        print(f"  Size: {metadata['file_size']:,} bytes")
        print(f"  Header (hex): {metadata['header_hex']}")
        
    return results

# Usage example
if __name__ == "__main__":
    # Run this on extracted cinematics directory
    cinematics_path = "extracted_files/resource/cinematics/"
    results = investigate_all_cnb_files(cinematics_path)
    
    # Save results for analysis
    import json
    with open("cnb_investigation_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"\nInvestigation complete. Results saved to cnb_investigation_results.json")
```

### Phase 2: Binary Structure Mapping
```python
#!/usr/bin/env python3
"""
CNB Binary Structure Mapper
Phase 2: Understanding data organization
"""

import struct
import numpy as np
from pathlib import Path

class CNBStructureMapper:
    def __init__(self, cnb_file_path):
        self.cnb_path = Path(cnb_file_path)
        self.data = self.load_file_data()
        self.sections = []
        
    def load_file_data(self):
        """Load entire CNB file into memory for analysis"""
        with open(self.cnb_path, 'rb') as f:
            return f.read()
            
    def find_section_boundaries(self):
        """Attempt to identify section boundaries in the file"""
        
        # Common section markers in game files
        section_markers = [
            b'\xFF\xFF\xFF\xFF',  # -1 as uint32
            b'\x00\x00\x00\x00',  # 0 as uint32
            b'DATA',
            b'HEAD',
            b'BODY',
            b'FOOT',
        ]
        
        boundaries = []
        for marker in section_markers:
            offset = 0
            while True:
                pos = self.data.find(marker, offset)
                if pos == -1:
                    break
                boundaries.append((pos, marker))
                offset = pos + 1
                
        # Sort by position
        boundaries.sort(key=lambda x: x[0])
        
        print(f"Potential section boundaries in {self.cnb_path.name}:")
        for pos, marker in boundaries[:20]:  # Show first 20
            print(f"  {pos:08X}: {marker}")
            
        return boundaries
        
    def analyze_data_patterns(self):
        """Look for patterns that might indicate data types"""
        
        # Check for floating point patterns (coordinates, transforms)
        float_candidates = []
        for i in range(0, min(len(self.data) - 4, 10000), 4):
            try:
                value = struct.unpack('<f', self.data[i:i+4])[0]
                # Look for reasonable coordinate ranges
                if -1000.0 <= value <= 1000.0 and abs(value) > 0.001:
                    float_candidates.append((i, value))
            except:
                continue
                
        print(f"Potential floating point coordinates (first 10):")
        for offset, value in float_candidates[:10]:
            print(f"  {offset:08X}: {value:.6f}")
            
        # Look for string references
        string_candidates = []
        for i in range(len(self.data) - 10):
            if self.data[i] != 0:  # Not null
                continue
            # Check if followed by printable ASCII
            try:
                string_data = self.data[i+1:i+50]
                null_pos = string_data.find(0)
                if null_pos > 3:  # At least 4 character string
                    string = string_data[:null_pos].decode('ascii')
                    if string.isprintable() and len(string) > 3:
                        string_candidates.append((i+1, string))
            except:
                continue
                
        print(f"Potential embedded strings (first 10):")
        for offset, string in string_candidates[:10]:
            print(f"  {offset:08X}: '{string}'")
            
    def create_hexdump_sections(self, section_size=256):
        """Create hexdump-style output for manual analysis"""
        
        output_file = f"{self.cnb_path.stem}_hexdump.txt"
        
        with open(output_file, 'w') as f:
            f.write(f"CNB File Hexdump: {self.cnb_path.name}\n")
            f.write(f"File Size: {len(self.data):,} bytes\n")
            f.write("="*80 + "\n\n")
            
            for offset in range(0, len(self.data), section_size):
                section_data = self.data[offset:offset+section_size]
                
                f.write(f"Offset {offset:08X}:\n")
                
                # Hex representation
                for i in range(0, len(section_data), 16):
                    line_data = section_data[i:i+16]
                    hex_str = ' '.join(f'{b:02X}' for b in line_data)
                    ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in line_data)
                    f.write(f"{offset+i:08X}: {hex_str:<48} |{ascii_str}|\n")
                    
                f.write("\n")
                
        print(f"Hexdump saved to: {output_file}")

# Usage for specific analysis
def deep_cnb_analysis(cnb_file_path):
    """Perform comprehensive analysis of a single CNB file"""
    
    mapper = CNBStructureMapper(cnb_file_path)
    
    print(f"Deep analysis of: {cnb_file_path}")
    print("="*60)
    
    # Find section boundaries
    boundaries = mapper.find_section_boundaries()
    
    # Analyze data patterns
    mapper.analyze_data_patterns()
    
    # Create hexdump for manual inspection
    mapper.create_hexdump_sections()
    
    return mapper

if __name__ == "__main__":
    # Analyze a specific CNB file
    cnb_file = "extracted_files/resource/cinematics/cin1_1.cnb"
    
    if Path(cnb_file).exists():
        analysis = deep_cnb_analysis(cnb_file)
        print("\nAnalysis complete. Check generated hexdump file for detailed inspection.")
    else:
        print(f"CNB file not found: {cnb_file}")
        print("Extract files from PKB archives first using appropriate tools.")
```

## 🎯 **CNB Viewer Development Roadmap**

### Stage 1: Format Understanding (CRITICAL)
```yaml
investigation_priority:
  header_analysis:
    priority: "CRITICAL"
    goal: "Identify magic bytes, version, section count"
    approach: "Hex analysis + pattern recognition"
    
  section_mapping:
    priority: "CRITICAL"  
    goal: "Map file structure (header, data blocks, footer)"
    approach: "Boundary detection + size calculation"
    
  data_type_identification:
    priority: "HIGH"
    goal: "Identify models, textures, animations, camera data"
    approach: "Pattern analysis + known format comparison"
```

### Stage 2: Data Extraction (HIGH PRIORITY)
```cpp
// CNB Data Extractor (C++ implementation)
class CNBExtractor {
private:
    std::vector<uint8_t> fileData;
    CNBHeader header;
    std::vector<CNBSection> sections;
    
public:
    bool loadCNBFile(const std::string& filePath);
    bool parseHeader();
    bool extractSections();
    
    // Extract specific data types
    std::vector<Model3D> extractModels();
    std::vector<Camera> extractCameraData();
    std::vector<Animation> extractAnimations();
    std::vector<Audio> extractAudioReferences();
    std::vector<Texture> extractTextureReferences();
    
    // Export to intermediate formats
    bool exportToJSON(const std::string& outputPath);
    bool exportModelsToOBJ(const std::string& outputDir);
    bool exportCameraToFBX(const std::string& outputPath);
};

// CNB format structures (to be determined through analysis)
struct CNBHeader {
    char magic[4];          // CNB format identifier
    uint32_t version;       // Format version
    uint32_t sectionCount;  // Number of sections
    uint32_t totalSize;     // Total file size
    uint32_t flags;         // Format flags
    // Additional fields TBD
};

struct CNBSection {
    uint32_t type;          // Section type identifier
    uint32_t offset;        // Offset to section data
    uint32_t size;          // Section size in bytes
    uint32_t flags;         // Section flags
    // Additional fields TBD
};
```

### Stage 3: Viewer Implementation (MEDIUM PRIORITY)
```python
#!/usr/bin/env python3
"""
CNB Viewer - Real-time 3D Cinematic Player
Stage 3: Implementing the actual viewer
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class CNBViewer:
    def __init__(self, cnb_file_path):
        self.cnb_file = cnb_file_path
        self.extracted_data = None
        self.current_frame = 0
        self.playing = False
        
        # Initialize OpenGL context
        pygame.init()
        pygame.display.set_mode((1024, 768), pygame.OPENGL | pygame.DOUBLEBUF)
        
    def load_cnb_data(self):
        """Load and parse CNB file data"""
        
        extractor = CNBExtractor(self.cnb_file)
        self.extracted_data = {
            'models': extractor.extract_models(),
            'cameras': extractor.extract_camera_data(),
            'animations': extractor.extract_animations(),
            'audio': extractor.extract_audio_references(),
            'textures': extractor.extract_texture_references()
        }
        
    def setup_opengl(self):
        """Configure OpenGL for 3D rendering"""
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        # Set up lighting
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        
        # Set up material
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        
    def render_frame(self, frame_number):
        """Render a specific frame of the cinematic"""
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set camera position for this frame
        camera = self.get_camera_for_frame(frame_number)
        gluLookAt(
            camera['position'][0], camera['position'][1], camera['position'][2],
            camera['target'][0], camera['target'][1], camera['target'][2],
            camera['up'][0], camera['up'][1], camera['up'][2]
        )
        
        # Render all models for this frame
        for model in self.extracted_data['models']:
            self.render_model(model, frame_number)
            
        pygame.display.flip()
        
    def render_model(self, model, frame_number):
        """Render a single 3D model with animation"""
        
        # Apply animation transforms for this frame
        transform = self.get_model_transform(model, frame_number)
        
        glPushMatrix()
        glMultMatrixf(transform)
        
        # Render model geometry
        glBegin(GL_TRIANGLES)
        for face in model['faces']:
            for vertex_index in face:
                vertex = model['vertices'][vertex_index]
                normal = model['normals'][vertex_index]
                
                glNormal3f(normal[0], normal[1], normal[2])
                glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()
        
        glPopMatrix()
        
    def play_cinematic(self):
        """Main playback loop"""
        
        clock = pygame.time.Clock()
        self.playing = True
        
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.toggle_playback()
                    elif event.key == pygame.K_RIGHT:
                        self.current_frame += 1
                    elif event.key == pygame.K_LEFT:
                        self.current_frame = max(0, self.current_frame - 1)
                        
            if self.playing:
                self.render_frame(self.current_frame)
                self.current_frame += 1
                
                # Check for end of cinematic
                if self.current_frame >= self.get_total_frames():
                    self.playing = False
                    
            clock.tick(30)  # 30 FPS
            
    def export_video(self, output_path):
        """Export cinematic as standard video file"""
        
        # This would render all frames and encode to MP4
        # Preserving the cinematic for posterity
        pass

# Usage example
if __name__ == "__main__":
    viewer = CNBViewer("extracted_files/resource/cinematics/cin1_1.cnb")
    viewer.load_cnb_data()
    viewer.setup_opengl()
    viewer.play_cinematic()
```

## 🤝 **Community Development Strategy**

### Skill Requirements
```yaml
developer_skills_needed:
  essential:
    - "Binary file format analysis"
    - "Hex editor proficiency"
    - "Pattern recognition skills"
    - "C++ or Python programming"
    
  helpful:
    - "3D graphics programming (OpenGL/DirectX)"
    - "Game engine knowledge (Lithtech familiarity)"
    - "Animation system understanding"
    - "Video codec experience"
    
  tools_required:
    - "Hex editor (HxD, 010 Editor)"
    - "Development environment (Visual Studio, Qt)"
    - "3D graphics libraries (OpenGL, DirectX)"
    - "Sample CNB files (extracted from PKB)"
```

### Collaboration Framework
```bash
# GitHub repository structure for CNB development
cnb-viewer-project/
├── investigation/
│   ├── format_analysis/
│   ├── sample_files/
│   └── research_notes/
├── extraction/
│   ├── cnb_parser/
│   ├── data_structures/
│   └── export_tools/
├── viewer/
│   ├── rendering_engine/
│   ├── animation_system/
│   └── user_interface/
├── tests/
│   ├── sample_cinematics/
│   ├── unit_tests/
│   └── integration_tests/
└── documentation/
    ├── format_specification/
    ├── api_documentation/
    └── user_guides/
```

### Development Phases
```yaml
phase_1_investigation:
  duration: "2-4 weeks"
  team_size: "2-3 researchers"
  deliverable: "Complete CNB format specification"
  blockers: "Need PKB extraction tools first"
  
phase_2_extraction:
  duration: "4-6 weeks"  
  team_size: "3-4 developers"
  deliverable: "Working CNB data extractor"
  depends_on: "Phase 1 completion"
  
phase_3_viewer:
  duration: "6-8 weeks"
  team_size: "4-6 developers"
  deliverable: "Functional CNB viewer application"
  depends_on: "Phase 2 completion"
  
phase_4_polish:
  duration: "2-4 weeks"
  team_size: "2-3 developers"
  deliverable: "User-friendly viewer with export"
  depends_on: "Phase 3 completion"
```

## 🚨 **Critical Dependencies**

### Prerequisite: PKB Extraction
```yaml
cnb_access_problem:
  issue: "CNB files are stored inside PKB archives"
  blocker: "reztools (PKB extractor) is lost"
  priority: "CRITICAL - Must be solved first"
  alternatives:
    - "Recreate PKB extraction tools"
    - "Find existing PKB extraction capability"
    - "Reverse engineer PKB format"
    
  impact: "Cannot access CNB files without PKB extraction"
  community_focus: "PKB tools must be priority #1"
```

### Sample Files Required
```bash
# We need access to these files for development:
resource/cinematics/cin1_1.cnb  # Act 1, Scene 1 (Tutorial/Introduction)
resource/cinematics/cin1_2.cnb  # Act 1, Scene 2
resource/cinematics/cin1_3.cnb  # Act 1, Scene 3
# ... all 12 cinematic files

# File acquisition strategy:
1. Extract from original Matrix Online installation
2. Extract from PKB archives (requires tools)
3. Community file sharing (legal gray area)
4. Clean room implementation from scratch
```

## 📊 **Progress Tracking**

### CNB Research Checklist
- [ ] **PKB Extraction Solved** (Prerequisite)
- [ ] **CNB Files Acquired** (Sample set for development)
- [ ] **File Format Analysis** (Header structure documented)
- [ ] **Section Mapping** (Data organization understood)
- [ ] **Model Extraction** (3D geometry accessible)
- [ ] **Animation Extraction** (Character movement data)
- [ ] **Camera Extraction** (Cinematic camera paths)
- [ ] **Audio Integration** (Soundtrack and dialogue)
- [ ] **Rendering Engine** (OpenGL/DirectX implementation)
- [ ] **User Interface** (Playback controls)
- [ ] **Export Functionality** (Save as standard video)
- [ ] **Community Release** (Public viewer available)

### Success Metrics
```yaml
development_milestones:
  proof_of_concept:
    goal: "Display single frame from CNB file"
    impact: "Proves format can be decoded"
    
  basic_playback:
    goal: "Play cinematic with basic rendering"
    impact: "Demonstrates technical feasibility"
    
  full_viewer:
    goal: "Complete viewer with all features"
    impact: "Enables story preservation"
    
  community_adoption:
    goal: "100+ downloads of viewer"
    impact: "Mission accomplished - story preserved"
```

## 🎯 **Call to Action**

### For Technical Contributors
```bash
# If you can help with CNB development:
1. Join the Matrix Online Discord
2. Focus on PKB extraction first (enables CNB access)
3. Share any CNB format discoveries
4. Coordinate with community researchers

# Priority contributions needed:
- Binary analysis experts
- Game file format researchers  
- 3D graphics programmers
- Video codec developers
```

### For Community Members
```bash
# If you have Matrix Online files:
1. Share original game installations
2. Help extract and distribute CNB files
3. Test viewer builds when available
4. Document story content for preservation

# Every CNB file shared helps the effort
```

### For Story Preservationists
```bash
# If you care about Matrix Online's story:
1. Advocate for CNB viewer development
2. Document existing story knowledge
3. Record what you remember from cinematics
4. Support development financially if possible

# The complete Matrix story depends on CNB access
```

## 🌟 **The Vision: What Success Looks Like**

### Short-term Success (6 months)
- CNB format fully documented and understood
- Basic viewer can display cinematics frame-by-frame
- Community has access to all 12 story cinematics
- Technical foundation established for enhancement

### Long-term Vision (1-2 years)
- Professional-quality CNB viewer with full features
- Export capability to preserve cinematics as video
- Enhanced viewer with modern graphics improvements
- Integration with Matrix Online emulators for in-game playback

### Ultimate Goal
```yaml
story_preservation_achieved:
  complete_matrix_story: "All 12 cinematics preserved and viewable"
  player_avatar_support: "Your character in cutscenes working"
  modern_compatibility: "Runs on current operating systems"  
  community_access: "Free and open source forever"
  
  impact:
    cultural: "Matrix Online story preserved for future generations"
    technical: "Advanced game preservation techniques demonstrated"
    community: "Proof that collaborative development works"
    educational: "Complete documentation for learning purposes"
```

## Remember

> *"The One is just another system of control."* - Agent Smith (But CNB liberation breaks all control systems.)

The CNB format represents the most important undocumented content in Matrix Online. Every hour spent on CNB investigation is an hour spent preserving irreplaceable digital culture.

**The story of The Matrix Online must not be lost.**

This investigation guide provides the roadmap. The community provides the effort. Together, we will crack the CNB format and liberate the complete Matrix Online story.

---

**CNB Status**: 🔴 FORMAT UNKNOWN - URGENT RESEARCH NEEDED  
**Story Preservation**: 🔴 AT RISK - TIME SENSITIVE  
**Community Priority**: 🚨 #1 MOST CRITICAL PROJECT  

*The truth is out there. In CNB files. Let's find it.*

---

[← Back to Technical](index.md) | [PKB Investigation →](pkb-archive-investigation.md) | [Tool Development →](../04-tools-modding/tool-development-guide.md)