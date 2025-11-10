#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo/cập nhật phòng ban theo cấu trúc mới
Nếu phòng ban đã tồn tại → đổi tên
Nếu chưa có → tạo mới
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

def create_or_update_department(uid, models, name, old_names=None):
    """Tạo mới hoặc cập nhật phòng ban"""
    
    # Tìm phòng ban hiện có với tên mới
    dept_ids = models.execute_kw(
        DB, uid, PASSWORD,
        'hr.department', 'search',
        [[['name', '=', name]]]
    )
    
    if dept_ids:
        print(f"  ✅ Phòng ban '{name}' đã tồn tại (ID: {dept_ids[0]})")
        return dept_ids[0]
    
    # Nếu có tên cũ, tìm và đổi tên
    if old_names:
        for old_name in old_names:
            old_dept_ids = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.department', 'search',
                [[['name', '=', old_name]]]
            )
            
            if old_dept_ids:
                # Đổi tên phòng ban
                models.execute_kw(
                    DB, uid, PASSWORD,
                    'hr.department', 'write',
                    [[old_dept_ids[0]], {'name': name}]
                )
                print(f"  🔄 Đã đổi tên: '{old_name}' → '{name}' (ID: {old_dept_ids[0]})")
                return old_dept_ids[0]
    
    # Tạo mới nếu không tìm thấy
    dept_id = models.execute_kw(
        DB, uid, PASSWORD,
        'hr.department', 'create',
        [{
            'name': name,
            'company_id': 1  # My Company
        }]
    )
    
    print(f"  ✨ Đã tạo mới: '{name}' (ID: {dept_id})")
    return dept_id

def main():
    """Hàm main"""
    print("\n" + "="*80)
    print("🏢 TẠO/CẬP NHẬT CẤU TRÚC PHÒNG BAN")
    print("="*80)
    
    # Cấu trúc phòng ban mới
    # Format: (tên mới, [danh sách tên cũ có thể])
    departments = [
        ("Ban Giám đốc", []),
        ("Phòng Kinh doanh", ["Phòng Kinh Doanh"]),
        ("Phòng Mua hàng", []),
        ("Phòng Kho vận", []),
        ("Phòng Kế toán", ["Phòng Kế Toán Tài Chính"]),
        ("Phòng Kỹ thuật", ["Phòng Quan Trắc Môi Trường (QT)"]),
        ("Phòng Thí nghiệm (PTN)", ["Phòng Phân Tích Hóa (PTH)", "Phòng Phân Tích Sinh (PTS)"]),
        ("Bộ phận Dự án", []),
        ("Phòng Tư vấn", []),
        ("Phòng Pháp lý", []),
        ("Phòng Nhân sự", ["Phòng Hành Chính Nhân Sự"]),
    ]
    
    try:
        # Kết nối
        print("\n🔌 Đang kết nối tới Odoo...")
        uid, models = connect_odoo()
        print(f"✅ Kết nối thành công! User ID: {uid}")
        
        # Lấy danh sách phòng ban hiện có
        existing_depts = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'search_read',
            [[]],
            {'fields': ['name']}
        )
        
        print(f"\n📊 Hiện có {len(existing_depts)} phòng ban trong hệ thống")
        print("\n🔧 Đang xử lý các phòng ban...")
        print("="*80)
        
        created_depts = {}
        
        for dept_name, old_names in departments:
            dept_id = create_or_update_department(uid, models, dept_name, old_names)
            created_depts[dept_name] = dept_id
        
        # Xóa các phòng ban không còn sử dụng
        print("\n🗑️  Kiểm tra phòng ban cũ không còn dùng...")
        
        old_dept_names = [
            "Phòng IT",
            "Phòng QA/QC"
        ]
        
        for old_name in old_dept_names:
            old_ids = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.department', 'search',
                [[['name', '=', old_name]]]
            )
            
            if old_ids:
                # Kiểm tra xem có nhân viên không
                emp_count = models.execute_kw(
                    DB, uid, PASSWORD,
                    'hr.employee', 'search_count',
                    [[['department_id', '=', old_ids[0]]]]
                )
                
                if emp_count > 0:
                    print(f"  ⚠️  '{old_name}' còn {emp_count} nhân viên, không xóa")
                else:
                    models.execute_kw(
                        DB, uid, PASSWORD,
                        'hr.department', 'unlink',
                        [old_ids]
                    )
                    print(f"  🗑️  Đã xóa: '{old_name}'")
        
        print("\n" + "="*80)
        print("📊 DANH SÁCH PHÒNG BAN SAU KHI CẬP NHẬT")
        print("="*80)
        
        final_depts = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'search_read',
            [[]],
            {'fields': ['name', 'total_employee'], 'order': 'name'}
        )
        
        for dept in final_depts:
            emp_count = dept.get('total_employee', 0)
            print(f"  📁 {dept['name']}: {emp_count} nhân viên")
        
        print("\n" + "="*80)
        print("✅ HOÀN TẤT CẬP NHẬT CẤU TRÚC PHÒNG BAN!")
        print("="*80)
        print(f"\n📊 Tổng số phòng ban: {len(final_depts)}")
        print("\n📌 Xem danh sách phòng ban:")
        print("   Employees → Configuration → Departments")
        print("\n💡 Lưu ý:")
        print("   - Nhân viên từ phòng cũ vẫn giữ nguyên phòng ban")
        print("   - Bạn có thể di chuyển nhân viên sang phòng mới bằng tay")
        print("   - Phòng IT và QA/QC còn nhân viên nên chưa xóa")
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
