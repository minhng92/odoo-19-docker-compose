#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cài đặt các module cần thiết cho phân quyền
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

def install_module(uid, models, module_name):
    """Cài đặt module"""
    print(f"🔍 Kiểm tra module '{module_name}'...")
    
    # Tìm module
    module_ids = models.execute_kw(
        DB, uid, PASSWORD,
        'ir.module.module', 'search',
        [[['name', '=', module_name]]]
    )
    
    if not module_ids:
        print(f"  ❌ Không tìm thấy module '{module_name}'")
        return False
    
    # Kiểm tra trạng thái
    module_info = models.execute_kw(
        DB, uid, PASSWORD,
        'ir.module.module', 'read',
        [module_ids, ['name', 'state']]
    )
    
    if module_info[0]['state'] == 'installed':
        print(f"  ✅ Module '{module_name}' đã được cài đặt")
        return True
    
    print(f"  📦 Đang cài đặt module '{module_name}'...")
    
    try:
        # Cài đặt module
        models.execute_kw(
            DB, uid, PASSWORD,
            'ir.module.module', 'button_immediate_install',
            [module_ids]
        )
        
        print(f"  ⏳ Đợi module '{module_name}' hoàn tất...")
        time.sleep(3)
        
        print(f"  ✅ Module '{module_name}' đã được cài đặt!")
        return True
    except Exception as e:
        print(f"  ❌ Lỗi cài đặt '{module_name}': {str(e)}")
        return False

def main():
    """Hàm main"""
    print("\n" + "="*80)
    print("📦 CÀI ĐẶT CÁC MODULE CẦN THIẾT")
    print("="*80 + "\n")
    
    # Danh sách module cần cài đặt
    required_modules = [
        'sale_management',      # Sales & CRM
        'crm',                  # CRM
        'project',              # Project Management
        'purchase',             # Purchase
        'stock',                # Inventory
        'account',              # Accounting
        'hr',                   # HR (đã cài)
        'hr_timesheet',         # Timesheet
    ]
    
    try:
        uid, models = connect_odoo()
        print(f"✅ Kết nối thành công! User ID: {uid}\n")
        
        installed = 0
        for module in required_modules:
            if install_module(uid, models, module):
                installed += 1
            print()
        
        print("="*80)
        print(f"✅ Đã cài đặt {installed}/{len(required_modules)} module")
        print("="*80)
        print("\n⏳ Đang restart Odoo để áp dụng các module mới...")
        print("   Vui lòng chờ 10 giây...\n")
        time.sleep(10)
        
        print("✅ HOÀN TẤT! Bây giờ có thể chạy script phân quyền:")
        print("   python3 scripts/setup_permissions.py")
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
