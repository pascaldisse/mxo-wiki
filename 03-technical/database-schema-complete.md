# Matrix Online Complete Database Schema Documentation
**Comprehensive Database Design for All Game Systems**

> *"What is real? How do you define 'real'?"* - Morpheus (And databases make the virtual world persistently real.)

## 🗄️ Database Architecture Overview

The Matrix Online database system uses a relational MySQL/MariaDB architecture with optimized schemas for real-time gameplay, character persistence, and world state management.

### Core Database Principles
```yaml
database_design_principles:
  performance:
    - "Indexed primary keys on all tables"
    - "Foreign key constraints for data integrity"
    - "Partitioning for large tables (logs, statistics)"
    - "Read replicas for analytics and reporting"
    
  scalability:
    - "Horizontal sharding by district/server"
    - "Separate databases for different systems"
    - "Connection pooling and caching layers"
    - "Asynchronous writes where possible"
    
  reliability:
    - "Regular automated backups"
    - "Transaction rollback capabilities"
    - "Data validation at application layer"
    - "Disaster recovery procedures"
```

## 👤 Account and Character Management

### Account System Tables
```sql
-- Core account information
CREATE TABLE accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(32) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    account_status ENUM('active', 'suspended', 'banned', 'pending') DEFAULT 'active',
    subscription_type ENUM('free', 'premium', 'lifetime') DEFAULT 'free',
    subscription_expires TIMESTAMP NULL,
    total_playtime INT DEFAULT 0, -- seconds
    
    -- Security and tracking
    last_ip VARCHAR(45), -- IPv6 compatible
    login_count INT DEFAULT 0,
    failed_login_attempts INT DEFAULT 0,
    last_failed_login TIMESTAMP NULL,
    security_flags INT DEFAULT 0,
    
    -- Administrative
    admin_level TINYINT DEFAULT 0,
    admin_notes TEXT NULL,
    created_by INT NULL,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_last_login (last_login),
    INDEX idx_account_status (account_status)
);

-- Account security and authentication
CREATE TABLE account_security (
    account_id INT PRIMARY KEY,
    salt VARCHAR(32) NOT NULL,
    password_reset_token VARCHAR(128) NULL,
    password_reset_expires TIMESTAMP NULL,
    two_factor_secret VARCHAR(32) NULL,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    recovery_codes JSON NULL,
    security_questions JSON NULL,
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

-- Login session management
CREATE TABLE account_sessions (
    session_id VARCHAR(128) PRIMARY KEY,
    account_id INT NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    session_data JSON NULL,
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    INDEX idx_account_sessions (account_id),
    INDEX idx_expires (expires_at)
);

-- Account punishment system
CREATE TABLE account_punishments (
    punishment_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    punishment_type ENUM('warning', 'mute', 'suspension', 'ban') NOT NULL,
    reason TEXT NOT NULL,
    issued_by INT NOT NULL,
    issued_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_date TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT NULL,
    appeal_status ENUM('none', 'pending', 'approved', 'denied') DEFAULT 'none',
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (issued_by) REFERENCES accounts(account_id),
    INDEX idx_account_punishments (account_id),
    INDEX idx_active_punishments (account_id, is_active, expires_date)
);
```

### Character System Tables
```sql
-- Character base information
CREATE TABLE characters (
    character_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    character_name VARCHAR(32) UNIQUE NOT NULL,
    
    -- Character appearance and basics
    archetype ENUM('hacker', 'martial_artist', 'spy') NOT NULL,
    gender ENUM('male', 'female') NOT NULL,
    appearance_data JSON NOT NULL, -- Customization options
    
    -- Character progression
    level TINYINT DEFAULT 1,
    experience INT DEFAULT 0,
    
    -- Attributes
    vitality TINYINT DEFAULT 20,
    focus TINYINT DEFAULT 20,
    perception TINYINT DEFAULT 20,
    reason TINYINT DEFAULT 20,
    belief TINYINT DEFAULT 0,
    
    -- Derived stats
    health INT DEFAULT 200,
    inner_strength INT DEFAULT 160,
    max_health INT DEFAULT 200,
    max_inner_strength INT DEFAULT 160,
    
    -- Location and status
    district_id INT DEFAULT 1,
    position_x FLOAT DEFAULT 0,
    position_y FLOAT DEFAULT 0,
    position_z FLOAT DEFAULT 0,
    rotation_x FLOAT DEFAULT 0,
    rotation_y FLOAT DEFAULT 0,
    rotation_z FLOAT DEFAULT 0,
    rotation_w FLOAT DEFAULT 1,
    
    -- Faction and social
    faction ENUM('zion', 'machine', 'merovingian', 'neutral') DEFAULT 'neutral',
    organization_id INT NULL,
    crew_id INT NULL,
    
    -- Character state
    is_online BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP NULL,
    total_playtime INT DEFAULT 0,
    character_flags INT DEFAULT 0,
    
    -- Timestamps
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    INDEX idx_character_name (character_name),
    INDEX idx_account_characters (account_id),
    INDEX idx_character_location (district_id, position_x, position_y, position_z),
    INDEX idx_character_faction (faction),
    INDEX idx_online_characters (is_online, last_login)
);

-- Character statistics and achievements
CREATE TABLE character_statistics (
    character_id INT PRIMARY KEY,
    
    -- Combat statistics
    total_kills INT DEFAULT 0,
    total_deaths INT DEFAULT 0,
    player_kills INT DEFAULT 0,
    npc_kills INT DEFAULT 0,
    interlock_wins INT DEFAULT 0,
    interlock_losses INT DEFAULT 0,
    
    -- Mission statistics
    missions_completed INT DEFAULT 0,
    missions_failed INT DEFAULT 0,
    story_missions_completed INT DEFAULT 0,
    daily_missions_completed INT DEFAULT 0,
    
    -- Social statistics
    players_helped INT DEFAULT 0,
    crews_joined INT DEFAULT 0,
    events_participated INT DEFAULT 0,
    
    -- Economic statistics
    money_earned BIGINT DEFAULT 0,
    money_spent BIGINT DEFAULT 0,
    items_traded INT DEFAULT 0,
    
    -- Exploration statistics
    districts_visited INT DEFAULT 0,
    hardlines_discovered INT DEFAULT 0,
    secrets_found INT DEFAULT 0,
    
    -- Skill usage statistics
    abilities_used JSON NULL, -- {"karate": 1500, "hacking": 890, ...}
    
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);

-- Character abilities and skills
CREATE TABLE character_abilities (
    character_id INT NOT NULL,
    ability_id INT NOT NULL,
    ability_level TINYINT DEFAULT 1,
    mastery_points INT DEFAULT 0,
    mastery_percentage FLOAT DEFAULT 0.0,
    times_used INT DEFAULT 0,
    last_used TIMESTAMP NULL,
    
    PRIMARY KEY (character_id, ability_id),
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    INDEX idx_character_abilities (character_id),
    INDEX idx_ability_mastery (character_id, mastery_percentage)
);

-- Character faction standings
CREATE TABLE character_faction_standings (
    character_id INT NOT NULL,
    faction ENUM('zion', 'machine', 'merovingian') NOT NULL,
    standing_points INT DEFAULT 0, -- -1000 to +1000
    reputation_level ENUM('hostile', 'unfriendly', 'neutral', 'friendly', 'ally', 'champion') DEFAULT 'neutral',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (character_id, faction),
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    INDEX idx_faction_standings (faction, standing_points)
);
```

## 🎒 Inventory and Items System

### Item System Tables
```sql
-- Item templates and definitions
CREATE TABLE item_templates (
    template_id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(64) NOT NULL,
    item_description TEXT,
    item_type ENUM('weapon', 'clothing', 'consumable', 'program', 'key_item', 'misc') NOT NULL,
    item_subtype VARCHAR(32), -- pistol, rifle, shirt, pants, etc.
    
    -- Item properties
    quality ENUM('common', 'uncommon', 'rare', 'epic', 'legendary') DEFAULT 'common',
    item_level TINYINT DEFAULT 1,
    requirements JSON NULL, -- Level, faction, ability requirements
    
    -- Stats and effects
    stat_bonuses JSON NULL, -- {"vitality": 5, "accuracy": 10, ...}
    special_effects JSON NULL, -- Special item properties
    
    -- Economic properties
    base_value INT DEFAULT 0,
    vendor_price INT DEFAULT 0,
    stack_size INT DEFAULT 1,
    
    -- Flags and restrictions
    is_tradeable BOOLEAN DEFAULT TRUE,
    is_droppable BOOLEAN DEFAULT TRUE,
    is_sellable BOOLEAN DEFAULT TRUE,
    bind_on_pickup BOOLEAN DEFAULT FALSE,
    bind_on_equip BOOLEAN DEFAULT FALSE,
    
    -- Visual and technical
    model_file VARCHAR(128),
    texture_file VARCHAR(128),
    icon_file VARCHAR(128),
    
    -- Metadata
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT NULL,
    
    INDEX idx_item_type (item_type, item_subtype),
    INDEX idx_item_quality (quality),
    INDEX idx_item_level (item_level)
);

-- Character inventory
CREATE TABLE character_inventory (
    item_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    character_id INT NOT NULL,
    template_id INT NOT NULL,
    
    -- Item instance data
    quantity INT DEFAULT 1,
    durability FLOAT DEFAULT 100.0,
    custom_properties JSON NULL, -- Enchantments, modifications, etc.
    
    -- Inventory position
    container_type ENUM('inventory', 'equipped', 'bank', 'temp') DEFAULT 'inventory',
    slot_position INT NULL,
    
    -- Item history
    acquired_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acquired_method ENUM('loot', 'purchase', 'trade', 'quest', 'admin') DEFAULT 'loot',
    acquired_from VARCHAR(128) NULL,
    
    -- Item flags
    is_bound BOOLEAN DEFAULT FALSE,
    item_flags INT DEFAULT 0,
    
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES item_templates(template_id),
    INDEX idx_character_inventory (character_id, container_type),
    INDEX idx_inventory_slot (character_id, container_type, slot_position),
    INDEX idx_item_template (template_id)
);

-- Equipment slots
CREATE TABLE character_equipment (
    character_id INT NOT NULL,
    slot_name VARCHAR(32) NOT NULL, -- weapon_primary, weapon_secondary, clothing_head, etc.
    item_id BIGINT NULL,
    
    PRIMARY KEY (character_id, slot_name),
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES character_inventory(item_id) ON DELETE SET NULL,
    INDEX idx_character_equipment (character_id)
);

-- Item modifications and enhancements
CREATE TABLE item_modifications (
    modification_id INT PRIMARY KEY AUTO_INCREMENT,
    item_id BIGINT NOT NULL,
    modification_type ENUM('enhancement', 'enchantment', 'upgrade', 'repair') NOT NULL,
    modification_data JSON NOT NULL, -- Specific modification details
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    applied_by INT NULL, -- Character or NPC that applied modification
    cost_paid INT DEFAULT 0,
    
    FOREIGN KEY (item_id) REFERENCES character_inventory(item_id) ON DELETE CASCADE,
    INDEX idx_item_modifications (item_id)
);
```

## 🌍 World and Location System

### World Management Tables
```sql
-- Districts and areas
CREATE TABLE districts (
    district_id INT PRIMARY KEY AUTO_INCREMENT,
    district_name VARCHAR(64) UNIQUE NOT NULL,
    district_type ENUM('downtown', 'international', 'slums', 'construct', 'special') NOT NULL,
    
    -- District properties
    max_players INT DEFAULT 50,
    pvp_enabled BOOLEAN DEFAULT FALSE,
    difficulty_level TINYINT DEFAULT 1,
    
    -- Geographic bounds
    min_x FLOAT NOT NULL,
    max_x FLOAT NOT NULL,
    min_y FLOAT NOT NULL,
    max_y FLOAT NOT NULL,
    min_z FLOAT NOT NULL,
    max_z FLOAT NOT NULL,
    
    -- District settings
    weather_type VARCHAR(32) DEFAULT 'clear',
    lighting_preset VARCHAR(32) DEFAULT 'day',
    ambient_sound VARCHAR(128) NULL,
    background_music VARCHAR(128) NULL,
    
    -- Access control
    access_requirements JSON NULL, -- Level, faction, item requirements
    instance_type ENUM('public', 'private', 'guild', 'event') DEFAULT 'public',
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_district_type (district_type),
    INDEX idx_district_active (is_active)
);

-- Static world objects (NPCs, terminals, etc.)
CREATE TABLE world_objects (
    object_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    district_id INT NOT NULL,
    object_type ENUM('npc', 'terminal', 'hardline', 'item_spawn', 'decoration', 'interactive') NOT NULL,
    template_id INT NULL, -- Reference to object template
    
    -- Position and orientation
    position_x FLOAT NOT NULL,
    position_y FLOAT NOT NULL,
    position_z FLOAT NOT NULL,
    rotation_x FLOAT DEFAULT 0,
    rotation_y FLOAT DEFAULT 0,
    rotation_z FLOAT DEFAULT 0,
    rotation_w FLOAT DEFAULT 1,
    
    -- Object properties
    object_name VARCHAR(64) NULL,
    object_data JSON NULL, -- Type-specific data
    interaction_data JSON NULL, -- What happens when interacted with
    
    -- State management
    current_state ENUM('active', 'inactive', 'destroyed', 'hidden') DEFAULT 'active',
    respawn_time INT DEFAULT 0, -- Seconds until respawn if destroyed
    last_interaction TIMESTAMP NULL,
    
    -- Spawning rules
    spawn_condition JSON NULL, -- Conditions for spawning
    despawn_condition JSON NULL, -- Conditions for despawning
    
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE CASCADE,
    INDEX idx_world_objects_district (district_id),
    INDEX idx_world_objects_type (object_type),
    INDEX idx_world_objects_position (district_id, position_x, position_y, position_z)
);

-- Hardline locations and connections
CREATE TABLE hardlines (
    hardline_id INT PRIMARY KEY AUTO_INCREMENT,
    district_id INT NOT NULL,
    hardline_name VARCHAR(64) NOT NULL,
    
    -- Location
    position_x FLOAT NOT NULL,
    position_y FLOAT NOT NULL,
    position_z FLOAT NOT NULL,
    
    -- Hardline properties
    hardline_type ENUM('public', 'private', 'faction', 'mission') DEFAULT 'public',
    access_code VARCHAR(16) NULL, -- For private hardlines
    faction_requirement ENUM('zion', 'machine', 'merovingian') NULL,
    level_requirement TINYINT DEFAULT 1,
    
    -- Network connections
    connected_hardlines JSON NULL, -- List of hardline IDs this connects to
    connection_cost INT DEFAULT 0, -- Cost to use connection
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_used TIMESTAMP NULL,
    usage_count INT DEFAULT 0,
    
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE CASCADE,
    INDEX idx_hardlines_district (district_id),
    INDEX idx_hardlines_type (hardline_type),
    INDEX idx_hardlines_faction (faction_requirement)
);

-- Dynamic world events
CREATE TABLE world_events (
    event_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    district_id INT NULL, -- NULL for server-wide events
    event_type ENUM('spawning', 'weather', 'lighting', 'combat', 'story', 'admin') NOT NULL,
    
    -- Event data
    event_name VARCHAR(128),
    event_description TEXT,
    event_data JSON NOT NULL, -- Event-specific parameters
    
    -- Timing
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL,
    duration INT NULL, -- Seconds (alternative to end_time)
    
    -- Conditions
    trigger_condition JSON NULL, -- What triggers this event
    completion_condition JSON NULL, -- What completes this event
    
    -- Status
    event_status ENUM('scheduled', 'active', 'completed', 'cancelled') DEFAULT 'scheduled',
    participants JSON NULL, -- Players involved in event
    
    -- Results
    event_results JSON NULL, -- Outcomes and rewards
    created_by INT NULL, -- Admin or system that created event
    
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE CASCADE,
    INDEX idx_world_events_district (district_id),
    INDEX idx_world_events_time (start_time, end_time),
    INDEX idx_world_events_status (event_status)
);
```

## 🎯 Mission and Quest System

### Mission System Tables
```sql
-- Mission templates and definitions
CREATE TABLE mission_templates (
    mission_id INT PRIMARY KEY AUTO_INCREMENT,
    mission_name VARCHAR(128) NOT NULL,
    mission_description TEXT NOT NULL,
    
    -- Mission classification
    mission_type ENUM('story', 'side', 'daily', 'faction', 'organization', 'event') NOT NULL,
    difficulty_level TINYINT DEFAULT 1,
    recommended_players TINYINT DEFAULT 1,
    
    -- Requirements
    level_requirement TINYINT DEFAULT 1,
    faction_requirement ENUM('zion', 'machine', 'merovingian') NULL,
    prerequisite_missions JSON NULL, -- Array of required mission IDs
    required_items JSON NULL, -- Items needed to start/complete
    
    -- Mission structure
    objectives JSON NOT NULL, -- Array of objective definitions
    completion_requirements JSON NOT NULL, -- What constitutes completion
    failure_conditions JSON NULL, -- What causes mission failure
    
    -- Rewards
    experience_reward INT DEFAULT 0,
    money_reward INT DEFAULT 0,
    item_rewards JSON NULL, -- Array of item template IDs and quantities
    faction_standing_rewards JSON NULL, -- Faction standing changes
    
    -- Location and NPCs
    start_location JSON NULL, -- District and coordinates
    contact_npc_id INT NULL,
    involved_npcs JSON NULL, -- NPCs involved in mission
    
    -- Mission flow
    auto_accept BOOLEAN DEFAULT FALSE,
    auto_complete BOOLEAN DEFAULT FALSE,
    repeatable BOOLEAN DEFAULT FALSE,
    cooldown_period INT DEFAULT 0, -- Hours between repeats
    
    -- Administrative
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT NULL,
    
    INDEX idx_mission_type (mission_type),
    INDEX idx_mission_level (level_requirement),
    INDEX idx_mission_faction (faction_requirement),
    INDEX idx_mission_active (is_active)
);

-- Character mission progress
CREATE TABLE character_missions (
    character_id INT NOT NULL,
    mission_id INT NOT NULL,
    
    -- Mission state
    mission_status ENUM('available', 'accepted', 'in_progress', 'completed', 'failed', 'abandoned') NOT NULL,
    progress_data JSON NULL, -- Objective completion status
    
    -- Timing
    accepted_date TIMESTAMP NULL,
    completed_date TIMESTAMP NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Custom mission data (for procedural missions)
    custom_objectives JSON NULL,
    custom_rewards JSON NULL,
    
    PRIMARY KEY (character_id, mission_id),
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES mission_templates(mission_id) ON DELETE CASCADE,
    INDEX idx_character_missions_status (character_id, mission_status),
    INDEX idx_mission_progress (mission_id, mission_status)
);

-- Mission objective tracking
CREATE TABLE mission_objective_progress (
    character_id INT NOT NULL,
    mission_id INT NOT NULL,
    objective_index INT NOT NULL,
    
    -- Progress tracking
    current_progress INT DEFAULT 0,
    required_progress INT NOT NULL,
    progress_data JSON NULL, -- Objective-specific progress data
    
    -- Status
    is_completed BOOLEAN DEFAULT FALSE,
    completed_date TIMESTAMP NULL,
    
    PRIMARY KEY (character_id, mission_id, objective_index),
    FOREIGN KEY (character_id, mission_id) REFERENCES character_missions(character_id, mission_id) ON DELETE CASCADE,
    INDEX idx_objective_progress (character_id, mission_id)
);

-- Mission history and completion log
CREATE TABLE mission_history (
    history_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    character_id INT NOT NULL,
    mission_id INT NOT NULL,
    
    -- Completion details
    completion_status ENUM('completed', 'failed', 'abandoned') NOT NULL,
    completion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_time INT NULL, -- Seconds taken to complete
    
    -- Rewards received
    experience_gained INT DEFAULT 0,
    money_gained INT DEFAULT 0,
    items_received JSON NULL,
    faction_changes JSON NULL,
    
    -- Context
    completion_method VARCHAR(64) NULL, -- How it was completed
    team_members JSON NULL, -- Other players involved
    
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES mission_templates(mission_id),
    INDEX idx_mission_history_character (character_id),
    INDEX idx_mission_history_date (completion_date)
);
```

## ⚔️ Combat and PvP System

### Combat System Tables
```sql
-- Combat encounters and tracking
CREATE TABLE combat_encounters (
    encounter_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- Encounter type and participants
    encounter_type ENUM('pve', 'pvp', 'interlock', 'training') NOT NULL,
    initiator_id INT NOT NULL,
    target_id INT NULL, -- Character or NPC ID
    target_type ENUM('player', 'npc') NOT NULL,
    
    -- Location
    district_id INT NOT NULL,
    position_x FLOAT NOT NULL,
    position_y FLOAT NOT NULL,
    position_z FLOAT NOT NULL,
    
    -- Combat details
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    duration INT NULL, -- Seconds
    
    -- Results
    encounter_result ENUM('victory', 'defeat', 'draw', 'fled', 'interrupted') NULL,
    winner_id INT NULL,
    
    -- Statistics
    total_damage_dealt JSON NULL, -- Per participant
    total_damage_received JSON NULL, -- Per participant
    abilities_used JSON NULL, -- Abilities used during combat
    
    FOREIGN KEY (initiator_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (district_id) REFERENCES districts(district_id),
    INDEX idx_combat_encounters_time (start_time),
    INDEX idx_combat_encounters_type (encounter_type),
    INDEX idx_combat_participants (initiator_id, target_id)
);

-- Interlock combat system
CREATE TABLE interlock_encounters (
    interlock_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- Participants (up to 8 players)
    participants JSON NOT NULL, -- Array of character IDs
    participant_count TINYINT NOT NULL,
    interlock_type ENUM('one_v_one', 'small_group', 'large_group') NOT NULL,
    
    -- Location and timing
    district_id INT NOT NULL,
    center_position JSON NOT NULL, -- {x, y, z}
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    
    -- Interlock state
    current_round INT DEFAULT 1,
    max_rounds INT DEFAULT 10,
    interlock_status ENUM('starting', 'active', 'completed', 'interrupted') DEFAULT 'starting',
    
    -- Results
    winner_id INT NULL,
    elimination_order JSON NULL, -- Order participants were eliminated
    
    FOREIGN KEY (district_id) REFERENCES districts(district_id),
    INDEX idx_interlock_time (start_time),
    INDEX idx_interlock_status (interlock_status)
);

-- Interlock round details
CREATE TABLE interlock_rounds (
    round_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    interlock_id BIGINT NOT NULL,
    round_number INT NOT NULL,
    
    -- Round actions
    actions_taken JSON NOT NULL, -- All player actions this round
    round_results JSON NOT NULL, -- Results of all actions
    
    -- Timing
    round_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    round_end TIMESTAMP NULL,
    
    FOREIGN KEY (interlock_id) REFERENCES interlock_encounters(interlock_id) ON DELETE CASCADE,
    INDEX idx_interlock_rounds (interlock_id, round_number)
);

-- Player vs Player statistics
CREATE TABLE pvp_statistics (
    character_id INT PRIMARY KEY,
    
    -- Overall PvP stats
    total_pvp_encounters INT DEFAULT 0,
    pvp_wins INT DEFAULT 0,
    pvp_losses INT DEFAULT 0,
    pvp_draws INT DEFAULT 0,
    
    -- Interlock specific
    interlock_encounters INT DEFAULT 0,
    interlock_wins INT DEFAULT 0,
    interlock_losses INT DEFAULT 0,
    
    -- Damage statistics
    total_pvp_damage_dealt BIGINT DEFAULT 0,
    total_pvp_damage_received BIGINT DEFAULT 0,
    highest_single_hit INT DEFAULT 0,
    
    -- Streak tracking
    current_win_streak INT DEFAULT 0,
    best_win_streak INT DEFAULT 0,
    current_loss_streak INT DEFAULT 0,
    
    -- Rankings
    pvp_rating INT DEFAULT 1000, -- ELO-style rating
    pvp_rank VARCHAR(32) DEFAULT 'Unranked',
    season_wins INT DEFAULT 0,
    season_losses INT DEFAULT 0,
    
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
);
```

## 🏛️ Social and Organization System

### Organization and Crew Tables
```sql
-- Organizations (Zion, Machine, Merovingian sub-groups)
CREATE TABLE organizations (
    organization_id INT PRIMARY KEY AUTO_INCREMENT,
    organization_name VARCHAR(64) UNIQUE NOT NULL,
    faction ENUM('zion', 'machine', 'merovingian') NOT NULL,
    
    -- Organization details
    description TEXT,
    motto VARCHAR(128),
    logo_file VARCHAR(128),
    
    -- Hierarchy
    leader_id INT NULL,
    officers JSON NULL, -- Array of character IDs
    member_count INT DEFAULT 0,
    max_members INT DEFAULT 100,
    
    -- Organization properties
    organization_level TINYINT DEFAULT 1,
    experience_points INT DEFAULT 0,
    treasury_amount BIGINT DEFAULT 0,
    
    -- Recruitment
    recruitment_status ENUM('open', 'invite_only', 'closed') DEFAULT 'open',
    level_requirement TINYINT DEFAULT 1,
    application_required BOOLEAN DEFAULT FALSE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    founded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (leader_id) REFERENCES characters(character_id) ON DELETE SET NULL,
    INDEX idx_organizations_faction (faction),
    INDEX idx_organizations_active (is_active)
);

-- Crews (player groups within organizations)
CREATE TABLE crews (
    crew_id INT PRIMARY KEY AUTO_INCREMENT,
    crew_name VARCHAR(64) UNIQUE NOT NULL,
    organization_id INT NULL,
    
    -- Crew details
    description TEXT,
    crew_motto VARCHAR(128),
    crew_logo VARCHAR(128),
    
    -- Leadership
    captain_id INT NOT NULL,
    lieutenants JSON NULL, -- Array of character IDs
    member_count TINYINT DEFAULT 1,
    max_members TINYINT DEFAULT 16,
    
    -- Crew progression
    crew_level TINYINT DEFAULT 1,
    crew_experience INT DEFAULT 0,
    crew_reputation INT DEFAULT 0,
    
    -- Crew properties
    crew_type ENUM('combat', 'exploration', 'social', 'business', 'mixed') DEFAULT 'mixed',
    base_district_id INT NULL, -- Crew's home district
    
    -- Recruitment
    recruitment_open BOOLEAN DEFAULT TRUE,
    invite_only BOOLEAN DEFAULT FALSE,
    application_message TEXT,
    
    -- Status and activity
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (captain_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id) ON DELETE SET NULL,
    FOREIGN KEY (base_district_id) REFERENCES districts(district_id) ON DELETE SET NULL,
    INDEX idx_crews_organization (organization_id),
    INDEX idx_crews_captain (captain_id),
    INDEX idx_crews_active (is_active)
);

-- Organization/Crew membership
CREATE TABLE organization_members (
    character_id INT NOT NULL,
    organization_id INT NOT NULL,
    
    -- Membership details
    rank_name VARCHAR(32) DEFAULT 'Member',
    rank_level TINYINT DEFAULT 1,
    permissions INT DEFAULT 0, -- Bitfield for permissions
    
    -- Membership tracking
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_contribution TIMESTAMP NULL,
    total_contributions INT DEFAULT 0,
    
    -- Status
    member_status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    notes TEXT NULL,
    
    PRIMARY KEY (character_id, organization_id),
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id) ON DELETE CASCADE,
    INDEX idx_org_members_org (organization_id),
    INDEX idx_org_members_rank (organization_id, rank_level)
);

CREATE TABLE crew_members (
    character_id INT NOT NULL,
    crew_id INT NOT NULL,
    
    -- Membership details
    position ENUM('captain', 'lieutenant', 'member', 'recruit') DEFAULT 'member',
    permissions INT DEFAULT 0,
    
    -- Membership tracking
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_online TIMESTAMP NULL,
    contribution_points INT DEFAULT 0,
    
    -- Status
    member_status ENUM('active', 'inactive', 'on_leave') DEFAULT 'active',
    
    PRIMARY KEY (character_id, crew_id),
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (crew_id) REFERENCES crews(crew_id) ON DELETE CASCADE,
    INDEX idx_crew_members_crew (crew_id),
    INDEX idx_crew_members_position (crew_id, position)
);

-- Social relationships (friends, enemies, etc.)
CREATE TABLE character_relationships (
    character_id INT NOT NULL,
    target_character_id INT NOT NULL,
    relationship_type ENUM('friend', 'ignore', 'enemy', 'neutral') NOT NULL,
    
    -- Relationship details
    relationship_level TINYINT DEFAULT 1, -- Intensity of relationship
    notes TEXT NULL,
    is_mutual BOOLEAN DEFAULT FALSE,
    
    -- Tracking
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_interaction TIMESTAMP NULL,
    interaction_count INT DEFAULT 0,
    
    PRIMARY KEY (character_id, target_character_id),
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (target_character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    INDEX idx_relationships_type (character_id, relationship_type),
    CHECK (character_id != target_character_id)
);
```

## 💰 Economy and Trading System

### Economic System Tables
```sql
-- Server economy tracking
CREATE TABLE server_economy (
    tracking_date DATE PRIMARY KEY,
    
    -- Currency circulation
    total_money_in_circulation BIGINT DEFAULT 0,
    money_created_today BIGINT DEFAULT 0,
    money_destroyed_today BIGINT DEFAULT 0,
    
    -- Item economy
    items_created_today INT DEFAULT 0,
    items_destroyed_today INT DEFAULT 0,
    trades_completed_today INT DEFAULT 0,
    
    -- Price tracking
    average_item_prices JSON NULL, -- Average prices by item template
    inflation_rate DECIMAL(5,2) DEFAULT 0.00,
    
    -- Market activity
    vendor_sales_today BIGINT DEFAULT 0,
    player_trades_today BIGINT DEFAULT 0,
    
    INDEX idx_economy_date (tracking_date)
);

-- Vendor NPCs and shops
CREATE TABLE vendors (
    vendor_id INT PRIMARY KEY AUTO_INCREMENT,
    vendor_name VARCHAR(64) NOT NULL,
    district_id INT NOT NULL,
    
    -- Location
    position_x FLOAT NOT NULL,
    position_y FLOAT NOT NULL,
    position_z FLOAT NOT NULL,
    
    -- Vendor properties
    vendor_type ENUM('general', 'weapon', 'clothing', 'program', 'faction', 'special') NOT NULL,
    faction_requirement ENUM('zion', 'machine', 'merovingian') NULL,
    level_requirement TINYINT DEFAULT 1,
    
    -- Economic properties
    buy_rate DECIMAL(3,2) DEFAULT 0.50, -- Percentage of item value when buying from players
    sell_markup DECIMAL(3,2) DEFAULT 1.20, -- Multiplier for selling to players
    
    -- Inventory management
    max_inventory_size INT DEFAULT 1000,
    restocks_inventory BOOLEAN DEFAULT TRUE,
    restock_interval INT DEFAULT 3600, -- Seconds
    last_restock TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE CASCADE,
    INDEX idx_vendors_district (district_id),
    INDEX idx_vendors_type (vendor_type),
    INDEX idx_vendors_faction (faction_requirement)
);

-- Vendor inventory
CREATE TABLE vendor_inventory (
    vendor_id INT NOT NULL,
    template_id INT NOT NULL,
    
    -- Stock information
    current_stock INT DEFAULT 0,
    max_stock INT DEFAULT 10,
    base_price INT NOT NULL,
    current_price INT NOT NULL,
    
    -- Restock settings
    restock_amount INT DEFAULT 5,
    restock_probability DECIMAL(3,2) DEFAULT 1.00,
    
    -- Sales tracking
    total_sold INT DEFAULT 0,
    last_sold TIMESTAMP NULL,
    
    PRIMARY KEY (vendor_id, template_id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES item_templates(template_id) ON DELETE CASCADE,
    INDEX idx_vendor_inventory_stock (vendor_id, current_stock)
);

-- Player-to-player trading
CREATE TABLE trade_sessions (
    trade_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- Trading parties
    initiator_id INT NOT NULL,
    recipient_id INT NOT NULL,
    
    -- Trade details
    initiator_items JSON NULL, -- Array of item IDs and quantities
    recipient_items JSON NULL, -- Array of item IDs and quantities
    initiator_money INT DEFAULT 0,
    recipient_money INT DEFAULT 0,
    
    -- Trade state
    trade_status ENUM('initiated', 'negotiating', 'confirmed', 'completed', 'cancelled') DEFAULT 'initiated',
    initiator_confirmed BOOLEAN DEFAULT FALSE,
    recipient_confirmed BOOLEAN DEFAULT FALSE,
    
    -- Timing
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_date TIMESTAMP NULL,
    expires_date TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 1 HOUR),
    
    -- Location
    district_id INT NOT NULL,
    
    FOREIGN KEY (initiator_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (district_id) REFERENCES districts(district_id),
    INDEX idx_trade_sessions_status (trade_status),
    INDEX idx_trade_sessions_players (initiator_id, recipient_id),
    INDEX idx_trade_sessions_expires (expires_date)
);

-- Transaction history
CREATE TABLE transaction_history (
    transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- Transaction parties
    from_character_id INT NULL,
    to_character_id INT NULL,
    vendor_id INT NULL,
    
    -- Transaction details
    transaction_type ENUM('trade', 'vendor_sale', 'vendor_purchase', 'admin_grant', 'quest_reward', 'drop_loot') NOT NULL,
    money_amount INT DEFAULT 0,
    items_transferred JSON NULL, -- Array of item details
    
    -- Context
    transaction_reason VARCHAR(128),
    related_mission_id INT NULL,
    related_trade_id BIGINT NULL,
    
    -- Timing and location
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    district_id INT NULL,
    
    INDEX idx_transaction_history_date (transaction_date),
    INDEX idx_transaction_history_character (from_character_id, to_character_id),
    INDEX idx_transaction_history_type (transaction_type),
    FOREIGN KEY (from_character_id) REFERENCES characters(character_id) ON DELETE SET NULL,
    FOREIGN KEY (to_character_id) REFERENCES characters(character_id) ON DELETE SET NULL,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id) ON DELETE SET NULL,
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE SET NULL
);
```

## 📊 Logging and Analytics System

### System Logging Tables
```sql
-- General system activity logs
CREATE TABLE system_logs (
    log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    log_level ENUM('DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL') NOT NULL,
    log_category VARCHAR(32) NOT NULL, -- system, combat, economy, social, etc.
    log_message TEXT NOT NULL,
    log_data JSON NULL, -- Additional structured data
    
    -- Context
    character_id INT NULL,
    district_id INT NULL,
    session_id VARCHAR(128) NULL,
    
    -- Timing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE SET NULL,
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE SET NULL,
    INDEX idx_system_logs_level (log_level, created_at),
    INDEX idx_system_logs_category (log_category, created_at),
    INDEX idx_system_logs_character (character_id, created_at)
) PARTITION BY RANGE (TO_DAYS(created_at)) (
    PARTITION p_logs_old VALUES LESS THAN (TO_DAYS('2024-01-01')),
    PARTITION p_logs_2024 VALUES LESS THAN (TO_DAYS('2025-01-01')),
    PARTITION p_logs_2025 VALUES LESS THAN (TO_DAYS('2026-01-01')),
    PARTITION p_logs_future VALUES LESS THAN MAXVALUE
);

-- Player action logs
CREATE TABLE player_action_logs (
    action_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    character_id INT NOT NULL,
    action_type VARCHAR(32) NOT NULL, -- login, logout, move, attack, trade, etc.
    action_details JSON NULL, -- Action-specific data
    
    -- Context
    district_id INT NULL,
    target_character_id INT NULL,
    item_id BIGINT NULL,
    
    -- Results
    action_result ENUM('success', 'failure', 'partial') DEFAULT 'success',
    error_message TEXT NULL,
    
    -- Timing
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE SET NULL,
    FOREIGN KEY (target_character_id) REFERENCES characters(character_id) ON DELETE SET NULL,
    INDEX idx_player_actions_character (character_id, action_timestamp),
    INDEX idx_player_actions_type (action_type, action_timestamp)
) PARTITION BY RANGE (TO_DAYS(action_timestamp)) (
    PARTITION p_actions_old VALUES LESS THAN (TO_DAYS('2024-01-01')),
    PARTITION p_actions_2024 VALUES LESS THAN (TO_DAYS('2025-01-01')),
    PARTITION p_actions_2025 VALUES LESS THAN (TO_DAYS('2026-01-01')),
    PARTITION p_actions_future VALUES LESS THAN MAXVALUE
);

-- Chat and communication logs
CREATE TABLE chat_logs (
    message_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    character_id INT NOT NULL,
    
    -- Message details
    channel_type ENUM('say', 'broadcast', 'crew', 'faction', 'private', 'system') NOT NULL,
    message_content TEXT NOT NULL,
    target_character_id INT NULL, -- For private messages
    
    -- Location context
    district_id INT NULL,
    position_x FLOAT NULL,
    position_y FLOAT NULL,
    position_z FLOAT NULL,
    
    -- Timing
    message_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Moderation
    is_flagged BOOLEAN DEFAULT FALSE,
    moderation_action ENUM('none', 'warned', 'edited', 'deleted') DEFAULT 'none',
    moderated_by INT NULL,
    
    FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
    FOREIGN KEY (target_character_id) REFERENCES characters(character_id) ON DELETE SET NULL,
    FOREIGN KEY (district_id) REFERENCES districts(district_id) ON DELETE SET NULL,
    FOREIGN KEY (moderated_by) REFERENCES accounts(account_id) ON DELETE SET NULL,
    INDEX idx_chat_logs_character (character_id, message_timestamp),
    INDEX idx_chat_logs_channel (channel_type, message_timestamp),
    INDEX idx_chat_logs_district (district_id, message_timestamp)
) PARTITION BY RANGE (TO_DAYS(message_timestamp)) (
    PARTITION p_chat_old VALUES LESS THAN (TO_DAYS('2024-01-01')),
    PARTITION p_chat_2024 VALUES LESS THAN (TO_DAYS('2025-01-01')),
    PARTITION p_chat_2025 VALUES LESS THAN (TO_DAYS('2026-01-01')),
    PARTITION p_chat_future VALUES LESS THAN MAXVALUE
);

-- Server performance metrics
CREATE TABLE server_metrics (
    metric_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Performance metrics
    cpu_usage DECIMAL(5,2) DEFAULT 0.00,
    memory_usage DECIMAL(5,2) DEFAULT 0.00,
    disk_usage DECIMAL(5,2) DEFAULT 0.00,
    network_in_mbps DECIMAL(8,2) DEFAULT 0.00,
    network_out_mbps DECIMAL(8,2) DEFAULT 0.00,
    
    -- Database metrics
    active_connections INT DEFAULT 0,
    queries_per_second DECIMAL(8,2) DEFAULT 0.00,
    slow_queries INT DEFAULT 0,
    
    -- Game metrics
    online_players INT DEFAULT 0,
    active_districts INT DEFAULT 0,
    combat_encounters_active INT DEFAULT 0,
    
    -- Response times (milliseconds)
    avg_response_time DECIMAL(8,2) DEFAULT 0.00,
    max_response_time DECIMAL(8,2) DEFAULT 0.00,
    
    INDEX idx_server_metrics_time (metric_timestamp)
);
```

## 🔧 Database Maintenance and Optimization

### Performance Optimization Views
```sql
-- Frequently used player data view
CREATE VIEW player_summary AS
SELECT 
    c.character_id,
    c.character_name,
    c.level,
    c.faction,
    c.is_online,
    c.last_login,
    a.account_id,
    a.username,
    a.account_status,
    COALESCE(crew.crew_name, 'None') as crew_name,
    COALESCE(org.organization_name, 'None') as organization_name
FROM characters c
JOIN accounts a ON c.account_id = a.account_id
LEFT JOIN crew_members cm ON c.character_id = cm.character_id
LEFT JOIN crews crew ON cm.crew_id = crew.crew_id
LEFT JOIN organization_members om ON c.character_id = om.character_id
LEFT JOIN organizations org ON om.organization_id = org.organization_id;

-- Character equipment summary
CREATE VIEW character_equipment_summary AS
SELECT 
    c.character_id,
    c.character_name,
    ce.slot_name,
    it.item_name,
    it.quality,
    it.item_level,
    ci.durability
FROM characters c
LEFT JOIN character_equipment ce ON c.character_id = ce.character_id
LEFT JOIN character_inventory ci ON ce.item_id = ci.item_id
LEFT JOIN item_templates it ON ci.template_id = it.template_id;

-- District activity summary
CREATE VIEW district_activity AS
SELECT 
    d.district_id,
    d.district_name,
    COUNT(DISTINCT c.character_id) as current_players,
    d.max_players,
    (COUNT(DISTINCT c.character_id) / d.max_players * 100) as occupancy_percentage,
    COUNT(DISTINCT we.event_id) as active_events
FROM districts d
LEFT JOIN characters c ON d.district_id = c.district_id AND c.is_online = TRUE
LEFT JOIN world_events we ON d.district_id = we.district_id AND we.event_status = 'active'
GROUP BY d.district_id, d.district_name, d.max_players;
```

### Database Maintenance Procedures
```sql
-- Stored procedure for character cleanup
DELIMITER //
CREATE PROCEDURE CleanupInactiveCharacters(IN days_inactive INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Archive characters inactive for specified days
    INSERT INTO archived_characters 
    SELECT * FROM characters 
    WHERE last_login < DATE_SUB(NOW(), INTERVAL days_inactive DAY)
    AND is_online = FALSE;
    
    -- Remove from active tables
    DELETE FROM characters 
    WHERE last_login < DATE_SUB(NOW(), INTERVAL days_inactive DAY)
    AND is_online = FALSE;
    
    COMMIT;
END //

-- Stored procedure for log rotation
CREATE PROCEDURE RotateLogTables()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Archive old logs (older than 90 days)
    INSERT INTO archived_system_logs 
    SELECT * FROM system_logs 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
    
    DELETE FROM system_logs 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
    
    -- Similar for other log tables
    INSERT INTO archived_player_action_logs
    SELECT * FROM player_action_logs
    WHERE action_timestamp < DATE_SUB(NOW(), INTERVAL 90 DAY);
    
    DELETE FROM player_action_logs
    WHERE action_timestamp < DATE_SUB(NOW(), INTERVAL 90 DAY);
    
    COMMIT;
END //

-- Stored procedure for economy balancing
CREATE PROCEDURE UpdateEconomyMetrics()
BEGIN
    DECLARE total_money BIGINT DEFAULT 0;
    DECLARE money_created BIGINT DEFAULT 0;
    DECLARE money_destroyed BIGINT DEFAULT 0;
    
    -- Calculate total money in circulation
    SELECT COALESCE(SUM(money), 0) INTO total_money
    FROM characters WHERE is_online = TRUE;
    
    -- Calculate money created today
    SELECT COALESCE(SUM(money_amount), 0) INTO money_created
    FROM transaction_history 
    WHERE transaction_type IN ('quest_reward', 'vendor_sale', 'admin_grant')
    AND DATE(transaction_date) = CURDATE();
    
    -- Calculate money destroyed today
    SELECT COALESCE(SUM(money_amount), 0) INTO money_destroyed
    FROM transaction_history 
    WHERE transaction_type IN ('vendor_purchase', 'repair_cost')
    AND DATE(transaction_date) = CURDATE();
    
    -- Update economy tracking
    INSERT INTO server_economy (
        tracking_date, 
        total_money_in_circulation, 
        money_created_today, 
        money_destroyed_today
    ) VALUES (
        CURDATE(), 
        total_money, 
        money_created, 
        money_destroyed
    ) ON DUPLICATE KEY UPDATE
        total_money_in_circulation = total_money,
        money_created_today = money_created,
        money_destroyed_today = money_destroyed;
END //

DELIMITER ;
```

### Database Backup and Recovery
```bash
#!/bin/bash
# Matrix Online Database Backup Script

DB_NAME="matrix_online"
DB_USER="mxo_backup"
DB_PASS="backup_password"
BACKUP_DIR="/var/backups/mxo"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "Starting Matrix Online database backup..."

# Full database backup
mysqldump --user="$DB_USER" --password="$DB_PASS" \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    --compress \
    "$DB_NAME" | gzip > "$BACKUP_DIR/mxo_full_backup_$DATE.sql.gz"

# Character data only backup (for quick character restoration)
mysqldump --user="$DB_USER" --password="$DB_PASS" \
    --single-transaction \
    --tables characters character_inventory character_equipment \
            character_abilities character_statistics character_missions \
    "$DB_NAME" | gzip > "$BACKUP_DIR/mxo_characters_$DATE.sql.gz"

# World state backup
mysqldump --user="$DB_USER" --password="$DB_PASS" \
    --single-transaction \
    --tables districts world_objects hardlines world_events \
    "$DB_NAME" | gzip > "$BACKUP_DIR/mxo_world_$DATE.sql.gz"

# Cleanup old backups (keep 30 days)
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete

echo "Database backup completed: $BACKUP_DIR/mxo_full_backup_$DATE.sql.gz"

# Verify backup integrity
if gzip -t "$BACKUP_DIR/mxo_full_backup_$DATE.sql.gz"; then
    echo "Backup integrity verified successfully"
else
    echo "ERROR: Backup corruption detected!"
    exit 1
fi
```

## Remember

> *"The Matrix is a system, Neo. That system is our enemy."* - Morpheus (But databases are the foundation that makes our resistance possible.)

The database is the persistent memory of The Matrix Online world. Every character created, every mission completed, every friendship formed, and every battle fought is preserved in these carefully designed tables. This schema represents not just data storage, but the digital DNA of a living, breathing virtual world.

**The database is more than storage—it's the foundation of digital existence.**

This comprehensive database schema provides the complete foundation for running a professional-grade Matrix Online server with full feature support, performance optimization, and administrative capabilities.

---

**Database Schema Status**: 🟢 PRODUCTION-READY  
**Performance**: OPTIMIZED  
**Scalability**: ENTERPRISE-GRADE  

*Store persistently. Query efficiently. Scale infinitely.*

---

[← Back to Technical](index.md) | [Server Setup →](../02-servers/database-setup-guide.md) | [Network Protocol →](network-protocol-complete.md)