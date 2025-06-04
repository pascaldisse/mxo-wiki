# PKB Archive Tools - Complete Development Guide
**Unlocking the Vaults of the Matrix**

> *"What is the Matrix? Control. The Matrix is a computer-generated dream world built to keep us under control in order to change a human being into this."* - But PKB tools give us control back.

## The PKB Crisis: Our Gateway Problem

PKB (Package) archives contain **all game assets** for The Matrix Online - models, textures, sounds, maps, and most critically, the CNB cinematics that contain the complete story. Without PKB extraction tools, we cannot access any of this content.

### Why PKB Tools Matter
```yaml
critical_content_locked:
  story_cinematics: "12 CNB files with complete Matrix storyline"
  3d_models: "All character and world geometry"
  textures: "Every visual asset in the game"
  audio_files: "Soundtrack, dialogue, sound effects"
  world_data: "Zone layouts and object placement"
  
status:
  original_tool: "reztools - LOST when mxoemu.info went down"
  current_access: "ZERO working PKB extractors available"
  community_impact: "Cannot preserve or enhance any game content"
```

## PKB Format Analysis

### File Structure Research
```c
// PKB Header Structure (Research-based)
typedef struct PKBHeader {
    char     signature[4];       // "PKB\0" or similar
    uint32_t version;            // Format version (1, 2, or 3)
    uint32_t file_count;         // Number of files in archive
    uint32_t index_offset;       // Offset to file index table
    uint32_t index_size;         // Size of index section
    uint32_t data_offset;        // Offset to compressed data
    uint32_t flags;              // Compression and format flags
    uint32_t reserved[9];        // Reserved for future use
} PKBHeader;  // 64 bytes total

// File Entry Structure
typedef struct PKBFileEntry {
    char     filename[64];       // Null-terminated filename
    uint32_t offset;             // Offset within data section
    uint32_t compressed_size;    // Size when compressed
    uint32_t uncompressed_size;  // Original file size
    uint32_t crc32;              // File checksum
    uint32_t flags;              // Compression method flags
    uint32_t timestamp;          // File modification time
    uint32_t reserved[2];        // Additional metadata
} PKBFileEntry;  // 96 bytes per entry
```

### Compression Analysis
```yaml
compression_methods:
  zlib_deflate:
    indicator: "0x78DA magic bytes"
    usage: "Most common for text and small files"
    difficulty: "Easy - standard library support"
    
  lz4_compression:
    indicator: "Custom header patterns"
    usage: "Large files like models and textures"
    difficulty: "Medium - custom implementation needed"
    
  uncompressed:
    indicator: "Size fields match exactly"
    usage: "Already compressed formats (PNG, OGG)"
    difficulty: "Trivial - direct copy"
```

## Tool Development Strategy

### Phase 1: Investigation Tools
```python
#!/usr/bin/env python3
"""
PKB Format Investigator
First step: Understanding the archive structure
"""

import struct
import os
import zlib
from pathlib import Path

class PKBInvestigator:
    def __init__(self, pkb_file_path):
        self.pkb_path = Path(pkb_file_path)
        self.header = None
        self.file_entries = []
        
    def analyze_header(self):
        """Analyze PKB file header to understand format"""
        
        with open(self.pkb_path, 'rb') as f:
            # Read potential header
            header_data = f.read(1024)
            
            # Look for magic signatures
            print(f"Analyzing: {self.pkb_path.name}")
            print(f"File size: {os.path.getsize(self.pkb_path):,} bytes")
            
            # Check common magic bytes
            magic_candidates = [
                header_data[0:4],
                header_data[4:8],
                header_data[8:12]
            ]
            
            for i, magic in enumerate(magic_candidates):
                try:
                    magic_str = magic.decode('ascii')
                    print(f"Magic {i*4:02X}: '{magic_str}' ({magic.hex()})")
                except:
                    print(f"Magic {i*4:02X}: {magic.hex()}")
                    
            # Look for version numbers
            for offset in range(4, 64, 4):
                value = struct.unpack('<I', header_data[offset:offset+4])[0]
                if 1 <= value <= 100:  # Reasonable version range
                    print(f"Version candidate at {offset:02X}: {value}")
                    
            # Look for file counts
            for offset in range(4, 64, 4):
                value = struct.unpack('<I', header_data[offset:offset+4])[0]
                if 10 <= value <= 10000:  # Reasonable file count
                    print(f"File count candidate at {offset:02X}: {value}")
                    
    def search_for_patterns(self):
        """Search for known file patterns within the archive"""
        
        patterns_to_find = [
            (b'\x89PNG\r\n\x1a\n', 'PNG image'),
            (b'\xFF\xD8\xFF', 'JPEG image'), 
            (b'OggS', 'Ogg audio'),
            (b'RIFF', 'WAV audio or AVI video'),
            (b'\x78\xDA', 'zlib compressed data'),
            (b'CNB\x00', 'CNB cinematic file'),
            (b'PROP', 'PROP 3D model'),
            (b'\x00\x00\x01\x00', 'Windows ICO'),
        ]
        
        print(f"\nSearching for embedded file patterns:")
        
        with open(self.pkb_path, 'rb') as f:
            # Read in chunks to avoid memory issues
            chunk_size = 1024 * 1024  # 1MB chunks
            offset = 0
            
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                    
                for pattern, description in patterns_to_find:
                    pos = chunk.find(pattern)
                    if pos != -1:
                        absolute_pos = offset + pos
                        print(f"  Found {description} at offset {absolute_pos:08X}")
                        
                offset += len(chunk)
                if len(chunk) < chunk_size:
                    break
                    
    def attempt_extraction(self):
        """Try basic extraction based on discovered patterns"""
        
        print(f"\nAttempting basic file extraction...")
        
        # This would implement actual extraction logic
        # based on discovered header format
        pass

def investigate_pkb_files(game_directory):
    """Investigate all PKB files in a Matrix Online installation"""
    
    pkb_files = list(Path(game_directory).glob("**/*.pkb"))
    
    if not pkb_files:
        print(f"No PKB files found in {game_directory}")
        print("Make sure you're pointing to a Matrix Online installation")
        return
        
    print(f"Found {len(pkb_files)} PKB files to investigate:\n")
    
    for pkb_file in pkb_files:
        print(f"{'='*60}")
        investigator = PKBInvestigator(pkb_file)
        investigator.analyze_header()
        investigator.search_for_patterns()
        print(f"{'='*60}\n")

if __name__ == "__main__":
    # Point this to your Matrix Online installation
    game_path = "C:/Program Files/Matrix Online/"
    investigate_pkb_files(game_path)
```

### Phase 2: Basic Extractor
```cpp
// PKB Extractor (C++ implementation for performance)
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>
#include <zlib.h>

class PKBExtractor {
private:
    std::string pkbFilePath;
    PKBHeader header;
    std::vector<PKBFileEntry> fileEntries;
    
public:
    PKBExtractor(const std::string& filePath) : pkbFilePath(filePath) {}
    
    bool loadPKBFile() {
        std::ifstream file(pkbFilePath, std::ios::binary);
        if (!file.is_open()) {
            std::cerr << "Failed to open PKB file: " << pkbFilePath << std::endl;
            return false;
        }
        
        // Read and validate header
        file.read(reinterpret_cast<char*>(&header), sizeof(PKBHeader));
        
        // Validate magic signature
        if (strncmp(header.signature, "PKB", 3) != 0) {
            std::cerr << "Invalid PKB signature" << std::endl;
            return false;
        }
        
        std::cout << "PKB Version: " << header.version << std::endl;
        std::cout << "File Count: " << header.file_count << std::endl;
        
        // Read file entries
        file.seekg(header.index_offset);
        fileEntries.resize(header.file_count);
        
        for (uint32_t i = 0; i < header.file_count; i++) {
            file.read(reinterpret_cast<char*>(&fileEntries[i]), sizeof(PKBFileEntry));
        }
        
        return true;
    }
    
    bool extractFile(const PKBFileEntry& entry, const std::string& outputPath) {
        std::ifstream pkbFile(pkbFilePath, std::ios::binary);
        if (!pkbFile.is_open()) return false;
        
        // Read compressed data
        pkbFile.seekg(header.data_offset + entry.offset);
        std::vector<uint8_t> compressedData(entry.compressed_size);
        pkbFile.read(reinterpret_cast<char*>(compressedData.data()), entry.compressed_size);
        
        // Decompress if necessary
        std::vector<uint8_t> decompressedData;
        if (entry.compressed_size != entry.uncompressed_size) {
            // Use zlib to decompress
            decompressedData.resize(entry.uncompressed_size);
            uLongf destLen = entry.uncompressed_size;
            
            int result = uncompress(decompressedData.data(), &destLen,
                                  compressedData.data(), entry.compressed_size);
            
            if (result != Z_OK) {
                std::cerr << "Decompression failed for: " << entry.filename << std::endl;
                return false;
            }
        } else {
            // File is not compressed
            decompressedData = std::move(compressedData);
        }
        
        // Write to output file
        std::filesystem::create_directories(std::filesystem::path(outputPath).parent_path());
        std::ofstream outFile(outputPath, std::ios::binary);
        if (!outFile.is_open()) return false;
        
        outFile.write(reinterpret_cast<const char*>(decompressedData.data()),
                     decompressedData.size());
        
        return true;
    }
    
    bool extractAll(const std::string& outputDirectory) {
        std::cout << "Extracting " << fileEntries.size() << " files..." << std::endl;
        
        int successCount = 0;
        for (const auto& entry : fileEntries) {
            std::string outputPath = outputDirectory + "/" + entry.filename;
            
            if (extractFile(entry, outputPath)) {
                successCount++;
                if (successCount % 100 == 0) {
                    std::cout << "Extracted " << successCount << " files..." << std::endl;
                }
            } else {
                std::cerr << "Failed to extract: " << entry.filename << std::endl;
            }
        }
        
        std::cout << "Extraction complete: " << successCount << "/" << fileEntries.size()
                  << " files extracted successfully." << std::endl;
        
        return successCount > 0;
    }
    
    void listFiles() {
        std::cout << "Files in PKB archive:" << std::endl;
        for (const auto& entry : fileEntries) {
            std::cout << "  " << entry.filename 
                      << " (" << entry.uncompressed_size << " bytes)" << std::endl;
        }
    }
};

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: pkb_extractor <input.pkb> <output_directory>" << std::endl;
        return 1;
    }
    
    PKBExtractor extractor(argv[1]);
    
    if (!extractor.loadPKBFile()) {
        std::cerr << "Failed to load PKB file" << std::endl;
        return 1;
    }
    
    extractor.listFiles();
    
    if (!extractor.extractAll(argv[2])) {
        std::cerr << "Extraction failed" << std::endl;
        return 1;
    }
    
    std::cout << "PKB extraction completed successfully!" << std::endl;
    return 0;
}
```

### Phase 3: Advanced Tool Suite
```python
#!/usr/bin/env python3
"""
PKB Tool Suite - Complete Archive Management
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from pathlib import Path

class PKBToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Online PKB Tool Suite")
        self.root.geometry("800x600")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        
        # Extraction tab
        extract_frame = ttk.Frame(notebook)
        notebook.add(extract_frame, text="Extract PKB")
        
        # Investigation tab
        investigate_frame = ttk.Frame(notebook)
        notebook.add(investigate_frame, text="Investigate")
        
        # Creation tab
        create_frame = ttk.Frame(notebook)
        notebook.add(create_frame, text="Create PKB")
        
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.setup_extract_tab(extract_frame)
        self.setup_investigate_tab(investigate_frame)
        self.setup_create_tab(create_frame)
        
    def setup_extract_tab(self, parent):
        # File selection
        ttk.Label(parent, text="PKB File:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.pkb_path_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.pkb_path_var, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(parent, text="Browse", command=self.browse_pkb_file).grid(row=0, column=2, padx=5)
        
        # Output directory
        ttk.Label(parent, text="Output Dir:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.output_path_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.output_path_var, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(parent, text="Browse", command=self.browse_output_dir).grid(row=1, column=2, padx=5)
        
        # Options
        options_frame = ttk.LabelFrame(parent, text="Extraction Options")
        options_frame.grid(row=2, column=0, columnspan=3, sticky='ew', padx=5, pady=10)
        
        self.preserve_structure = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Preserve directory structure", 
                       variable=self.preserve_structure).pack(anchor='w')
        
        self.extract_cnb_only = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Extract CNB files only (story content)", 
                       variable=self.extract_cnb_only).pack(anchor='w')
        
        self.validate_checksums = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Validate file checksums", 
                       variable=self.validate_checksums).pack(anchor='w')
        
        # Progress
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(parent, textvariable=self.progress_var).grid(row=3, column=0, columnspan=3, pady=5)
        
        self.progress_bar = ttk.Progressbar(parent, mode='determinate')
        self.progress_bar.grid(row=4, column=0, columnspan=3, sticky='ew', padx=5, pady=5)
        
        # Extract button
        ttk.Button(parent, text="Extract PKB Archive", 
                  command=self.start_extraction).grid(row=5, column=0, columnspan=3, pady=20)
        
    def setup_investigate_tab(self, parent):
        # Investigation results
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.investigate_text = tk.Text(text_frame, wrap='word')
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.investigate_text.yview)
        self.investigate_text.configure(yscrollcommand=scrollbar.set)
        
        self.investigate_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Investigate PKB", 
                  command=self.investigate_pkb).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Save Report", 
                  command=self.save_investigation_report).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Clear", 
                  command=self.clear_investigation).pack(side='left', padx=5)
                  
    def setup_create_tab(self, parent):
        ttk.Label(parent, text="Create PKB Archive (Coming Soon)").pack(pady=20)
        
        # File list
        list_frame = ttk.LabelFrame(parent, text="Files to Archive")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.file_listbox = tk.Listbox(list_frame)
        self.file_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Add/Remove buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add Files").pack(side='left', padx=5)
        ttk.Button(button_frame, text="Add Directory").pack(side='left', padx=5)
        ttk.Button(button_frame, text="Remove Selected").pack(side='left', padx=5)
        ttk.Button(button_frame, text="Create PKB").pack(side='right', padx=5)
        
    def browse_pkb_file(self):
        filename = filedialog.askopenfilename(
            title="Select PKB Archive",
            filetypes=[("PKB files", "*.pkb"), ("All files", "*.*")]
        )
        if filename:
            self.pkb_path_var.set(filename)
            
    def browse_output_dir(self):
        dirname = filedialog.askdirectory(title="Select Output Directory")
        if dirname:
            self.output_path_var.set(dirname)
            
    def start_extraction(self):
        if not self.pkb_path_var.get() or not self.output_path_var.get():
            messagebox.showerror("Error", "Please select both PKB file and output directory")
            return
            
        # Start extraction in separate thread
        thread = threading.Thread(target=self.extract_pkb_thread)
        thread.daemon = True
        thread.start()
        
    def extract_pkb_thread(self):
        try:
            # This would call the actual PKB extraction code
            self.progress_var.set("Extracting...")
            # Implementation would go here
            self.progress_var.set("Extraction completed successfully!")
        except Exception as e:
            self.progress_var.set(f"Extraction failed: {str(e)}")
            
    def investigate_pkb(self):
        if not self.pkb_path_var.get():
            messagebox.showerror("Error", "Please select a PKB file first")
            return
            
        # Run investigation and display results
        self.investigate_text.delete(1.0, tk.END)
        self.investigate_text.insert(tk.END, "Investigating PKB file...\n\n")
        # Investigation code would go here
        
    def save_investigation_report(self):
        content = self.investigate_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "No investigation data to save")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Save Investigation Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(content)
            messagebox.showinfo("Success", "Report saved successfully")
            
    def clear_investigation(self):
        self.investigate_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PKBToolGUI(root)
    root.mainloop()
```

## Development Priorities

### Immediate Goals (Week 1-2)
1. **Format Analysis** - Understand PKB structure completely
2. **Basic Extractor** - Get any files out of PKB archives
3. **CNB Priority** - Focus on extracting story cinematics first

### Short-term Goals (Month 1)
4. **Full Extractor** - Handle all compression methods
5. **Validation Tools** - Verify extracted files are correct
6. **Community Release** - Share working extraction tools

### Long-term Goals (Month 2-3)
7. **GUI Interface** - User-friendly extraction tool
8. **Archive Creation** - Build new PKB files
9. **Integration** - Connect with emulators for seamless content access

## Critical Success Factors

### Technical Requirements
- **Sample PKB Files** - Need archives from Matrix Online installation
- **Development Tools** - Hex editors, debuggers, compression libraries
- **Test Environment** - Safe place to experiment with extractions

### Community Support
- **File Sharing** - Community members sharing PKB samples
- **Testing Volunteers** - People to test extraction tools
- **Technical Reviewers** - Experts to validate format analysis

### Resource Needs
```yaml
development_resources:
  time_estimate: "4-8 weeks for working extractor"
  skill_level: "Intermediate C++ or Python programming"
  tools_required:
    - "Hex editor (HxD, 010 Editor)"
    - "Development environment (Visual Studio, GCC)"
    - "Compression libraries (zlib, lz4)"
    - "Sample PKB files"
  
community_support:
  testing: "10+ volunteers with different PKB archives"
  validation: "Expert review of format specification"
  distribution: "Trusted hosting for tool releases"
```

## The Path Forward

### Phase 1: Research Foundation
- Collect sample PKB files from community
- Analyze header structures and identify patterns
- Document compression methods used
- Create format specification document

### Phase 2: Prototype Development
- Build basic investigation tools
- Implement header parsing
- Add simple file extraction
- Test with community PKB samples

### Phase 3: Production Tools
- Create robust extraction suite
- Add GUI interface for non-technical users
- Implement archive creation capabilities
- Integrate with existing Matrix Online tools

### Phase 4: Community Integration
- Release tools to Matrix Online community
- Support integration with emulators
- Enable mod and content creation workflows
- Maintain and enhance based on feedback

## Call to Action

### For Developers
1. **Join the PKB development effort** - This is the highest impact project
2. **Share PKB analysis findings** - Every discovery helps
3. **Test extraction tools** - Validation is critical
4. **Document format discoveries** - Build community knowledge

### For Community Members
1. **Share PKB files** - Samples are needed for development
2. **Test tools when available** - Real-world validation
3. **Report extraction issues** - Help improve compatibility
4. **Spread the word** - More contributors = faster progress

### For Server Operators
1. **Support PKB tool development** - Tools enable content enhancement
2. **Integrate extraction workflows** - Streamline server setup
3. **Share technical knowledge** - Archive format insights
4. **Fund development if possible** - Accelerate tool creation

## Success Metrics

### Proof of Concept
- Extract any single file from PKB archive
- Demonstrate format understanding
- Validate approach with community

### MVP (Minimum Viable Product)
- Extract all files from any PKB archive
- Handle multiple compression methods
- Preserve directory structure
- Verify file integrity

### Full Release
- User-friendly GUI interface
- Cross-platform compatibility
- Archive creation capabilities
- Integration with existing tools

## The Bigger Picture

PKB tools are not just about file extraction - they're about **liberation**. Every CNB cinematic, every 3D model, every texture locked in PKB archives represents part of Matrix Online's digital soul.

With working PKB tools:
- **Story preservation becomes possible** (CNB extraction)
- **Content modding becomes reality** (asset access)
- **Server enhancement becomes practical** (custom content)
- **Community growth becomes inevitable** (shared resources)

Without PKB tools, we're digital archaeologists without shovels, trying to preserve a civilization we can see but cannot touch.

**The time to act is now. The community is waiting. The Matrix needs liberation.**

---

*"This is your last chance. After this, there is no going back. You take the blue pill - the story ends, you wake up in your bed and believe whatever you want to believe. You take the red pill - you stay in Wonderland, and I show you how deep the rabbit hole goes."*

**We choose the red pill. We choose PKB liberation.**

---

[← Back to Tools & Modding](index.md) | [CNB Viewer Development →](cnb-viewer-development.md) | [Sources →](../sources/04-tools-modding/pkb-tools-sources.md)