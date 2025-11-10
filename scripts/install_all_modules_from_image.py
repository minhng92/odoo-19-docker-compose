#!/usr/bin/env python3
import xmlrpc.client
import time

url = "http://localhost:10019"
db = "odoo19"
username = "admin"
password = "admin"

print("=" * 70)
print("CÀI ĐẶT TẤT CẢ MODULES TRONG HÌNH")
print("=" * 70)
print()

# Kết nối
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("❌ Không thể đăng nhập!")
    exit(1)

print(f"✅ Đã đăng nhập: uid={uid}")
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Tất cả modules trong hình
modules_to_install = {
    # Hàng 1
    'board': 'My Dashboard',
    'voip': 'Chi tiết cuộc tiện thoại',
    'appointment': 'Cuộc hẹn',
    'project': 'Dự án',
    'knowledge': 'Kiến thức',
    'contacts': 'Liên hệ',
    
    # Hàng 2  
    'crm': 'CRM',
    'sale_management': 'Bán hàng',
    'account': 'Báo cáo',
    'documents': 'Tài liệu',
    'timesheet_grid': 'Bảng chấm công',
    'planning': 'Lập kế hoạch',
    
    # Hàng 3
    'helpdesk': 'Hỗ trợ',
    'website': 'Trang web',
    'web_studio': 'Học trực tuyến / Studio',
    'social': 'Tự động hóa marketing',
    'mass_mailing': 'Marketing qua Email',
    'sms': 'SMS Marketing',
    
    # Hàng 4
    'event': 'Sự kiện',
    'survey': 'Khảo sát',
    'purchase': 'Mua hàng',
    'stock': 'Tồn kho',
    'mrp': 'Bảo trì',
    'repair': 'Sửa chữa',
    
    # Hàng 5
    'hr': 'Nhân viên',
    'hr_attendance': 'Chấm công',
    'fleet': 'Đội xe',
    'approvals': 'Nghỉ phép',
    'hr_expense': 'Chi phí',
    'hr_recruitment': 'Tuyển dụng',
    
    # Hàng 6 (từ hình 2)
    'base_automation': 'Các hoạt động',
    'sign': 'Hợp đồng ký kết',
    'hr_payroll': 'Quản lý văn bản',
    'maintenance': 'Trạng tổng quan',
    'account_accountant': 'Kế toán',
    'dashboards': 'KPI',
    
    # Hàng 7
    'barcode': 'Mã vạch',
    'account_payment': 'Bảng lương',
    'hr_referral': 'Tuyển dụng',
    'quality_control': 'Phê duyệt',
    'l10n_vn': 'Ứng dụng',
    'web_enterprise': 'Cài đặt',
    
    # Hàng 8
    'sale_subscription': 'Thông báo',
    'zalo': 'Zalo Makerting',
    'calendar': 'Lịch',
    'note': 'Viết cần làm',
    
    # Thêm các modules khác
    'whatsapp': 'WhatsApp',
    'lunch': 'Thảo luận',
    'iot': 'IoT',
    'pos_restaurant': 'POS',
    'quality': 'Quality',
}

print()
print(f"📦 Cài đặt {len(modules_to_install)} modules...")
print()

installed_count = 0
already_installed = 0
failed_count = 0
not_found = []

for module_name, description in modules_to_install.items():
    try:
        # Tìm module
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[['name', '=', module_name]]])
        
        if not module_ids:
            print(f"   ⚠️  {module_name}: Không tìm thấy - {description}")
            not_found.append(module_name)
            continue
        
        # Lấy thông tin module
        module = models.execute_kw(db, uid, password,
            'ir.module.module', 'read',
            [module_ids], {'fields': ['name', 'state', 'summary']})[0]
        
        if module['state'] == 'installed':
            print(f"   ✓ {module_name}: Đã có - {description}")
            already_installed += 1
            continue
        
        # Cài đặt
        print(f"   ⏳ {module_name}: Đang cài - {description}...", end='', flush=True)
        
        try:
            models.execute_kw(db, uid, password,
                'ir.module.module', 'button_immediate_install', [module_ids])
            
            time.sleep(2)
            
            # Kiểm tra lại
            module = models.execute_kw(db, uid, password,
                'ir.module.module', 'read',
                [module_ids], {'fields': ['state']})[0]
            
            if module['state'] == 'installed':
                print(f" ✅")
                installed_count += 1
            else:
                print(f" ⚠️")
                
        except Exception as install_error:
            error_msg = str(install_error)
            if 'already' in error_msg.lower() or 'installed' in error_msg.lower():
                print(f" ✓")
                already_installed += 1
            else:
                print(f" ❌")
                failed_count += 1
            
    except Exception as e:
        print(f"   ❌ {module_name}: Lỗi - {description}")
        failed_count += 1

print()
print("=" * 70)
print("KẾT QUẢ:")
print("=" * 70)
print(f"✅ Cài mới: {installed_count} modules")
print(f"✓  Đã có: {already_installed} modules")
print(f"❌ Thất bại: {failed_count} modules")
print(f"⚠️  Không tìm thấy: {len(not_found)} modules")

if not_found:
    print()
    print("⚠️  Modules không tìm thấy (có thể không có trong Odoo 19):")
    for mod in not_found:
        print(f"   - {mod}")

print()
print("=" * 70)
print("🎉 HOÀN TẤT!")
print("=" * 70)
print(f"📊 Tổng: {installed_count + already_installed} modules sẵn sàng")
print()
print("🔄 Refresh trang Odoo để thấy tất cả modules!")
print()
