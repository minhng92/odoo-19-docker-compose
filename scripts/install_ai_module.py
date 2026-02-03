#!/usr/bin/env python3
import xmlrpc.client
import time

url = "http://localhost:10019"
db = "odoo19"
username = "admin"
password = "admin"

print("=" * 70)
print("CÀI ĐẶT ODOO AI MODULE")
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

# Tìm các AI modules
ai_modules = ['ai_app', 'ai', 'odoo_ai', 'base_ai', 'web_ai']

print()
print(f"🔍 Tìm kiếm AI modules...")
print()

found_modules = []

for module_name in ai_modules:
    try:
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[['name', '=', module_name]]])
        
        if module_ids:
            module = models.execute_kw(db, uid, password,
                'ir.module.module', 'read',
                [module_ids], {'fields': ['name', 'state', 'summary', 'shortdesc']})[0]
            
            found_modules.append(module)
            print(f"   ✓ Tìm thấy: {module['name']}")
            print(f"     Tên: {module.get('shortdesc', 'N/A')}")
            print(f"     Trạng thái: {module['state']}")
            print()
    except Exception as e:
        continue

if not found_modules:
    print("❌ Không tìm thấy AI module trong hệ thống!")
    print()
    print("🔍 Tìm tất cả modules có chứa 'ai' trong tên...")
    print()
    
    # Tìm tất cả modules có 'ai' trong tên
    all_ai = models.execute_kw(db, uid, password,
        'ir.module.module', 'search_read',
        [[['name', 'ilike', 'ai']]],
        {'fields': ['name', 'state', 'shortdesc'], 'limit': 20})
    
    if all_ai:
        print(f"📋 Tìm thấy {len(all_ai)} modules liên quan đến AI:")
        print()
        for mod in all_ai:
            status = "✓ Installed" if mod['state'] == 'installed' else "○ Available"
            print(f"   {status} - {mod['name']}: {mod.get('shortdesc', 'N/A')}")
    else:
        print("⚠️  Không tìm thấy module nào liên quan đến AI")
    
    print()
    print("=" * 70)
    print("THÔNG TIN:")
    print("=" * 70)
    print()
    print("📌 Module AI là tính năng mới của Odoo 19 Enterprise.")
    print("   Có thể module chưa có trong bản Enterprise này.")
    print()
    print("💡 GIẢI PHÁP:")
    print("   1. Update Enterprise addons về phiên bản mới nhất")
    print("   2. Kiểm tra xem module có trong thư mục enterprise/")
    print("   3. Module AI có thể cần subscription/license key riêng")
    print()
    exit(0)

# Cài đặt modules tìm thấy
print()
print("=" * 70)
print("CÀI ĐẶT AI MODULES")
print("=" * 70)
print()

installed_count = 0

for module in found_modules:
    module_name = module['name']
    
    if module['state'] == 'installed':
        print(f"✓ {module_name}: Đã cài đặt")
        continue
    
    print(f"⏳ {module_name}: Đang cài đặt...", end='', flush=True)
    
    try:
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[['name', '=', module_name]]])
        
        models.execute_kw(db, uid, password,
            'ir.module.module', 'button_immediate_install', [module_ids])
        
        time.sleep(3)
        print(f" ✅")
        installed_count += 1
        
    except Exception as e:
        print(f" ❌ Lỗi: {str(e)[:60]}")

print()
print("=" * 70)
print("KẾT QUẢ:")
print("=" * 70)
print(f"✅ Đã cài: {installed_count} AI modules")
print()
print("🔄 Refresh trang Odoo để thấy AI module!")
print()
