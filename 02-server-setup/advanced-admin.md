# Advanced Server Administration
**Master the Matrix Administration**

> *"Choice. The problem is choice."* - Neo

Advanced administration techniques for Matrix Online server operators. This guide covers complex configurations, performance optimization, and troubleshooting procedures for experienced administrators.

## 🎯 Prerequisites

### Required Knowledge
- **Basic Server Setup**: Completed [MXOEmu](mxoemu-setup.md) or [Hardline Dreams](hardline-dreams-setup.md) setup
- **Database Administration**: Familiar with [Database Setup](database-setup.md)
- **Command Line Experience**: Comfortable with terminal/command prompt
- **Network Configuration**: Understanding of port forwarding and firewalls

### Administrative Access
- **Server Console**: Direct access to server terminal
- **Database Access**: Administrative privileges on MySQL/PostgreSQL
- **System Administration**: Root/Administrator access to host system
- **Network Control**: Ability to modify firewall and routing rules

## 🛠️ Advanced Configuration

### Performance Optimization

#### Server Performance Tuning
```bash
# MySQL optimization for MXO
[mysqld]
innodb_buffer_pool_size = 2G
innodb_log_file_size = 512M
max_connections = 200
query_cache_size = 128M
query_cache_type = 1

# Monitor server performance
htop
iotop
nethogs
```

#### Memory Management
```bash
# Check server memory usage
free -h
cat /proc/meminfo

# Java heap tuning (for applicable servers)
export JAVA_OPTS="-Xms2g -Xmx4g -XX:+UseG1GC"

# Monitor memory leaks
valgrind --leak-check=full ./server_binary
```

#### Network Optimization
```bash
# Network tuning
echo 'net.core.rmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem = 4096 87380 134217728' >> /etc/sysctl.conf

# Apply network changes
sysctl -p
```

### Advanced Security

#### Firewall Configuration
```bash
# UFW rules for MXO server
ufw allow 7000/tcp  # MXO game port
ufw allow 7001/tcp  # Admin port
ufw allow 3306/tcp from 192.168.1.0/24  # MySQL (local network only)
ufw deny 22/tcp  # Disable SSH from public (use VPN)

# iptables advanced rules
iptables -A INPUT -p tcp --dport 7000 -m conntrack --ctstate NEW -m limit --limit 10/minute -j ACCEPT
iptables -A INPUT -p tcp --dport 7000 -m conntrack --ctstate NEW -j DROP
```

#### Database Security
```sql
-- Create limited database user
CREATE USER 'mxo_limited'@'localhost' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE ON mxo_database.* TO 'mxo_limited'@'localhost';

-- Revoke dangerous permissions
REVOKE FILE ON *.* FROM 'mxo_user'@'localhost';
REVOKE PROCESS ON *.* FROM 'mxo_user'@'localhost';

-- Enable MySQL logging
SET GLOBAL general_log = 'ON';
SET GLOBAL log_output = 'FILE';
```

#### SSL/TLS Setup
```bash
# Generate SSL certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout mxo-server.key -out mxo-server.crt

# Configure server for SSL
server.ssl.enabled=true
server.ssl.certificate=/path/to/mxo-server.crt
server.ssl.private-key=/path/to/mxo-server.key
```

## 🔧 Administration Tools

### GM Commands System

#### Player Management
```
/teleport <player> <x> <y> <z>  # Teleport player to coordinates
/kick <player> [reason]         # Kick player from server
/ban <player> [duration] [reason] # Ban player temporarily or permanently
/unban <player>                 # Remove player ban
/mute <player> [duration]       # Prevent player from chatting
/unmute <player>                # Restore player chat privileges
```

#### Character Manipulation
```
/setlevel <player> <level>      # Set player level
/givexp <player> <amount>       # Give experience points
/giveitem <player> <item_id> <quantity> # Give items to player
/setstat <player> <stat> <value> # Modify player statistics
/heal <player>                  # Restore player health
/godmode <player> [on/off]      # Toggle player invincibility
```

#### World Management
```
/weather <type>                 # Change weather effects
/time <hour>                    # Set world time
/broadcast <message>            # Send message to all players
/shutdown <minutes>             # Schedule server shutdown
/restart <minutes>              # Schedule server restart
/save                          # Force save all player data
```

### Monitoring and Diagnostics

#### Real-time Monitoring
```bash
# Monitor server logs
tail -f server.log | grep ERROR
tail -f access.log | grep -v "heartbeat"

# Database query monitoring
mysql -e "SHOW PROCESSLIST;"
mysql -e "SHOW ENGINE INNODB STATUS;"

# Player connection monitoring
netstat -an | grep :7000 | wc -l
ss -tuln | grep 7000
```

#### Performance Analysis
```bash
# CPU and memory profiling
perf record -g ./mxo_server
perf report

# Database performance
mysql -e "SELECT * FROM information_schema.processlist WHERE time > 5;"
mysql -e "SHOW GLOBAL STATUS LIKE 'Slow_queries';"

# Network analysis
tcpdump -i eth0 port 7000 -w mxo_traffic.pcap
wireshark mxo_traffic.pcap
```

### Backup and Recovery

#### Automated Backup System
```bash
#!/bin/bash
# MXO Server Backup Script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/mxo"
DB_NAME="mxo_database"

# Database backup
mysqldump --single-transaction --routines --triggers $DB_NAME > $BACKUP_DIR/db_$DATE.sql

# Character data backup
cp -r /server/characters $BACKUP_DIR/characters_$DATE

# Configuration backup
cp /server/config/* $BACKUP_DIR/config_$DATE/

# Compress backup
tar -czf $BACKUP_DIR/mxo_backup_$DATE.tar.gz $BACKUP_DIR/*_$DATE*

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

#### Disaster Recovery
```bash
# Database recovery
mysql $DB_NAME < backup_db.sql

# Character data recovery
cp -r backup_characters/* /server/characters/

# Verify data integrity
mysqlcheck --check --all-databases
```

## 🚨 Troubleshooting

### Common Issues

#### High CPU Usage
```bash
# Identify CPU-intensive processes
top -p $(pgrep mxo_server)
strace -p $(pgrep mxo_server) -c

# Check for infinite loops
gdb -p $(pgrep mxo_server)
(gdb) bt
(gdb) continue
```

#### Memory Leaks
```bash
# Monitor memory usage over time
while true; do
  ps aux | grep mxo_server | grep -v grep >> memory_usage.log
  sleep 60
done

# Analyze memory patterns
cat memory_usage.log | awk '{print $6}' | tail -100
```

#### Database Connectivity
```sql
-- Check database connections
SHOW PROCESSLIST;
SHOW GLOBAL STATUS LIKE 'Max_used_connections';
SHOW GLOBAL STATUS LIKE 'Threads_connected';

-- Identify problematic queries
SELECT * FROM information_schema.processlist WHERE time > 10;
```

#### Network Issues
```bash
# Test server connectivity
telnet localhost 7000
nc -zv localhost 7000

# Check port availability
netstat -tuln | grep 7000
lsof -i :7000

# Monitor network traffic
iftop -i eth0
```

### Performance Bottlenecks

#### Database Optimization
```sql
-- Identify slow queries
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;

-- Analyze query performance
EXPLAIN SELECT * FROM characters WHERE name = 'PlayerName';

-- Optimize indexes
CREATE INDEX idx_character_name ON characters(name);
ANALYZE TABLE characters;
```

#### Application Tuning
```bash
# Profile application performance
perf top -p $(pgrep mxo_server)

# Monitor system calls
strace -p $(pgrep mxo_server) -f -e trace=network

# Check file descriptor usage
lsof -p $(pgrep mxo_server) | wc -l
```

## 🔐 Security Hardening

### Server Security

#### System Hardening
```bash
# Disable unnecessary services
systemctl disable telnet
systemctl disable ftp
systemctl disable rsh

# Secure SSH configuration
echo "PermitRootLogin no" >> /etc/ssh/sshd_config
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
systemctl reload sshd

# File permissions
chmod 600 /server/config/database.conf
chown mxo:mxo /server/logs
```

#### Application Security
```bash
# Run server as non-root user
useradd -r -s /bin/false mxoserver
chown -R mxoserver:mxoserver /server

# Limit resource usage
echo "mxoserver soft nofile 65536" >> /etc/security/limits.conf
echo "mxoserver hard nofile 65536" >> /etc/security/limits.conf
```

### Monitoring and Alerting

#### Security Monitoring
```bash
# Monitor failed login attempts
tail -f /var/log/auth.log | grep "Failed password"

# Watch for suspicious activity
fail2ban-client status
fail2ban-client status sshd

# Monitor server access
tail -f server.log | grep -E "(admin|gm|ban|kick)"
```

#### Automated Alerts
```bash
#!/bin/bash
# Alert script for critical events

# Check server status
if ! pgrep mxo_server > /dev/null; then
    echo "MXO Server Down!" | mail -s "Server Alert" admin@example.com
fi

# Check database connectivity
if ! mysql -e "SELECT 1;" &> /dev/null; then
    echo "Database Connection Failed!" | mail -s "DB Alert" admin@example.com
fi

# Check disk space
if [ $(df / | tail -1 | awk '{print $5}' | sed 's/%//') -gt 90 ]; then
    echo "Low Disk Space!" | mail -s "Disk Alert" admin@example.com
fi
```

## 📊 Advanced Analytics

### Player Behavior Analysis
```sql
-- Player login patterns
SELECT HOUR(login_time) as hour, COUNT(*) as logins
FROM login_log 
WHERE login_time > NOW() - INTERVAL 7 DAY
GROUP BY HOUR(login_time);

-- Popular locations
SELECT x, y, z, COUNT(*) as visits
FROM player_locations
GROUP BY x, y, z
ORDER BY visits DESC
LIMIT 10;

-- Character progression rates
SELECT level, AVG(DATEDIFF(NOW(), created_date)) as avg_days
FROM characters
GROUP BY level
ORDER BY level;
```

### Server Performance Metrics
```bash
# Generate performance report
echo "=== MXO Server Performance Report ===" > performance_report.txt
echo "Date: $(date)" >> performance_report.txt
echo "Uptime: $(uptime)" >> performance_report.txt
echo "Memory Usage: $(free -h | grep Mem:)" >> performance_report.txt
echo "CPU Usage: $(top -bn1 | grep load)" >> performance_report.txt
echo "Active Players: $(netstat -an | grep :7000 | grep ESTABLISHED | wc -l)" >> performance_report.txt
```

## 🤝 Advanced Community Management

### Player Communication
- **Announcement System**: Scheduled broadcasts and event notifications
- **Community Events**: Organizing and managing special events
- **Feedback Collection**: Player satisfaction surveys and improvement tracking
- **Conflict Resolution**: Handling player disputes and rule violations

### Content Management
- **Dynamic Events**: Creating temporary world changes
- **Content Updates**: Managing patches and new content deployment
- **Quality Assurance**: Testing changes before production deployment
- **Rollback Procedures**: Reverting problematic updates safely

---

## 🌟 Mastery Achievement

You've completed the advanced administration guide! You now have the knowledge to:
- ✅ **Optimize Performance** - Tune server and database for maximum efficiency
- ✅ **Secure Systems** - Implement comprehensive security measures
- ✅ **Monitor Operations** - Track server health and player activity
- ✅ **Troubleshoot Issues** - Diagnose and resolve complex problems
- ✅ **Manage Community** - Handle advanced administrative scenarios

**Welcome to Matrix Online server mastery. The digital world is under your control.**

---

[← Back to Database Setup](database-setup.md) | [Server Troubleshooting →](server-troubleshooting.md) | [Join the Resistance →](../08-community/join-the-resistance.md)

📚 [View Sources](../sources/02-server-setup/advanced-admin-sources.md)