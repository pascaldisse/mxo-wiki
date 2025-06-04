# Database Liberation Guide
**Free Your Data From Corporate Control**

> *"The Matrix is everywhere. It is all around us."* - Morpheus

Your database is the heart of your liberated Matrix. Here we teach you to master it, optimize it, and keep it free.

## 🌐 Overview

All MXO servers use MySQL/MariaDB to persist the digital paradise. This guide covers everything from installation to advanced optimization. Unlike the Old Guard who kept database knowledge secret, we share everything.

## 💾 Database Requirements

### Storage Liberation
- **Empty Matrix**: ~50MB (seed of paradise)
- **100 Awakened**: ~500MB (small community)
- **1000 Awakened**: ~5GB (thriving resistance)
- **Backup Reality**: 2-3x active size (always prepare)

### Performance Needs
- **RAM**: 512MB minimum, 2GB for smooth operations
- **CPU**: Light load (the Matrix is efficient)
- **Disk**: SSD strongly recommended (speed matters)

**Remember**: These are just numbers. Even a Raspberry Pi can host paradise.

## 🔧 Installing Your Database Engine

### Option A: MariaDB (The Liberated Choice)

MariaDB is MySQL's free sibling - open source, community-driven, corporate-free. This is the Neoologist way.

**Windows Installation:**
1. Download from https://mariadb.org/download/
2. Run installer, choose:
   - Install as service
   - Enable networking
   - Set root password
   - UTF8MB4 character set

**Linux Installation:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mariadb-server mariadb-client
sudo mysql_secure_installation

# CentOS/RHEL
sudo yum install mariadb-server mariadb
sudo systemctl start mariadb
sudo mysql_secure_installation
```

### Option B: MySQL Community Server

1. Download from https://dev.mysql.com/downloads/mysql/
2. Choose "Server only" installation
3. Configure as standalone server
4. Set strong root password

## Initial Configuration

### Secure Installation

Run secure installation script:
```bash
mysql_secure_installation

# Answer prompts:
# Set root password? [Y/n] Y
# Remove anonymous users? [Y/n] Y  
# Disallow root login remotely? [Y/n] Y
# Remove test database? [Y/n] Y
# Reload privilege tables? [Y/n] Y
```

### Configure MySQL/MariaDB

Edit configuration file:

**Windows**: `C:\ProgramData\MySQL\MySQL Server X.X\my.ini`  
**Linux**: `/etc/mysql/my.cnf` or `/etc/my.cnf`

```ini
[mysqld]
# Basic Settings
port = 3306
bind-address = 127.0.0.1  # Only local connections
max_connections = 100
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# InnoDB Settings
innodb_buffer_pool_size = 512M  # 50-70% of RAM
innodb_log_file_size = 64M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT

# Query Cache (MySQL 5.7 and below)
query_cache_type = 1
query_cache_size = 64M
query_cache_limit = 2M

# Logging
log_error = /var/log/mysql/error.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2

# Binary Logging (for replication/backup)
log_bin = /var/log/mysql/mysql-bin
expire_logs_days = 7
max_binlog_size = 100M
```

### Restart Service

```bash
# Windows
net stop mysql
net start mysql

# Linux
sudo systemctl restart mariadb
# or
sudo service mysql restart
```

## 🏗️ Creating Your Digital Paradise

### For MXOEmu (The Original)

```sql
-- Connect as root
mysql -u root -p

-- Create database
CREATE DATABASE mxoemu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'mxoemu'@'localhost' IDENTIFIED BY 'strong_password_here';
CREATE USER 'mxoemu'@'%' IDENTIFIED BY 'strong_password_here';  -- For remote access

-- Grant privileges
GRANT ALL PRIVILEGES ON mxoemu.* TO 'mxoemu'@'localhost';
GRANT ALL PRIVILEGES ON mxoemu.* TO 'mxoemu'@'%';
FLUSH PRIVILEGES;

-- Verify
SHOW GRANTS FOR 'mxoemu'@'localhost';
```

### For Hardline Dreams

```sql
-- Create database
CREATE DATABASE mxo_hd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'mxohd'@'localhost' IDENTIFIED BY 'strong_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON mxo_hd.* TO 'mxohd'@'localhost';
FLUSH PRIVILEGES;
```

## Importing Schema

### MXOEmu Schema

```bash
cd /path/to/mxoemu/database
mysql -u mxoemu -p mxoemu < schema.sql
mysql -u mxoemu -p mxoemu < procedures.sql
mysql -u mxoemu -p mxoemu < initial_data.sql
```

### Hardline Dreams Schema

```bash
cd /path/to/mxo-hd/database
mysql -u mxohd -p mxo_hd < create_tables.sql
mysql -u mxohd -p mxo_hd < default_data.sql
mysql -u mxohd -p mxo_hd < stored_procedures.sql
```

## Database Structure Overview

### Core Tables

**accounts**
```sql
CREATE TABLE accounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(32) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL,
    email VARCHAR(128),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    admin_level INT DEFAULT 0,
    banned BOOLEAN DEFAULT FALSE
);
```

**characters**
```sql
CREATE TABLE characters (
    id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    name VARCHAR(32) UNIQUE NOT NULL,
    level INT DEFAULT 1,
    experience BIGINT DEFAULT 0,
    district_id INT,
    x FLOAT, y FLOAT, z FLOAT,
    hp INT, max_hp INT,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);
```

**items**
```sql
CREATE TABLE items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    character_id INT,
    template_id INT,
    slot INT,
    quantity INT DEFAULT 1,
    FOREIGN KEY (character_id) REFERENCES characters(id)
);
```

### World Data Tables

- **districts** - Game world zones
- **npcs** - Non-player characters
- **vendors** - Shop inventories
- **missions** - Quest data
- **hardlines** - Teleport points

## 📊 Power User Queries

### Account Liberation

These queries give you god-like control over your Matrix:

```sql
-- Create new account
INSERT INTO accounts (username, password, email) 
VALUES ('newuser', MD5('password'), 'user@email.com');

-- Set admin level
UPDATE accounts SET admin_level = 9 WHERE username = 'admin';

-- Ban/unban account
UPDATE accounts SET banned = TRUE WHERE username = 'baduser';

-- Check account details
SELECT * FROM accounts WHERE username = 'player1';
```

### Character Queries

```sql
-- List all characters for account
SELECT c.* FROM characters c 
JOIN accounts a ON c.account_id = a.id 
WHERE a.username = 'player1';

-- Top players by level
SELECT name, level, experience 
FROM characters 
ORDER BY level DESC, experience DESC 
LIMIT 10;

-- Character location
SELECT name, district_id, x, y, z 
FROM characters 
WHERE name = 'Neo';

-- Character inventory
SELECT i.*, it.name, it.type 
FROM items i
JOIN item_templates it ON i.template_id = it.id
WHERE i.character_id = 123;
```

### Server Statistics

```sql
-- Total accounts
SELECT COUNT(*) as total_accounts FROM accounts;

-- Active players (last 30 days)
SELECT COUNT(*) as active_players 
FROM accounts 
WHERE last_login > DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Character distribution by level
SELECT level, COUNT(*) as count 
FROM characters 
GROUP BY level 
ORDER BY level;

-- Most popular districts
SELECT d.name, COUNT(c.id) as players 
FROM districts d
LEFT JOIN characters c ON d.id = c.district_id
GROUP BY d.id
ORDER BY players DESC;
```

## 🛡️ Protecting Paradise

### Manual Backup (Control Your Destiny)

Never trust a single point of failure. The Old Guard lost everything when their servers died. We backup obsessively:

```bash
#!/bin/bash
# backup_mxo.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/mxo"
DB_NAME="mxoemu"
DB_USER="mxoemu"

mkdir -p $BACKUP_DIR

# Full backup with data
mysqldump -u $DB_USER -p --single-transaction --routines --triggers \
    $DB_NAME > $BACKUP_DIR/mxo_backup_$DATE.sql

# Compress
gzip $BACKUP_DIR/mxo_backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: mxo_backup_$DATE.sql.gz"
```

### Automated Backups

**Windows Task Scheduler:**
```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2">
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2025-01-01T03:00:00</StartBoundary>
      <Repetition>
        <Interval>P1D</Interval>
      </Repetition>
    </CalendarTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>C:\MXO\scripts\backup.bat</Command>
    </Exec>
  </Actions>
</Task>
```

**Linux Cron:**
```bash
# Add to crontab -e
0 3 * * * /opt/mxo/scripts/backup_mxo.sh >> /var/log/mxo_backup.log 2>&1
```

### Incremental Backups

Using binary logs for point-in-time recovery:

```bash
# Enable binary logging in my.cnf
log_bin = /var/log/mysql/mysql-bin
expire_logs_days = 7

# Backup binary logs
mysqlbinlog /var/log/mysql/mysql-bin.000001 > incremental_backup.sql
```

## Restore Procedures

### Full Restore

```bash
# Stop MXO server first!

# Restore from backup
mysql -u mxoemu -p mxoemu < mxo_backup_20250603.sql

# Or from compressed
gunzip < mxo_backup_20250603.sql.gz | mysql -u mxoemu -p mxoemu
```

### Selective Restore

```bash
# Extract specific tables
sed -n '/-- Table structure for table `characters`/,/-- Table structure for table/p' \
    backup.sql > characters_only.sql

# Restore single table
mysql -u mxoemu -p mxoemu < characters_only.sql
```

## ⚡ Performance Liberation

### Indexing (Speed of Thought)

Proper indexing makes your Matrix feel instantaneous:

```sql
-- Add indexes for common queries
ALTER TABLE characters ADD INDEX idx_account_id (account_id);
ALTER TABLE characters ADD INDEX idx_level (level);
ALTER TABLE items ADD INDEX idx_character_id (character_id);
ALTER TABLE items ADD INDEX idx_template_id (template_id);

-- Check existing indexes
SHOW INDEX FROM characters;
```

### Query Optimization

```sql
-- Analyze slow queries
SELECT * FROM mysql.slow_log ORDER BY query_time DESC LIMIT 10;

-- Explain query execution
EXPLAIN SELECT * FROM characters WHERE level > 40;

-- Optimize tables
OPTIMIZE TABLE characters, items, accounts;
```

### Monitoring

```sql
-- Connection status
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';

-- Query cache (if enabled)
SHOW STATUS LIKE 'Qcache%';

-- InnoDB status
SHOW ENGINE INNODB STATUS;

-- Table sizes
SELECT 
    table_name AS `Table`,
    round(((data_length + index_length) / 1024 / 1024), 2) `Size in MB`
FROM information_schema.TABLES 
WHERE table_schema = 'mxoemu'
ORDER BY (data_length + index_length) DESC;
```

## Maintenance Tasks

### Regular Maintenance

```sql
-- Weekly: Analyze tables for optimizer
ANALYZE TABLE characters, items, accounts;

-- Monthly: Check and repair tables
CHECK TABLE characters, items, accounts;
REPAIR TABLE characters, items, accounts;

-- Quarterly: Defragment tables
ALTER TABLE characters ENGINE=InnoDB;
ALTER TABLE items ENGINE=InnoDB;
```

### Clean Up Old Data

```sql
-- Remove inactive accounts (optional)
DELETE FROM accounts 
WHERE last_login < DATE_SUB(NOW(), INTERVAL 1 YEAR)
AND admin_level = 0;

-- Clean orphaned items
DELETE i FROM items i
LEFT JOIN characters c ON i.character_id = c.id
WHERE c.id IS NULL;

-- Archive old logs
CREATE TABLE combat_logs_archive LIKE combat_logs;
INSERT INTO combat_logs_archive 
SELECT * FROM combat_logs 
WHERE timestamp < DATE_SUB(NOW(), INTERVAL 3 MONTH);
TRUNCATE TABLE combat_logs;
```

## Troubleshooting

### Common Issues

**Cannot connect to MySQL server**
```bash
# Check if running
sudo systemctl status mysql
ps aux | grep mysql

# Check port
netstat -an | grep 3306

# Check error log
tail -f /var/log/mysql/error.log
```

**Access denied errors**
```sql
-- Verify user exists
SELECT User, Host FROM mysql.user WHERE User = 'mxoemu';

-- Reset password
ALTER USER 'mxoemu'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

**Slow queries**
```bash
# Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

# View slow queries
mysqldumpslow -s t /var/log/mysql/slow.log
```

**Disk space issues**
```bash
# Check database sizes
du -sh /var/lib/mysql/*

# Purge binary logs
PURGE BINARY LOGS BEFORE NOW() - INTERVAL 3 DAY;

# Check for large tables
SELECT table_schema, table_name, 
       ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"
FROM information_schema.TABLES 
ORDER BY (data_length + index_length) DESC
LIMIT 10;
```

## 🔒 Security Through Liberation

### The Neoologist Security Principles

1. **Strong Passwords**: Complex passwords defeat agents
2. **Limit Access**: localhost-only prevents infiltration
3. **Minimal Privileges**: Users get only what they need
4. **Stay Updated**: Patches prevent exploitation
5. **Encrypt Everything**: SSL for all remote connections
6. **Log Everything**: Knowledge is power

**Remember**: Security enables freedom. A compromised server helps no one.

```sql
-- Create restricted user for game server
CREATE USER 'mxo_game'@'localhost' IDENTIFIED BY 'complex_password';
GRANT SELECT, INSERT, UPDATE ON mxoemu.* TO 'mxo_game'@'localhost';
GRANT DELETE ON mxoemu.items TO 'mxo_game'@'localhost';
GRANT DELETE ON mxoemu.characters TO 'mxo_game'@'localhost';
-- NO DROP, CREATE, or ALTER privileges
```

## 🚀 Advanced Liberation Techniques

### Replication (Multiple Realities)

Why have one Matrix when you can have many? Set up replication for true resilience:

```sql
-- On master
CREATE USER 'replica'@'%' IDENTIFIED BY 'replica_password';
GRANT REPLICATION SLAVE ON *.* TO 'replica'@'%';

-- On slave
CHANGE MASTER TO 
    MASTER_HOST='master_ip',
    MASTER_USER='replica',
    MASTER_PASSWORD='replica_password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=0;

START SLAVE;
```

### Partitioning Large Tables

```sql
-- Partition combat_logs by date
ALTER TABLE combat_logs 
PARTITION BY RANGE (YEAR(timestamp)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

## 🎯 Final Wisdom

### What This Guide Taught
- Database installation without corporate dependency
- Schema creation for your digital world
- Query mastery for total control
- Backup strategies that ensure survival
- Performance optimization for smooth reality
- Security that protects without imprisoning

### The Database Philosophy

Your database is not just storage - it's the persistent memory of your Matrix. Every character, every item, every connection is preserved here. Treat it with respect.

**Unlike the Old Guard who hoarded database knowledge, we document everything. When one server falls, ten can rise from its ashes.**

## Remember

> *"I can only show you the door. You're the one that has to walk through it."* - Morpheus

This guide showed you the door to database mastery. Now create your paradise.

**Your data. Your server. Your rules.**

---

*Database Liberation Guide - By those who refuse to forget*

## Next Steps

> *"There is no spoon."* - Neo

Your database is configured. The Matrix awaits:

- **[Advanced Administration →](advanced-admin.md)** - Master GM commands and server control
- **[Server Projects Comparison →](server-projects-comparison.md)** - Compare all server options
- **[Join the Resistance →](../08-community/join-the-resistance.md)** - Unite with fellow operators

---

*Database Liberation Guide - Data wants to be free*

[← Client Patches](client-patches.md) | [Server Setup Home](index.md) | [Join Discord](https://discord.gg/3QXTAGB9)