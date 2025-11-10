#!/bin/bash

# Script tự động kích hoạt Odoo 19 Enterprise License
# Tác giả: Auto Setup Script
# Ngày: November 9, 2025

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Main script
print_header "🔐 KÍCH HOẠT ODOO 19 ENTERPRISE LICENSE"

# Kiểm tra container đang chạy
print_info "Kiểm tra Odoo container..."
if ! docker compose ps | grep -q "odoo19.*Up"; then
    print_error "Odoo container chưa chạy!"
    print_info "Khởi động container..."
    docker compose up -d
    sleep 5
fi

print_success "Odoo container đang chạy"

# Hỏi Subscription Code
echo ""
print_warning "QUAN TRỌNG: Bạn cần có Subscription Code từ Odoo.com"
print_info "Code có dạng: ODOO-ENTERPRISE-XXXXXXXXX"
echo ""
echo -e "${YELLOW}Nếu chưa có code, hãy lấy từ:${NC}"
echo "1. Email xác nhận từ Odoo"
echo "2. https://www.odoo.com/my/home → Subscriptions"
echo "3. Partner/đại lý nơi bạn mua license"
echo "4. Email support@odoo.com để lấy lại"
echo ""

read -p "Nhập Subscription Code (hoặc nhấn Enter để mở hướng dẫn): " SUBSCRIPTION_CODE

# Nếu không nhập code, mở hướng dẫn
if [ -z "$SUBSCRIPTION_CODE" ]; then
    print_info "Mở hướng dẫn chi tiết..."
    
    if command -v xdg-open > /dev/null; then
        xdg-open "HUONG_DAN_KICH_HOAT_LICENSE.md" &
    elif command -v open > /dev/null; then
        open "HUONG_DAN_KICH_HOAT_LICENSE.md" &
    else
        print_warning "Vui lòng đọc file: HUONG_DAN_KICH_HOAT_LICENSE.md"
    fi
    
    echo ""
    print_header "🌐 CÁC BƯỚC KÍCH HOẠT THỦ CÔNG"
    echo "1. Truy cập: http://localhost:10019"
    echo "2. Login: admin / admin"
    echo "3. Vào Settings → Tìm 'Enterprise Subscription'"
    echo "4. Nhập Subscription Code và click Activate"
    echo ""
    print_success "Hoàn tất!"
    exit 0
fi

# Trim whitespace
SUBSCRIPTION_CODE=$(echo "$SUBSCRIPTION_CODE" | xargs)

# Validate code format
if [[ ! "$SUBSCRIPTION_CODE" =~ ^ODOO-ENTERPRISE-[A-Z0-9]+$ ]]; then
    print_warning "Code format không chuẩn (nên có dạng: ODOO-ENTERPRISE-XXXXXXXXX)"
    read -p "Bạn có chắc muốn tiếp tục? (y/N): " CONFIRM
    if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
        print_error "Đã hủy"
        exit 1
    fi
fi

# Lưu code vào file để backup
print_info "Lưu Subscription Code vào file..."
echo "$SUBSCRIPTION_CODE" > subscription_code.txt
chmod 600 subscription_code.txt
print_success "Đã lưu vào: subscription_code.txt"

# Kiểm tra internet connectivity
print_info "Kiểm tra kết nối internet..."
if docker compose exec -T odoo19 ping -c 3 services.odoo.com > /dev/null 2>&1; then
    print_success "Kết nối internet OK"
else
    print_error "Không thể kết nối tới services.odoo.com"
    print_warning "Kích hoạt license cần kết nối internet!"
    exit 1
fi

# Hướng dẫn kích hoạt thủ công qua giao diện
print_header "📝 HƯỚNG DẪN KÍCH HOẠT"

echo ""
echo -e "${GREEN}Subscription Code của bạn:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}$SUBSCRIPTION_CODE${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${GREEN}Các bước kích hoạt:${NC}"
echo ""
echo "1. 🌐 Truy cập Odoo:"
echo "   URL: http://localhost:10019"
echo "   Database: odoo19"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "2. ⚙️  Vào Settings:"
echo "   Click icon Settings (⚙️) ở menu trên"
echo ""
echo "3. 🔍 Tìm 'Enterprise Subscription':"
echo "   Scroll xuống tìm section 'Odoo Enterprise' hoặc 'Subscription'"
echo ""
echo "4. ✍️  Nhập Subscription Code:"
echo "   Paste code phía trên vào field 'Subscription Code'"
echo "   Code đã được copy vào clipboard (nếu có xclip)"
echo ""
echo "5. ✅ Click 'Activate' hoặc 'Register'"
echo ""
echo "6. 🎉 Kiểm tra kích hoạt thành công:"
echo "   - Thấy Expiration Date"
echo "   - Thấy Number of users"
echo "   - Status: Active"
echo ""

# Copy to clipboard nếu có xclip
if command -v xclip > /dev/null; then
    echo "$SUBSCRIPTION_CODE" | xclip -selection clipboard 2>/dev/null || true
    print_success "Subscription Code đã được copy vào clipboard!"
elif command -v pbcopy > /dev/null; then
    echo "$SUBSCRIPTION_CODE" | pbcopy 2>/dev/null || true
    print_success "Subscription Code đã được copy vào clipboard!"
fi

# Mở browser
print_info "Mở Odoo trong browser..."
sleep 2

if command -v xdg-open > /dev/null; then
    xdg-open "http://localhost:10019/web/database/manager" &
elif command -v open > /dev/null; then
    open "http://localhost:10019/web/database/manager" &
else
    print_warning "Không thể tự động mở browser. Vui lòng truy cập thủ công:"
    echo "http://localhost:10019"
fi

echo ""
print_header "⏳ CHỜ BẠN KÍCH HOẠT TRÊN GIAO DIỆN"

# Hỏi xem đã kích hoạt xong chưa
echo ""
read -p "Nhấn Enter sau khi bạn đã kích hoạt thành công trên giao diện..." 

# Restart container để apply changes
print_info "Restart Odoo container để áp dụng thay đổi..."
docker compose restart odoo19

print_success "Đã restart Odoo"

# Chờ Odoo khởi động lại
print_info "Chờ Odoo khởi động (15 giây)..."
sleep 15

# Kiểm tra logs
print_info "Kiểm tra logs..."
echo ""
docker compose logs --tail=20 odoo19 | grep -i "enterprise\|subscription\|license" || true

echo ""
print_header "✅ HOÀN TẤT"

echo ""
echo -e "${GREEN}Các bước kiểm tra:${NC}"
echo ""
echo "1. Truy cập: http://localhost:10019"
echo "2. Vào Settings → Kiểm tra 'Enterprise Subscription'"
echo "3. Nếu thấy:"
echo "   ✅ Expiration Date"
echo "   ✅ Number of users"
echo "   ✅ Status: Active"
echo "   → Đã kích hoạt thành công!"
echo ""
echo "4. Test Enterprise Apps:"
echo "   Apps → Search: Studio, Documents, Helpdesk, Sign, Planning"
echo "   Nếu không có watermark 'Trial' → OK!"
echo ""

print_success "Script hoàn tất!"
print_info "Nếu có vấn đề, xem: HUONG_DAN_KICH_HOAT_LICENSE.md"
echo ""

# Tạo summary file
cat > ACTIVATION_SUMMARY.txt << EOF
═══════════════════════════════════════════════════════════
📋 THÔNG TIN KÍCH HOẠT ODOO 19 ENTERPRISE
═══════════════════════════════════════════════════════════

Ngày kích hoạt: $(date '+%Y-%m-%d %H:%M:%S')

Subscription Code: $SUBSCRIPTION_CODE

URL Odoo: http://localhost:10019
Database: odoo19
Username: admin
Password: admin

═══════════════════════════════════════════════════════════
📊 KIỂM TRA KÍCH HOẠT
═══════════════════════════════════════════════════════════

1. Vào Settings → Tìm 'Enterprise Subscription'
2. Kiểm tra:
   ✅ Expiration Date: ________________
   ✅ Number of users: ________________
   ✅ Status: Active

3. Test Enterprise Apps:
   Apps → Search các app sau:
   □ Studio
   □ Documents
   □ Helpdesk
   □ Sign
   □ Planning
   □ Social Marketing
   □ Field Service
   □ Quality

═══════════════════════════════════════════════════════════
🔧 TROUBLESHOOTING
═══════════════════════════════════════════════════════════

Nếu có vấn đề:
1. Restart: docker compose restart odoo19
2. Xem logs: docker compose logs -f odoo19
3. Xem hướng dẫn: HUONG_DAN_KICH_HOAT_LICENSE.md
4. Liên hệ: support@odoo.com

═══════════════════════════════════════════════════════════
EOF

print_success "Đã tạo file tóm tắt: ACTIVATION_SUMMARY.txt"

echo ""
print_info "Subscription Code đã được lưu tại: subscription_code.txt"
print_warning "⚠️  Giữ file này an toàn! Không share với người khác!"

echo ""
