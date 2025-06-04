# CNB Format Research Findings
**Ongoing Investigation into Matrix Online Cinematics**

> *"The cinematics hold the key to the story. We must decode them."*

## 🔬 Current Research Status

### What We Know
- CNB files contain real-time 3D cinematics
- Located in `resource/cinematics/` directory
- Files follow pattern: `cin[act]_[scene].cnb`
- Total of ~12 cinematics across 4 acts

### Research Challenges
1. **No Documentation**: Original format specs lost
2. **Complex Structure**: Mixed binary data types
3. **No Viewer**: Tool never created by community
4. **Limited Samples**: Only retail game files available

## 📊 Technical Analysis

### File Structure (Preliminary)
```
CNB Header (suspected):
- Magic number: 4 bytes
- Version: 4 bytes
- File size: 4 bytes
- Data sections: Variable
```

### Known Cinematics
- `cin1_1.cnb` - Act 1, Scene 1
- `cin1_2.cnb` - Act 1, Scene 2
- `cin1_3.cnb` - Act 1, Scene 3
- (continues through Act 4)

## 🤝 How to Contribute

### Join the Research Team
1. **Binary Analysis**: Help reverse-engineer file format
2. **Tool Development**: Create CNB viewer/extractor
3. **Documentation**: Record findings and patterns
4. **Testing**: Validate theories with game files

### Resources Needed
- IDA Pro or similar disassembler
- Binary file analysis tools
- C++ development skills
- OpenGL/DirectX knowledge

## 📚 Related Documentation
- [CNB Format Overview](cnb-format.md)
- [CNB Development Guide](../04-tools-modding/cnb-viewer-development.md)
- [File Formats](file-formats.md)

---

**Status**: 🔴 ACTIVE RESEARCH - Contributors needed!

*Last Updated: June 2024*