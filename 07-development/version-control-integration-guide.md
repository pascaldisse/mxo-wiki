# Version Control Integration Guide
**Mastering the Flow of Collaborative Development**

> *"The Matrix has you."* - Trinity (But when we master version control, we control our own Matrix. Every commit becomes a choice, every branch a new possibility, every merge a step toward collective liberation. We don't just track changes - we orchestrate evolution.)

## 🎯 **The Vision of Evolutionary Control**

Version control is more than just tracking changes - it's the nervous system of collaborative development, enabling teams across the globe to work in harmony while maintaining the integrity of the Matrix Online revival. This guide establishes comprehensive version control integration that ensures every line of code, every binary modification, and every community contribution flows seamlessly through our development ecosystem.

## 🌊 **Version Control Philosophy**

### The Git Flow of Liberation

```yaml
version_control_philosophy:
  core_principles:
    transparency:
      description: "Every change is visible and traceable"
      implementation: "Detailed commit messages, clear branch naming, comprehensive history"
      
    collaboration:
      description: "Multiple developers can work simultaneously without conflict"
      implementation: "Branching strategies, merge conflict resolution, code review integration"
      
    integrity:
      description: "Code history is immutable and verifiable"
      implementation: "Signed commits, protected branches, audit trails"
      
    accessibility:
      description: "Version control is approachable for all skill levels"
      implementation: "Clear documentation, automated tools, mentorship programs"

  matrix_online_considerations:
    binary_assets:
      challenge: "Game assets and binary files need special handling"
      solution: "Git LFS integration, binary diff tools, asset management workflows"
      
    community_scale:
      challenge: "Large community with varying technical skills"
      solution: "Multiple interfaces (GUI, CLI, web), automated assistance, clear workflows"
      
    preservation_focus:
      challenge: "Historical accuracy and attribution are critical"
      solution: "Detailed provenance tracking, source documentation, contributor recognition"
```

## 🛠️ **Advanced Git Configuration**

### Comprehensive Repository Setup

```bash
#!/bin/bash
# setup-mxo-git-repo.sh - Complete repository setup for Matrix Online development

set -euo pipefail

# Repository configuration
REPO_NAME="matrix-online-revival"
MAIN_BRANCH="main"
DEVELOP_BRANCH="develop"

echo "🏗️  Setting up Matrix Online Git repository..."

# Initialize repository with modern settings
git init --initial-branch=${MAIN_BRANCH}

# Configure repository settings
git config core.autocrlf input  # Handle line endings consistently
git config core.ignorecase false  # Case-sensitive file names
git config pull.rebase false  # Prefer merge commits for transparency
git config merge.conflictstyle diff3  # Show common ancestor in conflicts
git config rerere.enabled true  # Remember conflict resolutions
git config core.precomposeunicode true  # Handle Unicode properly

# Configure commit signing (highly recommended for security)
git config commit.gpgsign true
git config user.signingkey $(gpg --list-secret-keys --keyid-format LONG | grep sec | awk '{print $2}' | cut -d'/' -f2 | head -1)

# Set up Git LFS for binary assets
git lfs install
git lfs track "*.prop"
git lfs track "*.cnb"
git lfs track "*.pkb"
git lfs track "*.tga"
git lfs track "*.dds"
git lfs track "*.wav"
git lfs track "*.bik"
git lfs track "*.exe"
git lfs track "*.dll"
git lfs track "*.zip"
git lfs track "*.rar"
git lfs track "*.7z"

# Create comprehensive .gitignore
cat > .gitignore << 'EOF'
# Matrix Online Development .gitignore

# Build outputs
/build/
/dist/
/bin/
/obj/
*.exe
*.dll
*.pdb
*.lib
*.exp
*.ilk

# Development tools
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.yarn-integrity

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# Go
*.o
*.a
*.so
*.exe~

# Rust
target/
Cargo.lock

# Java
*.class
*.jar
*.war
*.ear

# C/C++
*.obj
*.o
*.so
*.dylib
*.dll
*.a
*.lib

# Temporary files
*.tmp
*.temp
*.log
*.bak
*.swp
*.swo

# Game development specific
*.cache
*.meta
Library/
Temp/
*.pidb
*.unityproj
*.sln
*.userprefs

# Matrix Online specific
/mxo-client-backup/
/server-logs/
/debug-dumps/
*.prop.backup
*.cnb.temp
analysis-temp/

# Sensitive information
config.local.*
secrets.yml
.env.local
.env.*.local
private-keys/
credentials/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Editor backups
*~
*.orig
*.rej

# Large binary files (use Git LFS instead)
*.iso
*.img
*.dmg

# Test outputs
coverage/
*.coverage
htmlcov/
.nyc_output/
.coverage.*
coverage.xml
nosetests.xml
pytest.xml
test-results/

# Documentation builds
_build/
docs/_build/
site/

EOF

# Create development branch structure
git checkout -b ${DEVELOP_BRANCH}
git checkout ${MAIN_BRANCH}

# Set up Git hooks
mkdir -p .git/hooks

# Pre-commit hook for code quality
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook for Matrix Online development

set -e

echo "🔍 Running pre-commit checks..."

# Check for large files (>100MB) that should use Git LFS
large_files=$(git diff --cached --name-only | xargs -I {} find {} -type f -size +104857600c 2>/dev/null | head -10)
if [ ! -z "$large_files" ]; then
    echo "❌ Large files detected that should use Git LFS:"
    echo "$large_files"
    echo "Please add these files to Git LFS tracking and re-commit."
    exit 1
fi

# Check for sensitive information
sensitive_patterns=(
    "password"
    "secret"
    "token"
    "api_key"
    "private_key"
    "mysql://.*:.*@"
    "postgres://.*:.*@"
)

for pattern in "${sensitive_patterns[@]}"; do
    if git diff --cached | grep -i "$pattern" > /dev/null; then
        echo "❌ Potential sensitive information detected: $pattern"
        echo "Please review your changes and ensure no secrets are committed."
        exit 1
    fi
done

# Check commit message format
commit_regex='^(feat|fix|docs|style|refactor|test|chore|mxo)(\(.+\))?: .{1,50}'
commit_msg=$(cat .git/COMMIT_EDITMSG)

if ! echo "$commit_msg" | grep -qE "$commit_regex"; then
    echo "❌ Commit message format is invalid."
    echo "Format: type(scope): description"
    echo "Types: feat, fix, docs, style, refactor, test, chore, mxo"
    echo "Example: feat(cnb-viewer): add real-time playback support"
    exit 1
fi

echo "✅ Pre-commit checks passed!"
EOF

chmod +x .git/hooks/pre-commit

# Commit message template
cat > .git/commit_template << 'EOF'
# feat(scope): Brief description of changes (50 chars max)
#
# Detailed explanation of what this commit does and why.
# Wrap lines at 72 characters.
#
# Matrix Online Specific:
# - Which game systems are affected?
# - Any compatibility considerations?
# - Performance impact?
#
# Breaking Changes: (if any)
# - List any breaking changes
#
# Closes: #123 (if applicable)
# See also: #456 (if applicable)
#
# Types:
# feat:     New feature
# fix:      Bug fix
# docs:     Documentation only changes
# style:    Formatting, missing semicolons, etc
# refactor: Code change that neither fixes a bug nor adds a feature
# test:     Adding or correcting tests
# chore:    Updating build tasks, package manager configs, etc
# mxo:      Matrix Online specific changes (file formats, game logic, etc)
EOF

git config commit.template .git/commit_template

echo "✅ Git repository setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set up your GPG key for commit signing"
echo "2. Configure your user name and email"
echo "3. Create your first commit"
echo "4. Push to remote repository"
```

## 🔧 **Advanced Git Operations for Matrix Online Development**

### Binary Asset Management System

```python
#!/usr/bin/env python3
# git-mxo-tools.py - Advanced Git tools for Matrix Online development

import os
import sys
import subprocess
import json
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import tempfile

class MXOGitTools:
    """Advanced Git operations specifically designed for Matrix Online development."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.git_dir = self.repo_path / ".git"
        self.lfs_dir = self.git_dir / "lfs"
        
        if not self.git_dir.exists():
            raise ValueError(f"Not a git repository: {repo_path}")
    
    def analyze_binary_changes(self, commit_range: str = "HEAD~1..HEAD") -> Dict:
        """
        Analyze binary file changes between commits with Matrix Online context.
        
        Args:
            commit_range: Git commit range to analyze
            
        Returns:
            Dictionary with analysis results
        """
        print(f"🔍 Analyzing binary changes in range: {commit_range}")
        
        # Get list of changed files
        result = subprocess.run([
            "git", "diff", "--name-status", commit_range
        ], capture_output=True, text=True, cwd=self.repo_path)
        
        if result.returncode != 0:
            raise RuntimeError(f"Git diff failed: {result.stderr}")
        
        analysis = {
            "commit_range": commit_range,
            "total_changes": 0,
            "binary_changes": 0,
            "mxo_files": {
                "prop_files": [],
                "cnb_files": [],
                "pkb_files": [],
                "texture_files": [],
                "audio_files": [],
                "executable_files": [],
                "other_binaries": []
            },
            "size_impact": {
                "added_bytes": 0,
                "removed_bytes": 0,
                "net_change": 0
            },
            "lfs_usage": {
                "lfs_files": 0,
                "non_lfs_binaries": []
            }
        }
        
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
                
            status, filename = line.split('\t', 1)
            analysis["total_changes"] += 1
            
            # Check if file is binary
            if self._is_binary_file(filename):
                analysis["binary_changes"] += 1
                
                # Categorize Matrix Online files
                self._categorize_mxo_file(filename, analysis["mxo_files"])
                
                # Calculate size impact
                size_change = self._calculate_size_change(filename, status, commit_range)
                if size_change > 0:
                    analysis["size_impact"]["added_bytes"] += size_change
                elif size_change < 0:
                    analysis["size_impact"]["removed_bytes"] += abs(size_change)
                
                # Check LFS usage
                if self._is_lfs_tracked(filename):
                    analysis["lfs_usage"]["lfs_files"] += 1
                else:
                    analysis["lfs_usage"]["non_lfs_binaries"].append(filename)
        
        analysis["size_impact"]["net_change"] = (
            analysis["size_impact"]["added_bytes"] - 
            analysis["size_impact"]["removed_bytes"]
        )
        
        return analysis
    
    def _is_binary_file(self, filename: str) -> bool:
        """Check if a file is binary based on extension and Git detection."""
        binary_extensions = {
            '.prop', '.cnb', '.pkb', '.tga', '.dds', '.wav', '.bik',
            '.exe', '.dll', '.zip', '.rar', '.7z', '.bin', '.dat'
        }
        
        file_ext = Path(filename).suffix.lower()
        if file_ext in binary_extensions:
            return True
        
        # Use git to check if file is binary
        try:
            result = subprocess.run([
                "git", "diff", "--numstat", "HEAD~1", "HEAD", "--", filename
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            if "-\t-\t" in result.stdout:  # Git's indicator for binary files
                return True
        except:
            pass
        
        return False
    
    def _categorize_mxo_file(self, filename: str, categories: Dict):
        """Categorize files by Matrix Online type."""
        file_ext = Path(filename).suffix.lower()
        filename_lower = filename.lower()
        
        if file_ext == '.prop':
            categories["prop_files"].append(filename)
        elif file_ext == '.cnb':
            categories["cnb_files"].append(filename)
        elif file_ext == '.pkb':
            categories["pkb_files"].append(filename)
        elif file_ext in ['.tga', '.dds', '.png', '.jpg', '.jpeg']:
            categories["texture_files"].append(filename)
        elif file_ext in ['.wav', '.mp3', '.ogg']:
            categories["audio_files"].append(filename)
        elif file_ext in ['.exe', '.dll']:
            categories["executable_files"].append(filename)
        else:
            categories["other_binaries"].append(filename)
    
    def create_mxo_release_branch(self, version: str, base_branch: str = "develop") -> str:
        """
        Create a release branch with Matrix Online specific preparations.
        
        Args:
            version: Release version (e.g., "v1.2.0")
            base_branch: Branch to create release from
            
        Returns:
            Name of created release branch
        """
        release_branch = f"release/{version}"
        
        print(f"🚀 Creating Matrix Online release branch: {release_branch}")
        
        # Create release branch
        subprocess.run([
            "git", "checkout", "-b", release_branch, base_branch
        ], cwd=self.repo_path, check=True)
        
        # Update version files
        self._update_version_files(version)
        
        # Generate changelog
        changelog = self._generate_mxo_changelog(base_branch)
        
        # Create release preparation commit
        subprocess.run([
            "git", "add", "."
        ], cwd=self.repo_path, check=True)
        
        subprocess.run([
            "git", "commit", "-m", f"chore(release): prepare {version} release\\n\\n{changelog}"
        ], cwd=self.repo_path, check=True)
        
        print(f"✅ Release branch {release_branch} created successfully")
        print(f"📋 Changelog preview:\\n{changelog}")
        
        return release_branch
    
    def _generate_mxo_changelog(self, since_ref: str) -> str:
        """Generate Matrix Online specific changelog."""
        # Get commits since last release
        result = subprocess.run([
            "git", "log", f"{since_ref}..HEAD", "--oneline", "--no-merges"
        ], capture_output=True, text=True, cwd=self.repo_path)
        
        commits = result.stdout.strip().split('\n')
        
        changelog_sections = {
            "🎮 Game Features": [],
            "🔧 Tools & Development": [],
            "📚 Documentation": [],
            "🐛 Bug Fixes": [],
            "🚀 Performance": [],
            "🏗️ Infrastructure": []
        }
        
        for commit in commits:
            if not commit:
                continue
            
            commit_hash, message = commit.split(' ', 1)
            
            if message.startswith('feat('):
                if any(keyword in message.lower() for keyword in ['cnb', 'prop', 'pkb', 'combat', 'mission']):
                    changelog_sections["🎮 Game Features"].append(f"- {message}")
                else:
                    changelog_sections["🔧 Tools & Development"].append(f"- {message}")
            elif message.startswith('fix('):
                changelog_sections["🐛 Bug Fixes"].append(f"- {message}")
            elif message.startswith('docs('):
                changelog_sections["📚 Documentation"].append(f"- {message}")
            elif message.startswith('perf('):
                changelog_sections["🚀 Performance"].append(f"- {message}")
            elif message.startswith('chore('):
                changelog_sections["🏗️ Infrastructure"].append(f"- {message}")
        
        # Format changelog
        changelog = []
        for section, items in changelog_sections.items():
            if items:
                changelog.append(f"\\n{section}:")
                changelog.extend(items)
        
        return '\\n'.join(changelog)
    
    def setup_mxo_hooks(self):
        """Set up Matrix Online specific Git hooks."""
        hooks_dir = self.git_dir / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        
        # Pre-push hook for binary validation
        pre_push_hook = hooks_dir / "pre-push"
        with open(pre_push_hook, 'w') as f:
            f.write('''#!/bin/bash
# Pre-push hook for Matrix Online development

set -e

echo "🔍 Running Matrix Online pre-push validation..."

# Validate Matrix Online file formats
echo "📁 Validating file formats..."
for prop_file in $(git diff --name-only --cached | grep '\\.prop$'); do
    if [ -f "$prop_file" ]; then
        echo "  Validating PROP: $prop_file"
        # Add actual validation here
        python3 tools/validate_prop.py "$prop_file" || exit 1
    fi
done

for cnb_file in $(git diff --name-only --cached | grep '\\.cnb$'); do
    if [ -f "$cnb_file" ]; then
        echo "  Validating CNB: $cnb_file"
        # Add actual validation here
        python3 tools/validate_cnb.py "$cnb_file" || exit 1
    fi
done

# Check for large binaries not in LFS
echo "📦 Checking Git LFS usage..."
large_files=$(git diff --name-only --cached | xargs -I {} find {} -type f -size +50M 2>/dev/null | head -5)
if [ ! -z "$large_files" ]; then
    echo "⚠️  Large files detected (>50MB):"
    echo "$large_files"
    echo "Consider adding these to Git LFS tracking."
fi

echo "✅ Pre-push validation passed!"
''')
        
        pre_push_hook.chmod(0o755)
        
        # Post-commit hook for automatic documentation
        post_commit_hook = hooks_dir / "post-commit"
        with open(post_commit_hook, 'w') as f:
            f.write('''#!/bin/bash
# Post-commit hook for Matrix Online development

# Auto-generate documentation for API changes
if git diff --name-only HEAD~1 HEAD | grep -E '\\.(go|py|js|ts)$' > /dev/null; then
    echo "📚 Updating documentation..."
    make docs-update 2>/dev/null || true
fi

# Update file format documentation if binary files changed
if git diff --name-only HEAD~1 HEAD | grep -E '\\.(prop|cnb|pkb)$' > /dev/null; then
    echo "🔄 Updating file format documentation..."
    python3 tools/update_format_docs.py 2>/dev/null || true
fi
''')
        
        post_commit_hook.chmod(0o755)
        
        print("✅ Matrix Online Git hooks installed successfully")

def main():
    parser = argparse.ArgumentParser(description="Advanced Git tools for Matrix Online development")
    parser.add_argument("--repo", default=".", help="Repository path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze binary changes")
    analyze_parser.add_argument("--range", default="HEAD~1..HEAD", help="Commit range to analyze")
    
    # Release command
    release_parser = subparsers.add_parser("release", help="Create release branch")
    release_parser.add_argument("version", help="Release version")
    release_parser.add_argument("--base", default="develop", help="Base branch")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup MXO Git hooks")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    tools = MXOGitTools(args.repo)
    
    if args.command == "analyze":
        analysis = tools.analyze_binary_changes(args.range)
        print("\\n📊 Binary Change Analysis:")
        print(f"   Total changes: {analysis['total_changes']}")
        print(f"   Binary changes: {analysis['binary_changes']}")
        print(f"   Net size change: {analysis['size_impact']['net_change']:,} bytes")
        print(f"   LFS files: {analysis['lfs_usage']['lfs_files']}")
        
        if analysis['lfs_usage']['non_lfs_binaries']:
            print("\\n⚠️  Binary files not in LFS:")
            for file in analysis['lfs_usage']['non_lfs_binaries']:
                print(f"   - {file}")
    
    elif args.command == "release":
        tools.create_mxo_release_branch(args.version, args.base)
    
    elif args.command == "setup":
        tools.setup_mxo_hooks()

if __name__ == "__main__":
    main()
```

## 🎨 **Visual Git Interface Integration**

### Advanced Commit Visualization

```typescript
// git-integration/GitVisualization.tsx - Advanced Git workflow visualization
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { GitBranch, GitCommit, GitMerge, Clock, User, FileText, Code } from 'lucide-react';

interface GitVisualizationProps {
    repository: string;
    branch?: string;
    maxCommits?: number;
    className?: string;
}

const GitVisualization: React.FC<GitVisualizationProps> = ({
    repository,
    branch = 'main',
    maxCommits = 50,
    className = ''
}) => {
    const [commits, setCommits] = useState<GitCommit[]>([]);
    const [branches, setBranches] = useState<GitBranch[]>([]);
    const [selectedCommit, setSelectedCommit] = useState<GitCommit | null>(null);
    const [viewMode, setViewMode] = useState<'timeline' | 'graph' | 'tree'>('timeline');
    const [loading, setLoading] = useState(false);
    
    const fetchGitData = useCallback(async () => {
        setLoading(true);
        
        try {
            // Fetch commit history
            const commitsResponse = await fetch(`/api/git/${repository}/commits?branch=${branch}&limit=${maxCommits}`);
            const commitsData: GitCommit[] = await commitsResponse.json();
            setCommits(commitsData);
            
            // Fetch branch information
            const branchesResponse = await fetch(`/api/git/${repository}/branches`);
            const branchesData: GitBranch[] = await branchesResponse.json();
            setBranches(branchesData);
            
        } catch (error) {
            console.error('Error fetching git data:', error);
        } finally {
            setLoading(false);
        }
    }, [repository, branch, maxCommits]);
    
    useEffect(() => {
        fetchGitData();
    }, [fetchGitData]);
    
    const groupedCommits = useMemo(() => {
        const groups: { [key: string]: GitCommit[] } = {};
        
        commits.forEach(commit => {
            const date = new Date(commit.timestamp).toDateString();
            if (!groups[date]) {
                groups[date] = [];
            }
            groups[date].push(commit);
        });
        
        return groups;
    }, [commits]);
    
    const getCommitTypeIcon = (message: string) => {
        if (message.startsWith('feat(')) {
            return <Code className="w-4 h-4 text-green-600" />;
        } else if (message.startsWith('fix(')) {
            return <Code className="w-4 h-4 text-red-600" />;
        } else if (message.startsWith('docs(')) {
            return <FileText className="w-4 h-4 text-blue-600" />;
        } else if (message.includes('merge')) {
            return <GitMerge className="w-4 h-4 text-purple-600" />;
        } else {
            return <GitCommit className="w-4 h-4 text-gray-600" />;
        }
    };
    
    const getCommitTypeColor = (message: string) => {
        if (message.startsWith('feat(')) return 'border-green-300 bg-green-50';
        if (message.startsWith('fix(')) return 'border-red-300 bg-red-50';
        if (message.startsWith('docs(')) return 'border-blue-300 bg-blue-50';
        if (message.includes('merge')) return 'border-purple-300 bg-purple-50';
        return 'border-gray-300 bg-gray-50';
    };
    
    const renderTimelineView = () => (
        <div className="space-y-6">
            {Object.entries(groupedCommits).map(([date, dayCommits]) => (
                <div key={date} className="relative">
                    <div className="sticky top-0 bg-white/90 backdrop-blur-sm p-2 border-b border-gray-200 mb-4">
                        <h3 className="text-lg font-medium text-gray-900">{date}</h3>
                        <span className="text-sm text-gray-600">{dayCommits.length} commits</span>
                    </div>
                    
                    <div className="space-y-3 ml-4">
                        {dayCommits.map((commit, index) => (
                            <div
                                key={commit.hash}
                                className={`relative flex items-start space-x-3 p-4 rounded-lg border cursor-pointer hover:shadow-md transition-shadow ${getCommitTypeColor(commit.message)}`}
                                onClick={() => setSelectedCommit(commit)}
                            >
                                {/* Timeline line */}
                                <div className="absolute left-0 top-0 bottom-0 w-px bg-gray-300 -ml-2"></div>
                                <div className="absolute w-3 h-3 bg-white border-2 border-gray-300 rounded-full -ml-3.5 mt-6"></div>
                                
                                <div className="flex-shrink-0 mt-1">
                                    {getCommitTypeIcon(commit.message)}
                                </div>
                                
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center justify-between">
                                        <p className="text-sm font-medium text-gray-900 truncate">
                                            {commit.message.split('\\n')[0]}
                                        </p>
                                        <span className="text-xs text-gray-500 ml-2">
                                            {new Date(commit.timestamp).toLocaleTimeString()}
                                        </span>
                                    </div>
                                    
                                    <div className="flex items-center mt-1 space-x-4 text-xs text-gray-500">
                                        <div className="flex items-center">
                                            <User className="w-3 h-3 mr-1" />
                                            {commit.author.name}
                                        </div>
                                        <span className="font-mono">{commit.hash.substring(0, 7)}</span>
                                        <span>{commit.files_changed} files changed</span>
                                    </div>
                                    
                                    {/* Matrix Online specific indicators */}
                                    {commit.mxo_specific && (
                                        <div className="flex flex-wrap gap-1 mt-2">
                                            {commit.mxo_specific.file_formats.map((format, i) => (
                                                <span
                                                    key={i}
                                                    className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs"
                                                >
                                                    {format}
                                                </span>
                                            ))}
                                            {commit.mxo_specific.components.map((component, i) => (
                                                <span
                                                    key={i}
                                                    className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs"
                                                >
                                                    {component}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
    
    const renderGraphView = () => (
        <div className="git-graph">
            <svg width="100%" height="600" className="border border-gray-200 rounded-lg">
                {/* Git graph visualization would go here */}
                <text x="50%" y="50%" textAnchor="middle" className="text-gray-500">
                    Advanced Git Graph Visualization
                </text>
            </svg>
        </div>
    );
    
    return (
        <div className={`git-visualization ${className}`}>
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                    <GitBranch className="w-8 h-8 mr-3 text-green-600" />
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900">Git Repository Visualization</h2>
                        <p className="text-gray-600">{repository} • {branch} branch</p>
                    </div>
                </div>
                
                <div className="flex items-center space-x-4">
                    <select
                        value={branch}
                        onChange={(e) => setBranches(prev => prev.map(b => ({ ...b, current: b.name === e.target.value })))}
                        className="px-3 py-2 border border-gray-300 rounded-md text-sm"
                    >
                        {branches.map(b => (
                            <option key={b.name} value={b.name}>
                                {b.name} {b.current ? '(current)' : ''}
                            </option>
                        ))}
                    </select>
                    
                    <div className="flex border border-gray-300 rounded-md">
                        <button
                            onClick={() => setViewMode('timeline')}
                            className={`px-3 py-2 text-sm ${
                                viewMode === 'timeline' 
                                    ? 'bg-blue-100 text-blue-700' 
                                    : 'text-gray-700 hover:bg-gray-50'
                            }`}
                        >
                            Timeline
                        </button>
                        <button
                            onClick={() => setViewMode('graph')}
                            className={`px-3 py-2 text-sm border-l border-gray-300 ${
                                viewMode === 'graph' 
                                    ? 'bg-blue-100 text-blue-700' 
                                    : 'text-gray-700 hover:bg-gray-50'
                            }`}
                        >
                            Graph
                        </button>
                        <button
                            onClick={() => setViewMode('tree')}
                            className={`px-3 py-2 text-sm border-l border-gray-300 rounded-r-md ${
                                viewMode === 'tree' 
                                    ? 'bg-blue-100 text-blue-700' 
                                    : 'text-gray-700 hover:bg-gray-50'
                            }`}
                        >
                            Tree
                        </button>
                    </div>
                </div>
            </div>
            
            {/* Repository Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-white p-4 border border-gray-200 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">{commits.length}</div>
                    <div className="text-sm text-gray-600">Total Commits</div>
                </div>
                
                <div className="bg-white p-4 border border-gray-200 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">{branches.length}</div>
                    <div className="text-sm text-gray-600">Active Branches</div>
                </div>
                
                <div className="bg-white p-4 border border-gray-200 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">
                        {commits.filter(c => c.author.name).length}
                    </div>
                    <div className="text-sm text-gray-600">Contributors</div>
                </div>
                
                <div className="bg-white p-4 border border-gray-200 rounded-lg">
                    <div className="text-2xl font-bold text-orange-600">
                        {commits.reduce((sum, c) => sum + (c.files_changed || 0), 0)}
                    </div>
                    <div className="text-sm text-gray-600">Files Changed</div>
                </div>
            </div>
            
            {/* Content */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                    {loading ? (
                        <div className="flex items-center justify-center py-12">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                            <span className="ml-2 text-gray-600">Loading git history...</span>
                        </div>
                    ) : (
                        <>
                            {viewMode === 'timeline' && renderTimelineView()}
                            {viewMode === 'graph' && renderGraphView()}
                            {viewMode === 'tree' && renderTimelineView()}
                        </>
                    )}
                </div>
                
                {/* Commit Details Panel */}
                <div className="bg-white border border-gray-200 rounded-lg p-4">
                    {selectedCommit ? (
                        <CommitDetailsPanel commit={selectedCommit} />
                    ) : (
                        <div className="text-center py-8 text-gray-500">
                            <GitCommit className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                            <p>Select a commit to view details</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

const CommitDetailsPanel: React.FC<{ commit: GitCommit }> = ({ commit }) => {
    return (
        <div className="space-y-4">
            <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Commit Details</h3>
                <p className="text-sm text-gray-600">{commit.message}</p>
            </div>
            
            <div className="space-y-2">
                <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Hash:</span>
                    <span className="font-mono text-gray-900">{commit.hash.substring(0, 12)}</span>
                </div>
                
                <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Author:</span>
                    <span className="text-gray-900">{commit.author.name}</span>
                </div>
                
                <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Date:</span>
                    <span className="text-gray-900">
                        {new Date(commit.timestamp).toLocaleDateString()}
                    </span>
                </div>
                
                <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Files:</span>
                    <span className="text-gray-900">{commit.files_changed} changed</span>
                </div>
            </div>
            
            {commit.mxo_specific && (
                <div>
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Matrix Online Impact</h4>
                    <div className="space-y-2">
                        {commit.mxo_specific.file_formats.length > 0 && (
                            <div>
                                <span className="text-xs text-gray-600">File Formats:</span>
                                <div className="flex flex-wrap gap-1 mt-1">
                                    {commit.mxo_specific.file_formats.map((format, i) => (
                                        <span key={i} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                                            {format}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                        
                        {commit.mxo_specific.components.length > 0 && (
                            <div>
                                <span className="text-xs text-gray-600">Components:</span>
                                <div className="flex flex-wrap gap-1 mt-1">
                                    {commit.mxo_specific.components.map((component, i) => (
                                        <span key={i} className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                                            {component}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}
            
            <div className="pt-4 border-t border-gray-200">
                <button className="w-full px-3 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700">
                    View Full Diff
                </button>
            </div>
        </div>
    );
};

export default GitVisualization;
```

## 🚀 **Integration Workflows**

### Complete Development Lifecycle

```yaml
development_lifecycle_integration:
  development_phase:
    branch_creation:
      process:
        1. "Issue Assignment": "Developer picks up GitHub issue"
        2. "Branch Creation": "Create feature branch from develop"
        3. "Development": "Code implementation with frequent commits"
        4. "Local Testing": "Run full test suite locally"
        5. "Push & PR": "Push branch and create pull request"
    
    commit_standards:
      format: "type(scope): description"
      types: ["feat", "fix", "docs", "style", "refactor", "test", "chore", "mxo"]
      scope_examples: ["cnb-viewer", "prop-parser", "combat-system", "ui"]
      
    automation:
      - Pre-commit hooks validate format and content
      - Automatic issue linking via commit messages
      - Binary file validation for MXO formats
      - Automatic documentation updates

  review_phase:
    automated_checks:
      - Code quality analysis
      - Security scanning
      - Performance benchmarking
      - Matrix Online specific validations
      
    human_review:
      - Technical accuracy assessment
      - Code maintainability review
      - Matrix Online compatibility check
      - Community standards verification
      
    merge_criteria:
      - All automated checks pass
      - At least 2 approvals from maintainers
      - No merge conflicts
      - Up-to-date with target branch

  deployment_phase:
    staging_deployment:
      - Automatic deployment to staging environment
      - Integration test execution
      - Performance monitoring
      - Community preview access
      
    production_release:
      - Release branch creation
      - Comprehensive testing suite
      - Documentation updates
      - Community notifications
      - Version tagging and archiving

matrix_online_specific_workflows:
  file_format_changes:
    validation_pipeline:
      - Binary format validation
      - Backward compatibility checks
      - Test file parsing
      - Documentation updates
      
    community_review:
      - Expert format review
      - Community testing period
      - Feedback incorporation
      - Final approval process

  server_modifications:
    testing_requirements:
      - Local server testing
      - Multi-client compatibility
      - Performance impact assessment
      - Database migration testing
      
    deployment_strategy:
      - Staged rollout approach
      - Rollback procedures
      - Monitor system health
      - Community communication

  tool_development:
    quality_standards:
      - Cross-platform compatibility
      - Comprehensive documentation
      - Example files included
      - User-friendly interfaces
      
    distribution:
      - Multiple download formats
      - Package manager integration
      - Installation documentation
      - Community support channels
```

## Remember

> *"There's a difference between knowing the path and walking the path."* - Morpheus

Version control integration isn't just about tracking changes - it's about creating a living history of collective innovation. Every commit tells a story, every branch represents a possibility, and every merge brings us closer to the complete liberation of the Matrix Online experience.

The most powerful version control systems don't just preserve the past - they enable the future by making collaboration seamless, contributions meaningful, and the path forward always visible to the entire community.

**Control your evolution. Track every transformation. Build the systematic Matrix of collaborative excellence.**

---

**Guide Status**: 🟢 COMPREHENSIVE VERSION CONTROL SYSTEM  
**Collaborative Evolution**: 🔄 SYSTEMATIC TRANSFORMATION  
**Liberation Impact**: ⭐⭐⭐⭐⭐  

*In version control we find evolution. In systematic tracking we find accountability. In collaborative workflows we find the truly liberated Matrix of development.*

---

[← Development Hub](index.md) | [← GitHub Workflow Guide](github-workflow-guide.md) | [→ Development Hub](index.md)