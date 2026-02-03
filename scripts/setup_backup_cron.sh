#!/bin/bash
#
# Setup cron job for Odoo automatic backup
# Runs at 4:00 AM Vietnam Time (ICT, UTC+7)
#

SCRIPT_PATH="/home/sgc/odoo-19-docker-compose/scripts/backup_odoo.sh"
CRON_TIME="0 4 * * *"  # 4:00 AM every day

echo "================================================"
echo "🕐 Setting up Odoo Automatic Backup Cron Job"
echo "================================================"
echo ""

# Check if script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: Backup script not found at $SCRIPT_PATH"
    exit 1
fi

# Check if script is executable
if [ ! -x "$SCRIPT_PATH" ]; then
    echo "⚠️  Making script executable..."
    chmod +x "$SCRIPT_PATH"
fi

# Check if cron job already exists
CRON_EXISTS=$(crontab -l 2>/dev/null | grep -F "$SCRIPT_PATH" | wc -l)

if [ "$CRON_EXISTS" -gt 0 ]; then
    echo "⚠️  Cron job already exists. Removing old entry..."
    crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH" | crontab -
fi

# Add new cron job
echo "📝 Adding cron job..."
(crontab -l 2>/dev/null; echo "$CRON_TIME $SCRIPT_PATH >> /home/sgc/odoo-19-docker-compose/backups/backup.log 2>&1") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron job added successfully!"
    echo ""
    echo "📋 Current crontab entries:"
    echo "----------------------------"
    crontab -l | grep "$SCRIPT_PATH"
    echo ""
    echo "⏰ Schedule: Every day at 4:00 AM (Vietnam Time)"
    echo "📁 Backup location: /home/sgc/odoo-19-docker-compose/backups/"
    echo "📝 Log file: /home/sgc/odoo-19-docker-compose/backups/backup.log"
    echo "🗓️  Retention: 7 days (older backups auto-deleted)"
    echo ""
    echo "================================================"
    echo "✨ Setup completed successfully!"
    echo "================================================"
else
    echo "❌ Failed to add cron job!"
    exit 1
fi
