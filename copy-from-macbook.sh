#!/bin/bash
# Script copy file Odoo Enterprise từ Macbook về server

echo "=============================================="
echo "COPY ODOO ENTERPRISE TỪ MACBOOK VỀ SERVER"
echo "=============================================="
echo ""

echo "📋 THÔNG TIN FILE:"
echo "   Tên file: odoo_19.0+e.20251109.tar.gz"
echo "   Kích thước: 384.4 MB"
echo "   Vị trí hiện tại: Downloads/ trên Macbook"
echo ""

echo "🎯 ĐÍCH ĐẾN:"
echo "   Server: /home/sgc/odoo-19-docker-compose/"
echo ""

# IP Tailscale của server
SERVER_IP="100.122.93.102"

echo "🔍 IP Server (Tailscale): $SERVER_IP"
echo ""

echo "📝 LỆNH COPY CHO MACBOOK:"
echo ""
echo "Mở Terminal trên Macbook và chạy lệnh sau:"
echo ""
echo "┌─────────────────────────────────────────────────────────────────────────────────┐"
echo "│ cd ~/Downloads                                                                  │"
echo "│ scp odoo_19.0+e.20251109.tar.gz sgc@${SERVER_IP}:/home/sgc/odoo-19-docker-compose/ │"
echo "└─────────────────────────────────────────────────────────────────────────────────┘"
echo ""

echo "🔒 Nếu yêu cầu password, nhập password của user 'sgc'"
echo ""

echo "📱 HOẶC DÙNG RSYNC (Nhanh hơn, hiển thị progress):"
echo ""
echo "┌─────────────────────────────────────────────────────────────────────────────────┐"
echo "│ cd ~/Downloads                                                                  │"
echo "│ rsync -avz --progress odoo_19.0+e.20251109.tar.gz sgc@${SERVER_IP}:/home/sgc/odoo-19-docker-compose/ │"
echo "└─────────────────────────────────────────────────────────────────────────────────┘"
echo ""

echo "🔄 KIỂM TRA SAU KHI COPY:"
echo ""
echo "Trên server này, chạy lệnh kiểm tra:"
echo "ls -lh /home/sgc/odoo-19-docker-compose/*.tar.gz"
echo ""

echo "⚡ SAU KHI COPY XONG:"
echo ""
echo "1. File sẽ xuất hiện tại: /home/sgc/odoo-19-docker-compose/odoo_19.0+e.20251109.tar.gz"
echo "2. Chạy script cài đặt tự động: ./install-enterprise.sh"
echo "3. Hoặc giải nén thủ công và cấu hình"
echo ""

echo "🆘 NẾU GẶP LỖI:"
echo ""
echo "1. 'Permission denied': Kiểm tra SSH service đang chạy"
echo "2. 'Connection refused': Kiểm tra firewall/network"
echo "3. 'No space left': Kiểm tra dung lượng disk"
echo ""

# Kiểm tra SSH service
echo "🔧 KIỂM TRA SSH SERVICE:"
if systemctl is-active --quiet ssh; then
    echo "   ✅ SSH service đang chạy"
else
    echo "   ❌ SSH service không chạy - Khởi động..."
    sudo systemctl start ssh
fi

echo ""
echo "🔑 SSH Port: $(ss -tlnp | grep ':22 ' | head -1 | awk '{print $4}' | cut -d':' -f2 || echo '22')"
echo ""

echo "=================================="
echo "SẴN SÀNG NHẬN FILE!"
echo "=================================="
echo ""
echo "Hãy mở Terminal trên Macbook và chạy lệnh copy ở trên."
echo "File sẽ được copy vào thư mục hiện tại."