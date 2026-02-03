#!/bin/bash
# Full Backup Script for Odoo 19 Docker Setup

set -e

echo "=============================================="
echo "ODOO 19 FULL BACKUP SNAPSHOT"
echo "=============================================="
echo ""

# Thông tin
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/sgc/odoo-backups"
BACKUP_NAME="odoo19_backup_${BACKUP_DATE}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Tạo thư mục backup
echo "📁 Tạo thư mục backup..."
mkdir -p "$BACKUP_PATH"
echo "   ✓ Thư mục: $BACKUP_PATH"
echo ""

# 1. Backup PostgreSQL Database
echo "🗄️  BƯỚC 1: Backup PostgreSQL Database..."
echo "   Database: odoo19"
docker compose exec -T db pg_dump -U odoo odoo19 > "${BACKUP_PATH}/odoo19_database.sql"
DB_SIZE=$(du -h "${BACKUP_PATH}/odoo19_database.sql" | cut -f1)
echo "   ✓ Database đã backup: ${DB_SIZE}"
echo ""

# 2. Backup Odoo filestore (attachments)
echo "📎 BƯỚC 2: Backup Odoo Filestore..."
if [ -d "/home/sgc/odoo-19-docker-compose/etc/filestore/odoo19" ]; then
    cp -r /home/sgc/odoo-19-docker-compose/etc/filestore "${BACKUP_PATH}/"
    FILESTORE_SIZE=$(du -sh "${BACKUP_PATH}/filestore" | cut -f1)
    echo "   ✓ Filestore đã backup: ${FILESTORE_SIZE}"
else
    echo "   ⚠️  Filestore không tồn tại hoặc chưa có dữ liệu"
fi
echo ""

# 3. Backup configurations
echo "⚙️  BƯỚC 3: Backup Configurations..."
cp docker-compose.yml "${BACKUP_PATH}/"
cp entrypoint.sh "${BACKUP_PATH}/"
mkdir -p "${BACKUP_PATH}/etc"
cp etc/odoo.conf "${BACKUP_PATH}/etc/" 2>/dev/null || true
cp etc/requirements.txt "${BACKUP_PATH}/etc/" 2>/dev/null || true
cp etc/logrotate "${BACKUP_PATH}/etc/" 2>/dev/null || true
echo "   ✓ docker-compose.yml"
echo "   ✓ entrypoint.sh"
echo "   ✓ etc/odoo.conf"
echo "   ✓ etc/requirements.txt"
echo "   ✓ etc/logrotate"
echo ""

# 4. Backup custom addons
echo "📦 BƯỚC 4: Backup Custom Addons..."
if [ -d "addons" ] && [ "$(ls -A addons)" ]; then
    cp -r addons "${BACKUP_PATH}/"
    ADDONS_SIZE=$(du -sh "${BACKUP_PATH}/addons" | cut -f1)
    echo "   ✓ Custom addons đã backup: ${ADDONS_SIZE}"
else
    echo "   ⚠️  Không có custom addons"
fi
echo ""

# 5. Backup Enterprise modules (không cần vì có thể tải lại)
echo "🏢 BƯỚC 5: Backup Enterprise info..."
if [ -d "enterprise" ]; then
    # Chỉ backup thông tin, không backup toàn bộ modules
    ls enterprise/ | head -20 > "${BACKUP_PATH}/enterprise_modules_list.txt"
    echo "   ✓ Đã lưu danh sách Enterprise modules"
    echo "   ℹ️  Enterprise modules có thể tải lại từ Odoo.com"
else
    echo "   ⚠️  Không có Enterprise modules"
fi
echo ""

# 6. Backup scripts
echo "📜 BƯỚC 6: Backup Scripts..."
if [ -d "scripts" ]; then
    cp -r scripts "${BACKUP_PATH}/"
    SCRIPTS_COUNT=$(ls scripts/*.py | wc -l)
    echo "   ✓ Đã backup ${SCRIPTS_COUNT} scripts"
else
    echo "   ⚠️  Không có scripts"
fi
echo ""

# 7. Tạo backup info file
echo "📋 BƯỚC 7: Tạo Backup Info..."
cat > "${BACKUP_PATH}/backup_info.txt" << EOF
ODOO 19 BACKUP INFORMATION
==========================

Backup Date: $(date)
Backup Name: ${BACKUP_NAME}
Server: $(hostname)
User: $(whoami)

BACKUP CONTENTS:
- Database: odoo19_database.sql
- Filestore: filestore/ (attachments, documents)
- Config: docker-compose.yml, entrypoint.sh, etc/
- Custom Addons: addons/
- Scripts: scripts/
- Enterprise: enterprise_modules_list.txt

DATABASE INFO:
- PostgreSQL Version: 18
- Database Name: odoo19
- Database User: odoo

ODOO INFO:
- Odoo Version: 19.0 Enterprise
- Port: 10019
- Chat Port: 20019

RESTORE INSTRUCTIONS:
=====================
1. Copy backup folder to target server
2. Run restore script: ./restore.sh
3. Or manual restore:
   - Import database: psql -U odoo odoo19 < odoo19_database.sql
   - Restore filestore to etc/filestore/
   - Restore configs
   - docker-compose up -d

NOTES:
- Enterprise modules cần tải lại từ Odoo.com nếu restore sang server mới
- Đảm bảo PostgreSQL 18 + pgvector extension
- Password database: odoo19@2025

EOF
echo "   ✓ Backup info đã tạo"
echo ""

# 8. Nén backup
echo "🗜️  BƯỚC 8: Nén backup..."
cd "$BACKUP_DIR"
tar -czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME"
ARCHIVE_SIZE=$(du -h "${BACKUP_NAME}.tar.gz" | cut -f1)
echo "   ✓ Đã nén: ${BACKUP_NAME}.tar.gz (${ARCHIVE_SIZE})"
echo ""

# Xóa thư mục tạm
rm -rf "$BACKUP_NAME"

# 9. Tạo restore script
echo "📝 BƯỚC 9: Tạo Restore Script..."
cat > "${BACKUP_DIR}/${BACKUP_NAME}_restore.sh" << 'EOF'
#!/bin/bash
# Restore script for Odoo 19

set -e

echo "=============================================="
echo "ODOO 19 RESTORE FROM BACKUP"
echo "=============================================="
echo ""

# Lấy tên backup từ tên script
SCRIPT_NAME=$(basename "$0")
BACKUP_NAME="${SCRIPT_NAME%_restore.sh}"
BACKUP_ARCHIVE="${BACKUP_NAME}.tar.gz"

if [ ! -f "$BACKUP_ARCHIVE" ]; then
    echo "❌ Không tìm thấy file backup: $BACKUP_ARCHIVE"
    exit 1
fi

echo "📦 Giải nén backup..."
tar -xzf "$BACKUP_ARCHIVE"
cd "$BACKUP_NAME"

echo ""
echo "🛑 Dừng containers..."
docker compose down

echo ""
echo "🗄️  Restore database..."
docker compose up -d db
sleep 5
docker compose exec -T db psql -U odoo -c "DROP DATABASE IF EXISTS odoo19;"
docker compose exec -T db psql -U odoo -c "CREATE DATABASE odoo19;"
cat odoo19_database.sql | docker compose exec -T db psql -U odoo odoo19
echo "   ✓ Database restored"

echo ""
echo "📎 Restore filestore..."
if [ -d "filestore" ]; then
    mkdir -p ../etc/filestore
    cp -r filestore/* ../etc/filestore/
    echo "   ✓ Filestore restored"
fi

echo ""
echo "⚙️  Restore configs..."
cp docker-compose.yml ../
cp entrypoint.sh ../
cp -r etc/* ../etc/
chmod +x ../entrypoint.sh
echo "   ✓ Configs restored"

echo ""
echo "📦 Restore addons..."
if [ -d "addons" ]; then
    cp -r addons ../
    echo "   ✓ Addons restored"
fi

echo ""
echo "📜 Restore scripts..."
if [ -d "scripts" ]; then
    cp -r scripts ../
    echo "   ✓ Scripts restored"
fi

echo ""
echo "🚀 Khởi động Odoo..."
cd ..
docker compose up -d

echo ""
echo "=============================================="
echo "✅ RESTORE HOÀN TẤT!"
echo "=============================================="
echo ""
echo "🌐 Truy cập: http://localhost:10019"
echo "👤 Login: admin / admin"
echo ""
echo "📝 Lưu ý: Nếu restore sang server mới, cần:"
echo "   - Cài Enterprise modules từ Odoo.com"
echo "   - Cài pgvector extension cho PostgreSQL"
echo ""
EOF

chmod +x "${BACKUP_DIR}/${BACKUP_NAME}_restore.sh"
echo "   ✓ Restore script: ${BACKUP_NAME}_restore.sh"
echo ""

# 10. Tạo link latest
echo "🔗 BƯỚC 10: Tạo link latest..."
cd "$BACKUP_DIR"
ln -sf "${BACKUP_NAME}.tar.gz" "odoo19_latest_backup.tar.gz"
ln -sf "${BACKUP_NAME}_restore.sh" "odoo19_latest_restore.sh"
echo "   ✓ odoo19_latest_backup.tar.gz -> ${BACKUP_NAME}.tar.gz"
echo ""

# Thống kê
echo "=============================================="
echo "✅ BACKUP HOÀN TẤT!"
echo "=============================================="
echo ""
echo "📊 THỐNG KÊ:"
echo "   Backup location: ${BACKUP_DIR}/"
echo "   Archive file: ${BACKUP_NAME}.tar.gz"
echo "   Archive size: ${ARCHIVE_SIZE}"
echo "   Restore script: ${BACKUP_NAME}_restore.sh"
echo ""
echo "📋 NỘI DUNG BACKUP:"
ls -lh "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
echo ""
echo "🔄 RESTORE:"
echo "   cd ${BACKUP_DIR}"
echo "   ./${BACKUP_NAME}_restore.sh"
echo ""
echo "🗂️  TẤT CẢ BACKUPS:"
ls -lh "${BACKUP_DIR}/" | grep "odoo19_backup"
echo ""
echo "💾 Lưu ý: Backup đã hoàn tất và có thể copy sang server khác!"
echo ""
