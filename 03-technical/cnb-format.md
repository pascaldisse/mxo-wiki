# CNB File Format
**The Lost Cinematics - Our Highest Priority**

> *"Unfortunately, no one can be told what the Matrix is. You have to see it for yourself."* - But we CAN'T see it without a viewer.

## 🔴 CRITICAL: No CNB Viewer Exists

This is our **#1 PRIORITY**. CNB files contain real-time 3D cinematics that tell the entire Matrix Online story. Without a viewer, this narrative is LOST.

## What Are CNB Files?

**Cinematic Bundles** - Real-time 3D cutscenes that:
- Integrate player avatars into story scenes
- Render dynamically with game engine
- Contain the core narrative of MXO
- Are completely inaccessible today

### Known CNB Files
```
resource/cinematics/
├── cin1_1.cnb through cin1_3.cnb (Act 1)
├── cin2_1.cnb through cin2_3.cnb (Act 2)  
├── cin3_1.cnb through cin3_3.cnb (Act 3)
├── cin4_1.cnb through cin4_3.cnb (Act 4)
└── ~12 total files containing ALL story cinematics
```

## Why This Matters

### The Story is Trapped
- Major plot points locked in CNB
- Character moments inaccessible
- Morpheus' fate unrevealed
- Neo's legacy hidden

### Not Just Videos
- **Real-time**: Rendered live with player avatar
- **Dynamic**: Camera movements, lighting
- **Interactive**: Player appears in scenes
- **Unique**: Can't be replaced with video capture

*These aren't movies. They're experiences. And they're lost.*

## Technical Challenge

### What We Know
- Proprietary format (no documentation)
- Contains 3D scene data
- References character models
- Includes camera paths
- Has dialogue/audio triggers

### What We Don't Know
- ❓ File structure
- ❓ Compression method
- ❓ Scene graph format
- ❓ Animation data layout
- ❓ Everything else

## The Void

### No Tools Exist
- ❌ No viewer (not even read-only)
- ❌ No extractor
- ❌ No converter
- ❌ No documentation
- ❌ No community knowledge

### Historical Attempts
- No record of anyone cracking CNB
- rajkosto likely understood it (but private)
- No public tools ever created
- Format remains completely opaque

## Liberation Priority

### Why CNB First?
1. **Preserves the story** - Core MXO narrative
2. **Unique content** - Can't be recreated
3. **Player integration** - Your avatar in history
4. **Time sensitive** - Knowledge fading
5. **Community impact** - Everyone wants this

### What Success Enables
- Story preservation for all time
- New players can experience plot
- Content creators get material
- Historians document properly
- The Matrix story continues

## Research Approach

### Starting Points
1. **File Headers** - Identify format signatures
2. **Compression** - Test standard algorithms
3. **References** - Find model/texture links
4. **Structure** - Map data organization
5. **Comparison** - Check similar formats

### Tools Needed
- Hex editor for analysis
- Compression testers
- 3D format knowledge
- Pattern recognition
- Community collaboration

## Call to Action

### 🚨 URGENT: We Need You

#### For Reverse Engineers
- This is the holy grail
- Glory awaits the decoder
- Full community support
- Document EVERYTHING

#### For Developers  
- Build analysis tools
- Create format parsers
- Test rendering approaches
- Share all progress

#### For Community
- Share ANY knowledge
- Test tools immediately
- Spread the word
- Support the effort

## Technical Speculation

### Possible Structure
```
CNB File {
    Header {
        magic_number
        version
        scene_count
        offset_table
    }
    
    Scenes[] {
        camera_paths
        model_references
        animation_data
        audio_triggers
        lighting_info
    }
    
    Resources {
        compressed_data
        reference_table
    }
}
```

### Similar Formats
- Lithtech cinematic systems
- Bink video containers (but different)
- Game engine cutscene formats
- Real-time scene graphs

## The Dream

### What We're Building
```python
# The future
cnb_viewer = CNBViewer()
cnb_viewer.load("cin1_1.cnb")
cnb_viewer.play()
# Result: The story lives again
```

### Features Needed
1. **Basic Viewer** - Just play them
2. **Export Function** - Preserve as video
3. **Avatar Integration** - Use your character
4. **Scene Editor** - Create new stories

## Resources

### What We Have
- 12 CNB files (complete story)
- File names indicating acts
- Community desperate for access
- Will to succeed

### What We Need
- Format documentation
- Decompression method
- Rendering pipeline
- Your help

## The Stakes

Without CNB liberation:
- ❌ Story remains locked forever
- ❌ New players never experience plot
- ❌ History incomplete
- ❌ Content lost to time

With CNB liberation:
- ✅ Complete story accessible
- ✅ New cinematics possible
- ✅ History preserved
- ✅ Eden truly reborn

## The Manifesto

> *"I'm trying to free your mind, Neo. But I can only show you the door. You're the one that has to walk through it."*

The door is CNB. Behind it lies the complete Matrix Online story. We stand before it, waiting for the one who will open it.

**Will it be you?**

---

## 🎯 ACTION REQUIRED

This is not just another format. This is THE format. The story of The Matrix Online lives or dies with CNB.

**Priority Level: MAXIMUM**  
**Difficulty: Unknown**  
**Reward: Eternal Glory**  
**Status: Waiting for a hero**

---

> *"The story remains locked until someone breaks the code. Will you be the one?"*

---

[← File Formats](file-formats.md) | [🏠 Home](../index.md) | [PKB Archives →](pkb-archives.md)