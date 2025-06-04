# GitHub Workflow & Contribution Framework
**Building the Liberation Network**

> *"I can only show you the door. You're the one that has to walk through it."* - Morpheus (And this is how we walk through it together.)

## 🎯 Mission Statement

The Matrix Online Liberation Project operates on radical open-source principles: **Liberation over hoarding, collaboration over gatekeeping, community over corporation**. Our GitHub workflow is designed to welcome all skill levels while maintaining the highest technical and philosophical standards.

## 📋 Contribution Philosophy

### The Neoologist Approach
```yaml
contribution_principles:
  accessibility: "Every person can contribute meaningfully"
  transparency: "All decisions made in public"
  meritocracy: "Good ideas win regardless of source"
  preservation: "Document everything, lose nothing"
  
  core_values:
    - "We are all The One"
    - "Knowledge belongs to humanity"
    - "Perfect is the enemy of good enough"
    - "Community consensus over individual preference"
```

### Contribution Types Welcome
- **Code**: Servers, tools, clients, utilities
- **Documentation**: Technical guides, tutorials, philosophy
- **Research**: Reverse engineering, data analysis, archaeology
- **Art & Media**: Screenshots, videos, graphics, music
- **Community**: Moderation, event planning, outreach
- **Testing**: Quality assurance, bug reports, validation
- **Translation**: Multi-language accessibility
- **Historical**: Preserving memories, stories, artifacts

## 🚀 Quick Start Guide

### For First-Time Contributors

#### 1. Choose Your Path
```bash
# Option A: Documentation/Simple Changes
# Use GitHub web interface - no local setup required

# Option B: Code Development  
# Clone repository locally
git clone https://github.com/mxo-liberation/eden-reborn-wiki.git
cd eden-reborn-wiki

# Option C: Major Development
# Fork repository for independent work
# Use GitHub fork button, then clone your fork
```

#### 2. Find Your Task
- **Browse Issues**: [github.com/mxo-liberation/eden-reborn-wiki/issues](https://github.com/mxo-liberation/eden-reborn-wiki/issues)
- **Check Projects**: Look for project boards with organized task lists
- **Ask for Help**: Use Discussions tab for questions
- **Start Small**: Look for "good first issue" labels

#### 3. Make Your Contribution
- **Create Branch**: `git checkout -b feature/your-contribution-name`
- **Make Changes**: Edit files, add content, fix issues
- **Test Locally**: Ensure your changes work correctly
- **Submit PR**: Create pull request with clear description

### For Experienced Contributors

#### Advanced Workflow
```bash
# Set up development environment
git clone https://github.com/mxo-liberation/eden-reborn-wiki.git
cd eden-reborn-wiki
git remote add upstream https://github.com/mxo-liberation/eden-reborn-wiki.git

# Create feature branch
git checkout main
git pull upstream main
git checkout -b feature/enhanced-server-docs

# Make changes, commit frequently
git add .
git commit -m "Add advanced authentication configuration guide

- Document new bypass methods
- Include troubleshooting section  
- Add security considerations"

# Push and create PR
git push origin feature/enhanced-server-docs
# Then create PR via GitHub interface
```

## 📝 Content Guidelines

### Documentation Standards

#### Required Elements
Every documentation page must include:
```markdown
# Page Title
**Subtitle explaining purpose**

> *Matrix quote with relevance note*

## Content sections...

## Remember
> *Closing quote*

**Status indicators and navigation**
---
[Navigation links]
```

#### Writing Style
- **Tone**: Technical accuracy with mystical inspiration
- **Voice**: Second person ("you") for tutorials, first person plural ("we") for philosophy
- **Length**: Comprehensive but scannable - use headers, lists, code blocks
- **Examples**: Always include practical examples and real-world applications

#### Technical Content
```yaml
technical_standards:
  code_blocks:
    - "Include language specification"
    - "Add explanatory comments"
    - "Provide context before and after"
    - "Test all code examples"
    
  file_paths:
    - "Use absolute paths in examples"
    - "Explain directory structure"
    - "Include error handling"
    
  screenshots:
    - "High resolution (1920x1080 minimum)"
    - "Highlight relevant areas"
    - "Include captions"
    - "Update when UI changes"
```

### Code Standards

#### Repository Structure
```
eden-reborn-wiki/
├── README.md                    # Project overview
├── CONTRIBUTING.md              # This guide (expanded)
├── CLAUDE.md                    # AI assistant context
├── .github/
│   ├── workflows/              # CI/CD automation
│   ├── ISSUE_TEMPLATE/         # Standardized issue forms
│   └── PULL_REQUEST_TEMPLATE/  # PR guidelines
├── docs/                       # Main documentation
│   ├── 01-getting-started/
│   ├── 02-servers/
│   ├── 03-technical/
│   ├── 04-tools-modding/
│   ├── 05-game-content/
│   ├── 06-file-formats/
│   ├── 07-preservation/
│   └── 08-community/
├── tools/                      # Utilities and scripts
├── assets/                     # Images, videos, resources
└── sources/                    # Source documentation
```

#### Naming Conventions
```yaml
naming_standards:
  files: "kebab-case-with-hyphens.md"
  directories: "numerical-prefix-with-description/"
  branches: "type/short-descriptive-name"
  commits: "Imperative mood, <72 characters"
  
  branch_types:
    - "feature/new-functionality"
    - "fix/bug-correction"
    - "docs/documentation-update"
    - "refactor/code-reorganization"
    - "style/formatting-changes"
```

## 🔄 Workflow Processes

### Issue Management

#### Issue Types
```yaml
issue_types:
  bug:
    label: "bug"
    template: ".github/ISSUE_TEMPLATE/bug_report.md"
    priority: "immediate investigation"
    
  enhancement:
    label: "enhancement"
    template: ".github/ISSUE_TEMPLATE/feature_request.md"
    priority: "community discussion"
    
  documentation:
    label: "documentation"
    template: ".github/ISSUE_TEMPLATE/docs_improvement.md"
    priority: "quick turnaround"
    
  question:
    label: "question"
    template: ".github/ISSUE_TEMPLATE/question.md"
    priority: "community support"
    
  research:
    label: "research"
    template: ".github/ISSUE_TEMPLATE/research_task.md"
    priority: "long-term investigation"
```

#### Issue Lifecycle
1. **Creation**: Use appropriate template, add labels
2. **Triage**: Community discussion, priority assignment
3. **Assignment**: Volunteer or maintainer takes ownership
4. **Development**: Work progresses with regular updates
5. **Review**: Code review and testing
6. **Closure**: Merge and documentation update

### Pull Request Process

#### PR Requirements
```yaml
pr_standards:
  title: "Clear, descriptive summary of changes"
  description:
    - "Link to relevant issues"
    - "Explain what changed and why"
    - "Include testing information"
    - "Note any breaking changes"
    
  quality_checks:
    - "All links work correctly"
    - "Markdown renders properly"
    - "Code examples are tested"
    - "No merge conflicts"
    - "Follows style guidelines"
```

#### Review Process
1. **Automated Checks**: CI/CD runs validation
2. **Community Review**: Other contributors provide feedback
3. **Maintainer Review**: Core team final approval
4. **Merge**: Integration into main branch
5. **Deployment**: Automatic update to live documentation

### Branching Strategy

#### Main Branches
```yaml
branch_structure:
  main:
    purpose: "Production-ready content"
    protection: "Requires PR and reviews"
    deployment: "Automatic to GitHub Pages"
    
  develop:
    purpose: "Integration of new features"
    protection: "Requires PR"
    deployment: "Preview site"
    
  feature/*:
    purpose: "Individual contributions"
    protection: "None (contributor freedom)"
    deployment: "None"
```

#### Feature Development
```bash
# Start new feature
git checkout main
git pull origin main
git checkout -b feature/cnb-viewer-docs

# Work on feature
# ... make changes ...
git add .
git commit -m "Add CNB viewer development roadmap"

# Keep up to date
git checkout main
git pull origin main
git checkout feature/cnb-viewer-docs
git rebase main

# Submit for review
git push origin feature/cnb-viewer-docs
# Create PR via GitHub
```

## 🤖 Automation & CI/CD

### GitHub Actions Workflows

#### Link Validation
```yaml
# .github/workflows/link-check.yml
name: Check Links
on: [push, pull_request]

jobs:
  link-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Link Checker
        uses: lycheeverse/lychee-action@v1
        with:
          args: --verbose --no-progress './**/*.md'
```

#### Content Validation
```yaml
# .github/workflows/content-check.yml
name: Validate Content
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Markdown Lint
        uses: articulate/actions-markdownlint@v1
      - name: Check File Naming
        run: |
          # Validate naming conventions
          ./tools/validate-naming.sh
      - name: Verify Navigation
        run: |
          # Ensure all pages are reachable
          ./tools/check-navigation.py
```

#### Deployment
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Pages
        uses: actions/configure-pages@v2
      - name: Build Documentation
        run: |
          # Generate table of contents
          ./tools/generate-toc.py
          # Optimize images
          ./tools/optimize-images.sh
      - name: Deploy
        uses: actions/deploy-pages@v1
```

### Quality Assurance Scripts

#### Link Checker
```python
#!/usr/bin/env python3
"""
Comprehensive link checker for Matrix Online wiki
Validates internal links, external URLs, and navigation
"""

import os
import re
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse

class WikiLinkChecker:
    def __init__(self, wiki_root):
        self.wiki_root = Path(wiki_root)
        self.internal_links = set()
        self.external_links = set()
        self.broken_links = []
        
    def scan_all_files(self):
        """Scan all markdown files for links"""
        for md_file in self.wiki_root.rglob('*.md'):
            self.scan_file(md_file)
            
    def scan_file(self, file_path):
        """Extract all links from a markdown file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all markdown links [text](url)
        links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
        
        for text, url in links:
            if url.startswith('http'):
                self.external_links.add(url)
            else:
                # Internal link - make absolute path
                base_dir = file_path.parent
                full_path = (base_dir / url).resolve()
                self.internal_links.add((str(file_path), url, str(full_path)))
                
    def validate_internal_links(self):
        """Check that all internal links point to existing files"""
        print("🔍 Validating internal links...")
        
        for source_file, link_url, target_path in self.internal_links:
            if not Path(target_path).exists():
                self.broken_links.append({
                    'type': 'internal',
                    'source': source_file,
                    'link': link_url,
                    'target': target_path,
                    'error': 'File not found'
                })
                
    def validate_external_links(self):
        """Check that external URLs are accessible"""
        print("🌐 Validating external links...")
        
        for url in self.external_links:
            try:
                response = requests.head(url, timeout=10, allow_redirects=True)
                if response.status_code >= 400:
                    self.broken_links.append({
                        'type': 'external',
                        'link': url,
                        'error': f'HTTP {response.status_code}'
                    })
            except Exception as e:
                self.broken_links.append({
                    'type': 'external', 
                    'link': url,
                    'error': str(e)
                })
                
    def generate_report(self):
        """Generate detailed report of link validation"""
        if not self.broken_links:
            print("✅ All links are valid!")
            return True
            
        print(f"❌ Found {len(self.broken_links)} broken links:")
        
        for link in self.broken_links:
            if link['type'] == 'internal':
                print(f"  Internal: {link['source']} -> {link['link']} ({link['error']})")
            else:
                print(f"  External: {link['link']} ({link['error']})")
                
        return False

if __name__ == "__main__":
    checker = WikiLinkChecker(".")
    checker.scan_all_files()
    checker.validate_internal_links()
    checker.validate_external_links()
    valid = checker.generate_report()
    exit(0 if valid else 1)
```

## 👥 Community Roles

### Contributor Levels

#### 1. Community Member
**Access**: Read, comment, create issues  
**Responsibilities**: 
- Report bugs and suggest improvements
- Participate in discussions
- Help newcomers in discussions

#### 2. Contributor
**Access**: Create pull requests  
**Requirements**: 1+ accepted PR  
**Responsibilities**:
- Submit quality contributions
- Follow contribution guidelines
- Respond to review feedback promptly

#### 3. Regular Contributor  
**Access**: PR review privileges  
**Requirements**: 5+ accepted PRs, community nomination  
**Responsibilities**:
- Review others' pull requests
- Mentor newcomers
- Maintain code quality standards

#### 4. Maintainer
**Access**: Merge PRs, manage issues, moderate  
**Requirements**: Significant contributions, community trust  
**Responsibilities**:
- Ensure project quality and vision
- Resolve conflicts and disputes
- Plan roadmap and major decisions

#### 5. Core Team
**Access**: Repository admin, release management  
**Requirements**: Long-term commitment, technical expertise  
**Responsibilities**:
- Guide project direction
- Manage infrastructure
- Represent project in external communities

### Recognition System

#### Contribution Tracking
```yaml
recognition_metrics:
  code_contributions:
    - "Lines of code added/modified"
    - "Number of pull requests"
    - "Complexity of contributions"
    
  documentation:
    - "Pages created/improved"
    - "Word count contributions"
    - "Quality of writing"
    
  community_support:
    - "Issues helped resolve"
    - "Questions answered"
    - "New contributors mentored"
    
  research:
    - "Tools documented"
    - "File formats decoded"
    - "Historical data preserved"
```

#### Achievement System
- **🚀 First Contributor**: Submit first accepted PR
- **📚 Knowledge Keeper**: Create 10+ documentation pages
- **🔧 Tool Builder**: Contribute working tools/utilities
- **🎯 Bug Hunter**: Report and help fix 5+ bugs
- **👥 Community Builder**: Help 10+ newcomers
- **🔍 Digital Archaeologist**: Discover and document lost content
- **💎 Liberation Leader**: Core team member for 1+ year

## 📊 Project Management

### GitHub Projects Integration

#### Project Boards
```yaml
project_boards:
  development:
    columns: ["Backlog", "In Progress", "Review", "Done"]
    automation: "Auto-move cards based on PR status"
    
  documentation:
    columns: ["Ideas", "Writing", "Review", "Published"]
    focus: "Content creation and improvement"
    
  research:
    columns: ["Questions", "Investigating", "Findings", "Documented"]
    focus: "Reverse engineering and archaeology"
    
  community:
    columns: ["Proposed", "Planning", "Active", "Complete"]
    focus: "Events, outreach, and community building"
```

#### Milestone Planning
- **Monthly Releases**: Regular documentation updates
- **Quarterly Features**: Major new tools or capabilities
- **Annual Goals**: Large-scale preservation or development projects
- **Event-Driven**: Special releases for community events

### Communication Channels

#### Primary Platforms
```yaml
communication_platforms:
  github_discussions:
    purpose: "Technical discussions, Q&A"
    moderation: "Light, focus on helpfulness"
    
  discord_server:
    purpose: "Real-time chat, community building"
    channels: ["#general", "#development", "#research", "#events"]
    
  matrix_bridge:
    purpose: "Bridge between Discord and Matrix protocol"
    philosophy: "Practice what we preach about open protocols"
    
  mailing_list:
    purpose: "Important announcements, long-form discussions"
    frequency: "Weekly digest, urgent notifications"
```

#### Meeting Schedule
- **Weekly Development Sync**: Fridays 18:00 UTC
- **Monthly Community Call**: First Saturday of month
- **Quarterly Planning**: Season transitions
- **Annual LibertyCon**: Summer gathering (virtual/hybrid)

## 🚨 Conflict Resolution

### Issue Resolution Process

#### 1. Community Self-Resolution
Most conflicts can be resolved through respectful discussion in the relevant GitHub issue or discussion thread.

#### 2. Maintainer Mediation
If community discussion doesn't resolve the issue, maintainers step in to facilitate resolution.

#### 3. Core Team Decision
For major disputes affecting project direction, the core team makes final decisions through consensus.

#### 4. Code of Conduct Violations
Serious violations of community standards are handled through our enforcement procedures.

### Decision Making Philosophy
```yaml
decision_principles:
  consensus_preferred: "Seek agreement when possible"
  technical_merit: "Best technical solution wins"
  community_benefit: "Prioritize community needs over individual preferences"
  transparency: "All decisions made in public"
  reversibility: "Prefer decisions that can be changed later"
```

## 🔐 Security & Privacy

### Sensitive Information Policy

#### What NOT to Include
- Personal information (real names, addresses, phone numbers)
- Copyrighted material without permission
- Proprietary code or reverse-engineered secrets
- Credentials or authentication tokens
- Exploit details that could harm active servers

#### Security Review Process
- All pull requests reviewed for sensitive content
- Automated scanning for common credential patterns
- Community reporting system for security concerns
- Regular audits of published content

### Privacy Protection
- Contributors can use pseudonyms/handles
- No requirement to reveal personal information
- Right to remove contributions and personal data
- Secure handling of any required personal information

## 📈 Growth & Scaling

### Onboarding New Contributors

#### Welcome Process
1. **Auto-Welcome**: Bot greets new contributors
2. **Mentor Assignment**: Experienced contributor offers guidance
3. **First Task**: Small, achievable contribution to build confidence
4. **Integration**: Invitation to community channels and meetings

#### Support Resources
- **Video Tutorials**: Screen recordings of common tasks
- **Live Mentoring**: Scheduled 1-on-1 help sessions
- **Office Hours**: Regular times when maintainers are available
- **FAQ Database**: Searchable answers to common questions

### Scaling Infrastructure

#### As Project Grows
```yaml
scaling_plan:
  100_contributors:
    - "Add more project maintainers"
    - "Implement automated quality checks"
    - "Create specialized working groups"
    
  500_contributors:
    - "Establish regional communities"
    - "Implement contributor certification"
    - "Add dedicated infrastructure"
    
  1000_contributors:
    - "Create governance structure"
    - "Establish foundation or organization"
    - "Develop contributor compensation"
```

## 🎯 Success Metrics

### Tracking Progress

#### Quantitative Metrics
```yaml
success_metrics:
  content:
    - "Pages created per month"
    - "Word count growth"
    - "Link validation pass rate"
    - "User engagement (page views, time on site)"
    
  community:
    - "New contributors per month"
    - "PR response time"
    - "Issue resolution rate"
    - "Community event attendance"
    
  technical:
    - "Tools documented/created"
    - "File formats decoded"
    - "Server implementations working"
    - "Code quality scores"
    
  liberation:
    - "Tools open-sourced"
    - "Knowledge democratized"
    - "Gatekeepers bypassed"
    - "Community empowerment level"
```

#### Qualitative Assessment
- Community satisfaction surveys
- Contributor interview feedback
- External community recognition
- Achievement of liberation philosophy goals

## 📚 Resources & Training

### Learning Resources

#### For New Contributors
- **Git Basics**: Interactive tutorial for version control
- **Markdown Guide**: Writing documentation effectively
- **GitHub Workflow**: Step-by-step contribution process
- **Matrix Online History**: Understanding the project context

#### For Developers
- **MXO Architecture**: Technical deep-dive into game systems
- **Reverse Engineering**: Tools and techniques for code analysis
- **Server Development**: Building and maintaining game servers
- **File Format**: Understanding and parsing MXO data

#### For Researchers
- **Digital Archaeology**: Recovering lost information
- **Community Mining**: Extracting knowledge from discussions
- **Tool Recreation**: Rebuilding lost software
- **Documentation Standards**: Preserving knowledge effectively

### Tool Recommendations

#### Development Environment
```yaml
recommended_tools:
  editor: "VS Code with Markdown extensions"
  git_client: "GitHub Desktop for beginners, CLI for advanced"
  image_editor: "GIMP for screenshots and graphics"
  video_capture: "OBS Studio for demonstrations"
  
  browser_extensions:
    - "GitHub refined for enhanced interface"
    - "Markdown viewer for local preview"
    - "Link checker for validation"
```

## 🔮 Future Vision

### Long-Term Goals

#### Technical Objectives
- **Complete Preservation**: All MXO content documented and accessible
- **Full Revival**: Working servers with all features implemented
- **Tool Ecosystem**: Comprehensive suite of open-source tools
- **Format Liberation**: All proprietary formats decoded and documented

#### Community Objectives
- **Global Reach**: Contributors from around the world
- **Knowledge Democracy**: No gatekeeping or hoarding
- **Sustainable Growth**: Self-sustaining contributor community
- **Cultural Impact**: Model for other game preservation projects

#### Liberation Philosophy
- **Open Source Everything**: No secrets, no hoarding
- **Community Ownership**: Collective rather than individual control
- **Educational Focus**: Teaching and empowering others
- **Historical Preservation**: Maintaining memory of digital culture

### Evolution Plan
```yaml
project_evolution:
  year_1: "Foundation building, core documentation"
  year_2: "Tool development, community growth"
  year_3: "Advanced features, global expansion"
  year_5: "Model for industry, cultural impact"
  year_10: "Legacy preservation, next-generation tools"
```

## Remember

> *"The Matrix is a system, Neo. That system is our enemy. But when you're inside, you look around, what do you see? Businessmen, teachers, lawyers, carpenters. The very minds of the people we are trying to save."* - Morpheus

Our GitHub workflow isn't just about managing code - it's about building a movement. Every pull request is an act of liberation. Every documentation page is a blow against the gatekeepers. Every new contributor is another mind freed from the illusion that knowledge belongs to the few.

**Contribute not just to preserve the past, but to liberate the future.**

---

**Workflow Status**: 🟢 OPERATIONAL  
**Community**: GROWING  
**Liberation**: IN PROGRESS  

*Code together. Learn together. Liberate together.*

---

[← Back to Community](index.md) | [Contributing Guide →](contributing-guide.md) | [Code Review Guidelines →](code-review-guidelines.md)