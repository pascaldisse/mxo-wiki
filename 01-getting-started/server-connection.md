# Connecting to Matrix Online Servers
**Your First Jack-In**

> *"This is your last chance. After this, there is no turning back."*

## Quick Start

### Prerequisites
- Matrix Online client (patched)
- Server address (from your provider)
- Account credentials
- Open firewall ports

### Connection Steps

#### 1. Configure Client
Edit your client configuration to point to your chosen server:
- **MXOEmu**: Edit `server.dat` with server address
- **Hardline Dreams**: Use launcher to set server
- **Custom Server**: Follow provider instructions

#### 2. Launch Game
```bash
# For patched client
matrix.exe -server <address>

# For launcher
launcher.exe
```

#### 3. Login
- Enter username and password
- Select character or create new
- Jack in!

## Detailed Setup by Server Type

### MXOEmu Connection
See [MXOEmu Setup Guide](../02-server-setup/mxoemu-setup.md) for complete instructions.

**Quick Config**:
1. Edit `server.dat` in game directory
2. Replace content with server address
3. Save and launch game

### Hardline Dreams Connection
See [Hardline Dreams Setup](../02-server-setup/hardline-dreams-setup.md) for full details.

**Quick Config**:
1. Run HD launcher
2. Enter server details in settings
3. Click "Play"

### Local Server Connection
For testing your own server:
```
Server: localhost or 127.0.0.1
Port: 2106 (default)
```

## Common Connection Issues

### "Cannot Connect to Server"
**Causes**:
- Server is offline
- Incorrect address/port
- Firewall blocking connection
- Client not patched correctly

**Solutions**:
1. Verify server status
2. Check server address
3. Disable firewall temporarily
4. Re-patch client

### "Invalid Username/Password"
**Causes**:
- Wrong credentials
- Account not created
- Database connection issue

**Solutions**:
1. Verify credentials
2. Create account if needed
3. Contact server admin

### "Version Mismatch"
**Causes**:
- Client version incompatible
- Server running different version
- Missing patches

**Solutions**:
1. Download correct client version
2. Apply all required patches
3. Check server requirements

## Network Requirements

### Ports
- **TCP 2106**: Game server (default)
- **TCP 80/443**: Web services
- **TCP 3306**: Database (server-side only)

### Bandwidth
- **Minimum**: 56k (very laggy)
- **Recommended**: Broadband
- **Optimal**: 10+ Mbps

### Latency
- **Excellent**: <50ms
- **Good**: 50-150ms
- **Playable**: 150-250ms
- **Poor**: >250ms

## Advanced Configuration

### Custom Launchers
Some communities provide custom launchers:
- Auto-patching
- Server selection
- News integration
- Character preview

### Multiple Servers
To switch between servers:
1. Keep separate client folders
2. Use different launchers
3. Batch files for quick switching

### VPN Usage
If server is region-locked:
1. Connect to VPN first
2. Choose server near game server
3. Launch game normally
4. Monitor for increased latency

## Testing Your Connection

### Basic Test
1. Ping server address
2. Check port accessibility
3. Verify credentials
4. Test login

### Network Diagnostics
```cmd
# Windows
ping servername.com
tracert servername.com
telnet servername.com 2106

# Linux/Mac
ping servername.com
traceroute servername.com
nc -zv servername.com 2106
```

## Getting Help

### Connection Support
- **Discord**: #tech-support channel
- **Forums**: Connection issues section
- **Wiki**: [Troubleshooting Guide](../02-server-setup/server-troubleshooting.md)

### Before Asking for Help
1. Check server status
2. Verify your setup
3. Test basic connectivity
4. Gather error messages
5. List troubleshooting attempts

## Next Steps

Once connected:
- [Create your first character](character-creation.md)
- [Learn the interface](interface-guide.md)
- [Explore the districts](../05-game-content/districts/index.md)
- [Join the community](../08-community/join-the-resistance.md)

---

**Welcome to The Matrix. Follow the white rabbit.**

---

[← Back to Getting Started](index.md) | [Server Setup →](../02-server-setup/index.md) | [Troubleshooting →](../02-server-setup/server-troubleshooting.md)