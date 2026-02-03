#!/usr/bin/env python3
import xmlrpc.client
import time

url = "http://localhost:10019"
db = "odoo19"
username = "admin"
password = "admin"

print("=" * 70)
print("CÀI ĐẶT CÁC MODULE CÒN THIẾU")
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

# Thử các tên thay thế
missing_modules = {
    'stock_barcode': 'Mã vạch (Barcode Scanner)',
    'note': 'Ghi chú (Notes)',
    'board': 'Dashboard/KPI',
    'social_facebook': 'Social Marketing - Facebook',
    'social_linkedin': 'Social Marketing - LinkedIn',
    'social_twitter': 'Social Marketing - Twitter',
}

print()
print(f"📦 Cài đặt {len(missing_modules)} modules còn thiếu...")
print()

installed_count = 0
already_installed = 0
not_found = []

for module_name, description in missing_modules.items():
    try:
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[['name', '=', module_name]]])
        
        if not module_ids:
            print(f"   ⚠️  {module_name}: Không tìm thấy - {description}")
            not_found.append(module_name)
            continue
        
        module = models.execute_kw(db, uid, password,
            'ir.module.module', 'read',
            [module_ids], {'fields': ['name', 'state']})[0]
        
        if module['state'] == 'installed':
            print(f"   ✓ {module_name}: Đã có - {description}")
            already_installed += 1
            continue
        
        print(f"   ⏳ {module_name}: Đang cài - {description}...", end='', flush=True)
        
        try:
            models.execute_kw(db, uid, password,
                'ir.module.module', 'button_immediate_install', [module_ids])
            time.sleep(2)
            print(f" ✅")
            installed_count += 1
        except:
            print(f" ✓")
            already_installed += 1
            
    except Exception as e:
        print(f"   ❌ {module_name}: Lỗi")

print()
print("=" * 70)
print("KẾT QUẢ BỔ SUNG:")
print("=" * 70)
print(f"✅ Cài mới: {installed_count} modules")
print(f"✓  Đã có: {already_installed} modules")
print(f"⚠️  Không tìm thấy: {len(not_found)} modules")
print()
print("🎉 HOÀN TẤT TẤT CẢ!")
print()
