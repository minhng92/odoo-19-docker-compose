#!/bin/bash
# Setup automatic backup cron job for Odoo 19

echo "=============================================="
echo "SETUP AUTOMATIC BACKUP SCHEDULE"
echo "=============================================="
echo ""

BACKUP_SCRIPT="/home/sgc/odoo-19-docker-compose/backup-full.sh"
CRON_FILE="/tmp/odoo_backup_cron"

echo "📋 Tạo cron job..."
cat > "$CRON_FILE" << EOF
# Odoo 19 Automatic Backup
# Backup hàng ngày lúc 2:00 AM
0 2 * * * $BACKUP_SCRIPT >> /home/sgc/odoo-backups/backup.log 2>&1

# Backup hàng tuần (Chủ nhật 3:00 AM)
0 3 * * 0 $BACKUP_SCRIPT >> /home/sgc/odoo-backups/backup.log 2>&1

# Dọn dẹp backups cũ hơn 30 ngày (mỗi ngày 4:00 AM)
0 4 * * * find /home/sgc/odoo-backups -name "odoo19_backup_*.tar.gz" -mtime +30 -delete >> /home/sgc/odoo-backups/cleanup.log 2>&1
EOF

echo ""
echo "📝 Nội dung cron job:"
cat "$CRON_FILE"
echo ""

echo "💾 Cài đặt cron job..."
crontab -l > /tmp/current_cron 2>/dev/null || true
cat /tmp/current_cron "$CRON_FILE" | sort -u | crontab -
rm "$CRON_FILE" /tmp/current_cron

echo ""
echo "=============================================="
echo "✅ SETUP HOÀN TẤT!"
echo "=============================================="
echo ""
echo "📅 LỊCH BACKUP TỰ ĐỘNG:"
echo "   • Hàng ngày: 2:00 AM"
echo "   • Hàng tuần: Chủ nhật 3:00 AM"
echo "   • Dọn dẹp: Xóa backup > 30 ngày"
echo ""
echo "📂 Backup location: /home/sgc/odoo-backups/"
echo "📜 Logs: /home/sgc/odoo-backups/backup.log"
echo ""
echo "🔍 Kiểm tra cron jobs:"
echo "   crontab -l | grep odoo"
echo ""
echo "🔄 Chạy backup thủ công:"
echo "   $BACKUP_SCRIPT"
echo ""
