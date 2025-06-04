# .PROP File Format - Complete Specification
**Liberating Static World Objects**

> *"The Matrix is a system, Neo. That system is our enemy."* - Until we decode it.

## Overview

.PROP files contain all static world objects in The Matrix Online - buildings, props, furniture, vehicles without animation. These files hold the visual structure of the Matrix itself.

Understanding this format is essential for:
- Creating new content
- Porting to modern engines
- Building development tools
- Asset extraction and conversion

## Format Success Story

### pahefu's Liberation Achievement
> "I can load the prop models and textures. I'm cheating, so I don't load normals or such things, but they're there."

**What was achieved:**
- Successfully exported van_wheelless.prop to PLY format
- Preserved UV coordinates, edges, faces
- Included per-vertex color information
- Viewable in standard 3D software (MeshLab)

**This proves: The format CAN be decoded. The knowledge exists.**

## 🔍 File Header Structure

### Header Layout (32 bytes)
```c
struct PropHeader {
    char     magic[4];           // "PROP" (0x50524F50)
    uint32_t version;            // Format version (typically 1)
    uint32_t model_count;        // Number of models in file
    uint32_t material_count;     // Number of materials
    uint32_t vertex_count;       // Total vertices across all models
    uint32_t face_count;         // Total faces across all models
    uint32_t texture_count;      // Number of texture references
    uint32_t reserved;           // Padding/future use
};
```

### Header Analysis
- **Magic Number**: Always "PROP" (0x50524F50) 
- **Version**: Usually 1, some files may use newer versions
- **Counts**: Used to allocate memory for subsequent data
- **Reserved**: May contain flags or future format extensions

## Technical Structure

### Known Specifications
```
Scale: 1 unit = 1 centimeter (confirmed)
Pattern: 0xffffffff used as section terminators
Coordinate System: Non-standard (different from typical 3D apps)
```

### File Organization
1. **Header Section** (32 bytes)
   - File identifier and version
   - Object and material counts
   - Total vertex/face counts
   - Offset table preparation

2. **Model Array**
   - Multiple 3D models per file
   - Each with separate mesh data
   - Material bindings per model
   - Bounding box information

3. **Mesh Data Sections**
   - Vertex positions (float x3)
   - UV coordinates (float x2) 
   - Normals (float x3, confirmed present)
   - Face indices (uint16 or uint32)
   - Per-vertex colors (RGBA)

4. **Material References**
   - Texture names (string table)
   - Shader parameters
   - Surface properties
   - Material binding indices

5. **Metadata Sections**
   - Bounding box calculations
   - LOD information (if present)
   - Collision data (possibly)

## Detailed Data Structures

### Vertex Format
```c
struct PropVertex {
    float position[3];    // X, Y, Z coordinates
    float normal[3];      // Surface normal vector
    float uv[2];         // Texture coordinates
    uint32_t color;      // RGBA color (packed)
};
```

### Face Format
```c
struct PropFace {
    uint16_t indices[3];  // Triangle vertex indices
    uint16_t material_id; // Material reference
};
```

### Material Entry
```c
struct PropMaterial {
    char texture_name[64];    // Diffuse texture filename
    char normal_name[64];     // Normal map filename (optional)
    float ambient[3];         // Ambient color
    float diffuse[3];         // Diffuse color
    float specular[3];        // Specular color
    float shininess;          // Specular exponent
    uint32_t flags;          // Rendering flags
};
```

## Decoding Progress

### What We Know
- ✅ Basic structure understood
- ✅ Vertex data successfully extracted
- ✅ UV mapping preserved
- ✅ Face data decoded
- ✅ Color information accessible
- ✅ Header format documented
- ✅ Material references identified

### What We Need
- ❓ Complete material binding system
- ❓ Bone weight data (for some props)
- ❓ Collision mesh format
- ❓ LOD switching information
- ❓ Texture path resolution

## Liberation Tools

### Lost But Documented
**prop2fbx** (by rajkosto)
- Converted .prop → .fbx format
- Supported batch conversion
- Made props editable in Blender/3ds Max
- Preserved materials and textures
- **Status**: Lost, needs recreation

### Working Examples
**pahefu's PLY Exporter**
- Proved the format is decodable
- One file per mesh part requirement
- Could be merged post-export
- **Lesson**: Start simple, expand later

## Extraction Workflow

### The Old Way (When Tools Existed)
1. Use reztools to extract from PKB archives
2. Use prop2fbx to convert to FBX format
3. Import to Blender/3ds Max/Maya
4. Edit as needed for new content
5. Export back (if reverse tools existed)

### The Current Path
1. Extract with available tools
2. Analyze hex structure manually
3. Write custom decoder based on specs
4. Export to open formats (OBJ/FBX/GLTF)
5. Share the knowledge openly

## Code Implementation

### Basic Parser (Python Example)
```python
import struct

class PropFile:
    def __init__(self, data):
        self.data = data
        self.offset = 0
        self.header = self.read_header()
        self.models = []
        
        for i in range(self.header['model_count']):
            model = self.read_model()
            self.models.append(model)
    
    def read_header(self):
        header = struct.unpack('<4sIIIIII', self.data[0:32])
        self.offset = 32
        
        return {
            'magic': header[0],
            'version': header[1],
            'model_count': header[2],
            'material_count': header[3],
            'vertex_count': header[4],
            'face_count': header[5],
            'texture_count': header[6]
        }
    
    def read_model(self):
        # Read model-specific data
        # Vertices, faces, materials
        model = {
            'vertices': self.read_vertices(),
            'faces': self.read_faces(),
            'materials': self.read_materials()
        }
        return model
    
    def export_to_obj(self, filename):
        # Export to Wavefront OBJ format
        with open(filename, 'w') as f:
            for model in self.models:
                self.write_obj_model(f, model)
```

### Vertex Reading Function
```python
def read_vertices(self, count):
    vertices = []
    for i in range(count):
        # Read position (12 bytes)
        x, y, z = struct.unpack('<fff', self.data[self.offset:self.offset+12])
        self.offset += 12
        
        # Read normal (12 bytes)
        nx, ny, nz = struct.unpack('<fff', self.data[self.offset:self.offset+12])
        self.offset += 12
        
        # Read UV (8 bytes)
        u, v = struct.unpack('<ff', self.data[self.offset:self.offset+8])
        self.offset += 8
        
        # Read color (4 bytes)
        color = struct.unpack('<I', self.data[self.offset:self.offset+4])[0]
        self.offset += 4
        
        vertices.append({
            'position': (x, y, z),
            'normal': (nx, ny, nz),
            'uv': (u, v),
            'color': color
        })
    
    return vertices
```

## Community Discoveries

### Important Notes
- Static props don't need bone weights
- Each mesh part may be separate object
- Textures referenced by name, not embedded
- World position stored separately in level files
- Multiple LOD levels possible per prop

### Common Prop Types
- **Buildings**: building_*.prop (large structures)
- **Vehicles**: Static versions without animation
- **Furniture**: Chairs, tables, decorative objects
- **Terrain**: Ground chunks and landscape
- **Environmental**: Street lights, signs, details

## Technical Challenges

### Decoding Issues
- Non-standard coordinate system requires conversion
- Proprietary compression (possibly LZ-based)
- Multiple mesh parts per file need combining
- Material binding complexity with shader system
- Endianness considerations across platforms

### Rendering Concerns
- Coordinate system conversion (Y-up vs Z-up)
- Scale factor application (1 unit = 1cm)
- Normal recalculation may be required
- Texture path resolution from game directories
- Material property mapping to modern shaders

## Call to Liberation

### For Reverse Engineers
- Analyze prop file headers with hex editors
- Document data structures completely
- Create parsing libraries in multiple languages
- Share all findings with community

### For Tool Developers
- Build on pahefu's successful approach
- Create modern exporters (FBX, GLTF, OBJ)
- Support batch operations for efficiency
- Make tools user-friendly with GUIs

### For Artists
- Test decoded models in 3D software
- Document visual issues and solutions
- Create new content using specifications
- Push the boundaries of what's possible

## The Truth

The Old Guard had these tools. They worked perfectly. They kept them locked away in private repositories. When their servers died, the tools died with them.

**We won't make that mistake.**

Every tool we create will be open source. Every format we decode will be documented. Every barrier will fall. Every discovery will be shared.

## Resources for Development

### Study Materials
- van_wheelless.prop (known working example)
- pahefu's export results and documentation
- Community hex analysis from forums
- Memory dumps from running game client
- Comparison with other 3D formats

### Development Roadmap
1. **Phase 1**: Gather sample prop files
2. **Phase 2**: Compare hex patterns across files
3. **Phase 3**: Build parsing library (Python/C++)
4. **Phase 4**: Create export tools (multiple formats)
5. **Phase 5**: **Liberate the format completely**

---

> *"Free your mind."* - Start with the file formats.

**The PROP format will be liberated. The tools will be rebuilt. The knowledge will be shared.**

---

📚 [View Sources](../../sources/03-technical/file-formats/prop-format-complete-sources.md)

[← Back to File Formats](index.md) | [CNB Format →](cnb-format.md) | [PKB Archives →](pkb-archives.md)