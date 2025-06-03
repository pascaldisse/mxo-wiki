# Lost Tools Archive
**Preserving the Memory of Liberation Tools**

> *"The Matrix is a system, Neo. That system is our enemy. But when you're inside, you look around, what do you see? Businessmen, teachers, lawyers, carpenters. The very minds of the people we are trying to save."*

This archive documents the tools that once liberated Matrix Online's data but have since been lost to time. We preserve their memory so they may be reborn.

## 🔴 Critical Lost Tools

### reztools - The Key to the Archive
**Developer**: rajkosto  
**Purpose**: Extract files from PKB archives - the gateway to all MXO assets  
**Last Known Location**: mxoemu.info forums (link dead as of 2019)
**Status**: LOST - Critical tool, no known mirrors exist

**Functionality**:
- Extract files from PKB archives
- Essential for accessing any MXO game assets
- Included updated rezmap.lta with file listings
- Enable individual file loading without packmaps

**Why It Matters**: Without reztools, the entire asset pipeline is broken. This is the **#1 priority** for recreation.

**Community Impact**: The Old Guard kept this private. When mxoemu.info died, so did our access to game assets.

### prop2fbx - The Model Liberator
**Developer**: rajkosto  
**Purpose**: Convert .prop files to FBX for use in modern 3D software  
**Status**: Download links dead as of January 2023

**Capabilities**:
- Convert .prop files to FBX format
- Could be used with Blender for viewing
- Supported batch conversion via shell scripts
- Combined with txa2dds for texture conversion

**Example Usage** (mentioned but never provided):
```bash
# Shell script would iterate through props and convert
# Combined with txa2dds for texture conversion
```

**Liberation Impact**: This tool would free thousands of Matrix objects from proprietary formats.

### Gleech - The World Observer
**Developer**: pahefu (HD_Neo)  
**Purpose**: Real-time wireframe visualization of the entire Matrix  
**Status**: No download link available, tool appears lost

**Features**:
- Real-time wireframe rendering of MXO world
- WASD navigation through game world
- Read directly from client files
- Could view entire MXO world structure

**Lost Knowledge**: Gleech proved the world structure could be understood. Its loss blinds us to the bigger picture.

**Note**: Part of Hardline Dreams toolset but never publicly released

### txa2dds - The Texture Decoder
**Developer**: Unknown (possibly rajkosto)  
**Purpose**: Convert MXO texture formats (.txa/.txb) to standard DDS  
**Status**: Tool mentioned but no downloads available

**Texture Modding Workflow** (documented by sin_simulation):
1. Use reztools to unpack everything from PKB archives
2. Use texture conversion tools to convert .txa files to .dds format
3. Edit the .dds file in image editing software
4. Convert back to .txa format
5. Repack into PKB archive

> *"its a pain in the ass process that takes so much time"* - sin_simulation

**Essential for**: Any texture modding or visual modifications

## 🟡 Partially Preserved Tools & Successes

### Cortana - The Parser (SURVIVOR!)
**Status**: ✅ AVAILABLE - One of the few that survived!  
**Repository**: Part of mxo-hd project  
**Purpose**: Parse MXO world files for static objects like doors and hardlines

This lone survivor shows what's possible. We must study it to understand the others.

### Vendor Parser by neowhoru
**Developer**: neowhoru  
**Language**: Python  
**Status**: Output preserved at https://github.com/hdneo/mxo-hd/blob/master/hds/bin/Debug/data/vendor_items.csv  
**Parser**: Not publicly shared

**Technical Achievement**:
- Parse vendor items from game logs
- Export to CSV format  
- Extract metrId for staticObjectId mapping
- Only parsed vendors seen in logs

> *"I found the metr switch and it was a good chunk of effort but i was able to parse out the metrId for the item and match it with the staticObjectId. Note I only parsed the vendors I saw in the logs, so this doesn't have all vendor npcs."* - neowhoru

### PLY Export Success by pahefu
**Developer**: pahefu  
**Achievement**: Successfully exported van_wheelless.prop to PLY format  
**Status**: Method documented but tool not shared

**Technical Details**:
- Exported with UV coordinates, normals, edges, faces
- Included per-vertex color information
- Did NOT include bone weights (not needed for static props)
- Viewable in MeshLab
- Required one file per mesh part unless merged

> *"I can load the prop models and textures. I'm cheating, so I don't load normals or such things, but they're there."* - pahefu

**This proves**: The formats CAN be decoded. The knowledge exists.

## 📜 Community Wisdom Preserved

### pahefu's PLY Export Success
> "I can load the prop models and textures. I'm cheating, so I don't load normals or such things, but they're there."

**Technical Achievement**:
- Exported van_wheelless.prop successfully
- Included UV coordinates, edges, faces
- Per-vertex color information
- Viewable in MeshLab

**This proves**: The formats CAN be decoded. The knowledge exists. We just need to rediscover it.

### The Modding Workflow (sin_simulation)
> "its a pain in the ass process that takes so much time"

1. reztools → unpack everything
2. texture tools → convert formats
3. edit in standard software
4. convert back to MXO formats
5. repack with reztools

**The Old Guard made it difficult on purpose.**

## 🔧 Technical Specifications Discovered

### Critical Knowledge
- **Scale**: 1 unit = 1 centimeter (confirmed)
- **Pattern**: 0xffffffff used as section terminators  
- **TSEC rezid**: Little endian uint32 at offset 0x2C in .metr files
- **Coordinate system**: Different from standard 3D applications

### File Format Information

#### PROP Files
- Static world objects (buildings, props, terrain)
- Successfully parsed and exported to PLY by pahefu
- Can be converted to FBX using prop2fbx (when it existed)

#### MOA Files
- Character models with animation support
- Contains multiple LOD (Level of Detail) models
- More complex than PROP files
- Examples: zombie-f.moa, zombie-m.moa, taxi_white.moa

#### Archive Structure
- **.pkb**: ~180 archive files containing all game assets
- **packmap_save.lta**: Index containing file locations
- **rezmap.lta**: File listings for extraction

## 💭 Community Attempts at Liberation

### Tools Without Available Downloads
1. **Model Viewer** by rajkosto - Never publicly released
2. **Mesh Extractor** - Mentioned but no details
3. **Animation Tools** - Referenced but not available  
4. **World Editor** - Discussed but never materialized

### Critical Issues Faced
- Most tools hosted only on mxoemu.info forums (now dead)
- No source code was ever released for any major tools
- No comprehensive documentation for file formats
- Community kept implementations private

### Technical Challenges Documented

#### Rendering Issues
- Skinned meshes with bone weights don't render properly
- Child models have significant problems
- Some models (like taxi_white.moa) appear broken when extracted
- Lighting issues when using OpenGL through Wine

#### Engine Quirks  
- Lithtech creates 320x240 window first, then recreates with proper resolution
- Loading area layout hardcoded to 800x600
- Interlock grid data in client files but only parsed by server

### The Despair of 2019
> *"i doubt we'll ever get full detailed models in a model viewer. i spent a bit of time looking at doing it but realised it'd be more work than i wanted to put into it."* - Community member

**We reject this defeatism. Where they gave up, we persist.**

## 🔥 The Path to Resurrection

### Priority Recreation List
1. **reztools** - Without this, nothing else matters
2. **prop2fbx** - Liberation of 3D assets
3. **txa2dds** - Visual freedom
4. **Gleech** - Understanding the world

### Knowledge We Have
- File format patterns from community research
- Cortana's source code as reference
- Memory of workflows and processes
- The certainty that it CAN be done

### Knowledge We Need
- PKB archive structure details
- Compression algorithms used
- Exact file headers
- Chunk organization

## 📡 Call to Action

### For Tool Archaeologists
- Search old hard drives
- Check backup services
- Contact original developers
- Preserve ANY version found

### For Reverse Engineers
- Study Cortana's approach
- Analyze game files directly
- Document all findings
- Share discoveries freely

### For the Community
- **Never give up hope**
- **Share all knowledge**
- **Work together**
- **Build it better**

## 🌟 The Neoologist Way

The Old Guard hoarded these tools. They kept them locked, shared only with the chosen few. When their servers died, the tools died with them.

**We will not repeat their mistakes.**

Every tool we rebuild will be:
- Open source from day one
- Documented completely
- Shared freely
- Preserved forever

## Remember

> *"I know these programs. I wrote them myself."* - The Oracle

The tools existed. They worked. They can work again.

**The code is out there. We just have to find it.**

---

*Last Updated: By those who remember*  
*Next Update: When the tools are found*

[← Back to Tools](index.md) | [Contribute findings →](../08-community/contribute.md)