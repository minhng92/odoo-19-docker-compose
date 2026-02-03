#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cài đặt module HR (Nhân sự) trong Odoo
"""

import xmlrpc.client
import time

# Cấu hình kết nối
URL = "http://localhost:10019"
DB = "odoo19"
USERNAME = "admin"
PASSWORD = "admin"

def connect_odoo():
    """Kết nối tới Odoo"""
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USERNAME, PASSWORD, {})
    
    if not uid:
        raise Exception("Không thể xác thực. Kiểm tra lại username/password!")
    
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    return uid, models

def install_module(uid, models, module_name):
    """Cài đặt module"""
    print(f"🔍 Đang tìm module '{module_name}'...")
    
    # Tìm module
    module_ids = models.execute_kw(
        DB, uid, PASSWORD,
        'ir.module.module', 'search',
        [[['name', '=', module_name]]]
    )
    
    if not module_ids:
        print(f"❌ Không tìm thấy module '{module_name}'")
        return False
    
    # Kiểm tra trạng thái
    module_info = models.execute_kw(
        DB, uid, PASSWORD,
        'ir.module.module', 'read',
        [module_ids, ['name', 'state']]
    )
    
    if module_info[0]['state'] == 'installed':
        print(f"✅ Module '{module_name}' đã được cài đặt!")
        return True
    
    print(f"📦 Đang cài đặt module '{module_name}'...")
    
    # Cài đặt module
    models.execute_kw(
        DB, uid, PASSWORD,
        'ir.module.module', 'button_immediate_install',
        [module_ids]
    )
    
    print(f"⏳ Đợi module '{module_name}' hoàn tất cài đặt...")
    time.sleep(5)  # Đợi 5 giây để module được cài đặt
    
    # Kiểm tra lại
    module_info = models.execute_kw(
        DB, uid, PASSWORD,
        'ir.module.module', 'read',
        [module_ids, ['name', 'state']]
    )
    
    if module_info[0]['state'] == 'installed':
        print(f"✅ Module '{module_name}' đã được cài đặt thành công!")
        return True
    else:
        print(f"⚠️  Module '{module_name}' đang trong trạng thái: {module_info[0]['state']}")
        return False

def main():
    """Hàm main"""
    print("\n" + "="*80)
    print("📦 CÀI ĐẶT MODULE HR (NHÂN SỰ) TRONG ODOO")
    print("="*80)
    print(f"🌐 URL: {URL}")
    print(f"🗄️  Database: {DB}")
    print(f"👤 User: {USERNAME}")
    print("="*80 + "\n")
    
    try:
        # Kết nối Odoo
        print("🔌 Đang kết nối tới Odoo...")
        uid, models = connect_odoo()
        print(f"✅ Kết nối thành công! User ID: {uid}\n")
        
        # Cài đặt module hr
        success = install_module(uid, models, 'hr')
        
        if success:
            print("\n" + "="*80)
            print("✅ HOÀN TẤT! MODULE HR ĐÃ SẴN SÀNG SỬ DỤNG")
            print("="*80)
            print("\n📌 Bây giờ bạn có thể chạy script tạo cấu trúc tổ chức:")
            print("   python3 scripts/create_company_structure.py")
            print("="*80 + "\n")
        else:
            print("\n❌ Không thể cài đặt module HR. Vui lòng kiểm tra log Odoo.")
        
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
