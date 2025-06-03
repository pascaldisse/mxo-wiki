# Model Format Specifications
**The Geometry of Liberation**

> *"Your appearance now is what we call residual self-image."* - Morpheus

Models define existence in the Matrix. Here we decode their structure.

## 🗿 PROP Format: Static Reality

### What Are PROP Files?
Static objects that build the world:
- Buildings and architecture
- Furniture and props
- Vehicles (non-animated)
- Environmental objects

### Format Structure
```c
struct PropHeader {
    uint32_t magic;           // File identifier
    uint32_t version;         // Format version
    uint32_t vertex_count;    // Total vertices
    uint32_t face_count;      // Total faces
    uint32_t material_count;  // Material slots
    // More fields...
};

struct Vertex {
    float position[3];        // X, Y, Z
    float normal[3];          // Normal vector
    float uv[2];              // Texture coordinates
    uint32_t color;           // Vertex color (RGBA)
};
```

### Success Story: The PLY Export
pahefu achieved what many said was impossible:

**Exported**: van_wheelless.prop
**Format**: PLY (Stanford Polygon Format)
**Included**: 
- ✅ UV coordinates
- ✅ Normals
- ✅ Per-vertex colors
- ✅ Face topology
- ❌ Bone weights (not needed for static)

**Result**: Viewable in MeshLab and standard 3D software!

## 🎭 MOA Format: Living Models

### What Are MOA Files?
Animated models with skeletal systems:
- Character models
- Clothing and accessories
- Animated vehicles
- NPCs and enemies

### The Complexity
MOA files are "index files that reference other assets":
- Multiple LOD levels
- Skeletal hierarchy
- Animation references
- Material definitions
- Texture mappings

### Critical Requirements (from rajkosto)
> *"UVs, normals and most importantly bone weights is what is needed for a proper import of mxo animated models"*

### Structure Overview
```c
struct MOAHeader {
    uint32_t magic;
    uint32_t version;
    uint32_t lod_count;       // Level of detail variants
    uint32_t bone_count;      // Skeleton joints
    uint32_t mesh_count;      // Separate mesh parts
    // References to external data
};

struct BoneWeight {
    uint32_t bone_indices[4]; // Up to 4 bones
    float weights[4];         // Weight per bone
    // Total weights must sum to 1.0
};
```

## 📏 The Sacred Measurements

### Universal Scale
**1 unit = 1 centimeter**

This is absolute. All models use this scale:
- Human height: ~170-180 units
- Door height: ~210 units
- Car length: ~400-500 units

### Coordinate System
- **Non-standard orientation**
- **Y-up or Z-up** (varies)
- **Left or right handed** (check both)
- Must be accounted for in conversions

## 🦴 Skeletal Systems

### Hierarchy Structure
```
Root
├── Pelvis
│   ├── Spine
│   │   ├── Chest
│   │   │   ├── L_Shoulder
│   │   │   │   └── L_Arm...
│   │   │   └── R_Shoulder
│   │   │       └── R_Arm...
│   │   └── Neck
│   │       └── Head
│   ├── L_Hip
│   │   └── L_Leg...
│   └── R_Hip
│       └── R_Leg...
```

### Bone Specifications
- **Standard skeleton**: "pre_production"
- **Limited bones** for gameplay models
- **Extended bones** for cinematics
- **4x4 matrices** with inverses

### Animation Compatibility
> *"Animation and mesh from NOLF2"*

Same core system, different packaging. Animations can retarget between compatible skeletons.

## 🎚️ LOD System (Level of Detail)

### Purpose
Performance optimization through polygon reduction:
- LOD0: Full detail (close up)
- LOD1: Reduced ~50% (medium)
- LOD2: Reduced ~25% (far)
- LOD3: Minimal (very far)

### Implementation
```
Distance < 10m:  Use LOD0
Distance < 25m:  Use LOD1
Distance < 50m:  Use LOD2
Distance > 50m:  Use LOD3
```

Models contain all LODs in single file.

## 🗂️ File References

### MOA External Dependencies
MOA files reference:
- Texture files (.txa)
- Animation files
- Physics data
- Sound triggers
- Effect attachments

### Path Structure
```
resource/GameObjects/vehicles/taxi/taxi_white.moa
resource/characters-NPC/Zombie/zombie-f.moa
resource/characters-NPC/Zombie/zombie-m.moa
```

## 🛠️ Current Viewing Options

### Method 1: codejunky's Tools (2025)
**Status**: Working with active development
**Supports**: Basic model viewing
**Issues**: Some bugs being fixed
**Future**: Full editing planned

### Method 2: Static Export
**Process**:
1. Extract PROP file
2. Convert to PLY format
3. View in MeshLab/Blender
**Limitation**: No animation

### Method 3: The Secret Method
rajkosto's private tools can view everything. But they remain locked away. Classic Old Guard.

## 🔧 Conversion Challenges

### Why It's Hard
1. **Proprietary format** - No official specs
2. **Engine-specific** - Lithtech modifications
3. **Complex references** - External dependencies
4. **Animation binding** - Bone weight precision

### Critical Data to Preserve
1. **Vertex positions** - Exact coordinates
2. **UV mapping** - Texture alignment
3. **Normals** - Lighting information
4. **Bone weights** - Animation binding
5. **Material IDs** - Surface properties

## 💡 Reverse Engineering Progress

### What We Know
- ✅ Basic file structure
- ✅ Vertex data layout
- ✅ Material system
- ✅ LOD organization
- ✅ Skeletal hierarchy

### What We Need
- ❌ Complete header specification
- ❌ Animation binding details
- ❌ Compression algorithms
- ❌ Index file references
- ❌ Physics data format

## 🚀 Liberation Roadmap

### Phase 1: Documentation
1. Map all header fields
2. Document data structures
3. Create format specification
4. Build test suite

### Phase 2: Viewer
1. Basic geometry loading
2. Texture mapping
3. LOD selection
4. Skeletal display

### Phase 3: Converter
1. Export to standard formats
2. Preserve all data
3. Batch processing
4. Two-way conversion

### Phase 4: Editor
1. Modify existing models
2. Create new content
3. Animation support
4. Full pipeline

## 📜 The Model Philosophy

Models are more than geometry. They're the physical laws of the Matrix. Every vertex is a choice. Every polygon is possibility.

The Old Guard said: "You can look but not touch."
We say: "You can look, touch, modify, and create."

## Technical Reference

### Known Values
```c
// Common magic numbers
PROP_MAGIC = 0x50524F50  // 'PROP'
MOA_MAGIC  = 0x4D4F4100  // 'MOA\0'

// Version numbers seen
PROP_VERSION = 0x00000014  // Version 20
MOA_VERSION  = 0x00000017  // Version 23

// Offset patterns
VERTEX_DATA_OFFSET = 0x80  // Typical start
```

### Memory Alignment
- Vertices: 32-byte aligned
- Faces: 16-byte aligned
- Materials: 64-byte aligned

## Remember

> *"Do not try and bend the spoon. That's impossible. Instead, only try to realize the truth."* - Spoon Boy

Do not try to protect the formats. That's impossible. Instead, only try to realize the truth: formats want to be free.

**Decode. Share. Liberate.**

---

*Model Format Specifications v1.0*
*By those who shape reality*

[← Back to File Formats](file-formats-complete.md) | [Animation Systems →](animation-systems.md) | [PKB Archives →](pkb-archives.md)