# HƯỚNG DẪN BACKUP & RESTORE ODOO 19

## 📍 VỊ TRÍ BACKUP

**Folder chính**: `/home/sgc/odoo-backups/`

## ⏰ LỊCH BACKUP TỰ ĐỘNG

- **Thời gian**: 4:00 AM hàng ngày (GMT+7)
- **Loại**: Full snapshot (Database + Filestore + Configs)
- **Giữ lại**: 7 ngày gần nhất
- **Cron job**: Đã cấu hình tự động

### Kiểm tra cron job:
```bash
crontab -l | grep backup
```

## 📦 BACKUP THỦ CÔNG

### 1. Full Snapshot (Khuyến nghị):
```bash
cd /home/sgc/odoo-19-docker-compose
./backup-full.sh
```

### 2. Backup tự động (giống lịch 4AM):
```bash
bash /home/sgc/odoo-19-docker-compose/scripts/backup_odoo.sh
```

## 📋 CẤU TRÚC BACKUP

Mỗi backup snapshot bao gồm:
- ✅ **Database SQL**: odoo19_database.sql (64MB)
- ✅ **Filestore**: Tất cả attachments, documents (32MB)
- ✅ **Configurations**: docker-compose.yml, odoo.conf, requirements.txt
- ✅ **Custom Addons**: Các module tùy chỉnh
- ✅ **Scripts**: Tất cả automation scripts

Tất cả được nén thành file `.tar.gz` (~16MB)

## 📊 THỐNG KÊ BACKUP

```bash
# Xem tất cả backups
ls -lh /home/sgc/odoo-backups/

# Xem log backup
tail -50 /home/sgc/odoo-backups/backup.log

# Kiểm tra dung lượng
du -sh /home/sgc/odoo-backups/
```

## 🔄 RESTORE BACKUP

### Cách 1: Dùng Restore Script (Tự động)
```bash
cd /home/sgc/odoo-backups/
./odoo19_latest_restore.sh
```

### Cách 2: Restore thủ công

```bash
cd /home/sgc/odoo-backups/

# Giải nén backup
tar -xzf odoo19_auto_YYYYMMDD_HHMMSS.tar.gz
cd odoo19_auto_YYYYMMDD_HHMMSS/

# 1. Dừng containers
cd /home/sgc/odoo-19-docker-compose
docker compose down

# 2. Restore database
docker compose up -d db
sleep 5
docker compose exec -T db psql -U odoo -c "DROP DATABASE IF EXISTS odoo19;"
docker compose exec -T db psql -U odoo -c "CREATE DATABASE odoo19;"
cat /home/sgc/odoo-backups/odoo19_auto_*/odoo19_database.sql | docker compose exec -T db psql -U odoo odoo19

# 3. Restore filestore
cp -r /home/sgc/odoo-backups/odoo19_auto_*/filestore/* /home/sgc/odoo-19-docker-compose/etc/filestore/

# 4. Restore configs (nếu cần)
cp /home/sgc/odoo-backups/odoo19_auto_*/docker-compose.yml .
cp /home/sgc/odoo-backups/odoo19_auto_*/entrypoint.sh .

# 5. Khởi động lại
docker compose up -d
```

## 🗑️ DỌN DẸP BACKUP CŨ

### Tự động:
- Backups > 7 ngày sẽ tự động xóa lúc 4AM hàng ngày

### Thủ công:
```bash
# Xóa backup cũ hơn 7 ngày
find /home/sgc/odoo-backups -name "odoo19_auto_*.tar.gz" -mtime +7 -delete

# Xóa backup cụ thể
rm /home/sgc/odoo-backups/odoo19_auto_20251109_*.tar.gz
```

## 📤 COPY BACKUP SANG SERVER KHÁC

### Từ server hiện tại:
```bash
# Dùng SCP
scp /home/sgc/odoo-backups/odoo19_latest_backup.tar.gz user@remote-server:/backup/

# Dùng rsync
rsync -avz /home/sgc/odoo-backups/odoo19_latest_backup.tar.gz user@remote-server:/backup/
```

### Qua Tailscale:
```bash
scp /home/sgc/odoo-backups/odoo19_latest_backup.tar.gz user@100.122.93.XXX:/backup/
```

## 🔧 THAY ĐỔI CẤU HÌNH BACKUP

### Thay đổi thời gian backup:
```bash
# Mở crontab
crontab -e

# Sửa dòng (ví dụ đổi sang 2AM):
0 2 * * * /home/sgc/odoo-19-docker-compose/scripts/backup_odoo.sh >> /home/sgc/odoo-backups/backup.log 2>&1
```

### Thay đổi thời gian giữ backup:
```bash
# Sửa file
nano /home/sgc/odoo-19-docker-compose/scripts/backup_odoo.sh

# Tìm dòng:
RETENTION_DAYS=7

# Đổi sang số ngày mong muốn (ví dụ 14 ngày):
RETENTION_DAYS=14
```

## ⚠️ LƯU Ý QUAN TRỌNG

1. **Dung lượng**: Mỗi backup ~16MB, 7 ngày = ~112MB
2. **Quyền truy cập**: Backup cần quyền read database và filestore
3. **Enterprise modules**: Không backup trong snapshot (có thể tải lại)
4. **pgvector extension**: Cần cài lại nếu restore sang server mới
5. **Passwords**: Database password: `odoo19@2025`

## 🆘 TROUBLESHOOTING

### Backup fails:
```bash
# Kiểm tra log
tail -100 /home/sgc/odoo-backups/backup.log

# Kiểm tra containers
docker compose ps

# Test thủ công
bash /home/sgc/odoo-19-docker-compose/scripts/backup_odoo.sh
```

### Restore fails:
```bash
# Kiểm tra PostgreSQL
docker compose exec db psql -U odoo -l

# Kiểm tra permissions
ls -la /home/sgc/odoo-19-docker-compose/etc/filestore/
```

## 📞 SUPPORT

- Log file: `/home/sgc/odoo-backups/backup.log`
- Backup script: `/home/sgc/odoo-19-docker-compose/scripts/backup_odoo.sh`
- Manual backup: `/home/sgc/odoo-19-docker-compose/backup-full.sh`
