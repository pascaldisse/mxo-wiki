#\!/usr/bin/env python3

import os
import re
from collections import defaultdict
from pathlib import Path

# Wiki root directory
WIKI_ROOT = Path("/Users/pascaldisse/mxoemu_forum_scrape/wiki")

# Regex pattern for markdown links
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Initialize counters
total_links = 0
working_links = 0
broken_links = 0
broken_link_counts = defaultdict(int)
broken_files = defaultdict(int)
broken_dirs = defaultdict(int)
link_sources = defaultdict(list)  # Track which files contain each broken link

# Find all markdown files
for root, dirs, files in os.walk(WIKI_ROOT):
    for file in files:
        if file.endswith('.md'):
            file_path = Path(root) / file
            rel_path = file_path.relative_to(WIKI_ROOT)
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Find all links in the file
            for match in LINK_PATTERN.finditer(content):
                link_text = match.group(1)
                link_target = match.group(2)
                
                # Skip external links, anchors, and empty links
                if (link_target.startswith('http://') or 
                    link_target.startswith('https://') or 
                    link_target.startswith('#') or 
                    not link_target):
                    continue
                
                # Remove anchor from link
                link_target = link_target.split('#')[0]
                if not link_target:
                    continue
                
                total_links += 1
                
                # Resolve the link path
                if link_target.startswith('/'):
                    # Absolute path from wiki root
                    target_path = WIKI_ROOT / link_target[1:]
                else:
                    # Relative path from current file's directory
                    target_path = (file_path.parent / link_target).resolve()
                
                # Check if target exists
                if target_path.exists():
                    working_links += 1
                else:
                    broken_links += 1
                    broken_link_counts[link_target] += 1
                    link_sources[link_target].append(str(rel_path))
                    
                    # Categorize as file or directory
                    if link_target.endswith('/'):
                        broken_dirs[link_target] += 1
                    else:
                        broken_files[link_target] += 1

# Generate report
print("=== MATRIX ONLINE WIKI LINK VALIDATION REPORT ===")
print(f"\nDate: Wiki Check Cycle 3 Phase 2")
print(f"Wiki Root: {WIKI_ROOT}")
print(f"\n=== OVERALL STATISTICS ===")
print(f"Total markdown files scanned: {sum(1 for _ in WIKI_ROOT.rglob('*.md'))}")
print(f"Total internal links found: {total_links}")
print(f"Working links: {working_links}")
print(f"Broken links: {broken_links}")
if total_links > 0:
    health = (working_links / total_links) * 100
    print(f"Wiki health: {health:.1f}%")
    print(f"\nComparison to previous cycle:")
    print(f"Previous: 751 links, 96 broken (87.2% health)")
    print(f"Current: {total_links} links, {broken_links} broken ({health:.1f}% health)")
    if health > 87.2:
        print(f"Improvement: +{health - 87.2:.1f}% health")
    else:
        print(f"Decline: {health - 87.2:.1f}% health")

print(f"\n=== BROKEN LINK CATEGORIES ===")
print(f"Missing files: {len(broken_files)} unique ({sum(broken_files.values())} total occurrences)")
print(f"Missing directories: {len(broken_dirs)} unique ({sum(broken_dirs.values())} total occurrences)")

print(f"\n=== TOP 10 MOST FREQUENTLY BROKEN LINKS ===")
sorted_broken = sorted(broken_link_counts.items(), key=lambda x: x[1], reverse=True)[:10]
for i, (link, count) in enumerate(sorted_broken, 1):
    print(f"{i}. [{count} occurrences] {link}")
    # Show first 3 source files for context
    sources = link_sources[link][:3]
    for source in sources:
        print(f"   - Found in: {source}")
    if len(link_sources[link]) > 3:
        print(f"   - And {len(link_sources[link]) - 3} more files...")

# Additional analysis
print(f"\n=== LINK PATTERNS ANALYSIS ===")
image_links = sum(1 for link in broken_link_counts if link.endswith(('.png', '.jpg', '.jpeg', '.gif')))
asset_links = sum(1 for link in broken_link_counts if '/assets/' in link)
relative_up = sum(1 for link in broken_link_counts if link.startswith('../'))

print(f"Broken image links: {image_links}")
print(f"Broken asset links: {asset_links}")
print(f"Broken relative parent links (../): {relative_up}")

# List all unique broken links for fixing
print(f"\n=== ALL UNIQUE BROKEN LINKS ({len(broken_link_counts)}) ===")
for link in sorted(broken_link_counts.keys()):
    print(f"- {link} ({broken_link_counts[link]} occurrences)")