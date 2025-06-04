# Visual Preservation Archive
**Capturing the Digital Aesthetic of The Matrix**

> *"The image translators work for the construct program."* - Morpheus (And we preserve them all.)

## 🎨 Preservation Mission

The visual identity of The Matrix Online wasn't just graphics - it was a carefully crafted aesthetic that brought the Matrix mythology to life. Every screenshot, every texture, every UI element carries the digital DNA of this lost world. Our mission: preserve it all.

## 📸 Archive Categories

### Visual Content Taxonomy
```yaml
preservation_categories:
  screenshots:
    types: [gameplay, environments, characters, events]
    priority: critical
    formats: [png, jpg, tga]
    metadata: [timestamp, location, context]
    
  ui_elements:
    types: [menus, hud, interface, icons]
    priority: high
    formats: [png, vector_recreation]
    metadata: [screen_resolution, ui_version]
    
  textures:
    types: [txa_originals, converted_images, upscaled]
    priority: high
    formats: [txa, dds, png]
    metadata: [dimensions, compression, usage]
    
  promotional:
    types: [marketing, trailers, concept_art]
    priority: medium
    formats: [jpg, png, video]
    metadata: [release_date, campaign, source]
    
  community:
    types: [player_art, mods, recreations]
    priority: medium
    formats: [any]
    metadata: [creator, date, technique]
```

## 🗂️ Archive Structure

### Directory Organization
```bash
visual_archive/
├── 01_screenshots/
│   ├── gameplay/
│   │   ├── combat/
│   │   ├── exploration/
│   │   ├── social/
│   │   └── missions/
│   ├── environments/
│   │   ├── downtown/
│   │   ├── westview/
│   │   ├── international/
│   │   └── slums/
│   ├── characters/
│   │   ├── player_created/
│   │   ├── npcs/
│   │   └── iconic_characters/
│   └── events/
│       ├── live_events/
│       ├── cinematics/
│       └── special_occasions/
├── 02_ui_interface/
│   ├── menus/
│   ├── hud_elements/
│   ├── chat_interface/
│   ├── inventory/
│   └── character_creation/
├── 03_textures/
│   ├── originals/
│   │   ├── txa_files/
│   │   └── extracted/
│   ├── upscaled/
│   │   ├── ai_enhanced/
│   │   └── manual_recreations/
│   └── analysis/
│       ├── texture_maps/
│       └── usage_documentation/
├── 04_promotional/
│   ├── official_marketing/
│   ├── screenshots_press/
│   ├── concept_art/
│   └── video_stills/
├── 05_community/
│   ├── player_screenshots/
│   ├── fan_art/
│   ├── mod_screenshots/
│   └── recreations/
└── 06_metadata/
    ├── catalogs/
    ├── indexes/
    └── preservation_logs/
```

## 📊 Metadata Standards

### Image Metadata Schema
```json
{
  "image_metadata": {
    "file_info": {
      "filename": "downtown_zion_hq_001.png",
      "original_filename": "screenshot_20050812_143022.jpg",
      "file_size": 2457600,
      "dimensions": "1024x768",
      "format": "PNG",
      "compression": "lossless",
      "creation_date": "2005-08-12T14:30:22Z",
      "preservation_date": "2025-12-04T10:15:00Z"
    },
    "content_info": {
      "category": "screenshot",
      "subcategory": "environment",
      "location": "Downtown Zion HQ",
      "coordinates": [-392, 2, -1552],
      "district": "Downtown",
      "description": "Interior view of Zion headquarters main lobby",
      "subjects": ["architecture", "interior_design", "zion_aesthetic"],
      "quality_rating": "high",
      "rarity": "common"
    },
    "technical_info": {
      "original_resolution": "1024x768",
      "color_depth": 24,
      "has_transparency": false,
      "enhancement_applied": false,
      "source_type": "in_game_screenshot",
      "capture_method": "printscreen",
      "post_processing": "none"
    },
    "preservation_info": {
      "source": "community_submission",
      "submitter": "neo_awakened_2005",
      "verification_status": "verified",
      "backup_locations": [
        "archive.org",
        "community_mirror_1",
        "preservation_database"
      ],
      "access_level": "public",
      "copyright_status": "fair_use_preservation"
    },
    "contextual_info": {
      "game_version": "1.0",
      "patch_level": "initial_release",
      "server": "syntax",
      "character_name": "redpill_user",
      "time_period": "pre_closure",
      "historical_significance": "shows_original_zion_layout",
      "related_events": ["beta_testing", "launch_period"],
      "mission_context": "tutorial_sequence"
    }
  }
}
```

### Batch Metadata Generation
```python
#!/usr/bin/env python3
"""Automated metadata generation for MXO visual archive"""

import os
import json
from PIL import Image
from PIL.ExifTags import TAGS
import hashlib
from datetime import datetime
import re

class VisualArchiveMetadata:
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.metadata_db = {}
        self.location_patterns = self.load_location_patterns()
        
    def load_location_patterns(self):
        """Load regex patterns to identify locations from filenames"""
        return {
            'downtown': r'(?i)(downtown|richland|zion.*hq|tabor.*park)',
            'westview': r'(?i)(westview|machine.*hq|apartment)',
            'international': r'(?i)(international|merovingian|le.*vrai|museum)',
            'slums': r'(?i)(slums|warehouse|industrial|power.*plant)',
            'subway': r'(?i)(subway|mara.*central|station|platform)',
            'rooftop': r'(?i)(rooftop|roof|aerial|helicopter.*pad)'
        }
        
    def process_image(self, file_path):
        """Generate comprehensive metadata for a single image"""
        try:
            # Basic file info
            file_stats = os.stat(file_path)
            filename = os.path.basename(file_path)
            
            # Open image to get technical details
            with Image.open(file_path) as img:
                width, height = img.size
                format_type = img.format
                mode = img.mode
                
                # Extract EXIF data if available
                exif_data = {}
                if hasattr(img, '_getexif') and img._getexif():
                    exif = img._getexif()
                    for tag, value in exif.items():
                        tag_name = TAGS.get(tag, tag)
                        exif_data[tag_name] = value
                        
            # Generate file hash for integrity checking
            file_hash = self.calculate_file_hash(file_path)
            
            # Analyze filename for content clues
            content_analysis = self.analyze_filename(filename)
            
            # Create metadata object
            metadata = {
                'file_info': {
                    'filename': filename,
                    'full_path': file_path,
                    'file_size': file_stats.st_size,
                    'dimensions': f"{width}x{height}",
                    'format': format_type,
                    'color_mode': mode,
                    'creation_date': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                    'modification_date': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                    'hash_sha256': file_hash
                },
                'content_analysis': content_analysis,
                'exif_data': exif_data,
                'preservation_info': {
                    'processed_date': datetime.now().isoformat(),
                    'processor_version': '1.0',
                    'verification_status': 'auto_processed'
                }
            }
            
            return metadata
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
            
    def analyze_filename(self, filename):
        """Extract content information from filename patterns"""
        analysis = {
            'detected_location': 'unknown',
            'likely_category': 'unknown',
            'confidence': 'low',
            'extracted_info': {}
        }
        
        filename_lower = filename.lower()
        
        # Check for location patterns
        for location, pattern in self.location_patterns.items():
            if re.search(pattern, filename):
                analysis['detected_location'] = location
                analysis['confidence'] = 'medium'
                break
                
        # Check for category indicators
        if any(term in filename_lower for term in ['screenshot', 'capture', 'screen']):
            analysis['likely_category'] = 'screenshot'
        elif any(term in filename_lower for term in ['ui', 'interface', 'menu', 'hud']):
            analysis['likely_category'] = 'ui_element'
        elif any(term in filename_lower for term in ['texture', 'txa', 'material']):
            analysis['likely_category'] = 'texture'
        elif any(term in filename_lower for term in ['concept', 'art', 'promotional']):
            analysis['likely_category'] = 'promotional'
            
        # Extract date if present in filename
        date_match = re.search(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})', filename)
        if date_match:
            analysis['extracted_info']['date'] = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
            
        # Extract resolution if present
        res_match = re.search(r'(\d{3,4})x(\d{3,4})', filename)
        if res_match:
            analysis['extracted_info']['resolution'] = f"{res_match.group(1)}x{res_match.group(2)}"
            
        return analysis
        
    def calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash for file integrity"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
        
    def process_directory(self, directory_path):
        """Process all images in a directory"""
        supported_formats = {'.jpg', '.jpeg', '.png', '.tga', '.bmp', '.tiff'}
        processed_count = 0
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in supported_formats:
                    print(f"Processing: {file}")
                    metadata = self.process_image(file_path)
                    
                    if metadata:
                        self.metadata_db[file_path] = metadata
                        processed_count += 1
                        
        print(f"Processed {processed_count} images")
        return self.metadata_db
        
    def generate_catalog(self, output_path):
        """Generate searchable catalog of all images"""
        catalog = {
            'archive_info': {
                'creation_date': datetime.now().isoformat(),
                'total_images': len(self.metadata_db),
                'processor_version': '1.0',
                'description': 'Matrix Online Visual Preservation Archive Catalog'
            },
            'images': []
        }
        
        for file_path, metadata in self.metadata_db.items():
            catalog_entry = {
                'id': hashlib.md5(file_path.encode()).hexdigest()[:12],
                'filename': metadata['file_info']['filename'],
                'path': file_path,
                'dimensions': metadata['file_info']['dimensions'],
                'size': metadata['file_info']['file_size'],
                'category': metadata['content_analysis']['likely_category'],
                'location': metadata['content_analysis']['detected_location'],
                'hash': metadata['file_info']['hash_sha256']
            }
            catalog['images'].append(catalog_entry)
            
        # Save catalog
        with open(output_path, 'w') as f:
            json.dump(catalog, f, indent=2)
            
        return catalog
        
    def create_duplicate_report(self):
        """Find potential duplicate images by hash"""
        hash_map = {}
        duplicates = []
        
        for file_path, metadata in self.metadata_db.items():
            file_hash = metadata['file_info']['hash_sha256']
            
            if file_hash in hash_map:
                duplicates.append({
                    'hash': file_hash,
                    'files': [hash_map[file_hash], file_path],
                    'size': metadata['file_info']['file_size']
                })
            else:
                hash_map[file_hash] = file_path
                
        return duplicates

if __name__ == "__main__":
    # Process visual archive
    processor = VisualArchiveMetadata("/path/to/visual_archive")
    metadata = processor.process_directory("/path/to/visual_archive")
    
    # Generate catalog
    catalog = processor.generate_catalog("visual_archive_catalog.json")
    
    # Check for duplicates
    duplicates = processor.create_duplicate_report()
    
    print(f"Archive processing complete:")
    print(f"- {len(metadata)} images processed")
    print(f"- {len(duplicates)} potential duplicates found")
    print(f"- Catalog saved to visual_archive_catalog.json")
```

## 🔍 Screenshot Collection Priorities

### Critical Screenshots Needed
```yaml
high_priority_captures:
  character_creation:
    description: "Complete character creation process"
    frames_needed: 15
    specific_shots:
      - "Initial face selection grid"
      - "Hair style options"
      - "Clothing customization"
      - "Final character preview"
      
  faction_headquarters:
    description: "All three faction bases in detail"
    locations:
      - zion_hq: [-392, 2, -1552]
      - machine_center: [-2567, 45, -1234]
      - le_vrai: [-456, 12, 234]
    angles: ["exterior", "main_entrance", "interior_lobby", "command_center"]
    
  combat_system:
    description: "Interlock and free-fire combat"
    shots_needed:
      - "Interlock grid selection"
      - "Combat abilities menu"
      - "Damage effects"
      - "Victory/defeat screens"
      
  ui_elements:
    description: "Every interface element"
    priority: critical
    elements:
      - "Main HUD layout"
      - "Chat interface"
      - "Inventory screens"
      - "Mission log"
      - "Map interface"
      - "Options menus"
```

### Community Screenshot Drives
```yaml
community_collection_campaigns:
  "redpill_memories":
    description: "Personal player screenshots from 2005-2009"
    target: 1000
    current: 247
    reward: "Recognition in preservation credits"
    
  "rare_moments":
    description: "Unique events, glitches, easter eggs"
    target: 100
    current: 23
    reward: "Special archive contributor status"
    
  "complete_districts":
    description: "Every location in all four districts"
    target: 500
    current: 156
    reward: "Virtual tour creation collaboration"
    
  "ui_archaeology":
    description: "Interface evolution through patches"
    target: 200
    current: 34
    reward: "UI recreation project leadership"
```

## 🎨 Visual Enhancement Projects

### AI Upscaling Pipeline
```python
class MXOImageUpscaler:
    """AI-powered upscaling for Matrix Online visuals"""
    
    def __init__(self, model_path="esrgan_4x.pth"):
        self.model_path = model_path
        self.supported_formats = ['.jpg', '.png', '.tga']
        
    def upscale_image(self, input_path, output_path, scale_factor=4):
        """Upscale image using AI model"""
        try:
            # This would use Real-ESRGAN or similar
            command = f"realesrgan-ncnn-vulkan -i {input_path} -o {output_path} -s {scale_factor}"
            subprocess.run(command, shell=True, check=True)
            
            # Verify output quality
            return self.verify_upscale_quality(input_path, output_path)
            
        except subprocess.CalledProcessError as e:
            print(f"Upscaling failed: {e}")
            return False
            
    def batch_upscale(self, input_dir, output_dir, scale_factor=4):
        """Process entire directories"""
        processed = 0
        failed = 0
        
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in self.supported_formats):
                    input_path = os.path.join(root, file)
                    
                    # Maintain directory structure
                    rel_path = os.path.relpath(input_path, input_dir)
                    output_path = os.path.join(output_dir, rel_path)
                    
                    # Create output directory if needed
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    if self.upscale_image(input_path, output_path, scale_factor):
                        processed += 1
                    else:
                        failed += 1
                        
        return processed, failed
        
    def verify_upscale_quality(self, original, upscaled):
        """Basic quality verification"""
        try:
            from PIL import Image
            
            orig_img = Image.open(original)
            upsc_img = Image.open(upscaled)
            
            # Check if dimensions increased correctly
            orig_w, orig_h = orig_img.size
            upsc_w, upsc_h = upsc_img.size
            
            expected_w = orig_w * 4
            expected_h = orig_h * 4
            
            if upsc_w >= expected_w * 0.9 and upsc_h >= expected_h * 0.9:
                return True
                
        except Exception as e:
            print(f"Quality verification failed: {e}")
            
        return False
```

### Texture Recreation Project
```yaml
texture_recreation:
  project_scope:
    total_textures: 2847
    priority_textures: 450
    completed: 67
    in_progress: 23
    
  recreation_methods:
    ai_upscaling:
      description: "4x upscaling with Real-ESRGAN"
      quality: "good"
      automation: "high"
      
    manual_recreation:
      description: "Artist recreation from reference"
      quality: "excellent"
      automation: "none"
      
    procedural_generation:
      description: "Algorithm-based recreation"
      quality: "variable"
      automation: "medium"
      
  workflow:
    1: "Extract original TXA files"
    2: "Convert to standard formats"
    3: "Analyze texture properties"
    4: "Apply enhancement method"
    5: "Quality check and verification"
    6: "Community review"
    7: "Archive final version"
```

## 📱 Mobile Archive Access

### Progressive Web App
```javascript
// Matrix Online Visual Archive PWA
class MXOVisualArchive {
    constructor() {
        this.imageCache = new Map();
        this.metadataCache = new Map();
        this.currentView = 'grid';
        this.filters = {};
    }
    
    async loadCatalog() {
        try {
            const response = await fetch('visual_archive_catalog.json');
            const catalog = await response.json();
            
            this.images = catalog.images;
            this.totalImages = catalog.archive_info.total_images;
            
            this.renderGallery();
            
        } catch (error) {
            console.error('Failed to load catalog:', error);
        }
    }
    
    renderGallery() {
        const container = document.getElementById('gallery-container');
        
        const filteredImages = this.filterImages();
        const html = filteredImages.map(image => this.createImageCard(image)).join('');
        
        container.innerHTML = html;
        
        // Lazy load images
        this.setupLazyLoading();
    }
    
    createImageCard(image) {
        return `
            <div class="image-card" data-id="${image.id}">
                <div class="image-container">
                    <img data-src="${image.path}" 
                         alt="${image.filename}"
                         class="lazy-image">
                    <div class="image-overlay">
                        <span class="category">${image.category}</span>
                        <span class="location">${image.location}</span>
                    </div>
                </div>
                <div class="image-info">
                    <h4>${image.filename}</h4>
                    <p>${image.dimensions} • ${this.formatFileSize(image.size)}</p>
                </div>
            </div>
        `;
    }
    
    setupLazyLoading() {
        const images = document.querySelectorAll('.lazy-image');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy-image');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    filterImages() {
        return this.images.filter(image => {
            if (this.filters.category && image.category !== this.filters.category) {
                return false;
            }
            if (this.filters.location && image.location !== this.filters.location) {
                return false;
            }
            if (this.filters.search) {
                const searchTerm = this.filters.search.toLowerCase();
                return image.filename.toLowerCase().includes(searchTerm);
            }
            return true;
        });
    }
    
    formatFileSize(bytes) {
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`;
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    const archive = new MXOVisualArchive();
    archive.loadCatalog();
});
```

## 🛡️ Preservation Standards

### Quality Guidelines
```yaml
image_quality_standards:
  screenshots:
    minimum_resolution: "800x600"
    preferred_resolution: "1024x768+"
    format: "PNG (lossless) or high-quality JPEG"
    compression: "minimal"
    alterations: "none (original captures only)"
    
  textures:
    format: "TXA original + PNG converted"
    enhancement: "acceptable if documented"
    upscaling: "AI upscaling permitted with attribution"
    recreation: "vector recreation encouraged"
    
  ui_elements:
    format: "PNG with transparency preserved"
    background: "transparent or original background"
    resolution: "native game resolution minimum"
    cropping: "minimal, preserve context"
    
  promotional:
    format: "highest available quality"
    source: "official sources preferred"
    watermarks: "remove if legally permissible"
    authenticity: "verify source and date"
```

### Legal Considerations
```yaml
preservation_ethics:
  copyright_approach:
    philosophy: "fair_use_preservation"
    justification: "historical_preservation"
    commercial_use: "prohibited"
    attribution: "always_provide_source"
    
  community_content:
    player_screenshots: "creator_retains_rights"
    submission_license: "preservation_use_only"
    attribution: "credit_original_creator"
    removal_requests: "honor_creator_wishes"
    
  enhancement_attribution:
    ai_upscaling: "note_enhancement_method"
    manual_recreation: "credit_artist"
    composite_works: "list_all_sources"
    derivative_works: "clear_transformation_note"
```

## 🌐 Distribution & Access

### Archive Hosting Strategy
```yaml
distribution_plan:
  primary_archive:
    host: "Internet Archive"
    url: "archive.org/details/matrix-online-visuals"
    backup_frequency: "weekly"
    access_level: "public"
    
  community_mirrors:
    - host: "GitHub LFS"
      capacity: "limited"
      purpose: "active_development"
      
    - host: "Discord CDN"
      capacity: "moderate" 
      purpose: "community_sharing"
      
    - host: "IPFS Network"
      capacity: "unlimited"
      purpose: "decentralized_backup"
      
  specialized_access:
    researchers:
      method: "bulk_download_links"
      format: "organized_ZIP_archives"
      
    developers:
      method: "API_access"
      format: "JSON_metadata_REST"
      
    casual_browsers:
      method: "web_gallery"
      format: "progressive_loading"
```

### API for Developers
```python
# Visual Archive API
from flask import Flask, jsonify, request, send_file
import json
import os
from functools import wraps

app = Flask(__name__)

def load_catalog():
    with open('visual_archive_catalog.json', 'r') as f:
        return json.load(f)

@app.route('/api/images')
def list_images():
    """List all images with filtering"""
    catalog = load_catalog()
    images = catalog['images']
    
    # Apply filters
    category = request.args.get('category')
    location = request.args.get('location')
    search = request.args.get('search')
    
    if category:
        images = [img for img in images if img['category'] == category]
    if location:
        images = [img for img in images if img['location'] == location]
    if search:
        search_lower = search.lower()
        images = [img for img in images if search_lower in img['filename'].lower()]
    
    # Pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    start = (page - 1) * per_page
    end = start + per_page
    
    return jsonify({
        'images': images[start:end],
        'total': len(images),
        'page': page,
        'per_page': per_page,
        'pages': (len(images) + per_page - 1) // per_page
    })

@app.route('/api/images/<image_id>')
def get_image_metadata(image_id):
    """Get detailed metadata for specific image"""
    catalog = load_catalog()
    
    image = next((img for img in catalog['images'] if img['id'] == image_id), None)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
        
    return jsonify(image)

@app.route('/api/images/<image_id>/download')
def download_image(image_id):
    """Download image file"""
    catalog = load_catalog()
    
    image = next((img for img in catalog['images'] if img['id'] == image_id), None)
    if not image:
        return jsonify({'error': 'Image not found'}), 404
        
    if os.path.exists(image['path']):
        return send_file(image['path'], as_attachment=True)
    else:
        return jsonify({'error': 'File not found on disk'}), 404

@app.route('/api/stats')
def archive_stats():
    """Get archive statistics"""
    catalog = load_catalog()
    images = catalog['images']
    
    stats = {
        'total_images': len(images),
        'categories': {},
        'locations': {},
        'formats': {},
        'total_size': 0
    }
    
    for image in images:
        # Count by category
        cat = image['category']
        stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
        
        # Count by location
        loc = image['location']
        stats['locations'][loc] = stats['locations'].get(loc, 0) + 1
        
        # Count by format
        ext = os.path.splitext(image['filename'])[1].lower()
        stats['formats'][ext] = stats['formats'].get(ext, 0) + 1
        
        # Sum file sizes
        stats['total_size'] += image['size']
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
```

## 🎯 Community Contribution Guide

### How to Submit Images
```markdown
# Contributing to the Visual Archive

## Submission Process

1. **Prepare Your Images**
   - Ensure original quality (no compression artifacts)
   - Include any available context/metadata
   - Remove personal information if desired

2. **Create Submission Package**
   ```
   submission_package/
   ├── images/
   │   ├── your_screenshot_001.png
   │   ├── your_screenshot_002.jpg
   │   └── ...
   ├── metadata.json
   └── submission_info.txt
   ```

3. **Fill Out Metadata**
   ```json
   {
     "submitter": "your_username",
     "submission_date": "2025-12-04",
     "images": [
       {
         "filename": "your_screenshot_001.png",
         "date_taken": "2005-08-15",
         "location": "Downtown Zion HQ",
         "description": "Main lobby during tutorial",
         "character_name": "optional",
         "server": "syntax",
         "additional_notes": "captured during beta"
       }
     ]
   }
   ```

4. **Submit Through**
   - GitHub Issues (preferred)
   - Discord uploads
   - Email to preservation team
   - Community forum posts

## Quality Guidelines

- **Original captures only** (no edited/filtered images)
- **Include context** when possible
- **Verify authenticity** before submitting
- **Respect others' privacy** (blur names if needed)
```

### Recognition System
```yaml
contributor_recognition:
  ranks:
    archivist:
      requirements: "5+ verified submissions"
      benefits: ["contributor badge", "archive access"]
      
    curator:
      requirements: "25+ submissions, metadata quality"
      benefits: ["review privileges", "batch upload access"]
      
    preservationist:
      requirements: "100+ submissions, quality improvements"
      benefits: ["admin access", "project leadership"]
      
  special_awards:
    "first_capture":
      description: "First to document specific content"
      recognition: "permanent archive credit"
      
    "quality_enhancement":
      description: "Significant improvement to existing content"
      recognition: "enhancement attribution"
      
    "lost_media_recovery":
      description: "Recovering previously lost content"
      recognition: "hero status in credits"
```

## Remember

> *"I know this steak doesn't exist. I know that when I put it in my mouth, the Matrix is telling my brain that it is juicy and delicious."* - Cypher

But the images are real. Every screenshot preserves a moment that existed in digital space. Every texture captures the artistic vision that brought the Matrix to life. We are the guardians of visual memory.

**Preserve what was. Enhance what can be. Never let it fade to black.**

---

**Archive Status**: 🟡 ACTIVE COLLECTION  
**Visual Legacy**: PRESERVED  
**Enhancement**: ONGOING  

*See what was. Save what is. Share what matters.*

---

[← Back to Game Content](index.md) | [Screenshot Guide →](screenshot-guide.md) | [Texture Archive →](texture-archive.md)