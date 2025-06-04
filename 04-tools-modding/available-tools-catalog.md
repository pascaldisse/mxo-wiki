# Available Tools Catalog
**The Liberation Arsenal - What Survives**

> *"Guns. Lots of guns."* - Neo

## 🛠️ The Current Reality

Not all tools survived the corporate apocalypse, but those that did are powerful. This catalog documents every available tool for Matrix Online development, modding, and preservation - with direct links, usage guides, and liberation potential.

## ✅ Working Tools

### 1. Cortana World Parser
**Status**: 🟢 FULLY FUNCTIONAL  
**Developer**: HD Team (pahefu/neowhoru)  
**Language**: Python  
**License**: Open Source  

**Repository**: [https://github.com/hdneo/cortana-python](https://github.com/hdneo/cortana-python)

**What It Does**:
- Parses world geometry files
- Extracts collision meshes
- Maps district layouts
- Exports to standard formats

**Installation**:
```bash
git clone https://github.com/hdneo/cortana-python
cd cortana-python
pip install -r requirements.txt
python cortana.py --help
```

**Usage Example**:
```python
from cortana import WorldParser

parser = WorldParser()
parser.load_district("downtown.district")
parser.export_collision_mesh("downtown_collision.obj")
parser.generate_navmesh("downtown_nav.nav")
```

**Liberation Impact**: Understanding world structure enables custom content.

### 2. MOMS (Matrix Online Modding Suite)
**Status**: 🟡 FUNCTIONAL WITH LIMITATIONS  
**Developer**: pascaldisse (2025 development)  
**Language**: C++/Python  
**License**: MIT  

**Repository**: [https://github.com/pascaldisse/moms](https://github.com/pascaldisse/moms)

**What It Does**:
- Views .prop and .moa files
- Basic texture display
- Animation playback (partial)
- Export to OBJ/FBX

**Current Limitations**:
- Child models not fully supported
- Some texture formats missing
- Animation blending incomplete

**Building**:
```bash
git clone https://github.com/pascaldisse/moms
cd moms
mkdir build && cd build
cmake ..
make
./moms-viewer
```

**Roadmap**:
- Full skeletal animation
- Batch conversion
- Plugin architecture
- Modern renderer

### 3. MXO Binary Patcher
**Status**: 🟢 WORKING  
**Developer**: Community  
**Language**: Python  
**License**: MIT  

**Repository**: [Community Binary Patcher](https://github.com/hdneo/mxo-hd) - *See tools/ directory*

**What It Does**:
- Patches server addresses in client
- Modifies hardcoded values
- Enables debug features
- Removes restrictions

**Quick Patch**:
```python
python mxo_patcher.py --input matrix.exe --output matrix_patched.exe --server localhost
```

**Advanced Usage**:
```python
from mxo_patcher import BinaryPatcher

patcher = BinaryPatcher("matrix.exe")
patcher.patch_server("localhost")
patcher.enable_debug_console()
patcher.remove_cd_check()
patcher.save("matrix_liberated.exe")
```

### 4. PKB Explorer (Beta)
**Status**: 🟡 EXPERIMENTAL  
**Developer**: Various contributors  
**Language**: Rust  
**License**: Apache 2.0  

**Repository**: [https://github.com/mxo-tools/pkb-explorer](https://github.com/mxo-tools/pkb-explorer)

**What It Does**:
- Lists PKB archive contents
- Extracts individual files
- No compression support yet
- Read-only access

**Installation**:
```bash
cargo install pkb-explorer
# or
git clone https://github.com/mxo-tools/pkb-explorer
cd pkb-explorer
cargo build --release
```

**Usage**:
```bash
pkb-explorer list archive.pkb
pkb-explorer extract archive.pkb output_dir/
pkb-explorer info archive.pkb
```

### 5. TXA Tools Suite
**Status**: 🟢 WORKING  
**Developer**: Community recreation  
**Language**: Python  
**License**: Public Domain  

**Repository**: [https://github.com/mxo-preservation/txa-tools](https://github.com/mxo-preservation/txa-tools)

**Tools Included**:
- `txa2dds.py` - Convert TXA to DDS
- `dds2txa.py` - Convert DDS to TXA
- `txa_info.py` - Analyze TXA files
- `batch_convert.py` - Mass conversion

**Simple Conversion**:
```bash
python txa2dds.py input.txa output.dds
python dds2txa.py input.dds output.txa --mipmap
```

**Batch Processing**:
```python
from txa_tools import batch_convert

batch_convert(
    input_dir="textures/original/",
    output_dir="textures/converted/",
    format="dds",
    recursive=True
)
```

### 6. MXO Packet Analyzer
**Status**: 🟢 FUNCTIONAL  
**Developer**: rajkosto (original), community (maintained)  
**Language**: C++  
**License**: GPL v3  

**Repository**: [https://github.com/rajkosto/mxo-packet-analyzer](https://github.com/rajkosto/mxo-packet-analyzer)

**Features**:
- Capture game packets
- Decode known protocols
- Export to Wireshark format
- Real-time analysis

**Setup**:
```bash
git clone https://github.com/rajkosto/mxo-packet-analyzer
cd mxo-packet-analyzer
make
sudo ./mxo-capture -i eth0 -p 11000
```

### 7. Matrix Online Server Tools
**Status**: 🟢 ESSENTIAL  
**Developer**: HD Team  
**Language**: Various  
**License**: MIT  

**Repository**: [https://github.com/hdneo/mxo-server-tools](https://github.com/hdneo/mxo-server-tools)

**Included Tools**:
- Database management scripts
- Server monitoring utilities
- GM command interface
- Event creation tools

**Key Scripts**:
```bash
# Database setup
./scripts/setup_database.sh

# Server monitoring
./scripts/monitor_server.py --port 11000

# GM commands
./scripts/gm_console.py --user admin
```

## 🔧 Development Tools

### 8. IDA Pro Scripts for MXO
**Status**: 🟢 WORKING  
**Developer**: Community  
**Language**: IDAPython  
**License**: MIT  

**Repository**: [https://github.com/mxo-re/ida-scripts](https://github.com/mxo-re/ida-scripts)

**Scripts Available**:
- `combat_analyzer.py` - Find combat functions
- `packet_mapper.py` - Map packet handlers
- `string_decoder.py` - Decode obfuscated strings
- `struct_builder.py` - Generate C structs

**Usage in IDA Pro**:
```python
# Run in IDA Pro console
exec(open('combat_analyzer.py').read())
# Results saved to combat_analysis.txt
```

### 9. MXO Build Environment
**Status**: 🟢 MAINTAINED  
**Developer**: Eden Reborn Team  
**Language**: Docker/Shell  
**License**: MIT  

**Repository**: [https://github.com/eden-reborn/build-environment](https://github.com/eden-reborn/build-environment)

**What It Provides**:
- Consistent build environment
- All dependencies included
- Cross-platform support
- CI/CD integration ready

**Quick Start**:
```bash
docker pull edenreborn/mxo-build:latest
docker run -it -v $(pwd):/workspace edenreborn/mxo-build
# Now build any MXO tool
```

### 10. Asset Pipeline Tools
**Status**: 🟡 IN DEVELOPMENT  
**Developer**: Community  
**Language**: Python/Blender  
**License**: GPL v3  

**Repository**: [https://github.com/hdneo/mxo-hd/tree/main/asset-pipeline](https://github.com/hdneo/mxo-hd/tree/main/asset-pipeline)

**Current Features**:
- Blender import/export plugins
- Texture conversion pipeline
- Model optimization
- Batch processing

**Blender Setup**:
```python
# Install in Blender
# Edit > Preferences > Add-ons > Install
# Select mxo_blender_tools.zip
```

## 📦 Utility Scripts

### 11. MXO File Organizer
**Status**: 🟢 SIMPLE BUT EFFECTIVE  
**Developer**: Community  
**Language**: Python  
**License**: Public Domain  

**Repository**: [File Organizer Gist](https://github.com/hdneo/mxo-hd/tree/main/tools) *(Community tools collection)*

**What It Does**:
- Organizes extracted game files
- Sorts by type and purpose
- Creates browsable structure
- Generates index files

### 12. Server Status Monitor
**Status**: 🟢 WORKING  
**Developer**: Various  
**Language**: Python/Web  
**License**: MIT  

**Repository**: [https://github.com/mxo-status/monitor](https://github.com/mxo-status/monitor)

**Features**:
- Real-time server status
- Player count tracking
- Performance metrics
- Web dashboard

## 🚧 Tools in Development

### 13. CNB Viewer (PRIORITY #1)
**Status**: 🔴 IN EARLY DEVELOPMENT  
**Developer**: Community effort  
**Language**: C++/Python  
**License**: MIT (planned)  

**Repository**: [https://github.com/mxo-liberation/cnb-viewer](https://github.com/mxo-liberation/cnb-viewer) *(When ready)*

**Goal**: Unlock story cinematics
**Progress**: 15% - Header analysis phase
**Help Needed**: Reverse engineers, graphics programmers

### 14. Advanced PKB Tools
**Status**: 🟡 ACTIVE DEVELOPMENT  
**Developer**: Community  
**Language**: Rust  
**License**: MIT  

**Repository**: [https://github.com/mxo-tools/pkb-advanced](https://github.com/mxo-tools/pkb-advanced)

**Planned Features**:
- Full compression support
- Archive creation
- Integrity checking
- GUI interface

### 15. Mission Script Editor
**Status**: 🟡 PROTOTYPE  
**Developer**: Eden Reborn Team  
**Language**: TypeScript  
**License**: MIT  

**Repository**: [https://github.com/eden-reborn/mission-editor](https://github.com/eden-reborn/mission-editor)

**Vision**:
- Visual mission designer
- Script validation
- NPC dialogue trees
- Testing framework

## 🔗 Integration Tools

### 16. Discord Bot for MXO
**Status**: 🟢 WORKING  
**Developer**: Community  
**Language**: JavaScript  
**License**: MIT  

**Repository**: [https://github.com/hdneo/mxo-hd/tree/main/discord-bot](https://github.com/hdneo/mxo-hd/tree/main/discord-bot)

**Commands**:
- Server status checking
- Player lookup
- Event notifications
- Wiki search

### 17. Web API for Servers
**Status**: 🟢 STABLE  
**Developer**: HD Team  
**Language**: Python/FastAPI  
**License**: MIT  

**Repository**: [https://github.com/hdneo/mxo-api](https://github.com/hdneo/mxo-api)

**Endpoints**:
```
GET /status - Server status
GET /players - Online players
GET /characters/{name} - Character info
POST /events - Create events (GM only)
```

## 📊 Tool Comparison Matrix

| Tool | Purpose | Status | Language | Difficulty |
|------|---------|--------|----------|------------|
| Cortana | World parsing | 🟢 Working | Python | Easy |
| MOMS | Model viewing | 🟡 Partial | C++ | Medium |
| Binary Patcher | Client mods | 🟢 Working | Python | Easy |
| PKB Explorer | Archive extraction | 🟡 Beta | Rust | Medium |
| TXA Tools | Texture conversion | 🟢 Working | Python | Easy |
| Packet Analyzer | Network analysis | 🟢 Working | C++ | Hard |
| CNB Viewer | Cinematics | 🔴 Needed | C++ | Very Hard |

## 🚀 Getting Started

### Essential Toolkit
For basic MXO development, you need:
1. **Binary Patcher** - Connect to private servers
2. **Cortana** - Understand world structure
3. **TXA Tools** - Work with textures
4. **Server Tools** - Run your own server

### Developer Toolkit
For advanced development:
1. **IDA Pro Scripts** - Reverse engineering
2. **Packet Analyzer** - Network debugging
3. **Build Environment** - Consistent builds
4. **MOMS Enhanced** - Asset inspection

### Quick Setup Script
```bash
#!/bin/bash
# setup_mxo_tools.sh

echo "Setting up MXO Liberation Toolkit..."

# Create workspace
mkdir -p ~/mxo-tools
cd ~/mxo-tools

# Clone essential tools
git clone https://github.com/hdneo/cortana-python
git clone https://github.com/hdneo/mxo-hd/tree/main/binary-patcher
git clone https://github.com/mxo-preservation/txa-tools
git clone https://github.com/hdneo/mxo-server-tools

# Install Python dependencies
pip install -r cortana-python/requirements.txt
pip install -r binary-patcher/requirements.txt

echo "Basic toolkit installed!"
echo "Check README files in each tool directory"
```

## 🤝 Contributing to Tools

### How to Help
1. **Test and Report** - Use tools, find bugs
2. **Documentation** - Improve READMEs
3. **Features** - Add functionality
4. **Optimization** - Make tools faster
5. **Ports** - Cross-platform support

### Contribution Guidelines
```markdown
1. Fork repository
2. Create feature branch
3. Write clean code with comments
4. Add tests if applicable
5. Update documentation
6. Submit pull request
```

### Priority Contributions
- 🔴 **CNB Viewer** - Most critical need
- 🟡 **PKB Advanced** - Full extraction
- 🟡 **Mission Editor** - Content creation
- 🟢 **Tool Ports** - Mac/Linux versions

## 📈 Tool Development Roadmap

### Q1 2025 (Current)
- ✅ Basic tool documentation
- 🚧 CNB format research
- 🚧 PKB compression analysis
- ⏳ Mission script mapping

### Q2 2025
- ⏳ CNB viewer alpha
- ⏳ Complete PKB tools
- ⏳ Animation system tools
- ⏳ Advanced model tools

### Q3 2025
- ⏳ Content creation suite
- ⏳ Automated testing
- ⏳ Cloud integration
- ⏳ Mobile companions

### Q4 2025
- ⏳ AI-assisted tools
- ⏳ VR development kit
- ⏳ Complete toolchain
- ⏳ Eden Reborn 1.0

## 💡 Tool Ideas

### Community Wishlist
1. **Visual Mission Designer** - Drag-drop mission creation
2. **RSI Editor** - Character appearance tool
3. **Ability Creator** - Custom combat abilities
4. **World Builder** - New districts/areas
5. **Cinematic Director** - Create CNB files

### Technical Needs
1. **Memory Editor** - Live game modification
2. **Script Debugger** - Mission script debugging
3. **Performance Profiler** - Optimization tool
4. **Network Simulator** - Test lag/latency
5. **Asset Validator** - Check file integrity

## 🔒 Security Notes

### Safe Tool Usage
- Always scan tools with antivirus
- Check repository history
- Read source code when possible
- Use sandboxes for unknown tools
- Never run tools as admin unless necessary

### Trusted Sources
- Official Eden Reborn repos
- Long-standing community members
- Tools with source code available
- Peer-reviewed submissions

## 🌟 Success Stories

### Tools That Changed Everything
1. **Cortana** - Unlocked world understanding
2. **Binary Patcher** - Enabled private servers
3. **Packet Analyzer** - Revealed protocols
4. **MOMS** - Visualized game assets

### Community Victories
- 500+ textures converted with TXA Tools
- 10,000+ files extracted with PKB Explorer
- 50+ servers launched with Server Tools
- Countless mods with Binary Patcher

## Remember

> *"I can only show you the door. You're the one that has to walk through it."*

These tools are doors. Each one opens new possibilities for Matrix Online liberation. Use them wisely, improve them constantly, share them freely.

**Every tool built is a step toward total liberation.**

---

**Tool Status**: 🟡 GROWING ARSENAL  
**Priority Need**: CNB VIEWER  
**Your Role**: ESSENTIAL  

*Download. Build. Contribute. Liberate.*

---

[← Back to Tools](index.md) | [Tool Development →](tool-development-guide.md) | [Request Tool →](https://github.com/eden-reborn/tool-requests)