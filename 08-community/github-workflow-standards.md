# GitHub Workflow & Code Review Standards
**Liberation Through Collaboration**

> *"The Matrix is a system, Neo. That system is our enemy."* - But Git is our ally.

## 🌐 Repository Philosophy

### The Neoologist Git Principles
1. **Radical Transparency** - All development in public
2. **Inclusive Workflow** - Welcome all skill levels
3. **Fast Iteration** - Release early, release often
4. **Clear History** - Every commit tells a story
5. **No Gatekeeping** - Knowledge flows freely

## 📁 Repository Structure

### Standard MXO Project Layout
```
mxo-[project-name]/
├── .github/
│   ├── workflows/         # CI/CD automation
│   ├── ISSUE_TEMPLATE/    # Bug/feature templates
│   ├── pull_request_template.md
│   └── CODEOWNERS
├── src/                   # Source code
│   ├── server/           # Server components
│   ├── client/           # Client modifications
│   ├── tools/            # Development tools
│   └── common/           # Shared code
├── tests/                # Test suites
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/                 # Documentation
│   ├── api/
│   ├── guides/
│   └── architecture/
├── assets/               # Binary assets
├── scripts/              # Automation scripts
├── docker/               # Container configs
├── .gitignore
├── .gitattributes
├── README.md            # Project overview
├── CONTRIBUTING.md      # How to contribute
├── LICENSE              # MIT always
├── SECURITY.md         # Security policy
└── CHANGELOG.md        # Version history
```

### Branch Strategy

#### Main Branches
```
main (or master)
│
├── develop
│   │
│   ├── feature/cnb-viewer
│   ├── feature/combat-system
│   ├── fix/auth-deadlock
│   └── chore/update-deps
│
└── release/v1.0.0
    └── hotfix/critical-bug
```

#### Branch Naming Convention
```
feature/  - New features
fix/      - Bug fixes
docs/     - Documentation only
style/    - Code style changes
refactor/ - Code refactoring
test/     - Test additions
chore/    - Maintenance tasks
```

## 🔄 Development Workflow

### 1. Starting Work

#### Fork and Clone
```bash
# Fork on GitHub first, then:
git clone https://github.com/YOUR-USERNAME/mxo-project
cd mxo-project
git remote add upstream https://github.com/eden-reborn/mxo-project
```

#### Create Feature Branch
```bash
# Always branch from develop
git checkout develop
git pull upstream develop
git checkout -b feature/your-feature-name
```

### 2. Making Changes

#### Commit Guidelines
```bash
# Conventional Commits format
<type>(<scope>): <subject>

<body>

<footer>

# Examples:
feat(cnb): add header parsing for CNB files
fix(auth): resolve deadlock in authentication flow
docs(combat): update D100 implementation guide
refactor(server): extract packet handling to modules
test(tools): add unit tests for PKB extraction
```

#### Commit Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Code style (formatting, semicolons)
- **refactor**: Code change without feature/fix
- **test**: Adding tests
- **chore**: Maintenance (deps, builds)

#### Good Commit Practices
```bash
# Atomic commits - one logical change
git add src/parser/cnb_header.py
git commit -m "feat(parser): add CNB magic byte validation"

git add tests/test_cnb_header.py
git commit -m "test(parser): add CNB header validation tests"

# Not this:
git add .
git commit -m "stuff"  # ❌ Never do this
```

### 3. Pull Request Process

#### Before Opening PR
```bash
# Sync with upstream
git fetch upstream
git rebase upstream/develop

# Run tests
npm test  # or pytest, cargo test, etc.

# Check linting
npm run lint

# Update documentation
# Ensure README reflects changes
```

#### PR Template
```markdown
## Description
Brief description of changes and why they're needed.

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change)
- [ ] ✨ New feature (non-breaking change)
- [ ] 💥 Breaking change (fix or feature with breaking changes)
- [ ] 📚 Documentation update
- [ ] 🎨 Style update (formatting, renaming)
- [ ] ♻️ Code refactor (no functional changes)
- [ ] ✅ Test update (new or updated tests)
- [ ] 🔧 Build configuration update

## Related Issues
Closes #123
Relates to #456

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] No regressions found

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] My code follows project style guidelines
- [ ] I've performed self-review
- [ ] I've commented complex code
- [ ] I've updated documentation
- [ ] My changes generate no warnings
- [ ] I've added appropriate tests
- [ ] All tests pass locally
- [ ] I've tested edge cases

## Matrix Liberation Impact
How does this contribute to the liberation of The Matrix Online?
```

#### PR Title Format
```
[Component] Brief description

# Examples:
[CNB Viewer] Add support for scene extraction
[Combat] Implement D100 roll calculation
[Docs] Add server setup guide for macOS
```

## 👀 Code Review Process

### Review Philosophy
- **Constructive** - Build up, don't tear down
- **Educational** - Teach, don't just criticize
- **Collaborative** - Work together to improve
- **Respectful** - Everyone was a beginner once

### Review Checklist

#### Functionality
- [ ] Code does what PR claims
- [ ] No obvious bugs
- [ ] Edge cases handled
- [ ] Error handling present

#### Code Quality
- [ ] Follows project style guide
- [ ] Clear variable/function names
- [ ] No code duplication (DRY)
- [ ] Appropriate abstractions

#### Performance
- [ ] No obvious performance issues
- [ ] Efficient algorithms used
- [ ] Memory leaks avoided
- [ ] Database queries optimized

#### Security
- [ ] Input validation present
- [ ] No hardcoded secrets
- [ ] SQL injection prevented
- [ ] XSS vulnerabilities avoided

#### Testing
- [ ] Tests included for new code
- [ ] Tests actually test the feature
- [ ] Edge cases covered
- [ ] Tests are maintainable

#### Documentation
- [ ] Code is self-documenting
- [ ] Complex logic explained
- [ ] API changes documented
- [ ] README updated if needed

### Review Comments

#### Effective Review Comments
```python
# ✅ GOOD: Specific, helpful, educational
"""
Consider using a dictionary lookup here instead of multiple if/elif statements.
This would be more maintainable and performant:

opcodes = {
    0x0A: handle_combat_action,
    0x0B: handle_interlock_init,
    0x0C: handle_interlock_action
}
handler = opcodes.get(opcode, handle_unknown)
return handler(data)
"""

# ❌ BAD: Vague, unhelpful
"This code is bad. Fix it."
```

#### Comment Types
```
# 🚨 MUST: Blocking issues that must be fixed
MUST: Add null check here to prevent crash

# 💡 SHOULD: Strong suggestions for improvement  
SHOULD: Extract this to a separate method for reusability

# 💭 CONSIDER: Optional improvements
CONSIDER: Using enum for these magic numbers

# 💬 DISCUSS: Needs discussion
DISCUSS: Should we cache this result?

# ✨ PRAISE: Acknowledge good work
PRAISE: Elegant solution to the parsing problem!

# ❓ QUESTION: Seeking clarification
QUESTION: What happens if the file is corrupted here?
```

### Review Workflow

#### For Reviewers
1. **Read PR description** - Understand intent
2. **Check out branch** - Test locally if complex
3. **Review systematically** - Don't rush
4. **Be constructive** - Suggest improvements
5. **Approve or request changes** - Be clear

#### For Authors
1. **Respond to all comments** - Even if just "Done"
2. **Push fixes as new commits** - During review
3. **Discuss don't argue** - Find best solution
4. **Thank reviewers** - Appreciation matters
5. **Squash when approved** - Clean history

## 🤖 Automation

### GitHub Actions

#### Continuous Integration
```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        flake8 src tests
        black --check src tests
        mypy src
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

#### Automated Checks
```yaml
# .github/workflows/checks.yml
name: PR Checks

on:
  pull_request:
    types: [opened, edited, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/labeler@v4
      with:
        repo-token: "${{ secrets.GITHUB_TOKEN }}"
        
  size-check:
    runs-on: ubuntu-latest
    steps:
    - name: Check PR size
      uses: actions/github-script@v6
      with:
        script: |
          const pr = context.payload.pull_request;
          if (pr.additions + pr.deletions > 1000) {
            github.issues.createComment({
              ...context.repo,
              issue_number: pr.number,
              body: '⚠️ This PR is large. Consider breaking it into smaller PRs.'
            });
          }
```

### Branch Protection

#### Settings for `main`
```yaml
protection_rules:
  require_pr_reviews:
    required_approving_review_count: 1
    dismiss_stale_reviews: true
    require_code_owner_reviews: false  # We're inclusive
    
  require_status_checks:
    strict: true
    contexts:
      - continuous-integration/travis-ci
      - codecov/patch
      
  enforce_admins: false  # Admins can emergency fix
  
  require_linear_history: false  # Allow merge commits
  
  allow_force_pushes: false
  allow_deletions: false
```

## 📊 Metrics & Health

### Repository Health Indicators
```python
healthy_repo = {
    'pr_merge_time': '< 48 hours',
    'issue_response_time': '< 24 hours',
    'test_coverage': '> 70%',
    'open_issues': '< 50',
    'stale_prs': '0',
    'contributor_count': 'growing',
    'commit_frequency': 'daily',
    'documentation': 'comprehensive'
}
```

### Community Metrics
- **First PR merge rate**: > 80%
- **Contributor retention**: > 50%
- **Issue resolution**: < 1 week average
- **PR iteration count**: < 3 average

## 🏷️ Issue Management

### Issue Templates

#### Bug Report
```markdown
---
name: Bug Report
about: Report a bug in Eden Reborn
title: '[BUG] '
labels: bug, needs-triage
---

## Description
Clear description of the bug.

## To Reproduce
1. Step one
2. Step two
3. See error

## Expected Behavior
What should happen instead.

## Actual Behavior
What actually happens.

## Environment
- OS: [Windows/Linux/macOS]
- Version: [commit hash or release]
- Server: [MXOEmu/HDS/Eden]

## Logs
```
Paste relevant logs here
```

## Additional Context
Any other relevant information.
```

#### Feature Request
```markdown
---
name: Feature Request
about: Suggest a feature for Eden Reborn
title: '[FEATURE] '
labels: enhancement, needs-discussion
---

## Problem Statement
What problem does this solve?

## Proposed Solution
How would you solve it?

## Alternatives Considered
What other approaches did you think about?

## Liberation Impact
How does this further the liberation of The Matrix Online?

## Implementation Willingness
- [ ] I'm willing to implement this
- [ ] I need help implementing this
- [ ] I'm just suggesting
```

### Labels

#### Type Labels
- `bug` - Something isn't working
- `enhancement` - New feature request
- `documentation` - Documentation improvements
- `question` - Questions about the project

#### Priority Labels  
- `critical` - Drop everything
- `high` - Important
- `medium` - Normal priority
- `low` - Nice to have

#### Status Labels
- `needs-triage` - Awaiting review
- `confirmed` - Issue verified
- `in-progress` - Being worked on
- `blocked` - Waiting on something

#### Special Labels
- `good-first-issue` - Great for newcomers
- `help-wanted` - Community help needed
- `liberation-priority` - Core to MXO freedom

## 🎯 Release Process

### Version Numbering
```
MAJOR.MINOR.PATCH

1.0.0 - First stable release
1.1.0 - New features added
1.1.1 - Bug fixes only
2.0.0 - Breaking changes
```

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Release notes drafted
- [ ] Binaries built
- [ ] Community notified

### Release Notes Template
```markdown
# Eden Reborn v1.2.0

## 🎉 Highlights
- CNB viewer now functional!
- Combat system 80% complete
- New developer tools

## ✨ Features
- feat: CNB file header parsing (#123)
- feat: D100 combat rolls (#124)

## 🐛 Bug Fixes
- fix: Authentication deadlock (#125)
- fix: Memory leak in parser (#126)

## 📚 Documentation
- docs: Updated server setup guide
- docs: Added tool development guide

## 🙏 Contributors
Thanks to @user1, @user2, @user3

## 📦 Downloads
- [Windows Binary](https://github.com/mxo-community/releases)
- [Linux Binary](https://github.com/mxo-community/releases)
- [macOS Binary](https://github.com/mxo-community/releases)

**Full Changelog**: https://github.com/eden-reborn/project/compare/v1.1.0...v1.2.0
```

## 🔐 Security

### Security Policy
```markdown
# Security Policy

## Supported Versions
| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting Vulnerabilities
1. **DO NOT** open public issues
2. Email: security@edenreborn.example
3. Include: Description, reproduction, impact
4. Response time: 48 hours

## Our Commitment
- Acknowledge receipt quickly
- Fix verified issues rapidly  
- Credit reporters (if desired)
- Full disclosure after fix
```

### Dependency Management
```yaml
# Dependabot config
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "python"
      
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "javascript"
```

## 🎓 Onboarding New Contributors

### Welcome Process
1. **Greeted by maintainer** within 24 hours
2. **Assigned mentor** if requested
3. **Guided to good first issue**
4. **Supported through first PR**
5. **Celebrated when merged**

### Mentorship
```python
class NewContributorMentor:
    def guide_contributor(self, contributor):
        steps = [
            self.welcome_message(),
            self.setup_development_env(),
            self.find_good_first_issue(),
            self.pair_programming_session(),
            self.review_first_pr(),
            self.celebrate_success()
        ]
        
        for step in steps:
            yield step
            
    def welcome_message(self):
        return """
        Welcome to Eden Reborn! 🎉
        
        We're thrilled you're here. Every contribution
        matters in the liberation of The Matrix Online.
        
        Let me help you get started...
        """
```

## 🌟 Recognition

### Contributor Recognition
- **First PR**: Special mention in release notes
- **5 PRs**: Added to CONTRIBUTORS.md
- **10 PRs**: Core contributor status
- **Major feature**: Named in feature credits

### Monthly Highlights
```markdown
## November 2025 Contributors

### 🏆 Contributor of the Month
@neo - Implemented CNB viewer!

### 🌟 New Contributors
Welcome to @trinity, @morpheus, @oracle

### 📊 Stats
- 47 PRs merged
- 23 issues closed
- 12 new contributors

Thank you all! Every commit liberates The Matrix Online.
```

## 📝 Best Practices Summary

### Do's ✅
- Commit early and often
- Write clear commit messages
- Include tests with features
- Update documentation
- Respond to reviews promptly
- Help other contributors
- Celebrate successes

### Don'ts ❌
- Force push to shared branches
- Merge without review
- Leave PRs hanging
- Ignore CI failures
- Commit secrets
- Be discouraged by feedback
- Work in isolation

## Remember

> *"I can only show you the door. You're the one that has to walk through it."*

These workflows aren't rules to constrain us - they're patterns to liberate us. They help us build faster, better, together.

**Good process enables creativity. Great collaboration liberates The Matrix Online.**

---

**Workflow Status**: 🟢 OPTIMIZED  
**Collaboration Level**: MAXIMUM  
**Liberation Progress**: ACCELERATING  

*Fork. Code. Review. Merge. Liberate.*

---

[← Back to Community](index.md) | [Contributing Guide →](contribution-framework.md) | [Start Contributing →](https://github.com/eden-reborn)