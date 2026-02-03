#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo cấu trúc tổ chức đầy đủ cho công ty admin
- Tạo phòng ban đầy đủ
- Tạo 50 nhân viên với thông tin chi tiết
- Phân bổ nhân viên vào các phòng ban
"""

import xmlrpc.client
import random
from datetime import datetime, timedelta

# Cấu hình kết nối
URL = "http://localhost:10019"
DB = "odoo19"
USERNAME = "admin"
PASSWORD = "admin"

# Danh sách tên Việt Nam
LAST_NAMES = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
MIDDLE_NAMES = ["Văn", "Thị", "Đức", "Minh", "Hữu", "Thanh", "Công", "Thành", "Quốc", "Anh", "Tuấn", "Duy", "Hoàng", "Ngọc", "Phương", "Hồng"]
FIRST_NAMES_MALE = ["Hùng", "Cường", "Tài", "Toàn", "Nam", "Dũng", "Long", "Khoa", "Phong", "Bình", "Hải", "Đạt", "Phúc", "Quân", "Khánh", "Sơn", "Tuấn", "Vũ", "Thắng", "Hiếu"]
FIRST_NAMES_FEMALE = ["Lan", "Hương", "Mai", "Hoa", "Thu", "Linh", "Nga", "Trang", "Anh", "Hà", "Thảo", "Dung", "Hằng", "Nhung", "Huyền", "Chi", "Vy", "My", "Ngân", "Yến"]

PHONE_PREFIXES = ["090", "091", "093", "094", "097", "098", "096", "086", "088", "089"]
EMAIL_DOMAINS = ["gmail.com", "quantracxanh.vn", "envitech.vn", "outlook.com", "yahoo.com"]

# Danh sách địa chỉ ở các quận TP.HCM
ADDRESSES = [
    "123 Nguyễn Văn Linh, Quận 7, TP.HCM",
    "45 Lê Văn Việt, Quận 9, TP.HCM",
    "78 Võ Văn Ngân, Thủ Đức, TP.HCM",
    "234 Lê Đức Thọ, Gò Vấp, TP.HCM",
    "56 Phan Văn Trị, Bình Thạnh, TP.HCM",
    "89 Hoàng Văn Thụ, Tân Bình, TP.HCM",
    "12 Cách Mạng Tháng 8, Quận 3, TP.HCM",
    "67 Nguyễn Thị Minh Khai, Quận 1, TP.HCM",
    "145 Điện Biên Phủ, Quận 10, TP.HCM",
    "23 Lý Thường Kiệt, Quận 11, TP.HCM",
    "98 Lạc Long Quân, Quận 11, TP.HCM",
    "34 Nguyễn Oanh, Gò Vấp, TP.HCM",
    "76 Phạm Văn Đồng, Thủ Đức, TP.HCM",
    "21 Kha Vạn Cân, Thủ Đức, TP.HCM",
    "54 Quang Trung, Gò Vấp, TP.HCM",
]

def generate_phone():
    """Tạo số điện thoại ngẫu nhiên"""
    prefix = random.choice(PHONE_PREFIXES)
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"{prefix}{suffix}"

def generate_email(full_name, domain=None):
    """Tạo email từ tên"""
    if domain is None:
        domain = random.choice(EMAIL_DOMAINS)
    # Loại bỏ dấu và tạo email
    name_parts = full_name.lower().split()
    # Lấy tên và họ
    if len(name_parts) >= 2:
        email_name = f"{name_parts[-1]}.{name_parts[0]}"
    else:
        email_name = name_parts[0]
    
    # Chuyển đổi tiếng Việt không dấu
    replacements = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'đ': 'd',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    }
    
    for viet, latin in replacements.items():
        email_name = email_name.replace(viet, latin)
    
    return f"{email_name}@{domain}"

def generate_name(is_male=True):
    """Tạo tên ngẫu nhiên"""
    last_name = random.choice(LAST_NAMES)
    middle_name = random.choice(MIDDLE_NAMES)
    first_name = random.choice(FIRST_NAMES_MALE if is_male else FIRST_NAMES_FEMALE)
    return f"{last_name} {middle_name} {first_name}"

def generate_random_date(start_year=1980, end_year=2000):
    """Tạo ngày sinh ngẫu nhiên"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    time_between = end_date - start_date
    days = random.randint(0, time_between.days)
    return (start_date + timedelta(days=days)).strftime("%Y-%m-%d")

def connect_odoo():
    """Kết nối tới Odoo"""
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USERNAME, PASSWORD, {})
    
    if not uid:
        raise Exception("Không thể xác thực. Kiểm tra lại username/password!")
    
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    return uid, models

def create_departments(uid, models):
    """Tạo các phòng ban"""
    print("\n" + "="*60)
    print("📋 ĐANG TẠO CÁC PHÒNG BAN...")
    print("="*60)
    
    departments_data = [
        # Phòng ban chính
        {
            'name': 'Phòng Quan Trắc Môi Trường (QT)',
            'code': 'QT',
            'manager_name': 'Nguyễn Thanh Hùng',
            'employees_count': 15
        },
        {
            'name': 'Phòng Phân Tích Hóa (PTH)',
            'code': 'PTH',
            'parent': 'Phòng Thí Nghiệm',
            'manager_name': 'Nguyễn Trần Minh Toàn',
            'employees_count': 5
        },
        {
            'name': 'Phòng Phân Tích Sinh (PTS)',
            'code': 'PTS',
            'parent': 'Phòng Thí Nghiệm',
            'manager_name': 'Trần Thị Hồng Linh',
            'employees_count': 5
        },
        # Các phòng ban khác
        {
            'name': 'Phòng Hành Chính Nhân Sự',
            'code': 'HCNS',
            'manager_name': 'Lê Văn Nam',
            'employees_count': 5
        },
        {
            'name': 'Phòng Kế Toán Tài Chính',
            'code': 'KTTC',
            'manager_name': 'Phạm Thị Mai',
            'employees_count': 4
        },
        {
            'name': 'Phòng Kinh Doanh',
            'code': 'KD',
            'manager_name': 'Hoàng Đức Cường',
            'employees_count': 6
        },
        {
            'name': 'Phòng Kỹ Thuật',
            'code': 'KT',
            'manager_name': 'Vũ Quốc Đạt',
            'employees_count': 5
        },
        {
            'name': 'Phòng IT',
            'code': 'IT',
            'manager_name': 'Đặng Minh Khoa',
            'employees_count': 3
        },
        {
            'name': 'Phòng QA/QC',
            'code': 'QAQC',
            'manager_name': 'Bùi Thị Thảo',
            'employees_count': 2
        },
    ]
    
    created_departments = {}
    
    for dept_data in departments_data:
        dept_vals = {
            'name': dept_data['name'],
            'company_id': 1,  # My Company (admin company)
        }
        
        dept_id = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'create',
            [dept_vals]
        )
        
        created_departments[dept_data['code']] = {
            'id': dept_id,
            'name': dept_data['name'],
            'code': dept_data['code'],
            'manager_name': dept_data['manager_name'],
            'employees_count': dept_data['employees_count'],
            'employees': []
        }
        
        print(f"  ✅ Đã tạo: {dept_data['name']} (ID: {dept_id})")
    
    return created_departments

def create_employees(uid, models, departments):
    """Tạo 50 nhân viên với thông tin đầy đủ"""
    print("\n" + "="*60)
    print("👥 ĐANG TẠO 50 NHÂN VIÊN...")
    print("="*60)
    
    employee_count = 0
    
    # Tạo trưởng phòng trước
    print("\n🎯 Tạo các trưởng phòng:")
    for dept_code, dept_info in departments.items():
        is_male = random.choice([True, False])
        
        # Sử dụng tên đã định cho các trưởng phòng cụ thể
        if dept_code == 'QT':
            full_name = 'Nguyễn Thanh Hùng'
            is_male = True
        elif dept_code == 'PTH':
            full_name = 'Nguyễn Trần Minh Toàn'
            is_male = True
        elif dept_code == 'PTS':
            full_name = 'Trần Thị Hồng Linh'
            is_male = False
        else:
            full_name = dept_info['manager_name']
            is_male = 'Thị' not in full_name
        
        work_email = generate_email(full_name, "quantracxanh.vn")
        
        emp_vals = {
            'name': full_name,
            'work_phone': generate_phone(),
            'work_email': work_email,
            'mobile_phone': generate_phone(),
            'department_id': dept_info['id'],
            'job_title': f"Trưởng phòng {dept_info['name']}",
            'company_id': 1,
        }
        
        emp_id = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.employee', 'create',
            [emp_vals]
        )
        
        # Cập nhật manager cho department
        models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'write',
            [[dept_info['id']], {'manager_id': emp_id}]
        )
        
        dept_info['employees'].append(emp_id)
        employee_count += 1
        
        print(f"  ✅ Trưởng phòng {dept_code}: {full_name} (ID: {emp_id})")
    
    # Tạo nhân viên cho từng phòng ban
    print("\n👨‍💼 Tạo nhân viên các phòng ban:")
    for dept_code, dept_info in departments.items():
        remaining = dept_info['employees_count'] - 1  # Trừ trưởng phòng
        
        print(f"\n  📌 Phòng {dept_code} - Tạo {remaining} nhân viên:")
        
        for i in range(remaining):
            is_male = random.choice([True, False])
            full_name = generate_name(is_male)
            work_email = generate_email(full_name, "quantracxanh.vn")
            
            # Chức danh ngẫu nhiên
            job_titles = [
                "Chuyên viên",
                "Nhân viên chính",
                "Nhân viên",
                "Kỹ thuật viên",
                "Chuyên viên cao cấp"
            ]
            
            emp_vals = {
                'name': full_name,
                'work_phone': generate_phone(),
                'work_email': work_email,
                'mobile_phone': generate_phone(),
                'department_id': dept_info['id'],
                'job_title': f"{random.choice(job_titles)} {dept_info['name']}",
                'company_id': 1,
            }
            
            emp_id = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.employee', 'create',
                [emp_vals]
            )
            
            dept_info['employees'].append(emp_id)
            employee_count += 1
            
            print(f"    • {full_name}")
    
    print(f"\n✅ Đã tạo tổng cộng {employee_count} nhân viên!")
    return employee_count

def print_summary(departments):
    """In tóm tắt cấu trúc tổ chức"""
    print("\n" + "="*80)
    print("📊 TÓM TẮT CẤU TRÚC TỔ CHỨC")
    print("="*80)
    
    total_employees = 0
    
    for dept_code, dept_info in departments.items():
        emp_count = len(dept_info['employees'])
        total_employees += emp_count
        
        print(f"\n🏢 {dept_info['name']} ({dept_code})")
        print(f"   👤 Trưởng phòng: {dept_info['manager_name']}")
        print(f"   👥 Số nhân viên: {emp_count}")
    
    print("\n" + "="*80)
    print(f"📈 TỔNG SỐ NHÂN VIÊN: {total_employees}")
    print("="*80)

def main():
    """Hàm main"""
    print("\n" + "="*80)
    print("🏢 TẠO CẤU TRÚC TỔ CHỨC ĐẦY ĐỦ CHO CÔNG TY ADMIN")
    print("="*80)
    print(f"🌐 URL: {URL}")
    print(f"🗄️  Database: {DB}")
    print(f"👤 User: {USERNAME}")
    print("="*80)
    
    try:
        # Kết nối Odoo
        print("\n🔌 Đang kết nối tới Odoo...")
        uid, models = connect_odoo()
        print(f"✅ Kết nối thành công! User ID: {uid}")
        
        # Tạo phòng ban
        departments = create_departments(uid, models)
        
        # Tạo nhân viên
        employee_count = create_employees(uid, models, departments)
        
        # In tóm tắt
        print_summary(departments)
        
        print("\n" + "="*80)
        print("✅ HOÀN TẤT! TẤT CẢ DỮ LIỆU ĐÃ ĐƯỢC TẠO TRONG DATABASE odoo19")
        print("="*80)
        print("\n📌 Truy cập Odoo để xem kết quả:")
        print(f"   🌐 URL: {URL}")
        print(f"   👤 Username: {USERNAME}")
        print(f"   🔑 Password: {PASSWORD}")
        print("\n📂 Xem danh sách nhân viên:")
        print("   Settings → Users & Companies → Employees")
        print("\n📂 Xem cơ cấu tổ chức:")
        print("   Settings → Users & Companies → Departments")
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
