#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script kích hoạt các ứng dụng cơ bản trong Odoo 19
Giúp bật nhanh các app quan trọng cho doanh nghiệp
"""

import xmlrpc.client
import time

URL = "http://localhost:10019"
DB = "odoo19"
USERNAME = "admin"
PASSWORD = "admin"

def connect_odoo():
    """Kết nối tới Odoo"""
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USERNAME, PASSWORD, {})
    
    if not uid:
        raise Exception("Không thể xác thực!")
    
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    return uid, models

def install_app(uid, models, app_name, display_name):
    """Cài đặt ứng dụng"""
    print(f"\n🔍 Kiểm tra '{display_name}'...")
    
    # Tìm module
    module_ids = models.execute_kw(
        DB, uid, PASSWORD,
        'ir.module.module', 'search',
        [[['name', '=', app_name]]]
    )
    
    if not module_ids:
        print(f"  ❌ Không tìm thấy app '{app_name}'")
        return False
    
    # Kiểm tra trạng thái
    module_info = models.execute_kw(
        DB, uid, PASSWORD,
        'ir.module.module', 'read',
        [module_ids, ['name', 'state', 'shortdesc']]
    )
    
    state = module_info[0]['state']
    
    if state == 'installed':
        print(f"  ✅ {display_name} đã được cài đặt")
        return True
    elif state == 'to upgrade':
        print(f"  ⚠️  {display_name} đang chờ nâng cấp")
        return True
    elif state == 'to install':
        print(f"  ⏳ {display_name} đang trong hàng đợi cài đặt")
        return True
    
    print(f"  📦 Đang cài đặt {display_name}...")
    
    try:
        # Cài đặt module
        models.execute_kw(
            DB, uid, PASSWORD,
            'ir.module.module', 'button_immediate_install',
            [module_ids]
        )
        
        print(f"  ⏳ Đợi {display_name} hoàn tất...")
        time.sleep(2)
        
        print(f"  ✅ {display_name} đã được cài đặt!")
        return True
    except Exception as e:
        print(f"  ❌ Lỗi cài đặt {display_name}: {str(e)}")
        return False

def main():
    """Hàm main"""
    print("\n" + "="*80)
    print("🚀 KÍCH HOẠT CÁC ỨNG DỤNG CƠ BẢN CHO ODOO 19")
    print("="*80)
    print(f"🌐 URL: {URL}")
    print(f"🗄️  Database: {DB}")
    print("="*80)
    
    # Danh sách ứng dụng cần cài đặt
    apps_to_install = [
        # Core Business Apps
        ('sale_management', 'Sales (Bán hàng)'),
        ('crm', 'CRM (Quản lý khách hàng)'),
        ('purchase', 'Purchase (Mua hàng)'),
        ('stock', 'Inventory (Quản lý kho)'),
        ('mrp', 'Manufacturing (Sản xuất)'),
        
        # Project & Services
        ('project', 'Project (Quản lý dự án)'),
        ('hr_timesheet', 'Timesheets (Chấm công)'),
        ('helpdesk', 'Helpdesk (Hỗ trợ khách hàng)'),
        
        # Accounting & Finance
        ('account', 'Accounting (Kế toán)'),
        ('account_accountant', 'Accounting Full (Kế toán đầy đủ)'),
        ('l10n_vn', 'Vietnam - Accounting (Kế toán Việt Nam)'),
        
        # HR & Payroll
        ('hr', 'Employees (Nhân viên)'),
        ('hr_attendance', 'Attendances (Chấm công)'),
        ('hr_holidays', 'Time Off (Nghỉ phép)'),
        ('hr_expense', 'Expenses (Chi phí)'),
        ('hr_recruitment', 'Recruitment (Tuyển dụng)'),
        
        # Marketing & Communication
        ('mass_mailing', 'Email Marketing'),
        ('sms', 'SMS Marketing'),
        ('social_media', 'Social Marketing'),
        
        # Website & E-commerce
        ('website', 'Website Builder'),
        ('website_sale', 'eCommerce'),
        ('website_blog', 'Blog'),
        ('website_forum', 'Forum'),
        
        # Point of Sale
        ('point_of_sale', 'Point of Sale (Bán lẻ)'),
        
        # Additional Tools
        ('documents', 'Documents (Quản lý tài liệu)'),
        ('approvals', 'Approvals (Phê duyệt)'),
        ('calendar', 'Calendar (Lịch)'),
        ('contacts', 'Contacts (Danh bạ)'),
        ('note', 'Notes (Ghi chú)'),
        
        # Productivity
        ('mail', 'Discuss (Chat nội bộ)'),
        ('board', 'Dashboards'),
        ('web_studio', 'Studio (Tùy chỉnh)'),
        
        # Reporting
        ('account_reports', 'Accounting Reports'),
        ('sale_margin', 'Sales Margin'),
    ]
    
    try:
        # Kết nối
        print("\n🔌 Đang kết nối tới Odoo...")
        uid, models = connect_odoo()
        print(f"✅ Kết nối thành công! User ID: {uid}")
        
        installed_count = 0
        failed_count = 0
        
        print("\n" + "="*80)
        print("📦 BẮT ĐẦU CÀI ĐẶT CÁC ỨNG DỤNG")
        print("="*80)
        
        for app_name, display_name in apps_to_install:
            if install_app(uid, models, app_name, display_name):
                installed_count += 1
            else:
                failed_count += 1
            time.sleep(0.5)  # Tránh quá tải
        
        print("\n" + "="*80)
        print("📊 KẾT QUẢ CÀI ĐẶT")
        print("="*80)
        print(f"✅ Thành công: {installed_count}/{len(apps_to_install)}")
        if failed_count > 0:
            print(f"❌ Thất bại: {failed_count}/{len(apps_to_install)}")
        
        print("\n" + "="*80)
        print("✅ HOÀN TẤT KÍCH HOẠT ỨNG DỤNG!")
        print("="*80)
        print("\n📌 Truy cập Odoo để sử dụng:")
        print(f"   🌐 URL: {URL}")
        print(f"   👤 Username: {USERNAME}")
        print(f"   🔑 Password: {PASSWORD}")
        print("\n📂 Xem danh sách apps:")
        print("   Apps → Main Menu (góc trên trái)")
        print("\n⚠️  Lưu ý:")
        print("   - Một số app có thể yêu cầu cấu hình thêm")
        print("   - Reload lại trang web để thấy menu mới")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
