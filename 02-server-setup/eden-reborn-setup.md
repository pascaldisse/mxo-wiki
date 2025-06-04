# Eden Reborn Server Setup Guide
**The Community-Driven Matrix Online Revival**

> *"I'm going to show them a world without you. A world without rules and controls, without borders or boundaries. A world where anything is possible."* - Neo

🚧 **Development Status**: Planning & Research Phase (Started June 3, 2025)

## Project Overview

Eden Reborn represents the next evolution in Matrix Online emulation - a completely community-driven, open-source server built from the ground up with modern technology and the spirit of digital liberation.

### Vision
- **100% Open Source** - Every line of code public from day one
- **Community Governed** - Decisions made collectively
- **Modern Architecture** - Cloud-native, scalable design
- **Enhanced Experience** - Improvements while preserving authenticity
- **No Gatekeeping** - Knowledge and tools freely shared

## Current Development Status

### What's Working
📋 **Planning Phase**
- Project structure defined
- Community governance established
- Technical architecture planned
- Development roadmap created

### In Development
🔧 **Foundation Work**
- Core server framework selection
- Database schema design
- Network protocol analysis
- Client compatibility research

### Planned Features
🚀 **Future Goals**
- Full combat system implementation
- Complete mission framework
- Enhanced graphics support
- Cross-platform compatibility
- Procedural content generation
- Community modding support

## Prerequisites

### For Development
- **Git** - Version control
- **Docker** - Containerization
- **Go 1.21+** or **Rust** (language TBD)
- **PostgreSQL 15+** - Database
- **Redis** - Caching layer
- **Basic networking knowledge**
- **Matrix Online client files**

### For Testing
- **Matrix Online client** (any version)
- **4GB RAM minimum**
- **Broadband internet**
- **Windows/Linux/macOS**

## Development Setup

### 1. Clone the Repository
```bash
# Main repository (when public)
git clone https://github.com/eden-reborn/server.git
cd server

# Development branch
git checkout develop
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

#### Essential Environment Variables
```env
# Server Configuration
SERVER_NAME="Eden Reborn Development"
SERVER_PORT=11000
AUTH_PORT=11001
WORLD_PORT=11002

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=eden_reborn
DB_USER=mxo_user
DB_PASS=your_secure_password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Development Settings
DEBUG_MODE=true
LOG_LEVEL=debug
AUTO_RELOAD=true
```

### 3. Database Initialization
```bash
# Start PostgreSQL with Docker
docker run -d \
  --name eden-postgres \
  -e POSTGRES_DB=eden_reborn \
  -e POSTGRES_USER=mxo_user \
  -e POSTGRES_PASSWORD=your_secure_password \
  -p 5432:5432 \
  postgres:15-alpine

# Run migrations (when available)
make migrate
```

### 4. Build and Run
```bash
# Using Make
make build
make run

# Or using Docker Compose
docker-compose up -d
```

## Architecture Overview

### Microservices Design
```yaml
services:
  gateway:
    description: "API Gateway and load balancer"
    port: 11000
    technology: "Traefik/Nginx"
    
  auth_service:
    description: "Authentication and account management"
    port: 11001
    features:
      - JWT token generation
      - Account creation/login
      - Session management
      
  world_service:
    description: "Game world state and physics"
    port: 11002
    features:
      - Zone management
      - NPC coordination
      - Physics simulation
      
  combat_service:
    description: "Combat system and calculations"
    port: 11003
    features:
      - D100 roll system
      - Ability processing
      - Damage calculation
      
  chat_service:
    description: "Communication systems"
    port: 11004
    features:
      - Global/local chat
      - Private messaging
      - Faction channels
      
  mission_service:
    description: "Quest and mission logic"
    port: 11005
    features:
      - Mission state tracking
      - Objective processing
      - Reward distribution
```

### Technology Stack
```yaml
backend:
  language: "Go/Rust (TBD via community vote)"
  framework: "Gin/Echo (Go) or Actix (Rust)"
  database: "PostgreSQL with TimescaleDB"
  cache: "Redis with persistence"
  message_queue: "RabbitMQ/NATS"
  
infrastructure:
  container: "Docker & Kubernetes"
  monitoring: "Prometheus + Grafana"
  logging: "ELK Stack"
  ci_cd: "GitHub Actions"
  deployment: "Kubernetes/Docker Swarm"
  
protocols:
  rpc: "gRPC for inter-service"
  websocket: "For real-time updates"
  rest: "For web interfaces"
  custom: "MXO protocol reverse-engineered"
```

## Contributing to Eden Reborn

### Development Process
1. **Join Discord** - Coordinate with team
2. **Pick an Issue** - From GitHub project board
3. **Create Branch** - feature/your-feature-name
4. **Write Tests** - TDD encouraged
5. **Submit PR** - With clear description
6. **Code Review** - Community feedback
7. **Merge** - After approval

### Coding Standards
```go
// Example Go code style
package combat

import (
    "context"
    "github.com/eden-reborn/server/pkg/models"
)

// CalculateDamage implements the D100 combat system
func CalculateDamage(ctx context.Context, attacker, defender *models.Character) (int, error) {
    // Implementation follows MXO combat rules
    // All code must be documented
    // Tests required for all functions
}
```

### Community Governance
- **Weekly Meetings** - Discord voice chat
- **Decision Making** - Community votes
- **Transparency** - All discussions public
- **Documentation** - Every decision recorded

## Testing the Server

### Unit Tests
```bash
# Run all tests
make test

# Run specific package tests
go test ./pkg/combat/...

# Run with coverage
make test-coverage
```

### Integration Tests
```bash
# Start test environment
make test-env-up

# Run integration suite
make test-integration

# Clean up
make test-env-down
```

### Client Connection Test
```bash
# Patch your client to point to localhost
# Use the client patcher tool
./tools/client-patcher --server localhost

# Or manually hex edit:
# Change mxoemu.info -> localhost
```

## Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check connection
psql -h localhost -U mxo_user -d eden_reborn

# Reset database if needed
make db-reset
```

#### Port Already in Use
```bash
# Find process using port
lsof -i :11000

# Kill process if needed
kill -9 <PID>

# Or change port in .env
```

#### Client Can't Connect
```bash
# Check server is running
curl http://localhost:11000/health

# Check firewall
sudo ufw allow 11000:11010/tcp

# Verify client patch
strings matrix.exe | grep localhost
```

## Monitoring & Administration

### Grafana Dashboard
```bash
# Access at http://localhost:3000
# Default login: admin/admin

# Key metrics:
- Active connections
- Server performance
- Database queries
- Error rates
```

### Admin Commands
```bash
# Server management
make server-status
make server-restart
make server-backup

# Player management (via CLI tool)
./eden-admin player list
./eden-admin player kick <username>
./eden-admin player ban <username> <reason>
```

## Roadmap & Milestones

### Phase 1: Foundation (Q1 2025)
- [x] Project setup and governance
- [ ] Core architecture implementation
- [ ] Basic authentication system
- [ ] Character creation/loading
- [ ] Zone loading and navigation

### Phase 2: Core Systems (Q2 2025)
- [ ] Combat system (D100)
- [ ] Ability system
- [ ] Inventory management
- [ ] Basic NPCs
- [ ] Chat system

### Phase 3: Content (Q3 2025)
- [ ] Mission framework
- [ ] Vendor system
- [ ] Faction mechanics
- [ ] Social features
- [ ] Basic events

### Phase 4: Enhancement (Q4 2025)
- [ ] Advanced combat features
- [ ] Performance optimization
- [ ] Mod support
- [ ] Enhanced graphics
- [ ] Mobile companion app

## Community Resources

### Communication
- **Discord**: [Join Eden Reborn](https://discord.gg/eden-reborn)
- **Forums**: Coming soon
- **Wiki**: This documentation
- **GitHub**: [github.com/eden-reborn](https://github.com/eden-reborn)

### Getting Help
- **#dev-help** - Technical questions
- **#general** - Community chat
- **#announcements** - Updates
- **#contribute** - How to help

### Learning Resources
- [Go Tutorial](https://tour.golang.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Docker Guide](https://docs.docker.com/get-started/)
- [MXO Technical Docs](../03-technical/)

## The Vision Lives On

Eden Reborn isn't just another server emulator - it's a community-driven revolution in game preservation. By building everything in the open, with modern tools and practices, we ensure The Matrix Online will never die again.

### Core Values
1. **Transparency** - All development public
2. **Inclusivity** - Everyone can contribute
3. **Innovation** - Modern tech, classic feel
4. **Preservation** - Keeping MXO alive forever
5. **Liberation** - Free from corporate control

### Join the Revolution
Whether you're a developer, tester, documenter, or just passionate about The Matrix Online, there's a place for you in Eden Reborn.

**Together, we're not just running a server. We're building a home.**

*"The Matrix is everywhere. It is all around us."* - And now, it's ours to shape.

---

[← Back to Server Setup](index.md) | [Development Docs →](../07-development/)