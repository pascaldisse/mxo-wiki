# MXOEmu Server Setup Guide

## Overview

MXOEmu is the original Matrix Online server emulator created by rajkosto. It's the most mature server implementation with the longest development history, starting in 2005. This guide will walk you through setting up your own MXOEmu server.

**Current Status**: Development appears inactive (last updates ~2019), but the server remains functional for basic gameplay.

## Prerequisites

### Hardware Requirements
- **Minimum**: 2GB RAM, Dual-core CPU, 10GB storage
- **Recommended**: 4GB RAM, Quad-core CPU, 20GB SSD storage
- **Network**: Static IP or Dynamic DNS service
- **Bandwidth**: 10Mbps+ upload for multiple players

### Software Requirements
- **Operating System**: Windows 7/8/10/11 or Windows Server
- **Database**: MySQL 5.x or MariaDB
- **Runtime**: Visual C++ 2010 SP1 Redistributable
- **.NET Framework**: 4.0 or higher
- **Development** (optional): Visual Studio 2010 or later

## Step 1: Download MXOEmu

### Option A: Pre-compiled Binaries
1. Check [MXOEmu Releases](https://github.com/rajkosto/mxoemu/releases)
2. Download the latest release package
3. Extract to a folder like `C:\MXOEmu`

### Option B: Build from Source
```bash
# Clone the repository
git clone https://github.com/rajkosto/mxoemu.git
cd mxoemu

# Open Reality.sln in Visual Studio
# Build in Release mode
```

## Step 2: Database Setup

### Install MySQL/MariaDB

1. Download [MariaDB](https://mariadb.org/download/) or [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
2. Run installer with default settings
3. Set root password (remember this!)
4. Ensure MySQL service is running

### Create Database

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database and user
CREATE DATABASE mxoemu;
CREATE USER 'mxoemu'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON mxoemu.* TO 'mxoemu'@'localhost';
FLUSH PRIVILEGES;
```

### Import Schema

```bash
# Navigate to MXOEmu directory
cd C:\MXOEmu\Database

# Import the schema
mysql -u mxoemu -p mxoemu < schema.sql
mysql -u mxoemu -p mxoemu < data.sql
```

## Step 3: Server Configuration

### Edit Configuration Files

**1. Database Configuration** (`config/database.xml`):
```xml
<?xml version="1.0" encoding="utf-8"?>
<database>
    <host>localhost</host>
    <port>3306</port>
    <database>mxoemu</database>
    <username>mxoemu</username>
    <password>your_password_here</password>
</database>
```

**2. World Server Configuration** (`config/world.xml`):
```xml
<?xml version="1.0" encoding="utf-8"?>
<world>
    <name>My MXO Server</name>
    <port>10000</port>
    <maxplayers>100</maxplayers>
    <pvp>true</pvp>
    <hardline_timer>30</hardline_timer>
</world>
```

**3. Authentication Server** (`config/auth.xml`):
```xml
<?xml version="1.0" encoding="utf-8"?>
<auth>
    <port>11000</port>
    <allow_registration>true</allow_registration>
    <require_email_verification>false</require_email_verification>
</auth>
```

## Step 4: Network Configuration

### Port Forwarding

Forward these ports on your router:
- **10000** TCP/UDP - World Server
- **11000** TCP - Authentication Server
- **11001** TCP - Patch Server (optional)

### Firewall Rules

```powershell
# Windows Firewall rules (run as Administrator)
netsh advfirewall firewall add rule name="MXO World" dir=in action=allow protocol=TCP localport=10000
netsh advfirewall firewall add rule name="MXO Auth" dir=in action=allow protocol=TCP localport=11000
netsh advfirewall firewall add rule name="MXO World UDP" dir=in action=allow protocol=UDP localport=10000
```

## Step 5: Starting the Server

### Manual Start

1. Start MySQL service (if not running)
2. Run Authentication Server:
   ```
   C:\MXOEmu\AuthServer.exe
   ```
3. Run World Server:
   ```
   C:\MXOEmu\WorldServer.exe
   ```

### Create Batch File

Create `start_server.bat`:
```batch
@echo off
echo Starting MXOEmu Server...
start "Auth Server" /D "C:\MXOEmu" AuthServer.exe
timeout /t 5
start "World Server" /D "C:\MXOEmu" WorldServer.exe
echo Server started!
pause
```

## Step 6: Creating Admin Account

### Using Console Commands

1. With servers running, in the Auth Server console:
```
create_account username password email@example.com
set_admin username 1
```

### Direct Database Method

```sql
-- Insert admin account directly
INSERT INTO accounts (username, password, email, admin_level) 
VALUES ('admin', MD5('your_password'), 'admin@example.com', 9);
```

## Step 7: Client Configuration

Players need to patch their clients to connect to your server:

1. Edit `launcher.exe` and `matrix.exe` to point to your server IP
2. Or provide a pre-patched launcher with your server address
3. See [Client Patching Guide](client-patches.md) for details

## Troubleshooting

### Common Issues

**Server won't start**
- Check all ports are free: `netstat -an | find "10000"`
- Verify MySQL is running: `sc query mysql`
- Check logs in `logs/` directory

**Database connection failed**
- Verify MySQL credentials
- Check MySQL is listening on localhost
- Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`

**Players can't connect**
- Verify port forwarding with: https://www.yougetsignal.com/tools/open-ports/
- Check Windows Firewall isn't blocking
- Ensure client is properly patched

### Log Files

Check these logs for issues:
- `logs/authserver.log` - Authentication issues
- `logs/worldserver.log` - Game server problems
- `logs/mysql_errors.log` - Database problems

## Advanced Configuration

### Performance Tuning

**MySQL Optimization** (`my.ini`):
```ini
[mysqld]
innodb_buffer_pool_size = 512M
innodb_log_file_size = 64M
max_connections = 100
query_cache_size = 64M
```

**Server Threading** (`config/performance.xml`):
```xml
<performance>
    <worker_threads>4</worker_threads>
    <io_threads>2</io_threads>
    <max_packet_size>65536</max_packet_size>
</performance>
```

### Features Configuration

**Enable/Disable Systems** (`config/features.xml`):
```xml
<features>
    <combat>false</combat>  <!-- Combat not fully implemented -->
    <missions>true</missions>
    <email>false</email>
    <auction>false</auction>
    <crews>true</crews>
</features>
```

## Maintenance

### Regular Tasks

1. **Daily**: Check server logs for errors
2. **Weekly**: Backup database
3. **Monthly**: Clear old logs, update server

### Backup Script

Create `backup.bat`:
```batch
@echo off
set BACKUP_DIR=C:\MXOEmu\backups
set DATE=%date:~-4,4%%date:~-10,2%%date:~-7,2%
mysqldump -u mxoemu -p mxoemu > "%BACKUP_DIR%\mxoemu_%DATE%.sql"
echo Backup complete: mxoemu_%DATE%.sql
```

## Known Limitations

- Combat system not fully implemented
- Many missions non-functional
- No email/auction house
- Limited NPC interactions
- Some areas may crash clients

## Next Steps

- [Configure GM Commands](gm-commands.md)
- [Add Custom Content](custom-content.md)
- [Connect Test Client](../01-getting-started/server-connection.md)
- [Compare with Hardline Dreams](hardline-dreams-setup.md)

---

**Need Help?** Join the [Discord](https://discord.gg/3QXTAGB9) or check the [Troubleshooting Guide](troubleshooting.md).

[← Back to Server Setup](index.md) | [Next: Hardline Dreams Setup →](hardline-dreams-setup.md)