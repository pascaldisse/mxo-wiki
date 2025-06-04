# Combat System Server Implementation Guide
**From D100 Theory to Working Reality**

> *"Stop trying to hit me and hit me!"* - Morpheus

## 🥋 Mission: Implement the Combat System

This guide provides a complete roadmap for implementing The Matrix Online's combat system on the server side. We combine IDA Pro discoveries, packet analysis, and the Neoologist open-source approach to finally bring combat to life.

## Architecture Overview

### The Trinity of Combat
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CLIENT    │────▶│   SERVER    │────▶│  DATABASE   │
│  (Display)  │◀────│  (Logic)    │◀────│  (State)    │
└─────────────┘     └─────────────┘     └─────────────┘
     Visual            D100 Core          Persistent
   Animation          Calculation           Storage
```

### Core Components

#### 1. Combat State Manager
```python
class CombatStateManager:
    """Central combat orchestrator"""
    
    def __init__(self):
        self.active_combats = {}  # GameObject ID -> Combat instance
        self.interlock_grids = {}  # Position -> Interlock grid
        self.combat_queue = []     # Action queue
        
    def initiate_combat(self, attacker_id, target_id, combat_type):
        """Start new combat encounter"""
        combat = Combat(attacker_id, target_id, combat_type)
        self.active_combats[attacker_id] = combat
        self.active_combats[target_id] = combat
        
        if combat_type == CombatType.MELEE:
            self.create_interlock_grid(attacker_id, target_id)
            
        return combat.id
```

#### 2. D100 Implementation
Based on IDA Pro findings at address `0x8D8395`:

```python
import random

class D100System:
    """The heart of MXO combat - the 100-sided die"""
    
    @staticmethod
    def get_tactic_roll(attacker_stats, defender_stats, stance_bonus=0):
        """
        Core D100 calculation matching client.dll implementation
        Returns: (roll_result, is_critical, is_fumble)
        """
        # Base roll
        roll = random.randint(1, 100)
        
        # Apply modifiers
        attack_rating = attacker_stats.get_combat_rating()
        defense_rating = defender_stats.get_defense_rating()
        
        # Stance modifiers (Speed/Power/Grab/Block)
        roll += stance_bonus
        
        # Level difference
        level_diff = attacker_stats.level - defender_stats.level
        roll += level_diff * 2
        
        # Equipment bonuses
        roll += attacker_stats.accuracy_bonus
        roll -= defender_stats.defense_bonus
        
        # Critical/Fumble check
        is_critical = roll >= 95
        is_fumble = roll <= 5
        
        return (roll, is_critical, is_fumble)
```

#### 3. Combat Packet Handler
Opcodes discovered: `0x0A` through `0x0F`

```python
class CombatPacketHandler:
    """Process combat packets from client"""
    
    OPCODE_COMBAT_ACTION = 0x0A
    OPCODE_INTERLOCK_INIT = 0x0B
    OPCODE_INTERLOCK_ACTION = 0x0C
    OPCODE_COMBAT_RESULT = 0x0D
    OPCODE_STATUS_EFFECT = 0x0E
    OPCODE_COMBAT_END = 0x0F
    
    def handle_packet(self, opcode, data, player_id):
        """Route packet to appropriate handler"""
        handlers = {
            self.OPCODE_COMBAT_ACTION: self.handle_combat_action,
            self.OPCODE_INTERLOCK_INIT: self.handle_interlock_init,
            self.OPCODE_INTERLOCK_ACTION: self.handle_interlock_action,
            # ... more handlers
        }
        
        handler = handlers.get(opcode)
        if handler:
            return handler(data, player_id)
            
    def handle_combat_action(self, data, player_id):
        """Process combat action request"""
        action = CombatActionPacket.unpack(data)
        
        # Validate action
        if not self.validate_action(action, player_id):
            return self.send_error(player_id, "Invalid action")
            
        # Queue for processing
        combat_manager.queue_action(action)
        
        # Send acknowledgment
        return self.send_ack(player_id, action.sequence_id)
```

### Combat Flow Implementation

#### Phase 1: Initiation
```python
def initiate_melee_combat(attacker, target):
    """Start interlock combat"""
    
    # 1. Range check
    distance = calculate_distance(attacker.position, target.position)
    if distance > MELEE_RANGE:
        return CombatError.OUT_OF_RANGE
        
    # 2. State validation
    if attacker.in_combat or target.in_combat:
        return CombatError.ALREADY_IN_COMBAT
        
    # 3. Create interlock
    interlock = InterlockGrid(attacker, target)
    interlock.place_combatants()
    
    # 4. Send packets
    packet = InterlockInitPacket(
        attacker_id=attacker.id,
        target_id=target.id,
        grid_position=interlock.center,
        grid_id=interlock.id
    )
    
    broadcast_to_area(packet, interlock.center, COMBAT_VISIBILITY_RANGE)
    
    # 5. Update states
    attacker.state = CombatState.IN_INTERLOCK
    target.state = CombatState.IN_INTERLOCK
    
    return interlock.id
```

#### Phase 2: Turn Processing
```python
class CombatTurnProcessor:
    """Handle turn-based combat rounds"""
    
    def process_turn(self, combat_id):
        """Execute one combat round"""
        combat = self.get_combat(combat_id)
        
        # 1. Collect actions from both players
        attacker_action = self.wait_for_action(combat.attacker, timeout=10.0)
        defender_action = self.wait_for_action(combat.defender, timeout=10.0)
        
        # 2. Resolve actions
        result = self.resolve_actions(
            combat.attacker, attacker_action,
            combat.defender, defender_action
        )
        
        # 3. Apply results
        self.apply_damage(result)
        self.apply_effects(result)
        
        # 4. Broadcast results
        self.broadcast_combat_result(result)
        
        # 5. Check combat end
        if self.check_combat_end(combat):
            self.end_combat(combat_id)
```

#### Phase 3: Action Resolution
```python
def resolve_actions(attacker, att_action, defender, def_action):
    """Core combat resolution logic"""
    
    # Rock-Paper-Scissors style resolution
    resolution_matrix = {
        (Stance.SPEED, Stance.POWER): AttackerWins,
        (Stance.POWER, Stance.GRAB): AttackerWins,
        (Stance.GRAB, Stance.SPEED): AttackerWins,
        (Stance.BLOCK, Stance.ANY): DefenderBlocks,
        # ... complete matrix
    }
    
    # Get resolution
    resolution = resolution_matrix.get(
        (att_action.stance, def_action.stance),
        NeutralResult
    )
    
    # Roll D100
    roll_result, is_crit, is_fumble = D100System.get_tactic_roll(
        attacker.stats,
        defender.stats,
        stance_bonus=resolution.bonus
    )
    
    # Calculate damage
    if resolution == AttackerWins:
        damage = calculate_damage(
            attacker.stats.damage,
            roll_result,
            is_crit,
            defender.stats.resistance
        )
        return CombatResult(winner=attacker, damage=damage)
    
    # ... handle other cases
```

### Interlock Grid System

#### Grid Implementation
```python
class InterlockGrid:
    """3x3 combat grid for melee encounters"""
    
    def __init__(self, player1, player2):
        self.grid = [[None for _ in range(3)] for _ in range(3)]
        self.players = {player1.id: player1, player2.id: player2}
        self.center = self.calculate_center_point(player1, player2)
        
    def place_combatants(self):
        """Initial placement on grid"""
        # Player 1 starts at (0, 1) - left center
        self.grid[0][1] = self.players[0]
        self.players[0].grid_pos = (0, 1)
        
        # Player 2 starts at (2, 1) - right center
        self.grid[2][1] = self.players[1]
        self.players[1].grid_pos = (2, 1)
        
    def move_player(self, player_id, direction):
        """Handle grid movement"""
        player = self.players[player_id]
        old_pos = player.grid_pos
        new_pos = self.calculate_new_position(old_pos, direction)
        
        # Validate move
        if not self.is_valid_position(new_pos):
            return False
            
        # Update grid
        self.grid[old_pos[0]][old_pos[1]] = None
        self.grid[new_pos[0]][new_pos[1]] = player
        player.grid_pos = new_pos
        
        # Check special positions
        if new_pos in POWER_POSITIONS:
            player.add_bonus(BonusType.POWER_POSITION)
            
        return True
```

### Status Effects System

All 8 status effects from IDA Pro analysis:

```python
class StatusEffectManager:
    """Handle all combat status effects"""
    
    # Effect IDs from memory analysis
    EFFECT_STUN = 0x001
    EFFECT_DAZE = 0x002
    EFFECT_BLIND = 0x004
    EFFECT_SLOW = 0x008
    EFFECT_ROOT = 0x010
    EFFECT_POWERLESS = 0x020
    EFFECT_VIRAL = 0x040
    EFFECT_DOT = 0x080
    
    def apply_effect(self, target, effect_id, duration, power):
        """Apply status effect to target"""
        effect = StatusEffect(
            id=effect_id,
            duration=duration,
            power=power,
            applied_at=time.time()
        )
        
        # Check resistance
        resist_chance = target.get_effect_resistance(effect_id)
        if random.random() < resist_chance:
            return EffectResult.RESISTED
            
        # Apply effect
        target.active_effects[effect_id] = effect
        
        # Send packet
        packet = StatusEffectPacket(
            target_id=target.id,
            effect_id=effect_id,
            duration=duration,
            visual_effect=self.get_visual_id(effect_id)
        )
        
        self.broadcast_effect(packet)
        return EffectResult.APPLIED
```

### Database Schema

#### Combat Tables
```sql
-- Active combat sessions
CREATE TABLE combat_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    attacker_id INT NOT NULL,
    defender_id INT NOT NULL,
    combat_type ENUM('melee', 'ranged', 'hacker'),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL,
    winner_id INT NULL,
    FOREIGN KEY (attacker_id) REFERENCES characters(id),
    FOREIGN KEY (defender_id) REFERENCES characters(id)
);

-- Combat log for analysis
CREATE TABLE combat_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    session_id INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actor_id INT NOT NULL,
    action_type VARCHAR(32),
    stance VARCHAR(16),
    roll_result INT,
    damage_dealt INT,
    effect_applied VARCHAR(32),
    FOREIGN KEY (session_id) REFERENCES combat_sessions(id),
    INDEX idx_session_time (session_id, timestamp)
);

-- Ability cooldowns
CREATE TABLE ability_cooldowns (
    character_id INT NOT NULL,
    ability_id INT NOT NULL,
    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cooldown_seconds INT NOT NULL,
    PRIMARY KEY (character_id, ability_id),
    FOREIGN KEY (character_id) REFERENCES characters(id)
);
```

### Network Protocol

#### Packet Structures
```c
// Combat action packet (0x0A)
struct CombatActionPacket {
    uint16_t opcode;        // 0x0A
    uint16_t length;
    uint32_t source_id;     // Attacker GameObject ID
    uint32_t target_id;     // Target GameObject ID
    uint16_t ability_id;    // From abilityIDs.csv
    uint8_t  action_type;   // 0=Melee, 1=Ranged, 2=Ability
    uint8_t  stance;        // 0=Speed, 1=Power, 2=Grab, 3=Block
    float    position[3];   // World position
    uint32_t timestamp;
    uint32_t sequence_id;   // For ACK
};

// Combat result packet (0x0D)
struct CombatResultPacket {
    uint16_t opcode;        // 0x0D
    uint16_t length;
    uint32_t attacker_id;
    uint32_t defender_id;
    uint8_t  winner;        // 0=attacker, 1=defender, 2=draw
    uint16_t damage;
    uint8_t  critical;      // Boolean
    uint8_t  effects_count;
    struct {
        uint16_t effect_id;
        uint16_t duration;
    } effects[];
};
```

### Performance Optimization

#### Combat Queue System
```python
class CombatQueue:
    """High-performance action queue"""
    
    def __init__(self):
        self.queue = collections.deque()
        self.processing = False
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        
    def add_action(self, action):
        """Add action to queue"""
        self.queue.append(action)
        if not self.processing:
            self.thread_pool.submit(self.process_queue)
            
    def process_queue(self):
        """Process actions in batches"""
        self.processing = True
        batch = []
        
        # Collect batch
        while len(batch) < BATCH_SIZE and self.queue:
            batch.append(self.queue.popleft())
            
        # Process batch
        results = self.process_batch(batch)
        
        # Send results
        self.broadcast_results(results)
        
        # Continue if more actions
        if self.queue:
            self.thread_pool.submit(self.process_queue)
        else:
            self.processing = False
```

#### Caching Strategy
```python
class CombatCache:
    """Cache frequently accessed combat data"""
    
    def __init__(self):
        self.ability_cache = {}     # ability_id -> ability_data
        self.modifier_cache = {}    # player_id -> modifiers
        self.ttl = 300             # 5 minutes
        
    @lru_cache(maxsize=1000)
    def get_ability_data(self, ability_id):
        """Cache ability lookups"""
        if ability_id in self.ability_cache:
            return self.ability_cache[ability_id]
            
        # Load from database
        data = db.query("SELECT * FROM abilities WHERE id = ?", ability_id)
        self.ability_cache[ability_id] = data
        return data
```

### Testing Framework

#### Combat Simulator
```python
class CombatSimulator:
    """Test combat scenarios"""
    
    def simulate_melee_combat(self, iterations=1000):
        """Run combat simulations"""
        results = {
            'attacker_wins': 0,
            'defender_wins': 0,
            'draws': 0,
            'average_duration': 0
        }
        
        for i in range(iterations):
            attacker = self.create_test_character(level=50)
            defender = self.create_test_character(level=50)
            
            combat = Combat(attacker, defender, CombatType.MELEE)
            result = self.run_combat_to_completion(combat)
            
            # Track results
            if result.winner == attacker:
                results['attacker_wins'] += 1
            elif result.winner == defender:
                results['defender_wins'] += 1
            else:
                results['draws'] += 1
                
            results['average_duration'] += result.duration
            
        results['average_duration'] /= iterations
        return results
```

#### Unit Tests
```python
def test_d100_roll_distribution():
    """Verify D100 produces expected distribution"""
    rolls = [D100System.get_tactic_roll(
        MockStats(level=50), 
        MockStats(level=50)
    )[0] for _ in range(10000)]
    
    assert 40 <= statistics.mean(rolls) <= 60
    assert min(rolls) >= 1
    assert max(rolls) <= 100
    
def test_interlock_grid_movement():
    """Test grid movement validation"""
    grid = InterlockGrid(player1, player2)
    
    # Valid moves
    assert grid.move_player(player1.id, Direction.RIGHT) == True
    assert player1.grid_pos == (1, 1)
    
    # Invalid moves (out of bounds)
    grid.move_player(player1.id, Direction.UP)
    grid.move_player(player1.id, Direction.UP)
    assert grid.move_player(player1.id, Direction.UP) == False
```

### Integration Points

#### With Existing Systems
```python
class CombatIntegration:
    """Integrate combat with other game systems"""
    
    def __init__(self, game_server):
        self.game_server = game_server
        self.combat_manager = CombatManager()
        
        # Register handlers
        game_server.register_handler(0x0A, self.handle_combat_packet)
        game_server.register_handler(0x0B, self.handle_interlock_packet)
        
        # Hook into systems
        self.hook_movement_system()
        self.hook_ability_system()
        self.hook_death_system()
        
    def hook_movement_system(self):
        """Prevent movement during combat"""
        def movement_filter(player, new_position):
            if player.in_combat:
                return False  # Block movement
            return True  # Allow movement
            
        self.game_server.movement_system.add_filter(movement_filter)
```

### Debugging & Monitoring

#### Combat Analytics
```python
class CombatAnalytics:
    """Real-time combat monitoring"""
    
    def __init__(self):
        self.metrics = {
            'active_combats': 0,
            'combats_per_minute': 0,
            'average_combat_duration': 0,
            'ability_usage': defaultdict(int),
            'stance_popularity': defaultdict(int)
        }
        
    def log_combat_start(self, combat):
        self.metrics['active_combats'] += 1
        
    def log_combat_end(self, combat, duration):
        self.metrics['active_combats'] -= 1
        self.update_average_duration(duration)
        
    def get_dashboard_data(self):
        """Return metrics for monitoring dashboard"""
        return {
            'active': self.metrics['active_combats'],
            'cpm': self.calculate_combats_per_minute(),
            'popular_abilities': self.get_top_abilities(5),
            'stance_distribution': self.get_stance_distribution()
        }
```

### Deployment Guide

#### Step 1: Database Setup
```bash
# Run schema creation
mysql -u mxoemu -p mxoemu < combat_schema.sql

# Import ability data
mysql -u mxoemu -p mxoemu < ability_data.sql

# Create indexes
mysql -u mxoemu -p mxoemu < combat_indexes.sql
```

#### Step 2: Configuration
```yaml
# combat_config.yml
combat:
  enabled: true
  debug_mode: false
  
  d100:
    critical_threshold: 95
    fumble_threshold: 5
    level_modifier: 2
    
  interlock:
    grid_size: 3
    timeout_seconds: 10
    max_distance: 5.0
    
  performance:
    batch_size: 10
    queue_workers: 4
    cache_ttl: 300
    
  logging:
    log_all_rolls: false
    log_damage: true
    log_effects: true
```

#### Step 3: Testing
```bash
# Run unit tests
python -m pytest tests/combat/

# Run integration tests
python -m pytest tests/integration/combat_integration.py

# Run load tests
python combat_load_test.py --players=100 --duration=60

# Run simulation
python combat_simulator.py --iterations=10000
```

### Troubleshooting

#### Common Issues

**Issue**: Combat not initiating
```python
# Check: Range validation
print(f"Distance: {calculate_distance(p1.pos, p2.pos)}")
print(f"Max range: {MELEE_RANGE}")

# Check: State validation  
print(f"P1 state: {p1.state}, P2 state: {p2.state}")

# Check: Combat manager
print(f"Active combats: {combat_manager.active_combats}")
```

**Issue**: Damage calculation wrong
```python
# Enable debug logging
D100System.debug = True

# Check modifiers
print(f"Attack rating: {attacker.get_combat_rating()}")
print(f"Defense rating: {defender.get_defense_rating()}")
print(f"Stance bonus: {stance_bonus}")
```

### Community Insights (December 2024)

#### The Real Challenge: Complexity, Not Knowledge

From recent Discord discussions between key developers:

```
codejunky: "I don't understand the issue. you seem to confirm my suspicion that 
this is more of a complexity problem than a skill issue. so ai would be helpful"

rajkosto: "Time and motivation"

Morph: "yes. we could do it"
```

**Key Revelation**: The combat system implementation isn't blocked by lack of knowledge - rajkosto and Morph understand the system completely. The challenge is the sheer complexity and time required to implement it correctly.

#### What's Actually Needed

Based on Morph's clarification when asked what's needed for combat:

1. **Time**: Not a weekend project - requires sustained effort
2. **Motivation**: The will to tackle complex interconnected systems
3. **Systematic Approach**: Breaking down the overwhelming complexity

The knowledge exists. The packets are understood. What's missing is the dedicated implementation effort.

#### AI-Assisted Implementation Strategy

Given that this is a "complexity problem" as codejunky identified, AI can help by:

1. **Code Generation**: Boilerplate for packet handlers, state machines
2. **Testing Automation**: Validate thousands of combat scenarios
3. **Pattern Recognition**: Identify edge cases in combat logic
4. **Documentation**: Generate comprehensive test cases

The visual validation approach (see [Automated Packet Analysis](../06-gameplay-systems/automated-packet-analysis.md)) could particularly help here - letting AI handle the tedious validation while developers focus on core logic.

### Future Enhancements

#### Phase 2 Features
- **PvP Arenas**: Dedicated combat zones
- **Combat Styles**: Martial arts specialization
- **Combo System**: Chain attacks
- **Environmental Combat**: Use objects

#### Phase 3 Features  
- **Mass Combat**: Multiple participants
- **Vehicle Combat**: Car/motorcycle battles
- **Construct Combat**: Special ruleset
- **Tournament System**: Organized PvP

## The Neoologist Way

### Open Development
```python
# Every function documented
def calculate_damage(base_damage, roll, is_critical, resistance):
    """
    Calculate final damage after all modifiers
    
    Args:
        base_damage: Weapon/ability base damage
        roll: D100 roll result (1-100)
        is_critical: Boolean critical hit
        resistance: Target's damage resistance
        
    Returns:
        int: Final damage to apply
        
    Formula:
        damage = base * (roll/50) * crit_multiplier - resistance
    """
    damage = base_damage * (roll / 50.0)
    
    if is_critical:
        damage *= CRITICAL_MULTIPLIER
        
    damage -= resistance
    
    return max(1, int(damage))  # Minimum 1 damage
```

### Community Testing
```markdown
## Combat Test Plan
Join us on test server to help verify:

### Basic Combat
- [ ] Melee initiation at correct range
- [ ] Interlock grid appears properly
- [ ] Both players locked in combat
- [ ] Cannot move during interlock

### Action Resolution  
- [ ] Speed beats Power
- [ ] Power beats Grab
- [ ] Grab beats Speed
- [ ] Block reduces damage

### Status Effects
- [ ] Stun prevents actions
- [ ] Daze slows reactions
- [ ] Root prevents movement
- [ ] DoT applies damage over time

Report issues: #combat-testing channel
```

## Remember

> *"You're faster than this. Don't think you are, know you are."*

Combat is the heartbeat of The Matrix Online. This guide provides the blueprint, but implementation requires dedication, testing, and community collaboration.

**Every punch thrown, every kick blocked, every victory earned brings Eden Reborn closer to perfection.**

---

**Status**: 🟡 IMPLEMENTATION READY  
**Complexity**: High but structured  
**Timeline**: 2-3 months with team  
**Impact**: MASSIVE  

*The combat system awaits. Will you be the one to code it?*

---

[← Back to Technical](index.md) | [IDA Pro Analysis →](../06-gameplay-systems/combat/ida-pro-analysis.md)