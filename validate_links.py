#!/usr/bin/env python3
"""
Enhanced Matrix Online Wiki Link Validator
Comprehensive link validation with change tracking and categorization
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

class WikiLinkValidator:
    def __init__(self, wiki_root):
        self.wiki_root = Path(wiki_root)
        self.results = {
            'total_files': 0,
            'total_links': 0,
            'broken_links': [],
            'working_links': [],
            'categories': defaultdict(list),
            'file_stats': {},
            'timestamp': datetime.now().isoformat()
        }
        
    def find_markdown_files(self):
        """Find all markdown files in the wiki"""
        return list(self.wiki_root.rglob("*.md"))
    
    def extract_links(self, content, file_path):
        """Extract all markdown links from content"""
        links = []
        
        # Standard markdown links: [text](url)
        markdown_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
        for text, url in markdown_links:
            links.append({
                'type': 'markdown',
                'text': text.strip(),
                'url': url.strip(),
                'file': str(file_path)
            })
        
        # Reference-style links: [text][ref]
        ref_links = re.findall(r'\[([^\]]+)\]\[([^\]]*)\]', content)
        for text, ref in ref_links:
            links.append({
                'type': 'reference',
                'text': text.strip(),
                'url': ref.strip() if ref else text.strip(),
                'file': str(file_path)
            })
        
        # Wiki-style links: [[Page Name]]
        wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
        for link in wiki_links:
            links.append({
                'type': 'wiki',
                'text': link.strip(),
                'url': link.strip(),
                'file': str(file_path)
            })
        
        return links
    
    def categorize_link(self, link):
        """Categorize link by type and target"""
        url = link['url'].lower()
        
        if url.startswith('http'):
            return 'external'
        elif url.startswith('#'):
            return 'anchor'
        elif url.endswith('.md'):
            return 'internal_md'
        elif '/' in url and not url.startswith('.'):
            return 'internal_path'
        elif url.startswith('.'):
            return 'relative'
        else:
            return 'other'
    
    def validate_internal_link(self, link, source_file):
        """Validate internal markdown links"""
        url = link['url']
        source_dir = Path(source_file).parent
        
        # Handle different link formats
        if url.startswith('#'):
            # Anchor link - would need content analysis
            return True, "anchor_not_validated"
        
        # Clean URL
        clean_url = url.split('#')[0]  # Remove anchors
        
        # Try different resolution strategies
        possible_paths = []
        
        # 1. Relative to source file
        possible_paths.append(source_dir / clean_url)
        
        # 2. Relative to wiki root
        possible_paths.append(self.wiki_root / clean_url)
        
        # 3. Try adding .md extension if missing
        if not clean_url.endswith('.md'):
            possible_paths.append(source_dir / f"{clean_url}.md")
            possible_paths.append(self.wiki_root / f"{clean_url}.md")
        
        # 4. Try removing leading slash
        if clean_url.startswith('/'):
            clean_url_no_slash = clean_url[1:]
            possible_paths.append(self.wiki_root / clean_url_no_slash)
            if not clean_url_no_slash.endswith('.md'):
                possible_paths.append(self.wiki_root / f"{clean_url_no_slash}.md")
        
        # Check if any path exists
        for path in possible_paths:
            if path.exists() and path.is_file():
                return True, str(path)
        
        return False, f"tried: {[str(p) for p in possible_paths[:3]]}"
    
    def validate_all_links(self):
        """Validate all links in all markdown files"""
        markdown_files = self.find_markdown_files()
        self.results['total_files'] = len(markdown_files)
        
        print(f"🔍 Scanning {len(markdown_files)} markdown files...")
        
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                links = self.extract_links(content, file_path)
                file_stats = {
                    'total_links': len(links),
                    'broken_links': 0,
                    'working_links': 0,
                    'categories': Counter()
                }
                
                for link in links:
                    self.results['total_links'] += 1
                    category = self.categorize_link(link)
                    file_stats['categories'][category] += 1
                    
                    # Only validate internal links
                    if category in ['internal_md', 'internal_path', 'relative']:
                        is_valid, details = self.validate_internal_link(link, file_path)
                        
                        link_result = {
                            **link,
                            'category': category,
                            'valid': is_valid,
                            'details': details,
                            'source_file': str(file_path.relative_to(self.wiki_root))
                        }
                        
                        if is_valid:
                            self.results['working_links'].append(link_result)
                            file_stats['working_links'] += 1
                        else:
                            self.results['broken_links'].append(link_result)
                            file_stats['broken_links'] += 1
                            
                        self.results['categories'][category].append(link_result)
                    else:
                        # External links, anchors - assume working for now
                        link_result = {
                            **link,
                            'category': category,
                            'valid': True,
                            'details': 'external_or_anchor',
                            'source_file': str(file_path.relative_to(self.wiki_root))
                        }
                        self.results['working_links'].append(link_result)
                        file_stats['working_links'] += 1
                        self.results['categories'][category].append(link_result)
                
                self.results['file_stats'][str(file_path.relative_to(self.wiki_root))] = file_stats
                
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
    
    def generate_report(self):
        """Generate comprehensive validation report"""
        total_internal = len(self.results['broken_links']) + len([l for l in self.results['working_links'] if l['category'] in ['internal_md', 'internal_path', 'relative']])
        broken_count = len(self.results['broken_links'])
        
        if total_internal > 0:
            failure_rate = (broken_count / total_internal) * 100
            health_score = max(0, 10 - (failure_rate / 10))
        else:
            failure_rate = 0
            health_score = 10
        
        report = f"""
# Matrix Online Wiki Link Validation Report
Generated: {self.results['timestamp']}

## 📊 Summary Statistics
- **Total Files Scanned**: {self.results['total_files']}
- **Total Links Found**: {self.results['total_links']}
- **Internal Links Tested**: {total_internal}
- **Broken Links**: {broken_count}
- **Failure Rate**: {failure_rate:.1f}%
- **Health Score**: {health_score:.1f}/10

## 📈 Changes Since Last Check
- Files: 110 → {self.results['total_files']} ({self.results['total_files'] - 110:+d})
- Previous: 119 broken links, 18.1% failure rate
- Current: {broken_count} broken links, {failure_rate:.1f}% failure rate
- **Improvement**: {18.1 - failure_rate:+.1f} percentage points

## 🔗 Link Categories
"""
        
        category_stats = Counter()
        for category, links in self.results['categories'].items():
            category_stats[category] = len(links)
        
        for category, count in category_stats.most_common():
            broken_in_cat = len([l for l in self.results['broken_links'] if l['category'] == category])
            report += f"- **{category}**: {count} total, {broken_in_cat} broken\n"
        
        if self.results['broken_links']:
            report += f"""
## ❌ Broken Links ({len(self.results['broken_links'])})

"""
            
            # Group by source file
            by_file = defaultdict(list)
            for link in self.results['broken_links']:
                by_file[link['source_file']].append(link)
            
            for file_path, file_links in sorted(by_file.items()):
                report += f"### {file_path} ({len(file_links)} broken)\n"
                for link in file_links:
                    report += f"- `[{link['text']}]({link['url']})` → {link['details']}\n"
                report += "\n"
        
        # Most problematic files
        problem_files = [(f, stats['broken_links']) for f, stats in self.results['file_stats'].items() if stats['broken_links'] > 0]
        problem_files.sort(key=lambda x: x[1], reverse=True)
        
        if problem_files:
            report += f"""
## 🚨 Most Problematic Files
"""
            for file_path, broken_count in problem_files[:10]:
                total = self.results['file_stats'][file_path]['total_links']
                rate = (broken_count / total * 100) if total > 0 else 0
                report += f"- **{file_path}**: {broken_count}/{total} broken ({rate:.0f}%)\n"
        
        # Recommendations
        report += f"""
## 🛠️ Recommendations

### High Priority Fixes
"""
        
        # Find most common broken patterns
        broken_patterns = Counter()
        for link in self.results['broken_links']:
            if 'tried:' in link['details']:
                broken_patterns[link['url']] += 1
        
        for pattern, count in broken_patterns.most_common(5):
            report += f"- Fix `{pattern}` (appears {count} times)\n"
        
        report += f"""
### Link Health Improvement Strategy
1. **Focus on internal_md links** - highest failure rate
2. **Standardize relative paths** - use consistent `.md` extensions
3. **Validate anchor links** - check heading references
4. **Update outdated paths** - especially in recently added files

### Progress Assessment
- **Previous Health Score**: 7.5/10
- **Current Health Score**: {health_score:.1f}/10
- **Change**: {health_score - 7.5:+.1f} points
"""
        
        if health_score > 7.5:
            report += "✅ **IMPROVEMENT** - Link health has gotten better!\n"
        elif health_score < 7.5:
            report += "⚠️ **REGRESSION** - Link health has declined.\n"
        else:
            report += "📊 **STABLE** - Link health unchanged.\n"
        
        return report

def main():
    wiki_root = "/Users/pascaldisse/mxoemu_forum_scrape/wiki"
    validator = WikiLinkValidator(wiki_root)
    
    print("🚀 Starting enhanced Matrix Online Wiki link validation...")
    validator.validate_all_links()
    
    report = validator.generate_report()
    print(report)
    
    # Save detailed results
    results_file = Path(wiki_root) / "link_validation_results.json"
    with open(results_file, 'w') as f:
        json.dump(validator.results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    main()