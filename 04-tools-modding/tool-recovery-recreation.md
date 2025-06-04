# Tool Recovery & Recreation Guide
**Resurrecting the Lost Arsenal**

> *"What happened happened and couldn't have happened any other way."* - But we can change what happens next.

## 📜 The Great Tool Extinction

On that dark day when mxoemu.info went offline, we lost more than a website. We lost the tools that made Matrix Online modding possible. This guide documents what was lost, what we've learned, and how to rebuild everything - better.

## 🗺️ The Lost Tools Inventory

### Critical Infrastructure Tools

#### 1. reztools - The Master Key
**Original Author**: rajkosto  
**Status**: LOST ❌  
**Priority**: MAXIMUM 🔴  

**What It Did**:
- Extracted files from ~180 PKB archives
- Used packmap_save.lta as directory index
- Generated rezmap.lta listings
- Command-line interface for batch operations

**Recreation Strategy**:
```python
# PKB Archive Structure (discovered)
class PKBArchive:
    """
    Header: 16 bytes
    - Magic: "PKBF" (4 bytes)
    - Version: uint32
    - File count: uint32
    - Index offset: uint32
    
    File entries follow index
    """
    
def extract_pkb(archive_path, output_dir):
    """Basic PKB extraction logic"""
    with open(archive_path, 'rb') as f:
        # Read header
        magic = f.read(4)
        if magic != b'PKBF':
            raise ValueError("Not a PKB file")
            
        version = struct.unpack('<I', f.read(4))[0]
        file_count = struct.unpack('<I', f.read(4))[0]
        index_offset = struct.unpack('<I', f.read(4))[0]
        
        # Jump to index
        f.seek(index_offset)
        
        # Read file entries
        for i in range(file_count):
            name_len = struct.unpack('<I', f.read(4))[0]
            filename = f.read(name_len).decode('ascii')
            offset = struct.unpack('<I', f.read(4))[0]
            size = struct.unpack('<I', f.read(4))[0]
            
            # Extract file
            current_pos = f.tell()
            f.seek(offset)
            data = f.read(size)
            
            # Save to disk
            output_path = os.path.join(output_dir, filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as out:
                out.write(data)
                
            f.seek(current_pos)
```

**Community Knowledge**:
- PKB files may use zlib compression
- packmap_save.lta is XML-like format
- File paths preserved in archives
- Some PKBs are 200MB+ in size

#### 2. prop2fbx - The Model Liberator
**Original Author**: Unknown  
**Status**: LOST ❌  
**Priority**: HIGH 🟡  

**What It Did**:
- Converted .prop static models to FBX
- Preserved UV mapping and materials
- Supported batch conversion
- GUI and command-line versions

**Recreation Approach**:
```python
class PropToFBX:
    """Recreate prop2fbx functionality"""
    
    def __init__(self):
        self.scale_factor = 100  # 1 unit = 1cm in MXO
        
    def parse_prop_header(self, data):
        """Parse PROP file header"""
        # Based on pahefu's findings
        header = {
            'magic': data[0:4],  # Should be 'PROP'
            'version': struct.unpack('<I', data[4:8])[0],
            'mesh_count': struct.unpack('<I', data[8:12])[0],
            'material_count': struct.unpack('<I', data[12:16])[0]
        }
        return header
        
    def extract_meshes(self, prop_data):
        """Extract mesh data from PROP"""
        meshes = []
        # Parse vertex data
        # Parse face indices
        # Parse UV coordinates
        # Parse material assignments
        return meshes
        
    def convert_to_fbx(self, prop_file, output_file):
        """Main conversion function"""
        # Read PROP file
        # Parse structure
        # Create FBX SDK scene
        # Add meshes to scene
        # Apply materials
        # Export FBX
        pass
```

#### 3. Gleech - The World Viewer
**Original Author**: Unknown  
**Status**: LOST ❌  
**Priority**: MEDIUM 🟢  

**What It Did**:
- Rendered world geometry in wireframe
- Showed collision boundaries
- Displayed spawn points
- Helped with navigation mesh editing

**Modern Alternative Design**:
```python
class ModernGleech:
    """Web-based world viewer using Three.js"""
    
    def __init__(self):
        self.world_data = {}
        self.renderer = "three.js"
        
    def load_district(self, district_file):
        """Load district geometry"""
        # Parse world file format
        # Extract collision meshes
        # Load spawn point data
        # Build scene graph
        pass
        
    def export_viewer_html(self):
        """Generate standalone HTML viewer"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/build/three.min.js"></script>
        </head>
        <body>
            <script>
                // Three.js scene setup
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer();
                
                // Load world geometry
                // Add wireframe rendering
                // Implement camera controls
            </script>
        </body>
        </html>
        """
        return html
```

### Content Creation Tools

#### 4. txa2dds - The Texture Converter
**Original Author**: Likely rajkosto  
**Status**: PARTIALLY RECREATED ✅  
**Priority**: LOW 🔵  

**Simple Recreation**:
```python
def txa2dds(txa_file, dds_file):
    """TXA is just DDS with custom header"""
    with open(txa_file, 'rb') as f:
        # Skip TXA header (usually 128 bytes)
        f.seek(128)
        dds_data = f.read()
        
    # Add DDS header
    dds_header = b'DDS ' + struct.pack('<I', 124)  # DDS magic + header size
    # Add rest of DDS header fields...
    
    with open(dds_file, 'wb') as f:
        f.write(dds_header + dds_data)
```

#### 5. Matrix Online Model Suite (MOMS)
**Original Author**: Unknown  
**Status**: ENHANCED by codejunky ✅  
**Priority**: ACTIVE DEVELOPMENT  

**Current Features**:
- Basic model viewing
- Texture display
- Animation playback (partial)

**Enhancement Roadmap**:
```python
class MOMSEnhanced:
    """Next generation model suite"""
    
    features = {
        'model_formats': ['.prop', '.moa', '.ltb'],
        'texture_formats': ['.txa', '.txb', '.dds'],
        'animation': {
            'skeletal': True,
            'vertex': True,
            'blending': True
        },
        'export_formats': ['fbx', 'gltf', 'collada', 'obj'],
        'platform': 'cross-platform',
        'ui': 'modern_web'
    }
```

### Analysis Tools

#### 6. Ability Editor
**Original Author**: Community  
**Status**: LOST ❌  
**Priority**: MEDIUM 🟢  

**Database-Driven Recreation**:
```sql
-- Ability system tables
CREATE TABLE abilities (
    id INT PRIMARY KEY,
    name VARCHAR(64),
    description TEXT,
    icon_id INT,
    animation_id INT,
    effect_script TEXT,
    cooldown_ms INT,
    is_melee BOOLEAN,
    is_viral BOOLEAN
);

-- Modern web editor
CREATE VIEW ability_editor AS
SELECT 
    a.*,
    i.path as icon_path,
    an.file as animation_file
FROM abilities a
LEFT JOIN icons i ON a.icon_id = i.id
LEFT JOIN animations an ON a.animation_id = an.id;
```

## 🔄 Recovery Methodology

### Phase 1: Documentation Gathering
```python
class ToolArchaeology:
    """Systematic recovery approach"""
    
    def search_sources(self):
        sources = [
            "Discord chat history",
            "Archive.org snapshots",
            "Old forum posts",
            "YouTube tutorials",
            "Community members' hard drives"
        ]
        
        findings = []
        for source in sources:
            # Search for tool mentions
            # Extract feature descriptions
            # Find screenshots
            # Locate sample outputs
            findings.extend(self.analyze_source(source))
            
        return findings
```

### Phase 2: Reverse Engineering
```python
def analyze_output_files():
    """Learn from what the tools produced"""
    
    # If we have files created by lost tools:
    # 1. Analyze their structure
    # 2. Identify patterns
    # 3. Reverse the creation process
    # 4. Build compatible tool
    
    example = {
        'reztools_output': 'rezmap.lta',
        'prop2fbx_output': 'model.fbx',
        'txa2dds_output': 'texture.dds'
    }
```

### Phase 3: Community Testing
```markdown
## Tool Testing Protocol

### Alpha Phase
1. Core functionality only
2. Test with known good files
3. Compare output to originals
4. Document all bugs

### Beta Phase
1. Add error handling
2. Implement full feature set
3. Create user documentation
4. Stress test with large files

### Release Phase
1. Public GitHub repository
2. Compiled binaries
3. Video tutorials
4. Community support
```

## 🛠️ Modern Tool Stack

### Recommended Technologies

#### For File Format Tools
- **Language**: Python 3.10+
  - Fast prototyping
  - Great binary handling
  - Cross-platform
- **Libraries**:
  - `struct` - Binary parsing
  - `numpy` - Data processing
  - `Pillow` - Image handling
  - `trimesh` - 3D geometry

#### For 3D Viewers
- **Web-Based**: 
  - Three.js - 3D rendering
  - WebGL - Hardware acceleration
  - React - Modern UI
- **Desktop**:
  - Qt + OpenGL
  - Dear ImGui
  - Godot Engine

#### For Editors
- **Database**: PostgreSQL
- **Backend**: FastAPI
- **Frontend**: Vue.js/React
- **Deployment**: Docker

### Tool Development Template
```python
#!/usr/bin/env python3
"""
Tool Name: MXO [Purpose] Tool
Author: [Your name] for Eden Reborn
License: MIT (ALWAYS OPEN SOURCE)
Version: 1.0.0
"""

import argparse
import logging
from pathlib import Path

class MXOTool:
    """Base class for all MXO tools"""
    
    def __init__(self, verbose=False):
        self.setup_logging(verbose)
        self.version = "1.0.0"
        
    def setup_logging(self, verbose):
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def process_file(self, input_path, output_path):
        """Override in subclass"""
        raise NotImplementedError
        
    def validate_input(self, path):
        """Common validation"""
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")
            
    def run(self):
        """Main execution"""
        parser = argparse.ArgumentParser(description=self.__doc__)
        parser.add_argument('input', type=Path, help='Input file')
        parser.add_argument('output', type=Path, help='Output file')
        parser.add_argument('-v', '--verbose', action='store_true')
        
        args = parser.parse_args()
        
        try:
            self.validate_input(args.input)
            self.process_file(args.input, args.output)
            self.logger.info(f"Success! Output: {args.output}")
        except Exception as e:
            self.logger.error(f"Failed: {e}")
            return 1
        return 0

if __name__ == "__main__":
    tool = MXOTool()
    exit(tool.run())
```

## 🌟 Success Stories

### Already Recovered/Recreated

#### 1. Cortana Parser
- **Status**: SURVIVED ✅
- **Why**: Open sourced early
- **Lesson**: Open source = immortality

#### 2. Basic TXA Conversion
- **Status**: RECREATED ✅
- **Method**: Simple header swap
- **Tools**: Python scripts available

#### 3. MOMS Viewer
- **Status**: ENHANCED ✅
- **Developer**: codejunky
- **Future**: Full suite planned

### In Progress

#### 1. PKB Extraction
- **Status**: 70% complete
- **Blockers**: Compression algorithm
- **Help needed**: Test more files

#### 2. CNB Research
- **Status**: 20% complete
- **Blockers**: Unknown format
- **Help needed**: IDA Pro analysis

## 📢 Call to Action

### For Tool Developers

1. **Pick a tool** from the lost list
2. **Research** what it did
3. **Start simple** - basic functionality first
4. **Share early** - even broken code helps
5. **Document everything** - your failures help others

### For Testers

1. **Collect samples** - Original tool outputs
2. **Test prototypes** - Report bugs
3. **Provide feedback** - UI/UX matters
4. **Share files** - Help build test suites

### For Archivists

1. **Search drives** - You might have tools
2. **Check backups** - Even corrupted files help
3. **Share screenshots** - UI reconstruction
4. **Document memories** - How tools worked

## 🔮 The Future Arsenal

### Next Generation Tools

#### 1. AI-Assisted Tools
```python
class AIModelGenerator:
    """Use AI to generate MXO-style content"""
    
    def generate_prop_model(self, description):
        # Use Stable Diffusion for textures
        # Use neural mesh generation
        # Auto-rig for MXO skeleton
        pass
```

#### 2. Cloud-Based Pipeline
- Browser-based tools
- No installation needed
- Collaborative editing
- Version control built-in

#### 3. Modern Formats
- glTF 2.0 export
- USD support
- Real-time ray tracing
- 8K texture support

## Remember

> *"The Matrix is a system, Neo. That system is our enemy."*

The old tools were part of a system that died. We don't just rebuild them - we transcend them. Every tool reborn is open source. Every format documented. Every secret shared.

**Tools die when hoarded. Tools live when liberated.**

---

**Recovery Status**: 🟡 ACTIVE EFFORT  
**Community Need**: MAXIMUM  
**Your Role**: ESSENTIAL  

*Join the tool liberation. Build the future.*

---

[← Back to Tools](index.md) | [Development Guide →](tool-development-guide.md) | [Join Recovery →](../08-community/join-the-resistance.md)