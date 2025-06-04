# Game Master Commands Reference
**Server Administration Toolkit**

> *"With great power comes great responsibility."* - The commands to shape the Matrix.

## Overview

Complete reference for Game Master (GM) commands available in Matrix Online emulators. These commands provide administrative control over server operations, player management, and world state.

## Command Categories

### Player Management
```bash
# Player Information
/player info <name>          # Display player details
/player stats <name>         # Show character statistics
/player location <name>      # Get player coordinates
/player online               # List all online players

# Player Moderation
/kick <player> [reason]      # Disconnect player
/ban <player> [duration]     # Ban player account
/unban <player>              # Remove player ban
/mute <player> [duration]    # Silence player chat
/unmute <player>             # Restore chat privileges
```

### World Manipulation
```bash
# Teleportation
/teleport <x> <y> <z>        # Move to coordinates
/goto <player>               # Teleport to player
/summon <player>             # Bring player to you
/return                      # Return to previous location

# World State
/weather <type>              # Change weather effects
/time <hour>                 # Set world time
/spawn <npc_id> [count]      # Spawn NPCs
/despawn <target_id>         # Remove spawned entities
```

### Combat & Stats
```bash
# Character Modification
/setlevel <player> <level>   # Change player level
/sethealth <player> <hp>     # Modify health points
/setinfo <player> <inf>      # Set information stat
/addxp <player> <amount>     # Grant experience points
/addcash <player> <amount>   # Give player money

# Combat Control
/god [player]                # Toggle invincibility
/noclip [player]             # Toggle collision
/invisible [player]          # Toggle visibility
/speed <player> <multiplier> # Modify movement speed
```

### Item Management
```bash
# Item Creation
/createitem <item_id>        # Create item in inventory
/giveitem <player> <item_id> # Give item to player
/removeitem <player> <item_id> # Remove item from player
/clearinventory <player>     # Empty player inventory

# Equipment
/equip <player> <slot> <item> # Force equip item
/unequip <player> <slot>     # Remove equipped item
/repair <player> [slot]      # Repair equipment
```

## Server-Specific Commands

### MXOEmu Server
```bash
# Database Operations
/savechar <player>           # Force character save
/loadchar <player>           # Reload character data
/resetchar <player>          # Reset character to defaults

# World Events
/event start <event_id>      # Trigger server event
/event stop <event_id>       # End active event
/broadcast <message>         # Server-wide announcement
```

### Hardline Dreams
```bash
# Zone Management
/zone info                   # Display zone information
/zone reload                 # Refresh zone data
/zone list                   # Show available zones
/changezone <zone_id>        # Switch to different zone

# System Control
/shutdown [delay]            # Graceful server shutdown
/restart [delay]             # Restart server process
/maintenance [on|off]        # Toggle maintenance mode
```

## Command Usage Guidelines

### Permission Levels
```yaml
Admin (Level 5):
  - Full command access
  - Server control commands
  - Database operations
  - Player account management

Senior GM (Level 4):
  - Player moderation
  - World manipulation
  - Event control
  - Advanced debugging

Junior GM (Level 3):
  - Basic player help
  - Limited teleportation
  - Item assistance
  - Chat moderation

Helper (Level 2):
  - Information commands
  - Player assistance
  - Basic troubleshooting
```

### Best Practices

#### Do:
- ✅ Always announce major world changes
- ✅ Keep detailed logs of administrative actions
- ✅ Use minimum permissions necessary
- ✅ Verify player consent for major modifications
- ✅ Document reasons for disciplinary actions

#### Don't:
- ❌ Use admin powers for personal advantage
- ❌ Modify players without permission
- ❌ Share admin commands with regular players
- ❌ Use commands during roleplay events
- ❌ Abuse teleportation for normal gameplay

## Troubleshooting

### Common Issues
```bash
# Command not recognized
- Check spelling and syntax
- Verify permission level
- Ensure target player is online

# Database sync problems
/savechar <player>           # Force save first
/reloadchar <player>         # Then reload

# Stuck players
/teleport 0 0 0             # Emergency teleport to spawn
/unstick <player>            # Server-specific unstick command
```

### Emergency Procedures
```bash
# Server Crisis Response
1. /maintenance on           # Enable maintenance mode
2. /broadcast "Emergency maintenance - all players please log out"
3. /kick all                 # Disconnect all players
4. Address the issue
5. /maintenance off          # Resume normal operations
```

## Command Aliases

### Common Shortcuts
```bash
/tp = /teleport
/tele = /teleport
/go = /goto
/bring = /summon
/heal = /sethealth 100
/kill = /sethealth 0
/hide = /invisible
/fly = /noclip
/god = /god
/money = /addcash
```

## Server Configuration

### Command Permissions Setup
```ini
# commands.cfg
[Permissions]
Admin=5
SeniorGM=4
JuniorGM=3
Helper=2
Player=1

[Commands]
teleport=3
kick=4
ban=5
setlevel=4
createitem=3
```

### Logging Configuration
```ini
# logging.cfg
[GMCommands]
LogFile=gm_commands.log
LogLevel=INFO
IncludeTimestamp=true
IncludePlayerInfo=true
```

## Security Considerations

### Account Protection
- Regular password changes for admin accounts
- Two-factor authentication where supported
- Limited command access based on role
- Regular audit of command usage logs

### Server Security
- Restrict command console access
- Monitor for command abuse
- Regular backup before major changes
- Separate admin and player databases

## Training Resources

### New GM Orientation
1. **Read server rules and policies**
2. **Practice commands on test server**
3. **Shadow experienced GMs**
4. **Start with helper role privileges**
5. **Graduate to higher permissions gradually**

### Ongoing Education
- Monthly GM meetings
- Command reference updates
- Server feature training
- Player interaction workshops

## Command Scripts

### Automated Routines
```bash
# Daily maintenance script
#!/bin/bash
/broadcast "Daily maintenance in 5 minutes"
sleep 300
/savechar all
/maintenance on
# Perform maintenance tasks
/maintenance off
/broadcast "Maintenance complete - welcome back!"
```

### Event Management
```bash
# Event startup
/zone reload
/event prepare <event_id>
/broadcast "Event starting in 10 minutes - zone: <location>"
/event start <event_id>

# Event cleanup
/event stop <event_id>
/despawn all_event_npcs
/zone reset
/broadcast "Event concluded - thank you for participating!"
```

## Appendices

### A. Complete Command List
*[Comprehensive alphabetical listing of all available commands with syntax and permission requirements]*

### B. Item ID Reference
*[Database of all item IDs for use with item creation commands]*

### C. Zone and Location Codes
*[Reference for teleportation coordinates and zone identifiers]*

### D. NPC ID Database
*[Spawnable NPC identifiers and their functions]*

---

**Remember**: With great admin power comes great responsibility. Use these commands to enhance player experience, maintain server stability, and preserve the integrity of the Matrix Online world.

*The power to reshape reality lies in your hands. Use it wisely.*

---

[← Back to Server Setup](index.md) | [Database Setup →](database-setup.md) | [Sources →](../sources/02-server-setup/gm-commands-sources.md)