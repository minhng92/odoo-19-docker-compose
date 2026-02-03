#!/usr/bin/env python3
import xmlrpc.client

url = "http://localhost:10019"
db = "odoo19"
username = "admin"
password = "admin"

print("=" * 60)
print("CẬP NHẬT APPS LIST - KÍCH HOẠT ENTERPRISE")
print("=" * 60)
print()

# Kết nối
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("❌ Không thể đăng nhập!")
    exit(1)

print(f"✅ Đã đăng nhập: uid={uid}")
print()

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Update apps list
print("🔄 Đang update apps list...")
try:
    models.execute_kw(db, uid, password, 'ir.module.module', 'update_list', [])
    print("✅ Đã update apps list!")
except Exception as e:
    print(f"❌ Lỗi update: {e}")
    exit(1)

print()

# Tìm Enterprise modules
print("🔍 Tìm Enterprise modules...")
enterprise_modules = models.execute_kw(db, uid, password,
    'ir.module.module', 'search_read',
    [[['name', 'in', ['web_studio', 'documents', 'helpdesk', 'social', 'sign', 
                      'planning', 'account_accountant', 'hr_payroll', 'quality_control']]]],
    {'fields': ['name', 'state', 'summary']})

if enterprise_modules:
    print(f"✅ Tìm thấy {len(enterprise_modules)} Enterprise modules!")
    print()
    print("📋 Danh sách Enterprise modules:")
    for mod in enterprise_modules:
        status = "✓ Installed" if mod['state'] == 'installed' else "○ Available"
        print(f"   {status} - {mod['name']}: {mod.get('summary', 'N/A')}")
else:
    print("❌ KHÔNG tìm thấy Enterprise modules!")
    print()
    print("🔍 Kiểm tra addons_path...")
    
    # Lấy config
    config = models.execute_kw(db, uid, password,
        'ir.config_parameter', 'search_read',
        [[['key', '=', 'addons_path']]],
        {'fields': ['value']})
    
    if config:
        print(f"   addons_path: {config[0]['value']}")
    else:
        print("   ⚠️  Không tìm thấy addons_path trong config")

print()
print("=" * 60)
print("HOÀN TẤT!")
print("=" * 60)
print()
print("📌 BƯỚC TIẾP THEO:")
print("1. Truy cập: http://localhost:10019")
print("2. Vào Apps → Remove filter 'Apps'")
print("3. Tìm 'Studio' hoặc 'Documents' để verify Enterprise")
print()
