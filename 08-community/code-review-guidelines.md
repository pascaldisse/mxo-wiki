# Code Review Guidelines
**Ensuring Quality Through Collaborative Review**

> *"I can only show you the door. You're the one that has to walk through it."* - But we'll review your code before you do.

## 🎯 Purpose of Code Review

Code review in the Matrix Online community serves to:
- **Maintain quality** - Catch bugs before they affect others
- **Share knowledge** - Learn from each other's approaches
- **Ensure consistency** - Follow project standards
- **Build community** - Collaborative improvement

## 📋 Review Process

### For Contributors (Submitting Code)

#### Before Submitting
- [ ] Run all tests locally
- [ ] Check code formatting
- [ ] Update documentation
- [ ] Write clear commit messages
- [ ] Self-review your changes

#### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added (if applicable)
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots here]

## Related Issues
Fixes #(issue number)
```

### For Reviewers

#### Review Checklist
- [ ] **Functionality** - Does it work as intended?
- [ ] **Code Quality** - Is it clean and maintainable?
- [ ] **Performance** - Any optimization needed?
- [ ] **Security** - Any vulnerabilities?
- [ ] **Documentation** - Is it well documented?
- [ ] **Tests** - Adequate test coverage?

#### Review Priorities
1. **Critical** - Security vulnerabilities, data loss risks
2. **High** - Bugs, performance issues
3. **Medium** - Code style, optimization
4. **Low** - Minor formatting, preferences

## 💬 Review Communication

### Giving Feedback

#### Do's ✅
- Be constructive and specific
- Suggest improvements
- Acknowledge good code
- Ask questions for clarity
- Provide code examples

#### Don'ts ❌
- Personal attacks
- Vague criticism
- Nitpicking without value
- Demanding changes without explanation
- Ignoring positive aspects

### Feedback Examples

#### Good Feedback ✅
```
"This function could be more efficient using a map lookup instead of nested loops. Here's an example:
```cpp
std::unordered_map<int, Item> itemMap;
// ... populate map
auto it = itemMap.find(itemId);
if (it != itemMap.end()) {
    return it->second;
}
```
This would reduce complexity from O(n²) to O(1)."
```

#### Poor Feedback ❌
```
"This code is bad. Rewrite it."
```

### Responding to Feedback

#### Best Practices
- Thank reviewers for their time
- Ask for clarification if needed
- Explain your reasoning
- Be open to suggestions
- Update code based on valid feedback

#### Example Response
```
"Thanks for catching that! You're right about the performance issue. 
I've updated to use a map as suggested. I also added a comment 
explaining why we cache these values. Let me know if you see any 
other improvements!"
```

## 🔍 What to Review

### Code Quality
- **Readability** - Can others understand it?
- **Maintainability** - Easy to modify?
- **Efficiency** - Appropriate algorithms?
- **Reusability** - DRY principles followed?

### Matrix Online Specific
- **Game mechanics** - Follows MXO rules?
- **Network protocols** - Correct packet handling?
- **Database queries** - Optimized and safe?
- **Client compatibility** - Works with MXO client?

### Architecture
- **Design patterns** - Appropriate patterns used?
- **Dependencies** - Minimal and necessary?
- **Modularity** - Well-organized code?
- **Scalability** - Handles growth?

## ⏱️ Review Timeline

### Expected Response Times
- **Critical fixes**: Within 24 hours
- **Features**: Within 3 days
- **Documentation**: Within 1 week
- **Major changes**: Allow extra time

### Keeping Reviews Moving
- Set "review by" dates
- Follow up on stale reviews
- Break large PRs into smaller ones
- Communicate delays

## 🛠️ Tools and Automation

### Automated Checks
Before human review:
- CI/CD pipeline tests
- Code formatting (clang-format)
- Static analysis
- Test coverage reports

### Review Tools
- GitHub PR interface
- Inline commenting
- Suggested changes feature
- Review approval system

## 📚 Language-Specific Guidelines

### C++ (Server/Client)
- Memory management review
- RAII principles
- STL usage appropriateness
- Performance considerations

### Python (Tools)
- PEP 8 compliance
- Type hints usage
- Virtual environment setup
- Dependency management

### SQL (Database)
- Query optimization
- Index usage
- SQL injection prevention
- Transaction handling

## 🎓 Learning Through Review

### For New Contributors
- Study approved PRs
- Ask questions during review
- Learn project patterns
- Build on feedback

### For Experienced Developers
- Mentor through reviews
- Share knowledge
- Suggest alternatives
- Explain decisions

## 🚀 Special Considerations

### Large Features
- Design review first
- Incremental PRs
- Architecture documentation
- Team discussion

### Breaking Changes
- Compatibility review
- Migration path
- Documentation updates
- Community notification

### Security Fixes
- Private review first
- Coordinated disclosure
- Quick turnaround
- Careful testing

## 📊 Review Metrics

### Healthy Review Culture
- Average review time: < 3 days
- Constructive feedback: 100%
- Knowledge sharing: High
- Contributor retention: Growing

### Warning Signs
- Long review delays
- Harsh criticism
- Abandoned PRs
- Contributor frustration

## 🤝 Building Review Culture

### Community Values
- **Respect** - Value everyone's time
- **Learning** - Grow together
- **Quality** - Strive for excellence
- **Collaboration** - Work as a team

### Recognition
- Thank thorough reviewers
- Highlight great code
- Share learning moments
- Celebrate improvements

## 📝 Review Templates

### Approval
```
LGTM! (Looks Good To Me)
✅ Tests pass
✅ Code quality excellent
✅ Documentation complete

Great work on [specific aspect]. This will really help with [benefit].
```

### Requesting Changes
```
Thanks for the PR! I found a few things that need adjustment:

1. **[Issue]**: [Description]
   Suggestion: [How to fix]

2. **[Issue]**: [Description]
   Example: [Code sample]

Once these are addressed, this will be ready to merge!
```

### Clarification Needed
```
I'm not quite understanding the approach here. Could you:
- Explain why [specific choice]?
- Add comments around [complex section]?
- Provide example usage?

This will help future maintainers understand the code better.
```

## 🎯 Goal

The goal of code review isn't perfection—it's continuous improvement. Every review makes our code better, our developers stronger, and our community more connected.

---

**Remember**: We're building the future of Matrix Online together. Every review is an opportunity to make that future better.

---

[← Back to Community](index.md) | [GitHub Workflow →](github-workflow-standards.md) | [Contributing →](contribution-framework.md)