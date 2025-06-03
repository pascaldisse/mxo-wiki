# Texture Format Deep Dive
**Liberating the Visual Essence**

> *"What you know you can't explain, but you feel it."* - Morpheus

Textures are the skin of the Matrix. Here we peel back the layers.

## 🎨 TXA/TXB Format: The Custom Canvas

### The Big Secret (Revealed)
rajkosto told us the truth:
> *"replace the custom header with dds header and its a dds file"*

**It's literally that simple.** The MXO texture format is just DDS with a custom header. Yet this knowledge was hoarded for years.

### Format Structure
```
[Custom MXO Header] [DDS Data]
     ↓ Replace ↓
[Standard DDS Header] [DDS Data]
     ↓ Result ↓
   Viewable DDS File!
```

### Compression Types Found
- **DXT1** - Basic compression (no alpha)
- **DXT3** - With alpha channel
- **DXT5** - Better alpha compression
- **RGB16** - Uncompressed 16-bit
- **V8U8** - Normal maps

## 🔧 The Lost Tool: txa2dds

### What It Did
- Extract .txa/.txb from PKB archives
- Replace headers automatically
- Batch conversion support
- Both directions (txa↔dds)

### Why It Matters
Without txa2dds, texture modding requires:
1. Manual header analysis
2. Hex editing each file
3. No batch processing
4. Painful reverse conversion

**Status**: LOST. Must be recreated.

## 📁 Texture Categories in MXO

### Character Textures
**Location**: `char_*.pkb` archives
- Skin textures (various tones)
- Clothing (all types)
- Hair textures
- Accessories
- RSI customization layers

### World Textures
**Location**: `worlds_*.pkb`, `prefabs_*.pkb`
- Building facades
- Street textures
- Sidewalk patterns
- Signage and decals
- Environmental details

### Effect Textures
**Location**: `fx.pkb`
- Particle effects
- Glows and auras
- Code vision effects
- Bullet time visuals
- UI elements

### Special Textures
- **Cubemaps** - Reflections
- **Normal maps** - Surface detail
- **Specular maps** - Shininess
- **Glow maps** - Self-illumination

## 🛠️ Texture Modding Workflow

### The Old Way (When Tools Existed)
```bash
# 1. Extract from PKB
reztools -e textures_city.pkb

# 2. Convert to DDS
txa2dds building_facade.txa building_facade.dds

# 3. Edit in Photoshop/GIMP
# (Maintain dimensions, use DDS plugin)

# 4. Convert back
dds2txa building_facade.dds building_facade.txa

# 5. Repack into PKB
reztools -p textures_city.pkb
```

### The Current Way (Tools Lost)
Manual process - painful but possible:
1. Extract file from PKB (somehow)
2. Hex edit to replace header
3. Edit DDS in graphics software
4. Hex edit back to TXA
5. Reinsert into PKB (somehow)

*This is why we need tools rebuilt.*

## 🎯 Texture Requirements

### Dimension Rules
- **Power of 2** required (128, 256, 512, 1024)
- **Aspect ratios** flexible (256x512 OK)
- **Maximum size** varies by type
- **Mipmaps** auto-generated

### Quality Guidelines
- Character textures: 512x512 minimum
- World textures: 256-1024 varied
- UI elements: Exact sizes required
- Effects: Often smaller (128x128)

### Alpha Channel Usage
- **Transparency** - Glass, effects
- **Glow maps** - Self-illumination
- **Specular** - Reflection intensity
- **Team colors** - Faction overlays

## 💡 Modding Best Practices

### Maintain Original Properties
1. **Keep dimensions** - Don't resize
2. **Preserve compression** - Match format
3. **Alpha channels** - Don't delete
4. **Mipmap levels** - Let tools handle

### Visual Consistency
- Study original art style
- Match color palettes
- Respect Matrix aesthetic
- Test in various lighting

### Performance Considerations
- Texture memory limited
- Compression reduces load
- Mipmaps prevent aliasing
- Balance quality vs. performance

## 🔬 Technical Deep Dive

### Header Comparison
**MXO TXA Header** (first 128 bytes):
```
[Custom identifier]
[Dimension data]
[Compression type]
[Mipmap count]
[Unknown fields]
```

**Standard DDS Header**:
```
'DDS ' (magic number)
[Header size]
[Flags]
[Height/Width]
[Pitch/LinearSize]
[Depth]
[MipMapCount]
[Reserved]
[PixelFormat]
[Caps]
```

The conversion is just mapping fields!

### Compression Analysis
Most textures use DXT compression because:
- 6:1 compression ratio
- Hardware accelerated
- Good quality/size balance
- Fast loading

## 🚀 Tool Recreation Guide

### Building New txa2dds

**Step 1**: Analyze headers
```python
# Read first 128 bytes of .txa
# Identify dimension fields
# Map compression types
# Document differences
```

**Step 2**: Build converter
```python
def txa_to_dds(input_file):
    # Read TXA header
    # Extract image dimensions
    # Determine compression
    # Build DDS header
    # Copy image data
    # Write new file
```

**Step 3**: Add batch support
```python
# Process entire directories
# Maintain folder structure
# Generate conversion log
```

## 🌟 Success Stories

### What's Been Done
- Individual texture replacements
- UI customization mods
- Character texture swaps
- Some effect modifications

### What's Possible
- Complete visual overhauls
- HD texture packs
- Custom faction designs
- Modern visual effects

## 📚 Resources Needed

### For Tool Development
1. Sample .txa files
2. Corresponding .dds versions
3. Header documentation
4. Compression specifications

### For Modding
1. DDS plugin for Photoshop/GIMP
2. Texture templates
3. Color palette guides
4. Testing methodology

## 🎭 The Philosophy of Textures

Textures are more than pixels. They're the visual language of the Matrix. Every surface tells a story. Every detail adds to immersion.

The Old Guard hoarded the tools to control this language. They wanted to be the only artists in paradise.

**We reject this gatekeeping.**

## Remember

> *"The Matrix is everywhere. It is all around us."* - Morpheus

Every texture is part of the illusion. Master them, and you master the visual reality of the Matrix.

**Your textures. Your vision. Your Matrix.**

---

*Texture Liberation Guide v1.0*
*For those who see beyond the surface*

[← Back to File Formats](file-formats-complete.md) | [Model Formats →](model-formats.md) | [Tool Development →](../04-tools-modding/tool-development-guide.md)