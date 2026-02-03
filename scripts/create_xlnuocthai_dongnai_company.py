#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo công ty TNHH Xử Lý Nước Thải Công Nghiệp Đồng Nai
17 nhân viên, 6 phòng ban
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

def create_company(uid, models):
    """Tạo công ty mới"""
    print("\n🏢 Tạo công ty TNHH Xử Lý Nước Thải Công Nghiệp Đồng Nai...")
    
    company_data = {
        'name': 'TNHH Xử Lý Nước Thải Công Nghiệp Đồng Nai',
        'street': '789 Quốc lộ 1A',
        'street2': 'Phường Tân Tiến, Thành phố Biên Hòa',
        'city': 'Đồng Nai',
        'zip': '810000',
        'country_id': 241,  # Vietnam
        'phone': '0251-3836-888',
        'email': 'info@xlnuocthai-dongnai.vn',
        'website': 'www.xlnuocthai-dongnai.vn',
        'vat': '3600123456',
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
            [[['name', '=', 'TNHH Xử Lý Nước Thải Công Nghiệp Đồng Nai']]]
        )
        if company_ids:
            print(f"✅ Sử dụng công ty hiện có (ID: {company_ids[0]})")
            return company_ids[0]
        raise e

def create_departments(uid, models, company_id):
    """Tạo các phòng ban"""
    print("\n📂 Tạo phòng ban...")
    
    departments = [
        {"name": "Ban Giám đốc", "description": "Điều hành chung"},
        {"name": "Phòng Vận hành - Kỹ thuật", "description": "Vận hành hệ thống XLNT"},
        {"name": "Phòng Kinh doanh - Dịch vụ", "description": "Kinh doanh dịch vụ XLNT"},
        {"name": "Phòng Phân tích - Quan trắc", "description": "Phân tích nước thải"},
        {"name": "Phòng Thiết kế - Thi công", "description": "Thiết kế và thi công hệ thống XLNT"},
        {"name": "Phòng Hành chính - Kế toán", "description": "Quản lý hành chính, tài chính"}
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
    """Tạo 17 nhân viên với thông tin chi tiết"""
    print("\n👥 Tạo nhân viên...")
    
    employees = [
        # Ban Giám đốc (2)
        {
            "name": "Nguyễn Hoàng Minh",
            "department": "Ban Giám đốc",
            "job_title": "Giám đốc",
            "work_phone": "0251-3836-888",
            "mobile_phone": "0908123456",
            "work_email": "giamdoc@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Trần Văn Công",
            "department": "Ban Giám đốc",
            "job_title": "Phó Giám đốc",
            "work_phone": "0251-3836-889",
            "mobile_phone": "0908234567",
            "work_email": "pgd@xlnuocthai-dongnai.vn"
        },
        
        # Phòng Vận hành - Kỹ thuật (5)
        {
            "name": "Lê Thanh Tùng",
            "department": "Phòng Vận hành - Kỹ thuật",
            "job_title": "Trưởng phòng Vận hành",
            "work_phone": "0251-3836-890",
            "mobile_phone": "0918123456",
            "work_email": "tpvanhanh@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Phạm Văn Đạt",
            "department": "Phòng Vận hành - Kỹ thuật",
            "job_title": "Kỹ sư Vận hành XLNT",
            "work_phone": "0251-3836-891",
            "mobile_phone": "0918234567",
            "work_email": "ksvanhanh@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Võ Minh Quân",
            "department": "Phòng Vận hành - Kỹ thuật",
            "job_title": "Kỹ thuật viên Điện - Cơ",
            "work_phone": "0251-3836-892",
            "mobile_phone": "0918345678",
            "work_email": "ktv.dienco@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Hoàng Văn Bình",
            "department": "Phòng Vận hành - Kỹ thuật",
            "job_title": "Công nhân Vận hành",
            "work_phone": "0251-3836-893",
            "mobile_phone": "0918456789",
            "work_email": "congnhan1@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Ngô Văn Hùng",
            "department": "Phòng Vận hành - Kỹ thuật",
            "job_title": "Công nhân Vận hành",
            "work_phone": "0251-3836-894",
            "mobile_phone": "0918567890",
            "work_email": "congnhan2@xlnuocthai-dongnai.vn"
        },
        
        # Phòng Kinh doanh - Dịch vụ (3)
        {
            "name": "Phan Thị Thu Hà",
            "department": "Phòng Kinh doanh - Dịch vụ",
            "job_title": "Trưởng phòng Kinh doanh",
            "work_phone": "0251-3836-895",
            "mobile_phone": "0928123456",
            "work_email": "tpkd@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Đỗ Văn Long",
            "department": "Phòng Kinh doanh - Dịch vụ",
            "job_title": "Nhân viên Kinh doanh",
            "work_phone": "0251-3836-896",
            "mobile_phone": "0928234567",
            "work_email": "nvkd@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Lý Thị Ánh",
            "department": "Phòng Kinh doanh - Dịch vụ",
            "job_title": "Nhân viên Chăm sóc khách hàng",
            "work_phone": "0251-3836-897",
            "mobile_phone": "0928345678",
            "work_email": "cskh@xlnuocthai-dongnai.vn"
        },
        
        # Phòng Phân tích - Quan trắc (2)
        {
            "name": "Trương Thị Mai",
            "department": "Phòng Phân tích - Quan trắc",
            "job_title": "Trưởng phòng Phân tích",
            "work_phone": "0251-3836-898",
            "mobile_phone": "0938123456",
            "work_email": "tpphanttich@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Bùi Văn Tài",
            "department": "Phòng Phân tích - Quan trắc",
            "job_title": "Kỹ thuật viên Phân tích",
            "work_phone": "0251-3836-899",
            "mobile_phone": "0938234567",
            "work_email": "ktv.phantich@xlnuocthai-dongnai.vn"
        },
        
        # Phòng Thiết kế - Thi công (3)
        {
            "name": "Đinh Quốc Việt",
            "department": "Phòng Thiết kế - Thi công",
            "job_title": "Trưởng phòng Thiết kế",
            "work_phone": "0251-3836-900",
            "mobile_phone": "0948123456",
            "work_email": "tpthietke@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Huỳnh Văn Sơn",
            "department": "Phòng Thiết kế - Thi công",
            "job_title": "Kỹ sư Thiết kế XLNT",
            "work_phone": "0251-3836-901",
            "mobile_phone": "0948234567",
            "work_email": "ksthietke@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Nguyễn Thị Lan",
            "department": "Phòng Thiết kế - Thi công",
            "job_title": "Kỹ sư Giám sát Thi công",
            "work_phone": "0251-3836-902",
            "mobile_phone": "0948345678",
            "work_email": "ksgsamsat@xlnuocthai-dongnai.vn"
        },
        
        # Phòng Hành chính - Kế toán (2)
        {
            "name": "Cao Thị Ngọc",
            "department": "Phòng Hành chính - Kế toán",
            "job_title": "Kế toán - Thủ quỹ",
            "work_phone": "0251-3836-903",
            "mobile_phone": "0958123456",
            "work_email": "ketoan@xlnuocthai-dongnai.vn"
        },
        {
            "name": "Lâm Văn Toàn",
            "department": "Phòng Hành chính - Kế toán",
            "job_title": "Nhân viên Hành chính",
            "work_phone": "0251-3836-904",
            "mobile_phone": "0958234567",
            "work_email": "hanhchinh@xlnuocthai-dongnai.vn"
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
    print("🏢 TẠO CÔNG TY TNHH XỬ LÝ NƯỚC THẢI CÔNG NGHIỆP ĐỒNG NAI")
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
            {'fields': ['name', 'street', 'city', 'phone', 'email', 'website', 'vat']}
        )[0]
        
        print(f"\n🏢 {company_info['name']}")
        print(f"📍 {company_info.get('street', '')}, {company_info.get('city', '')}")
        print(f"☎️  {company_info.get('phone', 'N/A')}")
        print(f"📧 {company_info.get('email', 'N/A')}")
        print(f"🌐 {company_info.get('website', 'N/A')}")
        print(f"🏛️  MST: {company_info.get('vat', 'N/A')}")
        
        # Thống kê phòng ban
        print("\n📂 CƠ CẤU TỔ CHỨC:")
        
        all_depts = models.execute_kw(
            DB, uid, PASSWORD,
            'hr.department', 'search_read',
            [[['company_id', '=', company_id]]],
            {'fields': ['name', 'total_employee'], 'order': 'name'}
        )
        
        total_emps = 0
        for dept in all_depts:
            if dept['total_employee'] > 0:
                print(f"  👥 {dept['name']}: {dept['total_employee']} nhân viên")
                total_emps += dept['total_employee']
        
        print(f"\n✅ Tổng số phòng ban: {len([d for d in all_depts if d['total_employee'] > 0])}")
        print(f"👥 Tổng số nhân viên: {total_emps}")
        
        print("\n" + "="*80)
        print("🔐 THÔNG TIN ĐĂNG NHẬP")
        print("="*80)
        print("URL: http://localhost:10019")
        print("Database: odoo19")
        print("\nTài khoản mẫu:")
        print("  - Giám đốc: giamdoc@xlnuocthai-dongnai.vn / admin123")
        print("  - Phó GĐ: pgd@xlnuocthai-dongnai.vn / admin123")
        print("  - TP Vận hành: tpvanhanh@xlnuocthai-dongnai.vn / admin123")
        print("  - Các tài khoản khác: [email] / admin123")
        
        # Liệt kê tất cả công ty trong database
        print("\n" + "="*80)
        print("📋 DANH SÁCH TẤT CẢ CÔNG TY TRONG DATABASE")
        print("="*80)
        
        all_companies = models.execute_kw(
            DB, uid, PASSWORD,
            'res.company', 'search_read',
            [[]],
            {'fields': ['name', 'city'], 'order': 'name'}
        )
        
        for idx, company in enumerate(all_companies, 1):
            city = company.get('city', 'N/A')
            print(f"{idx}. {company['name']} - {city}")
        
        print(f"\n✅ Tổng số công ty: {len(all_companies)}")
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
