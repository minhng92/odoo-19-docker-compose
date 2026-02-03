# HƯỚNG DẪN GITHUB BACKUP CHO ODOO 19

## 🎯 TỔNG QUAN

GitHub backup cho phép:
- ✅ Backup configs, scripts và addons lên GitHub
- ✅ Clone về server mới khi cần
- ✅ Version control cho setup Odoo
- ✅ Chia sẻ với team hoặc server khác

## 📁 VỊ TRÍ

- **Source**: `/home/sgc/odoo-19-docker-compose/` (project chính)
- **GitHub backup**: `/home/sgc/odoo-github-backup/` (chuẩn bị push)

## 🚀 BƯỚC 1: TẠO GITHUB REPOSITORY

1. **Đăng nhập GitHub**: https://github.com
2. **Tạo repository mới**: Click "New repository"
3. **Đặt tên**: `odoo-19-backup` hoặc tên khác
4. **Settings**:
   - Public hoặc Private (tùy ý)
   - Không tick "Add README" (đã có sẵn)
   - Không add .gitignore (đã có sẵn)

## 🔗 BƯỚC 2: SETUP GIT REMOTE

```bash
# Di chuyển đến thư mục GitHub backup
cd /home/sgc/odoo-github-backup

# Thêm remote GitHub (thay YOUR-USERNAME và REPO-NAME)
git remote add origin https://github.com/YOUR-USERNAME/odoo-19-backup.git

# Đổi branch thành main
git branch -M main

# Push lần đầu
git push -u origin main
```

**Ví dụ**:
```bash
git remote add origin https://github.com/john/odoo-19-backup.git
git branch -M main  
git push -u origin main
```

## 📤 BƯỚC 3: PUSH BACKUP LÊN GITHUB

### Lần đầu (sau khi setup):
```bash
cd /home/sgc/odoo-github-backup
git push
```

### Các lần sau:
```bash
# Chạy script backup (sẽ tự commit)
cd /home/sgc/odoo-19-docker-compose
./github-backup.sh

# Push lên GitHub
cd /home/sgc/odoo-github-backup
git push
```

## 📥 BƯỚC 4: RESTORE TỪ GITHUB

### Trên server mới:
```bash
# Cách 1: Dùng script restore
./github-restore.sh https://github.com/YOUR-USERNAME/odoo-19-backup.git

# Cách 2: Clone thủ công
git clone https://github.com/YOUR-USERNAME/odoo-19-backup.git odoo-19-docker-compose
cd odoo-19-docker-compose
./quick-start.sh
```

## 🔄 WORKFLOW THƯỜNG NGÀY

### 1. Backup + Push:
```bash
cd /home/sgc/odoo-19-docker-compose
./github-backup.sh
cd /home/sgc/odoo-github-backup
git push
```

### 2. Pull updates từ GitHub:
```bash
cd /home/sgc/odoo-github-backup
git pull
# Copy files về project chính nếu cần
```

## 📋 NỘI DUNG ĐƯỢC BACKUP

### ✅ Bao gồm:
- `docker-compose.yml` - Cấu hình Docker
- `entrypoint.sh` - Custom entrypoint
- `etc/odoo.conf` - Cấu hình Odoo
- `etc/requirements.txt` - Python packages
- `addons/` - Custom addons
- `scripts/` - Automation scripts
- `backup-full.sh` - Backup script
- `quick-start.sh` - Quick setup
- `README.md`, `BACKUP_GUIDE.md` - Documentation

### ❌ Không bao gồm:
- `postgresql/` - Database data
- `etc/filestore/` - Uploaded files
- `enterprise/` - Enterprise modules (download từ Odoo.com)
- Backup files (*.sql.gz, *.tar.gz)
- Log files

## 🔒 BẢO MẬT

### Repository Public:
- ✅ Chia sẻ dễ dàng
- ❌ Configs có thể chứa thông tin nhạy cảm

### Repository Private:
- ✅ Bảo mật tốt hơn
- ❌ Cần invite collaborators

### Lưu ý:
- Password database trong `odoo.conf` sẽ được backup
- Xem xét sử dụng environment variables cho production

## 🛠️ CUSTOMIZATION

### Sửa script backup:
```bash
nano /home/sgc/odoo-19-docker-compose/github-backup.sh
```

### Thêm files cần backup:
Thêm vào script tại phần "Copy additional files"

### Thay đổi commit message:
Sửa biến `COMMIT_MESSAGE` trong script

## 🆘 TROUBLESHOOTING

### Lỗi authentication:
```bash
# Sử dụng GitHub token thay vì password
git remote set-url origin https://YOUR-TOKEN@github.com/USERNAME/REPO.git
```

### Lỗi permission denied:
```bash
# Kiểm tra SSH key hoặc dùng HTTPS
git remote -v
```

### Lỗi merge conflict:
```bash
cd /home/sgc/odoo-github-backup
git pull --rebase
git push
```

## 📊 KIỂM TRA STATUS

```bash
# Xem status Git
cd /home/sgc/odoo-github-backup
git status
git log --oneline -10

# Xem remote
git remote -v

# Xem files được track
git ls-files
```

## 💡 BEST PRACTICES

1. **Backup thường xuyên**: Sau mỗi thay đổi lớn
2. **Commit message rõ ràng**: Mô tả thay đổi
3. **Kiểm tra .gitignore**: Không commit files nhạy cảm
4. **Test restore**: Thường xuyên test restore trên máy khác
5. **Documentation**: Cập nhật README.md khi thay đổi

## 🔗 USEFUL COMMANDS

```bash
# Xem diff
git diff

# Undo changes
git checkout -- filename

# Xem history
git log --graph --oneline

# Xem remote branches
git branch -r

# Push specific branch
git push origin branch-name
```

## 📞 SUPPORT

- **GitHub backup location**: `/home/sgc/odoo-github-backup/`
- **Backup script**: `/home/sgc/odoo-19-docker-compose/github-backup.sh`
- **Restore script**: `/home/sgc/odoo-19-docker-compose/github-restore.sh`
- **Quick start**: `./quick-start.sh`