# Matrix Online Wiki Tools

## Overview

This directory contains utilities for maintaining and improving the Matrix Online wiki.

## Available Tools

### 🔗 validate_wiki_links.py
**Automated link validation and health checking**

#### Features
- Scans all markdown files for links
- Validates internal and external links
- Generates health score and grade
- Identifies broken link patterns
- Provides actionable recommendations

#### Usage
```bash
# Basic validation with console output
python tools/validate_wiki_links.py

# Output as JSON
python tools/validate_wiki_links.py --json

# Save report to file
python tools/validate_wiki_links.py --output report.json

# Validate different wiki path
python tools/validate_wiki_links.py --path /path/to/wiki
```

#### Health Grades
- **A (90-100%)**: Excellent - Wiki is in great shape
- **B (80-89%)**: Good - Minor issues to address
- **C (70-79%)**: Fair - Needs attention
- **D (60-69%)**: Poor - Significant work needed
- **F (<60%)**: Critical - Major intervention required

#### Exit Codes
- `0`: Health ≥ 80% (Success)
- `1`: Health 60-79% (Warning)
- `2`: Health < 60% (Critical)

## GitHub Actions Integration

The wiki includes automated link validation that runs:
- On every push to main branch (when .md files change)
- On pull requests (when .md files change)
- Weekly on Sundays
- Manually via workflow dispatch

See `.github/workflows/link-validation.yml` for configuration.

## Adding New Tools

When adding new tools:
1. Place scripts in this directory
2. Update this README with documentation
3. Consider adding GitHub Actions integration
4. Follow Python best practices (type hints, docstrings)
5. Include help text and examples

## Future Tools Planned

- **content_analyzer.py** - Analyze wiki content statistics
- **source_checker.py** - Verify source documentation coverage
- **image_optimizer.py** - Optimize wiki images and assets
- **dead_link_fixer.py** - Automatically fix common broken links
- **wiki_stats.py** - Generate comprehensive wiki statistics

## Contributing

To contribute new tools:
1. Create tool following existing patterns
2. Add comprehensive documentation
3. Include unit tests if applicable
4. Submit PR with example usage

---

*For the liberation of knowledge*
*Tools must be open, accessible, and documented*