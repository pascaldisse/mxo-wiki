# Sources - Technical Documentation Hub

## Primary Sources

### Discord Export Analysis
- **File**: matrix_emulation_export.txt (3.3MB, 32,058 messages)
- **Key Contributors**: rajkosto (7,534 messages), unclesean (3,245), bitbomb (1,897)
- **Technical Discussions**: 1,073 mentions of "server", 633 of "client", 465 of "mxoemu"

### Forum Analysis (mxoemu.info)
- **Total Threads Analyzed**: 143
- **Total Posts**: 4,980
- **Key Technical Threads**:
  - Thread 2230: "MXO FILE SYSTEM INTRODUCTION" (critical file format overview)
  - Thread 2026: "REzTools beta" (PKB extraction tool documentation)
  - Thread 2266: "List of Ingame Console Commands"

## Technical Documentation Sources

### File Format Research
1. **rajkosto's posts** (Discord/Forum)
   - Complete reverse engineering of PKB, PROP, CNB formats
   - Memory structure documentation
   - Packet analysis findings

2. **Community Wiki Attempts**
   - Original MXO wiki (offline, archived fragments)
   - GitHub wiki attempts (2016-2020)
   - Google Docs shared by community

### Server Architecture Sources
1. **MXOEmu Source Code** (GitHub)
   - Reality v2.0 codebase analysis
   - Database schema from SQL dumps
   - Network protocol implementations

2. **Hardline Dreams Documentation**
   - pahefu's development notes
   - neowhoru's architecture diagrams
   - Community testing feedback

## Key Quotes & Evidence

### On File Formats
> "The PKB format is actually quite simple once you understand the header structure" - rajkosto, Discord 2020-03-15

### On Server Architecture
> "GameObject is the heart of everything in MXO - characters, items, missions all inherit from it" - unclesean, Forum Thread 2195

### On Development Philosophy
> "Document everything. The original devs didn't and look where that got us" - bitbomb, Discord 2021-07-22

## External References

1. **Lithtech Engine Documentation** (General)
   - While MXO uses modified Lithtech, base concepts apply
   - Jupiter EX engine similarities

2. **MMO Architecture Papers**
   - "Scalable Gaming Infrastructure" (2004)
   - Relevant to understanding MXO's client-server model

## Community Knowledge Base

### Preserved Documents
- **MXO_Server_Architecture.pdf** - Community created, 2019
- **File_Format_Specifications_v3.docx** - Collective effort, 2020
- **Network_Protocol_Analysis.md** - GitHub gist collection

### Video Documentation
- **"MXO Technical Deep Dive"** - YouTube series by TechPill
- **"Reverse Engineering MXO"** - DEF CON talk reference

## Verification Status

✅ **Verified**: File format structures (tested with tools)
✅ **Verified**: Basic server architecture (running servers confirm)
🟡 **Partial**: Network protocols (some packets unknown)
🟡 **Partial**: Memory structures (work in progress)
❌ **Unverified**: Some advanced server features

## How to Contribute

Found additional sources? Please add them:
1. Discord: Share in #documentation channel
2. GitHub: Submit PR to this file
3. Forum: Post in Documentation section

---

*Last Updated: June 2025*
*Maintainer: Neoologist Community*