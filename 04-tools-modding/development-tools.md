# Development Tools for Matrix Online
**The Developer's Arsenal**

> *"There is no spoon... but there are development tools."*

Comprehensive guide to development tools, environments, and workflows for Matrix Online development. Essential resources for contributors working on emulation, modding, and tool creation.

## 🎯 Development Environment Setup

### Core Development Stack

#### Essential Tools
```bash
# Version control
git --version
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Text editors and IDEs
code --version  # Visual Studio Code
vim --version   # Vim for server editing
nano --version  # Simple file editing
```

#### Programming Languages
```bash
# C++ (for engine modifications)
g++ --version
clang++ --version

# C# (for server development)
dotnet --version
mono --version

# Python (for tools and automation)
python3 --version
pip3 --version

# JavaScript/Node.js (for web tools)
node --version
npm --version
```

#### Build Systems
```bash
# Make for C/C++ projects
make --version

# CMake for cross-platform builds
cmake --version

# MSBuild for .NET projects (Windows)
msbuild --version

# Gradle for Java projects
gradle --version
```

### Development Dependencies

#### Graphics and File Format Libraries
```bash
# OpenGL development
sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev

# Image processing
sudo apt-get install libpng-dev libjpeg-dev

# 3D graphics libraries
sudo apt-get install libglew-dev libglfw3-dev

# Audio libraries
sudo apt-get install libopenal-dev libvorbis-dev
```

#### Database Development
```bash
# MySQL development headers
sudo apt-get install libmysqlclient-dev

# SQLite for lightweight databases
sudo apt-get install libsqlite3-dev

# Database administration tools
sudo apt-get install mysql-workbench
```

#### Network Development
```bash
# Network libraries
sudo apt-get install libssl-dev libcurl4-openssl-dev

# Protocol analysis
sudo apt-get install wireshark tshark

# Network testing
sudo apt-get install netcat-openbsd nmap
```

## 🔧 Specialized MXO Tools

### File Format Analysis

#### Hex Editors
```bash
# Command line hex editing
hexdump -C file.dat | head -20
xxd file.dat | head -20

# GUI hex editors
sudo apt-get install ghex    # GNOME hex editor
sudo apt-get install bless   # Advanced hex editor
```

#### Binary Analysis
```bash
# File type identification
file *.dat
strings file.dat | grep -i "matrix\|mxo"

# Binary comparison
diff <(hexdump -C file1.dat) <(hexdump -C file2.dat)

# Structure analysis
readelf -h binary_file
objdump -h binary_file
```

#### Archive Extraction
```bash
# PKB archive tools (custom format)
python3 pkb_extractor.py archive.pkb

# Standard archive formats
unzip archive.zip
tar -xzf archive.tar.gz
7z x archive.7z
```

### Reverse Engineering Tools

#### Disassemblers
```bash
# IDA Pro (commercial, industry standard)
# https://hex-rays.com/ida-pro/

# Ghidra (free, NSA open source)
# https://ghidra-sre.org/

# Radare2 (free, command line)
sudo apt-get install radare2
r2 -A matrix.exe
```

#### Debuggers
```bash
# GDB for Linux debugging
gdb ./mxo_server
(gdb) break main
(gdb) run
(gdb) bt

# Valgrind for memory analysis
valgrind --leak-check=full ./mxo_server

# strace for system call tracing
strace -o trace.log ./mxo_server
```

#### Memory Analysis
```bash
# Process memory examination
pmap $(pgrep mxo_server)
cat /proc/$(pgrep mxo_server)/maps

# Memory dumping
gcore $(pgrep mxo_server)
strings core.* | grep -i matrix
```

### Network Analysis Tools

#### Packet Capture
```bash
# Wireshark (GUI)
wireshark &

# tcpdump (command line)
sudo tcpdump -i eth0 port 7000 -w mxo_traffic.pcap

# Analyze captured packets
tshark -r mxo_traffic.pcap -Y "tcp.port == 7000"
```

#### Protocol Analysis
```bash
# Custom MXO protocol dissector
# Create Wireshark plugin for MXO packets
mkdir ~/.local/lib/wireshark/plugins/
# Add custom dissector.lua

# Manual packet analysis
hexdump -C packet.bin
python3 mxo_packet_parser.py packet.bin
```

#### Network Testing
```bash
# Server connectivity testing
nc -zv server_ip 7000

# Bandwidth testing
iperf3 -c server_ip -p 7001

# Latency monitoring
ping -c 100 server_ip
mtr server_ip
```

## 🛠️ Development Workflows

### Version Control Best Practices

#### Git Workflow
```bash
# Feature development workflow
git checkout -b feature/cnb-viewer
git add -A
git commit -m "Add CNB file header parsing"
git push origin feature/cnb-viewer

# Create pull request
gh pr create --title "CNB Viewer: Initial Implementation"

# Code review and merge
git checkout main
git pull origin main
git branch -d feature/cnb-viewer
```

#### Branch Management
```bash
# Development branches
main          # Stable, deployable code
develop       # Integration branch
feature/*     # New features
hotfix/*      # Critical bug fixes
release/*     # Release preparation

# Example branch creation
git checkout -b feature/pkb-extractor
git checkout -b hotfix/login-crash
git checkout -b release/v1.2.0
```

### Code Quality Tools

#### Static Analysis
```bash
# C++ analysis
cppcheck --enable=all src/
clang-static-analyzer src/

# C# analysis
dotnet format --verify-no-changes
dotnet build --verbosity normal

# Python analysis
pylint *.py
flake8 *.py
black *.py
```

#### Testing Frameworks
```bash
# C++ testing
sudo apt-get install libgtest-dev
g++ -lgtest -lgtest_main test.cpp

# C# testing
dotnet test

# Python testing
python3 -m pytest tests/
python3 -m unittest discover
```

#### Documentation Generation
```bash
# Doxygen for C/C++
sudo apt-get install doxygen graphviz
doxygen Doxyfile

# Sphinx for Python
pip3 install sphinx
sphinx-quickstart
make html
```

### Build Automation

#### Continuous Integration
```yaml
# GitHub Actions workflow (.github/workflows/build.yml)
name: Build and Test
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Build Environment
        run: |
          sudo apt-get update
          sudo apt-get install build-essential
      - name: Build Project
        run: make all
      - name: Run Tests
        run: make test
```

#### Local Build Scripts
```bash
#!/bin/bash
# build.sh - Local build script

set -e

echo "Building Matrix Online Tools..."

# Clean previous builds
make clean

# Configure build
cmake -DCMAKE_BUILD_TYPE=Release .

# Build project
make -j$(nproc)

# Run tests
make test

echo "Build completed successfully!"
```

### Debugging Workflows

#### Debug Build Configuration
```bash
# Debug flags for C/C++
CFLAGS="-g -O0 -DDEBUG -Wall -Wextra"
CXXFLAGS="-g -O0 -DDEBUG -Wall -Wextra -std=c++17"

# Debug build with CMake
cmake -DCMAKE_BUILD_TYPE=Debug .
make
```

#### Debugging Techniques
```bash
# GDB debugging session
gdb ./mxo_tool
(gdb) set args input.dat output.dat
(gdb) break parse_cnb_file
(gdb) run
(gdb) print variable_name
(gdb) step
(gdb) continue
```

#### Memory Debugging
```bash
# Valgrind memory check
valgrind --tool=memcheck --leak-check=full ./mxo_tool

# AddressSanitizer (compile-time option)
g++ -fsanitize=address -g -o mxo_tool src/*.cpp

# Memory profiling
valgrind --tool=massif ./mxo_tool
ms_print massif.out.*
```

## 📊 Performance Analysis Tools

### Profiling

#### CPU Profiling
```bash
# GNU gprof
g++ -pg -o mxo_tool src/*.cpp
./mxo_tool
gprof mxo_tool gmon.out > profile.txt

# Perf profiling
perf record -g ./mxo_tool
perf report

# Sampling profiler
sudo apt-get install linux-tools-common
perf top -p $(pgrep mxo_tool)
```

#### Memory Profiling
```bash
# Valgrind massif
valgrind --tool=massif ./mxo_tool
ms_print massif.out.* > memory_profile.txt

# Memory usage monitoring
ps aux | grep mxo_tool
top -p $(pgrep mxo_tool)
```

#### I/O Profiling
```bash
# I/O monitoring
iostat -x 1 10
iotop -p $(pgrep mxo_tool)

# File access tracing
strace -e trace=file ./mxo_tool
```

### Benchmarking

#### Performance Testing
```bash
# Time measurement
time ./mxo_tool large_file.dat

# Detailed timing
/usr/bin/time -v ./mxo_tool large_file.dat

# Custom benchmarking
hyperfine './mxo_tool input.dat' './competitor_tool input.dat'
```

#### Load Testing
```bash
# Multiple instances
for i in {1..10}; do
    ./mxo_tool test_$i.dat &
done
wait

# Stress testing
stress --cpu 4 --timeout 60s
stress --vm 2 --vm-bytes 1G --timeout 60s
```

## 🔬 Specialized Development Areas

### CNB Viewer Development

#### 3D Graphics Setup
```bash
# OpenGL development environment
sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev libglew-dev

# GLFW for window management
sudo apt-get install libglfw3-dev

# Graphics debugging
sudo apt-get install apitrace
apitrace trace ./cnb_viewer
qapitrace trace.trace
```

#### 3D Model Parsing
```cpp
// Example CNB header parsing
struct CNBHeader {
    uint32_t magic;      // File magic number
    uint32_t version;    // Format version
    uint32_t num_scenes; // Number of scenes
    uint32_t data_offset; // Offset to scene data
};

// Parse CNB file
bool parse_cnb_file(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    CNBHeader header;
    file.read(reinterpret_cast<char*>(&header), sizeof(header));
    
    if (header.magic != 0x424E43) { // "CNB"
        return false;
    }
    
    // Continue parsing...
    return true;
}
```

### PKB Archive Tools

#### Archive Structure Analysis
```python
# PKB archive parser example
import struct

def parse_pkb_header(data):
    # PKB header structure (hypothetical)
    magic, version, num_files, index_offset = struct.unpack('<4sIII', data[:16])
    
    if magic != b'PKB\x00':
        raise ValueError("Invalid PKB magic")
    
    return {
        'version': version,
        'num_files': num_files,
        'index_offset': index_offset
    }

def extract_pkb_files(pkb_path, output_dir):
    with open(pkb_path, 'rb') as f:
        header = parse_pkb_header(f.read(16))
        # Continue extraction...
```

#### File System Integration
```bash
# FUSE filesystem for PKB archives
sudo apt-get install libfuse-dev

# Mount PKB as filesystem
./pkb_fuse archive.pkb /mnt/pkb/
ls /mnt/pkb/
fusermount -u /mnt/pkb/
```

### Server Development

#### Database Schema Tools
```sql
-- Database migration system
CREATE TABLE schema_versions (
    version INT PRIMARY KEY,
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- Character data validation
SELECT c.* FROM characters c
LEFT JOIN accounts a ON c.account_id = a.id
WHERE a.id IS NULL;
```

#### API Development
```bash
# REST API testing
curl -X GET http://localhost:8080/api/characters/123
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"TestChar","level":1}' \
     http://localhost:8080/api/characters

# API documentation
sudo npm install -g swagger-ui-serve
swagger-ui-serve api-docs.yaml
```

## 🤝 Collaboration Tools

### Code Review

#### Pull Request Workflow
```bash
# Create feature branch
git checkout -b feature/improvement

# Make changes and commit
git add -A
git commit -m "Implement CNB parsing improvement"

# Push and create PR
git push origin feature/improvement
gh pr create --title "CNB Parser: Add error handling"
```

#### Code Review Tools
- **GitHub**: Built-in pull request reviews
- **GitLab**: Merge request system
- **Gerrit**: Advanced code review platform
- **Review Board**: Standalone review tool

### Communication

#### Development Communication
- **Discord**: Real-time chat and voice communication
- **Slack**: Team communication and integration
- **IRC**: Traditional developer communication
- **Matrix**: Decentralized communication platform

#### Documentation Platforms
- **Wiki**: Collaborative documentation editing
- **Confluence**: Enterprise documentation platform
- **GitBook**: Modern documentation platform
- **Notion**: All-in-one workspace

### Project Management

#### Issue Tracking
```bash
# GitHub Issues
gh issue create --title "CNB Viewer crashes on large files"
gh issue list --state open

# Issue templates
.github/ISSUE_TEMPLATE/bug_report.md
.github/ISSUE_TEMPLATE/feature_request.md
```

#### Project Planning
- **GitHub Projects**: Kanban boards and project tracking
- **Jira**: Advanced project management
- **Trello**: Simple kanban-style project management
- **Linear**: Modern issue tracking and project management

## 📚 Learning Resources

### Documentation

#### Official References
- **C++ Reference**: https://en.cppreference.com/
- **OpenGL Documentation**: https://docs.gl/
- **Git Documentation**: https://git-scm.com/docs
- **CMake Tutorial**: https://cmake.org/cmake/help/latest/guide/tutorial/

#### Matrix Online Specific
- **File Format Documentation**: [Technical Docs](../03-technical/index.md)
- **Server Architecture**: [Server Architecture](../03-technical/server-architecture.md)
- **Tool Development Guide**: [Tool Development](tool-development-guide.md)

### Community Resources

#### Development Communities
- **Matrix Online Discord**: Real-time development discussion
- **GitHub Discussions**: Asynchronous development topics
- **Reddit Communities**: r/gamedev, r/emulation
- **Stack Overflow**: Programming questions and answers

#### Learning Platforms
- **GitHub Learning Lab**: Interactive Git and development courses
- **FreeCodeCamp**: Free programming education
- **Coursera**: University-level computer science courses
- **Udemy**: Practical development skills courses

---

## 🌟 Developer Achievement Unlocked

You've mastered the Matrix Online development toolkit! You now have:
- ✅ **Complete Development Environment** - All tools configured and ready
- ✅ **Workflow Mastery** - Efficient development and collaboration processes
- ✅ **Debugging Skills** - Advanced troubleshooting and analysis capabilities
- ✅ **Performance Optimization** - Profiling and optimization techniques
- ✅ **Collaboration Knowledge** - Team development best practices

**Welcome to the Matrix development matrix. You're ready to build the future.**

---

[← Back to AI-Assisted Development](ai-assisted-development-mxo.md) | [Automation Scripts →](automation-scripts.md) | [Tool Development Guide →](tool-development-guide.md)

📚 [View Sources](../sources/04-tools-modding/development-tools-sources.md)