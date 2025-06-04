# Server Troubleshooting Guide
**Debugging the Digital Matrix**

> *"Unfortunately, no one can be told what the Matrix is. You have to debug it for yourself."*

Comprehensive troubleshooting guide for Matrix Online server administrators. Solutions for common problems, diagnostic procedures, and recovery techniques.

## 🚨 Emergency Procedures

### Server Won't Start

#### Quick Diagnostics
```bash
# Check if server process is running
ps aux | grep mxo
pgrep -f "mxo\|matrix"

# Verify port availability
netstat -tuln | grep 7000
lsof -i :7000

# Check system resources
free -h
df -h
```

#### Common Causes and Solutions

**1. Port Already in Use**
```bash
# Find what's using the port
lsof -i :7000
sudo kill -9 <PID>

# Or use different port
./mxo_server --port 7001
```

**2. Database Connection Failed**
```bash
# Test database connectivity
mysql -u mxo_user -p -h localhost mxo_database

# Check database service
systemctl status mysql
systemctl restart mysql
```

**3. Permission Issues**
```bash
# Fix file permissions
sudo chown -R mxo:mxo /server/
chmod +x /server/mxo_server
chmod 644 /server/config/*.conf
```

**4. Missing Dependencies**
```bash
# Check library dependencies
ldd /server/mxo_server
ldconfig -p | grep ssl

# Install missing libraries
sudo apt-get install libssl1.1 libmysqlclient21
```

### Database Issues

#### Connection Problems
```sql
-- Check user permissions
SELECT User, Host FROM mysql.user WHERE User = 'mxo_user';
SHOW GRANTS FOR 'mxo_user'@'localhost';

-- Reset user password
ALTER USER 'mxo_user'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

#### Corruption Recovery
```bash
# Check for corruption
mysqlcheck --check --all-databases

# Repair corrupted tables
mysqlcheck --repair mxo_database
mysqlcheck --optimize mxo_database

# Emergency recovery
mysqld --skip-grant-tables --skip-networking
```

#### Performance Issues
```sql
-- Check slow queries
SHOW GLOBAL STATUS LIKE 'Slow_queries';
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;

-- Monitor active connections
SHOW PROCESSLIST;
SHOW GLOBAL STATUS LIKE 'Threads_connected';

-- Optimize queries
EXPLAIN SELECT * FROM characters WHERE name = 'TestPlayer';
ANALYZE TABLE characters;
```

## 🔧 Common Problems and Solutions

### Player Connection Issues

#### "Unable to Connect to Server"
```bash
# Check server status
systemctl status mxo-server

# Verify network connectivity
telnet server_ip 7000
nc -zv server_ip 7000

# Check firewall rules
sudo ufw status
iptables -L | grep 7000
```

#### "Authentication Failed"
```sql
-- Check player account
SELECT * FROM accounts WHERE username = 'playername';

-- Reset player password
UPDATE accounts SET password = SHA1('newpassword') WHERE username = 'playername';

-- Check account status
SELECT username, status, banned FROM accounts WHERE username = 'playername';
```

#### "Character Load Failed"
```sql
-- Verify character data
SELECT * FROM characters WHERE account_id = 123;

-- Check for data corruption
SELECT * FROM characters WHERE x IS NULL OR y IS NULL OR z IS NULL;

-- Restore from backup
INSERT INTO characters SELECT * FROM characters_backup WHERE character_id = 456;
```

### Performance Problems

#### High CPU Usage
```bash
# Identify CPU-intensive processes
top -p $(pgrep mxo_server)
htop -p $(pgrep mxo_server)

# Profile application
perf record -g -p $(pgrep mxo_server)
perf report

# Check for infinite loops
strace -p $(pgrep mxo_server) -c
```

#### Memory Leaks
```bash
# Monitor memory usage
while true; do
    ps aux | grep mxo_server | grep -v grep | awk '{print strftime("%Y-%m-%d %H:%M:%S"), $6}' >> memory_log.txt
    sleep 60
done

# Analyze memory pattern
cat memory_log.txt | tail -100

# Use memory debugging tools
valgrind --leak-check=full --show-leak-kinds=all ./mxo_server
```

#### Network Lag
```bash
# Monitor network traffic
iftop -i eth0 -P
nethogs

# Check bandwidth usage
vnstat -i eth0 -h

# Test network latency
ping -c 10 client_ip
mtr client_ip
```

### Combat System Issues

#### Combat Not Working
```sql
-- Check combat configuration
SELECT * FROM server_config WHERE config_key LIKE '%combat%';

-- Verify skill data
SELECT * FROM character_skills WHERE character_id = 123;

-- Check for combat packets
SELECT * FROM packet_log WHERE packet_type = 'combat' ORDER BY timestamp DESC LIMIT 10;
```

#### Damage Calculation Errors
```bash
# Enable combat debugging
echo "debug.combat=true" >> /server/config/debug.conf

# Monitor combat logs
tail -f /server/logs/combat.log | grep ERROR

# Check damage formulas
grep -r "damage.*calculation" /server/src/
```

### Mission System Problems

#### Missions Not Loading
```sql
-- Check mission data
SELECT * FROM missions WHERE mission_id = 123;

-- Verify mission requirements
SELECT * FROM mission_requirements WHERE mission_id = 123;

-- Check player mission status
SELECT * FROM player_missions WHERE player_id = 456;
```

#### Mission Completion Issues
```sql
-- Reset mission progress
UPDATE player_missions SET status = 'available' WHERE player_id = 456 AND mission_id = 123;

-- Check mission triggers
SELECT * FROM mission_triggers WHERE mission_id = 123;

-- Verify reward data
SELECT * FROM mission_rewards WHERE mission_id = 123;
```

## 🔍 Diagnostic Tools

### Log Analysis

#### Server Logs
```bash
# Real-time log monitoring
tail -f /server/logs/server.log

# Error detection
grep -i error /server/logs/server.log | tail -20

# Connection tracking
grep "player.*connect" /server/logs/server.log | tail -10

# Performance analysis
grep "query.*time" /server/logs/database.log | awk '{if ($NF > 1000) print $0}'
```

#### Database Logs
```bash
# MySQL slow query log
tail -f /var/log/mysql/mysql-slow.log

# Connection analysis
grep "Connect\|Quit" /var/log/mysql/mysql.log | tail -20

# Error detection
grep -i error /var/log/mysql/error.log
```

### Network Diagnostics

#### Connection Testing
```bash
# Test game port
telnet server_ip 7000

# Check connection from client perspective
nmap -p 7000 server_ip

# Monitor active connections
netstat -an | grep :7000 | grep ESTABLISHED | wc -l

# Analyze connection patterns
ss -tuln | grep 7000
```

#### Packet Analysis
```bash
# Capture game traffic
tcpdump -i eth0 port 7000 -w game_traffic.pcap

# Analyze with wireshark
wireshark game_traffic.pcap

# Monitor specific connections
tcpdump -i eth0 host client_ip and port 7000
```

### System Monitoring

#### Resource Usage
```bash
# CPU monitoring
sar -u 1 10

# Memory analysis
free -h -s 1

# Disk I/O monitoring
iostat -x 1 10

# Network monitoring
sar -n DEV 1 10
```

#### Process Analysis
```bash
# Monitor server process
watch -n 1 'ps aux | grep mxo_server'

# File descriptor usage
lsof -p $(pgrep mxo_server) | wc -l

# System call analysis
strace -p $(pgrep mxo_server) -c
```

## 🛠️ Recovery Procedures

### Data Recovery

#### Character Recovery
```sql
-- Backup current data
CREATE TABLE characters_backup AS SELECT * FROM characters;

-- Restore from specific backup
INSERT INTO characters 
SELECT * FROM characters_20241201 
WHERE character_id = 123;

-- Verify data integrity
SELECT COUNT(*) FROM characters WHERE account_id IS NULL;
```

#### Database Recovery
```bash
# Full database restore
mysql mxo_database < backup_20241201.sql

# Selective table restore
mysql mxo_database -e "DROP TABLE characters;"
mysql mxo_database < characters_backup.sql

# Point-in-time recovery
mysqlbinlog --start-datetime="2024-12-01 10:00:00" \
           --stop-datetime="2024-12-01 15:00:00" \
           mysql-bin.000001 | mysql mxo_database
```

### Configuration Recovery

#### Server Configuration
```bash
# Backup current config
cp -r /server/config /server/config.backup.$(date +%Y%m%d)

# Restore default configuration
cp -r /server/config.default/* /server/config/

# Restore from backup
cp -r /server/config.backup.20241201/* /server/config/
```

#### User Recovery
```bash
# Reset admin password
mysql -e "UPDATE accounts SET password = SHA1('newadminpass') WHERE username = 'admin';"

# Restore user permissions
mysql -e "UPDATE accounts SET admin_level = 5 WHERE username = 'admin';"

# Unban all users (emergency)
mysql -e "UPDATE accounts SET banned = 0, ban_reason = NULL;"
```

## 📈 Performance Optimization

### Server Tuning

#### Memory Optimization
```bash
# Adjust JVM heap (if applicable)
export JAVA_OPTS="-Xms2g -Xmx4g -XX:+UseG1GC"

# System memory tuning
echo 'vm.swappiness=10' >> /etc/sysctl.conf
echo 'vm.dirty_ratio=15' >> /etc/sysctl.conf
sysctl -p
```

#### Network Tuning
```bash
# TCP optimization
echo 'net.core.rmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_congestion_control = bbr' >> /etc/sysctl.conf
sysctl -p
```

### Database Optimization

#### MySQL Tuning
```ini
[mysqld]
innodb_buffer_pool_size = 2G
innodb_log_file_size = 512M
max_connections = 200
query_cache_size = 128M
table_open_cache = 2000
thread_cache_size = 16
```

#### Index Optimization
```sql
-- Analyze table usage
SELECT table_name, 
       ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "MB"
FROM information_schema.tables 
WHERE table_schema = "mxo_database";

-- Create missing indexes
CREATE INDEX idx_character_name ON characters(name);
CREATE INDEX idx_account_username ON accounts(username);
CREATE INDEX idx_login_timestamp ON login_log(timestamp);
```

## 🔐 Security Troubleshooting

### Security Incidents

#### Suspicious Activity Detection
```bash
# Monitor failed login attempts
grep "authentication failed" /server/logs/server.log | tail -20

# Check for unusual connection patterns
netstat -an | grep :7000 | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr

# Analyze admin command usage
grep "admin.*command" /server/logs/server.log | tail -20
```

#### Intrusion Response
```bash
# Emergency shutdown
systemctl stop mxo-server

# Block suspicious IPs
iptables -A INPUT -s suspicious_ip -j DROP

# Change admin passwords
mysql -e "UPDATE accounts SET password = SHA1(RAND()) WHERE admin_level > 0;"

# Enable logging
echo "debug.security=true" >> /server/config/debug.conf
```

### Access Control Issues

#### Permission Problems
```sql
-- Check user permissions
SELECT username, admin_level, banned FROM accounts WHERE admin_level > 0;

-- Reset permissions
UPDATE accounts SET admin_level = 0 WHERE username != 'superadmin';

-- Audit admin actions
SELECT * FROM admin_log ORDER BY timestamp DESC LIMIT 20;
```

## 📞 Getting Help

### Community Support
- **Discord**: Join the [Matrix Online Community](https://discord.gg/3QXTAGB9)
- **Forums**: Check existing troubleshooting threads
- **Documentation**: Review [Server Setup Guides](index.md)

### Professional Support
- **Emergency Contact**: Critical server issues requiring immediate assistance
- **Consulting Services**: Advanced configuration and optimization
- **Training**: Administrator training and certification programs

### Self-Help Resources
- **Log Analysis Tools**: Automated log parsing and analysis
- **Monitoring Scripts**: Automated health checking and alerting
- **Recovery Procedures**: Step-by-step disaster recovery guides

---

## 🌟 Troubleshooting Mastery

You've completed the comprehensive troubleshooting guide! You now know how to:
- ✅ **Diagnose Issues** - Systematically identify problems
- ✅ **Implement Solutions** - Apply appropriate fixes quickly
- ✅ **Prevent Problems** - Proactive monitoring and maintenance
- ✅ **Recover from Failures** - Restore service after incidents
- ✅ **Optimize Performance** - Keep servers running smoothly

**Server problems are just puzzles waiting to be solved. You have the tools to solve them all.**

---

[← Back to Advanced Administration](advanced-admin.md) | [Performance Monitoring →](performance-monitoring.md) | [Join the Resistance →](../08-community/join-the-resistance.md)

📚 [View Sources](sources/index.md)