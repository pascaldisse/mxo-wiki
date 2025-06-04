#!/usr/bin/env python3
"""
Comprehensive Link Validator for Matrix Online Wiki
Validates all markdown links and reports broken ones with detailed analysis.
"""

import os
import re
import json
from collections import defaultdict
from pathlib import Path

class WikiLinkValidator:
    def __init__(self, wiki_root):
        self.wiki_root = Path(wiki_root)
        self.all_files = set()
        self.results = {
            'total_files': 0,
            'total_links': 0,
            'broken_links': 0,
            'files_with_broken_links': {},
            'broken_by_category': defaultdict(list),
            'link_types': defaultdict(int),
            'most_broken_files': [],
            'all_broken_links': []
        }
    
    def find_all_files(self):
        """Build a set of all files in the wiki for reference checking."""
        for root, dirs, files in os.walk(self.wiki_root):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), self.wiki_root)
                self.all_files.add(rel_path)
                self.all_files.add(rel_path.replace('.md', ''))  # Add without .md extension
    
    def extract_links(self, content):
        """Extract all markdown links from content."""
        # Pattern for [text](link) format
        link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, content)
        
        links = []
        for text, url in matches:
            links.append({
                'text': text,
                'url': url,
                'type': self.classify_link(url)
            })
        
        return links
    
    def classify_link(self, url):
        """Classify the type of link."""
        if url.startswith('http://') or url.startswith('https://'):
            return 'external'
        elif url.startswith('#'):
            return 'anchor'
        elif url.startswith('/'):
            return 'absolute_internal'
        else:
            return 'relative_internal'
    
    def resolve_link_path(self, current_file, link_url):
        """Resolve the actual file path that a link should point to."""
        current_dir = os.path.dirname(current_file)
        
        if link_url.startswith('/'):
            # Absolute path from wiki root
            target_path = link_url.lstrip('/')
        else:
            # Relative path from current file
            target_path = os.path.join(current_dir, link_url)
            target_path = os.path.normpath(target_path)
        
        return target_path
    
    def check_link_exists(self, current_file, link):
        """Check if a link target exists."""
        url = link['url']
        link_type = link['type']
        
        if link_type == 'external':
            return True, "External link (not validated)"
        
        if link_type == 'anchor':
            return True, "Anchor link (not validated)"
        
        # Internal link validation
        target_path = self.resolve_link_path(current_file, url)
        
        # Check various possible target files
        possible_targets = [
            target_path,
            target_path + '.md',
            target_path + '/index.md',
            target_path.replace('.md', ''),
        ]
        
        for target in possible_targets:
            if target in self.all_files:
                return True, f"Found: {target}"
        
        # Check if it's a directory that should exist
        if os.path.isdir(os.path.join(self.wiki_root, target_path)):
            return True, f"Valid directory: {target_path}"
        
        return False, f"Missing: {target_path} (tried: {', '.join(possible_targets)})"
    
    def validate_file(self, file_path):
        """Validate all links in a single markdown file."""
        rel_path = os.path.relpath(file_path, self.wiki_root)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                'file': rel_path,
                'error': f"Could not read file: {e}",
                'links': [],
                'broken_links': []
            }
        
        links = self.extract_links(content)
        broken_links = []
        
        for link in links:
            self.results['link_types'][link['type']] += 1
            
            if link['type'] in ['relative_internal', 'absolute_internal']:
                exists, reason = self.check_link_exists(rel_path, link)
                if not exists:
                    broken_links.append({
                        'text': link['text'],
                        'url': link['url'],
                        'type': link['type'],
                        'reason': reason
                    })
        
        return {
            'file': rel_path,
            'total_links': len(links),
            'broken_links': broken_links,
            'links': links
        }
    
    def categorize_broken_link(self, broken_link):
        """Categorize the type of broken link."""
        url = broken_link['url']
        reason = broken_link['reason']
        
        if 'index.md' in reason:
            return 'missing_index'
        elif url.endswith('.md'):
            return 'missing_md_file'
        elif '/' in url:
            return 'missing_directory_or_file'
        else:
            return 'missing_file'
    
    def run_validation(self):
        """Run complete validation on all markdown files."""
        print("🔍 Starting comprehensive wiki link validation...")
        
        # Find all files first
        self.find_all_files()
        
        # Find all markdown files
        md_files = list(self.wiki_root.glob('**/*.md'))
        self.results['total_files'] = len(md_files)
        
        print(f"📁 Found {len(md_files)} markdown files")
        print(f"📄 Total files in wiki: {len(self.all_files)}")
        
        # Validate each file
        for md_file in md_files:
            file_result = self.validate_file(md_file)
            
            if file_result.get('error'):
                print(f"❌ Error in {file_result['file']}: {file_result['error']}")
                continue
            
            self.results['total_links'] += file_result['total_links']
            
            if file_result['broken_links']:
                self.results['files_with_broken_links'][file_result['file']] = file_result['broken_links']
                self.results['broken_links'] += len(file_result['broken_links'])
                
                # Categorize broken links
                for broken_link in file_result['broken_links']:
                    category = self.categorize_broken_link(broken_link)
                    self.results['broken_by_category'][category].append({
                        'file': file_result['file'],
                        'link': broken_link
                    })
                    
                    self.results['all_broken_links'].append({
                        'file': file_result['file'],
                        'text': broken_link['text'],
                        'url': broken_link['url'],
                        'reason': broken_link['reason'],
                        'category': category
                    })
        
        # Calculate most broken files
        broken_counts = [(f, len(links)) for f, links in self.results['files_with_broken_links'].items()]
        self.results['most_broken_files'] = sorted(broken_counts, key=lambda x: x[1], reverse=True)
        
        return self.results
    
    def print_report(self):
        """Print a comprehensive validation report."""
        results = self.results
        
        print("\n" + "="*80)
        print("🔍 MATRIX ONLINE WIKI LINK VALIDATION REPORT")
        print("="*80)
        
        # Summary
        print(f"\n📊 SUMMARY:")
        print(f"   Total files analyzed: {results['total_files']}")
        print(f"   Total links found: {results['total_links']}")
        print(f"   Broken links: {results['broken_links']}")
        print(f"   Files with broken links: {len(results['files_with_broken_links'])}")
        print(f"   Success rate: {((results['total_links'] - results['broken_links']) / results['total_links'] * 100):.1f}%")
        
        # Link types
        print(f"\n🔗 LINK TYPES:")
        for link_type, count in results['link_types'].items():
            print(f"   {link_type}: {count}")
        
        # Most broken files
        print(f"\n💥 MOST BROKEN FILES:")
        for file, count in results['most_broken_files'][:10]:
            print(f"   {file}: {count} broken links")
        
        # Broken link categories
        print(f"\n📋 BROKEN LINK CATEGORIES:")
        for category, links in results['broken_by_category'].items():
            print(f"   {category}: {len(links)} links")
        
        # Critical files analysis
        critical_files = ['Home.md', '_Sidebar.md', 'index.md', 'README.md']
        print(f"\n🚨 CRITICAL FILES ANALYSIS:")
        for file in critical_files:
            matching_files = [f for f in results['files_with_broken_links'].keys() if file in f]
            if matching_files:
                for match in matching_files:
                    count = len(results['files_with_broken_links'][match])
                    print(f"   {match}: {count} broken links")
            else:
                print(f"   {file}: No broken links found")
        
        # Sample broken links
        print(f"\n🔍 SAMPLE BROKEN LINKS:")
        for i, broken_link in enumerate(results['all_broken_links'][:20]):
            print(f"   {i+1}. [{broken_link['text']}]({broken_link['url']}) in {broken_link['file']}")
            print(f"      Reason: {broken_link['reason']}")
        
        if len(results['all_broken_links']) > 20:
            print(f"   ... and {len(results['all_broken_links']) - 20} more broken links")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if results['broken_links'] > 0:
            print("   1. Fix navigation files first (Home.md, _Sidebar.md)")
            print("   2. Create missing index.md files in directories")
            print("   3. Update relative paths to use correct directory structure")
            print("   4. Consider using absolute paths for better consistency")
        else:
            print("   🎉 All links are working correctly!")

def main():
    wiki_root = "/Users/pascaldisse/mxoemu_forum_scrape/wiki"
    validator = WikiLinkValidator(wiki_root)
    validator.run_validation()
    validator.print_report()
    
    # Save detailed results to JSON
    with open(os.path.join(wiki_root, 'link_validation_results.json'), 'w') as f:
        json.dump(validator.results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {wiki_root}/link_validation_results.json")

if __name__ == "__main__":
    main()