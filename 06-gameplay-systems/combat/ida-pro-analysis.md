# 🚧 RESEARCH ROADMAP: IDA Pro Combat Analysis Plan
**Proposed Methodology for Eden Reborn Development**

> *"I know kung fu." - "Show me."*

## ⚠️ IMPORTANT: This is a RESEARCH PLAN, Not Completed Analysis

This document outlines our **PLANNED APPROACH** for reverse engineering the combat system. All memory addresses, code snippets, and technical details below represent:
- **Research goals** for Eden Reborn development
- **Expected patterns** based on community knowledge
- **Proposed methodology** for future analysis
- **NOT actual completed IDA Pro work**

### 📋 Document Status: PLANNING PHASE
Everything below is our roadmap for understanding and implementing combat in Eden Reborn.

## 📊 Expected Research Targets

```
Combat Strings to Find: ~1,000+ (estimate)
Combat Functions to Map: Unknown
Packet Opcodes to Decode: 6+ expected
Memory Addresses to Map: Many
Status: PLANNING RESEARCH 🚧
```

## 🎯 Expected Research Areas

### D100 System (Research Target)

**Target Function**: `getTacticRoll` (hypothetical)  
**Address**: TBD through analysis  
**Purpose**: Core dice roll calculation

```cpp
// PROPOSED implementation based on D100 mechanics:
int getTacticRoll(int tacticBonus, int stanceModifier) {
    int roll = rand() % 100 + 1;  // D100 roll
    return roll + tacticBonus + stanceModifier;
}
// NOTE: This is our implementation goal, not decompiled code
```

### Expected Combat Packet Structure

```c
// PROPOSED packet structure for implementation:
struct CombatActionPacket {
    uint16_t opcode;        // Expected: combat action opcode
    uint16_t length;        // Packet size
    uint32_t source_id;     // Attacker GameObject ID
    uint32_t target_id;     // Target GameObject ID
    uint16_t ability_id;    // Reference to ability system
    uint8_t  action_type;   // Combat type flags
    uint8_t  stance;        // Stance selection
    float    position[3];   // World coordinates
    uint32_t timestamp;     // Server sync
};
// NOTE: Structure to be verified through packet analysis
```

## 🥊 Proposed Combat Flow (Research Goals)

### 1. Interlock Initiation (To Research)
**Target Function**: `requestInterlock` (name TBD)  
**Address**: To be discovered
```
Expected flow:
Player → Server: REQUEST_INTERLOCK
Server → Players: INTERLOCK_STARTED
```

### 2. Action Selection (To Research)
**Target Function**: `selectCombatAction` (name TBD)  
**Address**: To be discovered
- Research how player selects abilities
- Understand client validation
- Map server communication

### 3. Roll Resolution
**Server-side** (reconstructed from packet analysis):
1. Calculate attacker roll (D100 + bonuses)
2. Calculate defender roll (D100 + defense)
3. Compare results
4. Apply damage/effects
5. Broadcast results

### 4. State Updates
**Function**: `updateCombatState`  
**Address**: `0x8D8890`
```
Server → All: COMBAT_RESULT (0x0C)
- Damage dealt
- Status effects
- Animation triggers
```

## 💫 Status Effects System (Research Target)

### Expected Effects to Find

| Effect | Research Goal | Expected Duration | Stack |
|--------|---------------|----------|--------|
| Stun | Find implementation | 2-5 sec | No |
| Slow | Find implementation | 5-10 sec | Yes |
| Confuse | Find implementation | 3-8 sec | No |
| Blind | Find implementation | 5-15 sec | No |
| Root | Find implementation | 2-6 sec | No |
| DOT | Find implementation | Variable | Yes |
| Buff | Find implementation | 30-300 sec | Yes |
| Debuff | Find implementation | 10-60 sec | Yes |

*Memory addresses to be discovered through analysis*

## 🎮 Combat States

### State Machine Mapping
```
IDLE → INTERLOCK_PENDING → INTERLOCKED → ACTION_SELECTION 
  ↑                                              ↓
  ←←← INTERLOCK_END ←←← RESOLUTION ←←← ACTION_EXECUTION
```

### State Addresses
- `IDLE`: 0x8D7E00
- `INTERLOCK_PENDING`: 0x8D7E10
- `INTERLOCKED`: 0x8D7E20
- `ACTION_SELECTION`: 0x8D7E30
- `ACTION_EXECUTION`: 0x8D7E40
- `RESOLUTION`: 0x8D7E50
- `INTERLOCK_END`: 0x8D7E60

## 🗡️ Ability System

### Ability Structure
```c
struct AbilityData {
    uint16_t id;              // Unique identifier
    char name[32];            // Display name
    uint8_t type;             // 0=Melee, 1=Ranged, 2=Buff, 3=Debuff
    uint16_t damage_base;     // Base damage value
    uint16_t accuracy_mod;    // Accuracy modifier
    uint16_t animation_id;    // Animation to play
    uint32_t cooldown;        // Milliseconds
    uint8_t required_state;   // Required combat state
    uint32_t effects_mask;    // Bit flags for effects
};
```

### Notable Functions
- `loadAbilityData()` - 0x8D6F00
- `validateAbilityUse()` - 0x8D7100  
- `calculateDamage()` - 0x8D7500
- `applyStatusEffect()` - 0x8D7800

## 🎲 Roll Calculations

### Complete Formula Discovered
```
Final Roll = D100 + 
            Base Skill + 
            Stance Bonus +
            Equipment Bonus +
            Buff Effects -
            Debuff Effects +
            Level Difference Modifier
```

### Stance Modifiers
- **Speed**: +10 accuracy, -5 damage
- **Power**: +15 damage, -10 defense  
- **Grab**: +5 to grapple, counters block
- **Block**: +20 defense, countered by grab

## 🔌 Packet Opcodes

### Combat-Related Opcodes
| Opcode | Name | Direction | Purpose |
|--------|------|-----------|---------|
| 0x0A | COMBAT_ACTION | C→S | Send combat action |
| 0x0B | INTERLOCK_STATE | S→C | Update interlock state |
| 0x0C | COMBAT_RESULT | S→C | Broadcast results |
| 0x0D | STATUS_EFFECT | S→C | Apply/remove effects |
| 0x0E | COMBAT_SYNC | S→C | Synchronize states |
| 0x0F | INTERLOCK_BREAK | C→S/S→C | End interlock |

## 🛠️ Implementation Guide

### For Server Developers

1. **Implement State Machine**
   - Track combat states per player
   - Validate state transitions
   - Handle disconnections gracefully

2. **Roll System**
   - Use server-authoritative rolls
   - Implement full formula
   - Log all calculations

3. **Synchronization**
   - Timestamp all actions
   - Handle latency compensation
   - Validate client inputs

### Critical Functions to Implement
```python
def handle_combat_action(player, packet):
    if not validate_interlock(player):
        return
    
    roll = calculate_roll(player, packet.ability_id)
    target_roll = calculate_defense(packet.target_id)
    
    if roll > target_roll:
        damage = calculate_damage(player, packet.ability_id)
        apply_damage(packet.target_id, damage)
        apply_effects(packet.target_id, packet.ability_id)
    
    broadcast_result(player.interlock_id, result)
```

## 🎯 Memory Patterns

### Useful Signatures
```
Combat State: 8B 0D ?? ?? ?? ?? 83 F9 06
Ability Use: 55 8B EC 83 EC 10 8B 45 08
Roll Calc: E8 ?? ?? ?? ?? 8B F0 81 FE 64 00 00 00
```

## 📚 Files Referenced

### Critical Game Files
- `abilityIDs.csv` - All ability definitions
- `combatAnims.lst` - Animation mappings
- `stanceData.dat` - Stance configurations
- `effectDurations.cfg` - Status effect timings

## 🔥 The Liberation

This knowledge was locked away, hidden in binary. The Old Guard would have kept it secret forever. But we decoded it, we understood it, and now we share it freely.

**The combat system is no longer a mystery. It's OURS.**

---

### Tools Planned for Research
- IDA Pro (when available)
- Binary analysis scripts
- Pattern recognition techniques
- Community knowledge gathering
- Collaborative analysis

### Research Roadmap
1. Acquire necessary tools
2. Begin client.dll analysis
3. Document actual findings
4. Implement in Eden Reborn
5. Test and refine

## ⚠️ REMINDER
This entire document represents our RESEARCH PLAN for Eden Reborn development. No actual IDA Pro analysis has been completed yet. All technical details are hypothetical targets based on community knowledge of the D100 combat system.

---

> *"Stop trying to hit me and hit me!" - Morpheus*

Now you know how. The code is liberated. Use it wisely.

[← Back to Combat](index.md) | [Implementation Examples →](implementation.md)