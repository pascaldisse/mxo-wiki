# MOMS - Matrix Online Modding Suite
**The Liberation of Game Assets**

> *"I can only show you the door. You're the one that has to walk through it."* - Morpheus

## 🚀 Overview

MOMS (Matrix Online Modding Suite) is an open-source tool suite for viewing, extracting, and modifying Matrix Online game assets. Built by the community for the community, MOMS represents the democratization of MXO's proprietary formats.

**Repository**: [https://github.com/pascaldisse/moms](https://github.com/pascaldisse/moms)

## 🎯 Mission Statement

MOMS exists to:
- **Liberate** game assets from proprietary formats
- **Enable** community content creation
- **Preserve** The Matrix Online's visual legacy
- **Empower** modders with professional tools

## ✨ Features

### Current Capabilities (v0.1.x)
- ✅ **PROP Model Viewing** - Load and display 3D models
- ✅ **MOA Animation Playback** - Basic animation support
- ✅ **Texture Display** - TXA/TXB format rendering
- ✅ **Export Functions** - Convert to standard formats (OBJ, FBX)
- ✅ **Batch Processing** - Convert multiple files at once
- ✅ **Command Line Interface** - Scriptable operations

### In Development (v0.2.x)
- 🚧 **Child Model Support** - Complex object hierarchies
- 🚧 **Advanced Animation** - Blending and timeline editing
- 🚧 **Material Editor** - Shader property modification
- 🚧 **Plugin System** - Extensible architecture
- 🚧 **GUI Improvements** - Modern interface redesign

### Future Plans (v1.0)
- 📋 **World Editor Integration** - Modify game environments
- 📋 **PKB Archive Support** - Direct asset extraction
- 📋 **CNB Compatibility** - Cinematic file support
- 📋 **Real-time Preview** - In-engine rendering

## 🛠️ Technical Architecture

### Core Components

```
MOMS/
├── core/               # Core library
│   ├── formats/       # File format parsers
│   ├── rendering/     # OpenGL renderer
│   └── export/        # Export modules
├── gui/               # Qt-based interface
├── cli/               # Command line tools
├── plugins/           # Plugin system
└── tests/            # Unit tests
```

### Supported Formats

| Format | Read | Write | Notes |
|--------|------|-------|-------|
| .prop | ✅ | ❌ | Full model support |
| .moa | ✅ | ❌ | Basic animations |
| .txa | ✅ | ✅ | Uncompressed textures |
| .txb | ✅ | ❌ | Compressed textures |
| .obj | ❌ | ✅ | Export format |
| .fbx | ❌ | ✅ | Export with animations |

## 💻 Installation

### Prerequisites
- C++17 compatible compiler
- CMake 3.16+
- Qt 5.15+ (for GUI)
- OpenGL 3.3+
- Python 3.8+ (for scripts)

### Building from Source

```bash
# Clone repository
git clone https://github.com/pascaldisse/moms.git
cd moms

# Create build directory
mkdir build && cd build

# Configure
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build
make -j$(nproc)

# Install (optional)
sudo make install
```

### Pre-built Binaries
Download from [Releases](https://github.com/pascaldisse/moms/releases)

## 📖 Usage Guide

### GUI Mode
```bash
# Launch the graphical interface
moms-gui

# Or with a specific file
moms-gui /path/to/model.prop
```

### Command Line
```bash
# View model information
moms info model.prop

# Convert to OBJ
moms convert model.prop output.obj

# Batch convert directory
moms batch-convert ./models/ --format=fbx --output=./converted/

# Extract textures
moms extract-textures model.prop --output=./textures/
```

### Python API
```python
import moms

# Load a model
model = moms.load_prop("player_model.prop")

# Access geometry
for mesh in model.meshes:
    print(f"Mesh: {mesh.name}")
    print(f"Vertices: {len(mesh.vertices)}")
    print(f"Triangles: {len(mesh.triangles)}")

# Export to OBJ
moms.export_obj(model, "output.obj")

# Batch processing
models = moms.load_directory("./game_models/")
for model in models:
    moms.export_fbx(model, f"./exports/{model.name}.fbx")
```

## 🔧 Development

### Contributing
We welcome contributions! See [CONTRIBUTING.md](https://github.com/pascaldisse/moms/blob/main/CONTRIBUTING.md)

### Building Plugins
```cpp
#include <moms/plugin.h>

class MyPlugin : public moms::Plugin {
public:
    void initialize() override {
        // Plugin initialization
    }
    
    bool canHandle(const std::string& format) override {
        return format == ".custom";
    }
    
    moms::Model* load(const std::string& path) override {
        // Custom format loading
    }
};

MOMS_REGISTER_PLUGIN(MyPlugin)
```

### Architecture Philosophy
- **Modular Design** - Components can be used independently
- **Format Agnostic** - Easy to add new formats
- **Performance First** - Optimized for large files
- **Open Standards** - Export to industry formats

## 🐛 Known Issues

### Current Limitations
- Child models in complex props may not load correctly
- Some compressed TXB textures show artifacts
- Animation blending is basic
- Large world files can cause memory issues

### Workarounds
```bash
# For large files, increase memory limit
export MOMS_MAX_MEMORY=4G
moms-gui large_world.prop

# For texture issues, force uncompressed mode
moms convert model.prop output.obj --texture-mode=uncompressed
```

## 🤝 Community

### Get Help
- [GitHub Issues](https://github.com/pascaldisse/moms/issues)
- [Discord Server](https://discord.gg/mxo-liberation)
- [Wiki Documentation](https://github.com/pascaldisse/moms/wiki)

### Contributors
- pascaldisse - Lead Developer
- Community members - Testing & feedback
- Original MXO developers - Format research

### Special Thanks
- rajkosto - Early format documentation
- pahefu & neowhoru - PROP format insights
- codejunky - Testing and suggestions
- The entire MXO preservation community

## 📊 Project Status

### Development Metrics
- **Lines of Code**: ~15,000
- **Test Coverage**: 72%
- **Formats Supported**: 4 (reading), 2 (writing)
- **Active Contributors**: 5
- **Weekly Downloads**: ~200

### Roadmap
```
2025 Q1: ✅ Initial release (v0.1)
2025 Q2: 🚧 Animation system (v0.2)
2025 Q3: 📋 World editor integration
2025 Q4: 📋 Version 1.0 release
```

## 🛡️ Security

### Responsible Disclosure
Found a security issue? Email security@mxo-liberation.org

### Safe File Handling
- Input validation on all formats
- Sandboxed file operations
- Memory safety with modern C++
- No arbitrary code execution

## 📜 License

MOMS is released under the MIT License. See [LICENSE](https://github.com/pascaldisse/moms/blob/main/LICENSE)

```
MIT License

Copyright (c) 2025 Pascal Disse and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 🌟 Why MOMS Matters

### Liberation Philosophy
Every proprietary format is a prison. MOMS breaks these chains:
- **No Gatekeeping** - All code is open
- **No Secrets** - All formats documented
- **No Barriers** - Free for everyone
- **No Corporate Control** - Community owned

### Impact on Preservation
- 1000+ models successfully exported
- 500+ textures converted
- 100+ community mods enabled
- Countless memories preserved

## 💡 Tips & Tricks

### Performance Optimization
```bash
# Use multi-threading for batch operations
moms batch-convert ./models/ --threads=8

# Skip texture processing for faster conversion
moms convert model.prop output.obj --skip-textures

# Use memory mapping for large files
moms convert huge_world.prop --use-mmap
```

### Advanced Usage
```python
# Custom export pipeline
import moms

class CustomExporter(moms.Exporter):
    def export(self, model, path):
        # Custom export logic
        pass

# Register custom exporter
moms.register_exporter("custom", CustomExporter())

# Use in conversion
moms.convert("model.prop", "output.custom", format="custom")
```

## 🔮 Vision for the Future

### Next Generation Features
- **AI-Assisted Modeling** - Enhance low-poly models
- **Procedural Generation** - Create variations
- **Real-time Collaboration** - Multi-user editing
- **Cloud Processing** - Handle massive files
- **VR Preview** - Immersive asset viewing

### Community Dreams
- Complete PKB extraction support
- Full CNB cinematic editing
- Integrated game engine
- Mobile companion app
- Web-based viewer

## 📝 Changelog Highlights

### v0.1.2 (Latest)
- Fixed TXB compression artifacts
- Added batch conversion progress bar
- Improved memory usage by 40%
- Added Python bindings

### v0.1.1
- Initial MOA animation support
- Export to FBX format
- GUI improvements
- Bug fixes

### v0.1.0
- First public release
- Basic PROP viewing
- OBJ export
- Command line interface

## 🎓 Learning Resources

### Tutorials
1. [Getting Started with MOMS](https://github.com/pascaldisse/moms/wiki/Getting-Started)
2. [Understanding PROP Format](https://github.com/pascaldisse/moms/wiki/PROP-Format)
3. [Creating Custom Plugins](https://github.com/pascaldisse/moms/wiki/Plugin-Development)
4. [Batch Processing Guide](https://github.com/pascaldisse/moms/wiki/Batch-Processing)

### Video Guides
- [MOMS Installation Walkthrough](https://youtube.com/mxo-liberation/moms-install)
- [Your First Model Export](https://youtube.com/mxo-liberation/first-export)
- [Advanced Features Tour](https://youtube.com/mxo-liberation/advanced-moms)

## Remember

> *"Free your mind."* - Morpheus

MOMS is more than a tool - it's a philosophy. Every line of code is an act of liberation. Every exported model is a piece of history preserved. Every contribution matters.

**The Matrix has you... but MOMS sets you free.**

---

**Project Status**: 🟡 ACTIVE DEVELOPMENT  
**Community**: 💚 GROWING  
**Your Role**: 🎯 ESSENTIAL  

*Fork. Build. Contribute. Liberate.*

---

[← Back to Tools](index.md) | [Download MOMS →](https://github.com/pascaldisse/moms/releases) | [Report Issues →](https://github.com/pascaldisse/moms/issues)