#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cập nhật tất cả nhân viên về My Company (công ty chính admin)
"""

import xmlrpc.client

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

def main():
    """Hàm main"""
    print("\n" + "="*80)
    print("🔄 CẬP NHẬT NHÂN VIÊN VỀ MY COMPANY")
    print("="*80)
    
    try:
        # Kết nối
        print("\n🔌 Đang kết nối tới Odoo...")
        uid, models = connect_odoo()
        print(f"✅ Kết nối thành công! User ID: {uid}")
        
        # Tìm My Company (company_id = 1)
        company = models.execute_kw(
            DB, uid, PASSWORD,
            'res.company', 'search_read',
            [[['id', '=', 1]]],
            {'fields': ['name'], 'limit': 1}
        )
        
        if not company:
            print("❌ Không tìm thấy My Company!")
            return False
        
        company_name = company[0]['name']
        print(f"✅ Tìm thấy công ty: {company_name}")
        
        # Lấy tất cả nhân viên
        employees = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.employee', 'search_read',
            [[]],
            {'fields': ['name', 'company_id']}
        )
        
        print(f"\n📊 Tìm thấy {len(employees)} nhân viên")
        
        # Cập nhật tất cả về My Company
        print("\n🔄 Đang cập nhật nhân viên về My Company...")
        
        updated_count = 0
        for emp in employees:
            current_company = emp['company_id'][1] if emp['company_id'] else 'Chưa có công ty'
            
            # Chỉ cập nhật nếu chưa thuộc My Company
            if emp['company_id'] and emp['company_id'][0] == 1:
                print(f"  ✓ {emp['name']}: Đã thuộc My Company")
            else:
                models.execute_kw(
                    DB, uid, PASSWORD,
                    'hr.employee', 'write',
                    [[emp['id']], {'company_id': 1}]
                )
                updated_count += 1
                print(f"  ✅ {emp['name']}: {current_company} → My Company")
        
        print("\n" + "="*80)
        print(f"✅ ĐÃ CẬP NHẬT {updated_count} NHÂN VIÊN VỀ MY COMPANY!")
        print("="*80)
        
        # Cập nhật departments về My Company
        print("\n🔄 Đang cập nhật phòng ban về My Company...")
        
        departments = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'search_read',
            [[]],
            {'fields': ['name', 'company_id']}
        )
        
        dept_updated = 0
        for dept in departments:
            if dept['company_id'] and dept['company_id'][0] != 1:
                models.execute_kw(
                    DB, uid, PASSWORD,
                    'hr.department', 'write',
                    [[dept['id']], {'company_id': 1}]
                )
                dept_updated += 1
                print(f"  ✅ {dept['name']} → My Company")
        
        print(f"\n✅ Đã cập nhật {dept_updated} phòng ban về My Company")
        
        print("\n" + "="*80)
        print("✅ HOÀN TẤT!")
        print("="*80)
        print("\n📌 Bây giờ bạn có thể xem nhân viên tại:")
        print("   Employees → Employees")
        print("   hoặc")
        print("   Settings → Users & Companies → Employees")
        print("\n📂 Xem cơ cấu tổ chức:")
        print("   Employees → Configuration → Departments")
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
