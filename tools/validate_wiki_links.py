#!/usr/bin/env python3
"""
Matrix Online Wiki Link Validator
Automated tool for checking wiki health and identifying broken links
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from urllib.parse import urlparse
from datetime import datetime

class WikiLinkValidator:
    def __init__(self, wiki_path):
        self.wiki_path = Path(wiki_path).resolve()
        self.total_files = 0
        self.total_links = 0
        self.working_links = 0
        self.broken_links = []
        self.link_types = defaultdict(int)
        
    def extract_links_from_file(self, file_path):
        """Extract all markdown links from a file."""
        links = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all markdown links [text](url)
            pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.findall(pattern, content)
            
            for text, url in matches:
                links.append({
                    'text': text,
                    'url': url,
                    'file': str(file_path),
                    'line': content[:content.find(f'[{text}]({url})')].count('\n') + 1
                })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return links
    
    def validate_link(self, link_url, base_path, current_file):
        """Validate a single link."""
        # Remove any anchors for file checking
        url_without_anchor = link_url.split('#')[0]
        
        # External links
        if url_without_anchor.startswith(('http://', 'https://', 'ftp://', 'mailto:')):
            return True, 'external'
        
        # Anchor-only links
        if link_url.startswith('#'):
            return True, 'anchor'
        
        # Internal links
        if url_without_anchor:
            current_dir = os.path.dirname(current_file)
            
            # Try to resolve the path
            if url_without_anchor.startswith('/'):
                # Absolute path from wiki root
                target_path = os.path.join(base_path, url_without_anchor[1:])
            else:
                # Relative path
                target_path = os.path.normpath(os.path.join(current_dir, url_without_anchor))
            
            # Check if file exists
            if os.path.exists(target_path):
                return True, 'internal'
            
            # Check with .md extension
            if not target_path.endswith('.md'):
                if os.path.exists(target_path + '.md'):
                    return True, 'internal'
            
            # Check if it's a directory with index.md
            if os.path.isdir(target_path):
                index_path = os.path.join(target_path, 'index.md')
                if os.path.exists(index_path):
                    return True, 'internal'
            
            return False, 'internal'
        
        return True, 'empty'
    
    def analyze_broken_links(self):
        """Analyze patterns in broken links."""
        if not self.broken_links:
            return {}
            
        # Count frequency of broken URLs
        broken_url_counts = Counter(link['url'] for link in self.broken_links)
        
        # Group by file
        by_file = defaultdict(list)
        for link in self.broken_links:
            by_file[link['file']].append(link)
        
        # Find patterns
        patterns = {
            'most_common': broken_url_counts.most_common(10),
            'by_file': {f: len(links) for f, links in sorted(by_file.items(), 
                       key=lambda x: len(x[1]), reverse=True)[:10]},
            'total_unique': len(broken_url_counts),
            'placeholder_links': sum(1 for url in broken_url_counts if url == 'link')
        }
        
        return patterns
    
    def validate_wiki(self):
        """Main validation process."""
        # Find all markdown files
        md_files = []
        for root, dirs, files in os.walk(self.wiki_path):
            # Skip hidden directories and common non-content directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', 'node_modules']]
            
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))
        
        self.total_files = len(md_files)
        
        # Extract and validate all links
        all_links = []
        for file_path in md_files:
            links = self.extract_links_from_file(file_path)
            all_links.extend(links)
        
        self.total_links = len(all_links)
        
        # Validate each link
        for link in all_links:
            is_valid, link_type = self.validate_link(
                link['url'], 
                self.wiki_path, 
                link['file']
            )
            self.link_types[link_type] += 1
            
            if is_valid:
                self.working_links += 1
            else:
                self.broken_links.append(link)
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive validation report."""
        health_percentage = (self.working_links / self.total_links * 100) if self.total_links > 0 else 0
        patterns = self.analyze_broken_links()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files': self.total_files,
                'total_links': self.total_links,
                'working_links': self.working_links,
                'broken_links': len(self.broken_links),
                'health_percentage': round(health_percentage, 1)
            },
            'link_types': dict(self.link_types),
            'broken_link_patterns': patterns,
            'broken_links': self.broken_links[:50]  # First 50 for detailed review
        }
        
        return report
    
    def print_report(self, report):
        """Print human-readable report."""
        print(f"\n{'='*60}")
        print(f"MATRIX ONLINE WIKI LINK VALIDATION REPORT")
        print(f"Generated: {report['timestamp']}")
        print(f"{'='*60}\n")
        
        # Summary
        s = report['summary']
        print(f"📊 SUMMARY")
        print(f"Total Files: {s['total_files']}")
        print(f"Total Links: {s['total_links']}")
        print(f"Working Links: {s['working_links']}")
        print(f"Broken Links: {s['broken_links']}")
        print(f"Health Score: {s['health_percentage']}%")
        
        # Health grade
        health = s['health_percentage']
        if health >= 90:
            grade = "A (Excellent)"
        elif health >= 80:
            grade = "B (Good)"
        elif health >= 70:
            grade = "C (Fair)"
        elif health >= 60:
            grade = "D (Poor)"
        else:
            grade = "F (Critical)"
        print(f"Grade: {grade}\n")
        
        # Link types
        print(f"📎 LINK TYPES")
        for link_type, count in sorted(report['link_types'].items()):
            print(f"  {link_type}: {count}")
        
        # Top broken links
        patterns = report['broken_link_patterns']
        if patterns.get('most_common'):
            print(f"\n🔴 TOP 10 BROKEN LINKS")
            for url, count in patterns['most_common']:
                print(f"  {url} ({count} occurrences)")
        
        # Files with most broken links
        if patterns.get('by_file'):
            print(f"\n📁 FILES WITH MOST BROKEN LINKS")
            for file, count in list(patterns['by_file'].items())[:5]:
                file_short = file.replace(str(self.wiki_path) + '/', '')
                print(f"  {file_short}: {count} broken links")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        if patterns.get('placeholder_links', 0) > 0:
            print(f"- Replace {patterns['placeholder_links']} generic 'link' placeholders")
        if s['broken_links'] > 50:
            print(f"- Focus on fixing high-frequency broken links first")
        if health < 70:
            print(f"- Consider a comprehensive wiki check cycle")
        if health >= 85:
            print(f"- Maintain current quality with regular checks")
            
def main():
    parser = argparse.ArgumentParser(description='Validate Matrix Online Wiki links')
    parser.add_argument('--path', default='/mxo/forum_scrape/wiki',
                       help='Path to wiki directory')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    parser.add_argument('--output', help='Save report to file')
    
    args = parser.parse_args()
    
    # Run validation
    validator = WikiLinkValidator(args.path)
    report = validator.validate_wiki()
    
    # Output results
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        validator.print_report(report)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {args.output}")
    
    # Return exit code based on health
    health = report['summary']['health_percentage']
    if health >= 80:
        return 0  # Success
    elif health >= 60:
        return 1  # Warning
    else:
        return 2  # Critical

if __name__ == '__main__':
    exit(main())