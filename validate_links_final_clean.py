#!/usr/bin/env python3
"""
Final comprehensive link validation for Matrix Online Wiki
Compares current state to previous validation results
Excludes validation reports from the scan
"""

import os
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

class WikiLinkValidator:
    def __init__(self, wiki_path):
        self.wiki_path = Path(wiki_path)
        self.links = []
        self.files = set()
        self.broken_links = []
        self.working_links = []
        
    def find_all_files(self):
        """Find all markdown files in the wiki"""
        excluded_files = {
            'LINK_VALIDATION_REPORT.md',
            'link_validation_final_report.md',
            'validate_links_final.py',
            'validate_links_final_clean.py'
        }
        
        for file_path in self.wiki_path.rglob("*.md"):
            if not any(part.startswith('.') for part in file_path.parts):
                if file_path.name not in excluded_files:
                    self.files.add(file_path.relative_to(self.wiki_path))
                
    def extract_links(self, file_path):
        """Extract all markdown links from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all markdown links [text](url)
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.findall(link_pattern, content)
            
            for text, url in matches:
                # Skip external links
                if url.startswith(('http://', 'https://', 'ftp://', 'mailto:')):
                    continue
                    
                # Skip anchors
                if url.startswith('#'):
                    continue
                    
                # Remove anchor from internal links
                clean_url = url.split('#')[0]
                if clean_url:
                    self.links.append({
                        'file': str(file_path.relative_to(self.wiki_path)),
                        'text': text,
                        'url': clean_url,
                        'original_url': url
                    })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
    def validate_link(self, link):
        """Check if a link is valid"""
        source_file = Path(self.wiki_path) / link['file']
        source_dir = source_file.parent
        
        # Handle absolute paths (starting with /)
        if link['url'].startswith('/'):
            target_path = self.wiki_path / link['url'][1:]
        else:
            # Relative path
            target_path = (source_dir / link['url']).resolve()
            
        # Check if file exists
        if target_path.exists():
            return True
            
        # Check with .md extension
        if not target_path.suffix:
            md_path = target_path.with_suffix('.md')
            if md_path.exists():
                return True
                
        # Check if it's a directory with index.md
        if target_path.is_dir():
            index_path = target_path / 'index.md'
            if index_path.exists():
                return True
                
        return False
        
    def run_validation(self):
        """Run the complete validation process"""
        print("🔍 Matrix Online Wiki - Final Link Validation (Clean)")
        print("=" * 60)
        
        # Find all files
        self.find_all_files()
        print(f"📁 Found {len(self.files)} markdown files (excluding reports)")
        
        # Extract all links
        for file_path in self.files:
            full_path = self.wiki_path / file_path
            self.extract_links(full_path)
            
        print(f"🔗 Found {len(self.links)} internal links")
        
        # Validate each link
        for link in self.links:
            if self.validate_link(link):
                self.working_links.append(link)
            else:
                self.broken_links.append(link)
                
        # Calculate metrics
        total_links = len(self.links)
        working_count = len(self.working_links)
        broken_count = len(self.broken_links)
        
        print("\n📊 CURRENT VALIDATION RESULTS")
        print("=" * 60)
        print(f"Total internal links found: {total_links}")
        print(f"✅ Working links: {working_count} ({working_count/total_links*100:.1f}%)")
        print(f"❌ Broken links: {broken_count} ({broken_count/total_links*100:.1f}%)")
        
        # Previous results (from your message)
        prev_total = 669
        prev_broken = 88
        prev_working = prev_total - prev_broken
        
        print("\n📈 IMPROVEMENT METRICS")
        print("=" * 60)
        print(f"Previous validation: {prev_broken} broken out of {prev_total} total")
        print(f"Current validation: {broken_count} broken out of {total_links} total")
        
        # Calculate improvement
        links_fixed = prev_broken - broken_count
        if links_fixed > 0:
            improvement_rate = (links_fixed / prev_broken * 100)
            print(f"✨ Links fixed: {links_fixed}")
            print(f"📈 Improvement rate: {improvement_rate:.1f}%")
        else:
            print(f"⚠️  Broken links increased by: {abs(links_fixed)}")
            
        prev_health = (prev_working / prev_total * 100)
        curr_health = (working_count / total_links * 100)
        print(f"📊 Wiki health score: {curr_health:.1f}% (was {prev_health:.1f}%)")
        
        # Analyze most frequent broken links
        broken_targets = Counter()
        for link in self.broken_links:
            broken_targets[link['url']] += 1
            
        print("\n🔴 MOST FREQUENT REMAINING BROKEN LINKS")
        print("=" * 60)
        for url, count in broken_targets.most_common(15):
            print(f"{count:3d} occurrences: {url}")
            
        # Group broken links by source file
        by_file = defaultdict(list)
        for link in self.broken_links:
            by_file[link['file']].append(link)
            
        print("\n📄 FILES WITH MOST BROKEN LINKS")
        print("=" * 60)
        sorted_files = sorted(by_file.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        for file, links in sorted_files:
            print(f"{len(links):3d} broken links in: {file}")
            
        # Show sample of remaining broken links
        print("\n🔍 SAMPLE OF REMAINING BROKEN LINKS")
        print("=" * 60)
        for link in self.broken_links[:15]:
            print(f"In {link['file']}:")
            print(f"  [{link['text']}]({link['url']})")
            
        # Summary report
        print("\n📋 FINAL WIKI HEALTH REPORT")
        print("=" * 60)
        print(f"✨ Wiki Health Score: {(working_count / total_links * 100):.1f}%")
        print(f"📊 Total Files: {len(self.files)}")
        print(f"🔗 Total Links: {total_links}")
        print(f"✅ Working Links: {working_count}")
        print(f"❌ Broken Links: {broken_count}")
        
        if links_fixed > 0:
            print(f"📈 Improvement: {links_fixed} links fixed ({improvement_rate:.1f}%)")
        else:
            print(f"⚠️  Status: {abs(links_fixed)} more broken links than before")
            
        # Identify which critical files were created
        critical_files = [
            'gm-commands.md',
            'custom-content.md', 
            'pkb-tools.md',
            'mission-examples.md',
            'mission-creator.md'
        ]
        
        print("\n🎯 CRITICAL FILES STATUS")
        print("=" * 60)
        for filename in critical_files:
            found = False
            for file_path in self.files:
                if file_path.name == filename:
                    found = True
                    print(f"✅ {filename} - CREATED")
                    break
            if not found:
                print(f"❌ {filename} - Not found")
                
        # Save detailed results
        report_path = self.wiki_path / 'final_link_validation_report.md'
        with open(report_path, 'w') as f:
            f.write(f"# Matrix Online Wiki - Final Link Validation Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Wiki Health Score**: {(working_count / total_links * 100):.1f}%\n")
            f.write(f"- **Total Files**: {len(self.files)}\n")
            f.write(f"- **Total Links**: {total_links}\n")
            f.write(f"- **Working Links**: {working_count} ({working_count/total_links*100:.1f}%)\n")
            f.write(f"- **Broken Links**: {broken_count} ({broken_count/total_links*100:.1f}%)\n\n")
            f.write(f"## Improvement Metrics\n\n")
            f.write(f"- **Previous Broken Links**: {prev_broken}\n")
            f.write(f"- **Current Broken Links**: {broken_count}\n")
            if links_fixed > 0:
                f.write(f"- **Links Fixed**: {links_fixed}\n")
                f.write(f"- **Improvement Rate**: {improvement_rate:.1f}%\n\n")
            else:
                f.write(f"- **Status**: {abs(links_fixed)} more broken links\n\n")
            f.write(f"## Critical Files Created\n\n")
            for filename in critical_files:
                found = any(file_path.name == filename for file_path in self.files)
                status = "✅ Created" if found else "❌ Missing"
                f.write(f"- {filename}: {status}\n")
            f.write(f"\n## All Broken Links\n\n")
            for link in sorted(self.broken_links, key=lambda x: (x['file'], x['url'])):
                f.write(f"- In `{link['file']}`: [{link['text']}]({link['url']})\n")
                
        print(f"\n💾 Detailed report saved to: {report_path}")

if __name__ == "__main__":
    validator = WikiLinkValidator("/Users/pascaldisse/mxoemu_forum_scrape/wiki")
    validator.run_validation()