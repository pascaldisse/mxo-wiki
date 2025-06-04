#!/usr/bin/env python3
"""
Matrix Online Wiki Link Validator
Systematically checks all markdown links for broken references.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

class WikiLinkValidator:
    def __init__(self, wiki_root):
        self.wiki_root = Path(wiki_root)
        self.broken_links = []
        self.external_links = []
        self.total_links = 0
        self.files_processed = 0
        
        # Track broken links by category
        self.broken_by_category = defaultdict(list)
        self.broken_by_file = defaultdict(list)
        
    def extract_markdown_links(self, content):
        """Extract all markdown links from content."""
        # Pattern for [text](link) format
        link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
        return re.findall(link_pattern, content)
    
    def is_external_link(self, link):
        """Check if link is external (http/https/discord etc.)"""
        return link.startswith(('http://', 'https://', 'discord:', 'mailto:'))
    
    def normalize_link_path(self, link, current_file_path):
        """Convert relative link to absolute file path."""
        # Remove anchors
        link = link.split('#')[0]
        
        # Skip empty links and anchors
        if not link or link.startswith('#'):
            return None
            
        # Handle external links
        if self.is_external_link(link):
            return None
            
        # Convert relative path to absolute
        current_dir = current_file_path.parent
        
        # Handle links without .md extension
        if not link.endswith('.md') and not link.endswith('/'):
            link += '.md'
        elif link.endswith('/'):
            link += 'index.md'
            
        target_path = (current_dir / link).resolve()
        return target_path
    
    def validate_file_links(self, file_path):
        """Validate all links in a single markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        links = self.extract_markdown_links(content)
        file_broken_links = []
        
        for link_text, link_url in links:
            self.total_links += 1
            
            if self.is_external_link(link_url):
                self.external_links.append((str(file_path), link_text, link_url))
                continue
                
            # Normalize and check internal links
            target_path = self.normalize_link_path(link_url, file_path)
            
            if target_path is None:
                continue  # Skip anchors and empty links
                
            if not target_path.exists():
                # Try to make path relative to wiki_root, fallback to absolute
                try:
                    expected_path = str(target_path.relative_to(self.wiki_root))
                except ValueError:
                    expected_path = str(target_path)
                
                broken_link = {
                    'source_file': str(file_path.relative_to(self.wiki_root)),
                    'link_text': link_text,
                    'link_url': link_url,
                    'expected_path': expected_path,
                    'category': self.categorize_broken_link(link_url, target_path)
                }
                
                self.broken_links.append(broken_link)
                file_broken_links.append(broken_link)
                self.broken_by_category[broken_link['category']].append(broken_link)
                self.broken_by_file[broken_link['source_file']].append(broken_link)
        
        return file_broken_links
    
    def categorize_broken_link(self, link_url, target_path):
        """Categorize the type of broken link."""
        if 'index.md' in str(target_path):
            return 'missing_index'
        elif target_path.suffix == '.md':
            return 'missing_page'
        elif '/' in link_url and not target_path.parent.exists():
            return 'missing_directory'
        else:
            return 'other'
    
    def validate_all_links(self):
        """Validate links in all markdown files."""
        md_files = list(self.wiki_root.rglob('*.md'))
        
        print(f"Found {len(md_files)} markdown files to validate...")
        
        for md_file in md_files:
            self.files_processed += 1
            if self.files_processed % 10 == 0:
                print(f"Processed {self.files_processed}/{len(md_files)} files...")
            
            self.validate_file_links(md_file)
    
    def generate_report(self):
        """Generate comprehensive link validation report."""
        report = {
            'summary': {
                'total_files_processed': self.files_processed,
                'total_links_found': self.total_links,
                'broken_links_count': len(self.broken_links),
                'external_links_count': len(self.external_links),
                'broken_link_percentage': round((len(self.broken_links) / self.total_links * 100), 2) if self.total_links > 0 else 0
            },
            'broken_links_by_category': dict(self.broken_by_category),
            'files_with_most_broken_links': self.get_top_broken_files(),
            'critical_navigation_issues': self.find_critical_navigation_issues(),
            'all_broken_links': self.broken_links,
            'external_links': self.external_links[:10]  # Sample of external links
        }
        
        return report
    
    def get_top_broken_files(self, limit=10):
        """Get files with the most broken links."""
        file_counts = [(file, len(links)) for file, links in self.broken_by_file.items()]
        file_counts.sort(key=lambda x: x[1], reverse=True)
        return file_counts[:limit]
    
    def find_critical_navigation_issues(self):
        """Identify broken links that affect main navigation."""
        critical_files = ['Home.md', 'index.md', '_Sidebar.md', '_Footer.md']
        critical_issues = []
        
        for broken_link in self.broken_links:
            source_file = broken_link['source_file']
            if any(critical in source_file for critical in critical_files):
                critical_issues.append(broken_link)
        
        return critical_issues
    
    def print_summary_report(self):
        """Print a human-readable summary report."""
        report = self.generate_report()
        
        print("\n" + "="*80)
        print("🔍 MATRIX ONLINE WIKI LINK VALIDATION REPORT")
        print("="*80)
        
        print(f"\n📊 SUMMARY STATISTICS")
        print(f"Files Processed: {report['summary']['total_files_processed']}")
        print(f"Total Links Found: {report['summary']['total_links_found']}")
        print(f"Broken Links: {report['summary']['broken_links_count']}")
        print(f"External Links: {report['summary']['external_links_count']}")
        print(f"Broken Link Rate: {report['summary']['broken_link_percentage']}%")
        
        if report['summary']['broken_links_count'] > 0:
            print(f"\n🚨 BROKEN LINKS BY CATEGORY")
            for category, links in report['broken_links_by_category'].items():
                print(f"  {category}: {len(links)} links")
        
        if report['files_with_most_broken_links']:
            print(f"\n📁 FILES WITH MOST BROKEN LINKS")
            for file_path, count in report['files_with_most_broken_links']:
                print(f"  {file_path}: {count} broken links")
        
        if report['critical_navigation_issues']:
            print(f"\n🔴 CRITICAL NAVIGATION ISSUES ({len(report['critical_navigation_issues'])})")
            for issue in report['critical_navigation_issues'][:10]:  # Show first 10
                print(f"  {issue['source_file']}: [{issue['link_text']}]({issue['link_url']})")
                print(f"    → Expected: {issue['expected_path']}")
        
        print(f"\n📝 DETAILED BROKEN LINKS")
        if len(self.broken_links) <= 20:
            # Show all if not too many
            for broken in self.broken_links:
                print(f"  {broken['source_file']}: [{broken['link_text']}]({broken['link_url']})")
                print(f"    → Expected: {broken['expected_path']} ({broken['category']})")
        else:
            # Show first 20 with count
            for broken in self.broken_links[:20]:
                print(f"  {broken['source_file']}: [{broken['link_text']}]({broken['link_url']})")
                print(f"    → Expected: {broken['expected_path']} ({broken['category']})")
            print(f"  ... and {len(self.broken_links) - 20} more broken links")
        
        print("\n" + "="*80)
        print("🎯 VALIDATION COMPLETE")
        print("="*80)


def main():
    wiki_root = '/Users/pascaldisse/mxoemu_forum_scrape/wiki'
    
    print("🕶️ Matrix Online Wiki Link Validator")
    print("Initiating comprehensive link validation...")
    
    validator = WikiLinkValidator(wiki_root)
    validator.validate_all_links()
    
    # Generate and save detailed report
    report = validator.generate_report()
    
    # Save JSON report
    report_file = Path(wiki_root) / 'link_validation_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Print summary
    validator.print_summary_report()
    
    print(f"\n📄 Detailed report saved to: {report_file}")

if __name__ == "__main__":
    main()