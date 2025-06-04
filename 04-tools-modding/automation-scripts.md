# Automation Scripts for Matrix Online Development
**Automate the Liberation**

> *"Programs hacking programs. Why is it so much easier to run?"*

Collection of automation scripts, utilities, and workflows to streamline Matrix Online development, testing, and maintenance tasks.

## 🎯 Script Categories

### Build Automation
### Testing Automation  
### Deployment Scripts
### Maintenance Utilities
### Content Processing
### Development Workflows

## 🔧 Build Automation Scripts

### Universal Build Script
```bash
#!/bin/bash
# build_mxo_project.sh - Universal MXO project builder

set -e

PROJECT_TYPE=${1:-"auto"}
BUILD_TYPE=${2:-"release"}
CLEAN_BUILD=${3:-"false"}

echo "🔨 Matrix Online Project Builder"
echo "Project Type: $PROJECT_TYPE"
echo "Build Type: $BUILD_TYPE"

# Detect project type if auto
if [ "$PROJECT_TYPE" = "auto" ]; then
    if [ -f "CMakeLists.txt" ]; then
        PROJECT_TYPE="cmake"
    elif [ -f "Makefile" ]; then
        PROJECT_TYPE="make"
    elif [ -f "*.sln" ]; then
        PROJECT_TYPE="msbuild"
    elif [ -f "package.json" ]; then
        PROJECT_TYPE="node"
    else
        echo "❌ Could not detect project type"
        exit 1
    fi
fi

# Clean build if requested
if [ "$CLEAN_BUILD" = "true" ]; then
    echo "🧹 Cleaning previous build..."
    case $PROJECT_TYPE in
        "cmake")
            rm -rf build/
            ;;
        "make")
            make clean
            ;;
        "node")
            rm -rf node_modules/ dist/
            ;;
    esac
fi

# Build based on project type
case $PROJECT_TYPE in
    "cmake")
        echo "📦 Building CMake project..."
        mkdir -p build
        cd build
        if [ "$BUILD_TYPE" = "debug" ]; then
            cmake -DCMAKE_BUILD_TYPE=Debug ..
        else
            cmake -DCMAKE_BUILD_TYPE=Release ..
        fi
        make -j$(nproc)
        ;;
    "make")
        echo "📦 Building Make project..."
        if [ "$BUILD_TYPE" = "debug" ]; then
            make DEBUG=1 -j$(nproc)
        else
            make -j$(nproc)
        fi
        ;;
    "msbuild")
        echo "📦 Building .NET project..."
        if [ "$BUILD_TYPE" = "debug" ]; then
            dotnet build --configuration Debug
        else
            dotnet build --configuration Release
        fi
        ;;
    "node")
        echo "📦 Building Node.js project..."
        npm install
        npm run build
        ;;
    *)
        echo "❌ Unsupported project type: $PROJECT_TYPE"
        exit 1
        ;;
esac

echo "✅ Build completed successfully!"
```

### Dependency Check Script
```bash
#!/bin/bash
# check_dependencies.sh - Verify development dependencies

echo "🔍 Checking Matrix Online Development Dependencies"

# Function to check command availability
check_command() {
    if command -v $1 &> /dev/null; then
        echo "✅ $1: $(which $1)"
        if [ "$2" != "" ]; then
            echo "   Version: $($1 $2 2>/dev/null || echo 'Unknown')"
        fi
    else
        echo "❌ $1: Not found"
        return 1
    fi
}

# Function to check library availability
check_library() {
    if ldconfig -p | grep -q $1; then
        echo "✅ Library $1: Available"
    else
        echo "❌ Library $1: Not found"
        return 1
    fi
}

echo "📋 Core Development Tools:"
check_command "git" "--version"
check_command "gcc" "--version"
check_command "g++" "--version"
check_command "make" "--version"
check_command "cmake" "--version"

echo ""
echo "📋 Scripting Languages:"
check_command "python3" "--version"
check_command "node" "--version"
check_command "dotnet" "--version"

echo ""
echo "📋 Development Libraries:"
check_library "libssl"
check_library "libmysqlclient"
check_library "libgl"

echo ""
echo "📋 Specialized Tools:"
check_command "hexdump" ""
check_command "gdb" "--version"
check_command "valgrind" "--version"

echo ""
echo "🎯 Dependency check completed!"
```

### Cross-Platform Build Script
```python
#!/usr/bin/env python3
# cross_platform_build.py - Build for multiple platforms

import os
import sys
import subprocess
import platform
import argparse

class CrossPlatformBuilder:
    def __init__(self):
        self.system = platform.system().lower()
        self.supported_platforms = ['linux', 'windows', 'darwin']
        
    def detect_compiler(self):
        """Detect available compilers"""
        compilers = {
            'gcc': self.check_command('gcc'),
            'clang': self.check_command('clang'),
            'msvc': self.check_command('cl') if self.system == 'windows' else False
        }
        return {k: v for k, v in compilers.items() if v}
    
    def check_command(self, cmd):
        """Check if command is available"""
        try:
            subprocess.run([cmd, '--version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def build_for_platform(self, target_platform, compiler='auto'):
        """Build for specific platform"""
        print(f"🔨 Building for {target_platform}...")
        
        if target_platform == 'linux':
            return self.build_linux(compiler)
        elif target_platform == 'windows':
            return self.build_windows(compiler)
        elif target_platform == 'darwin':
            return self.build_macos(compiler)
        else:
            print(f"❌ Unsupported platform: {target_platform}")
            return False
    
    def build_linux(self, compiler):
        """Build for Linux"""
        if compiler == 'auto':
            compiler = 'gcc' if self.check_command('gcc') else 'clang'
        
        env = os.environ.copy()
        env['CC'] = compiler
        env['CXX'] = compiler + '++'
        
        commands = [
            ['mkdir', '-p', 'build/linux'],
            ['cmake', '-B', 'build/linux', '-DCMAKE_BUILD_TYPE=Release', '.'],
            ['make', '-C', 'build/linux', '-j4']
        ]
        
        return self.run_commands(commands, env)
    
    def build_windows(self, compiler):
        """Build for Windows"""
        if self.system != 'windows':
            print("🔄 Cross-compiling for Windows from Unix...")
            # Cross-compilation setup would go here
            compiler = 'x86_64-w64-mingw32-gcc'
        
        commands = [
            ['mkdir', '-p', 'build/windows'],
            ['cmake', '-B', 'build/windows', 
             '-DCMAKE_TOOLCHAIN_FILE=cmake/windows.cmake', '.'],
            ['make', '-C', 'build/windows', '-j4']
        ]
        
        return self.run_commands(commands)
    
    def build_macos(self, compiler):
        """Build for macOS"""
        if compiler == 'auto':
            compiler = 'clang'
        
        env = os.environ.copy()
        env['CC'] = compiler
        env['CXX'] = compiler + '++'
        
        commands = [
            ['mkdir', '-p', 'build/macos'],
            ['cmake', '-B', 'build/macos', '-DCMAKE_BUILD_TYPE=Release', '.'],
            ['make', '-C', 'build/macos', '-j4']
        ]
        
        return self.run_commands(commands, env)
    
    def run_commands(self, commands, env=None):
        """Execute command sequence"""
        for cmd in commands:
            try:
                print(f"▶ {' '.join(cmd)}")
                subprocess.run(cmd, check=True, env=env)
            except subprocess.CalledProcessError as e:
                print(f"❌ Command failed: {e}")
                return False
        return True

def main():
    parser = argparse.ArgumentParser(description='Cross-platform MXO builder')
    parser.add_argument('--platforms', nargs='+', 
                       choices=['linux', 'windows', 'darwin', 'all'],
                       default=['all'], help='Target platforms')
    parser.add_argument('--compiler', default='auto',
                       help='Compiler to use (gcc, clang, msvc, auto)')
    
    args = parser.parse_args()
    
    builder = CrossPlatformBuilder()
    
    if 'all' in args.platforms:
        platforms = builder.supported_platforms
    else:
        platforms = args.platforms
    
    print("🚀 Matrix Online Cross-Platform Builder")
    print(f"Target platforms: {', '.join(platforms)}")
    
    success_count = 0
    for platform in platforms:
        if builder.build_for_platform(platform, args.compiler):
            print(f"✅ {platform} build successful")
            success_count += 1
        else:
            print(f"❌ {platform} build failed")
    
    print(f"\n🎯 Build Summary: {success_count}/{len(platforms)} successful")
    return success_count == len(platforms)

if __name__ == '__main__':
    sys.exit(0 if main() else 1)
```

## 🧪 Testing Automation Scripts

### Automated Test Runner
```bash
#!/bin/bash
# run_all_tests.sh - Comprehensive test automation

PROJECT_ROOT=$(dirname $(realpath $0))/..
TEST_RESULTS_DIR="$PROJECT_ROOT/test_results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🧪 Matrix Online Test Automation Suite"
echo "Timestamp: $TIMESTAMP"

# Create results directory
mkdir -p "$TEST_RESULTS_DIR"

# Function to run test suite
run_test_suite() {
    local suite_name=$1
    local test_command=$2
    local log_file="$TEST_RESULTS_DIR/${suite_name}_${TIMESTAMP}.log"
    
    echo "🔍 Running $suite_name tests..."
    echo "Log file: $log_file"
    
    if eval "$test_command" > "$log_file" 2>&1; then
        echo "✅ $suite_name: PASSED"
        return 0
    else
        echo "❌ $suite_name: FAILED"
        echo "   Check log: $log_file"
        return 1
    fi
}

# Unit Tests
run_test_suite "Unit Tests" "make test_unit"

# Integration Tests  
run_test_suite "Integration Tests" "make test_integration"

# File Format Tests
run_test_suite "File Format Tests" "python3 tests/test_file_formats.py"

# Server Tests
run_test_suite "Server Tests" "python3 tests/test_server.py"

# Performance Tests
run_test_suite "Performance Tests" "python3 tests/test_performance.py"

# Memory Leak Tests
run_test_suite "Memory Tests" "valgrind --leak-check=full --error-exitcode=1 ./test_memory"

# Generate test report
echo "📊 Generating test report..."
cat > "$TEST_RESULTS_DIR/test_report_${TIMESTAMP}.html" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>MXO Test Report - $TIMESTAMP</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .pass { color: green; }
        .fail { color: red; }
        pre { background: #f5f5f5; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Matrix Online Test Report</h1>
    <p>Generated: $TIMESTAMP</p>
    
    <h2>Test Results</h2>
    <ul>
EOF

# Process test results
for log_file in "$TEST_RESULTS_DIR"/*_${TIMESTAMP}.log; do
    if [ -f "$log_file" ]; then
        suite_name=$(basename "$log_file" | sed "s/_${TIMESTAMP}.log//")
        if grep -q "PASSED\|SUCCESS\|OK" "$log_file"; then
            echo "        <li class=\"pass\">✅ $suite_name: PASSED</li>" >> "$TEST_RESULTS_DIR/test_report_${TIMESTAMP}.html"
        else
            echo "        <li class=\"fail\">❌ $suite_name: FAILED</li>" >> "$TEST_RESULTS_DIR/test_report_${TIMESTAMP}.html"
        fi
    fi
done

cat >> "$TEST_RESULTS_DIR/test_report_${TIMESTAMP}.html" << EOF
    </ul>
    
    <h2>Detailed Logs</h2>
    <!-- Detailed logs would be included here -->
    
</body>
</html>
EOF

echo "✅ Test automation completed!"
echo "📋 Report: $TEST_RESULTS_DIR/test_report_${TIMESTAMP}.html"
```

### File Format Validation Script
```python
#!/usr/bin/env python3
# validate_file_formats.py - Automated file format testing

import os
import sys
import struct
import hashlib
from pathlib import Path

class FileFormatValidator:
    def __init__(self, test_data_dir):
        self.test_data_dir = Path(test_data_dir)
        self.results = {}
        
    def validate_cnb_files(self):
        """Validate CNB file format"""
        print("🔍 Validating CNB files...")
        cnb_files = list(self.test_data_dir.glob("*.cnb"))
        
        for cnb_file in cnb_files:
            try:
                with open(cnb_file, 'rb') as f:
                    # Read header
                    header = f.read(16)
                    if len(header) < 16:
                        self.results[cnb_file.name] = "❌ File too small"
                        continue
                    
                    # Check magic number (hypothetical)
                    magic = struct.unpack('<I', header[:4])[0]
                    if magic == 0x424E43:  # "CNB"
                        self.results[cnb_file.name] = "✅ Valid CNB format"
                    else:
                        self.results[cnb_file.name] = f"❌ Invalid magic: {magic:08x}"
                        
            except Exception as e:
                self.results[cnb_file.name] = f"❌ Error: {e}"
    
    def validate_pkb_files(self):
        """Validate PKB archive format"""
        print("🔍 Validating PKB files...")
        pkb_files = list(self.test_data_dir.glob("*.pkb"))
        
        for pkb_file in pkb_files:
            try:
                with open(pkb_file, 'rb') as f:
                    # Read header
                    header = f.read(16)
                    if len(header) < 16:
                        self.results[pkb_file.name] = "❌ File too small"
                        continue
                    
                    # Check PKB signature
                    if header[:4] == b'PKB\x00':
                        self.results[pkb_file.name] = "✅ Valid PKB format"
                    else:
                        self.results[pkb_file.name] = "❌ Invalid PKB signature"
                        
            except Exception as e:
                self.results[pkb_file.name] = f"❌ Error: {e}"
    
    def validate_prop_files(self):
        """Validate PROP file format"""
        print("🔍 Validating PROP files...")
        prop_files = list(self.test_data_dir.glob("*.prop"))
        
        for prop_file in prop_files:
            try:
                with open(prop_file, 'rb') as f:
                    # Basic size check
                    file_size = os.path.getsize(prop_file)
                    if file_size > 0:
                        self.results[prop_file.name] = "✅ PROP file exists"
                    else:
                        self.results[prop_file.name] = "❌ Empty PROP file"
                        
            except Exception as e:
                self.results[prop_file.name] = f"❌ Error: {e}"
    
    def generate_report(self):
        """Generate validation report"""
        print("\n📊 File Format Validation Report")
        print("=" * 50)
        
        total_files = len(self.results)
        passed_files = sum(1 for result in self.results.values() if "✅" in result)
        
        for filename, result in sorted(self.results.items()):
            print(f"{filename:30} {result}")
        
        print("=" * 50)
        print(f"Total files: {total_files}")
        print(f"Passed: {passed_files}")
        print(f"Failed: {total_files - passed_files}")
        print(f"Success rate: {passed_files/total_files*100:.1f}%")
        
        return passed_files == total_files

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_file_formats.py <test_data_directory>")
        sys.exit(1)
    
    test_data_dir = sys.argv[1]
    if not os.path.exists(test_data_dir):
        print(f"❌ Test data directory not found: {test_data_dir}")
        sys.exit(1)
    
    validator = FileFormatValidator(test_data_dir)
    
    # Run all validations
    validator.validate_cnb_files()
    validator.validate_pkb_files() 
    validator.validate_prop_files()
    
    # Generate report
    success = validator.generate_report()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
```

## 🚀 Deployment Scripts

### Automated Deployment Script
```bash
#!/bin/bash
# deploy_mxo_server.sh - Automated server deployment

DEPLOYMENT_ENV=${1:-"staging"}
VERSION=${2:-"latest"}
CONFIG_DIR="/etc/mxo"
SERVICE_NAME="mxo-server"

echo "🚀 Matrix Online Server Deployment"
echo "Environment: $DEPLOYMENT_ENV"
echo "Version: $VERSION"

# Validate environment
case $DEPLOYMENT_ENV in
    "development"|"staging"|"production")
        echo "✅ Valid environment: $DEPLOYMENT_ENV"
        ;;
    *)
        echo "❌ Invalid environment. Use: development, staging, or production"
        exit 1
        ;;
esac

# Pre-deployment checks
echo "🔍 Running pre-deployment checks..."

# Check disk space
AVAILABLE_SPACE=$(df / | tail -1 | awk '{print $4}')
if [ "$AVAILABLE_SPACE" -lt 1000000 ]; then
    echo "❌ Insufficient disk space"
    exit 1
fi

# Check service status
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "⚠️  Service is running, will restart after deployment"
    RESTART_REQUIRED=true
else
    RESTART_REQUIRED=false
fi

# Backup current deployment
echo "💾 Creating backup..."
BACKUP_DIR="/backup/mxo/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -d "/opt/mxo" ]; then
    cp -r /opt/mxo "$BACKUP_DIR/"
    echo "✅ Backup created: $BACKUP_DIR"
fi

# Download new version
echo "📦 Downloading version $VERSION..."
if [ "$VERSION" = "latest" ]; then
    DOWNLOAD_URL="https://releases.example.com/mxo/latest.tar.gz"
else
    DOWNLOAD_URL="https://releases.example.com/mxo/v${VERSION}.tar.gz"
fi

# Create deployment directory
mkdir -p /opt/mxo-new

# Download and extract
if wget -O /tmp/mxo-release.tar.gz "$DOWNLOAD_URL"; then
    tar -xzf /tmp/mxo-release.tar.gz -C /opt/mxo-new
    echo "✅ Download and extraction completed"
else
    echo "❌ Download failed"
    exit 1
fi

# Apply configuration
echo "⚙️  Applying configuration..."
cp "$CONFIG_DIR/$DEPLOYMENT_ENV.conf" /opt/mxo-new/config/server.conf
cp "$CONFIG_DIR/database.conf" /opt/mxo-new/config/

# Database migration
echo "🗄️  Running database migrations..."
cd /opt/mxo-new
./scripts/migrate_database.sh

# Run deployment tests
echo "🧪 Running deployment tests..."
if ./scripts/test_deployment.sh; then
    echo "✅ Deployment tests passed"
else
    echo "❌ Deployment tests failed"
    rm -rf /opt/mxo-new
    exit 1
fi

# Atomic deployment switch
echo "🔄 Switching to new deployment..."
if [ -d "/opt/mxo" ]; then
    mv /opt/mxo /opt/mxo-old
fi
mv /opt/mxo-new /opt/mxo

# Update service configuration
systemctl daemon-reload

# Restart service if needed
if [ "$RESTART_REQUIRED" = true ]; then
    echo "🔄 Restarting service..."
    systemctl restart $SERVICE_NAME
    
    # Wait for service to start
    sleep 5
    
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo "✅ Service restarted successfully"
    else
        echo "❌ Service failed to start"
        # Rollback
        echo "🔙 Rolling back..."
        systemctl stop $SERVICE_NAME
        rm -rf /opt/mxo
        mv /opt/mxo-old /opt/mxo
        systemctl start $SERVICE_NAME
        exit 1
    fi
else
    echo "🔄 Starting service..."
    systemctl start $SERVICE_NAME
fi

# Post-deployment verification
echo "✅ Running post-deployment checks..."
sleep 10

# Check service health
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

# Cleanup
echo "🧹 Cleaning up..."
rm -rf /opt/mxo-old
rm -f /tmp/mxo-release.tar.gz

echo "🎉 Deployment completed successfully!"
echo "📝 Deployment log: /var/log/mxo/deployment.log"
```

## 🔧 Maintenance Utilities

### Database Maintenance Script
```bash
#!/bin/bash
# maintain_database.sh - Automated database maintenance

DB_NAME="mxo_database"
DB_USER="mxo_admin"
BACKUP_DIR="/backup/database"
LOG_FILE="/var/log/mxo/maintenance.log"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🔧 Starting database maintenance"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Full database backup
log "💾 Creating database backup..."
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
mysqldump --single-transaction --routines --triggers "$DB_NAME" > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    log "✅ Backup created: $BACKUP_FILE"
    gzip "$BACKUP_FILE"
else
    log "❌ Backup failed"
    exit 1
fi

# Database optimization
log "⚡ Optimizing database tables..."
mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" << EOF
OPTIMIZE TABLE accounts;
OPTIMIZE TABLE characters;
OPTIMIZE TABLE login_log;
OPTIMIZE TABLE player_missions;
ANALYZE TABLE accounts;
ANALYZE TABLE characters;
EOF

# Clean old log entries
log "🧹 Cleaning old log entries..."
mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" << EOF
DELETE FROM login_log WHERE timestamp < DATE_SUB(NOW(), INTERVAL 90 DAY);
DELETE FROM error_log WHERE timestamp < DATE_SUB(NOW(), INTERVAL 30 DAY);
DELETE FROM audit_log WHERE timestamp < DATE_SUB(NOW(), INTERVAL 180 DAY);
EOF

# Clean old backups (keep 30 days)
log "🗑️  Cleaning old backups..."
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +30 -delete

# Generate database statistics
log "📊 Generating database statistics..."
mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" << EOF
SELECT 
    'accounts' as table_name,
    COUNT(*) as row_count,
    COUNT(CASE WHEN last_login > DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as active_30days
FROM accounts
UNION ALL
SELECT 
    'characters' as table_name,
    COUNT(*) as row_count,
    AVG(level) as avg_level
FROM characters;
EOF

log "✅ Database maintenance completed"
```

### Log Rotation and Cleanup
```python
#!/usr/bin/env python3
# cleanup_logs.py - Automated log management

import os
import sys
import gzip
import shutil
import datetime
from pathlib import Path

class LogManager:
    def __init__(self, config):
        self.config = config
        self.today = datetime.date.today()
        
    def rotate_logs(self):
        """Rotate current logs"""
        print("🔄 Rotating current logs...")
        
        for log_config in self.config['logs']:
            log_path = Path(log_config['path'])
            
            if not log_path.exists():
                continue
                
            # Create rotated filename
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            rotated_path = log_path.with_suffix(f'.{timestamp}{log_path.suffix}')
            
            # Rotate log
            shutil.move(str(log_path), str(rotated_path))
            
            # Compress if configured
            if log_config.get('compress', True):
                self.compress_file(rotated_path)
                
            # Create new empty log
            log_path.touch()
            os.chmod(log_path, 0o644)
            
            print(f"✅ Rotated: {log_path.name}")
    
    def compress_file(self, file_path):
        """Compress log file"""
        compressed_path = file_path.with_suffix(file_path.suffix + '.gz')
        
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove original
        file_path.unlink()
        print(f"🗜️  Compressed: {compressed_path.name}")
    
    def cleanup_old_logs(self):
        """Remove old log files"""
        print("🧹 Cleaning up old logs...")
        
        for log_config in self.config['logs']:
            log_dir = Path(log_config['path']).parent
            retention_days = log_config.get('retention_days', 30)
            cutoff_date = self.today - datetime.timedelta(days=retention_days)
            
            # Find old log files
            pattern = f"*{Path(log_config['path']).suffix}*"
            for log_file in log_dir.glob(pattern):
                if self.is_old_log(log_file, cutoff_date):
                    log_file.unlink()
                    print(f"🗑️  Removed: {log_file.name}")
    
    def is_old_log(self, log_file, cutoff_date):
        """Check if log file is older than cutoff"""
        # Extract date from filename
        parts = log_file.stem.split('_')
        for part in parts:
            if len(part) == 8 and part.isdigit():
                try:
                    file_date = datetime.datetime.strptime(part, '%Y%m%d').date()
                    return file_date < cutoff_date
                except ValueError:
                    continue
        
        # Fallback to file modification time
        mod_time = datetime.date.fromtimestamp(log_file.stat().st_mtime)
        return mod_time < cutoff_date
    
    def generate_report(self):
        """Generate log management report"""
        print("\n📊 Log Management Report")
        print("=" * 40)
        
        total_size = 0
        file_count = 0
        
        for log_config in self.config['logs']:
            log_dir = Path(log_config['path']).parent
            log_files = list(log_dir.glob(f"*{Path(log_config['path']).suffix}*"))
            
            section_size = sum(f.stat().st_size for f in log_files if f.is_file())
            total_size += section_size
            file_count += len(log_files)
            
            print(f"{log_config['name']:20} {len(log_files):3} files  {section_size/1024/1024:.1f} MB")
        
        print("=" * 40)
        print(f"{'Total':20} {file_count:3} files  {total_size/1024/1024:.1f} MB")

# Configuration
LOG_CONFIG = {
    'logs': [
        {
            'name': 'Server Logs',
            'path': '/var/log/mxo/server.log',
            'retention_days': 30,
            'compress': True
        },
        {
            'name': 'Access Logs', 
            'path': '/var/log/mxo/access.log',
            'retention_days': 90,
            'compress': True
        },
        {
            'name': 'Error Logs',
            'path': '/var/log/mxo/error.log',
            'retention_days': 180,
            'compress': True
        }
    ]
}

def main():
    print("📝 Matrix Online Log Management")
    
    manager = LogManager(LOG_CONFIG)
    
    # Rotate current logs
    manager.rotate_logs()
    
    # Clean up old logs
    manager.cleanup_old_logs()
    
    # Generate report
    manager.generate_report()
    
    print("✅ Log management completed!")

if __name__ == '__main__':
    main()
```

## 📦 Content Processing Scripts

### Asset Processing Pipeline
```python
#!/usr/bin/env python3
# process_game_assets.py - Automated asset processing

import os
import sys
import json
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

class AssetProcessor:
    def __init__(self, input_dir, output_dir, num_workers=4):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.num_workers = num_workers
        self.processed_count = 0
        self.error_count = 0
        
    def process_all_assets(self):
        """Process all assets in input directory"""
        print(f"🔄 Processing assets from {self.input_dir}")
        print(f"📁 Output directory: {self.output_dir}")
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all asset files
        asset_files = []
        for ext in ['.prop', '.cnb', '.pkb', '.tga', '.bmp']:
            asset_files.extend(self.input_dir.rglob(f'*{ext}'))
        
        print(f"📊 Found {len(asset_files)} asset files")
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            future_to_file = {
                executor.submit(self.process_asset, asset_file): asset_file
                for asset_file in asset_files
            }
            
            for future in as_completed(future_to_file):
                asset_file = future_to_file[future]
                try:
                    result = future.result()
                    if result:
                        self.processed_count += 1
                        if self.processed_count % 100 == 0:
                            print(f"✅ Processed {self.processed_count} files...")
                    else:
                        self.error_count += 1
                except Exception as e:
                    print(f"❌ Error processing {asset_file}: {e}")
                    self.error_count += 1
        
        print(f"🎯 Processing complete: {self.processed_count} successful, {self.error_count} errors")
    
    def process_asset(self, asset_file):
        """Process individual asset file"""
        try:
            # Determine file type and process accordingly
            suffix = asset_file.suffix.lower()
            
            if suffix == '.prop':
                return self.process_prop_file(asset_file)
            elif suffix == '.cnb':
                return self.process_cnb_file(asset_file)
            elif suffix == '.pkb':
                return self.process_pkb_file(asset_file)
            elif suffix in ['.tga', '.bmp']:
                return self.process_image_file(asset_file)
            else:
                return self.copy_file(asset_file)
                
        except Exception as e:
            print(f"❌ Error processing {asset_file}: {e}")
            return False
    
    def process_prop_file(self, prop_file):
        """Process PROP 3D model file"""
        # Create metadata
        metadata = self.create_metadata(prop_file)
        metadata['type'] = '3d_model'
        metadata['format'] = 'prop'
        
        # Copy file and create metadata
        output_file = self.get_output_path(prop_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy original file
        with open(prop_file, 'rb') as src, open(output_file, 'wb') as dst:
            dst.write(src.read())
        
        # Save metadata
        metadata_file = output_file.with_suffix('.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return True
    
    def process_cnb_file(self, cnb_file):
        """Process CNB cutscene file"""
        metadata = self.create_metadata(cnb_file)
        metadata['type'] = 'cutscene'
        metadata['format'] = 'cnb'
        
        # Analyze CNB structure
        with open(cnb_file, 'rb') as f:
            header = f.read(16)
            if len(header) >= 4:
                # Check for CNB magic number
                import struct
                magic = struct.unpack('<I', header[:4])[0]
                metadata['magic'] = f"0x{magic:08x}"
                metadata['valid'] = magic == 0x424E43  # "CNB"
        
        # Copy and save metadata
        output_file = self.get_output_path(cnb_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(cnb_file, 'rb') as src, open(output_file, 'wb') as dst:
            dst.write(src.read())
        
        metadata_file = output_file.with_suffix('.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return True
    
    def process_pkb_file(self, pkb_file):
        """Process PKB archive file"""
        metadata = self.create_metadata(pkb_file)
        metadata['type'] = 'archive'
        metadata['format'] = 'pkb'
        
        # Analyze PKB structure
        with open(pkb_file, 'rb') as f:
            header = f.read(16)
            if len(header) >= 4:
                if header[:4] == b'PKB\x00':
                    metadata['valid'] = True
                    # Could extract file count, etc.
                else:
                    metadata['valid'] = False
        
        # Copy and save metadata
        output_file = self.get_output_path(pkb_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(pkb_file, 'rb') as src, open(output_file, 'wb') as dst:
            dst.write(src.read())
        
        metadata_file = output_file.with_suffix('.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return True
    
    def process_image_file(self, image_file):
        """Process image file"""
        metadata = self.create_metadata(image_file)
        metadata['type'] = 'image'
        metadata['format'] = image_file.suffix[1:]  # Remove dot
        
        # Copy and save metadata
        output_file = self.get_output_path(image_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(image_file, 'rb') as src, open(output_file, 'wb') as dst:
            dst.write(src.read())
        
        metadata_file = output_file.with_suffix('.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return True
    
    def copy_file(self, file_path):
        """Copy file without special processing"""
        output_file = self.get_output_path(file_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'rb') as src, open(output_file, 'wb') as dst:
            dst.write(src.read())
        
        return True
    
    def create_metadata(self, file_path):
        """Create basic metadata for file"""
        stat = file_path.stat()
        
        # Calculate file hash
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        return {
            'filename': file_path.name,
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'sha256': file_hash,
            'relative_path': str(file_path.relative_to(self.input_dir))
        }
    
    def get_output_path(self, input_path):
        """Get output path for input file"""
        relative_path = input_path.relative_to(self.input_dir)
        return self.output_dir / relative_path

def main():
    if len(sys.argv) != 3:
        print("Usage: process_game_assets.py <input_dir> <output_dir>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(input_dir):
        print(f"❌ Input directory not found: {input_dir}")
        sys.exit(1)
    
    processor = AssetProcessor(input_dir, output_dir)
    processor.process_all_assets()

if __name__ == '__main__':
    main()
```

---

## 🌟 Automation Mastery Achieved

You now have a complete automation toolkit for Matrix Online development:

- ✅ **Build Automation** - Multi-platform builds and dependency management
- ✅ **Testing Automation** - Comprehensive test suites and validation
- ✅ **Deployment Scripts** - Reliable server deployment and rollback
- ✅ **Maintenance Utilities** - Database and log management
- ✅ **Content Processing** - Asset pipeline and metadata generation
- ✅ **Development Workflows** - Version control and collaboration

**The Matrix runs on automation. You've learned to automate the Matrix.**

---

[← Back to Development Tools](development-tools.md) | [Tool Development Guide →](tool-development-guide.md) | [AI-Assisted Development →](ai-assisted-development-mxo.md)

📚 [View Sources](sources/index.md)