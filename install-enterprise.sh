#!/bin/bash
# Script tự động cài đặt Odoo 19 Enterprise

set -e

echo "=================================="
echo "ODOO 19 ENTERPRISE INSTALLATION"
echo "=================================="
echo ""

# Kiểm tra file ZIP hoặc TAR.GZ Enterprise
echo "🔍 Bước 1: Tìm file Enterprise..."
ENTERPRISE_ZIP=$(ls odoo_19.0*.zip 2>/dev/null || echo "")
ENTERPRISE_TAR=$(ls odoo_19.0*.tar.gz 2>/dev/null || echo "")

if [ -z "$ENTERPRISE_ZIP" ] && [ -z "$ENTERPRISE_TAR" ]; then
    echo "❌ Không tìm thấy file odoo_19.0*.zip hoặc odoo_19.0*.tar.gz"
    echo ""
    echo "📥 Vui lòng tải file Enterprise từ:"
    echo "   https://www.odoo.com/my/home"
    echo ""
    echo "Sau khi tải, đặt file vào thư mục này và chạy lại script."
    exit 1
fi

# Xác định file nào được dùng
if [ -n "$ENTERPRISE_ZIP" ]; then
    ENTERPRISE_FILE="$ENTERPRISE_ZIP"
    EXTRACT_TYPE="zip"
    echo "✅ Tìm thấy file ZIP: $ENTERPRISE_ZIP"
elif [ -n "$ENTERPRISE_TAR" ]; then
    ENTERPRISE_FILE="$ENTERPRISE_TAR"
    EXTRACT_TYPE="tar"
    echo "✅ Tìm thấy file TAR.GZ: $ENTERPRISE_TAR"
fi

# Tạo thư mục enterprise
echo ""
echo "📂 Bước 2: Tạo thư mục enterprise..."
mkdir -p enterprise
echo "✅ Đã tạo thư mục enterprise/"

# Giải nén
echo ""
echo "📦 Bước 3: Giải nén Enterprise modules..."

# Xóa thư mục enterprise cũ nếu có
if [ -d "enterprise" ]; then
    echo "🗑️  Xóa thư mục enterprise/ cũ..."
    rm -rf enterprise
fi

mkdir -p enterprise

if [ "$EXTRACT_TYPE" = "zip" ]; then
    echo "📦 Giải nén file ZIP..."
    unzip -q "$ENTERPRISE_FILE" -d temp_extract/
    # Di chuyển nội dung từ thư mục con lên enterprise/
    mv temp_extract/*/* enterprise/ 2>/dev/null || mv temp_extract/* enterprise/
    rm -rf temp_extract/
elif [ "$EXTRACT_TYPE" = "tar" ]; then
    echo "📦 Giải nén file TAR.GZ..."
    tar -xzf "$ENTERPRISE_FILE" -C .
    # Di chuyển nội dung từ thư mục giải nén vào enterprise/
    EXTRACTED_DIR=$(tar -tzf "$ENTERPRISE_FILE" | head -1 | cut -f1 -d"/")
    if [ -d "$EXTRACTED_DIR" ]; then
        mv "$EXTRACTED_DIR"/* enterprise/
        rm -rf "$EXTRACTED_DIR"
    fi
fi

echo "✅ Đã giải nén"

# Kiểm tra cấu trúc
echo ""
echo "🔍 Bước 4: Kiểm tra cấu trúc thư mục..."
ENTERPRISE_MODULES=$(ls -d enterprise/*/ 2>/dev/null | wc -l)

if [ "$ENTERPRISE_MODULES" -gt 0 ]; then
    echo "✅ Tìm thấy $ENTERPRISE_MODULES Enterprise modules"
    echo ""
    echo "📋 Một số modules Enterprise:"
    ls -d enterprise/*/ | head -10 | sed 's/enterprise\//   - /'
else
    echo "⚠️  Không tìm thấy modules trong enterprise/"
    echo "Có thể cần điều chỉnh cấu trúc thư mục..."
fi

# Backup docker-compose.yml
echo ""
echo "💾 Bước 5: Backup docker-compose.yml..."
if [ -f docker-compose.yml ]; then
    cp docker-compose.yml docker-compose.yml.backup
    echo "✅ Đã backup: docker-compose.yml.backup"
fi

# Cập nhật docker-compose.yml
echo ""
echo "⚙️  Bước 6: Cập nhật docker-compose.yml..."

if grep -q "/mnt/enterprise-addons" docker-compose.yml; then
    echo "✅ docker-compose.yml đã được cấu hình Enterprise"
else
    echo "📝 Thêm volume mount cho Enterprise..."
    
    # Thêm volume mount vào section volumes của odoo19
    sed -i '/volumes:/a\      - ./enterprise:/mnt/enterprise-addons' docker-compose.yml
    
    echo "✅ Đã cập nhật docker-compose.yml"
fi

# Backup odoo.conf
echo ""
echo "💾 Bước 7: Backup odoo.conf..."
if [ -f etc/odoo.conf ]; then
    cp etc/odoo.conf etc/odoo.conf.backup
    echo "✅ Đã backup: etc/odoo.conf.backup"
fi

# Cập nhật odoo.conf
echo ""
echo "⚙️  Bước 8: Cập nhật addons_path trong odoo.conf..."

if grep -q "/mnt/enterprise-addons" etc/odoo.conf; then
    echo "✅ odoo.conf đã được cấu hình Enterprise"
else
    # Cập nhật addons_path
    sed -i 's|addons_path = /mnt/extra-addons|addons_path = /mnt/extra-addons,/mnt/enterprise-addons,/usr/lib/python3/dist-packages/odoo/addons|' etc/odoo.conf
    
    echo "✅ Đã cập nhật odoo.conf"
fi

# Dừng và khởi động lại container
echo ""
echo "🔄 Bước 9: Khởi động lại Odoo container..."
echo ""

read -p "Bạn có muốn restart container ngay bây giờ? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "⏹️  Dừng container..."
    docker compose down
    
    echo ""
    echo "🚀 Khởi động lại..."
    docker compose up -d
    
    echo ""
    echo "📊 Xem logs (Ctrl+C để thoát)..."
    sleep 2
    docker compose logs -f odoo19 &
    LOGS_PID=$!
    
    sleep 10
    kill $LOGS_PID 2>/dev/null || true
fi

# Kết quả
echo ""
echo "=================================="
echo "✅ CÀI ĐẶT HOÀN TẤT!"
echo "=================================="
echo ""
echo "📋 CÁC BƯỚC TIẾP THEO:"
echo ""
echo "1. Đăng nhập Odoo:"
echo "   http://localhost:10019"
echo ""
echo "2. Vào Settings → Activate Enterprise Edition"
echo ""
echo "3. Nhập Subscription Code từ Odoo.com"
echo ""
echo "4. Kiểm tra Apps → Các Enterprise modules sẽ có sẵn"
echo ""
echo "📚 Xem thêm: HUONG_DAN_CAI_DAT_ENTERPRISE.md"
echo ""
echo "=================================="
