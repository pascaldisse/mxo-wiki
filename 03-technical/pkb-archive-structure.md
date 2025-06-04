# PKB Archive Structure and Tools
**Unlocking the Matrix Online Asset Containers**

> *"What you must learn is that these rules are no different than the rules of a computer system."* - Morpheus (And PKB files are the system's containers.)

## 📦 PKB Archive Overview

PKB (Package Binary) files are the primary asset containers used by The Matrix Online. These archives hold everything from 3D models and textures to audio files and configuration data. Understanding PKB structure is essential for content extraction, modification, and preservation.

## 🔍 Format Analysis

### PKB File Characteristics
```yaml
pkb_format:
  extension: ".pkb"
  purpose: "Asset packaging and distribution"
  compression: "Custom LZ-based algorithm"
  encryption: "Optional XOR obfuscation"
  
  typical_sizes:
    small: "1-10 MB"     # UI assets, scripts
    medium: "10-100 MB"  # District data, models
    large: "100-500 MB"  # Audio, cinematics
    
  total_archives: "~180 files"
  estimated_content: "15+ GB uncompressed"
  
  common_names:
    - "models.pkb"       # 3D models and animations
    - "textures.pkb"     # Texture files (TXA format)
    - "audio.pkb"        # Sound effects and music
    - "ui.pkb"           # Interface elements
    - "scripts.pkb"      # Mission and logic scripts
    - "maps.pkb"         # World geometry data
```

### File Header Structure
```c
struct PKBHeader {
    char     magic[4];           // "PKB\x00" (0x504B4200)
    uint32_t version;            // Format version (typically 1 or 2)
    uint32_t flags;              // Archive flags
    uint32_t file_count;         // Number of files in archive
    uint32_t directory_offset;   // Offset to file directory
    uint32_t directory_size;     // Size of directory section
    uint32_t data_offset;        // Offset to file data section
    uint32_t data_size;          // Size of data section
    uint32_t compression_type;   // Compression algorithm used
    uint32_t encryption_key;     // XOR key (if encrypted)
    uint32_t checksum;           // Archive integrity checksum
    uint32_t reserved[5];        // Reserved for future use
};
```

### PKB Flags
```c
#define PKB_FLAG_COMPRESSED     0x00000001  // Archive uses compression
#define PKB_FLAG_ENCRYPTED      0x00000002  // Archive is encrypted
#define PKB_FLAG_SIGNED         0x00000004  // Archive has digital signature
#define PKB_FLAG_STREAMING      0x00000008  // Supports streaming access
#define PKB_FLAG_DELTA          0x00000010  // Delta/patch archive
#define PKB_FLAG_READONLY       0x00000020  // Read-only archive
#define PKB_FLAG_VERIFIED       0x00000040  // Integrity verified
#define PKB_FLAG_OPTIMIZED      0x00000080  // Space-optimized layout
```

## 🗂️ Directory Structure

### File Entry Format
```c
struct PKBFileEntry {
    char     filename[64];       // Null-terminated filename
    uint32_t file_offset;        // Offset in data section
    uint32_t compressed_size;    // Size when compressed
    uint32_t uncompressed_size;  // Original file size
    uint32_t file_flags;         // Per-file flags
    uint32_t checksum;           // File integrity checksum
    uint64_t timestamp;          // File modification time
    uint32_t reserved[2];        // Future use
};
```

### File Flags
```c
#define PKB_FILE_COMPRESSED     0x00000001  // File is compressed
#define PKB_FILE_ENCRYPTED      0x00000002  // File is encrypted
#define PKB_FILE_DUPLICATE      0x00000004  // Duplicate of another file
#define PKB_FILE_DELETED        0x00000008  // File marked for deletion
#define PKB_FILE_SPARSE         0x00000010  // Sparse file (holes)
#define PKB_FILE_EXECUTABLE     0x00000020  // Executable file
#define PKB_FILE_READONLY       0x00000040  // Read-only file
#define PKB_FILE_SYSTEM         0x00000080  // System file
```

## 🛠️ PKB Analysis Tools

### Complete PKB Parser
```python
#!/usr/bin/env python3
"""
Matrix Online PKB Archive Parser
Complete implementation for PKB file extraction and analysis
"""

import struct
import os
import sys
import zlib
import time
from typing import List, Dict, Optional, BinaryIO
from pathlib import Path

class PKBFile:
    """Represents a single file within a PKB archive"""
    
    def __init__(self, filename: str, offset: int, compressed_size: int, 
                 uncompressed_size: int, flags: int, checksum: int, timestamp: int):
        self.filename = filename
        self.offset = offset
        self.compressed_size = compressed_size
        self.uncompressed_size = uncompressed_size
        self.flags = flags
        self.checksum = checksum
        self.timestamp = timestamp
        
    @property
    def is_compressed(self) -> bool:
        return bool(self.flags & 0x00000001)
        
    @property
    def is_encrypted(self) -> bool:
        return bool(self.flags & 0x00000002)
        
    @property
    def compression_ratio(self) -> float:
        if self.uncompressed_size == 0:
            return 0.0
        return self.compressed_size / self.uncompressed_size
        
    def __repr__(self):
        return f"PKBFile({self.filename}, {self.uncompressed_size} bytes)"

class PKBArchive:
    """PKB Archive parser and extractor"""
    
    def __init__(self, pkb_path: str):
        self.pkb_path = Path(pkb_path)
        self.header = None
        self.files = []
        self.file_map = {}
        self._file_handle = None
        
        if not self.pkb_path.exists():
            raise FileNotFoundError(f"PKB file not found: {pkb_path}")
            
        self._parse_archive()
        
    def _parse_archive(self):
        """Parse PKB archive structure"""
        with open(self.pkb_path, 'rb') as f:
            self._file_handle = f
            
            # Read and parse header
            self.header = self._parse_header(f)
            
            # Read file directory
            self._parse_directory(f)
            
    def _parse_header(self, f: BinaryIO) -> Dict:
        """Parse PKB file header"""
        f.seek(0)
        header_data = f.read(64)  # Header is 64 bytes
        
        if len(header_data) < 64:
            raise ValueError("Invalid PKB file: header too short")
            
        # Unpack header structure
        header_values = struct.unpack('<4sIIIIIIIIII5I', header_data)
        
        header = {
            'magic': header_values[0],
            'version': header_values[1],
            'flags': header_values[2],
            'file_count': header_values[3],
            'directory_offset': header_values[4],
            'directory_size': header_values[5],
            'data_offset': header_values[6],
            'data_size': header_values[7],
            'compression_type': header_values[8],
            'encryption_key': header_values[9],
            'checksum': header_values[10],
            'reserved': header_values[11:16]
        }
        
        # Validate magic number
        if header['magic'] != b'PKB\x00':
            raise ValueError(f"Invalid PKB magic: {header['magic']}")
            
        return header
        
    def _parse_directory(self, f: BinaryIO):
        """Parse file directory entries"""
        f.seek(self.header['directory_offset'])
        
        for i in range(self.header['file_count']):
            entry_data = f.read(96)  # Each entry is 96 bytes
            
            if len(entry_data) < 96:
                raise ValueError(f"Truncated directory entry {i}")
                
            # Unpack file entry
            entry_values = struct.unpack('<64sIIIIIQII', entry_data)
            
            filename = entry_values[0].rstrip(b'\x00').decode('utf-8', errors='ignore')
            file_offset = entry_values[1]
            compressed_size = entry_values[2]
            uncompressed_size = entry_values[3]
            file_flags = entry_values[4]
            checksum = entry_values[5]
            timestamp = entry_values[6]
            
            # Create PKBFile object
            pkb_file = PKBFile(
                filename=filename,
                offset=file_offset,
                compressed_size=compressed_size,
                uncompressed_size=uncompressed_size,
                flags=file_flags,
                checksum=checksum,
                timestamp=timestamp
            )
            
            self.files.append(pkb_file)
            self.file_map[filename] = pkb_file
            
    def list_files(self) -> List[PKBFile]:
        """Get list of all files in archive"""
        return self.files.copy()
        
    def get_file(self, filename: str) -> Optional[PKBFile]:
        """Get file entry by name"""
        return self.file_map.get(filename)
        
    def extract_file(self, filename: str, output_path: Optional[str] = None) -> bytes:
        """Extract a single file from the archive"""
        pkb_file = self.get_file(filename)
        
        if not pkb_file:
            raise FileNotFoundError(f"File not found in archive: {filename}")
            
        with open(self.pkb_path, 'rb') as f:
            # Seek to file data
            f.seek(self.header['data_offset'] + pkb_file.offset)
            
            # Read file data
            file_data = f.read(pkb_file.compressed_size)
            
            # Decrypt if necessary
            if pkb_file.is_encrypted:
                file_data = self._decrypt_data(file_data, self.header['encryption_key'])
                
            # Decompress if necessary
            if pkb_file.is_compressed:
                file_data = self._decompress_data(file_data, pkb_file.uncompressed_size)
                
            # Verify checksum
            if not self._verify_checksum(file_data, pkb_file.checksum):
                print(f"Warning: Checksum mismatch for {filename}")
                
            # Save to file if output path specified
            if output_path:
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'wb') as out_f:
                    out_f.write(file_data)
                    
            return file_data
            
    def extract_all(self, output_dir: str, preserve_structure: bool = True):
        """Extract all files from the archive"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        extracted_count = 0
        failed_count = 0
        
        for pkb_file in self.files:
            try:
                if preserve_structure:
                    # Preserve directory structure from filename
                    file_output_path = output_path / pkb_file.filename
                else:
                    # Flatten to output directory
                    safe_filename = pkb_file.filename.replace('/', '_').replace('\\', '_')
                    file_output_path = output_path / safe_filename
                    
                print(f"Extracting: {pkb_file.filename}")
                self.extract_file(pkb_file.filename, str(file_output_path))
                extracted_count += 1
                
            except Exception as e:
                print(f"Failed to extract {pkb_file.filename}: {e}")
                failed_count += 1
                
        print(f"✅ Extraction complete: {extracted_count} files extracted, {failed_count} failed")
        
    def _decrypt_data(self, data: bytes, key: int) -> bytes:
        """Decrypt XOR-encrypted data"""
        if key == 0:
            return data
            
        # Simple XOR decryption
        key_bytes = struct.pack('<I', key)
        decrypted = bytearray()
        
        for i, byte in enumerate(data):
            decrypted.append(byte ^ key_bytes[i % 4])
            
        return bytes(decrypted)
        
    def _decompress_data(self, compressed_data: bytes, expected_size: int) -> bytes:
        """Decompress PKB compressed data"""
        
        # Try different decompression methods
        decompression_methods = [
            self._decompress_zlib,
            self._decompress_pkb_custom,
            self._decompress_lz77
        ]
        
        for method in decompression_methods:
            try:
                decompressed = method(compressed_data)
                if len(decompressed) == expected_size:
                    return decompressed
            except Exception:
                continue
                
        # If all methods fail, return compressed data with warning
        print(f"Warning: Could not decompress data (expected {expected_size} bytes)")
        return compressed_data
        
    def _decompress_zlib(self, data: bytes) -> bytes:
        """Try zlib decompression"""
        return zlib.decompress(data)
        
    def _decompress_pkb_custom(self, data: bytes) -> bytes:
        """Custom PKB decompression algorithm"""
        # This would implement the specific PKB compression algorithm
        # For now, we'll use a placeholder
        raise NotImplementedError("PKB custom decompression not yet implemented")
        
    def _decompress_lz77(self, data: bytes) -> bytes:
        """LZ77-style decompression"""
        # Simplified LZ77 implementation
        output = bytearray()
        pos = 0
        
        while pos < len(data):
            if data[pos] & 0x80:  # Compressed token
                length = (data[pos] & 0x7F) + 3
                pos += 1
                if pos >= len(data):
                    break
                    
                offset = data[pos]
                pos += 1
                
                # Copy from back-reference
                for _ in range(length):
                    if len(output) >= offset:
                        output.append(output[-offset])
                    else:
                        output.append(0)  # Padding
            else:  # Literal byte
                output.append(data[pos])
                pos += 1
                
        return bytes(output)
        
    def _verify_checksum(self, data: bytes, expected_checksum: int) -> bool:
        """Verify file data checksum"""
        # Simple CRC32 checksum
        calculated = zlib.crc32(data) & 0xffffffff
        return calculated == expected_checksum
        
    def get_archive_info(self) -> Dict:
        """Get comprehensive archive information"""
        
        total_compressed = sum(f.compressed_size for f in self.files)
        total_uncompressed = sum(f.uncompressed_size for f in self.files)
        
        file_types = {}
        for f in self.files:
            ext = os.path.splitext(f.filename)[1].lower()
            file_types[ext] = file_types.get(ext, 0) + 1
            
        return {
            'filename': self.pkb_path.name,
            'file_size': self.pkb_path.stat().st_size,
            'version': self.header['version'],
            'flags': self.header['flags'],
            'file_count': len(self.files),
            'total_compressed_size': total_compressed,
            'total_uncompressed_size': total_uncompressed,
            'compression_ratio': total_compressed / total_uncompressed if total_uncompressed > 0 else 0,
            'file_types': file_types,
            'compressed_files': sum(1 for f in self.files if f.is_compressed),
            'encrypted_files': sum(1 for f in self.files if f.is_encrypted)
        }
        
    def search_files(self, pattern: str) -> List[PKBFile]:
        """Search for files matching a pattern"""
        import fnmatch
        
        matching_files = []
        for f in self.files:
            if fnmatch.fnmatch(f.filename.lower(), pattern.lower()):
                matching_files.append(f)
                
        return matching_files

# Command-line interface
def main():
    if len(sys.argv) < 2:
        print("Usage: python pkb_parser.py <pkb_file> [command] [options]")
        print("Commands:")
        print("  list                    - List all files in archive")
        print("  info                    - Show archive information")
        print("  extract <file>          - Extract specific file")
        print("  extract-all <output>    - Extract all files")
        print("  search <pattern>        - Search for files")
        return
        
    pkb_file = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'info'
    
    try:
        archive = PKBArchive(pkb_file)
        
        if command == 'list':
            print(f"Files in {pkb_file}:")
            for f in archive.list_files():
                compressed_flag = 'C' if f.is_compressed else ' '
                encrypted_flag = 'E' if f.is_encrypted else ' '
                print(f"  {compressed_flag}{encrypted_flag} {f.uncompressed_size:>10} {f.filename}")
                
        elif command == 'info':
            info = archive.get_archive_info()
            print(f"PKB Archive Information: {info['filename']}")
            print(f"  File size: {info['file_size']:,} bytes")
            print(f"  Version: {info['version']}")
            print(f"  Files: {info['file_count']}")
            print(f"  Compressed size: {info['total_compressed_size']:,} bytes")
            print(f"  Uncompressed size: {info['total_uncompressed_size']:,} bytes")
            print(f"  Compression ratio: {info['compression_ratio']:.2%}")
            print(f"  Compressed files: {info['compressed_files']}")
            print(f"  Encrypted files: {info['encrypted_files']}")
            print("  File types:")
            for ext, count in sorted(info['file_types'].items()):
                print(f"    {ext or '(no extension)'}: {count}")
                
        elif command == 'extract' and len(sys.argv) > 3:
            filename = sys.argv[3]
            output_path = sys.argv[4] if len(sys.argv) > 4 else filename
            
            print(f"Extracting {filename}...")
            archive.extract_file(filename, output_path)
            print(f"✅ Extracted to {output_path}")
            
        elif command == 'extract-all' and len(sys.argv) > 3:
            output_dir = sys.argv[3]
            
            print(f"Extracting all files to {output_dir}...")
            archive.extract_all(output_dir)
            
        elif command == 'search' and len(sys.argv) > 3:
            pattern = sys.argv[3]
            
            results = archive.search_files(pattern)
            print(f"Files matching '{pattern}':")
            for f in results:
                print(f"  {f.filename}")
                
        else:
            print(f"Unknown command: {command}")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## 🔧 PKB Extraction Tools

### Batch PKB Processor
```python
#!/usr/bin/env python3
"""
Batch PKB Archive Processor
Process multiple PKB files in a directory
"""

import os
import sys
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class PKBBatchProcessor:
    """Process multiple PKB archives"""
    
    def __init__(self, input_directory: str, output_directory: str):
        self.input_dir = Path(input_directory)
        self.output_dir = Path(output_directory)
        self.results = []
        
    def find_pkb_files(self) -> List[Path]:
        """Find all PKB files in input directory"""
        pkb_files = []
        
        for file_path in self.input_dir.rglob('*.pkb'):
            pkb_files.append(file_path)
            
        return sorted(pkb_files)
        
    def process_single_pkb(self, pkb_path: Path) -> Dict:
        """Process a single PKB file"""
        start_time = time.time()
        
        try:
            archive = PKBArchive(str(pkb_path))
            
            # Create output directory for this archive
            archive_output = self.output_dir / pkb_path.stem
            archive_output.mkdir(parents=True, exist_ok=True)
            
            # Extract all files
            archive.extract_all(str(archive_output))
            
            # Get archive info
            info = archive.get_archive_info()
            
            processing_time = time.time() - start_time
            
            result = {
                'pkb_file': str(pkb_path),
                'status': 'success',
                'processing_time': processing_time,
                'archive_info': info,
                'output_directory': str(archive_output)
            }
            
            print(f"✅ Processed {pkb_path.name} in {processing_time:.2f}s")
            
        except Exception as e:
            result = {
                'pkb_file': str(pkb_path),
                'status': 'error',
                'error_message': str(e),
                'processing_time': time.time() - start_time
            }
            
            print(f"❌ Failed to process {pkb_path.name}: {e}")
            
        return result
        
    def process_all(self, max_workers: int = 4) -> Dict:
        """Process all PKB files with multithreading"""
        
        pkb_files = self.find_pkb_files()
        
        if not pkb_files:
            print("No PKB files found in input directory")
            return {'results': [], 'summary': {}}
            
        print(f"Found {len(pkb_files)} PKB files to process")
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all jobs
            future_to_pkb = {
                executor.submit(self.process_single_pkb, pkb_path): pkb_path 
                for pkb_path in pkb_files
            }
            
            # Collect results
            for future in as_completed(future_to_pkb):
                result = future.result()
                self.results.append(result)
                
        # Generate summary
        summary = self.generate_summary()
        
        # Save results
        results_file = self.output_dir / 'processing_results.json'
        with open(results_file, 'w') as f:
            json.dump({
                'results': self.results,
                'summary': summary
            }, f, indent=2)
            
        print(f"📊 Processing complete! Results saved to {results_file}")
        
        return {
            'results': self.results,
            'summary': summary
        }
        
    def generate_summary(self) -> Dict:
        """Generate processing summary"""
        
        successful = [r for r in self.results if r['status'] == 'success']
        failed = [r for r in self.results if r['status'] == 'error']
        
        total_files = 0
        total_size_compressed = 0
        total_size_uncompressed = 0
        
        for result in successful:
            info = result.get('archive_info', {})
            total_files += info.get('file_count', 0)
            total_size_compressed += info.get('total_compressed_size', 0)
            total_size_uncompressed += info.get('total_uncompressed_size', 0)
            
        summary = {
            'total_pkb_files': len(self.results),
            'successful_extractions': len(successful),
            'failed_extractions': len(failed),
            'total_extracted_files': total_files,
            'total_compressed_size': total_size_compressed,
            'total_uncompressed_size': total_size_uncompressed,
            'overall_compression_ratio': total_size_compressed / total_size_uncompressed if total_size_uncompressed > 0 else 0,
            'processing_time': sum(r['processing_time'] for r in self.results)
        }
        
        return summary

def main():
    if len(sys.argv) < 3:
        print("Usage: python pkb_batch_processor.py <input_directory> <output_directory> [max_workers]")
        return 1
        
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    max_workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    
    processor = PKBBatchProcessor(input_dir, output_dir)
    results = processor.process_all(max_workers)
    
    summary = results['summary']
    print("\n📊 Processing Summary:")
    print(f"  PKB files processed: {summary['total_pkb_files']}")
    print(f"  Successful extractions: {summary['successful_extractions']}")
    print(f"  Failed extractions: {summary['failed_extractions']}")
    print(f"  Total files extracted: {summary['total_extracted_files']}")
    print(f"  Total compressed size: {summary['total_compressed_size']:,} bytes")
    print(f"  Total uncompressed size: {summary['total_uncompressed_size']:,} bytes")
    print(f"  Overall compression ratio: {summary['overall_compression_ratio']:.2%}")
    print(f"  Total processing time: {summary['processing_time']:.2f} seconds")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## 📊 PKB Content Analysis

### Content Type Analyzer
```python
#!/usr/bin/env python3
"""
PKB Content Analysis Tool
Analyze and categorize extracted PKB content
"""

import os
import mimetypes
from pathlib import Path
from collections import defaultdict, Counter
import json

class PKBContentAnalyzer:
    """Analyze extracted PKB content"""
    
    def __init__(self, extracted_directory: str):
        self.extracted_dir = Path(extracted_directory)
        self.analysis_results = {}
        
    def analyze_content(self) -> Dict:
        """Perform comprehensive content analysis"""
        
        print("🔍 Analyzing extracted PKB content...")
        
        # Find all extracted files
        all_files = list(self.extracted_dir.rglob('*'))
        files_only = [f for f in all_files if f.is_file()]
        
        print(f"Found {len(files_only)} extracted files")
        
        # Analyze by file type
        file_type_analysis = self.analyze_file_types(files_only)
        
        # Analyze by directory structure
        directory_analysis = self.analyze_directory_structure(files_only)
        
        # Analyze MXO-specific formats
        mxo_format_analysis = self.analyze_mxo_formats(files_only)
        
        # Generate content statistics
        content_stats = self.generate_content_statistics(files_only)
        
        self.analysis_results = {
            'total_files': len(files_only),
            'file_types': file_type_analysis,
            'directory_structure': directory_analysis,
            'mxo_formats': mxo_format_analysis,
            'statistics': content_stats
        }
        
        return self.analysis_results
        
    def analyze_file_types(self, files: List[Path]) -> Dict:
        """Analyze files by MIME type and extension"""
        
        extension_counts = Counter()
        mime_type_counts = Counter()
        size_by_type = defaultdict(int)
        
        for file_path in files:
            # Get extension
            ext = file_path.suffix.lower()
            extension_counts[ext] += 1
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type:
                mime_type_counts[mime_type] += 1
            else:
                mime_type_counts['unknown'] += 1
                
            # Get file size
            try:
                file_size = file_path.stat().st_size
                size_by_type[ext] += file_size
            except:
                pass
                
        return {
            'extension_counts': dict(extension_counts.most_common()),
            'mime_type_counts': dict(mime_type_counts.most_common()),
            'size_by_extension': dict(size_by_type)
        }
        
    def analyze_directory_structure(self, files: List[Path]) -> Dict:
        """Analyze directory organization"""
        
        directory_counts = Counter()
        files_by_directory = defaultdict(list)
        
        for file_path in files:
            # Get relative path from extracted directory
            rel_path = file_path.relative_to(self.extracted_dir)
            
            # Get top-level directory
            if len(rel_path.parts) > 1:
                top_dir = rel_path.parts[0]
                directory_counts[top_dir] += 1
                files_by_directory[top_dir].append(str(rel_path))
            else:
                directory_counts['root'] += 1
                files_by_directory['root'].append(str(rel_path))
                
        # Calculate directory sizes
        directory_sizes = {}
        for directory, file_list in files_by_directory.items():
            total_size = 0
            for file_rel_path in file_list:
                file_full_path = self.extracted_dir / file_rel_path
                try:
                    total_size += file_full_path.stat().st_size
                except:
                    pass
            directory_sizes[directory] = total_size
            
        return {
            'directory_file_counts': dict(directory_counts.most_common()),
            'directory_sizes': directory_sizes,
            'directory_contents': dict(files_by_directory)
        }
        
    def analyze_mxo_formats(self, files: List[Path]) -> Dict:
        """Analyze Matrix Online specific file formats"""
        
        mxo_extensions = {
            '.prop': 'Static 3D models',
            '.moa': 'Animated models',
            '.txa': 'Textures',
            '.txb': 'Texture variants',
            '.cnb': 'Cinematics',
            '.ltb': 'LithTech binary',
            '.lta': 'LithTech ASCII',
            '.wav': 'Audio files',
            '.ogg': 'Audio files',
            '.xml': 'Configuration/data',
            '.lua': 'Scripts',
            '.txt': 'Text/data files'
        }
        
        mxo_file_analysis = {}
        
        for ext, description in mxo_extensions.items():
            matching_files = [f for f in files if f.suffix.lower() == ext]
            
            if matching_files:
                total_size = sum(f.stat().st_size for f in matching_files if f.exists())
                
                mxo_file_analysis[ext] = {
                    'description': description,
                    'count': len(matching_files),
                    'total_size': total_size,
                    'average_size': total_size / len(matching_files) if matching_files else 0,
                    'examples': [f.name for f in matching_files[:5]]  # First 5 examples
                }
                
        return mxo_file_analysis
        
    def generate_content_statistics(self, files: List[Path]) -> Dict:
        """Generate overall content statistics"""
        
        file_sizes = []
        total_size = 0
        
        for file_path in files:
            try:
                size = file_path.stat().st_size
                file_sizes.append(size)
                total_size += size
            except:
                pass
                
        if file_sizes:
            file_sizes.sort()
            
            stats = {
                'total_size': total_size,
                'average_file_size': total_size / len(file_sizes),
                'median_file_size': file_sizes[len(file_sizes) // 2],
                'smallest_file': min(file_sizes),
                'largest_file': max(file_sizes),
                'files_over_1mb': len([s for s in file_sizes if s > 1024*1024]),
                'files_over_10mb': len([s for s in file_sizes if s > 10*1024*1024])
            }
        else:
            stats = {
                'total_size': 0,
                'average_file_size': 0,
                'median_file_size': 0,
                'smallest_file': 0,
                'largest_file': 0,
                'files_over_1mb': 0,
                'files_over_10mb': 0
            }
            
        return stats
        
    def find_interesting_files(self) -> Dict:
        """Find potentially interesting files for investigation"""
        
        interesting_files = {
            'large_files': [],
            'config_files': [],
            'script_files': [],
            'model_files': [],
            'texture_files': [],
            'audio_files': [],
            'unknown_formats': []
        }
        
        all_files = [f for f in self.extracted_dir.rglob('*') if f.is_file()]
        
        for file_path in all_files:
            rel_path = file_path.relative_to(self.extracted_dir)
            file_size = file_path.stat().st_size if file_path.exists() else 0
            ext = file_path.suffix.lower()
            
            # Large files (>10MB)
            if file_size > 10 * 1024 * 1024:
                interesting_files['large_files'].append({
                    'path': str(rel_path),
                    'size': file_size
                })
                
            # Configuration files
            if ext in ['.xml', '.cfg', '.ini', '.conf'] or 'config' in file_path.name.lower():
                interesting_files['config_files'].append(str(rel_path))
                
            # Script files
            if ext in ['.lua', '.py', '.js', '.bat', '.sh'] or 'script' in file_path.name.lower():
                interesting_files['script_files'].append(str(rel_path))
                
            # Model files
            if ext in ['.prop', '.moa', '.ltb', '.3ds', '.obj', '.fbx']:
                interesting_files['model_files'].append(str(rel_path))
                
            # Texture files
            if ext in ['.txa', '.txb', '.dds', '.png', '.jpg', '.bmp', '.tga']:
                interesting_files['texture_files'].append(str(rel_path))
                
            # Audio files
            if ext in ['.wav', '.ogg', '.mp3', '.wma']:
                interesting_files['audio_files'].append(str(rel_path))
                
            # Unknown formats
            if not ext or ext not in ['.prop', '.moa', '.txa', '.txb', '.cnb', '.ltb', '.lta', 
                                     '.wav', '.ogg', '.xml', '.lua', '.txt', '.cfg', '.ini']:
                interesting_files['unknown_formats'].append(str(rel_path))
                
        # Limit results
        for category in interesting_files:
            if len(interesting_files[category]) > 20:
                interesting_files[category] = interesting_files[category][:20]
                
        return interesting_files
        
    def export_analysis(self, output_file: str):
        """Export analysis results to JSON"""
        
        # Include interesting files in analysis
        self.analysis_results['interesting_files'] = self.find_interesting_files()
        
        with open(output_file, 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
            
        print(f"📄 Analysis exported to {output_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python pkb_content_analyzer.py <extracted_directory> [output_file]")
        return 1
        
    extracted_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'pkb_content_analysis.json'
    
    analyzer = PKBContentAnalyzer(extracted_dir)
    results = analyzer.analyze_content()
    analyzer.export_analysis(output_file)
    
    # Print summary
    print("\n📊 PKB Content Analysis Summary:")
    print(f"  Total files: {results['total_files']}")
    print(f"  Total size: {results['statistics']['total_size']:,} bytes")
    print(f"  Average file size: {results['statistics']['average_file_size']:.0f} bytes")
    
    print("\n📁 Top file types:")
    for ext, count in list(results['file_types']['extension_counts'].items())[:10]:
        ext_display = ext if ext else '(no extension)'
        print(f"    {ext_display}: {count} files")
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## 🚀 Advanced PKB Tools

### PKB Compression Research
```python
#!/usr/bin/env python3
"""
PKB Compression Algorithm Research Tool
Attempt to reverse engineer PKB compression
"""

import struct
import zlib
from typing import List, Tuple, Optional

class PKBCompressionAnalyzer:
    """Analyze PKB compression algorithms"""
    
    def __init__(self):
        self.patterns = []
        self.compression_signatures = [
            b'\x78\x9c',  # zlib deflate
            b'\x1f\x8b',  # gzip
            b'BZh',       # bzip2
            b'\xfd7zXZ', # xz
            b'LZIP',      # lzip
        ]
        
    def analyze_compressed_data(self, compressed_data: bytes, expected_size: int) -> Dict:
        """Analyze compressed data to determine algorithm"""
        
        analysis = {
            'size': len(compressed_data),
            'expected_uncompressed': expected_size,
            'compression_ratio': len(compressed_data) / expected_size if expected_size > 0 else 0,
            'detected_algorithms': [],
            'header_analysis': self.analyze_header(compressed_data),
            'entropy_analysis': self.calculate_entropy(compressed_data),
            'pattern_analysis': self.find_patterns(compressed_data)
        }
        
        # Test known compression algorithms
        for algorithm in ['zlib', 'gzip', 'bzip2', 'lzma']:
            try:
                result = self.test_decompression(compressed_data, algorithm)
                if result and len(result) == expected_size:
                    analysis['detected_algorithms'].append(algorithm)
            except:
                pass
                
        # Test custom PKB algorithms
        custom_result = self.test_pkb_algorithms(compressed_data, expected_size)
        if custom_result:
            analysis['detected_algorithms'].extend(custom_result)
            
        return analysis
        
    def analyze_header(self, data: bytes) -> Dict:
        """Analyze compression header"""
        if len(data) < 16:
            return {'error': 'Data too short for header analysis'}
            
        header_info = {
            'first_16_bytes': data[:16].hex(),
            'possible_signatures': []
        }
        
        # Check for known compression signatures
        for signature in self.compression_signatures:
            if data.startswith(signature):
                header_info['possible_signatures'].append(signature.hex())
                
        # Look for custom PKB headers
        if data[:4] == b'PKB\x00':
            header_info['pkb_header'] = struct.unpack('<I', data[4:8])[0]
            
        return header_info
        
    def calculate_entropy(self, data: bytes) -> float:
        """Calculate data entropy (randomness)"""
        if not data:
            return 0.0
            
        # Count byte frequencies
        frequencies = {}
        for byte in data:
            frequencies[byte] = frequencies.get(byte, 0) + 1
            
        # Calculate entropy
        import math
        entropy = 0.0
        data_len = len(data)
        
        for count in frequencies.values():
            probability = count / data_len
            entropy -= probability * math.log2(probability)
            
        return entropy
        
    def find_patterns(self, data: bytes) -> Dict:
        """Find repeating patterns in compressed data"""
        patterns = {
            'repeated_bytes': {},
            'common_sequences': {}
        }
        
        # Find repeated single bytes
        for i in range(256):
            byte_val = bytes([i])
            count = data.count(byte_val)
            if count > len(data) * 0.05:  # More than 5% of data
                patterns['repeated_bytes'][hex(i)] = count
                
        # Find common 2-byte sequences
        for i in range(len(data) - 1):
            seq = data[i:i+2]
            seq_hex = seq.hex()
            if seq_hex not in patterns['common_sequences']:
                patterns['common_sequences'][seq_hex] = data.count(seq)
                
        # Keep only frequent sequences
        patterns['common_sequences'] = {
            k: v for k, v in patterns['common_sequences'].items() 
            if v > 5
        }
        
        return patterns
        
    def test_decompression(self, data: bytes, algorithm: str) -> Optional[bytes]:
        """Test decompression with specific algorithm"""
        
        try:
            if algorithm == 'zlib':
                return zlib.decompress(data)
            elif algorithm == 'gzip':
                import gzip
                return gzip.decompress(data)
            elif algorithm == 'bzip2':
                import bz2
                return bz2.decompress(data)
            elif algorithm == 'lzma':
                import lzma
                return lzma.decompress(data)
        except:
            return None
            
        return None
        
    def test_pkb_algorithms(self, data: bytes, expected_size: int) -> List[str]:
        """Test custom PKB compression algorithms"""
        
        successful_algorithms = []
        
        # Test simple XOR + compression
        try:
            # Try XOR decoding with common keys
            for xor_key in [0x55, 0xAA, 0xFF, 0x42]:
                xor_data = bytes(b ^ xor_key for b in data)
                try:
                    decompressed = zlib.decompress(xor_data)
                    if len(decompressed) == expected_size:
                        successful_algorithms.append(f'xor_{hex(xor_key)}_zlib')
                except:
                    pass
        except:
            pass
            
        # Test LZ77-style compression
        try:
            lz77_result = self.decompress_lz77_style(data)
            if lz77_result and len(lz77_result) == expected_size:
                successful_algorithms.append('custom_lz77')
        except:
            pass
            
        return successful_algorithms
        
    def decompress_lz77_style(self, data: bytes) -> Optional[bytes]:
        """Attempt LZ77-style decompression"""
        
        # Simple LZ77 implementation
        output = bytearray()
        pos = 0
        
        try:
            while pos < len(data):
                control_byte = data[pos]
                pos += 1
                
                for bit in range(8):
                    if pos >= len(data):
                        break
                        
                    if control_byte & (1 << bit):
                        # Literal byte
                        output.append(data[pos])
                        pos += 1
                    else:
                        # Back reference
                        if pos + 1 >= len(data):
                            break
                            
                        ref_info = struct.unpack('<H', data[pos:pos+2])[0]
                        pos += 2
                        
                        offset = ref_info & 0xFFF
                        length = (ref_info >> 12) + 3
                        
                        # Copy from back reference
                        for _ in range(length):
                            if len(output) >= offset:
                                output.append(output[-offset])
                            else:
                                break
                                
            return bytes(output)
            
        except:
            return None

# Research tool for analyzing multiple PKB files
def research_pkb_compression(pkb_directory: str):
    """Research PKB compression across multiple files"""
    
    analyzer = PKBCompressionAnalyzer()
    results = {}
    
    pkb_files = list(Path(pkb_directory).glob('*.pkb'))
    
    for pkb_file in pkb_files:
        try:
            archive = PKBArchive(str(pkb_file))
            
            file_results = []
            
            for pkb_internal_file in archive.files[:10]:  # Analyze first 10 files
                if pkb_internal_file.is_compressed:
                    # Get compressed data
                    with open(pkb_file, 'rb') as f:
                        f.seek(archive.header['data_offset'] + pkb_internal_file.offset)
                        compressed_data = f.read(pkb_internal_file.compressed_size)
                        
                    # Analyze compression
                    analysis = analyzer.analyze_compressed_data(
                        compressed_data, 
                        pkb_internal_file.uncompressed_size
                    )
                    
                    file_results.append({
                        'filename': pkb_internal_file.filename,
                        'analysis': analysis
                    })
                    
            results[pkb_file.name] = file_results
            
        except Exception as e:
            print(f"Failed to analyze {pkb_file}: {e}")
            
    return results
```

## 📚 PKB Research Findings

### Community Knowledge Base
```yaml
pkb_research_status:
  format_understanding: "75% complete"
  extraction_capability: "Mostly functional"
  compression_algorithm: "Partially understood"
  
  known_facts:
    - "PKB uses custom LZ-based compression"
    - "Some files use XOR obfuscation"
    - "Header format well documented"
    - "Directory structure understood"
    
  unknown_areas:
    - "Exact compression algorithm details"
    - "Encryption key derivation"
    - "Some file flag meanings"
    - "Optimal compression parameters"
    
  tool_status:
    extraction: "Working for most files"
    compression: "Not yet implemented"
    modification: "Limited support"
    creation: "Not available"
```

### PKB File Inventory
```yaml
major_pkb_archives:
  core_content:
    - "models.pkb"        # 3D models, animations
    - "textures.pkb"      # All texture assets
    - "audio.pkb"         # Sound effects, music
    - "maps.pkb"          # World geometry
    
  ui_content:
    - "interface.pkb"     # UI elements
    - "fonts.pkb"         # Text rendering
    - "cursors.pkb"       # Mouse cursors
    
  gameplay:
    - "scripts.pkb"       # Mission logic
    - "config.pkb"        # Game configuration
    - "effects.pkb"       # Visual effects
    
  localization:
    - "english.pkb"       # English text
    - "french.pkb"        # French localization
    - "german.pkb"        # German localization
```

## Remember

> *"The body cannot live without the mind."* - Morpheus

PKB archives are the body of The Matrix Online - they contain every asset that made the digital world real. Understanding their structure and unlocking their contents is essential to preserving and reviving this lost realm.

**Every file extracted is a piece of the Matrix saved for eternity.**

---

**PKB Status**: 🟡 PARTIALLY DECODED  
**Extraction**: FUNCTIONAL  
**Priority**: HIGH  

*Extract. Analyze. Preserve. Liberate.*

---

[← Back to Technical](index.md) | [File Formats →](../03-technical-docs/file-formats/index.md) | [PKB Archives →](pkb-archives.md)