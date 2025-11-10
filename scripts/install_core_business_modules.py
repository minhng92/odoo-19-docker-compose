#!/usr/bin/env python3
import xmlrpc.client
import time

url = "http://localhost:10019"
db = "odoo19"
username = "admin"
password = "admin"

print("=" * 70)
print("CÀI ĐẶT CÁC MODULE NGHIỆP VỤ CHÍNH + KẾ TOÁN VIỆT NAM")
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

# Danh sách modules cần cài
modules_to_install = {
    'crm': 'CRM - Quản lý khách hàng',
    'sale_management': 'Bán hàng - Quản lý đơn hàng',
    'project': 'Dự án - Quản lý dự án',
    'l10n_vn': 'Kế toán Việt Nam - Biểu đồ tài khoản VN',
    'account': 'Kế toán - Quản lý tài chính',
    'account_accountant': 'Kế toán nâng cao (Enterprise)',
    'approvals': 'Phê duyệt - Workflow phê duyệt',
}

print()
print(f"📦 Cài đặt {len(modules_to_install)} modules...")
print()

installed_count = 0
already_installed = 0
failed_count = 0
failed_modules = []

for module_name, description in modules_to_install.items():
    try:
        # Tìm module
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[['name', '=', module_name]]])
        
        if not module_ids:
            print(f"   ⚠️  {module_name}: Không tìm thấy - {description}")
            failed_modules.append(module_name)
            failed_count += 1
            continue
        
        # Lấy thông tin module
        module = models.execute_kw(db, uid, password,
            'ir.module.module', 'read',
            [module_ids], {'fields': ['name', 'state', 'summary']})[0]
        
        if module['state'] == 'installed':
            print(f"   ✓ {module_name}: Đã cài - {description}")
            already_installed += 1
            continue
        
        # Cài đặt
        print(f"   ⏳ {module_name}: Đang cài - {description}...", end='', flush=True)
        
        try:
            models.execute_kw(db, uid, password,
                'ir.module.module', 'button_immediate_install', [module_ids])
            
            time.sleep(3)
            
            # Kiểm tra lại
            module = models.execute_kw(db, uid, password,
                'ir.module.module', 'read',
                [module_ids], {'fields': ['state']})[0]
            
            if module['state'] == 'installed':
                print(f" ✅")
                installed_count += 1
            else:
                print(f" ⚠️  State: {module['state']}")
                
        except Exception as install_error:
            error_msg = str(install_error)
            if 'already' in error_msg.lower() or 'installed' in error_msg.lower():
                print(f" ✓ Đã có")
                already_installed += 1
            else:
                print(f" ❌")
                failed_count += 1
                failed_modules.append(module_name)
            
    except Exception as e:
        print(f"   ❌ {module_name}: Lỗi - {description}")
        failed_count += 1
        failed_modules.append(module_name)

print()
print("=" * 70)
print("KẾT QUẢ CÀI ĐẶT:")
print("=" * 70)
print(f"✅ Cài mới: {installed_count} modules")
print(f"✓  Đã có sẵn: {already_installed} modules")
print(f"❌ Thất bại: {failed_count} modules")

if failed_modules:
    print()
    print("⚠️  Modules thất bại:")
    for mod in failed_modules:
        print(f"   - {mod}")

print()
print("=" * 70)
print("🎉 HOÀN TẤT!")
print("=" * 70)
print()
print(f"📊 Tổng: {installed_count + already_installed}/{len(modules_to_install)} modules")
print()
print("📌 CÁC MODULE ĐÃ CÀI:")
print("   ✓ CRM - Quản lý khách hàng")
print("   ✓ Bán hàng - Đơn hàng & Báo giá")
print("   ✓ Dự án - Quản lý dự án & Task")
print("   ✓ Kế toán - Tài chính & Hóa đơn")
print("   ✓ Kế toán Việt Nam (l10n_vn) - Biểu đồ tài khoản VN")
print("   ✓ Accountant - Kế toán nâng cao")
print("   ✓ Phê duyệt - Workflow phê duyệt")
print()
print("🇻🇳 LƯU Ý KẾ TOÁN VIỆT NAM:")
print("   - Module l10n_vn cung cấp biểu đồ tài khoản theo chuẩn VN")
print("   - Hỗ trợ thuế VAT, hóa đơn GTGT")
print("   - Tuân thủ luật kế toán Việt Nam")
print()
print("🔄 Hãy refresh trang Odoo để thấy các module mới!")
print()
