# Tool Development Guide
**Rebuilding What Was Lost**

> *"I imagine that right now, you're feeling a bit like Alice. Tumbling down the rabbit hole?"* - Morpheus

The Old Guard took their tools to the grave. Now we rebuild, but this time with liberation in mind.

## 🎯 Priority Development Targets

### 1. reztools Recreation (CRITICAL)
**What We Know**:
- Extracts from ~180 .pkb archive files
- Uses packmap_save.lta as index
- Generates rezmap.lta for file listings
- Essential for ALL other tools

**Starting Points**:
- Study PKB file headers in hex editor
- Analyze packmap_save.lta structure
- Look for compression signatures
- Document all findings publicly

### 2. CNB Viewer (#1 COMMUNITY NEED)
**Files to Study**:
- resource/cinematics/cin1_1.cnb through cin4_3.cnb
- Real-time 3D cinematics with player integration
- No existing viewer or documentation

**Approach**:
- Compare CNB headers to known formats
- Look for model/animation references
- Study how game client loads them
- Build incrementally, share progress

### 3. Model Viewer Enhancement
**Building on Success**:
- codejunky has partial viewer (2025)
- pahefu proved PROP export works
- We know the scale (1 unit = 1cm)

**Next Steps**:
- Support .moa files (animated models)
- Implement bone weight rendering
- Fix child model issues
- Add texture support

## 🔧 Technical Foundation

### Known File Structures

#### PROP Format (Partially Decoded)
```
Header:
- Magic number identification
- Version information
- Mesh count
- Material references

Mesh Data:
- Vertex positions (3 floats)
- UV coordinates (2 floats)
- Normals (3 floats)
- Per-vertex colors
- Face indices
```

#### MOA Format (More Complex)
- Multiple LOD levels
- Animation data
- Bone hierarchy
- More challenging than PROP

#### PKB Archives (Priority)
- Container format for all assets
- Likely compressed
- Index in packmap_save.lta
- ~180 files total

### Critical Technical Details

**Coordinate System**:
- Non-standard orientation
- Different from typical 3D apps
- Must account for in converters

**Common Patterns**:
- 0xffffffff as terminators
- Little endian byte order
- TSEC rezid at offset 0x2C

**Engine Quirks**:
- Lithtech engine specific
- 320x240 initial window
- 800x600 hardcoded loading area

## 💡 Learning from Successes

### pahefu's PLY Export Method
Successfully exported van_wheelless.prop with:
- UV coordinates preserved
- Normals included (though he "cheated")
- Per-vertex colors
- Viewable in standard software

**Key Insight**: Start simple, get working output, iterate.

### neowhoru's Vendor Parser
Parsed game logs to extract:
- Vendor item databases
- metrId to staticObjectId mapping
- CSV output for easy use

**Key Insight**: Sometimes indirect methods work when direct access fails.

### Cortana's Survival
The only major tool to survive because:
- Part of larger project (mxo-hd)
- Focused scope (world objects)
- Practical over perfect

**Key Insight**: Release early, document well, integrate with community projects.

## 🚀 Development Philosophy

### The Neoologist Way

**DO**:
- Share code from day one
- Document EVERYTHING
- Release early and often
- Welcome all contributors
- Focus on liberation, not perfection

**DON'T**:
- Keep tools private
- Wait for "perfect" versions
- Work in isolation
- Gatekeep knowledge
- Give up when it's hard

### Start Small, Dream Big

1. **Minimum Viable Tool**
   - Single file format support
   - Basic functionality only
   - Command line is fine
   - Just make it work

2. **Iterate Publicly**
   - Push every commit
   - Document failures too
   - Ask for help often
   - Celebrate small wins

3. **Build Community**
   - Make it easy to contribute
   - Write clear documentation
   - Respond to issues
   - Share the credit

## 📚 Resources for Builders

### Where to Start
1. **GitHub Repositories**:
   - https://github.com/hdneo/mxo-hd (study Cortana)
   - Community forks and attempts
   - Related game tool projects

2. **Technical References**:
   - Lithtech engine documentation
   - Similar game format guides
   - 3D format specifications
   - Compression algorithms

3. **Community Knowledge**:
   - Discord discussions
   - Forum archives (when accessible)
   - Personal communications
   - Collective memory

### Development Environment

**Recommended Setup**:
- Python for rapid prototyping
- C++ for performance tools
- Hex editor for format study
- Git for version control
- GitHub for hosting

**Useful Libraries**:
- File parsing: struct (Python)
- 3D math: numpy, glm
- GUI: Qt, Dear ImGui
- Compression: zlib, lz4

## 🎮 Testing Resources

### Sample Files
Look for:
- Small .prop files for initial tests
- Simple .moa models
- Individual .pkb archives
- Known-good exports

### Validation Methods
- Compare with pahefu's PLY exports
- Check against game screenshots
- Verify scale and orientation
- Test with multiple files

## 🌟 The Future We Build

### Short Term Goals
1. Working PKB extractor
2. Basic model viewer
3. CNB format documentation
4. Texture conversion tools

### Long Term Vision
- Complete tool suite
- Modern engine port
- Enhanced graphics
- Community content

### Your Role
Every line of code matters. Every discovery helps. Every tool shared is a victory against the Old Guard's hoarding.

**You don't need permission to start.**
**You don't need to be perfect.**
**You just need to begin.**

## 📡 Call to Action

### For Beginners
- Pick ONE file format
- Study it in hex editor
- Document what you find
- Share your notes

### For Experienced Devs
- Tackle the hard problems
- Mentor newcomers
- Review pull requests
- Lead by example

### For Everyone
- **Reject gatekeeping**
- **Embrace failure**
- **Share everything**
- **Never give up**

## Remember

> *"There is a difference between knowing the path and walking the path."* - Morpheus

The tools were built once. They can be built again. Better. Freer. Together.

**The future is open source. The future is ours.**

---

*"Welcome to the desert of the real."*

[← Back to Tools](index.md) | [Join Development →](../08-community/contribute.md) | [Technical Specs →](../03-technical/file-formats.md)