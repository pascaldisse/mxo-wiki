# IDA Pro Scripts for Matrix Online - Overview
**Reverse Engineering Toolkit**

> *"The Matrix is a system, Neo."* - These scripts help us understand that system.

## 🎯 Quick Start

This guide introduces IDA Pro scripts for Matrix Online reverse engineering. IDA Pro is a disassembler that helps analyze binary files.

### What You'll Learn
- Basic script concepts
- Common analysis patterns
- Matrix Online specific techniques
- How to get started

## 📚 Script Categories

### 1. [Function Analysis Scripts](ida-pro-function-analysis.md)
Scripts that identify and categorize functions:
- Combat system functions
- Network packet handlers
- File format parsers
- Memory management

### 2. [Pattern Recognition Scripts](ida-pro-pattern-recognition.md)
Automated pattern detection:
- String decoding algorithms
- Encryption routines
- Data structures
- Protocol patterns

### 3. [Data Extraction Scripts](ida-pro-data-extraction.md)
Extract game data from binaries:
- Combat strings and formulas
- Item definitions
- Mission parameters
- Network protocols

### 4. [Advanced Analysis Scripts](ida-pro-advanced-scripts.md)
Complex analysis techniques:
- AI-enhanced classification
- Dynamic API monitoring
- Security vulnerability scanning
- Performance profiling

## 🚀 Getting Started

### Prerequisites
1. **IDA Pro** (version 7.0 or higher)
2. **Python** support enabled
3. **Matrix Online** client files
4. Basic reverse engineering knowledge

### Your First Script
Here's a simple script to find combat-related functions:

```python
# find_combat_functions.py
import idaapi
import idautils
import idc

def find_combat_strings():
    """Find all combat-related strings"""
    combat_keywords = [
        "damage", "attack", "defend", 
        "interlock", "accuracy", "critical"
    ]
    
    results = []
    
    # Search all strings
    for string in idautils.Strings():
        str_value = str(string).lower()
        
        # Check for combat keywords
        for keyword in combat_keywords:
            if keyword in str_value:
                results.append({
                    'address': string.ea,
                    'string': str(string),
                    'keyword': keyword
                })
                break
    
    return results

# Run the search
print("Searching for combat strings...")
combat_strings = find_combat_strings()

print(f"Found {len(combat_strings)} combat-related strings:")
for result in combat_strings[:10]:  # Show first 10
    print(f"  {hex(result['address'])}: {result['string']}")
```

### Running Scripts
1. Open Matrix Online executable in IDA Pro
2. Wait for initial analysis to complete
3. Go to File → Script File
4. Select your Python script
5. View results in output window

## 📖 Understanding Results

### Function Names
IDA Pro uses naming conventions:
- `sub_XXXXXX` - Unnamed functions
- `loc_XXXXXX` - Code locations
- Custom names you assign

### Address Format
- `0x00401000` - Virtual memory address
- `401000h` - IDA's hex notation
- `.text:00401000` - Section and offset

## 🎯 Matrix Online Specifics

### Key Areas to Analyze
1. **Combat System** - Functions handling damage calculations
2. **Network Code** - Packet handlers and protocols
3. **File Loaders** - PKB, CNB, PROP format handlers
4. **Game Logic** - Mission systems, inventory, abilities

### Known Patterns
Matrix Online uses several recognizable patterns:
- D100 combat rolls (1-100 random numbers)
- Interlock state machines
- Ability effect chains
- Network packet structures

## 🛠️ Common Tasks

### Find String References
```python
def find_string_refs(search_string):
    """Find all references to a string"""
    refs = []
    
    for string in idautils.Strings():
        if search_string in str(string):
            # Get cross-references
            for ref in idautils.XrefsTo(string.ea):
                refs.append(ref.frm)
    
    return refs
```

### Rename Functions
```python
def rename_combat_functions():
    """Rename identified combat functions"""
    combat_funcs = {
        0x00412340: "CalculateDamage",
        0x00412580: "ApplyCriticalHit",
        0x00412790: "CheckAccuracy"
    }
    
    for addr, name in combat_funcs.items():
        idc.set_name(addr, name, idc.SN_NOWARN)
```

## 📚 Next Steps

### Learn More
1. **[Function Analysis Scripts](ida-pro-function-analysis.md)** - Deep dive into function identification
2. **[Pattern Recognition](ida-pro-pattern-recognition.md)** - Automated pattern detection
3. **[Data Extraction](ida-pro-data-extraction.md)** - Extract game data

### Practice Projects
- Find all network packet handlers
- Map the combat calculation flow
- Identify file format loaders
- Trace ability execution

## 🤝 Contributing

Share your scripts with the community:
1. Document your findings
2. Comment your code clearly
3. Test on different versions
4. Submit to community repository

## 💡 Tips for Success

### Start Simple
- Begin with string searches
- Look for obvious patterns
- Build complexity gradually

### Document Everything
- Comment your scripts
- Note memory addresses
- Track version differences

### Collaborate
- Share findings on Discord
- Ask for help when stuck
- Contribute to community knowledge

## 🔗 Resources

### Community Scripts
- [GitHub Repository](https://github.com/hdneo/mxo-hd/tree/main/ida-scripts)
- [Discord #reverse-engineering](https://discord.gg/3QXTAGB9)

### IDA Pro Resources
- [Official Documentation](https://www.hex-rays.com/products/ida/support/idadoc/)
- [IDAPython Reference](https://www.hex-rays.com/products/ida/support/idapython_docs/)

---

**Remember**: Reverse engineering helps preserve gaming history. Use knowledge responsibly.

[← Back to Technical Docs](index.md) | [Function Analysis →](ida-pro-function-analysis.md) | [Glossary →](../glossary.md)