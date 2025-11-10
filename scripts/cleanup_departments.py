#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script dọn dẹp phòng ban trùng lặp và di chuyển nhân viên
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
    print("🧹 DỌN DẸP PHÒNG BAN TRÙNG LẶP VÀ DI CHUYỂN NHÂN VIÊN")
    print("="*80)
    
    try:
        uid, models = connect_odoo()
        print("✅ Kết nối thành công!")
        
        # Mapping: tên phòng ban cũ → tên phòng ban mới
        dept_mapping = {
            # Các phòng cũ → phòng mới
            "Phòng Kinh Doanh": "Phòng Kinh doanh",
            "Phòng Kế Toán Tài Chính": "Phòng Kế toán",
            "Phòng Quan Trắc Môi Trường (QT)": "Phòng Kỹ thuật",
            "Phòng Phân Tích Hóa (PTH)": "Phòng Thí nghiệm (PTN)",
            "Phòng Phân Tích Sinh (PTS)": "Phòng Thí nghiệm (PTN)",
            "Phòng Hành Chính Nhân Sự": "Phòng Nhân sự",
            "Phòng Kỹ Thuật": "Phòng Kỹ thuật",
            "Phòng IT": "Ban Giám đốc",  # IT thường có quyền cao
            "Phòng QA/QC": "Phòng Kỹ thuật",
        }
        
        print("\n🔄 Đang di chuyển nhân viên sang phòng ban mới...")
        print("="*80)
        
        moved_count = 0
        
        for old_dept_name, new_dept_name in dept_mapping.items():
            # Tìm phòng cũ
            old_dept_ids = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.department', 'search',
                [[['name', '=', old_dept_name]]]
            )
            
            # Tìm phòng mới
            new_dept_ids = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.department', 'search',
                [[['name', '=', new_dept_name]]]
            )
            
            if not old_dept_ids or not new_dept_ids:
                continue
            
            old_dept_id = old_dept_ids[0]
            new_dept_id = new_dept_ids[0]
            
            # Lấy nhân viên của phòng cũ
            employees = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.employee', 'search_read',
                [[['department_id', '=', old_dept_id]]],
                {'fields': ['name', 'department_id']}
            )
            
            if employees:
                print(f"\n📂 {old_dept_name} → {new_dept_name}")
                
                for emp in employees:
                    # Di chuyển nhân viên
                    models.execute_kw(
                        DB, uid, PASSWORD,
                        'hr.employee', 'write',
                        [[emp['id']], {'department_id': new_dept_id}]
                    )
                    print(f"  ✅ {emp['name']}")
                    moved_count += 1
        
        print(f"\n✅ Đã di chuyển {moved_count} nhân viên")
        
        # Xóa các phòng ban trống
        print("\n🗑️  Đang xóa phòng ban trống...")
        print("="*80)
        
        all_depts = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'search_read',
            [[]],
            {'fields': ['name', 'total_employee']}
        )
        
        deleted_count = 0
        keep_depts = ["Ban Giám đốc", "Phòng Kinh doanh", "Phòng Mua hàng", 
                      "Phòng Kho vận", "Phòng Kế toán", "Phòng Kỹ thuật",
                      "Phòng Thí nghiệm (PTN)", "Bộ phận Dự án", "Phòng Tư vấn",
                      "Phòng Pháp lý", "Phòng Nhân sự", "Administration"]
        
        for dept in all_depts:
            # Nếu phòng không có nhân viên và không trong danh sách giữ lại
            if dept['total_employee'] == 0 and dept['name'] not in keep_depts:
                try:
                    models.execute_kw(
                        DB, uid, PASSWORD,
                        'hr.department', 'unlink',
                        [[dept['id']]]
                    )
                    print(f"  🗑️  Đã xóa: {dept['name']}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  ⚠️  Không thể xóa {dept['name']}: {str(e)}")
        
        print(f"\n✅ Đã xóa {deleted_count} phòng ban trống")
        
        # Hiển thị kết quả cuối cùng
        print("\n" + "="*80)
        print("📊 CẤU TRÚC PHÒNG BAN SAU KHI DỌN DẸP")
        print("="*80)
        
        final_depts = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'search_read',
            [[]],
            {'fields': ['name', 'total_employee'], 'order': 'name'}
        )
        
        total_employees = 0
        for dept in final_depts:
            emp_count = dept.get('total_employee', 0)
            total_employees += emp_count
            icon = "👥" if emp_count > 0 else "📁"
            print(f"  {icon} {dept['name']}: {emp_count} nhân viên")
        
        print("\n" + "="*80)
        print("✅ HOÀN TẤT DỌN DẸP!")
        print("="*80)
        print(f"\n📊 Tổng số phòng ban: {len(final_depts)}")
        print(f"👥 Tổng số nhân viên: {total_employees}")
        print("\n📌 Xem kết quả:")
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
