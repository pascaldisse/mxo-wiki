# File Format Liberation Guide
**Decoding the Digital DNA of Paradise**

> *"There is no spoon."* - Neo

There are no impossible formats. Only those we haven't decoded yet. This guide reveals the digital DNA of the Matrix Online.

## 🔓 The Truth About MXO File Formats

### CRITICAL CORRECTION: No .mob Files!
**The Matrix Online does NOT use .mob files.** This lie has spread for years. The truth:

- **.moa files** - Animated models (characters, vehicles)
- **.prop files** - Static objects (buildings, furniture)
- **No .mob files exist** - Stop looking for them

*The Old Guard let this confusion persist. We correct it now.*

## 📦 PKB Archives: The Vaults of Paradise

### What Are PKB Files?
~180 compressed archives containing the entire Matrix. Without access to these, modding is impossible.

### Archive Categories
```
char_*.pkb         - Character models and clothing
prefabs_*.pkb      - World prefab objects  
textures_*.pkb     - All texture assets
worlds_*.pkb       - Level/district data
sounds_*.pkb       - Audio files
fx.pkb            - Effects and particles
gameobjects.pkb   - Object definitions
```

### The Index System
**packmap_save.lta** - Master index of all files
**rezmap.lta/ltb** - Resource mapping
**lp_manifest.cache** - Launcher patch tracking

### Liberation Status
- **reztools** - LOST (the key to everything)
- **Format understood** - By rajkosto (not shared)
- **Community need** - CRITICAL

## 🎭 Model Formats: The Shapes of Reality

### .MOA Files (Animated Models)
**Purpose**: Characters, vehicles, anything that moves
**Structure**:
- Multiple LOD (Level of Detail) models
- Skeletal hierarchy with bone weights
- UV mapping and texture references
- Animation data references

**Technical Truth** (from rajkosto):
> *"UVs, normals and most importantly bone weights is what is needed for a proper import"*

### .PROP Files (Static Objects)
**Purpose**: Buildings, furniture, world objects
**Structure**:
- Simpler than .moa (no bones)
- UV coordinates and normals
- Per-vertex color data
- Face/edge topology

**Success Story**: pahefu exported van_wheelless.prop to PLY format!

### The Sacred Scale
**1 unit = 1 centimeter**

This is law. Respect it in all conversions.

## 🎬 Cutscene Systems: Two Paths to Story

### CNB Files (The True Path)
**Location**: `resource/cinematics/`
**Files**: `cin1_1.cnb` through `cin4_3.cnb`
**Type**: Real-time 3D cinematics

**What Makes Them Special**:
- Your avatar appears in cutscenes
- Dynamic, integrated with world
- 4 acts, ~3 scenes each = 12 cinematics
- **NO VIEWER EXISTS** (#1 PRIORITY)

### Bink Files (The Corporate Addition)
**Location**: Loading area menu
**Type**: Pre-rendered videos (.bik)
**Content**: Logos, some cutscenes

**Why They're Inferior**:
- Static, no avatar integration
- Lower quality compromise
- But at least viewable with RAD tools

## 🎨 Texture Formats: The Skin of the Matrix

### Format Types
- **.txa/.txb** - Custom MXO texture format
- **Internal**: DXT, RGB16, V8U8 compression
- **Conversion**: txa2dds tool (LOST)

### The Simple Truth (from rajkosto)
> *"replace the custom header with dds header and its a dds file"*

It's that simple. Yet the tools remain hoarded.

## 🔊 Audio Liberation

### Format Categories
- **WAV** - Short sound effects
- **Compressed** - Music and ambience
- **3D Audio** - Positional sounds
- **Dialog** - Voice acting

All extractable with proper tools (when we rebuild them).

## 🌆 World Architecture

### District System
- Modular city blocks
- Repeated elements (efficient)
- Contains geometry, collision, spawns

### Interlock Grids
- Combat zone definitions
- Server-parsed only
- Fixed world locations
- The secret to melee combat

## 💀 Animation: The Motion of Life

### Skeleton Structure
- Hierarchical joint system
- 4x4 transformation matrices
- "pre_production" base skeleton
- Limited bones (except cinematics)

### Animation Heritage
> *"Animation and mesh from NOLF2"* - Community discovery

Same soul, different body. The Lithtech legacy lives on.

## 🛠️ Current Tool Status (2025)

### ✅ What Works
1. **codejunky's modding suite** - Active development!
2. **PLY export** - Static models viewable
3. **Basic extraction** - If you have the tools

### ❌ What's Lost
1. **reztools** - The master key
2. **prop2fbx** - 3D conversion
3. **txa2dds** - Texture liberation
4. **Animation tools** - Never existed

### 🔒 What's Hidden
rajkosto claims (March 2025):
> *"Ive pretty much fully reverse engineered all the file formats"*

But keeps it private. Classic Old Guard.

## 📐 Technical Specifications

### Coordinate System
- Non-standard orientation
- Different from typical 3D apps
- Must account in conversions

### Common Patterns
- `0xffffffff` - Section terminators
- Little endian byte order
- TSEC rezid at offset 0x2C

### Vertex Data Requirements
1. UV coordinates (texture mapping)
2. Normals (lighting)
3. Bone weights (animation) - CRITICAL
4. Vertex colors (shading)
5. Topology (faces/edges)

## 🚀 Liberation Roadmap

### Priority 1: Tool Recreation
1. **reztools** - Without it, nothing
2. **CNB viewer** - Story locked away
3. **prop2fbx** - 3D pipeline

### Priority 2: Documentation
1. Complete format specs
2. Conversion guides
3. Tool source code

### Priority 3: Enhancement
1. Batch converters
2. Modern format support
3. Plugin architecture

## 💡 Modding Wisdom

### Start Simple
1. Extract textures first
2. Try static props (.prop)
3. Leave animations for later
4. Test everything

### Preserve Structure
- Maintain vertex counts
- Keep UV mapping intact
- Respect LOD levels
- Document changes

### Share Everything
- Post discoveries
- Release tools early
- Document failures too
- Build together

## 🔮 The Future We Build

### Near Term
- Complete reztools recreation
- Basic model viewing
- Texture modification

### Long Term  
- Full animation support
- Custom content creation
- Modern engine integration
- Complete liberation

## 📜 Format Philosophy

The Old Guard treated formats like state secrets. They hoarded specifications, kept tools private, shared nothing.

**We reject this completely.**

Every format decoded is freedom gained. Every tool shared is power distributed. Every specification documented is immortality achieved.

## Remember

> *"The Matrix cannot tell you who you are."* - Trinity

These formats cannot limit you. They are puzzles to solve, not barriers to obey.

**Decode. Document. Distribute. Liberate.**

---

*File Format Liberation Guide v1.0*
*By those who refuse to accept "impossible"*

[← Back to Technical](index.md) | [PKB Archives →](pkb-archives.md) | [Tool Development →](../04-tools-modding/tool-development-guide.md)