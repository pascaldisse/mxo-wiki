# Tool Archaeology Report
**Excavating the Digital Ruins**

> *"Unfortunately, no one can be told what the Matrix is. You have to see it for yourself."* - Morpheus

This document chronicles our search through the digital ruins for the tools that once liberated Matrix Online. Updated June 3, 2025.

## 📊 Archaeological Survey Results

### Total Tools Documented: 15+
- **Lost Completely**: 8 (reztools, prop2fbx, txa2dds, Gleech, and others)
- **Output Preserved**: 2 (vendor parser output, PLY exports)
- **Still Available**: 1 (Cortana parser)
- **Never Existed**: 1 (CNB viewer - our #1 need)

### Time Period: 2016-2023
The golden age of MXO tool development, ending with the collapse of hosting sites.

## 🔍 The Great Search of 2025

### What We Searched

#### Primary Sources
- **mxoemu.info forums** - Dead since 2019
- **GitHub repositories** - Some survivors
- **Discord archives** - 32,000+ messages analyzed
- **Wayback Machine** - Limited captures
- **Personal collections** - Few willing to share

#### Key Developers Traced
- **rajkosto** - Created most tools, kept them private
- **pahefu (HD_Neo)** - Gleech developer, some success
- **neowhoru** - Parser creator, shared output only
- **codejunky** - Modern tools (excluded per request)

### What We Found

#### The Lone Survivor: Cortana
- **Location**: Part of mxo-hd project
- **Function**: Parse world files for static objects
- **Significance**: Proves tools CAN survive if shared

#### Preserved Outputs (Not Tools)
- **vendor_items.csv** - neowhoru's parser results
- **PLY exports** - pahefu's successful extractions
- **Screenshots** - Tool interfaces (expired Discord links)

#### Dead Links Cemetery
```
mxoemu.info/reztools.zip - Dead 2019
mxoemu.info/forum/thread-955.html - Tool thread gone
mxo.hardlinedreams.com/tools - Redirects nowhere
Discord CDN links - All expired
```

## 💀 The Graveyard of Lost Tools

### reztools - The Gatekeeper
**Last Seen**: mxoemu.info forums (2019)
**Death**: Forum closure, no mirrors
**Impact**: Entire modding pipeline broken
**Lesson**: Critical tools need multiple backups

### prop2fbx - The Liberator
**Last Seen**: Forum links (January 2023)
**Death**: Links died, source never shared
**Impact**: 3D workflow crippled
**Lesson**: Binary-only releases die with their hosts

### Gleech - The World Viewer
**Last Seen**: In HD_Neo's demonstrations
**Death**: Never publicly released
**Impact**: World understanding limited
**Lesson**: "Coming soon" often means never

### txa2dds - The Texture Bridge
**Last Seen**: Mentioned in workflows
**Death**: Part of lost toolchain
**Impact**: Visual modding blocked
**Lesson**: Dependent tools create cascading failures

## 📜 Wisdom from the Ruins

### Community Quotes Preserved

#### The Defeatist (2019)
> *"i doubt we'll ever get full detailed models in a model viewer. i spent a bit of time looking at doing it but realised it'd be more work than i wanted to put into it."*

**Our Response**: This attitude is why tools die. We reject it completely.

#### The Realist (pahefu)
> *"I can load the prop models and textures. I'm cheating, so I don't load normals or such things, but they're there."*

**Our Response**: "Cheating" that works is better than perfection that doesn't exist.

#### The Worker (neowhoru)
> *"I found the metr switch and it was a good chunk of effort but i was able to parse out the metrId for the item and match it with the staticObjectId."*

**Our Response**: This dedication is what we need. Every puzzle piece matters.

#### The Frustrated (sin_simulation)
> *"its a pain in the ass process that takes so much time"*

**Our Response**: The Old Guard made it painful on purpose. We'll make it simple.

## 🔬 Technical Discoveries from Archaeology

### What the Ruins Tell Us

#### File Format Clues
- Scale confirmed: 1 unit = 1 centimeter
- Terminators found: 0xffffffff patterns
- Byte order: Little endian confirmed
- Coordinates: Non-standard system

#### Workflow Fragments
1. reztools extracts PKB files
2. Conversion tools process formats
3. Standard tools edit assets
4. Reverse conversion
5. Repackaging into PKB

#### Success Patterns
- Simple tools survived longer
- Open source tools still exist
- Integrated tools (like Cortana) survived
- Standalone binaries all died

## 🏛️ Lessons for Future Archaeologists

### Why Tools Disappeared

1. **Single Point of Failure**
   - Hosted on one forum
   - No mirrors created
   - Source never shared
   - Developer vanished

2. **Intentional Hoarding**
   - "Not ready yet" excuses
   - Private development
   - Closed circles
   - Knowledge gatekeeping

3. **Technical Barriers**
   - Complex formats
   - Lack of documentation
   - No collaboration
   - Overwhelming scope

4. **Community Failures**
   - Didn't demand open source
   - Accepted "coming soon"
   - Failed to mirror files
   - Trusted single developers

## 🚀 Preventing Future Loss

### The Neoologist Protocol

**Every Tool Must**:
1. Be open source from commit #1
2. Have multiple mirrors
3. Include documentation
4. Accept contributions
5. Release early and often

**Every Developer Must**:
1. Share knowledge freely
2. Document everything
3. Collaborate openly
4. Pass the torch
5. Reject perfectionism

**Every User Must**:
1. Mirror downloads
2. Preserve documentation
3. Share discoveries
4. Support developers
5. Demand openness

## 📡 Active Excavation Sites

### Where We're Still Digging

1. **Old Hard Drives**
   - Community members' backups
   - Developer archives
   - Mirror sites

2. **Alternative Sources**
   - University archives
   - Gaming preservation groups
   - Private collections

3. **Indirect Evidence**
   - Forum quotes
   - Video demonstrations
   - Screenshot analysis

### Recent Discoveries

- **June 2025**: HD Enhanced server includes some tools
- **May 2025**: Community member claims PKB format knowledge
- **April 2025**: Cortana source studied for patterns
- **March 2025**: Workflow documentation found

## 🎯 Reconstruction Priorities

Based on our archaeological findings:

### Immediate Needs
1. **reztools** - Without it, nothing works
2. **CNB viewer** - Never existed, desperately needed
3. **prop2fbx** - For 3D liberation
4. **txa2dds** - For visual freedom

### Reconstruction Approach
1. Study Cortana for parsing patterns
2. Analyze PKB files directly
3. Reverse engineer from memory
4. Build incrementally
5. Share immediately

## 💭 Final Thoughts

### What We Lost
Not just tools, but:
- Years of knowledge
- Collaborative potential  
- Creative possibilities
- Community trust

### What We Learned
- Closed source = eventual death
- Single hosts = single points of failure
- Perfectionism = procrastination
- Hoarding = community harm

### What We'll Build
- Open tools for all
- Distributed preservation
- Collaborative development
- Sustainable future

## 📜 The Archaeological Record

This document serves as testimony that these tools existed, worked, and were lost through negligence and greed. Let it remind us:

**Never again will we allow knowledge to be hoarded.**
**Never again will we trust closed development.**
**Never again will we lose our tools to time.**

## Remember

> *"The Matrix is everywhere. It is all around us."* - Morpheus

The tools are out there, in fragments and memories. Through archaeology, reverse engineering, and determination, we will rebuild them all.

**The future is open. The code is eternal. The liberation continues.**

---

*Archaeological Survey Date: June 3, 2025*
*Next Survey: When tools are found or rebuilt*

[← Back to Preservation](index.md) | [Tool Development →](../04-tools-modding/tool-development-guide.md) | [Join the Search →](../08-community/contribute.md)