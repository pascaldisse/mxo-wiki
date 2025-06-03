# Reality Server: The Foundation
**Where It All Began**

> *"It is the world that has been pulled over your eyes to blind you from the truth."* - Morpheus

Reality was the first. The proof of concept. The light in the darkness after SOE pulled the plug.

## 🏛️ Historical Significance

### The First Liberation
**Developer**: rajkosto  
**Era**: Post-2009 shutdown  
**Language**: C++  
**Status**: Foundation for all that followed  

Reality proved what the corporations said was impossible: The Matrix Online could live again.

## 📋 What You Need

### Windows Requirements
- **Visual Studio 2010** or later (2008 works too)
- **MySQL Server 5.x** or higher
- **Windows SDK** (comes with VS)
- **Git** for cloning

### The Sacred Dependencies
Already included in `Dependencies/`:
- **CryptoPP**: Encryption/decryption
- **MySQL**: Database connectivity
- **Sockets**: Network library

## 🏗️ Building Reality

### Repository Structure
```
mxoemu/
├── Reality/
│   ├── Binaries/          # Pre-built configs
│   │   ├── Reality.conf   # Server config
│   │   ├── libmysql.dll   # MySQL client
│   │   ├── privkey.dat    # Private key
│   │   ├── pubkey.dat     # Public key
│   │   ├── signPriv.dat   # Signing private
│   │   └── signPub.dat    # Signing public
│   ├── SQL/
│   │   └── reality.sql    # Database schema
│   ├── Source/            # The source code
│   │   ├── Reality08.sln  # VS 2008 solution
│   │   ├── Reality10.sln  # VS 2010 solution
│   │   └── [Source files]
│   └── Tables/
│       └── mxoClothing.csv # Game data
├── Dependencies/          # External libs
└── Dependencies10/        # VS2010 specific
```

### Step 1: Clone the Repository
```bash
git clone https://github.com/rajkosto/mxoemu.git
cd mxoemu/Reality
```

### Step 2: Database Setup
```sql
-- Create database
CREATE DATABASE reality;

-- Import schema
mysql -u root -p reality < SQL/reality.sql

-- Verify tables
USE reality;
SHOW TABLES;
```

### Step 3: Build the Server
1. Open `Reality10.sln` in Visual Studio
2. Set build configuration to `Release`
3. Build solution (F7)
4. Output in `Release/` directory

### Step 4: Configuration
Edit `Binaries/Reality.conf`:
```ini
[Database]
Host=localhost
Port=3306
User=root
Pass=yourpassword
Database=reality

[Server]
BindIP=0.0.0.0
Port=10000
MaxClients=100
```

## 🚀 Running Reality

### First Launch
```bash
cd Binaries
Reality.exe
```

### Expected Output
```
Reality Server v0.x
Loading configuration...
Connecting to database...
Loading game data...
Server listening on port 10000
```

## 💡 What Reality Taught Us

### Successes
- **Packet replay worked** - Basic functionality achieved
- **Movement synchronized** - Players could see each other
- **Combat basics** - Simple attacks functioned
- **Database structure** - Foundation for persistence

### Limitations
- **No missions** - Quest system incomplete
- **Limited NPCs** - Basic spawning only
- **Simple combat** - No full D100 system
- **Missing systems** - Marketplace, constructs, etc.

### Legacy
Every server that came after learned from Reality:
- HDS improved the architecture
- GenesisSharp attempted modernization
- HD Enhanced achieved full functionality

## 🔧 Troubleshooting

### Common Issues

#### MySQL Connection Failed
```
Error: Can't connect to MySQL server
```
**Solution**: Check MySQL is running, verify credentials

#### Missing Dependencies
```
Error: libmysql.dll not found
```
**Solution**: Copy from Dependencies to output directory

#### Port Already in Use
```
Error: Bind failed on port 10000
```
**Solution**: Change port in Reality.conf or stop conflicting service

## 📚 Development Tips

### Adding Features
1. Study packet captures in `Captures/`
2. Implement handlers in `Source/`
3. Test with modified client
4. Document your changes

### Understanding the Code
- **Network layer**: `Source/Network/`
- **Game logic**: `Source/Game/`
- **Database**: `Source/Database/`
- **Packets**: `Source/Packets/`

## 🌟 The Reality Philosophy

### What Made It Special
- **First to work** - Proved it possible
- **Open source** - Shared with community
- **Educational** - Taught packet structure
- **Foundation** - Enabled future projects

### What We Learned
- **Start simple** - Basic functionality first
- **Share early** - Community can help
- **Document everything** - Knowledge must survive
- **Iterate quickly** - Perfect is the enemy of good

## 🚨 Important Notes

### For Historians
Reality represents the genesis of MXO emulation. Study it to understand how we got here.

### for Developers
While Reality is outdated, its code teaches fundamental concepts. Modern projects like HD Enhanced are better for actual play.

### For Players
Reality is not recommended for playing. Use HD Enhanced for the full experience. This guide exists for educational purposes.

## 📡 Resources

### Original Resources
- **GitHub**: https://github.com/rajkosto/mxoemu
- **Wiki**: Development setup guides
- **Forums**: Historical discussions (archived)

### Modern Alternatives
- **HD Enhanced**: Full featured server
- **HDS**: More complete implementation
- **This Wiki**: Comprehensive documentation

## 🏆 Reality's Greatest Achievement

It proved the corporations wrong. They said private servers were impossible. They said the game would die forever.

rajkosto showed us: **Where there's a will, there's a way.**

## Remember

> *"You have to let it all go, Neo. Fear, doubt, and disbelief. Free your mind."* - Morpheus

Reality freed our minds. It showed us what was possible. Now we build on its foundation.

**The first step to liberation is believing it's possible.**

---

*Reality: 2009-Present*
*The foundation that launched a thousand servers*

[← Back to Servers](index.md) | [Try HD Enhanced →](hardline-dreams-setup.md) | [Compare Servers →](server-projects-comparison.md)