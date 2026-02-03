#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script di chuyển nhân viên sang phòng ban mới (viết hoa/thường đúng)
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

def find_or_create_dept(uid, models, name):
    """Tìm hoặc tạo phòng ban"""
    dept_ids = models.execute_kw(
        DB, uid, PASSWORD,
        'hr.department', 'search',
        [[['name', '=', name]]]
    )
    
    if dept_ids:
        return dept_ids[0]
    
    # Tạo mới nếu chưa có
    dept_id = models.execute_kw(
        DB, uid, PASSWORD,
        'hr.department', 'create',
        [{'name': name, 'company_id': 1}]
    )
    print(f"  ✨ Tạo mới phòng: {name}")
    return dept_id

def main():
    """Hàm main"""
    print("\n" + "="*80)
    print("🔄 DI CHUYỂN NHÂN VIÊN SANG PHÒNG BAN MỚI")
    print("="*80)
    
    try:
        uid, models = connect_odoo()
        print("✅ Kết nối thành công!\n")
        
        # Mapping chi tiết: phòng cũ → phòng mới
        moves = [
            ("Phòng Kinh Doanh", "Phòng Kinh doanh"),
            ("Phòng Kế Toán Tài Chính", "Phòng Kế toán"),
            ("Phòng Kỹ Thuật", "Phòng Kỹ thuật"),
            ("Phòng Quan Trắc Môi Trường (QT)", "Phòng Kỹ thuật"),  # Gộp vào Kỹ thuật
            ("Phòng Phân Tích Hóa (PTH)", "Phòng Thí nghiệm (PTN)"),
            ("Phòng Phân Tích Sinh (PTS)", "Phòng Thí nghiệm (PTN)"),
            ("Phòng Hành Chính Nhân Sự", "Phòng Nhân sự"),
        ]
        
        total_moved = 0
        
        for old_name, new_name in moves:
            # Tìm phòng cũ
            old_dept = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.department', 'search_read',
                [[['name', '=', old_name]]],
                {'fields': ['id', 'name', 'total_employee']}
            )
            
            if not old_dept:
                continue
            
            old_dept = old_dept[0]
            emp_count = old_dept['total_employee']
            
            if emp_count == 0:
                continue
            
            # Tìm hoặc tạo phòng mới
            new_dept_id = find_or_create_dept(uid, models, new_name)
            
            # Lấy nhân viên
            employees = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.employee', 'search_read',
                [[['department_id', '=', old_dept['id']]]],
                {'fields': ['name']}
            )
            
            print(f"\n📂 {old_name} ({emp_count} NV) → {new_name}")
            
            # Di chuyển từng nhân viên
            for emp in employees:
                models.execute_kw(
                    DB, uid, PASSWORD,
                    'hr.employee', 'write',
                    [[emp['id']], {'department_id': new_dept_id}]
                )
                print(f"  ✅ {emp['name']}")
                total_moved += 1
        
        print(f"\n✅ Đã di chuyển {total_moved} nhân viên")
        
        # Xóa phòng ban cũ (trống)
        print("\n🗑️  Dọn dẹp phòng ban cũ...")
        
        old_depts = [
            "Phòng Kinh Doanh",
            "Phòng Kế Toán Tài Chính", 
            "Phòng Kỹ Thuật",
            "Phòng Quan Trắc Môi Trường (QT)",
            "Phòng Phân Tích Hóa (PTH)",
            "Phòng Phân Tích Sinh (PTS)",
            "Phòng Hành Chính Nhân Sự"
        ]
        
        for dept_name in old_depts:
            dept_ids = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.department', 'search',
                [[['name', '=', dept_name]]]
            )
            
            if dept_ids:
                try:
                    models.execute_kw(
                        DB, uid, PASSWORD,
                        'hr.department', 'unlink',
                        [dept_ids]
                    )
                    print(f"  🗑️  Xóa: {dept_name}")
                except:
                    pass
        
        # Hiển thị kết quả
        print("\n" + "="*80)
        print("📊 CẤU TRÚC PHÒNG BAN CUỐI CÙNG")
        print("="*80)
        
        final_depts = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'search_read',
            [[]],
            {'fields': ['name', 'total_employee'], 'order': 'name'}
        )
        
        dept_with_emp = []
        dept_without_emp = []
        
        for dept in final_depts:
            if dept['total_employee'] > 0:
                dept_with_emp.append(dept)
            else:
                dept_without_emp.append(dept)
        
        print("\n✅ PHÒNG BAN CÓ NHÂN VIÊN:")
        for dept in dept_with_emp:
            print(f"  👥 {dept['name']}: {dept['total_employee']} nhân viên")
        
        print("\n📁 PHÒNG BAN TRỐNG (chưa có nhân viên):")
        for dept in dept_without_emp:
            print(f"  📁 {dept['name']}")
        
        total_emp = sum(d['total_employee'] for d in final_depts)
        
        print("\n" + "="*80)
        print(f"✅ Tổng số phòng ban: {len(final_depts)}")
        print(f"👥 Tổng số nhân viên: {total_emp}")
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
