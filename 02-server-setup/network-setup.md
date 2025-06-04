# Network Setup Guide

> **Status**: Documentation in progress
> 
> This guide covers network configuration for Matrix Online server setups.

## Port Configuration

### Required Ports
- **10000**: Authentication Server
- **10001**: World Server  
- **10002**: Chat Server
- **3306**: MySQL Database (if external)

### Firewall Rules
```batch
netsh advfirewall firewall add rule name="MXO Auth" dir=in action=allow protocol=TCP localport=10000
netsh advfirewall firewall add rule name="MXO World" dir=in action=allow protocol=TCP localport=10001
netsh advfirewall firewall add rule name="MXO Chat" dir=in action=allow protocol=TCP localport=10002
```

## Router Configuration

### Port Forwarding
Forward these ports from your router to your server machine:
- TCP 10000 → Server IP:10000
- TCP 10001 → Server IP:10001  
- TCP 10002 → Server IP:10002

### Dynamic DNS
For home servers, consider using:
- No-IP
- DynDNS
- Duck DNS

## Testing Connectivity

### Internal Testing
```batch
telnet localhost 10000
netstat -an | findstr "10000"
```

### External Testing
Use online port checkers or have friends test connections.

---

[← Back to Server Setup](index.md) | [Next: Database Setup →](database-setup.md)