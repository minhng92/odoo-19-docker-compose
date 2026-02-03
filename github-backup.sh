#!/bin/bash
# GitHub Backup Script for Odoo 19 Docker Setup

set -e

echo "=============================================="
echo "ODOO 19 GITHUB BACKUP"
echo "=============================================="
echo ""

# Configuration
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
GITHUB_BACKUP_DIR="/home/sgc/odoo-github-backup"
COMMIT_MESSAGE="Backup Odoo 19 - $BACKUP_DATE"

# Tạo thư mục backup GitHub
echo "📁 Tạo thư mục GitHub backup..."
mkdir -p "$GITHUB_BACKUP_DIR"
cd "$GITHUB_BACKUP_DIR"

# Khởi tạo git nếu chưa có
if [ ! -d ".git" ]; then
    echo "🔧 Khởi tạo Git repository..."
    git init
    echo "✅ Git repository đã khởi tạo"
else
    echo "✅ Git repository đã tồn tại"
fi

echo ""
echo "📦 Thu thập dữ liệu cần backup..."

# 1. Copy configurations
echo "⚙️  Copy configurations..."
cp /home/sgc/odoo-19-docker-compose/docker-compose.yml ./
cp /home/sgc/odoo-19-docker-compose/entrypoint.sh ./
cp /home/sgc/odoo-19-docker-compose/run.sh ./

mkdir -p etc
cp /home/sgc/odoo-19-docker-compose/etc/odoo.conf ./etc/
cp /home/sgc/odoo-19-docker-compose/etc/requirements.txt ./etc/
cp /home/sgc/odoo-19-docker-compose/etc/logrotate ./etc/

echo "   ✓ Docker configs"
echo "   ✓ Odoo configs"

# 2. Copy custom addons
echo "📦 Copy custom addons..."
if [ -d "/home/sgc/odoo-19-docker-compose/addons" ]; then
    cp -r /home/sgc/odoo-19-docker-compose/addons ./
    echo "   ✓ Custom addons"
else
    mkdir -p addons
    echo "# Custom Addons Directory" > addons/README.md
    echo "   ⚠️  Không có custom addons"
fi

# 3. Copy scripts
echo "📜 Copy scripts..."
if [ -d "/home/sgc/odoo-19-docker-compose/scripts" ]; then
    cp -r /home/sgc/odoo-19-docker-compose/scripts ./
    echo "   ✓ Scripts copied"
else
    mkdir -p scripts
    echo "# Scripts Directory" > scripts/README.md
fi

# 4. Copy documentation
echo "📋 Copy documentation..."
cp /home/sgc/odoo-19-docker-compose/README.md ./README.md 2>/dev/null || echo "# Odoo 19 Docker Compose" > README.md
cp /home/sgc/odoo-19-docker-compose/LICENSE ./LICENSE 2>/dev/null || true
cp /home/sgc/odoo-19-docker-compose/BACKUP_GUIDE.md ./BACKUP_GUIDE.md 2>/dev/null || true

# Copy backup scripts
cp /home/sgc/odoo-19-docker-compose/backup-full.sh ./
cp /home/sgc/odoo-19-docker-compose/scripts/backup_odoo.sh ./scripts/ 2>/dev/null || true

echo "   ✓ Documentation và backup scripts"

# 5. Tạo backup info và recovery guide
echo "📝 Tạo backup info..."
cat > BACKUP_INFO.md << EOF
# ODOO 19 BACKUP INFORMATION

## Backup Details
- **Date**: $(date)
- **Server**: $(hostname)
- **User**: $(whoami)
- **Odoo Version**: 19.0 Enterprise
- **PostgreSQL**: 18 with pgvector

## Repository Contents
- \`docker-compose.yml\` - Docker services configuration
- \`entrypoint.sh\` - Custom Odoo entrypoint
- \`etc/\` - Odoo configuration files
- \`addons/\` - Custom addons directory
- \`scripts/\` - Automation scripts
- \`backup-full.sh\` - Full backup script

## Quick Setup Commands
\`\`\`bash
# Clone repository
git clone <your-repo-url> odoo-19-docker-compose
cd odoo-19-docker-compose

# Install Enterprise (if needed)
# Download from Odoo.com và chạy:
# ./install-enterprise.sh

# Start services
docker compose up -d

# Access
# URL: http://localhost:10019
# Admin: admin / admin
\`\`\`

## Database Restore
> **Note**: Repository này chỉ chứa configs và scripts.
> Database và filestore cần restore từ backup riêng.

\`\`\`bash
# Restore từ backup
cd /home/sgc/odoo-backups
./odoo19_latest_restore.sh
\`\`\`

## Enterprise Setup
1. Download Enterprise từ Odoo.com
2. Giải nén vào thư mục \`enterprise/\`
3. Restart containers: \`docker compose restart\`

## System Requirements
- Docker & Docker Compose
- PostgreSQL 18 with pgvector extension
- 4GB+ RAM recommended
- Port 10019, 20019 available
EOF

# 6. Tạo .gitignore
echo "🚫 Tạo .gitignore..."
cat > .gitignore << EOF
# Odoo 19 Docker Compose - Git Ignore

# Database & Data
postgresql/
etc/filestore/
etc/sessions/
etc/addons/

# Enterprise modules (tải từ Odoo.com)
enterprise/

# Backups
backups/
*.sql
*.sql.gz
*.tar.gz

# Logs
*.log
logs/

# Temporary files
.DS_Store
Thumbs.db
*.tmp
*.temp

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Odoo specific
odoo.conf.backup
docker-compose.yml.backup
EOF

# 7. Tạo quick start script
echo "🚀 Tạo quick start script..."
cat > quick-start.sh << 'EOF'
#!/bin/bash
# Quick Start Script for Odoo 19

echo "🚀 ODOO 19 QUICK START"
echo "====================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker chưa được cài đặt!"
    echo "   Vui lòng cài Docker và Docker Compose trước."
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose chưa khả dụng!"
    exit 1
fi

echo "✅ Docker và Docker Compose đã sẵn sàng"

# Create necessary directories
echo "📁 Tạo thư mục cần thiết..."
mkdir -p postgresql etc/filestore
chmod 755 postgresql etc/filestore
chmod +x entrypoint.sh

echo "🐳 Khởi động containers..."
docker compose up -d

echo ""
echo "⏳ Đợi Odoo khởi động (30 giây)..."
sleep 30

echo ""
echo "=============================================="
echo "✅ ODOO 19 ĐÃ KHỞI ĐỘNG!"
echo "=============================================="
echo ""
echo "🌐 URL: http://localhost:10019"
echo "👤 Admin: admin / admin"
echo "📊 Chat: http://localhost:20019"
echo ""
echo "📝 Lưu ý:"
echo "   - Lần đầu khởi động có thể mất 2-3 phút"
echo "   - Enterprise cần cài thêm từ Odoo.com"
echo "   - Database cần restore từ backup nếu có"
echo ""
echo "🔍 Kiểm tra logs:"
echo "   docker compose logs -f odoo19"
echo ""
EOF

chmod +x quick-start.sh

# 8. Git operations
echo ""
echo "🔄 Git operations..."

# Add all files
git add .

# Check if there are changes
if git diff --cached --quiet; then
    echo "   ℹ️  Không có thay đổi để commit"
else
    echo "   📝 Commit changes..."
    git commit -m "$COMMIT_MESSAGE"
    echo "   ✅ Changes committed"
fi

# Show status
echo ""
echo "📊 Git status:"
git status --porcelain
echo ""
echo "📋 Recent commits:"
git log --oneline -5 2>/dev/null || echo "   (Chưa có commits)"

echo ""
echo "=============================================="
echo "✅ GITHUB BACKUP PREPARED!"
echo "=============================================="
echo ""
echo "📍 Location: $GITHUB_BACKUP_DIR"
echo ""
echo "🔗 SETUP GITHUB REMOTE (lần đầu):"
echo "   cd $GITHUB_BACKUP_DIR"
echo "   git remote add origin https://github.com/YOUR-USERNAME/odoo-19-backup.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "📤 PUSH TO GITHUB:"
echo "   cd $GITHUB_BACKUP_DIR"
echo "   git push"
echo ""
echo "📥 PULL FROM GITHUB (trên server khác):"
echo "   git clone https://github.com/YOUR-USERNAME/odoo-19-backup.git"
echo "   cd odoo-19-backup"
echo "   ./quick-start.sh"
echo ""
echo "📄 Files included:"
ls -la "$GITHUB_BACKUP_DIR"
echo ""
echo "💾 Ready to push to GitHub!"
echo ""