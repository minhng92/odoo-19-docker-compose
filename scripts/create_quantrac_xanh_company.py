#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo công ty TNHH Quan Trắc Môi Trường Xanh
Công ty nhỏ: 20 nhân viên, 6 phòng ban chính
"""

import xmlrpc.client
import random

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

def create_company(uid, models):
    """Tạo công ty mới"""
    print("\n🏢 Tạo công ty TNHH Quan Trắc Môi Trường Xanh...")
    
    company_data = {
        'name': 'TNHH Quan Trắc Môi Trường Xanh',
        'street': '123 Đường Nguyễn Văn Linh',
        'street2': 'Phường Tân Phú, Quận 7',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'country_id': 241,  # Vietnam
        'phone': '028-3775-1234',
        'email': 'info@quantracxanh.vn',
        'website': 'www.quantracxanh.vn',
        'vat': '0123456789',
    }
    
    try:
        company_id = models.execute_kw(
            DB, uid, PASSWORD,
            'res.company', 'create',
            [company_data]
        )
        print(f"✅ Đã tạo công ty (ID: {company_id})")
        return company_id
    except Exception as e:
        print(f"⚠️  Công ty có thể đã tồn tại, tìm kiếm...")
        company_ids = models.execute_kw(
            DB, uid, PASSWORD,
            'res.company', 'search',
            [[['name', '=', 'TNHH Quan Trắc Môi Trường Xanh']]]
        )
        if company_ids:
            print(f"✅ Sử dụng công ty hiện có (ID: {company_ids[0]})")
            return company_ids[0]
        raise e

def create_departments(uid, models, company_id):
    """Tạo các phòng ban cho công ty quan trắc môi trường"""
    print("\n📂 Tạo phòng ban...")
    
    departments = [
        {
            "name": "Ban Giám đốc",
            "description": "Điều hành chung"
        },
        {
            "name": "Phòng Kinh doanh - Marketing",
            "description": "Tìm kiếm khách hàng, chăm sóc khách hàng, marketing"
        },
        {
            "name": "Phòng Quan trắc Môi trường",
            "description": "Lấy mẫu, quan trắc nước, không khí, đất, tiếng ồn"
        },
        {
            "name": "Phòng Phân tích Thí nghiệm",
            "description": "Phân tích mẫu môi trường (hóa, sinh, vi sinh)"
        },
        {
            "name": "Phòng Hành chính - Kế toán",
            "description": "Quản lý hành chính, nhân sự, kế toán, tài chính"
        },
        {
            "name": "Phòng Tư vấn Môi trường",
            "description": "Tư vấn ĐTM, giấy phép môi trường, ISO 14001"
        }
    ]
    
    dept_ids = {}
    for dept in departments:
        try:
            dept_id = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.department', 'create',
                [{
                    'name': dept['name'],
                    'company_id': company_id,
                }]
            )
            dept_ids[dept['name']] = dept_id
            print(f"  ✅ {dept['name']}")
        except:
            # Nếu đã tồn tại, tìm ID
            existing = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.department', 'search',
                [[['name', '=', dept['name']], ['company_id', '=', company_id]]]
            )
            if existing:
                dept_ids[dept['name']] = existing[0]
                print(f"  ✅ {dept['name']} (đã tồn tại)")
    
    return dept_ids

def create_employees(uid, models, company_id, dept_ids):
    """Tạo 20 nhân viên với thông tin chi tiết"""
    print("\n👥 Tạo nhân viên...")
    
    # Danh sách nhân viên thực tế
    employees = [
        # Ban Giám đốc (2)
        {
            "name": "Nguyễn Văn Minh",
            "department": "Ban Giám đốc",
            "job_title": "Giám đốc",
            "work_phone": "028-3775-1234",
            "mobile_phone": "0903123456",
            "work_email": "giamdoc@quantracxanh.vn",
            "gender": "male"
        },
        {
            "name": "Trần Thị Hương",
            "department": "Ban Giám đốc",
            "job_title": "Phó Giám đốc",
            "work_phone": "028-3775-1235",
            "mobile_phone": "0903234567",
            "work_email": "pgd@quantracxanh.vn",
            "gender": "female"
        },
        
        # Phòng Kinh doanh - Marketing (4)
        {
            "name": "Lê Hoàng Nam",
            "department": "Phòng Kinh doanh - Marketing",
            "job_title": "Trưởng phòng Kinh doanh",
            "work_phone": "028-3775-1236",
            "mobile_phone": "0913456789",
            "work_email": "tpkd@quantracxanh.vn",
            "gender": "male"
        },
        {
            "name": "Phạm Thị Mai",
            "department": "Phòng Kinh doanh - Marketing",
            "job_title": "Nhân viên Kinh doanh",
            "work_phone": "028-3775-1237",
            "mobile_phone": "0913567890",
            "work_email": "nvkd1@quantracxanh.vn",
            "gender": "female"
        },
        {
            "name": "Hoàng Văn Đức",
            "department": "Phòng Kinh doanh - Marketing",
            "job_title": "Nhân viên Kinh doanh",
            "work_phone": "028-3775-1238",
            "mobile_phone": "0913678901",
            "work_email": "nvkd2@quantracxanh.vn",
            "gender": "male"
        },
        {
            "name": "Vũ Thị Lan",
            "department": "Phòng Kinh doanh - Marketing",
            "job_title": "Nhân viên Marketing",
            "work_phone": "028-3775-1239",
            "mobile_phone": "0913789012",
            "work_email": "marketing@quantracxanh.vn",
            "gender": "female"
        },
        
        # Phòng Quan trắc Môi trường (5)
        {
            "name": "Ngô Thanh Tùng",
            "department": "Phòng Quan trắc Môi trường",
            "job_title": "Trưởng phòng Quan trắc",
            "work_phone": "028-3775-1240",
            "mobile_phone": "0923456789",
            "work_email": "tpquantrac@quantracxanh.vn",
            "gender": "male"
        },
        {
            "name": "Đặng Văn Hải",
            "department": "Phòng Quan trắc Môi trường",
            "job_title": "Kỹ thuật viên Quan trắc Nước",
            "work_phone": "028-3775-1241",
            "mobile_phone": "0923567890",
            "work_email": "ktvnuoc@quantracxanh.vn",
            "gender": "male"
        },
        {
            "name": "Bùi Thị Ngọc",
            "department": "Phòng Quan trắc Môi trường",
            "job_title": "Kỹ thuật viên Quan trắc Không khí",
            "work_phone": "028-3775-1242",
            "mobile_phone": "0923678901",
            "work_email": "ktvkhongkhi@quantracxanh.vn",
            "gender": "female"
        },
        {
            "name": "Phan Minh Quân",
            "department": "Phòng Quan trắc Môi trường",
            "job_title": "Kỹ thuật viên Quan trắc Đất",
            "work_phone": "028-3775-1243",
            "mobile_phone": "0923789012",
            "work_email": "ktvdat@quantracxanh.vn",
            "gender": "male"
        },
        {
            "name": "Lý Thị Hà",
            "department": "Phòng Quan trắc Môi trường",
            "job_title": "Nhân viên Lấy mẫu",
            "work_phone": "028-3775-1244",
            "mobile_phone": "0923890123",
            "work_email": "laymau@quantracxanh.vn",
            "gender": "female"
        },
        
        # Phòng Phân tích Thí nghiệm (5)
        {
            "name": "Võ Đức Thành",
            "department": "Phòng Phân tích Thí nghiệm",
            "job_title": "Trưởng phòng Thí nghiệm",
            "work_phone": "028-3775-1245",
            "mobile_phone": "0933456789",
            "work_email": "tptn@quantracxanh.vn",
            "gender": "male"
        },
        {
            "name": "Huỳnh Thị Thu",
            "department": "Phòng Phân tích Thí nghiệm",
            "job_title": "Kỹ thuật viên Phân tích Hóa",
            "work_phone": "028-3775-1246",
            "mobile_phone": "0933567890",
            "work_email": "ktvhoa@quantracxanh.vn",
            "gender": "female"
        },
        {
            "name": "Đỗ Văn Long",
            "department": "Phòng Phân tích Thí nghiệm",
            "job_title": "Kỹ thuật viên Phân tích Sinh",
            "work_phone": "028-3775-1247",
            "mobile_phone": "0933678901",
            "work_email": "ktvsinh@quantracxanh.vn",
            "gender": "male"
        },
        {
            "name": "Trần Thị Phương",
            "department": "Phòng Phân tích Thí nghiệm",
            "job_title": "Kỹ thuật viên Vi sinh",
            "work_phone": "028-3775-1248",
            "mobile_phone": "0933789012",
            "work_email": "ktvvisinh@quantracxanh.vn",
            "gender": "female"
        },
        {
            "name": "Nguyễn Minh Tuấn",
            "department": "Phòng Phân tích Thí nghiệm",
            "job_title": "Nhân viên Kiểm soát chất lượng",
            "work_phone": "028-3775-1249",
            "mobile_phone": "0933890123",
            "work_email": "qc@quantracxanh.vn",
            "gender": "male"
        },
        
        # Phòng Hành chính - Kế toán (2)
        {
            "name": "Lê Thị Thanh",
            "department": "Phòng Hành chính - Kế toán",
            "job_title": "Kế toán trưởng",
            "work_phone": "028-3775-1250",
            "mobile_phone": "0943456789",
            "work_email": "ketoan@quantracxanh.vn",
            "gender": "female"
        },
        {
            "name": "Phạm Văn Tài",
            "department": "Phòng Hành chính - Kế toán",
            "job_title": "Nhân viên Hành chính",
            "work_phone": "028-3775-1251",
            "mobile_phone": "0943567890",
            "work_email": "hanhchinh@quantracxanh.vn",
            "gender": "male"
        },
        
        # Phòng Tư vấn Môi trường (2)
        {
            "name": "Hoàng Thị Linh",
            "department": "Phòng Tư vấn Môi trường",
            "job_title": "Chuyên viên Tư vấn ĐTM",
            "work_phone": "028-3775-1252",
            "mobile_phone": "0953456789",
            "work_email": "tuvan1@quantracxanh.vn",
            "gender": "female"
        },
        {
            "name": "Đặng Quốc Hùng",
            "department": "Phòng Tư vấn Môi trường",
            "job_title": "Chuyên viên Tư vấn ISO",
            "work_phone": "028-3775-1253",
            "mobile_phone": "0953567890",
            "work_email": "tuvan2@quantracxanh.vn",
            "gender": "male"
        }
    ]
    
    created_count = 0
    
    for emp_data in employees:
        dept_id = dept_ids.get(emp_data['department'])
        if not dept_id:
            continue
        
        employee_info = {
            'name': emp_data['name'],
            'department_id': dept_id,
            'job_title': emp_data['job_title'],
            'work_email': emp_data['work_email'],
            'work_phone': emp_data.get('work_phone', ''),
            'mobile_phone': emp_data.get('mobile_phone', ''),
            'company_id': company_id,
        }
        
        try:
            emp_id = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.employee', 'create',
                [employee_info]
            )
            
            # Tạo user account
            try:
                user_data = {
                    'name': emp_data['name'],
                    'login': emp_data['work_email'],
                    'email': emp_data['work_email'],
                    'password': 'admin123',
                    'company_id': company_id,
                    'company_ids': [(6, 0, [company_id])],
                }
                
                models.execute_kw(
                    DB, uid, PASSWORD,
                    'res.users', 'create',
                    [user_data]
                )
            except:
                pass
            
            print(f"  ✅ {emp_data['name']} - {emp_data['job_title']}")
            print(f"     📧 {emp_data['work_email']} | 📱 {emp_data.get('mobile_phone', 'N/A')}")
            created_count += 1
            
        except Exception as e:
            print(f"  ❌ Lỗi tạo {emp_data['name']}: {str(e)}")
    
    return created_count

def main():
    """Hàm main"""
    print("\n" + "="*80)
    print("🏢 TẠO CÔNG TY TNHH QUAN TRẮC MÔI TRƯỜNG XANH")
    print("="*80)
    
    try:
        uid, models = connect_odoo()
        print("✅ Kết nối Odoo thành công!")
        
        # Tạo công ty
        company_id = create_company(uid, models)
        
        # Tạo phòng ban
        dept_ids = create_departments(uid, models, company_id)
        
        # Tạo nhân viên
        employee_count = create_employees(uid, models, company_id, dept_ids)
        
        # Tổng kết
        print("\n" + "="*80)
        print("📊 TỔNG KẾT CÔNG TY")
        print("="*80)
        
        # Lấy thông tin công ty
        company_info = models.execute_kw(
            DB, uid, PASSWORD,
            'res.company', 'read',
            [[company_id]],
            {'fields': ['name', 'street', 'city', 'phone', 'email', 'website']}
        )[0]
        
        print(f"\n🏢 {company_info['name']}")
        print(f"📍 {company_info.get('street', '')}, {company_info.get('city', '')}")
        print(f"☎️  {company_info.get('phone', 'N/A')}")
        print(f"📧 {company_info.get('email', 'N/A')}")
        print(f"🌐 {company_info.get('website', 'N/A')}")
        
        # Thống kê phòng ban
        print("\n📂 CƠ CẤU TỔ CHỨC:")
        
        all_depts = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'search_read',
            [[['company_id', '=', company_id]]],
            {'fields': ['name', 'total_employee'], 'order': 'name'}
        )
        
        for dept in all_depts:
            print(f"  👥 {dept['name']}: {dept['total_employee']} nhân viên")
        
        print(f"\n✅ Tổng số phòng ban: {len(all_depts)}")
        print(f"👥 Tổng số nhân viên: {employee_count}")
        
        print("\n" + "="*80)
        print("🔐 THÔNG TIN ĐĂNG NHẬP")
        print("="*80)
        print("URL: http://localhost:10019")
        print("Database: odoo19")
        print("\nTài khoản:")
        print("  - Giám đốc: giamdoc@quantracxanh.vn / admin123")
        print("  - Phó GĐ: pgd@quantracxanh.vn / admin123")
        print("  - Trưởng phòng KD: tpkd@quantracxanh.vn / admin123")
        print("  - Các tài khoản khác: [email] / admin123")
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
