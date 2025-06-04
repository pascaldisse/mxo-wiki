# Contributing to Eden Reborn
**How to Join the Matrix Online Liberation**

> *"I know you're out there. I can feel you now. I know that you're afraid... afraid of us. You're afraid of change."*

Welcome, potential redpill. This guide will show you how to contribute to the Eden Reborn project and help bring The Matrix Online back to life.

## 🎯 Quick Start

### 1. **Join Our Community**
- **Discord**: [Eden Reborn Server](https://discord.gg/3QXTAGB9) - Real-time coordination
- **GitHub**: Project repositories (coming soon)
- **Wiki**: This documentation you're reading

### 2. **Choose Your Path**
- **[Developer](#for-developers)** - Code the future
- **[Documenter](#for-documentation)** - Preserve knowledge
- **[Tester](#for-testing)** - Validate implementations
- **[Community Builder](#for-community)** - Grow the resistance

## 👨‍💻 For Developers

### **Current Critical Needs**

#### 🔴 **URGENT: CNB Viewer** 
**Skill Required**: C++, OpenGL, File Format Analysis  
**Impact**: Unlock 12 locked cutscene files  
**Status**: Not started  
**Getting Started**: [CNB Viewer Development Guide](../04-tools-modding/cnb-viewer-development.md)

#### 🟠 **HIGH: PKB Tools Recreation**
**Skill Required**: C++, Archive Formats, Python  
**Impact**: Enable asset extraction for all game content  
**Status**: Research phase  
**Getting Started**: [PKB Archives Documentation](../03-technical-docs/file-formats/pkb-archives.md)

#### 🟡 **MEDIUM: Combat System Implementation**
**Skill Required**: C#, Game Logic, Database Design  
**Impact**: Core gameplay functionality  
**Status**: Research and planning  
**Getting Started**: [Combat Implementation Guide](../03-technical/combat-implementation-guide.md)

### **Development Setup**

#### Prerequisites
```bash
# For Windows development
- Visual Studio 2019+ (C#/.NET development)
- MySQL Server 8.0+
- Git for version control

# For cross-platform development  
- .NET Core SDK
- MySQL or PostgreSQL
- Docker (optional)
```

#### Repository Structure (Planned)
```
eden-reborn/
├── server/           # Main server code (C#)
├── tools/           # CNB viewer, PKB tools
├── database/        # Schema and migrations
├── client-patches/  # Game client modifications
├── documentation/   # This wiki content
└── testing/         # Automated tests
```

### **Coding Standards**

#### C# Server Development
- **Framework**: .NET Core 6+
- **Database**: Entity Framework Core
- **Logging**: Serilog
- **Testing**: xUnit
- **Style**: Microsoft coding conventions

#### C++ Tool Development
- **Standard**: C++17 minimum
- **Build**: CMake
- **Libraries**: OpenGL, GLFW, Dear ImGui (for CNB viewer)
- **Style**: Google C++ Style Guide

### **First Contributions**

#### Easy Tasks (Good First Issues)
1. **Documentation**: Update setup guides with screenshots
2. **Testing**: Validate existing server setup instructions
3. **Research**: Analyze game files and document findings
4. **Community**: Improve Discord bot or wiki organization

#### Medium Tasks
1. **Database**: Design schema improvements
2. **Tools**: Add features to existing utilities
3. **Client**: Create connection testing tools
4. **Performance**: Profile and optimize existing code

#### Advanced Tasks
1. **CNB Viewer**: Complete implementation from scratch
2. **Combat System**: Implement D100 mechanics
3. **World Server**: Design scalable architecture
4. **Cross-Platform**: Linux/macOS compatibility

## 📚 For Documentation

### **Current Needs**

#### 🔴 **CRITICAL: Source Documentation**
- **Task**: Create source files for 50+ wiki pages
- **Skills**: Research, fact-checking, citation
- **Impact**: Wiki credibility and accuracy
- **Getting Started**: [Source Documentation System](../sources/README.md)

#### 🟠 **HIGH: Tool Tutorials**
- **Task**: Step-by-step guides for all tools
- **Skills**: Technical writing, screenshots/videos
- **Impact**: Lower barrier to entry for new contributors
- **Examples**: CNB viewer usage, server setup walkthroughs

#### 🟡 **MEDIUM: Story Preservation**
- **Task**: Document missions, events, and lore
- **Skills**: Game knowledge, content organization
- **Impact**: Preserve Matrix Online's narrative legacy
- **Getting Started**: [Story Preservation Guide](../05-game-content/story-preservation-guide.md)

### **Documentation Standards**

#### Wiki Contributions
- **Format**: Markdown with GitHub flavored extensions
- **Style**: Conversational but technical
- **Structure**: Clear headers, bullet points, code blocks
- **Links**: Always verify internal links work
- **Images**: Optimize for web, use descriptive alt text

#### Source Attribution
```markdown
## Sources
- **Discord**: [quote with date/user] 
- **Forum**: [thread link/archive]
- **Code**: [file path and line]
- **Documentation**: [official source]
```

### **Getting Started with Documentation**

#### 1. **Pick a Page**
- Choose from [pages needing sources](../sources/index.md)
- Or improve existing documentation with missing details

#### 2. **Research Phase**
- Check Discord export for relevant conversations
- Search forum archives for technical discussions  
- Examine code repositories for implementation details
- Validate claims against multiple sources

#### 3. **Write and Verify**
- Add source documentation file
- Update main page with proper citations
- Verify all links work
- Test instructions on fresh system

## 🧪 For Testing

### **Testing Opportunities**

#### 🔴 **URGENT: Server Setup Validation**
- **Task**: Follow setup guides on different systems
- **Skills**: Basic command line, attention to detail
- **Impact**: Ensure documentation accuracy
- **Systems**: Windows 10/11, various Linux distributions

#### 🟠 **HIGH: Tool Functionality**
- **Task**: Test existing tools and report issues
- **Skills**: File management, basic troubleshooting
- **Impact**: Identify bugs and usability problems
- **Tools**: Available tools catalog, server components

#### 🟡 **MEDIUM: Performance Testing**
- **Task**: Stress test servers with multiple connections
- **Skills**: Network testing, performance monitoring
- **Impact**: Validate scalability and stability
- **Tools**: Server monitoring, load testing scripts

### **Testing Workflow**

#### 1. **Environment Setup**
```bash
# Create test environment
- Virtual machine or dedicated system
- Clean OS installation
- Document all steps taken
- Note any issues encountered
```

#### 2. **Test Execution**
- Follow documentation exactly as written
- Document every command and result
- Screenshot important steps
- Note timing and performance

#### 3. **Issue Reporting**
```markdown
## Bug Report
**System**: Windows 11, 16GB RAM
**Step**: Database setup (Step 4)
**Expected**: MySQL service starts automatically
**Actual**: Service fails with error code 1067
**Solution**: Added firewall exception
**Documentation Update**: Added firewall note to Step 3
```

## 🤝 For Community

### **Community Building Tasks**

#### 🔴 **URGENT: Discord Moderation**
- **Skills**: Community management, patience
- **Commitment**: 2-5 hours/week
- **Responsibilities**: Help new users, moderate discussions

#### 🟠 **HIGH: Content Creation**
- **Skills**: Video editing, streaming, writing
- **Impact**: Attract new contributors
- **Types**: YouTube tutorials, Twitch streams, blog posts

#### 🟡 **MEDIUM: Outreach**
- **Skills**: Social media, networking
- **Impact**: Grow community size
- **Platforms**: Reddit, Matrix Online forums, gaming communities

### **Community Guidelines**

#### Code of Conduct
- **Respectful**: No harassment, discrimination, or toxicity
- **Helpful**: Assist newcomers and share knowledge
- **Constructive**: Provide feedback that improves the project
- **Open**: Welcome all skill levels and backgrounds

#### Communication Standards
- **Discord**: Real-time chat, voice coordination
- **GitHub**: Technical discussions, issue tracking
- **Wiki**: Structured documentation, guides
- **Forums**: Long-form discussions, community building

## 🎖️ Recognition System

### **Contributor Levels**

#### 🥉 **Contributor**
- Made first meaningful contribution
- Helped others in community
- Active in Discord discussions

#### 🥈 **Regular Contributor**  
- Multiple significant contributions
- Mentors new contributors
- Maintains area of expertise

#### 🥇 **Core Contributor**
- Major feature implementation
- Leadership in community decisions
- Recognized expertise in specialized area

#### 💎 **Project Maintainer**
- Long-term project stewardship
- Final decision authority in specialty
- Represents project to broader community

### **Recognition Benefits**
- **Discord**: Special roles and channel access
- **Wiki**: Contributor page listing
- **GitHub**: Repository access and permissions
- **Community**: Speaking opportunities, leadership roles

## 📅 Getting Started

### **This Week**
1. **Join Discord**: [Eden Reborn Server](https://discord.gg/3QXTAGB9)
2. **Read Documentation**: Familiarize yourself with the project
3. **Pick a Task**: Choose from critical needs above
4. **Ask Questions**: Don't hesitate to reach out for help

### **This Month**
1. **Make First Contribution**: Complete a small task successfully
2. **Find Your Niche**: Discover where your skills fit best
3. **Build Relationships**: Connect with other contributors
4. **Set Goals**: Plan your long-term involvement

### **This Year**
1. **Major Contribution**: Lead a significant feature or improvement
2. **Mentor Others**: Help new contributors get started
3. **Expand Skills**: Learn new technologies as needed
4. **Shape Direction**: Influence project priorities and decisions

## 🆘 Getting Help

### **When You're Stuck**
- **Discord #help**: General questions and troubleshooting
- **Discord #dev**: Technical development questions
- **Discord #docs**: Documentation and writing questions
- **GitHub Issues**: Bug reports and feature requests

### **Resources**
- **[Tool Development Guide](../04-tools-modding/tool-development-guide.md)** - Technical implementation
- **[Contribution Framework](contribution-framework.md)** - Detailed guidelines
- **[FAQ](../02-server-setup/faq.md)** - Common questions answered
- **[Discord](https://discord.gg/3QXTAGB9)** - Real-time community support

## 🌟 The Impact

Your contributions to Eden Reborn help:
- **Preserve gaming history** for future generations
- **Empower the community** to control their own gaming experience  
- **Advance open source gaming** as a viable alternative to corporate control
- **Reunite players** with a beloved game world
- **Demonstrate** that community passion can overcome corporate abandonment

## 💫 Join the Resistance

> *"This is your last chance. After this, there is no going back. You take the blue pill—the story ends, you wake up in your bed and believe whatever you want to believe. You take the red pill—you stay in Wonderland, and I show you how deep the rabbit hole goes."*

**You've chosen the red pill by reading this far.**

**Welcome to Eden Reborn. Welcome to the resistance.**

---

[Join Discord →](https://discord.gg/3QXTAGB9) | [Read Framework →](contribution-framework.md) | [Start Contributing →](../04-tools-modding/tool-development-guide.md)