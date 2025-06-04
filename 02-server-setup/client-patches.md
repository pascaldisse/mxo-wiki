# Matrix Online Client Patching Guide

## Overview

To connect to private Matrix Online servers, you need to modify your game client to point to the new server address instead of the original SOE servers. This guide covers multiple methods from simple to advanced.

**Important**: Always backup your original files before patching!

## Prerequisites

- Matrix Online client (version 66.6.6 preferred)
- Administrator access on Windows
- Basic understanding of IP addresses
- Hex editor (for manual method)

## Quick Reference

**Files that need patching:**
- `launcher.exe` - Game launcher
- `matrix.exe` - Main game executable
- `matrix.ini` - Configuration file (some methods)

**Original server addresses to replace:**
- `mxo.station.sony.com`
- `mxo-login.station.sony.com` 
- `patch.mxoemu.info`
- `testauth.mxoemu.info`

## Method 1: Automatic Patcher (Easiest)

### Using HD Client Patcher

1. Download HD Client Patcher from Hardline Dreams tools
2. Run as Administrator:
   ```batch
   HDClientPatcher.exe "C:\Program Files\Sony\Matrix Online" [server_ip]
   ```
3. Replace `[server_ip]` with your server's IP address
4. Patcher will backup and modify necessary files

### Using MXO Universal Patcher

```batch
# Download from community tools
MXOPatcher.exe --client "C:\Matrix Online" --server 192.168.1.100 --backup
```

## Method 2: Hex Editor (Manual)

### Required Tools

- Hex editor (HxD, Hex Workshop, or similar)
- Text editor with hex view capability

### Step-by-Step Process

#### 1. Patch launcher.exe

Open `launcher.exe` in hex editor:

**Find and Replace (maintain exact length):**
```
Original: testauth.mxoemu.info (20 bytes)
Replace:  192.168.001.100      (pad with spaces)

Original: patch.mxoemu.info    (17 bytes)
Replace:  192.168.001.100      (pad with spaces)
```

**Hex values to search:**
```
74 65 73 74 61 75 74 68 2E 6D 78 6F 65 6D 75 2E 69 6E 66 6F
```

#### 2. Patch matrix.exe

Similar process for `matrix.exe`:

**Common offsets (may vary by version):**
- Auth server: `0xB6194`
- Patch server: `0xAB373`
- DNS suffix: `0xB198C`

### Using Python Script

Create `patch_client.py`:

```python
#!/usr/bin/env python3
import sys
import shutil

def patch_file(filename, old_addr, new_addr):
    # Backup original
    shutil.copy(filename, filename + '.backup')
    
    # Read file
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Pad new address to match length
    new_addr_padded = new_addr.ljust(len(old_addr), b'\x00')
    
    # Replace
    data = data.replace(old_addr.encode(), new_addr_padded)
    
    # Write back
    with open(filename, 'wb') as f:
        f.write(data)
    
    print(f"Patched {filename}")

# Usage
if len(sys.argv) != 2:
    print("Usage: patch_client.py <server_ip>")
    sys.exit(1)

server_ip = sys.argv[1]
patch_file('launcher.exe', 'testauth.mxoemu.info', server_ip)
patch_file('matrix.exe', 'testauth.mxoemu.info', server_ip)
```

## Method 3: DNS Redirect

### Local Hosts File

Edit `C:\Windows\System32\drivers\etc\hosts`:

```
# Add these lines
192.168.1.100 mxo.station.sony.com
192.168.1.100 mxo-login.station.sony.com
192.168.1.100 patch.mxoemu.info
192.168.1.100 testauth.mxoemu.info
```

**Note**: Requires administrator access and may need DNS cache flush:
```batch
ipconfig /flushdns
```

### Using DNSMasq (Advanced)

For network-wide redirection:

```bash
# dnsmasq.conf
address=/mxoemu.info/192.168.1.100
address=/station.sony.com/192.168.1.100
```

## Method 4: Proxy Method

### Using Proxifier or Similar

1. Install Proxifier or similar proxy software
2. Create rules for Matrix Online executables
3. Redirect traffic to your server
4. No file modification needed

### Configuration Example

```xml
<ProxifierProfile>
  <Rule>
    <Name>Matrix Online</Name>
    <Applications>launcher.exe;matrix.exe</Applications>
    <Action>Direct</Action>
    <RemoteHost>your.server.ip:10000</RemoteHost>
  </Rule>
</ProxifierProfile>
```

## Verification

### Check Your Patch

1. Open patched file in hex editor
2. Search for old server addresses
3. Ensure all instances are replaced
4. Check file size hasn't changed

### Test Connection

```batch
# Test network connectivity
ping your.server.ip
telnet your.server.ip 11000

# Check if launcher connects
launcher.exe -debug
```

## Troubleshooting

### Common Issues

**"Unable to connect to server"**
- Verify server IP is correct
- Check firewall settings
- Ensure server is running

**"Version mismatch"**
- Client version doesn't match server
- Try different client version
- Check server compatibility

**Crash on startup**
- Patching error - restore backup
- Missing dependencies
- Incompatible client version

### Debug Mode

Enable debug logging:

1. Create `debug.ini` in game directory:
```ini
[Debug]
NetworkLogging=1
PacketDump=1
Verbose=1
```

2. Check `debug.log` for connection attempts

## Advanced Patching

### Custom Launcher

Create replacement launcher that handles patching:

```cpp
// Simple launcher replacement
#include <windows.h>
#include <string>

int main() {
    // Set environment variable for server
    SetEnvironmentVariable("MXO_SERVER", "192.168.1.100");
    
    // Launch matrix.exe with parameters
    ShellExecute(NULL, "open", "matrix.exe", 
                "-server 192.168.1.100", NULL, SW_SHOW);
    
    return 0;
}
```

### Binary Patching Tools

**Using radare2:**
```bash
# Open file
r2 -w launcher.exe

# Search for string
/ testauth.mxoemu.info

# Replace at address
w 192.168.001.100 @ 0xB6194
```

**Using Binary Ninja:**
- Load executable
- Find string references
- Patch data directly
- Save modified binary

## Server-Specific Instructions

### For MXOEmu Servers

Default addresses:
- Auth: `your.ip:11000`
- World: `your.ip:10000`

### For Hardline Dreams

May use different ports:
- Check server Config.xml
- Use provided patcher when available

## Best Practices

1. **Always Backup**: Keep original files safe
2. **Document Changes**: Note what you patched
3. **Test Thoroughly**: Verify each component works
4. **Use Correct Version**: Match client to server version
5. **Security**: Only connect to trusted servers

## Alternative Solutions

### Pre-Patched Clients

Some servers provide pre-patched clients:
- Easier for players
- No technical knowledge needed
- May include additional fixes

### Web Launcher

Modern approach using web technology:
- Downloads correct client
- Patches automatically
- Handles updates

## Legal Considerations

- Only patch clients you legally own
- Private servers for preservation/education
- Respect intellectual property
- No commercial use

---

**Need Help?** Check our [Discord](https://discord.gg/3QXTAGB9).

[← Back to Server Setup](index.md) | [Next: Database Setup →](database-setup.md)