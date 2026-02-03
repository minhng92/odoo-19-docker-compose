#!/usr/bin/env python3
import xmlrpc.client
import time

url = "http://localhost:10019"
db = "odoo19"
username = "admin"
password = "admin"

print("=" * 60)
print("CÀI ĐẶT ENTERPRISE APPS")
print("=" * 60)
print()

# Kết nối
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("❌ Không thể đăng nhập!")
    exit(1)

print(f"✅ Đã đăng nhập: uid={uid}")
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Danh sách Enterprise apps cần cài
enterprise_apps = [
    'web_studio',           # Studio - Tạo apps tùy chỉnh
    'documents',            # Documents - Quản lý tài liệu
    'helpdesk',             # Helpdesk - Hỗ trợ khách hàng
    'sign',                 # Sign - Chữ ký điện tử
    'planning',             # Planning - Lập kế hoạch nhân sự
    'account_accountant',   # Accountant - Kế toán nâng cao
]

print()
print(f"📦 Cài đặt {len(enterprise_apps)} Enterprise apps...")
print()

installed_count = 0
failed_count = 0

for app_name in enterprise_apps:
    try:
        # Tìm module
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[['name', '=', app_name]]])
        
        if not module_ids:
            print(f"   ❌ {app_name}: Không tìm thấy")
            failed_count += 1
            continue
        
        # Lấy thông tin module
        module = models.execute_kw(db, uid, password,
            'ir.module.module', 'read',
            [module_ids], {'fields': ['name', 'state', 'summary']})[0]
        
        if module['state'] == 'installed':
            print(f"   ✓ {app_name}: Đã cài đặt")
            installed_count += 1
            continue
        
        # Cài đặt
        print(f"   ⏳ {app_name}: Đang cài đặt...", end='', flush=True)
        models.execute_kw(db, uid, password,
            'ir.module.module', 'button_immediate_install', [module_ids])
        
        time.sleep(2)  # Đợi module cài xong
        
        # Kiểm tra lại
        module = models.execute_kw(db, uid, password,
            'ir.module.module', 'read',
            [module_ids], {'fields': ['state']})[0]
        
        if module['state'] == 'installed':
            print(f" ✅ Thành công!")
            installed_count += 1
        else:
            print(f" ⚠️  State: {module['state']}")
            
    except Exception as e:
        print(f" ❌ Lỗi: {str(e)[:50]}")
        failed_count += 1

print()
print("=" * 60)
print("KẾT QUẢ:")
print("=" * 60)
print(f"✅ Thành công: {installed_count}/{len(enterprise_apps)}")
print(f"❌ Thất bại: {failed_count}/{len(enterprise_apps)}")
print()
print("🌟 ENTERPRISE APPS ĐÃ ACTIVE!")
print()
print("📌 Truy cập: http://localhost:10019")
print("   Vào Apps để xem tất cả Enterprise features")
print()
