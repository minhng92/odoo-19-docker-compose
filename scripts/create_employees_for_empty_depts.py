#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo nhân viên cho các phòng ban trống
"""

import xmlrpc.client
import random

URL = "http://localhost:10019"
DB = "odoo19"
USERNAME = "admin"
PASSWORD = "admin"

# Danh sách họ và tên Việt Nam
LAST_NAMES = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
MIDDLE_NAMES = ["Văn", "Thị", "Đức", "Hữu", "Minh", "Thanh", "Hoàng", "Công", "Anh", "Quốc", "Hồng", "Thành", "Tuấn", "Duy"]
FIRST_NAMES_MALE = ["Hùng", "Dũng", "Cường", "Khoa", "Phong", "Toàn", "Hải", "Nam", "Sơn", "Đạt", "Tài", "Bình", "Khánh", "Quân", "Long", "Hưng", "Việt", "Đức", "Tuấn", "Huy"]
FIRST_NAMES_FEMALE = ["Hà", "Lan", "Hương", "Mai", "Linh", "Nga", "Yến", "My", "Trang", "Anh", "Huyền", "Phương", "Thu", "Thảo", "Chi"]

def generate_vietnamese_name(gender="male"):
    """Tạo tên người Việt Nam"""
    last = random.choice(LAST_NAMES)
    middle = random.choice(MIDDLE_NAMES)
    if gender == "male":
        first = random.choice(FIRST_NAMES_MALE)
    else:
        first = random.choice(FIRST_NAMES_FEMALE)
    return f"{last} {middle} {first}"

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
    print("👥 TẠO NHÂN VIÊN CHO CÁC PHÒNG BAN TRỐNG")
    print("="*80)
    
    try:
        uid, models = connect_odoo()
        print("✅ Kết nối thành công!\n")
        
        # Danh sách phòng ban và chức danh
        departments = [
            {
                "name": "Ban Giám đốc",
                "positions": [
                    {"title": "Giám đốc", "gender": "male"},
                    {"title": "Phó Giám đốc", "gender": "male"}
                ]
            },
            {
                "name": "Phòng Mua hàng",
                "positions": [
                    {"title": "Trưởng phòng Mua hàng", "gender": "male"},
                    {"title": "Nhân viên Mua hàng", "gender": "female"}
                ]
            },
            {
                "name": "Phòng Kho vận",
                "positions": [
                    {"title": "Trưởng phòng Kho vận", "gender": "male"},
                    {"title": "Nhân viên Kho", "gender": "male"}
                ]
            },
            {
                "name": "Bộ phận Dự án",
                "positions": [
                    {"title": "Trưởng bộ phận Dự án", "gender": "male"},
                    {"title": "Nhân viên Dự án", "gender": "female"}
                ]
            },
            {
                "name": "Phòng Tư vấn",
                "positions": [
                    {"title": "Trưởng phòng Tư vấn", "gender": "female"},
                    {"title": "Nhân viên Tư vấn", "gender": "female"}
                ]
            },
            {
                "name": "Phòng Pháp lý",
                "positions": [
                    {"title": "Trưởng phòng Pháp lý", "gender": "female"},
                    {"title": "Nhân viên Pháp lý", "gender": "female"}
                ]
            }
        ]
        
        # Lấy danh sách email đã tồn tại
        existing_employees = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.employee', 'search_read',
            [[]],
            {'fields': ['work_email']}
        )
        existing_emails = {emp['work_email'] for emp in existing_employees if emp.get('work_email')}
        
        total_created = 0
        
        for dept_info in departments:
            dept_name = dept_info["name"]
            
            # Tìm ID phòng ban
            dept_ids = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.department', 'search',
                [[['name', '=', dept_name]]]
            )
            
            if not dept_ids:
                print(f"⚠️  Không tìm thấy phòng: {dept_name}")
                continue
            
            dept_id = dept_ids[0]
            
            print(f"\n📂 {dept_name}")
            print("─" * 80)
            
            for position_info in dept_info["positions"]:
                # Tạo tên ngẫu nhiên
                max_attempts = 50
                for _ in range(max_attempts):
                    name = generate_vietnamese_name(position_info["gender"])
                    # Tạo email từ tên (bỏ dấu)
                    name_parts = name.lower().split()
                    # Simple ASCII conversion cho email
                    email_name = ""
                    replacements = {
                        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
                        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
                        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
                        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
                        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
                        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
                        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
                        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
                        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
                        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
                        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
                        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
                        'đ': 'd'
                    }
                    
                    for part in name_parts:
                        for char in part:
                            email_name += replacements.get(char, char)
                        email_name += ""
                    
                    email_name = email_name.strip()
                    work_email = f"{email_name}@quantracxanh.vn"
                    
                    if work_email not in existing_emails:
                        break
                else:
                    work_email = f"{email_name}{random.randint(1, 999)}@quantracxanh.vn"
                
                # Tạo số điện thoại
                mobile_phone = f"0{random.randint(300000000, 999999999)}"
                
                # Tạo nhân viên
                employee_data = {
                    'name': name,
                    'department_id': dept_id,
                    'job_title': position_info["title"],
                    'work_email': work_email,
                    'mobile_phone': mobile_phone,
                    'company_id': 1,
                }
                
                try:
                    emp_id = models.execute_kw(
                        DB, uid, PASSWORD,
                        'hr.employee', 'create',
                        [employee_data]
                    )
                    
                    # Tạo user account
                    try:
                        user_data = {
                            'name': name,
                            'login': work_email,
                            'email': work_email,
                            'password': 'admin123',
                            'company_id': 1,
                            'company_ids': [(6, 0, [1])],
                        }
                        
                        models.execute_kw(
                            DB, uid, PASSWORD,
                            'res.users', 'create',
                            [user_data]
                        )
                    except:
                        pass  # User có thể đã tồn tại
                    
                    print(f"  ✅ {name} - {position_info['title']}")
                    print(f"     📧 {work_email}")
                    print(f"     📱 {mobile_phone}")
                    
                    existing_emails.add(work_email)
                    total_created += 1
                    
                except Exception as e:
                    print(f"  ❌ Lỗi tạo {name}: {str(e)}")
        
        print("\n" + "="*80)
        print(f"✅ Đã tạo {total_created} nhân viên mới")
        
        # Hiển thị tổng kết
        print("\n📊 TỔNG KẾT SAU KHI TẠO")
        print("="*80)
        
        all_depts = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'search_read',
            [[]],
            {'fields': ['name', 'total_employee'], 'order': 'name'}
        )
        
        total_employees = 0
        for dept in all_depts:
            if dept['total_employee'] > 0:
                print(f"  👥 {dept['name']}: {dept['total_employee']} nhân viên")
                total_employees += dept['total_employee']
        
        print("\n" + "="*80)
        print(f"✅ Tổng số phòng ban: {len(all_depts)}")
        print(f"👥 Tổng số nhân viên: {total_employees}")
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
