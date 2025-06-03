# Hardline Dreams (MXO-HD) Server Setup Guide

## Overview

Hardline Dreams (HD) is an alternative Matrix Online server implementation developed by pahefu (HD_Neo) and neowhoru. It offers a different approach from MXOEmu with some unique features and a different codebase structure.

**Repository**: https://github.com/hdneo/mxo-hd

**Key Differences from MXOEmu**:
- Written in C# (.NET)
- Different packet handling approach
- Includes vendor data parsing
- More modular architecture
- Active development (as of 2023)

## Prerequisites

### Hardware Requirements
- **Minimum**: 2GB RAM, Dual-core CPU, 10GB storage
- **Recommended**: 4GB RAM, Quad-core CPU, 20GB SSD storage
- **Network**: Static IP or Dynamic DNS service

### Software Requirements
- **Operating System**: Windows 7/8/10/11
- **Framework**: .NET Framework 4.5 or higher
- **Database**: MySQL 5.x or MariaDB
- **IDE** (for development): Visual Studio 2017 or later

## Step 1: Getting Hardline Dreams

### Option A: Download Pre-built
```bash
# Clone the repository
git clone https://github.com/hdneo/mxo-hd.git
cd mxo-hd

# Check for pre-built binaries in:
# hds/bin/Debug/
# hds/bin/Release/
```

### Option B: Build from Source
1. Open `mxo-hd.sln` in Visual Studio
2. Restore NuGet packages
3. Build solution in Release mode
4. Output will be in `hds/bin/Release/`

## Step 2: Database Setup

### Create Database

```sql
-- Connect to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE mxo_hd;
CREATE USER 'mxohd'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON mxo_hd.* TO 'mxohd'@'localhost';
FLUSH PRIVILEGES;
```

### Import Schema

```bash
# From the mxo-hd directory
cd database
mysql -u mxohd -p mxo_hd < schema.sql
mysql -u mxohd -p mxo_hd < initial_data.sql
```

## Step 3: Configuration

### Main Configuration File

Edit `Config.xml` in the HD server directory:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Configuration>
    <Database>
        <Host>localhost</Host>
        <Port>3306</Port>
        <Database>mxo_hd</Database>
        <Username>mxohd</Username>
        <Password>your_password</Password>
    </Database>
    
    <Server>
        <Name>Hardline Dreams Server</Name>
        <IP>0.0.0.0</IP>
        <AuthPort>11000</AuthPort>
        <WorldPort>10000</WorldPort>
        <MaxPlayers>100</MaxPlayers>
    </Server>
    
    <Features>
        <AllowRegistration>true</AllowRegistration>
        <StartLevel>1</StartLevel>
        <StartMoney>1000</StartMoney>
    </Features>
</Configuration>
```

### Data Files Configuration

HD uses CSV data files located in `hds/bin/Debug/data/`:

- `vendor_items.csv` - Vendor inventory data
- `npc_spawns.csv` - NPC spawn locations
- `item_templates.csv` - Item definitions
- `mission_data.csv` - Mission information

## Step 4: Network Setup

### Port Configuration

Same as MXOEmu, forward these ports:
- **10000** TCP/UDP - World Server
- **11000** TCP - Authentication Server

### Windows Firewall

```powershell
# Add firewall rules (run as Administrator)
New-NetFirewallRule -DisplayName "HD World Server" -Direction Inbound -LocalPort 10000 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "HD Auth Server" -Direction Inbound -LocalPort 11000 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "HD World UDP" -Direction Inbound -LocalPort 10000 -Protocol UDP -Action Allow
```

## Step 5: Launching the Server

### Using HDS.exe Launcher

1. Navigate to HD server directory
2. Run `HDS.exe` (Hardline Dreams Server launcher)
3. Click "Start Server" button
4. Monitor the console output

### Manual Launch

```batch
# Start servers individually
cd C:\mxo-hd\hds\bin\Release
start AuthServer.exe
timeout /t 5
start WorldServer.exe
```

### Service Mode (Advanced)

Create Windows service for automatic startup:

```batch
# Install as service
sc create "HD Auth Server" binPath= "C:\mxo-hd\hds\bin\Release\AuthServer.exe"
sc create "HD World Server" binPath= "C:\mxo-hd\hds\bin\Release\WorldServer.exe"

# Set to auto-start
sc config "HD Auth Server" start= auto
sc config "HD World Server" start= auto
```

## Step 6: Initial Setup

### Create Admin Account

Using the HD console:
```
> account create admin password123 admin@example.com
> account setlevel admin 9
> account list
```

### Import Game Data

HD includes tools for importing game data:

```batch
# Import vendor data
DataImporter.exe vendors vendor_items.csv

# Import NPCs
DataImporter.exe npcs npc_spawns.csv
```

## Step 7: Client Connection

### Automatic Patcher

HD includes a client patcher:
```batch
# Run from HD tools directory
HDClientPatcher.exe "C:\Matrix Online\Client" your.server.ip
```

### Manual Configuration

See [Client Patching Guide](client-patches.md) for manual patching instructions.

## Features Comparison

| Feature | MXOEmu | Hardline Dreams |
|---------|---------|-----------------|
| Basic Movement | ✅ | ✅ |
| Chat System | ✅ | ✅ |
| Vendors | ⚠️ | ✅ |
| Missions | ⚠️ | ⚠️ |
| Combat | ❌ | ❌ |
| Abilities | ⚠️ | ⚠️ |
| Crafting | ❌ | ⚠️ |
| Email System | ❌ | ❌ |

## Troubleshooting

### Common Issues

**HDS.exe won't start**
- Check .NET Framework version: `reg query "HKLM\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full" /v Release`
- Run as Administrator
- Check for missing DLLs with Dependency Walker

**Database connection errors**
- Verify MySQL service is running
- Check credentials in Config.xml
- Test connection: `mysql -h localhost -u mxohd -p`

**Client connection timeouts**
- Verify server is listening: `netstat -an | findstr "10000"`
- Check client patch was successful
- Disable Windows Defender temporarily for testing

### Log Files

HD creates detailed logs in `logs/` directory:
- `auth_server.log` - Authentication events
- `world_server.log` - Game server events  
- `database.log` - Database queries
- `packets.log` - Network packet dumps (if enabled)

## Advanced Configuration

### Performance Tuning

Edit `Performance.config`:
```xml
<Performance>
    <ThreadPool>
        <MinWorkerThreads>4</MinWorkerThreads>
        <MaxWorkerThreads>100</MaxWorkerThreads>
    </ThreadPool>
    <Network>
        <SendBufferSize>8192</SendBufferSize>
        <ReceiveBufferSize>8192</ReceiveBufferSize>
    </Network>
</Performance>
```

### Custom Content

HD supports custom content through CSV files:

**Adding Items** (`data/custom_items.csv`):
```csv
id,name,type,icon,model,stats
9001,"Custom Shirt",clothing,shirt_icon,shirt_model,"defense:10,style:5"
```

**Adding NPCs** (`data/custom_npcs.csv`):
```csv
id,name,model,location,dialogue
5001,"Custom NPC",npc_model_01,"100.5,0,200.5","Welcome to the Matrix!"
```

## Development Features

### Debug Mode

Enable debug mode in `Config.xml`:
```xml
<Debug>
    <Enabled>true</Enabled>
    <PacketLogging>true</PacketLogging>
    <VerboseLogging>true</VerboseLogging>
    <SavePacketDumps>true</SavePacketDumps>
</Debug>
```

### GM Commands

HD includes GM commands:
- `/spawn [npc_id]` - Spawn NPC
- `/give [item_id] [quantity]` - Give items
- `/teleport [x] [y] [z]` - Teleport
- `/setlevel [level]` - Set character level

## Backup and Maintenance

### Automated Backup

Create `backup_hd.bat`:
```batch
@echo off
set BACKUP_PATH=C:\mxo-hd\backups
set TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%

mkdir "%BACKUP_PATH%\%TIMESTAMP%"
xcopy /E /I "data" "%BACKUP_PATH%\%TIMESTAMP%\data"
mysqldump -u mxohd -p mxo_hd > "%BACKUP_PATH%\%TIMESTAMP%\database.sql"

echo Backup completed: %TIMESTAMP%
```

## Known Issues

- Combat system incomplete
- Some missions may crash
- Ability system partially implemented
- Memory leaks with 50+ players
- Some areas have missing NPCs

## Resources

- [HD GitHub Repository](https://github.com/hdneo/mxo-hd)
- [HD Development Wiki](https://github.com/hdneo/mxo-hd/wiki)
- [Community Discord](../08-community/discord.md)

---

[← Back to Server Setup](index.md) | [Next: Client Patching →](client-patches.md)