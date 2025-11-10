#!/bin/bash
# GitHub Restore Script - Pull and setup Odoo from GitHub backup

set -e

echo "=============================================="
echo "RESTORE ODOO 19 FROM GITHUB"
echo "=============================================="
echo ""

# Configuration
GITHUB_URL="${1:-}"
TARGET_DIR="${2:-/home/sgc/odoo-19-docker-compose}"

if [ -z "$GITHUB_URL" ]; then
    echo "📝 Usage:"
    echo "   $0 <github-url> [target-directory]"
    echo ""
    echo "📋 Example:"
    echo "   $0 https://github.com/username/odoo-19-backup.git"
    echo "   $0 https://github.com/username/odoo-19-backup.git /path/to/restore"
    echo ""
    exit 1
fi

echo "📥 GitHub URL: $GITHUB_URL"
echo "📍 Target: $TARGET_DIR"
echo ""

# Backup existing directory if it exists
if [ -d "$TARGET_DIR" ]; then
    BACKUP_NAME="${TARGET_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
    echo "💾 Backing up existing directory to: $BACKUP_NAME"
    mv "$TARGET_DIR" "$BACKUP_NAME"
fi

echo "📁 Creating target directory..."
mkdir -p "$(dirname "$TARGET_DIR")"

echo "📥 Cloning from GitHub..."
git clone "$GITHUB_URL" "$TARGET_DIR"

cd "$TARGET_DIR"
echo "✅ Repository cloned successfully"
echo ""

echo "🔧 Setting up environment..."

# Make scripts executable
find . -name "*.sh" -exec chmod +x {} \;
echo "   ✓ Scripts made executable"

# Create missing directories
mkdir -p postgresql etc/filestore backups
chmod 755 postgresql etc/filestore
echo "   ✓ Directories created"

# Install dependencies if needed
echo "🐳 Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found! Please install Docker first."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose not found! Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose ready"
echo ""

echo "=============================================="
echo "✅ GITHUB RESTORE COMPLETED!"
echo "=============================================="
echo ""
echo "📍 Odoo location: $TARGET_DIR"
echo ""
echo "🚀 NEXT STEPS:"
echo ""
echo "1. Start Odoo (basic setup):"
echo "   cd $TARGET_DIR"
echo "   ./quick-start.sh"
echo ""
echo "2. OR with Enterprise (if you have):"
echo "   cd $TARGET_DIR"
echo "   # Download Enterprise from Odoo.com first"
echo "   # Extract to enterprise/ folder"
echo "   docker compose up -d"
echo ""
echo "3. Restore database (if you have backup):"
echo "   # Copy backup files to /home/sgc/odoo-backups/"
echo "   cd /home/sgc/odoo-backups"
echo "   ./odoo19_latest_restore.sh"
echo ""
echo "4. Access Odoo:"
echo "   🌐 URL: http://localhost:10019"
echo "   👤 Login: admin / admin"
echo ""
echo "📋 Available scripts:"
echo "   ./quick-start.sh     - Quick start Odoo"
echo "   ./backup-full.sh     - Create full backup"
echo "   ./github-backup.sh   - Backup to GitHub"
echo ""
echo "📖 Documentation:"
echo "   cat README.md"
echo "   cat BACKUP_INFO.md"
echo "   cat BACKUP_GUIDE.md"
echo ""