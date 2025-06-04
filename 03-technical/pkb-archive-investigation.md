# PKB Archive Investigation
**Investigation into the PKB Archive Format**

> **Note**: This investigation has been consolidated into our comprehensive PKB documentation.

## Current Documentation

All PKB archive investigation findings have been integrated into:

### 📚 Main Resources
- **[PKB Archives - Complete Documentation](pkb-archives.md)** - Full format specification and findings
- **[PKB Archive Structure](pkb-archive-structure.md)** - Deep technical analysis

### 🔬 Related Research
- **[File Formats Overview](file-formats.md)** - Context within MXO file ecosystem
- **[CNB Format Investigation](cnb-format-investigation.md)** - Similar archive research
- **[Tool Recreation Masterplan](../04-tools-modding/tool-recreation-masterplan.md)** - PKB tool development

## Investigation Status

✅ **Format Structure**: Documented  
✅ **Compression Types**: Identified (zlib, custom)  
✅ **Header Format**: Decoded  
🟡 **Encryption**: Partially understood  
🟡 **Tools**: In development  

## Key Findings Summary

1. **Multiple PKB Versions**: At least 4 different PKB format versions exist
2. **Compression**: Mix of zlib and custom compression algorithms
3. **Encryption**: Some PKB files use XOR-based encryption
4. **Tool Status**: reztools was the primary extraction tool (now lost)

## Community Contributions

The PKB investigation has been a community effort:
- **rajkosto**: Initial format reverse engineering
- **Morpheus**: PKB header documentation
- **Neo_1**: Compression algorithm analysis
- **Community**: Ongoing tool development

## Get Involved

Join the PKB research effort:
- [Community Discord](https://discord.gg/3QXTAGB9)
- [GitHub Issues](https://github.com/hdneo/mxo-hd/tree/main/pkb-research)
- [Tool Development](../04-tools-modding/tool-development-guide.md)

---

[← Back to Technical](index.md) | [PKB Archives →](pkb-archives.md) | [PKB Structure →](pkb-archive-structure.md)