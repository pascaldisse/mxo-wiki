# PKB Archive Format - Technical Deep Dive
**Advanced Archive Analysis and Extraction**

> *"There's always another level to the Matrix."*

Comprehensive technical analysis of Matrix Online's PKB archive format, including file structure, extraction methods, and tool development guidance.

## 🎯 PKB Format Overview

### Archive Purpose
PKB (Package Binary) files serve as The Matrix Online's primary asset containers:
- **Game Assets** - Textures, models, sounds, maps
- **Compressed Storage** - Efficient file size reduction
- **Hierarchical Organization** - Logical content grouping
- **Fast Access** - Optimized for game engine loading

### File Characteristics
- **File Extension**: `.pkb`
- **Binary Format**: Custom proprietary structure
- **Size Range**: 50MB - 2GB per archive
- **Content Types**: Mixed asset types in single container

## 🔬 Binary Structure Analysis

### Header Format
```c
typedef struct PKBHeader {
    char     magic[4];        // "PKB\0" signature
    uint32_t version;         // Format version (usually 1 or 2)
    uint32_t file_count;      // Number of files in archive
    uint32_t index_offset;    // Offset to file index table
    uint32_t index_size;      // Size of index table in bytes
    uint32_t data_offset;     // Offset to file data section
    uint32_t flags;           // Archive flags and options
    uint32_t reserved[3];     // Reserved for future use
} PKBHeader;
```

### File Index Structure
```c
typedef struct PKBFileEntry {
    char     filename[256];   // Null-terminated filename
    uint32_t offset;          // Offset from data_offset
    uint32_t compressed_size; // Size when compressed
    uint32_t uncompressed_size; // Original file size
    uint32_t checksum;        // CRC32 or similar
    uint16_t compression_type; // Compression method used
    uint16_t flags;           // File-specific flags
} PKBFileEntry;
```

### Archive Layout
```
+------------------+
| PKB Header       | 32 bytes
+------------------+
| Reserved Space   | Variable
+------------------+
| File Index       | file_count * sizeof(PKBFileEntry)
+------------------+
| Compressed Data  | Variable size
+------------------+
```

## 🛠️ Extraction Implementation

### Basic Extraction Algorithm
```python
def extract_pkb_archive(pkb_path, output_dir):
    with open(pkb_path, 'rb') as f:
        # Read header
        header = read_pkb_header(f)
        
        # Validate magic number
        if header.magic != b'PKB\0':
            raise ValueError("Invalid PKB file")
        
        # Read file index
        f.seek(header.index_offset)
        files = []
        for i in range(header.file_count):
            entry = read_file_entry(f)
            files.append(entry)
        
        # Extract files
        f.seek(header.data_offset)
        for entry in files:
            extract_file(f, entry, output_dir)
```

### Compression Handling
```python
def decompress_file_data(data, compression_type):
    if compression_type == 0:
        return data  # No compression
    elif compression_type == 1:
        return zlib.decompress(data)  # ZLIB
    elif compression_type == 2:
        return lzma.decompress(data)  # LZMA
    elif compression_type == 3:
        return custom_mxo_decompress(data)  # MXO custom
    else:
        raise ValueError(f"Unknown compression type: {compression_type}")
```

### File Type Detection
```python
def detect_file_type(filename, data):
    extension = filename.split('.')[-1].lower()
    magic_signatures = {
        b'\x89PNG': 'png',
        b'DDS ': 'dds',
        b'RIFF': 'wav',
        b'Ogg': 'ogg'
    }
    
    # Check magic numbers first
    for magic, file_type in magic_signatures.items():
        if data.startswith(magic):
            return file_type
    
    # Fall back to extension
    return extension
```

## 🔧 Tool Development

### PKB Extractor Requirements
Essential features for a complete PKB extraction tool:

#### Core Functionality
- **Archive validation** - Verify header integrity
- **File listing** - Display contents without extraction
- **Selective extraction** - Extract specific files or patterns
- **Batch processing** - Handle multiple archives
- **Progress reporting** - Show extraction progress
- **Error handling** - Graceful failure recovery

#### Advanced Features
- **Compression detection** - Automatic decompression
- **File type organization** - Sort by content type
- **Metadata preservation** - Maintain timestamps and attributes
- **Integrity verification** - Checksum validation
- **Search capabilities** - Find files by name or type

### Reference Implementation
```python
class PKBExtractor:
    def __init__(self, pkb_path):
        self.pkb_path = pkb_path
        self.header = None
        self.file_entries = []
        
    def load_archive(self):
        with open(self.pkb_path, 'rb') as f:
            self.header = self._read_header(f)
            self.file_entries = self._read_file_index(f)
    
    def list_files(self, pattern=None):
        if pattern:
            import fnmatch
            return [entry for entry in self.file_entries 
                   if fnmatch.fnmatch(entry.filename, pattern)]
        return self.file_entries
    
    def extract_file(self, filename, output_path):
        entry = self._find_file_entry(filename)
        if not entry:
            raise FileNotFoundError(f"File not found: {filename}")
        
        with open(self.pkb_path, 'rb') as f:
            f.seek(self.header.data_offset + entry.offset)
            compressed_data = f.read(entry.compressed_size)
            
            decompressed_data = self._decompress(
                compressed_data, entry.compression_type
            )
            
            with open(output_path, 'wb') as out_f:
                out_f.write(decompressed_data)
    
    def extract_all(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
        for entry in self.file_entries:
            output_path = os.path.join(output_dir, entry.filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            self.extract_file(entry.filename, output_path)
```

## 📊 Archive Content Analysis

### Common File Types in PKB Archives
| Type | Extension | Purpose | Typical Size |
|------|-----------|---------|--------------|
| **Textures** | .dds, .tga | Surface materials | 1-50MB |
| **Models** | .prop, .moa | 3D geometry | 100KB-10MB |
| **Audio** | .wav, .ogg | Sound effects, music | 1-100MB |
| **Maps** | .map, .bsp | Level geometry | 5-200MB |
| **Scripts** | .lua, .txt | Game logic | 1-100KB |
| **Config** | .ini, .cfg | Settings | 1-10KB |

### Archive Size Distribution
- **Small Archives** (50-200MB): Character models, UI elements
- **Medium Archives** (200MB-1GB): Zone content, textures
- **Large Archives** (1-2GB): Music, cinematics, voice acting

### Content Organization Patterns
```
Archive Structure Examples:
models/
├── characters/
│   ├── player/
│   └── npcs/
├── props/
│   ├── furniture/
│   └── vehicles/
└── weapons/
    ├── firearms/
    └── melee/

textures/
├── characters/
├── environments/
├── ui/
└── effects/
```

## 🔍 Reverse Engineering Methods

### Static Analysis
Tools and techniques for PKB format analysis:

#### Hex Editor Analysis
```bash
# Examine PKB header with hex editor
hexdump -C archive.pkb | head -20

# Search for magic patterns
strings archive.pkb | grep -E "(\.dds|\.wav|\.prop)"

# Find repeating structures (file index)
xxd archive.pkb | grep "00 00 00" | head -10
```

#### Binary Comparison
```python
def compare_pkb_structures(pkb1_path, pkb2_path):
    """Compare two PKB files to identify format patterns"""
    with open(pkb1_path, 'rb') as f1, open(pkb2_path, 'rb') as f2:
        header1 = f1.read(32)
        header2 = f2.read(32)
        
        # Compare headers byte by byte
        for i, (b1, b2) in enumerate(zip(header1, header2)):
            if b1 != b2:
                print(f"Difference at offset {i}: {b1:02x} vs {b2:02x}")
```

### Dynamic Analysis
Monitoring game engine behavior:

#### File Access Monitoring
```bash
# Monitor PKB file access on Windows
Process Monitor filter: Path contains ".pkb"

# Linux file access monitoring
strace -e trace=file ./matrix.exe 2>&1 | grep "\.pkb"
```

#### Memory Analysis
```python
def analyze_loaded_pkb_data(process_memory_dump):
    """Analyze PKB data structures in memory"""
    # Search for PKB signatures in memory
    pkb_signatures = [b'PKB\x00', b'PROP', b'DDS ']
    
    for signature in pkb_signatures:
        offsets = find_signature_offsets(process_memory_dump, signature)
        for offset in offsets:
            analyze_structure_at_offset(process_memory_dump, offset)
```

## 🧪 Testing and Validation

### Archive Integrity Testing
```python
def validate_pkb_archive(pkb_path):
    """Comprehensive PKB archive validation"""
    issues = []
    
    try:
        with open(pkb_path, 'rb') as f:
            # Validate header
            header = read_pkb_header(f)
            if header.magic != b'PKB\x00':
                issues.append("Invalid magic number")
            
            # Validate file index
            if header.index_offset + header.index_size > os.path.getsize(pkb_path):
                issues.append("Index extends beyond file size")
            
            # Validate file entries
            f.seek(header.index_offset)
            for i in range(header.file_count):
                entry = read_file_entry(f)
                if entry.offset + entry.compressed_size > os.path.getsize(pkb_path):
                    issues.append(f"File {i} data extends beyond archive")
    
    except Exception as e:
        issues.append(f"Read error: {e}")
    
    return issues
```

### Extraction Testing
```python
def test_extraction_accuracy(pkb_path, test_output_dir):
    """Test extraction accuracy and completeness"""
    extractor = PKBExtractor(pkb_path)
    extractor.load_archive()
    
    # Test individual file extraction
    for entry in extractor.file_entries[:10]:  # Test first 10 files
        try:
            output_path = os.path.join(test_output_dir, entry.filename)
            extractor.extract_file(entry.filename, output_path)
            
            # Verify file size
            if os.path.getsize(output_path) != entry.uncompressed_size:
                print(f"Size mismatch for {entry.filename}")
            
            # Verify checksum if available
            if entry.checksum:
                calculated_checksum = calculate_crc32(output_path)
                if calculated_checksum != entry.checksum:
                    print(f"Checksum mismatch for {entry.filename}")
        
        except Exception as e:
            print(f"Extraction failed for {entry.filename}: {e}")
```

## 📚 Community Resources

### Available Tools
Current community-developed PKB tools:

#### Legacy Tools (Lost)
- **reztools** - Original PKB extractor (no longer available)
- **PKB Explorer** - GUI-based archive browser (lost)
- **MXO Asset Extractor** - Batch extraction tool (unavailable)

#### Recreation Projects
- **Modern PKB Extractor** - Python-based recreation in development
- **PKB FUSE** - Filesystem mounting tool (experimental)
- **Web PKB Viewer** - Browser-based archive explorer (planned)

### Development Resources
- **[Technical Documentation](pkb-archive-structure.md)** - Detailed format analysis
- **[Tool Development Guide](../04-tools-modding/tool-development-guide.md)** - Development setup
- **[Community Discord](https://discord.gg/3QXTAGB9)** - Real-time development discussion

## 🚀 Future Development

### Priority Features
1. **Complete Format Specification** - Document all PKB variants
2. **Robust Extraction Tool** - Handle all compression types
3. **Archive Creation** - Build new PKB files from assets
4. **Integration with Game Engines** - Direct mounting support

### Technical Challenges
- **Compression Variants** - Multiple compression algorithms in use
- **Version Differences** - PKB format evolved over game lifetime
- **Large File Handling** - Memory-efficient processing of GB+ archives
- **Error Recovery** - Graceful handling of corrupted archives

### Community Goals
- **Tool Accessibility** - Easy-to-use tools for all skill levels
- **Documentation Completeness** - Comprehensive format specification
- **Asset Preservation** - Extract and preserve all game content
- **Modding Support** - Enable community content creation

---

## 🌟 PKB Archive Mastery

Understanding PKB archives is essential for:
- ✅ **Asset Extraction** - Access game textures, models, and sounds
- ✅ **Tool Development** - Create modern extraction utilities
- ✅ **Game Preservation** - Preserve Matrix Online content
- ✅ **Modding Support** - Enable community content creation

**Every archive contains treasures. Every tool unlocks possibilities.**

---

> *"Inside every PKB archive lies a piece of the Matrix. Extract them all, and the world is yours."*

---

[← File Formats](file-formats.md) | [🏠 Home](../index.md) | [PROP Format →](prop-format.md)