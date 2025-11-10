# 🚀 Hướng dẫn Setup Odoo 19 Hoàn chỉnh

## ✅ Đã hoàn tất:

### 1. Odoo 19 đang chạy
- ✅ Odoo container: Đang hoạt động
- ✅ PostgreSQL 18: Đang hoạt động
- ✅ URL: http://localhost:10019

### 2. Backup tự động đã được cài đặt
- ⏰ Thời gian: 4:00 sáng mỗi ngày (giờ Việt Nam)
- 📁 Vị trí: `/home/sgc/odoo-19-docker-compose/backups/`
- 🗓️ Lưu trữ: 7 ngày (tự động xóa backup cũ)
- 💾 Backup: Database + Filestore

### 3. Scripts đã sẵn sàng
- ✅ `scripts/create_companies.py` - Tạo 10 công ty Việt Nam
- ✅ `scripts/backup_odoo.sh` - Backup database
- ✅ `scripts/complete_setup.sh` - Setup tự động

---

## 📋 HƯỚNG DẪN TẠO DATABASE VÀ 10 CÔNG TY

### Bước 1: Tạo Database trên Web

**Trình duyệt đã được mở tại: http://localhost:10019**

1. Bạn sẽ thấy trang "Create a database"
2. Điền thông tin như sau:

```
┌─────────────────────────────────────────┐
│ Master Password: minhng.info            │
│ Database Name:  odoo19_production       │
│ Email:          admin@odoo19.local      │
│ Password:       Admin@2025!             │
│ Phone:          (để trống hoặc điền)    │
│ Language:       Vietnamese / Tiếng Việt │
│ Country:        Vietnam                 │
│ Demo data:      ☑ (checked/tích)        │
└─────────────────────────────────────────┘
```

3. Nhấn **"Create database"**
4. Đợi **2-3 phút** để Odoo khởi tạo database

### Bước 2: Đăng nhập vào Odoo

Sau khi database được tạo, bạn sẽ tự động đăng nhập với:
- 📧 Email: `admin@odoo19.local`
- 🔑 Password: `Admin@2025!`

### Bước 3: Tạo 10 Công ty Việt Nam

Mở terminal và chạy:

```bash
cd /home/sgc/odoo-19-docker-compose
python3 scripts/create_companies.py
```

Nhập thông tin khi được hỏi:
- Database name: `odoo19_production`
- Admin email: `admin@odoo19.local`
- Admin password: `Admin@2025!`

Script sẽ tạo 10 công ty:
1. ✅ Công ty TNHH Công Nghệ FPT
2. ✅ Công ty Cổ phần Viettel
3. ✅ Công ty Cổ phần Vinamilk
4. ✅ Ngân hàng TMCP Vietcombank
5. ✅ Tập đoàn Hòa Phát
6. ✅ Công ty Cổ phần Thế Giới Di Động
7. ✅ Tập đoàn Masan
8. ✅ Công ty Cổ phần Dược phẩm Hậu Giang
9. ✅ Công ty Cổ phần Sacombank
10. ✅ Công ty TNHH VNG Corporation

---

## 🎯 Thông tin đăng nhập

### Truy cập Odoo:
```
🌐 URL:      http://localhost:10019
💾 Database: odoo19_production
📧 Email:    admin@odoo19.local
🔑 Password: Admin@2025!
🔐 Master:   minhng.info
```

### Xem các công ty đã tạo:
1. Đăng nhập vào Odoo
2. Menu trên cùng → **Settings** (Cài đặt)
3. Menu bên trái → **Companies** (Công ty)
4. Bạn sẽ thấy 10 công ty Việt Nam

---

## 💾 Quản lý Backup

### Kiểm tra backup tự động:
```bash
# Xem cron job
crontab -l

# Xem danh sách backup
ls -lh /home/sgc/odoo-19-docker-compose/backups/

# Xem log backup
cat /home/sgc/odoo-19-docker-compose/backups/backup.log
```

### Chạy backup thủ công:
```bash
/home/sgc/odoo-19-docker-compose/scripts/backup_odoo.sh
```

### Restore từ backup:
```bash
# Giải nén
gunzip /home/sgc/odoo-19-docker-compose/backups/odoo19_production_YYYYMMDD_HHMMSS.sql.gz

# Restore
docker exec -i odoo-19-docker-compose-db-1 psql -U odoo -c "CREATE DATABASE odoo19_restored;"
docker exec -i odoo-19-docker-compose-db-1 psql -U odoo -d odoo19_restored < /home/sgc/odoo-19-docker-compose/backups/odoo19_production_YYYYMMDD_HHMMSS.sql
```

---

## 🛠️ Các lệnh hữu ích

### Quản lý Odoo:
```bash
# Khởi động
docker compose up -d

# Dừng
docker compose down

# Restart
docker compose restart

# Xem logs
docker compose logs -f odoo19

# Xem trạng thái
docker compose ps
```

### Truy cập PostgreSQL:
```bash
# Vào PostgreSQL shell
docker exec -it odoo-19-docker-compose-db-1 psql -U odoo -d odoo19_production

# List databases
docker exec odoo-19-docker-compose-db-1 psql -U odoo -d postgres -c "\l"

# List tables trong database
docker exec odoo-19-docker-compose-db-1 psql -U odoo -d odoo19_production -c "\dt"
```

---

## 🎉 Hoàn tất!

Bây giờ bạn có:
- ✅ Odoo 19 đang chạy
- ✅ Database sẵn sàng tạo
- ✅ Script tạo 10 công ty tự động
- ✅ Backup tự động mỗi ngày lúc 4:00 sáng
- ✅ Chỉ lưu backup 7 ngày gần nhất

**Bước tiếp theo:** Mở http://localhost:10019 và tạo database!
