# Matrix Online GM Commands and Server Administration Guide
**Complete Reference for Game Masters and Server Administrators**

> *"Welcome to the real world."* - Morpheus (Where administrators have god-like powers over the simulation.)

## 🛡️ Administrator Hierarchy

The Matrix Online server administration system uses a tiered permission structure that mirrors the power dynamics within the Matrix itself.

### Permission Levels
```yaml
admin_hierarchy:
  level_0_player:
    permissions: "Basic gameplay only"
    commands: []
    description: "Standard player account"
    
  level_1_helper:
    permissions: "Limited assistance commands"
    commands: ["help", "info", "whisper_assist"]
    description: "Community volunteers who can help with basic questions"
    
  level_2_moderator:
    permissions: "Chat moderation and basic discipline"
    commands: ["mute", "kick", "warn", "broadcast"]
    description: "Chat moderators and community management"
    
  level_3_gm:
    permissions: "Full game master capabilities"
    commands: ["teleport", "spawn", "modify", "event_tools"]
    description: "Game masters who run events and handle complex issues"
    
  level_4_admin:
    permissions: "Server configuration and advanced tools"
    commands: ["server_config", "database_access", "user_management"]
    description: "Technical administrators with server access"
    
  level_5_owner:
    permissions: "Complete system control"
    commands: ["all_commands", "permission_management", "server_control"]
    description: "Server owner with unrestricted access"
```

## 📜 Complete GM Command Reference

### Player Management Commands

#### Basic Player Information
```bash
# Get player information
/playerinfo <player_name>
# Returns: Level, location, faction, online time, last login

# Example output:
Player: NeoPhyte_01
Level: 35
Location: Mara Central (143, 67, 12)
Faction: Zion (Ally status)
Online Time: 4h 23m
Last Login: 2024-12-07 14:32:15
Account Status: Active
Warning Count: 0

# Get detailed player statistics
/playerstats <player_name>
# Returns: Attributes, abilities, equipment, mission progress

# Find player location
/findplayer <player_name>
# Returns: Current district and coordinates

# List online players
/who [filter]
# Options: /who all, /who zion, /who machine, /who merovingian, /who gm
```

#### Player Modification Commands
```bash
# Teleport commands
/teleport <player_name> <x> <y> <z> [district]
/teleport_to <target_player>
/teleport_here <player_name>
/teleport_all_to <location>

# Examples:
/teleport NeoPhyte_01 100 50 200 mara_central
/teleport_to Agent_Smith
/teleport_here NeoPhyte_01

# Character modification
/setlevel <player_name> <level>
/addexp <player_name> <amount>
/setattribute <player_name> <attribute> <value>
# Attributes: vitality, focus, perception, reason, belief

# Examples:
/setlevel NeoPhyte_01 50
/addexp NeoPhyte_01 50000
/setattribute NeoPhyte_01 reason 85

# Health and status
/heal <player_name> [amount]
/restore <player_name>  # Full health and IS
/cleardebuffs <player_name>
/resurrect <player_name>

# Faction management
/setfaction <player_name> <faction>
# Factions: zion, machine, merovingian, neutral

/addfactionstanding <player_name> <faction> <amount>
# Example: /addfactionstanding NeoPhyte_01 zion 100
```

#### Inventory and Items
```bash
# Item management
/giveitem <player_name> <item_id> [quantity]
/removeitem <player_name> <item_id> [quantity]
/clearinventory <player_name>

# Examples:
/giveitem NeoPhyte_01 weapon_pistol_enhanced 1
/giveitem NeoPhyte_01 consumable_health_pack 10

# Equipment commands
/equipitem <player_name> <item_id>
/unequipitem <player_name> <slot>
# Slots: weapon_primary, weapon_secondary, clothing_head, clothing_body, etc.

# Special item creation
/createitem <template_name> <custom_properties>
# Example: /createitem weapon_rifle damage=150 accuracy=95 name="Neo's Rifle"
```

### World and Environment Commands

#### Object and NPC Management
```bash
# Spawn NPCs
/spawnnpc <npc_id> <x> <y> <z> [rotation]
/spawnnpc_template <template_name> <location>

# Examples:
/spawnnpc agent_smith 100 50 200 0
/spawnnpc_template zion_guard current_location

# NPC management
/npcinfo <npc_id>
/removenpc <npc_id>
/npcfollow <npc_id> <player_name>
/npcstop <npc_id>

# Object spawning
/spawnobject <object_id> <x> <y> <z>
/removeobject <object_id>

# Examples:
/spawnobject hardline_terminal 150 60 180
/spawnobject vehicle_car_sedan 200 55 220

# Environment effects
/weather <district> <weather_type>
# Weather types: clear, rain, fog, storm, matrix_code_rain

/lighting <district> <lighting_preset>
# Presets: day, night, dawn, dusk, matrix_green, emergency_red

/ambience <district> <sound_file>
# Play ambient sound effects in specific districts
```

#### District and Server Management
```bash
# District control
/districtinfo <district_name>
/districtlist
/districtkick <district_name> <player_name>
/districtmsg <district_name> <message>

# Server-wide commands
/servermsg <message>  # Message to all players
/serverrestart <minutes> [message]
/servershutdown <minutes> [message]

# Examples:
/servermsg "Critical mission event starting in Westview in 10 minutes!"
/serverrestart 30 "Server restart for updates in 30 minutes"

# Player limits and restrictions
/setdistrictlimit <district> <max_players>
/lockdistrict <district> [reason]
/unlockdistrict <district>
```

### Event and Mission Commands

#### Mission Management
```bash
# Mission control
/startmission <player_name> <mission_id>
/completemission <player_name> <mission_id>
/failmission <player_name> <mission_id>
/clearmissions <player_name>

# Examples:
/startmission NeoPhyte_01 story_chapter_1_mission_3
/completemission NeoPhyte_01 daily_combat_training

# Mission status
/missioninfo <player_name> [mission_id]
/missionlist <player_name>

# Custom mission creation
/createmission <title> <description> <objectives> <rewards>
# This opens a detailed mission editor interface
```

#### Event Hosting Tools
```bash
# Event management
/event create <event_name> <event_type>
# Event types: combat_tournament, treasure_hunt, story_event, pvp_battle

/event start <event_name>
/event stop <event_name>
/event join <event_name> <player_name>
/event leave <event_name> <player_name>

# Event configuration
/event setlocation <event_name> <district> <x> <y> <z>
/event setrewards <event_name> <reward_list>
/event setduration <event_name> <minutes>

# Examples:
/event create "Downtown Throwdown" combat_tournament
/event setlocation "Downtown Throwdown" downtown_east 100 50 200
/event setrewards "Downtown Throwdown" "experience=5000,item=trophy_fighter"

# Special event commands
/criticalstoryevent <event_id>
# Triggers server-wide critical story events

/massiveevent <event_id> <all_districts>
# Events that span multiple districts simultaneously
```

### Communication and Moderation

#### Chat and Communication
```bash
# Messaging commands
/tell <player_name> <message>  # Private message
/broadcast <message>  # Server-wide announcement
/districtbroadcast <district> <message>
/factionbroadcast <faction> <message>

# Examples:
/broadcast "Server maintenance in 15 minutes. Please finish current activities."
/factionbroadcast zion "Zion forces, prepare for coordinated operation."

# Chat moderation
/mute <player_name> <duration_minutes> [reason]
/unmute <player_name>
/mutelist  # Show all muted players

# Examples:
/mute SpamBot_01 60 "Excessive advertising"
/mute ToxicPlayer 1440 "Harassment of other players"

# Channel management
/createchannel <channel_name> [password]
/deletechannel <channel_name>
/channelmod <channel_name> <player_name>
```

#### Disciplinary Actions
```bash
# Warning system
/warn <player_name> <reason>
/warnings <player_name>  # Show warning history
/clearwarnings <player_name>

# Temporary restrictions
/jail <player_name> <duration_minutes> [reason]
/unjail <player_name>
# Jail teleports player to restricted area

/freeze <player_name> <duration_minutes> [reason]
/unfreeze <player_name>
# Freeze prevents all player actions

# Account actions
/kick <player_name> [reason]
/ban <player_name> <duration> [reason]
/unban <account_name>

# Duration formats: 30m, 2h, 7d, permanent
# Examples:
/ban GrieferAccount 7d "Repeated harassment and rule violations"
/jail TrollPlayer 120 "Disrupting events"
```

### Advanced Administration

#### Database and Character Management
```bash
# Account administration
/accountinfo <account_name>
/accounthistory <account_name>  # Login history, violations, etc.
/resetpassword <account_name>
/lockaccount <account_name> [reason]
/unlockaccount <account_name>

# Character data management
/backupcharacter <player_name>
/restorecharacter <player_name> <backup_date>
/deletecharacter <player_name> [confirmation_code]

# Database queries (Level 4+ only)
/dbquery <sql_query>
/dbbackup [backup_name]
/dbrestore <backup_name>

# Examples:
/dbquery "SELECT name, level FROM characters WHERE faction='zion' AND level > 40"
/dbbackup "pre_event_backup_20241207"
```

#### Server Configuration
```bash
# Server settings (Level 4+ only)
/config set <setting> <value>
/config get <setting>
/config list [category]

# Important settings:
/config set max_players 150
/config set experience_rate 1.5
/config set pvp_enabled true
/config set event_mode true

# Economy controls
/economystats
/adjusteconomy <setting> <value>
# Settings: item_prices, vendor_stock, drop_rates

# Examples:
/adjusteconomy drop_rates 1.2  # 20% increase in drop rates
/adjusteconomy vendor_stock 0.8  # 20% decrease in vendor stock
```

### Debugging and Testing Commands

#### Development and Testing
```bash
# Debug information
/debuginfo <player_name>
/serverstats
/performancemonitor [start|stop]

# Testing tools
/testmode <on|off>  # Enables additional testing commands
/godmode <player_name> [on|off]
/noclip <player_name> [on|off]
/invisible <player_name> [on|off]

# Network debugging
/ping <player_name>
/traceroute <player_name>
/packetinfo <player_name>

# Examples:
/godmode TestCharacter on
/invisible GMInvestigator on
```

## 🎭 Event Hosting Guide

### Creating Memorable Events

#### Story Events
```yaml
story_event_planning:
  preparation:
    - "Coordinate with storyline continuity"
    - "Prepare NPCs and dialogue"
    - "Set up locations and props"
    - "Brief assistant GMs on their roles"
    
  execution:
    - "Use dramatic timing and pacing"
    - "Respond dynamically to player actions"
    - "Maintain character consistency"
    - "Document outcomes for future events"
    
  example_commands:
    setup: |
      /event create "Oracle's Prophecy" story_event
      /spawnnpc oracle 100 50 200
      /spawnnpc seraph 95 50 195
      /lighting apartment_complex mystical_green
      
    during_event: |
      /npcspeak oracle "I've been expecting you, NeoPhyte_01"
      /event_trigger prophecy_vision_sequence
      /giveitem NeoPhyte_01 oracle_cookie 1
```

#### Combat Tournaments
```yaml
tournament_setup:
  bracket_creation:
    - "/event create 'Downtown Dojo Tournament' combat_tournament"
    - "/event setlocation 'Downtown Dojo Tournament' dojo_main_floor"
    - "/event setrewards 'Downtown Dojo Tournament' 'experience=10000,item=champion_belt'"
    
  participant_management:
    - "/event join tournament_name player_name"
    - "/event brackets tournament_name"  # Display bracket
    - "/event nextmatch tournament_name"  # Advance bracket
    
  match_control:
    - "/combatarea create arena_01 50 50 300"  # Create fighting area
    - "/combatarea rules arena_01 no_weapons no_abilities"
    - "/startmatch player1 player2 arena_01"
```

### Advanced Event Scripting
```lua
-- Example event script (events/oracle_meeting.lua)
function oracle_meeting_event(trigger_player)
    -- Check if player meets requirements
    if not player_has_item(trigger_player, "red_pill_fragment") then
        gm_message(trigger_player, "You are not ready for this meeting.")
        return false
    end
    
    -- Setup the scene
    spawn_npc("oracle", 100, 50, 200)
    spawn_npc("seraph", 95, 50, 195)
    set_lighting("apartment_complex", "mystical")
    play_ambience("oracle_apartment_sounds.wav")
    
    -- Begin dialogue sequence
    npc_speak("oracle", "I've been expecting you.")
    wait(3000)  -- 3 second pause
    
    npc_speak("oracle", "You have questions, and I have answers... some of them.")
    
    -- Give player choice
    local choice = prompt_player(trigger_player, {
        "What is my purpose in the Matrix?",
        "How can I help free humanity?", 
        "What dangers lie ahead?"
    })
    
    if choice == 1 then
        oracle_purpose_dialogue(trigger_player)
    elseif choice == 2 then
        oracle_humanity_dialogue(trigger_player)
    else
        oracle_dangers_dialogue(trigger_player)
    end
    
    -- Reward player
    give_item(trigger_player, "oracle_insight", 1)
    add_experience(trigger_player, 5000)
    
    -- Cleanup
    wait(5000)
    remove_npc("oracle")
    remove_npc("seraph")
    restore_lighting("apartment_complex")
end
```

## 🔒 Security and Best Practices

### Admin Account Security
```yaml
security_guidelines:
  account_protection:
    - "Use strong, unique passwords for admin accounts"
    - "Enable two-factor authentication if available"
    - "Regularly rotate admin passwords"
    - "Limit admin account sharing"
    
  permission_management:
    - "Follow principle of least privilege"
    - "Regular audits of admin permissions"
    - "Document all permission changes"
    - "Remove inactive admin accounts"
    
  command_logging:
    - "All admin commands are logged automatically"
    - "Regular review of admin command logs"
    - "Investigate suspicious admin activity"
    - "Backup logs to secure location"
```

### Abuse Prevention
```bash
# Command rate limiting
/ratelimit <admin_level> <commands_per_minute>
# Example: /ratelimit 3 30  # Level 3 GMs limited to 30 commands/minute

# Command restrictions
/restrict_command <command> <min_level> [time_restriction]
# Example: /restrict_command "giveitem" 3 "300"  # 5 minute cooldown

# Audit trail
/adminlog <admin_name> [date_range]
/suspiciousactivity [threshold]
# Shows potentially abusive command patterns
```

## 📊 Server Monitoring and Maintenance

### Performance Monitoring
```bash
# Server performance
/performance cpu
/performance memory
/performance network
/performance database

# Player statistics
/playerstats online
/playerstats peak_concurrent
/playerstats average_session_time
/playerstats retention_rate

# System health
/systemcheck
/errorlog [severity_level]
/crashreports [date_range]
```

### Automated Maintenance
```yaml
automated_tasks:
  daily_maintenance:
    - "Database optimization and cleanup"
    - "Log file rotation and archival"
    - "Player inactivity checks"
    - "Economy balance adjustments"
    
  weekly_maintenance:
    - "Full database backup"
    - "Security audit review"
    - "Performance analysis"
    - "Update deployment"
    
  monthly_maintenance:
    - "Deep system analysis"
    - "Admin permission review"
    - "Long-term statistics compilation"
    - "Disaster recovery testing"
```

## 📋 Quick Reference Commands

### Emergency Commands
```bash
# Emergency server control
/emergency shutdown [reason]
/emergency kickall [reason]
/emergency lockserver [reason]

# Crisis management
/emergency broadcast <critical_message>
/emergency teleport_all_to safe_zone
/emergency restore_from_backup <backup_id>

# Player assistance
/emergency revive_all
/emergency clear_all_debuffs
/emergency mass_heal
```

### Common Command Shortcuts
```bash
# Frequently used shortcuts
/tp = /teleport
/tph = /teleport_here
/tpt = /teleport_to
/gi = /giveitem
/si = /setlevel
/bc = /broadcast
/w = /warn
/k = /kick
/m = /mute
```

## Remember

> *"Choice. The problem is choice."* - Neo (And administrators must choose wisely how to use their power.)

As a Game Master or Administrator in The Matrix Online, you wield considerable power over the digital realm. This power comes with the responsibility to enhance the experience for all players while maintaining the integrity and balance of the game world.

**Great power requires great responsibility. Use these commands wisely.**

Every command executed, every player helped, every event hosted contributes to the living, breathing world that keeps The Matrix Online alive for the community.

---

**GM System Status**: 🟢 COMPREHENSIVE TOOLS  
**Administration**: PROFESSIONAL GRADE  
**Community Impact**: WORLD-SHAPING  

*Command with wisdom. Moderate with fairness. Create with passion.*

---

[← Back to Servers](index.md) | [Database Setup →](database-setup.md) | [Server Troubleshooting →](server-troubleshooting.md)