#!/bin/bash
# Script hướng dẫn tải Odoo Enterprise bằng GitHub với authentication

echo "=============================================="
echo "TẢI ODOO 19 ENTERPRISE TỪ GITHUB"
echo "=============================================="
echo ""

echo "⚠️  LƯU Ý: Repository Odoo Enterprise là PRIVATE"
echo "Bạn cần có tài khoản GitHub được cấp quyền truy cập."
echo ""

# Kiểm tra xem đã có GitHub token chưa
if [ -z "$GITHUB_TOKEN" ]; then
    echo "📋 HƯỚNG DẪN LẤY GITHUB ACCESS TOKEN:"
    echo ""
    echo "1. Đăng nhập GitHub: https://github.com"
    echo "2. Vào Settings → Developer settings → Personal access tokens → Tokens (classic)"
    echo "3. Nhấn 'Generate new token (classic)'"
    echo "4. Đặt tên: 'Odoo Enterprise Access'"
    echo "5. Chọn scope: 'repo' (Full control of private repositories)"
    echo "6. Nhấn 'Generate token'"
    echo "7. Copy token (chỉ hiện 1 lần!)"
    echo ""
    
    read -p "Bạn đã có GitHub token? (y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        read -sp "Nhập GitHub Token: " GITHUB_TOKEN
        echo ""
        
        if [ -z "$GITHUB_TOKEN" ]; then
            echo "❌ Token không được để trống!"
            exit 1
        fi
    else
        echo ""
        echo "❌ Bạn cần có GitHub token để tiếp tục."
        echo "Vui lòng tạo token theo hướng dẫn trên và chạy lại script."
        exit 1
    fi
fi

# Kiểm tra tài khoản có quyền truy cập không
echo ""
echo "🔍 Kiểm tra quyền truy cập..."

REPO_CHECK=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/repos/odoo/enterprise | grep -o '"private": true' || echo "")

if [ -z "$REPO_CHECK" ]; then
    echo ""
    echo "❌ TÀI KHOẢN KHÔNG CÓ QUYỀN TRUY CẬP!"
    echo ""
    echo "📌 Repository Odoo Enterprise là PRIVATE và chỉ dành cho:"
    echo "   - Khách hàng Odoo Enterprise có subscription hợp lệ"
    echo "   - Partners chính thức của Odoo"
    echo "   - Nhân viên Odoo"
    echo ""
    echo "🔑 GIẢI PHÁP:"
    echo ""
    echo "1. SỬ DỤNG FILE ZIP TỪ ODOO.COM (Khuyến nghị):"
    echo "   - Đăng nhập: https://www.odoo.com/my/home"
    echo "   - Tải file odoo_19.0+e.*.zip"
    echo "   - Giải nén vào thư mục enterprise/"
    echo ""
    echo "2. YÊU CẦU QUYỀN TRUY CẬP:"
    echo "   - Liên hệ support@odoo.com"
    echo "   - Cung cấp subscription code của bạn"
    echo "   - Yêu cầu GitHub access"
    echo ""
    exit 1
fi

echo "✅ Tài khoản có quyền truy cập!"

# Clone repository
echo ""
echo "📥 Đang tải Odoo Enterprise modules..."
echo ""

# Xóa thư mục cũ nếu có
if [ -d "enterprise" ]; then
    echo "🗑️  Xóa thư mục enterprise/ cũ..."
    rm -rf enterprise
fi

# Clone với authentication
git clone https://${GITHUB_TOKEN}@github.com/odoo/enterprise.git --branch 19.0 --depth 1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Tải thành công!"
    
    # Xóa .git để giảm dung lượng
    echo ""
    echo "🧹 Dọn dẹp..."
    rm -rf enterprise/.git
    
    # Đếm số modules
    MODULE_COUNT=$(ls -d enterprise/*/ 2>/dev/null | wc -l)
    echo ""
    echo "📦 Đã tải $MODULE_COUNT Enterprise modules"
    echo ""
    echo "📋 Một số modules:"
    ls -d enterprise/*/ | head -15 | sed 's/enterprise\//   ✓ /'
    
    echo ""
    echo "=================================="
    echo "✅ HOÀN TẤT!"
    echo "=================================="
    echo ""
    echo "📌 BƯỚC TIẾP THEO:"
    echo ""
    echo "1. Chạy script cài đặt:"
    echo "   ./install-enterprise.sh"
    echo ""
    echo "2. Hoặc cập nhật thủ công:"
    echo "   - Sửa docker-compose.yml"
    echo "   - Sửa etc/odoo.conf"
    echo "   - docker-compose restart"
    echo ""
else
    echo ""
    echo "❌ Lỗi khi tải repository!"
    echo ""
    echo "Có thể do:"
    echo "1. Token không hợp lệ"
    echo "2. Tài khoản chưa được cấp quyền"
    echo "3. Lỗi mạng"
    echo ""
    echo "Vui lòng thử lại hoặc sử dụng phương án tải từ Odoo.com"
    exit 1
fi
