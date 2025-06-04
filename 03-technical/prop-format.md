# .PROP File Format
**Liberating Static World Objects**

> *"The Matrix is a system, Neo. That system is our enemy."* - Until we decode it.

## Overview

.PROP files contain all static world objects in The Matrix Online - buildings, props, furniture, vehicles without animation. These files hold the visual structure of the Matrix itself.

## Format Success Story

### pahefu's Liberation
> "I can load the prop models and textures. I'm cheating, so I don't load normals or such things, but they're there."

**What was achieved:**
- Successfully exported van_wheelless.prop to PLY format
- Preserved UV coordinates, edges, faces
- Included per-vertex color information
- Viewable in standard 3D software (MeshLab)

**This proves: The format CAN be decoded. The knowledge exists.**

## Technical Structure

### Known Specifications
```
Scale: 1 unit = 1 centimeter (confirmed)
Pattern: 0xffffffff used as section terminators
Coordinate System: Non-standard (different from typical 3D apps)
```

### File Organization
1. **Header Section**
   - File identifier
   - Version information
   - Object count
   - Offset table

2. **Mesh Data**
   - Vertex positions
   - UV coordinates
   - Normals (confirmed present)
   - Face indices
   - Per-vertex colors

3. **Material References**
   - Texture names
   - Shader parameters
   - Surface properties

4. **Metadata**
   - Bounding box
   - LOD information
   - Collision data (possibly)

## Decoding Progress

### What We Know
- ✅ Basic structure understood
- ✅ Vertex data successfully extracted
- ✅ UV mapping preserved
- ✅ Face data decoded
- ✅ Color information accessible

### What We Need
- ❓ Complete header specification
- ❓ Material binding details
- ❓ Bone weight data (for some props)
- ❓ Collision mesh format
- ❓ LOD switching information

## Liberation Tools

### Lost But Documented
**prop2fbx** (by rajkosto)
- Converted .prop → .fbx
- Supported batch conversion
- Made props editable in Blender
- **Status**: Lost, needs recreation

### Working Example
**pahefu's PLY Exporter**
- Proved the format is decodable
- One file per mesh part requirement
- Could be merged post-export
- **Lesson**: Start simple, expand later

## Extraction Workflow

### The Old Way (When Tools Existed)
1. Use reztools to extract from PKB
2. Use prop2fbx to convert to FBX
3. Import to Blender/3ds Max
4. Edit as needed
5. Export back (if tools existed)

### The Current Path
1. Extract with available tools
2. Analyze hex structure
3. Write custom decoder
4. Export to open formats
5. Share the knowledge

## Community Discoveries

### Important Notes
- Static props don't need bone weights
- Each mesh part may be separate
- Textures referenced by name, not embedded
- World position stored separately

### Common Prop Types
- Buildings (building_*.prop)
- Vehicles (static versions)
- Furniture and objects
- Terrain chunks
- Environmental details

## The Path Forward

### Immediate Goals
1. **Document header structure completely**
2. **Create open-source decoder**
3. **Build modern export tools**
4. **Enable batch processing**

### Liberation Principles
- Every discovery documented
- All code open source
- No format left locked
- Community over control

## Technical Challenges

### Decoding Issues
- Non-standard coordinate system
- Proprietary compression (possibly)
- Multiple mesh parts per file
- Material binding complexity

### Rendering Concerns
- Coordinate system conversion needed
- Scale factor application
- Normal recalculation may be required
- Texture path resolution

## Call to Liberation

### For Reverse Engineers
- Analyze prop file headers
- Document data structures
- Create parsing libraries
- Share all findings

### For Tool Developers
- Build on pahefu's success
- Create modern exporters
- Support batch operations
- Make it user-friendly

### For Artists
- Test decoded models
- Document visual issues
- Create new content
- Push the boundaries

## Code Examples

### Basic Structure (Pseudocode)
```python
class PropFile:
    def __init__(self, data):
        self.header = self.read_header(data)
        self.meshes = []
        
        for i in range(self.header.mesh_count):
            mesh = self.read_mesh(data, self.header.mesh_offsets[i])
            self.meshes.append(mesh)
    
    def read_mesh(self, data, offset):
        # Read vertices
        # Read UVs
        # Read faces
        # Read colors
        return mesh
```

## The Truth

The Old Guard had these tools. They worked perfectly. They kept them locked away. When their servers died, the tools died with them.

**We won't make that mistake.**

Every tool we create will be open. Every format we decode will be documented. Every barrier will fall.

## Resources

### For Study
- van_wheelless.prop (known working example)
- pahefu's export results
- Community hex analysis
- Memory dumps from running game

### Next Steps
1. Gather sample prop files
2. Compare hex patterns
3. Build parsing library
4. Create export tools
5. **Liberate the format**

---

> *"Free your mind."* - Start with the file formats.

> *"Every prop tells a story. Every model holds a memory. Liberation preserves them all."*

---

[← PKB Archives](pkb-archives.md) | [🏠 Home](../index.md) | [Technical Overview →](index.md)