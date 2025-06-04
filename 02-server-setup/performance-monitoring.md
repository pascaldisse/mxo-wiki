# Performance Monitoring Guide
**Optimizing Your Matrix Online Server**

> *"Unfortunately, no one can be told what good performance is. You have to measure it for yourself."*

## Overview

Performance monitoring is crucial for maintaining a smooth Matrix Online experience. This guide covers tools and techniques for monitoring and optimizing your server.

## Key Metrics to Monitor

### 🖥️ Server Resources
- **CPU Usage**: Should stay below 80% during peak
- **RAM Usage**: Recommended to keep 20% free
- **Disk I/O**: Monitor for bottlenecks
- **Network Bandwidth**: Track incoming/outgoing traffic

### 🎮 Game Metrics
- **Player Count**: Current vs maximum capacity
- **Tick Rate**: Server update frequency
- **Database Queries**: Response time and queue length
- **Object Count**: NPCs, items, active missions

### 📊 Performance Indicators
- **Login Time**: Should be under 5 seconds
- **Zone Loading**: Target under 10 seconds
- **Combat Lag**: Minimal delay in ability execution
- **Chat Delay**: Near-instantaneous delivery

## Monitoring Tools

### Built-in Server Commands
```bash
# MXOEmu monitoring
/server status
/server performance
/server connections

# Database monitoring
SHOW PROCESSLIST;
SHOW STATUS;
SHOW VARIABLES;
```

### System Tools

#### Linux
```bash
# CPU and Memory
top
htop
vmstat 1

# Disk I/O
iostat -x 1
iotop

# Network
netstat -tuln
iftop
```

#### Windows
- Task Manager (Basic)
- Performance Monitor
- Resource Monitor
- Process Explorer

### Third-Party Solutions
- **Prometheus + Grafana**: Professional monitoring stack
- **Nagios**: Alert-based monitoring
- **Zabbix**: Comprehensive monitoring platform
- **New Relic**: Application performance monitoring

## Performance Optimization

### Database Optimization
1. **Index Critical Tables**
   ```sql
   -- Example: Index character table
   CREATE INDEX idx_character_name ON characters(name);
   CREATE INDEX idx_character_location ON characters(district_id, x, y, z);
   ```

2. **Regular Maintenance**
   ```sql
   -- Optimize tables weekly
   OPTIMIZE TABLE characters;
   OPTIMIZE TABLE items;
   OPTIMIZE TABLE missions;
   ```

3. **Query Optimization**
   - Use EXPLAIN on slow queries
   - Avoid SELECT * when possible
   - Implement query caching

### Server Configuration

#### MXOEmu Optimization
```ini
# config.ini optimizations
MaxPlayers=100  # Set realistic limit
TickRate=30     # Balance performance vs responsiveness
ObjectPoolSize=10000  # Adjust based on RAM
```

#### System Optimization
- **CPU**: Enable performance governor
- **RAM**: Disable swap if sufficient memory
- **Disk**: Use SSD for database
- **Network**: Optimize TCP settings

### Common Performance Issues

#### High CPU Usage
**Symptoms**: Lag, delayed responses
**Solutions**:
- Reduce NPC spawn rates
- Optimize pathfinding algorithms
- Limit concurrent missions

#### Memory Leaks
**Symptoms**: Increasing RAM usage over time
**Solutions**:
- Regular server restarts
- Monitor object cleanup
- Update to latest patches

#### Database Bottlenecks
**Symptoms**: Slow loading, save failures
**Solutions**:
- Add database indexes
- Increase connection pool
- Consider database clustering

## Monitoring Dashboard Setup

### Basic Grafana Dashboard
1. Install Grafana and Prometheus
2. Configure server metrics export
3. Import MXO dashboard template
4. Set up alerts for critical thresholds

### Key Dashboard Panels
- Server resource usage
- Player count over time
- Database query performance
- Network traffic analysis
- Error rate monitoring

## Performance Benchmarks

### Minimum Requirements
- **10 Players**: 2 CPU cores, 4GB RAM
- **50 Players**: 4 CPU cores, 8GB RAM
- **100 Players**: 8 CPU cores, 16GB RAM
- **200+ Players**: Dedicated hardware recommended

### Target Performance
- **Server TPS**: 20+ (ticks per second)
- **Database Response**: <100ms average
- **Network Latency**: <150ms to players
- **Uptime**: 99.9% availability

## Troubleshooting Performance

### Performance Diagnostic Steps
1. Check system resources (CPU, RAM, Disk)
2. Review server logs for errors
3. Analyze database slow query log
4. Monitor network connectivity
5. Profile application hotspots

### Emergency Response
If performance degrades critically:
1. Notify players of issues
2. Restart affected services
3. Clear temporary data
4. Scale resources if needed
5. Implement fixes and monitor

## Best Practices

### Regular Maintenance
- **Daily**: Check error logs
- **Weekly**: Review performance trends
- **Monthly**: Optimize database
- **Quarterly**: Capacity planning

### Proactive Monitoring
- Set up automated alerts
- Track baseline performance
- Plan for growth
- Document all changes

## Community Resources

### Performance Optimization Guides
- Discord #server-performance channel
- Community benchmarking spreadsheet
- Optimization script collection

### Getting Help
- Share metrics when asking for help
- Use standardized benchmarking tools
- Contribute findings back to community

---

**Remember**: Good performance isn't just about hardware - it's about configuration, optimization, and continuous monitoring.

---

[← Back to Troubleshooting](server-troubleshooting.md) | [Advanced Administration →](advanced-admin.md) | [Server Security →](server-security-hardening.md)