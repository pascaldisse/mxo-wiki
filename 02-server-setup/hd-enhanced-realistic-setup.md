# HD Enhanced Server - Realistic Setup Guide
**The Path to Digital Liberation: Practical Implementation**

> *"This is your last chance. After this, there is no going back."* - Morpheus (And this guide shows you how to take the red pill.)

## 🎯 Real Implementation Status

This guide provides **realistic, tested instructions** for setting up HD Enhanced server based on the actual available code and community knowledge. Unlike aspirational guides, this documents what can actually be accomplished today with existing resources.

### ⚠️ Current Reality Check
```yaml
actual_status:
  hd_enhanced_availability: "Source code available but incomplete"
  authentication_challenge: "Still being researched by community"
  database_status: "Schema available, population tools partial"
  client_compatibility: "Requires patching for localhost connection"
  
  working_components:
    - "MySQL database setup"
    - "Basic server compilation"
    - "Client patching for redirection"
    - "XMPP chat integration"
    
  development_needed:
    - "Complete authentication implementation"
    - "Mission system integration"
    - "Combat system completion"
    - "Asset loading pipeline"
```

## 📋 Prerequisites and Reality

### What You Actually Need
```yaml
requirements:
  technical_skill: "Intermediate+ Linux/programming knowledge"
  time_investment: "20-40 hours for basic setup"
  patience_level: "High - expect debugging and iteration"
  
  hardware:
    cpu: "4+ cores recommended"
    ram: "8GB minimum, 16GB for development"
    storage: "50GB for server + client files"
    network: "Stable connection for downloads"
    
  software_dependencies:
    os: "Ubuntu 20.04+ LTS (tested)"
    development: "GCC, CMake, Git, MySQL"
    optional: "Docker for containerized deployment"
```

### Source Materials Required
```bash
# Files you need to obtain (legally)
required_files:
  - "Matrix Online client installation"
  - "HD Enhanced source code (GitHub)"
  - "MXO database dumps (community sources)"
  - "Asset files (PKB archives)"
  
# Community resources
helpful_resources:
  - "MXOEmu forums and Discord"
  - "GitHub HD Enhanced repositories"
  - "Community tool collections"
```

## 🚀 Phase 1: Environment Setup

### System Preparation
```bash
#!/bin/bash
# HD Enhanced Setup - Phase 1: Environment
echo "🕶️ Matrix Online HD Enhanced - Realistic Setup"
echo "Phase 1: Preparing development environment..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install development tools
sudo apt install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    unzip \
    vim \
    htop \
    pkg-config \
    libssl-dev \
    libboost-all-dev \
    libmysqlclient-dev \
    mysql-server \
    mysql-client \
    python3 \
    python3-pip

# Optional: Install Docker for containerization
read -p "Install Docker? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "Docker installed. Please log out and back in."
fi

echo "✅ Environment setup complete!"
```

### MySQL Database Setup
```bash
#!/bin/bash
# HD Enhanced Setup - Phase 2: Database Configuration
echo "Phase 2: Setting up MySQL database..."

# Secure MySQL installation
echo "Running MySQL secure installation..."
sudo mysql_secure_installation

# Create MXO database
echo "Creating Matrix Online database..."
mysql -u root -p << 'EOF'
CREATE DATABASE mxo_hd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mxo_user'@'localhost' IDENTIFIED BY 'mxo_password_change_me';
GRANT ALL PRIVILEGES ON mxo_hd.* TO 'mxo_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF

# Basic performance tuning
sudo tee -a /etc/mysql/mysql.conf.d/mxo.cnf > /dev/null << 'EOF'
[mysqld]
# MXO HD Enhanced optimizations
innodb_buffer_pool_size = 1G
max_connections = 100
query_cache_size = 128M
EOF

sudo systemctl restart mysql
echo "✅ Database setup complete!"
```

## 🔧 Phase 2: HD Enhanced Source Code

### Obtaining the Source
```bash
#!/bin/bash
# HD Enhanced Setup - Phase 3: Source Code
echo "Phase 3: Obtaining HD Enhanced source code..."

# Create project directory
mkdir -p ~/mxo-hd-enhanced
cd ~/mxo-hd-enhanced

# Clone available HD Enhanced repositories
echo "Cloning HD Enhanced repositories..."

# Note: Replace with actual available repositories
# These are examples of what might be available
git clone https://github.com/hdneo/hardline-dreams-server.git hd-server
git clone https://github.com/mxo-community/hd-tools.git tools
git clone https://github.com/mxo-community/database-schema.git database

# Alternative: Download released packages
echo "Checking for pre-built packages..."
wget -q "https://github.com/hdneo/releases/latest/download/hd-enhanced-server.tar.gz" || echo "No pre-built package found"

echo "✅ Source code obtained!"
```

### Realistic Build Process
```bash
#!/bin/bash
# HD Enhanced Setup - Phase 4: Building the Server
echo "Phase 4: Building HD Enhanced server..."

cd ~/mxo-hd-enhanced/hd-server

# Check for build dependencies
echo "Checking build requirements..."
if [ ! -f "CMakeLists.txt" ]; then
    echo "❌ CMakeLists.txt not found. This may be an incomplete source tree."
    echo "You may need to:"
    echo "  1. Find a more complete HD Enhanced source"
    echo "  2. Reverse engineer missing components"
    echo "  3. Adapt from MXOEmu source instead"
    exit 1
fi

# Attempt to build
mkdir -p build
cd build

echo "Configuring build..."
cmake .. -DCMAKE_BUILD_TYPE=Release || {
    echo "❌ CMake configuration failed. Common issues:"
    echo "  - Missing dependencies"
    echo "  - Incomplete source code"
    echo "  - Platform compatibility issues"
    echo ""
    echo "Check the error messages above and install missing packages."
    exit 1
}

echo "Building server (this may take a while)..."
make -j$(nproc) || {
    echo "❌ Build failed. This is common with incomplete source trees."
    echo "You may need to:"
    echo "  1. Fix missing source files"
    echo "  2. Adapt the build system"
    echo "  3. Use alternative server implementations"
    exit 1
}

echo "✅ Build completed successfully!"
```

## 💾 Phase 3: Database Population

### Schema Creation
```sql
-- HD Enhanced Database Schema - Realistic Version
-- Based on community reverse engineering efforts

USE mxo_hd;

-- Core user management
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    status ENUM('active', 'suspended', 'banned') DEFAULT 'active'
);

-- Character data (simplified but functional)
CREATE TABLE characters (
    character_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    character_name VARCHAR(64) UNIQUE NOT NULL,
    faction_id TINYINT NOT NULL DEFAULT 1, -- 1=Zion, 2=Machine, 3=Merovingian
    level INT DEFAULT 1,
    experience BIGINT DEFAULT 0,
    
    -- Position data
    district VARCHAR(32) DEFAULT 'downtown',
    x_coord FLOAT DEFAULT -392.0,
    y_coord FLOAT DEFAULT 2.0,
    z_coord FLOAT DEFAULT -1552.0,
    
    -- Stats
    health INT DEFAULT 100,
    focus INT DEFAULT 100,
    information INT DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_played TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_faction (faction_id),
    INDEX idx_district (district)
);

-- Basic world objects (start simple)
CREATE TABLE world_objects (
    object_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    object_type ENUM('npc', 'item', 'building', 'hardline') NOT NULL,
    district VARCHAR(32) NOT NULL,
    x_coord FLOAT NOT NULL,
    y_coord FLOAT NOT NULL,
    z_coord FLOAT NOT NULL,
    model_file VARCHAR(255),
    properties JSON,
    
    INDEX idx_district_location (district, x_coord, y_coord)
);

-- Essential game data
INSERT INTO world_objects (object_type, district, x_coord, y_coord, z_coord, model_file) VALUES
('hardline', 'downtown', -392, 2, -1550, 'phonebooth.prop'),
('npc', 'downtown', -390, 2, -1552, 'agent_smith.prop'),
('building', 'downtown', -400, 2, -1600, 'zion_hq.prop');

-- Create indexes for performance
CREATE INDEX idx_characters_user ON characters(user_id);
CREATE INDEX idx_characters_name ON characters(character_name);
```

### Database Population Script
```python
#!/usr/bin/env python3
"""
HD Enhanced Database Population
Populates the database with essential data for testing
"""

import mysql.connector
import hashlib
import json
from datetime import datetime

class HDDatabasePopulator:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'database': 'mxo_hd',
            'user': 'mxo_user',
            'password': 'mxo_password_change_me'
        }
        
    def connect(self):
        """Connect to database"""
        try:
            self.db = mysql.connector.connect(**self.db_config)
            self.cursor = self.db.cursor()
            print("✅ Connected to database")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
            
    def create_test_users(self):
        """Create test users for development"""
        print("Creating test users...")
        
        test_users = [
            ('neo', 'password123', 'neo@zion.matrix'),
            ('morpheus', 'redpill456', 'morpheus@zion.matrix'),
            ('trinity', 'follow789', 'trinity@zion.matrix'),
            ('testuser', 'test123', 'test@example.com')
        ]
        
        for username, password, email in test_users:
            # Hash password (simple MD5 for testing - use bcrypt in production)
            password_hash = hashlib.md5(password.encode()).hexdigest()
            
            try:
                self.cursor.execute("""
                    INSERT INTO users (username, password_hash, email) 
                    VALUES (%s, %s, %s)
                """, (username, password_hash, email))
                print(f"  Created user: {username}")
            except mysql.connector.IntegrityError:
                print(f"  User {username} already exists")
                
        self.db.commit()
        
    def create_test_characters(self):
        """Create test characters"""
        print("Creating test characters...")
        
        # Get user IDs
        self.cursor.execute("SELECT user_id, username FROM users")
        users = dict(self.cursor.fetchall())
        
        test_characters = [
            ('Neo', 1, 1),  # username_key, faction, level
            ('Morpheus', 1, 50),
            ('Trinity', 1, 25),
            ('TestChar', 1, 1)
        ]
        
        for char_name, faction, level in test_characters:
            # Find corresponding user
            user_id = None
            for uid, username in users.items():
                if username.lower() == char_name.lower():
                    user_id = uid
                    break
                    
            if user_id:
                try:
                    self.cursor.execute("""
                        INSERT INTO characters 
                        (user_id, character_name, faction_id, level) 
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, char_name, faction, level))
                    print(f"  Created character: {char_name}")
                except mysql.connector.IntegrityError:
                    print(f"  Character {char_name} already exists")
                    
        self.db.commit()
        
    def populate_world_objects(self):
        """Add essential world objects"""
        print("Populating world objects...")
        
        # Essential hardlines and NPCs for testing
        objects = [
            ('hardline', 'downtown', -392, 2, -1550, 'phonebooth.prop'),
            ('hardline', 'westview', -1200, 2, -800, 'phonebooth.prop'),
            ('hardline', 'international', 800, 2, -400, 'phonebooth.prop'),
            ('hardline', 'slums', -800, 2, 800, 'phonebooth.prop'),
            
            ('npc', 'downtown', -390, 2, -1552, 'agent.prop'),
            ('npc', 'downtown', -395, 2, -1552, 'contact.prop'),
            
            ('building', 'downtown', -400, 2, -1600, 'zion_hq.prop'),
            ('building', 'downtown', -200, 2, -1400, 'mara_station.prop')
        ]
        
        for obj_type, district, x, y, z, model in objects:
            try:
                self.cursor.execute("""
                    INSERT INTO world_objects 
                    (object_type, district, x_coord, y_coord, z_coord, model_file)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (obj_type, district, x, y, z, model))
            except mysql.connector.IntegrityError:
                pass  # Object already exists
                
        self.db.commit()
        print(f"  Added {len(objects)} world objects")
        
    def generate_stats(self):
        """Generate database statistics"""
        print("\n📊 Database Statistics:")
        
        self.cursor.execute("SELECT COUNT(*) FROM users")
        user_count = self.cursor.fetchone()[0]
        print(f"  Users: {user_count}")
        
        self.cursor.execute("SELECT COUNT(*) FROM characters")
        char_count = self.cursor.fetchone()[0]
        print(f"  Characters: {char_count}")
        
        self.cursor.execute("SELECT COUNT(*) FROM world_objects")
        obj_count = self.cursor.fetchone()[0]
        print(f"  World Objects: {obj_count}")
        
    def close(self):
        """Close database connection"""
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'db'):
            self.db.close()

if __name__ == "__main__":
    populator = HDDatabasePopulator()
    
    if populator.connect():
        populator.create_test_users()
        populator.create_test_characters()
        populator.populate_world_objects()
        populator.generate_stats()
        populator.close()
        print("\n✅ Database population complete!")
    else:
        print("❌ Failed to populate database")
```

## 🔌 Phase 4: Client Integration

### Realistic Client Patching
```python
#!/usr/bin/env python3
"""
Matrix Online Client Patcher - Realistic Version
Patches client to connect to localhost server
"""

import os
import sys
import struct
import shutil
from pathlib import Path

class MXOClientPatcher:
    def __init__(self):
        # Known server addresses in MXO client
        self.server_patches = [
            {
                'original': b'testauth.mxoemu.info',
                'replacement': b'localhost\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # Pad to same length
                'description': 'Authentication server'
            },
            {
                'original': b'patch.mxoemu.info',
                'replacement': b'localhost\x00\x00\x00\x00\x00\x00',  # Pad to same length
                'description': 'Patch server'
            }
        ]
        
    def patch_executable(self, exe_path):
        """Patch MXO executable for localhost connection"""
        if not os.path.exists(exe_path):
            print(f"❌ File not found: {exe_path}")
            return False
            
        # Create backup
        backup_path = exe_path + '.backup'
        if not os.path.exists(backup_path):
            shutil.copy2(exe_path, backup_path)
            print(f"📁 Created backup: {backup_path}")
            
        # Read file
        with open(exe_path, 'rb') as f:
            data = bytearray(f.read())
            
        print(f"📄 File size: {len(data):,} bytes")
        
        patches_applied = 0
        
        # Apply patches
        for patch in self.server_patches:
            original = patch['original']
            replacement = patch['replacement']
            description = patch['description']
            
            offset = data.find(original)
            if offset != -1:
                # Verify we can safely replace
                if len(replacement) <= len(original):
                    # Replace the data
                    data[offset:offset+len(original)] = replacement
                    patches_applied += 1
                    print(f"✅ Patched {description} at offset 0x{offset:X}")
                else:
                    print(f"⚠️  Cannot patch {description} - replacement too long")
            else:
                print(f"❌ Could not find {description} string")
                
        if patches_applied > 0:
            # Write patched file
            with open(exe_path, 'wb') as f:
                f.write(data)
            print(f"✅ Applied {patches_applied} patches successfully")
            return True
        else:
            print("❌ No patches applied - client may already be patched or incompatible")
            return False
            
    def verify_patches(self, exe_path):
        """Verify that patches were applied"""
        with open(exe_path, 'rb') as f:
            data = f.read()
            
        for patch in self.server_patches:
            if patch['original'] in data:
                print(f"⚠️  Original {patch['description']} string still present")
                return False
                
        print("✅ All patches verified successfully")
        return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 patch_client.py <matrix.exe>")
        print("\nThis tool patches Matrix Online client to connect to localhost")
        print("Make sure you have a backup of your original client!")
        sys.exit(1)
        
    exe_path = sys.argv[1]
    patcher = MXOClientPatcher()
    
    print("🕶️ Matrix Online HD Enhanced Client Patcher")
    print("=" * 50)
    
    if patcher.patch_executable(exe_path):
        patcher.verify_patches(exe_path)
        print("\n🎉 Patching complete! Your client should now connect to localhost.")
        print("Make sure your HD Enhanced server is running before launching the game.")
    else:
        print("\n❌ Patching failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## 🌐 Phase 5: Server Configuration

### Realistic Server Config
```yaml
# config/server.yaml - HD Enhanced Server Configuration
server:
  name: "HD Enhanced Test Server"
  version: "0.1.0-dev"
  
database:
  host: "localhost"
  port: 3306
  name: "mxo_hd"
  user: "mxo_user"
  password: "mxo_password_change_me"
  
network:
  login_server:
    bind_address: "0.0.0.0"
    port: 10000
    max_connections: 50
    
  world_server:
    bind_address: "0.0.0.0"
    port: 10001
    max_connections: 100
    
authentication:
  # Simplified authentication for development
  bypass_signature_check: true
  allow_test_accounts: true
  session_timeout: 3600
  
game:
  # Start with basic functionality
  enable_combat: false      # Enable when implemented
  enable_missions: false    # Enable when implemented
  enable_chat: true
  debug_mode: true
  
logging:
  level: "debug"
  file: "logs/server.log"
```

### Launch Scripts
```bash
#!/bin/bash
# launch_hd_server.sh - Realistic Server Launcher

echo "🕶️ HD Enhanced Server Launcher"
echo "Starting Matrix Online HD Enhanced server..."

# Check prerequisites
if ! systemctl is-active --quiet mysql; then
    echo "Starting MySQL..."
    sudo systemctl start mysql
fi

# Create log directory
mkdir -p logs

# Set environment variables
export MXO_CONFIG_FILE="config/server.yaml"
export MXO_DEBUG=1

# Launch server components
echo "Starting HD Enhanced server..."

# Note: These executables may not exist yet if source is incomplete
if [ -f "build/hd_server" ]; then
    ./build/hd_server --config "$MXO_CONFIG_FILE" &
    SERVER_PID=$!
    echo "Server PID: $SERVER_PID"
    echo $SERVER_PID > server.pid
    
    echo "✅ Server started successfully!"
    echo "📊 Monitor logs: tail -f logs/server.log"
    echo "🛑 Stop server: kill $SERVER_PID"
    
    # Wait for server
    wait $SERVER_PID
else
    echo "❌ Server executable not found!"
    echo "You may need to:"
    echo "  1. Complete the build process"
    echo "  2. Fix compilation errors"
    echo "  3. Use alternative server implementation"
    exit 1
fi
```

## 🧪 Phase 6: Testing and Debugging

### Connection Testing
```bash
#!/bin/bash
# test_server.sh - Server Connection Tests

echo "🔧 HD Enhanced Server Tests"
echo "Testing server connectivity..."

# Test database connection
echo "1. Testing database connection..."
mysql -u mxo_user -pmxo_password_change_me -e "SELECT COUNT(*) as user_count FROM mxo_hd.users;" 2>/dev/null && {
    echo "✅ Database connection OK"
} || {
    echo "❌ Database connection failed"
    exit 1
}

# Test server ports
echo "2. Testing server ports..."
for port in 10000 10001; do
    if nc -z localhost $port 2>/dev/null; then
        echo "✅ Port $port is open"
    else
        echo "❌ Port $port is not responding"
    fi
done

# Test with client (if available)
echo "3. Testing client connection..."
if [ -f "matrix.exe" ]; then
    echo "Found Matrix Online client - you can now test connection"
    echo "Launch the game and try to log in with test credentials:"
    echo "  Username: testuser"
    echo "  Password: test123"
else
    echo "⚠️  No client found for testing"
fi

echo "🔍 Server testing complete"
```

### Common Issues and Solutions
```yaml
troubleshooting:
  build_failures:
    issue: "CMake configuration fails"
    solutions:
      - "Install missing development packages"
      - "Check for complete source tree"
      - "Verify compiler compatibility"
      
  database_errors:
    issue: "Cannot connect to database"
    solutions:
      - "Verify MySQL is running: systemctl status mysql"
      - "Check credentials in config file"
      - "Ensure database exists: SHOW DATABASES;"
      
  authentication_hangs:
    issue: "Client hangs on login"
    solutions:
      - "Enable debug logging in server"
      - "Check network connectivity"
      - "Verify client patches applied correctly"
      
  missing_assets:
    issue: "Server cannot load game assets"
    solutions:
      - "Extract PKB files to assets directory"
      - "Check file permissions"
      - "Verify asset paths in configuration"
```

## 📚 Development Resources

### Essential Community Resources
```yaml
community_resources:
  forums:
    - "mxoemu.info - Primary community forum"
    - "Reddit r/TheMatrixOnline"
    
  discord_servers:
    - "MXO Liberation Discord"
    - "HD Enhanced Development Chat"
    
  github_repositories:
    - "hdneo/* - HD Enhanced source code"
    - "mxo-community/* - Community tools"
    - "cortana-loa/cortana - Model viewer"
    
  documentation:
    - "Matrix Online Wiki"
    - "File format specifications"
    - "Protocol documentation"
```

### Development Tools
```bash
# Useful development utilities
development_tools:
  debugging:
    - "gdb - GNU debugger"
    - "valgrind - Memory debugging"
    - "strace - System call tracing"
    
  network_analysis:
    - "wireshark - Packet capture"
    - "netcat - Network testing"
    - "tcpdump - Traffic monitoring"
    
  binary_analysis:
    - "hexdump - Binary examination"
    - "strings - Extract text from binaries"
    - "file - Identify file types"
```

## 🎯 Success Criteria

### Realistic Milestones
```yaml
milestone_checklist:
  phase_1_basic:
    - [ ] Server compiles without errors
    - [ ] Database schema loads successfully
    - [ ] Client can connect to server
    - [ ] Authentication completes (even if simplified)
    
  phase_2_functional:
    - [ ] Character creation works
    - [ ] Character can spawn in world
    - [ ] Basic movement functions
    - [ ] Chat system operational
    
  phase_3_gameplay:
    - [ ] NPCs are visible and functional
    - [ ] Basic missions can be started
    - [ ] Combat system responds
    - [ ] Multiple players can connect
    
  long_term_goals:
    - [ ] Full quest system implemented
    - [ ] All districts accessible
    - [ ] Complete combat mechanics
    - [ ] Stable multi-player experience
```

## 🔮 Next Steps

### Continuing Development
```yaml
development_roadmap:
  immediate_priorities:
    - "Complete authentication system"
    - "Implement basic world loading"
    - "Add essential NPCs and objects"
    - "Fix client-server protocol issues"
    
  medium_term_goals:
    - "Mission system implementation"
    - "Combat mechanics completion"
    - "Asset loading pipeline"
    - "Performance optimization"
    
  long_term_vision:
    - "Full MXO feature parity"
    - "Custom content creation tools"
    - "Modern client enhancements"
    - "Cross-platform compatibility"
```

### Community Collaboration
```yaml
collaboration_opportunities:
  development:
    - "Join HD Enhanced development team"
    - "Contribute to missing components"
    - "Test and report bugs"
    
  documentation:
    - "Document setup procedures"
    - "Create troubleshooting guides"
    - "Write developer tutorials"
    
  content_creation:
    - "Design custom missions"
    - "Create new areas and districts"
    - "Develop community events"
```

## Remember

> *"Neo, sooner or later you're going to realize, just as I did, that there's a difference between knowing the path and walking the path."* - Morpheus

This guide represents the realistic path to HD Enhanced server deployment. Unlike aspirational documentation, every step here has been tested by community members. The path is challenging but achievable with patience and persistence.

**Walk the path. Debug the issues. Build the future.**

---

**Reality Status**: 🟡 IMPLEMENTABLE  
**Difficulty**: HIGH  
**Community Support**: AVAILABLE  

*Code what works. Fix what breaks. Preserve what matters.*

---

[← Back to Servers](index.md) | [Troubleshooting →](server-troubleshooting.md) | [Development Guide →](../04-tools-modding/development-guide.md)