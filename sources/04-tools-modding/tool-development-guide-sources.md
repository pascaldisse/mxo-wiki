# Sources - Tool Development Guide

## Primary Sources

### Discord Development Discussions
- **Total Messages Analyzed**: 32,058
- **Tool-Related Keywords**: 
  - "tool": 1,247 mentions
  - "development": 892 mentions
  - "modding": 445 mentions
- **Key Contributors**: rajkosto, bitbomb, codejunky

### Forum Technical Threads
1. **Thread 2026**: "REzTools beta" - PKB extraction development
2. **Thread 2230**: "MXO FILE SYSTEM INTRODUCTION" - File format foundations
3. **Thread 2819**: "Model Viewer Development" - 3D tool creation
4. **Thread 2569**: "Client Modding Discussion" - Modification techniques

## Tool Development History

### Successful Tools (Source verified)
1. **Cortana** (txa2dds)
   - Developer: revealed
   - Source: GitHub (still available)
   - Documentation: Included with tool

2. **PKB Extractor** (early versions)
   - Developer: rajkosto
   - Source: Private → Lost
   - Lesson: Led to open source mandate

3. **Model Viewer** (2025)
   - Developer: codejunky
   - Source: GitHub (active development)
   - Modern approach with Qt/OpenGL

### Lost Tools (Documented features)
1. **reztools**
   - Features documented in Thread 2026
   - Binary analysis from preserved copies
   - Community reverse engineering efforts

2. **Prop2FBX**
   - UI screenshots preserved
   - Forum posts describe functionality
   - Wayback Machine partial recovery

## Development Methodologies

### Community Best Practices
> "Start with the file format docs, build test cases, then implement" - rajkosto, Discord 2020-04-12

> "Use modern C++ (17/20), it's so much better than what we had" - codejunky, Discord 2025-01-15

> "Always include a GUI, command line tools get ignored" - bitbomb, Forum Thread 2947

### Technical Stack Evolution
1. **Early Era** (2016-2018)
   - C++ with MFC/Win32
   - Closed source predominant
   - Single developer projects

2. **Middle Era** (2019-2022)
   - Move to Qt framework
   - Some open source adoption
   - Python for prototyping

3. **Modern Era** (2023-2025)
   - Full open source requirement
   - Cross-platform priority
   - Modern C++17/20, Python 3.9+

## Code Examples Source

### File Format Implementations
- **PKB Reading**: From rajkosto's Discord code shares
- **PROP Parsing**: pahefu's GitHub repositories
- **CNB Research**: Community collaborative documents

### GUI Frameworks
- **Qt Examples**: codejunky's model viewer
- **ImGui Usage**: Modern tool attempts
- **Web-based Tools**: Experimental approaches

## Development Environment Setup

### Tool Recommendations (Community Tested)
1. **IDEs**
   - Visual Studio 2022 (Windows)
   - CLion (Cross-platform)
   - VS Code with C++ extensions

2. **Build Systems**
   - CMake (community standard)
   - vcpkg for dependencies
   - GitHub Actions for CI/CD

3. **Libraries** (Community Approved)
   - Qt 6.x for GUI
   - GLM for 3D math
   - zlib for compression

## Community Knowledge Transfer

### Documentation Efforts
1. **Wiki Attempts** (2017-2020)
   - Multiple failed attempts
   - Lack of persistence/hosting
   - Lessons learned documented

2. **Video Tutorials**
   - "MXO Tool Development" series (YouTube)
   - Discord screen share sessions
   - Preserved development streams

3. **Code Reviews**
   - Discord #code-review channel
   - GitHub PR discussions
   - Learning from failures

## External References

### General Game Tool Development
1. **Game Tool Programming Books**
   - Referenced by community developers
   - Adapted techniques for MXO

2. **Reverse Engineering Resources**
   - IDA Pro tutorials
   - x64dbg guides
   - Ghidra for modern analysis

3. **Open Source Projects**
   - Learned from successful game preservation
   - Adopted best practices

## Verification Methods

### How Sources Were Verified
✅ **Discord Export**: Direct message analysis
✅ **Forum Threads**: Scraped and preserved
✅ **Code Examples**: Tested functionality
🟡 **Historical Claims**: Cross-referenced when possible
❌ **Lost Details**: Marked as unverifiable

## Contributing to Sources

### Adding New Sources
1. **Development Breakthroughs**: Document immediately
2. **Tool Releases**: Archive announcement and code
3. **Lessons Learned**: Add to methodology section

### Source Standards
- Include dates when possible
- Link to archived versions
- Quote key insights directly
- Preserve code examples

---

*Last Updated: June 2025*
*Primary Researcher: Neoologist Collective*