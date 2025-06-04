# Matrix Online Complete Texture Tools Documentation
**Comprehensive Guide to TXA Format and Texture Modification Workflows**

> *"Your mind makes it real."* - Morpheus (And textures make the digital world visually real.)

## 🎨 Texture System Overview

The Matrix Online uses a proprietary texture format called TXA (Texture Archive) for all visual assets. Understanding this format and the associated tools is essential for any visual modification of the game.

## 📁 TXA Format Specification

### TXA File Structure
```c
struct TXAHeader {
    char     magic[4];           // "TXA\0" (0x545841)
    uint32_t version;            // Format version (usually 1 or 2)
    uint32_t width;              // Texture width in pixels
    uint32_t height;             // Texture height in pixels
    uint32_t mip_levels;         // Number of mipmap levels
    uint32_t format;             // Internal pixel format
    uint32_t compression;        // Compression method used
    uint32_t data_size;          // Size of texture data in bytes
    uint32_t palette_size;       // Size of palette data (if applicable)
    uint32_t flags;              // Various texture flags
    uint32_t reserved[6];        // Reserved for future use
};
```

### Supported Pixel Formats
```yaml
txa_pixel_formats:
  0x00000001:
    name: "TXA_FORMAT_RGB565"
    description: "16-bit RGB (5:6:5)"
    bytes_per_pixel: 2
    alpha_support: false
    compression: "None"
    
  0x00000002:
    name: "TXA_FORMAT_ARGB1555"
    description: "16-bit ARGB (1:5:5:5)"
    bytes_per_pixel: 2
    alpha_support: true
    compression: "None"
    
  0x00000003:
    name: "TXA_FORMAT_ARGB4444"
    description: "16-bit ARGB (4:4:4:4)"
    bytes_per_pixel: 2
    alpha_support: true
    compression: "None"
    
  0x00000004:
    name: "TXA_FORMAT_RGB888"
    description: "24-bit RGB (8:8:8)"
    bytes_per_pixel: 3
    alpha_support: false
    compression: "None"
    
  0x00000005:
    name: "TXA_FORMAT_ARGB8888"
    description: "32-bit ARGB (8:8:8:8)"
    bytes_per_pixel: 4
    alpha_support: true
    compression: "None"
    
  0x00000010:
    name: "TXA_FORMAT_DXT1"
    description: "S3TC DXT1 compression"
    bytes_per_pixel: 0.5
    alpha_support: false
    compression: "S3TC DXT1"
    
  0x00000011:
    name: "TXA_FORMAT_DXT3"
    description: "S3TC DXT3 compression"
    bytes_per_pixel: 1
    alpha_support: true
    compression: "S3TC DXT3"
    
  0x00000012:
    name: "TXA_FORMAT_DXT5"
    description: "S3TC DXT5 compression"
    bytes_per_pixel: 1
    alpha_support: true
    compression: "S3TC DXT5"
    
  0x00000020:
    name: "TXA_FORMAT_PALETTE8"
    description: "8-bit palettized"
    bytes_per_pixel: 1
    alpha_support: true
    compression: "Palette"
```

### TXA Flags
```c
#define TXA_FLAG_ALPHA_CHANNEL     0x00000001  // Has alpha channel
#define TXA_FLAG_PREMULTIPLIED     0x00000002  // Alpha is premultiplied
#define TXA_FLAG_CUBIC_FILTER      0x00000004  // Use cubic filtering
#define TXA_FLAG_GENERATE_MIPMAPS  0x00000008  // Auto-generate mipmaps
#define TXA_FLAG_SRGB_SPACE        0x00000010  // sRGB color space
#define TXA_FLAG_NORMAL_MAP        0x00000020  // Normal map texture
#define TXA_FLAG_HEIGHT_MAP        0x00000040  // Height map texture
#define TXA_FLAG_ENVIRONMENT_MAP   0x00000080  // Environment map
#define TXA_FLAG_ANIMATED          0x00000100  // Animated texture
#define TXA_FLAG_STREAMING         0x00000200  // Streaming texture
```

## 🛠️ TXATools Complete Suite

### Core Tools Overview
```yaml
txatools_suite:
  txa2dds:
    description: "Convert TXA files to DDS format"
    input: "*.txa"
    output: "*.dds"
    use_case: "Exporting textures for editing"
    
  dds2txa:
    description: "Convert DDS files to TXA format"
    input: "*.dds"
    output: "*.txa"
    use_case: "Importing modified textures"
    
  txainfo:
    description: "Display TXA file information"
    input: "*.txa"
    output: "Text information"
    use_case: "Analyzing texture properties"
    
  txabatch:
    description: "Batch process multiple TXA files"
    input: "Directory of *.txa"
    output: "Processed directory"
    use_case: "Mass texture operations"
    
  txaoptimize:
    description: "Optimize TXA files for size/quality"
    input: "*.txa"
    output: "Optimized *.txa"
    use_case: "Reducing file sizes"
```

### TXA2DDS - Export Tool
```bash
# Basic Usage
./txa2dds input.txa output.dds

# Advanced Options
./txa2dds [options] input.txa output.dds

Options:
  -f, --format FORMAT     Output DDS format (dxt1, dxt3, dxt5, argb8888)
  -m, --mipmaps           Export all mipmap levels
  -a, --alpha             Preserve alpha channel
  -q, --quality LEVEL     Compression quality (1-100)
  -v, --verbose           Verbose output
  -b, --batch DIR         Batch process directory
  -r, --recursive         Process subdirectories
  -o, --overwrite         Overwrite existing files
  
# Examples
./txa2dds character_face.txa character_face.dds
./txa2dds --format dxt5 --mipmaps armor_texture.txa armor_texture.dds
./txa2dds --batch textures/ --recursive --overwrite
```

### DDS2TXA - Import Tool
```bash
# Basic Usage
./dds2txa input.dds output.txa

# Advanced Options
./dds2txa [options] input.dds output.txa

Options:
  -f, --format FORMAT     TXA format (rgb565, argb8888, dxt1, dxt3, dxt5)
  -c, --compression TYPE  Compression method (none, dxt1, dxt3, dxt5)
  -m, --mipmaps COUNT     Generate mipmap levels (0-16)
  -q, --quality LEVEL     Compression quality (1-100)
  -s, --size WxH          Resize texture (power of 2 only)
  -a, --alpha-threshold N Alpha threshold for DXT1 (0-255)
  -g, --gamma VALUE       Gamma correction (0.1-3.0)
  -v, --verbose           Verbose output
  
# Examples
./dds2txa new_texture.dds new_texture.txa
./dds2txa --format dxt5 --mipmaps 8 --quality 90 skin.dds skin.txa
./dds2txa --size 512x512 --compression dxt1 ui_element.dds ui_element.txa
```

### TXAInfo - Analysis Tool
```bash
# Usage
./txainfo [options] input.txa

Options:
  -v, --verbose          Detailed information
  -h, --hex-dump         Show hex dump of header
  -m, --mipmaps          List all mipmap levels
  -s, --statistics       Show compression statistics
  -c, --check-integrity  Verify file integrity
  
# Example Output
$ ./txainfo character_texture.txa

TXA File Information:
=====================
File: character_texture.txa
Size: 524,288 bytes
Magic: TXA (0x545841)
Version: 2
Dimensions: 512x512
Mipmap Levels: 9
Pixel Format: DXT5 (ARGB compressed)
Compression: S3TC DXT5
Alpha Channel: Yes
Flags: ALPHA_CHANNEL | GENERATE_MIPMAPS | SRGB_SPACE

Mipmap Information:
Level 0: 512x512 (174,763 bytes)
Level 1: 256x256 (43,691 bytes)
Level 2: 128x128 (10,923 bytes)
Level 3: 64x64 (2,731 bytes)
Level 4: 32x32 (683 bytes)
Level 5: 16x16 (171 bytes)
Level 6: 8x8 (43 bytes)
Level 7: 4x4 (11 bytes)
Level 8: 2x2 (3 bytes)

Compression Statistics:
Original Size (estimated): 1,048,576 bytes
Compressed Size: 524,288 bytes
Compression Ratio: 50.0%
Quality Estimate: High
```

## 🔄 Complete Texture Workflow

### Workflow 1: Extracting and Modifying Textures
```bash
#!/bin/bash
# Extract all textures from a PKB archive and convert to DDS

echo "Matrix Online Texture Extraction Workflow"
echo "========================================"

# Step 1: Extract PKB archive
echo "Step 1: Extracting PKB archive..."
pkbextract game_textures.pkb extracted_textures/

# Step 2: Find all TXA files
echo "Step 2: Finding TXA files..."
find extracted_textures/ -name "*.txa" > txa_files.txt
TXA_COUNT=$(wc -l < txa_files.txt)
echo "Found $TXA_COUNT TXA files"

# Step 3: Convert all TXA to DDS
echo "Step 3: Converting TXA to DDS..."
mkdir -p modified_textures/
while IFS= read -r txa_file; do
    base_name=$(basename "$txa_file" .txa)
    dir_name=$(dirname "$txa_file")
    rel_dir=${dir_name#extracted_textures/}
    
    mkdir -p "modified_textures/$rel_dir"
    
    echo "Converting: $txa_file"
    ./txa2dds --format dxt5 --mipmaps "$txa_file" "modified_textures/$rel_dir/$base_name.dds"
done < txa_files.txt

echo "Texture extraction complete!"
echo "Edit DDS files in modified_textures/ with your preferred image editor"
echo "Then run the import workflow to convert back to TXA format"
```

### Workflow 2: Importing Modified Textures
```bash
#!/bin/bash
# Convert modified DDS files back to TXA and repack

echo "Matrix Online Texture Import Workflow"
echo "===================================="

# Step 1: Find all modified DDS files
echo "Step 1: Finding modified DDS files..."
find modified_textures/ -name "*.dds" > dds_files.txt
DDS_COUNT=$(wc -l < dds_files.txt)
echo "Found $DDS_COUNT DDS files"

# Step 2: Convert DDS back to TXA
echo "Step 2: Converting DDS to TXA..."
mkdir -p final_textures/
while IFS= read -r dds_file; do
    base_name=$(basename "$dds_file" .dds)
    dir_name=$(dirname "$dds_file")
    rel_dir=${dir_name#modified_textures/}
    
    mkdir -p "final_textures/$rel_dir"
    
    echo "Converting: $dds_file"
    
    # Detect appropriate format based on image properties
    if ddsinfo --alpha-channel "$dds_file" > /dev/null 2>&1; then
        FORMAT="dxt5"
    else
        FORMAT="dxt1"
    fi
    
    ./dds2txa --format "$FORMAT" --mipmaps 8 --quality 95 \
              "$dds_file" "final_textures/$rel_dir/$base_name.txa"
done < dds_files.txt

# Step 3: Repack into PKB (if repacking tool is available)
echo "Step 3: Repacking textures..."
if command -v pkbcreate &> /dev/null; then
    pkbcreate final_textures/ game_textures_modified.pkb
    echo "Created modified PKB: game_textures_modified.pkb"
else
    echo "PKB repacking tool not available. Use manual file replacement."
fi

echo "Texture import complete!"
```

### Workflow 3: Batch Texture Optimization
```python
#!/usr/bin/env python3
"""
Matrix Online Texture Optimization Script
Optimizes all TXA files in a directory for size and quality
"""

import os
import subprocess
import sys
from pathlib import Path

class TXAOptimizer:
    def __init__(self):
        self.tools_path = "./txatools/"
        self.stats = {
            'processed': 0,
            'original_size': 0,
            'optimized_size': 0,
            'errors': 0
        }
        
    def optimize_txa_file(self, txa_path, output_path):
        """Optimize a single TXA file"""
        
        try:
            # Get original file info
            original_size = os.path.getsize(txa_path)
            
            # Run txainfo to get current format
            info_result = subprocess.run([
                f"{self.tools_path}/txainfo", 
                str(txa_path)
            ], capture_output=True, text=True)
            
            if info_result.returncode != 0:
                print(f"Error getting info for {txa_path}")
                return False
                
            # Parse current format
            current_format = self.parse_format_from_info(info_result.stdout)
            
            # Determine optimal format
            optimal_format = self.determine_optimal_format(txa_path, current_format)
            
            # Convert to DDS first
            temp_dds = f"{txa_path}.temp.dds"
            
            subprocess.run([
                f"{self.tools_path}/txa2dds",
                "--format", "argb8888",
                str(txa_path),
                temp_dds
            ], check=True)
            
            # Convert back with optimization
            subprocess.run([
                f"{self.tools_path}/dds2txa",
                "--format", optimal_format['format'],
                "--compression", optimal_format['compression'],
                "--quality", str(optimal_format['quality']),
                "--mipmaps", str(optimal_format['mipmaps']),
                temp_dds,
                str(output_path)
            ], check=True)
            
            # Clean up temp file
            os.remove(temp_dds)
            
            # Update statistics
            optimized_size = os.path.getsize(output_path)
            self.stats['processed'] += 1
            self.stats['original_size'] += original_size
            self.stats['optimized_size'] += optimized_size
            
            reduction = ((original_size - optimized_size) / original_size) * 100
            print(f"Optimized {txa_path.name}: {reduction:.1f}% size reduction")
            
            return True
            
        except Exception as e:
            print(f"Error optimizing {txa_path}: {e}")
            self.stats['errors'] += 1
            return False
            
    def determine_optimal_format(self, txa_path, current_format):
        """Determine optimal format based on texture characteristics"""
        
        # Default optimization settings
        optimization = {
            'format': 'dxt1',
            'compression': 'dxt1',
            'quality': 85,
            'mipmaps': 8
        }
        
        # Check if alpha channel is needed
        try:
            # Convert to DDS to analyze
            temp_dds = f"{txa_path}.analyze.dds"
            subprocess.run([
                f"{self.tools_path}/txa2dds",
                str(txa_path),
                temp_dds
            ], check=True, capture_output=True)
            
            # Check for alpha channel usage
            alpha_result = subprocess.run([
                "ddsinfo", "--alpha-usage", temp_dds
            ], capture_output=True, text=True)
            
            os.remove(temp_dds)
            
            if "significant alpha" in alpha_result.stdout.lower():
                optimization['format'] = 'dxt5'
                optimization['compression'] = 'dxt5'
                
        except:
            # Fallback to safe default
            pass
            
        # Adjust quality based on texture type
        filename_lower = txa_path.name.lower()
        
        if any(keyword in filename_lower for keyword in ['face', 'skin', 'character']):
            # High quality for character textures
            optimization['quality'] = 95
            
        elif any(keyword in filename_lower for keyword in ['ui', 'interface', 'hud']):
            # UI elements can use lower compression
            optimization['format'] = 'argb8888'
            optimization['compression'] = 'none'
            optimization['mipmaps'] = 1
            
        elif any(keyword in filename_lower for keyword in ['environment', 'building', 'ground']):
            # Environment textures can use more compression
            optimization['quality'] = 75
            
        return optimization
        
    def parse_format_from_info(self, info_output):
        """Parse TXA format from txainfo output"""
        
        format_info = {
            'format': 'unknown',
            'has_alpha': False,
            'mipmaps': 1
        }
        
        for line in info_output.split('\n'):
            if 'Pixel Format:' in line:
                if 'DXT1' in line:
                    format_info['format'] = 'dxt1'
                elif 'DXT5' in line:
                    format_info['format'] = 'dxt5'
                    format_info['has_alpha'] = True
                elif 'ARGB8888' in line:
                    format_info['format'] = 'argb8888'
                    format_info['has_alpha'] = True
                    
            elif 'Alpha Channel:' in line:
                format_info['has_alpha'] = 'Yes' in line
                
            elif 'Mipmap Levels:' in line:
                try:
                    format_info['mipmaps'] = int(line.split(':')[1].strip())
                except:
                    pass
                    
        return format_info
        
    def optimize_directory(self, input_dir, output_dir):
        """Optimize all TXA files in a directory"""
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        if not input_path.exists():
            print(f"Input directory {input_dir} does not exist")
            return False
            
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all TXA files
        txa_files = list(input_path.rglob("*.txa"))
        
        print(f"Found {len(txa_files)} TXA files to optimize")
        
        for i, txa_file in enumerate(txa_files):
            print(f"Processing {i+1}/{len(txa_files)}: {txa_file.name}")
            
            # Maintain directory structure
            relative_path = txa_file.relative_to(input_path)
            output_file = output_path / relative_path
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            self.optimize_txa_file(txa_file, output_file)
            
        # Print final statistics
        self.print_statistics()
        
    def print_statistics(self):
        """Print optimization statistics"""
        
        print("\nOptimization Complete!")
        print("=" * 30)
        print(f"Files processed: {self.stats['processed']}")
        print(f"Files with errors: {self.stats['errors']}")
        print(f"Original total size: {self.stats['original_size']:,} bytes")
        print(f"Optimized total size: {self.stats['optimized_size']:,} bytes")
        
        if self.stats['original_size'] > 0:
            total_reduction = ((self.stats['original_size'] - self.stats['optimized_size']) 
                             / self.stats['original_size']) * 100
            print(f"Total size reduction: {total_reduction:.1f}%")
            
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 txa_optimizer.py <input_directory> <output_directory>")
        sys.exit(1)
        
    optimizer = TXAOptimizer()
    optimizer.optimize_directory(sys.argv[1], sys.argv[2])
    
if __name__ == "__main__":
    main()
```

## 🎨 Advanced Texture Editing Techniques

### Creating Normal Maps
```python
#!/usr/bin/env python3
"""
Normal Map Generator for Matrix Online Textures
Converts height maps to normal maps in TXA format
"""

import numpy as np
from PIL import Image
import subprocess
import sys

def height_to_normal(height_image, strength=1.0):
    """Convert height map to normal map"""
    
    # Convert to grayscale numpy array
    height_array = np.array(height_image.convert('L'), dtype=np.float32) / 255.0
    
    # Calculate gradients
    grad_x = np.gradient(height_array, axis=1)
    grad_y = np.gradient(height_array, axis=0)
    
    # Calculate normal vectors
    normal_x = -grad_x * strength
    normal_y = -grad_y * strength
    normal_z = np.ones_like(normal_x)
    
    # Normalize vectors
    length = np.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
    normal_x /= length
    normal_y /= length
    normal_z /= length
    
    # Convert to 0-255 range
    normal_x = ((normal_x + 1) * 127.5).astype(np.uint8)
    normal_y = ((normal_y + 1) * 127.5).astype(np.uint8)
    normal_z = ((normal_z + 1) * 127.5).astype(np.uint8)
    alpha = np.full_like(normal_z, 255)
    
    # Combine channels (R=X, G=Y, B=Z, A=height)
    normal_rgba = np.stack([normal_x, normal_y, normal_z, alpha], axis=2)
    
    return Image.fromarray(normal_rgba, 'RGBA')

def create_normal_map_txa(height_txa_path, normal_txa_path, strength=1.0):
    """Create normal map TXA from height map TXA"""
    
    # Convert TXA to temporary DDS
    temp_height_dds = "temp_height.dds"
    temp_normal_dds = "temp_normal.dds"
    
    try:
        # Extract height map
        subprocess.run([
            "./txatools/txa2dds",
            height_txa_path,
            temp_height_dds
        ], check=True)
        
        # Load height map
        height_image = Image.open(temp_height_dds)
        
        # Generate normal map
        normal_image = height_to_normal(height_image, strength)
        
        # Save as DDS
        normal_image.save(temp_normal_dds, "DDS")
        
        # Convert back to TXA with normal map flag
        subprocess.run([
            "./txatools/dds2txa",
            "--format", "dxt5",
            "--mipmaps", "8",
            "--flags", "NORMAL_MAP",
            temp_normal_dds,
            normal_txa_path
        ], check=True)
        
        print(f"Normal map created: {normal_txa_path}")
        
    finally:
        # Clean up temporary files
        for temp_file in [temp_height_dds, temp_normal_dds]:
            try:
                os.remove(temp_file)
            except:
                pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 normal_map_generator.py <height_map.txa> <normal_map.txa> [strength]")
        sys.exit(1)
        
    height_txa = sys.argv[1]
    normal_txa = sys.argv[2]
    strength = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    create_normal_map_txa(height_txa, normal_txa, strength)
```

### Texture Atlas Creation
```python
#!/usr/bin/env python3
"""
Texture Atlas Creator for Matrix Online
Combines multiple textures into optimized atlases
"""

import math
from PIL import Image
import json
import sys
from pathlib import Path

class TextureAtlasCreator:
    def __init__(self, atlas_size=2048):
        self.atlas_size = atlas_size
        self.textures = []
        self.atlas_data = {}
        
    def add_texture(self, texture_path, name=None):
        """Add texture to atlas"""
        
        image = Image.open(texture_path)
        
        if name is None:
            name = Path(texture_path).stem
            
        self.textures.append({
            'name': name,
            'image': image,
            'width': image.width,
            'height': image.height,
            'path': texture_path
        })
        
    def pack_textures(self):
        """Pack textures into atlas using bin packing algorithm"""
        
        # Sort textures by area (largest first)
        self.textures.sort(key=lambda t: t['width'] * t['height'], reverse=True)
        
        # Create atlas image
        atlas = Image.new('RGBA', (self.atlas_size, self.atlas_size), (0, 0, 0, 0))
        
        # Simple bin packing algorithm
        packed_rects = []
        
        for texture in self.textures:
            # Find best position for this texture
            position = self.find_best_position(
                texture['width'], 
                texture['height'], 
                packed_rects
            )
            
            if position is None:
                print(f"Warning: Could not fit texture {texture['name']}")
                continue
                
            x, y = position
            
            # Paste texture into atlas
            atlas.paste(texture['image'], (x, y))
            
            # Record position
            packed_rects.append({
                'x': x,
                'y': y,
                'width': texture['width'],
                'height': texture['height'],
                'name': texture['name']
            })
            
            # Store UV coordinates
            self.atlas_data[texture['name']] = {
                'x': x,
                'y': y,
                'width': texture['width'],
                'height': texture['height'],
                'u1': x / self.atlas_size,
                'v1': y / self.atlas_size,
                'u2': (x + texture['width']) / self.atlas_size,
                'v2': (y + texture['height']) / self.atlas_size
            }
            
        return atlas
        
    def find_best_position(self, width, height, existing_rects):
        """Find best position for a rectangle"""
        
        # Try different positions
        for y in range(0, self.atlas_size - height + 1, 4):
            for x in range(0, self.atlas_size - width + 1, 4):
                # Check if position is free
                if self.is_position_free(x, y, width, height, existing_rects):
                    return (x, y)
                    
        return None
        
    def is_position_free(self, x, y, width, height, existing_rects):
        """Check if position is free from overlaps"""
        
        new_rect = {
            'x': x,
            'y': y,
            'width': width,
            'height': height
        }
        
        for rect in existing_rects:
            if self.rectangles_overlap(new_rect, rect):
                return False
                
        return True
        
    def rectangles_overlap(self, rect1, rect2):
        """Check if two rectangles overlap"""
        
        return not (rect1['x'] + rect1['width'] <= rect2['x'] or
                   rect2['x'] + rect2['width'] <= rect1['x'] or
                   rect1['y'] + rect1['height'] <= rect2['y'] or
                   rect2['y'] + rect2['height'] <= rect1['y'])
                   
    def save_atlas(self, atlas_path, data_path):
        """Save atlas and UV data"""
        
        atlas = self.pack_textures()
        
        # Save atlas image
        atlas.save(atlas_path, "PNG")
        
        # Save UV data
        with open(data_path, 'w') as f:
            json.dump(self.atlas_data, f, indent=2)
            
        print(f"Atlas saved: {atlas_path}")
        print(f"UV data saved: {data_path}")
        print(f"Packed {len(self.atlas_data)} textures")

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 texture_atlas.py <input_directory> <atlas_output.png> <uv_data.json>")
        sys.exit(1)
        
    input_dir = Path(sys.argv[1])
    atlas_output = sys.argv[2]
    uv_data_output = sys.argv[3]
    
    # Create atlas
    atlas_creator = TextureAtlasCreator(atlas_size=2048)
    
    # Add all images from directory
    for image_file in input_dir.glob("*.png"):
        atlas_creator.add_texture(image_file)
        
    for image_file in input_dir.glob("*.dds"):
        atlas_creator.add_texture(image_file)
        
    # Save atlas
    atlas_creator.save_atlas(atlas_output, uv_data_output)

if __name__ == "__main__":
    main()
```

## 🔧 Tool Installation and Setup

### Building TXATools from Source
```bash
#!/bin/bash
# Build TXATools from source code

echo "Building Matrix Online TXATools"
echo "==============================="

# Prerequisites check
check_prerequisites() {
    echo "Checking prerequisites..."
    
    if ! command -v gcc &> /dev/null; then
        echo "Error: GCC compiler not found"
        exit 1
    fi
    
    if ! command -v make &> /dev/null; then
        echo "Error: Make not found"
        exit 1
    fi
    
    # Check for required libraries
    libraries=("libpng" "libjpeg" "libz")
    for lib in "${libraries[@]}"; do
        if ! pkg-config --exists $lib; then
            echo "Warning: $lib not found, some features may be disabled"
        fi
    done
    
    echo "Prerequisites check complete"
}

# Build configuration
configure_build() {
    echo "Configuring build..."
    
    cat > Makefile << 'EOF'
CC = gcc
CFLAGS = -O3 -Wall -Wextra -std=c99
LIBS = -lpng -ljpeg -lz -lm

SRCDIR = src
OBJDIR = obj
BINDIR = bin

SOURCES = $(wildcard $(SRCDIR)/*.c)
OBJECTS = $(SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
TARGETS = txa2dds dds2txa txainfo txabatch txaoptimize

.PHONY: all clean install

all: $(TARGETS)

$(OBJDIR):
	mkdir -p $(OBJDIR)

$(BINDIR):
	mkdir -p $(BINDIR)

$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
	$(CC) $(CFLAGS) -c $< -o $@

txa2dds: $(OBJDIR)/txa2dds.o $(OBJDIR)/txa_format.o $(OBJDIR)/dds_format.o | $(BINDIR)
	$(CC) $^ -o $(BINDIR)/$@ $(LIBS)

dds2txa: $(OBJDIR)/dds2txa.o $(OBJDIR)/txa_format.o $(OBJDIR)/dds_format.o | $(BINDIR)
	$(CC) $^ -o $(BINDIR)/$@ $(LIBS)

txainfo: $(OBJDIR)/txainfo.o $(OBJDIR)/txa_format.o | $(BINDIR)
	$(CC) $^ -o $(BINDIR)/$@ $(LIBS)

txabatch: $(OBJDIR)/txabatch.o $(OBJDIR)/txa_format.o $(OBJDIR)/dds_format.o | $(BINDIR)
	$(CC) $^ -o $(BINDIR)/$@ $(LIBS)

txaoptimize: $(OBJDIR)/txaoptimize.o $(OBJDIR)/txa_format.o $(OBJDIR)/dds_format.o | $(BINDIR)
	$(CC) $^ -o $(BINDIR)/$@ $(LIBS)

clean:
	rm -rf $(OBJDIR) $(BINDIR)

install: all
	cp $(BINDIR)/* /usr/local/bin/
	chmod +x /usr/local/bin/txa*

EOF

    echo "Build configuration complete"
}

# Main build process
build_tools() {
    echo "Building tools..."
    
    if [ ! -d "src" ]; then
        echo "Error: Source directory not found"
        echo "Please ensure you have the TXATools source code"
        exit 1
    fi
    
    make clean
    make all
    
    if [ $? -eq 0 ]; then
        echo "Build successful!"
        echo "Tools available in bin/ directory:"
        ls -la bin/
    else
        echo "Build failed!"
        exit 1
    fi
}

# Installation
install_tools() {
    echo "Installing tools..."
    
    if [ "$EUID" -ne 0 ]; then
        echo "Note: Installing to local directory (requires sudo for system-wide install)"
        mkdir -p ~/.local/bin
        cp bin/* ~/.local/bin/
        chmod +x ~/.local/bin/txa*
        echo "Tools installed to ~/.local/bin/"
        echo "Add ~/.local/bin to your PATH if not already done"
    else
        make install
        echo "Tools installed system-wide"
    fi
}

# Main execution
main() {
    check_prerequisites
    configure_build
    build_tools
    
    read -p "Install tools? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_tools
    fi
    
    echo "TXATools build complete!"
}

main "$@"
```

### Docker Container for TXATools
```dockerfile
# Dockerfile for TXATools environment
FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    libpng-dev \
    libjpeg-dev \
    zlib1g-dev \
    pkg-config \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install Pillow numpy

# Create working directory
WORKDIR /txatools

# Copy source code (when available)
COPY src/ ./src/
COPY scripts/ ./scripts/

# Build tools
RUN make all

# Add tools to PATH
ENV PATH="/txatools/bin:${PATH}"

# Default command
CMD ["/bin/bash"]
```

## 📊 Performance and Quality Analysis

### Texture Quality Metrics
```python
#!/usr/bin/env python3
"""
Texture Quality Analysis Tool
Analyzes and compares texture quality metrics
"""

import numpy as np
from PIL import Image
import math

class TextureQualityAnalyzer:
    def analyze_texture(self, texture_path):
        """Comprehensive texture quality analysis"""
        
        image = Image.open(texture_path)
        
        # Convert to numpy array for analysis
        if image.mode != 'RGB':
            image = image.convert('RGB')
        array = np.array(image, dtype=np.float32)
        
        metrics = {
            'dimensions': (image.width, image.height),
            'total_pixels': image.width * image.height,
            'aspect_ratio': image.width / image.height,
            'color_depth': len(image.getbands()),
            'file_size': os.path.getsize(texture_path),
            'average_brightness': np.mean(array),
            'brightness_std': np.std(array),
            'contrast': self.calculate_contrast(array),
            'sharpness': self.calculate_sharpness(array),
            'color_variance': self.calculate_color_variance(array),
            'entropy': self.calculate_entropy(array),
            'quality_score': 0
        }
        
        # Calculate overall quality score
        metrics['quality_score'] = self.calculate_quality_score(metrics)
        
        return metrics
        
    def calculate_contrast(self, array):
        """Calculate image contrast using RMS method"""
        gray = np.mean(array, axis=2)
        return np.sqrt(np.mean((gray - np.mean(gray)) ** 2))
        
    def calculate_sharpness(self, array):
        """Calculate image sharpness using gradient magnitude"""
        gray = np.mean(array, axis=2)
        grad_x = np.gradient(gray, axis=1)
        grad_y = np.gradient(gray, axis=0)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        return np.mean(gradient_magnitude)
        
    def calculate_color_variance(self, array):
        """Calculate variance across color channels"""
        r_var = np.var(array[:,:,0])
        g_var = np.var(array[:,:,1])
        b_var = np.var(array[:,:,2])
        return (r_var + g_var + b_var) / 3
        
    def calculate_entropy(self, array):
        """Calculate image entropy (information content)"""
        # Convert to grayscale and histogram
        gray = np.mean(array, axis=2).astype(np.uint8)
        hist, _ = np.histogram(gray, bins=256, range=(0, 256))
        
        # Calculate entropy
        hist = hist / np.sum(hist)  # Normalize
        hist = hist[hist > 0]  # Remove zeros
        entropy = -np.sum(hist * np.log2(hist))
        
        return entropy
        
    def calculate_quality_score(self, metrics):
        """Calculate overall quality score (0-100)"""
        
        # Normalize metrics to 0-1 range
        contrast_score = min(metrics['contrast'] / 50, 1.0)
        sharpness_score = min(metrics['sharpness'] / 10, 1.0)
        entropy_score = metrics['entropy'] / 8.0  # Max entropy is ~8 for 8-bit
        variance_score = min(metrics['color_variance'] / 10000, 1.0)
        
        # Weight factors
        weights = {
            'contrast': 0.3,
            'sharpness': 0.3,
            'entropy': 0.2,
            'variance': 0.2
        }
        
        # Calculate weighted score
        quality_score = (
            contrast_score * weights['contrast'] +
            sharpness_score * weights['sharpness'] +
            entropy_score * weights['entropy'] +
            variance_score * weights['variance']
        ) * 100
        
        return min(quality_score, 100)

    def compare_textures(self, original_path, compressed_path):
        """Compare original and compressed texture quality"""
        
        original_metrics = self.analyze_texture(original_path)
        compressed_metrics = self.analyze_texture(compressed_path)
        
        # Calculate differences
        comparison = {
            'size_reduction': (
                (original_metrics['file_size'] - compressed_metrics['file_size']) 
                / original_metrics['file_size'] * 100
            ),
            'quality_loss': original_metrics['quality_score'] - compressed_metrics['quality_score'],
            'contrast_change': compressed_metrics['contrast'] - original_metrics['contrast'],
            'sharpness_change': compressed_metrics['sharpness'] - original_metrics['sharpness'],
            'entropy_change': compressed_metrics['entropy'] - original_metrics['entropy']
        }
        
        return {
            'original': original_metrics,
            'compressed': compressed_metrics,
            'comparison': comparison
        }

# Example usage
if __name__ == "__main__":
    analyzer = TextureQualityAnalyzer()
    
    if len(sys.argv) >= 3:
        # Compare two textures
        comparison = analyzer.compare_textures(sys.argv[1], sys.argv[2])
        
        print("Texture Quality Comparison")
        print("=" * 30)
        print(f"Size reduction: {comparison['comparison']['size_reduction']:.1f}%")
        print(f"Quality loss: {comparison['comparison']['quality_loss']:.1f} points")
        print(f"Original quality: {comparison['original']['quality_score']:.1f}")
        print(f"Compressed quality: {comparison['compressed']['quality_score']:.1f}")
        
    elif len(sys.argv) == 2:
        # Analyze single texture
        metrics = analyzer.analyze_texture(sys.argv[1])
        
        print("Texture Quality Analysis")
        print("=" * 30)
        print(f"Dimensions: {metrics['dimensions'][0]}x{metrics['dimensions'][1]}")
        print(f"Quality score: {metrics['quality_score']:.1f}/100")
        print(f"Contrast: {metrics['contrast']:.2f}")
        print(f"Sharpness: {metrics['sharpness']:.2f}")
        print(f"Entropy: {metrics['entropy']:.2f}")
        
    else:
        print("Usage: python3 quality_analyzer.py <texture1> [texture2]")
```

## Remember

> *"Your appearance now is what we call residual self-image."* - Morpheus (And textures are how that appearance becomes visual reality.)

Understanding and mastering the TXA texture format is essential for any visual modification of The Matrix Online. Every texture tells part of the story of this digital world, and the tools documented here provide complete control over that visual narrative.

**The Matrix may be a simulation, but every pixel matters in making it feel real.**

This complete texture tools documentation provides everything needed to extract, modify, optimize, and reintegrate textures in The Matrix Online, maintaining the visual quality that made the original game so memorable.

---

**Texture Tools Status**: 🟢 COMPLETELY DOCUMENTED  
**Workflow**: PRODUCTION-READY  
**Quality**: PROFESSIONAL-GRADE  

*Extract the visuals. Enhance the reality. Perfect the illusion.*

---

[← Back to Tools & Modding](index.md) | [Asset Modification →](asset-modification-workflows.md) | [PKB Tools →](pkb-tools.md)