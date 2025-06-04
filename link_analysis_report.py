#!/usr/bin/env python3
"""
Detailed Link Analysis for Matrix Online Wiki
Maps broken links to actual existing files to identify the root causes.
"""

import json
import os
from pathlib import Path

def analyze_link_issues():
    """Analyze the link validation results and map to actual file structure."""
    
    wiki_root = Path("/mxo/forum_scrape/wiki")
    
    # Load validation results
    with open(wiki_root / "link_validation_results.json") as f:
        results = json.load(f)
    
    # Get actual file structure
    actual_files = {}
    for md_file in wiki_root.glob("**/*.md"):
        rel_path = str(md_file.relative_to(wiki_root))
        actual_files[rel_path] = True
        actual_files[rel_path.replace('.md', '')] = True
    
    print("=" * 80)
    print("🔍 DETAILED LINK ISSUE ANALYSIS")
    print("=" * 80)
    
    # Categorize issues
    issues = {
        'wrong_directory': [],
        'missing_files': [],
        'anchor_issues': [],
        'path_mismatch': [],
        'structure_mismatch': []
    }
    
    for broken_link in results['all_broken_links']:
        file_path = broken_link['file']
        target_url = broken_link['url']
        link_text = broken_link['text']
        
        # Try to find similar files
        possible_matches = find_similar_files(target_url, actual_files)
        
        if '#' in target_url:
            issues['anchor_issues'].append({
                'file': file_path,
                'broken_link': target_url,
                'text': link_text,
                'matches': possible_matches
            })
        elif possible_matches:
            issues['path_mismatch'].append({
                'file': file_path,
                'broken_link': target_url,
                'text': link_text,
                'matches': possible_matches
            })
        else:
            issues['missing_files'].append({
                'file': file_path,
                'broken_link': target_url,
                'text': link_text
            })
    
    # Print analysis
    print(f"\n📊 ISSUE CATEGORIES:")
    for category, items in issues.items():
        print(f"   {category}: {len(items)} issues")
    
    print(f"\n🔗 PATH MISMATCH ANALYSIS (files exist but wrong path):")
    for issue in issues['path_mismatch'][:20]:
        print(f"   ❌ {issue['broken_link']} in {issue['file']}")
        print(f"      Should be: {issue['matches'][0]}")
        print()
    
    print(f"\n❓ MISSING FILES (completely missing):")
    for issue in issues['missing_files'][:10]:
        print(f"   ❌ {issue['broken_link']} in {issue['file']}")
        print(f"      Text: [{issue['text']}]")
        print()
    
    print(f"\n⚓ ANCHOR ISSUES (links with #):")
    for issue in issues['anchor_issues'][:10]:
        print(f"   ❌ {issue['broken_link']} in {issue['file']}")
        if issue['matches']:
            print(f"      Base file exists: {issue['matches'][0]}")
        print()
    
    # Generate fix suggestions
    print(f"\n🔧 SUGGESTED FIXES:")
    
    # Directory structure fixes
    directory_fixes = {}
    for issue in issues['path_mismatch']:
        broken = issue['broken_link']
        correct = issue['matches'][0] if issue['matches'] else None
        if correct:
            directory_fixes[broken] = correct
    
    print(f"\n   📁 DIRECTORY/PATH CORRECTIONS:")
    for broken, correct in list(directory_fixes.items())[:10]:
        print(f"      {broken} → {correct}")
    
    return issues

def find_similar_files(target_url, actual_files):
    """Find files that might match the broken link."""
    matches = []
    
    # Remove .md if present and try variations
    base_target = target_url.replace('.md', '')
    
    # Check for exact matches
    if target_url in actual_files:
        matches.append(target_url)
    
    # Check for filename matches in different directories
    filename = os.path.basename(base_target)
    for file_path in actual_files:
        if filename in file_path and file_path.endswith('.md'):
            matches.append(file_path)
    
    # Check for similar names
    for file_path in actual_files:
        if any(word in file_path.lower() for word in filename.lower().split('-')):
            if file_path.endswith('.md') and file_path not in matches:
                matches.append(file_path)
    
    return matches[:3]  # Return top 3 matches

def main():
    issues = analyze_link_issues()
    
    print(f"\n🎯 PRIORITY FIXES NEEDED:")
    print(f"   1. Fix main navigation files first (index.md, Home.md, _Sidebar.md)")
    print(f"   2. Update directory structure references")
    print(f"   3. Create missing critical files")
    print(f"   4. Fix anchor links")

if __name__ == "__main__":
    main()