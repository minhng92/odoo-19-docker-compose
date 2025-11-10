#!/bin/bash
#
# 🚀 HƯỚNG DẪN HOÀN CHỈNH - TẠO 10 CÔNG TY MÔI TRƯỜNG
#

clear
echo "================================================================================"
echo "🌿 HƯỚNG DẪN TẠO 10 CÔNG TY MÔI TRƯỜNG VÀ USERS - ODOO 19"
echo "================================================================================"
echo ""
echo "📍 Database đang dùng: odoo19"
echo "📍 URL Odoo: http://localhost:10019"
echo "📍 Master Password: minhng.info"
echo ""
echo "================================================================================"
echo "📋 CÁC BƯỚC THỰC HIỆN"
echo "================================================================================"
echo ""

echo "BƯỚC 1️⃣: TẠO DATABASE ODOO"
echo "----------------------------"
echo "Mở trình duyệt: http://localhost:10019"
echo ""
echo "⚠️  Database 'odoo19' đã tồn tại!"
echo "Nếu muốn tạo mới, xóa database cũ trong Odoo hoặc đổi tên khác"
echo ""
echo "Thông tin đăng nhập hiện tại:"
echo "  • Database Name: odoo19"
echo "  • Username: admin"
echo "  • Password: admin"
echo "  • Phone: +84 28 1234 5678"
echo "  • Language: Vietnamese (Tiếng Việt) / vi_VN"
echo "  • Country: Vietnam"
echo "  • Master Password: minhng.info"
echo "  • Demo data: ☑ Load demonstration data (recommended)"
echo ""
echo "Nhấn [Create Database] và đợi 2-3 phút..."
echo ""
read -p "⏸️  Đã tạo xong database? (y/n): " db_created

if [ "$db_created" != "y" ]; then
    echo ""
    echo "⚠️  Hãy tạo database trước, sau đó chạy lại script này!"
    exit 0
fi

echo ""
echo "BƯỚC 2️⃣: TẠO 10 CÔNG TY MÔI TRƯỜNG"
echo "----------------------------"
echo "Script sẽ tạo 10 công ty với thông tin đầy đủ:"
echo ""
echo "  1. 🌱 Quan Trắc Môi Trường Xanh (TP.HCM)"
echo "  2. 👷 Môi Trường và An Toàn Lao Động Miền Nam (Tiền Giang)"
echo "  3. 💧 Xử Lý Nước Thải Công Nghiệp Đồng Nai (Đồng Nai)"
echo "  4. 🌍 Tư Vấn Môi Trường và Năng Lượng Bền Vững (Bình Dương)"
echo "  5. 🌫️  Kiểm Kê Khí Nhà Kính và Tín Chỉ Carbon (Cần Thơ)"
echo "  6. 🔬 Phân Tích Môi Trường Miền Tây (Sóc Trăng)"
echo "  7. 🏭 Quan Trắc Môi Trường Lao Động An Toàn (Vũng Tàu)"
echo "  8. 🚰 Giải Pháp Xử Lý Nước Thải Đô Thị (Bình Dương)"
echo "  9. 📋 Tư Vấn và Đánh Giá Tác Động Môi Trường (Vĩnh Long)"
echo "  10. 🔧 Nghiên Cứu và Ứng Dụng Công Nghệ Môi Trường (An Giang)"
echo ""
read -p "🚀 Bắt đầu tạo 10 công ty? (y/n): " create_companies

if [ "$create_companies" = "y" ]; then
    echo ""
    echo "⏳ Đang tạo công ty..."
    python3 /home/sgc/odoo-19-docker-compose/scripts/quick_create_env_companies.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Tạo công ty thành công!"
    else
        echo ""
        echo "❌ Có lỗi xảy ra khi tạo công ty!"
        exit 1
    fi
fi

echo ""
echo "BƯỚC 3️⃣: TẠO USERS CHO TỪNG CÔNG TY"
echo "----------------------------"
echo "Script sẽ tạo 10 users, mỗi user cho 1 công ty:"
echo ""
echo "  • quantrac.xanh (password: xanh2025)"
echo "  • mtld.miennam (password: laodong2025)"
echo "  • nuocthai.dongnai (password: nuoc2025)"
echo "  • tuvan.benvung (password: benvung2025)"
echo "  • khi.carbon (password: carbon2025)"
echo "  • phantich.mientay (password: lab2025)"
echo "  • quantrac.vungtau (password: ohs2025)"
echo "  • giaiphap.nuoc (password: urban2025)"
echo "  • danhgia.eia (password: eia2025)"
echo "  • nghiencuu.mt (password: tech2025)"
echo ""
read -p "👥 Bắt đầu tạo users? (y/n): " create_users

if [ "$create_users" = "y" ]; then
    echo ""
    echo "⏳ Đang tạo users..."
    python3 /home/sgc/odoo-19-docker-compose/scripts/create_company_users.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Tạo users thành công!"
    else
        echo ""
        echo "⚠️  Một số users có thể đã tồn tại hoặc có lỗi!"
    fi
fi

echo ""
echo "================================================================================"
echo "✅ HOÀN TẤT THIẾT LẬP!"
echo "================================================================================"
echo ""
echo "🌐 THÔNG TIN TRUY CẬP:"
echo "----------------------------"
echo "URL: http://localhost:10019"
echo "Database: odoo19"
echo ""
echo "👤 Admin chính:"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "🏢 Users công ty (10 tài khoản):"
echo "   Xem chi tiết: cat /home/sgc/odoo-19-docker-compose/COMPANY_LOGIN_INFO.md"
echo ""
echo "================================================================================"
echo "📚 TÀI LIỆU THAM KHẢO:"
echo "================================================================================"
echo ""
echo "📄 Thông tin đăng nhập 10 công ty:"
echo "   cat /home/sgc/odoo-19-docker-compose/COMPANY_LOGIN_INFO.md"
echo ""
echo "📄 Chi tiết 10 công ty môi trường:"
echo "   cat /home/sgc/odoo-19-docker-compose/ENVIRONMENTAL_COMPANIES.md"
echo ""
echo "📄 Hướng dẫn backup và quản lý:"
echo "   cat /home/sgc/odoo-19-docker-compose/scripts/README.md"
echo ""
echo "================================================================================"
echo "🎯 BƯỚC TIẾP THEO:"
echo "================================================================================"
echo ""
echo "1. Đăng nhập Odoo với admin / admin"
echo "2. Chuyển đổi giữa các công ty bằng cách click vào tên công ty góc trên"
echo "3. Tùy chỉnh thông tin công ty tại Settings → Companies → Companies"
echo "4. Upload logo cho từng công ty"
echo "5. Thêm thông tin ngân hàng, chữ ký điện tử"
echo ""
echo "================================================================================"
echo "💾 BACKUP TỰ ĐỘNG:"
echo "================================================================================"
echo ""
echo "⏰ Đã cài đặt backup tự động lúc 4:00 sáng hàng ngày"
echo "📁 Backup location: /home/sgc/odoo-19-docker-compose/backups/"
echo "🗓️  Retention: 7 ngày"
echo ""
echo "Kiểm tra cron job:"
echo "   crontab -l"
echo ""
echo "Chạy backup thủ công:"
echo "   /home/sgc/odoo-19-docker-compose/scripts/backup_odoo.sh"
echo ""
echo "================================================================================"
echo "🎉 CHÚC BẠN SỬ DỤNG ODOO HIỆU QUẢ!"
echo "================================================================================"
echo ""
