# Matrix Online Technical Glossary
**Essential Terms for Liberation**

> *"Unfortunately, no one can be told what the Matrix is. You have to see it for yourself."* - But we can explain the technical terms!

## Quick Navigation
[A](#a) | [C](#c) | [D](#d) | [E](#e) | [G](#g) | [H](#h) | [I](#i) | [L](#l) | [M](#m) | [P](#p) | [R](#r) | [T](#t)

---

## A

### AI Director
System that dynamically adjusts game difficulty and events based on player behavior.

### API (Application Programming Interface)
Set of rules and protocols for building and interacting with software applications.

---

## C

### CNB (Cinematic Binary)
File format used by Matrix Online for storing real-time 3D cutscenes. These files contain:
- 3D models and animations
- Camera movements
- Dialogue and timing data
- Special effects

**Status**: No viewer exists yet - #1 community priority

### Combat Interlock
Matrix Online's unique turn-based combat system where players "lock" with enemies.

### Cortana
Open-source world parser tool that survived the mxoemu.info shutdown. Successfully extracts:
- World geometry
- Collision meshes
- District layouts

---

## D

### DirectX
Microsoft's collection of APIs for handling multimedia tasks in games.

### District
Major areas in Matrix Online's Mega City, such as:
- Richland (Downtown, Westview, International)
- Each district has unique architecture and missions

### DLL (Dynamic Link Library)
Windows library files containing code and data used by multiple programs.

---

## E

### Eden Reborn
Modern Matrix Online server project in active development. Features:
- Enhanced graphics and performance
- New content systems
- Cross-platform support
- Open-source philosophy

### Emulator
Software that enables one computer system to behave like another. MXO emulators recreate the original game servers.

---

## G

### GM (Game Master)
Administrator with special powers to manage the game world and help players.

### GPU (Graphics Processing Unit)
Specialized processor designed to accelerate graphics rendering.

---

## H

### HDS (Hardline Dreams Server)
Alternative Matrix Online server implementation by pahefu and neowhoru. Features:
- Different architecture than MXOEmu
- Some unique features and approaches
- Active development

### Hex Editor
Tool for viewing and editing binary files at the byte level. Essential for:
- File format reverse engineering
- Binary patching
- Data analysis

---

## I

### IDA Pro
Industry-standard disassembler and debugger used for reverse engineering. Matrix Online uses include:
- Combat system analysis (1,035 strings decoded)
- Network protocol discovery
- File format research

### IL (Intermediate Language)
Microsoft .NET bytecode that C# compiles to. Used in modifying .NET applications like HDS.exe.

---

## L

### LTB (Lithtech Binary)
File format from the Lithtech engine that Matrix Online is based on.

### Lithtech
Game engine by Monolith Productions used as the base for Matrix Online's heavily modified engine.

---

## M

### MOA (Model Animation)
Matrix Online's animation file format containing:
- Skeletal animation data
- Bone hierarchies
- Animation sequences

### MOMS (Matrix Online Modding Suite)
Active development tool for viewing and converting MXO assets. Current features:
- View .prop and .moa files
- Basic texture display
- Export to OBJ/FBX

### MXO
Common abbreviation for "The Matrix Online"

### MXOEmu (Matrix Online Emulator)
Original server emulator project by rajkosto. The foundation for most current server projects.

---

## P

### PKB (Package Binary)
Archive format containing Matrix Online game assets. Similar to ZIP files but with custom compression. Contains:
- Models (.prop files)
- Textures (.txa files)
- Sounds and other resources

**Note**: reztools (PKB extractor) was lost - recreation is high priority

### PROP (Property/Object)
Matrix Online's 3D model format containing:
- Mesh geometry
- Material properties
- Texture references
- Collision data

**Success**: Format decoded by pahefu in 2018

---

## R

### radare2
Open-source reverse engineering framework. Alternative to IDA Pro for:
- Binary analysis
- Patching executables
- Disassembly

### Reality Server
Original community server by rajkosto, predecessor to current mxoemu.info

### reztools
Lost tool that could extract PKB archives. Critical for:
- Asset extraction
- Modding capabilities
- Content preservation

### RSI (Residual Self Image)
In-game term for character appearance/avatar. Technically refers to character model and customization data.

---

## T

### TXA (Texture Archive)
Matrix Online's texture format. Can be converted to/from standard DDS format using community tools.

---

## Usage Notes

This glossary covers the most common technical terms in the Matrix Online preservation community. When writing documentation:

1. **First use**: Always expand acronyms on first use
2. **Link to glossary**: Link technical terms to this glossary
3. **Context matters**: Provide brief inline explanations for critical terms
4. **Keep it simple**: Use common alternatives when possible

## Contributing

Found a term that needs explanation? Please add it following this format:
- **Term name** (expansion if acronym)
- Brief, clear explanation
- Relevance to Matrix Online
- Current status if applicable

---

[← Back to Home](index.md) | [Technical Documentation →](03-technical/index.md)