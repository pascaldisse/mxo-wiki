# Server Setup Documentation

> ### 🚧 **Current Status: Development in Progress**
> **[Eden Reborn Project →](eden-reborn-success.md)**  
> *Started June 3, 2025: Community-driven MXO server development project. Currently in early research and planning phase.*

Welcome to the Matrix Online server setup section. Here you'll find everything needed to run your own MXO server, from basic installation to advanced administration.

## 🎯 Choose Your Server

### [MXOEmu](mxoemu-setup.md)
The original and most mature server emulator by rajkosto.

**Pros:**
- Longest development history (since 2005)
- Most documented
- Stable for basic features
- Large codebase

**Cons:**
- Development appears stalled
- Combat not implemented
- Some features incomplete
- Older architecture

**Best for:** Those wanting the "classic" experience or studying the original implementation.

### [Hardline Dreams](hardline-dreams-setup.md)
Alternative implementation by pahefu and neowhoru with active development.

**Pros:**
- Active development
- Modern C# codebase
- Better vendor system
- Cleaner architecture

**Cons:**
- Less mature
- Fewer players tested
- Documentation in progress
- Some instability

**Best for:** Developers wanting to contribute or those seeking latest features.

## 📋 Setup Process Overview

### 1. Prerequisites Check
- [ ] Hardware meets requirements
- [ ] Windows OS installed
- [ ] Network ports available
- [ ] Admin access confirmed

### 2. Server Installation
- [ ] Choose server type (MXOEmu or HD)
- [ ] Download/build server files
- [ ] Install dependencies
- [ ] Configure database

### 3. Network Configuration  
- [ ] Configure router port forwarding
- [ ] Set up firewall rules
- [ ] Obtain static IP or dynamic DNS
- [ ] Test external connectivity

### 4. Client Preparation
- [ ] Patch game clients
- [ ] Create test accounts
- [ ] Verify connections
- [ ] Distribute to players

### 5. Administration
- [ ] Set up admin tools
- [ ] Configure backups
- [ ] Monitor performance
- [ ] Plan events

## 🛠️ Essential Guides

### Setup & Installation
- [MXOEmu Complete Setup](mxoemu-setup.md)
- [Hardline Dreams Setup](hardline-dreams-setup.md)
- [Database Configuration](database-setup.md)
- [Network Setup](network-setup.md)

### Client Configuration
- [Client Patching Guide](client-patches.md)
- [Server Setup Comparison](server-projects-comparison.md)
- [Troubleshooting Guide](troubleshooting.md)

### Administration
- [Advanced Administration](advanced-admin.md)
- [GM Commands & Administration](gm-commands-administration.md)
- [Server Troubleshooting](server-troubleshooting.md)
- [Database Management](database-setup.md)

### Advanced Topics
- [Technical Documentation](../03-technical/index.md)
- [File Formats Reference](../03-technical/file-formats/index.md)
- [Combat Implementation](../06-gameplay-systems/combat/index.md)
- [Tool Development](../04-tools-modding/tool-development-guide.md)

## 💻 System Requirements

### Minimum (1-10 players)
- **CPU**: Dual-core 2GHz+
- **RAM**: 2GB
- **Storage**: 10GB HDD
- **Network**: 10Mbps upload
- **OS**: Windows 7+

### Recommended (10-50 players)
- **CPU**: Quad-core 3GHz+
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **Network**: 25Mbps upload
- **OS**: Windows 10/Server 2019

### Production (50+ players)
- **CPU**: 6+ cores
- **RAM**: 8GB+
- **Storage**: 50GB SSD
- **Network**: 100Mbps dedicated
- **OS**: Windows Server 2019+

## 🔧 Quick Commands

### Check Server Status
```batch
netstat -an | findstr "10000"
tasklist | findstr "Auth"
```

### Start Servers
```batch
cd C:\MXOServer
start AuthServer.exe
start WorldServer.exe
```

### Backup Database
```batch
mysqldump -u root -p mxodb > backup_%date%.sql
```

## ⚠️ Important Considerations

### Legal
- Server emulation for preservation/education
- Require legitimate client ownership
- No commercial operation
- Respect intellectual property

### Technical
- Combat system not implemented
- Many features incomplete
- Expect bugs and crashes
- Limited player capacity

### Community
- Small but dedicated playerbase
- Help others when possible
- Share knowledge and discoveries
- Report bugs constructively

## 🚦 Server Status Comparison

| Feature | MXOEmu | Hardline Dreams |
|---------|---------|-----------------|
| **Core Systems** |
| Login/Auth | ✅ Stable | ✅ Stable |
| Character Creation | ✅ Working | ✅ Working |
| World Navigation | ✅ Working | ✅ Working |
| Chat System | ✅ Working | ✅ Working |
| **Gameplay** |
| Combat | ❌ Not Implemented | ❌ Not Implemented |
| Missions | ⚠️ Partial | ⚠️ Partial |
| Abilities | ⚠️ Limited | ⚠️ Limited |
| Crafting | ❌ Missing | ⚠️ Partial |
| **Economy** |
| Vendors | ⚠️ Basic | ✅ Full |
| Trading | ⚠️ Basic | ⚠️ Basic |
| Auction | ❌ Missing | ❌ Missing |
| **Social** |
| Crews | ⚠️ Basic | ⚠️ Basic |
| Email | ❌ Missing | ❌ Missing |
| Events | Manual Only | Manual Only |

## 📚 Additional Resources

### Documentation
- [File Format Reference](../03-technical/file-formats/index.md)
- [Server Architecture](../03-technical/server-architecture.md)
- [Technical Overview](../03-technical/index.md)

### Tools
- [Available Tools Catalog](../04-tools-modding/available-tools-catalog.md)
- [Tool Development Guide](../04-tools-modding/tool-development-guide.md)
- [Lost Tools Archive](../04-tools-modding/lost-tools-archive.md)

### Support
- [FAQ](faq.md)
- [Troubleshooting Guide](troubleshooting.md)
- [Community Resources](../08-community/index.md)
- [Discord](https://discord.gg/3QXTAGB9)

## 🎯 Next Steps

1. **Choose your server type** - Compare features and pick what fits your needs
2. **Follow setup guide** - Step-by-step instructions for your chosen server
3. **Configure networking** - Ensure players can connect
4. **Test thoroughly** - Verify all components work
5. **Launch and maintain** - Keep your server running smoothly

---

*Running a Matrix Online server is a labor of love. Be patient, be persistent, and welcome to the community of server operators keeping MXO alive!*

[← Back to Wiki Home](../index.md) | [Next: MXOEmu Setup →](mxoemu-setup.md)