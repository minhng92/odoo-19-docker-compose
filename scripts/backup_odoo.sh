#!/bin/bash
#
# Odoo 19 Automatic Backup Script
# Runs at 4:00 AM Vietnam Time (ICT, UTC+7)
# Keeps only last 7 days of backups
#

set -e

# Configuration
BACKUP_DIR="/home/sgc/odoo-backups"
RETENTION_DAYS=7
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$BACKUP_DIR/backup.log"

# PostgreSQL connection details (from docker-compose.yml)
DB_CONTAINER="odoo-19-docker-compose-db-1"
POSTGRES_USER="odoo"
POSTGRES_PASSWORD="odoo19@2025"

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "🚀 Starting Odoo FULL SNAPSHOT backup..."
log "=========================================="

# Create snapshot directory
SNAPSHOT_NAME="odoo19_auto_${TIMESTAMP}"
SNAPSHOT_DIR="$BACKUP_DIR/$SNAPSHOT_NAME"
mkdir -p "$SNAPSHOT_DIR"

log "📁 Snapshot folder: $SNAPSHOT_NAME"

# 1. Backup all databases
log "📋 Backing up all databases..."
cd /home/sgc/odoo-19-docker-compose
docker compose exec -T db pg_dump -U odoo odoo19 > "$SNAPSHOT_DIR/odoo19_database.sql" 2>/dev/null
DB_SIZE=$(du -h "$SNAPSHOT_DIR/odoo19_database.sql" | cut -f1)
log "  ✅ Database backup: $DB_SIZE"

# 2. Backup Odoo filestore
log "� Backing up filestore..."
if [ -d "./etc/filestore" ]; then
    cp -r ./etc/filestore "$SNAPSHOT_DIR/" 2>/dev/null
    FILESTORE_SIZE=$(du -sh "$SNAPSHOT_DIR/filestore" | cut -f1)
    log "  ✅ Filestore backup: $FILESTORE_SIZE"
fi

# 3. Backup configurations
log "⚙️  Backing up configurations..."
cp docker-compose.yml "$SNAPSHOT_DIR/" 2>/dev/null
cp entrypoint.sh "$SNAPSHOT_DIR/" 2>/dev/null
mkdir -p "$SNAPSHOT_DIR/etc"
cp etc/odoo.conf "$SNAPSHOT_DIR/etc/" 2>/dev/null
cp etc/requirements.txt "$SNAPSHOT_DIR/etc/" 2>/dev/null
cp etc/logrotate "$SNAPSHOT_DIR/etc/" 2>/dev/null
log "  ✅ Configurations backed up"

# 4. Backup custom addons
log "📦 Backing up custom addons..."
if [ -d "addons" ]; then
    cp -r addons "$SNAPSHOT_DIR/" 2>/dev/null
    log "  ✅ Custom addons backed up"
fi

# 5. Compress snapshot
log "�️  Compressing snapshot..."
cd "$BACKUP_DIR"
tar -czf "${SNAPSHOT_NAME}.tar.gz" "$SNAPSHOT_NAME" 2>/dev/null
ARCHIVE_SIZE=$(du -h "${SNAPSHOT_NAME}.tar.gz" | cut -f1)
log "  ✅ Compressed: ${SNAPSHOT_NAME}.tar.gz ($ARCHIVE_SIZE)"

# Remove uncompressed snapshot
rm -rf "$SNAPSHOT_NAME"

# Update latest symlink
ln -sf "${SNAPSHOT_NAME}.tar.gz" "odoo19_latest_backup.tar.gz"
log "  🔗 Updated latest backup link"

# Clean up old backups (older than RETENTION_DAYS)
log "🧹 Cleaning up snapshots older than $RETENTION_DAYS days..."
DELETED_COUNT=0

find "$BACKUP_DIR" -name "odoo19_auto_*.tar.gz" -type f -mtime +$RETENTION_DAYS | while read OLD_BACKUP; do
    rm -f "$OLD_BACKUP"
    log "  🗑️  Deleted: $(basename $OLD_BACKUP)"
    DELETED_COUNT=$((DELETED_COUNT + 1))
done

find "$BACKUP_DIR" -name "odoo19_backup_*.tar.gz" -type f -mtime +$RETENTION_DAYS | while read OLD_MANUAL; do
    rm -f "$OLD_MANUAL"
    log "  🗑️  Deleted: $(basename $OLD_MANUAL)"
    DELETED_COUNT=$((DELETED_COUNT + 1))
done

if [ $DELETED_COUNT -eq 0 ]; then
    log "  ℹ️  No old backups to delete"
fi

# Summary
CURRENT_BACKUPS=$(find "$BACKUP_DIR" -name "*.tar.gz" -type f | wc -l)
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

log "=========================================="
log "✨ Backup completed successfully!"
log "📊 Current backups: $CURRENT_BACKUPS files"
log "💿 Total backup size: $TOTAL_SIZE"
log "📍 Backup location: $BACKUP_DIR"
log "=========================================="

# Keep only last 100 lines of log file to prevent it from growing too large
if [ -f "$LOG_FILE" ]; then
    tail -n 100 "$LOG_FILE" > "$LOG_FILE.tmp"
    mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

exit 0
