#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo công ty Cổ phần Môi Trường và An Toàn Lao Động Miền Nam
25 nhân viên, 7 phòng ban
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
    print("\n🏢 Tạo công ty Cổ phần Môi Trường và An Toàn Lao Động Miền Nam...")
    
    company_data = {
        'name': 'Công ty Cổ phần Môi Trường và An Toàn Lao Động Miền Nam',
        'street': '456 Đường Hoàng Văn Thụ',
        'street2': 'Phường 2, Quận Tân Bình',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'country_id': 241,  # Vietnam
        'phone': '028-3844-5678',
        'email': 'contact@moitruongatld.vn',
        'website': 'www.moitruongatld.vn',
        'vat': '0123456790',
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
            [[['name', '=', 'Công ty Cổ phần Môi Trường và An Toàn Lao Động Miền Nam']]]
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
        {"name": "Phòng Kinh doanh", "description": "Kinh doanh dịch vụ MT & ATVSLĐ"},
        {"name": "Phòng An toàn Vệ sinh Lao động", "description": "Dịch vụ ATVSLĐ, đo môi trường LĐ"},
        {"name": "Phòng Quan trắc - Phân tích", "description": "Lấy mẫu và phân tích môi trường"},
        {"name": "Phòng Tư vấn - Thiết kế", "description": "Tư vấn ĐTM, thiết kế HTXLMT"},
        {"name": "Phòng Hành chính - Nhân sự", "description": "Quản lý hành chính, nhân sự"},
        {"name": "Phòng Kế toán - Tài chính", "description": "Kế toán, tài chính, thuế"}
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
    """Tạo 25 nhân viên với thông tin chi tiết"""
    print("\n👥 Tạo nhân viên...")
    
    employees = [
        # Ban Giám đốc (3)
        {
            "name": "Trần Quốc Tuấn",
            "department": "Ban Giám đốc",
            "job_title": "Giám đốc",
            "work_phone": "028-3844-5678",
            "mobile_phone": "0909123456",
            "work_email": "giamdoc@moitruongatld.vn"
        },
        {
            "name": "Nguyễn Thị Hồng Nhung",
            "department": "Ban Giám đốc",
            "job_title": "Phó Giám đốc Kỹ thuật",
            "work_phone": "028-3844-5679",
            "mobile_phone": "0909234567",
            "work_email": "pgd.kythuat@moitruongatld.vn"
        },
        {
            "name": "Lê Văn Thành",
            "department": "Ban Giám đốc",
            "job_title": "Phó Giám đốc Kinh doanh",
            "work_phone": "028-3844-5680",
            "mobile_phone": "0909345678",
            "work_email": "pgd.kinhdoanh@moitruongatld.vn"
        },
        
        # Phòng Kinh doanh (4)
        {
            "name": "Phạm Minh Đức",
            "department": "Phòng Kinh doanh",
            "job_title": "Trưởng phòng Kinh doanh",
            "work_phone": "028-3844-5681",
            "mobile_phone": "0919123456",
            "work_email": "tpkd@moitruongatld.vn"
        },
        {
            "name": "Võ Thị Ánh Tuyết",
            "department": "Phòng Kinh doanh",
            "job_title": "Nhân viên Kinh doanh",
            "work_phone": "028-3844-5682",
            "mobile_phone": "0919234567",
            "work_email": "nvkd1@moitruongatld.vn"
        },
        {
            "name": "Đặng Văn Hiệp",
            "department": "Phòng Kinh doanh",
            "job_title": "Nhân viên Kinh doanh",
            "work_phone": "028-3844-5683",
            "mobile_phone": "0919345678",
            "work_email": "nvkd2@moitruongatld.vn"
        },
        {
            "name": "Huỳnh Thị Thanh Thảo",
            "department": "Phòng Kinh doanh",
            "job_title": "Nhân viên Chăm sóc khách hàng",
            "work_phone": "028-3844-5684",
            "mobile_phone": "0919456789",
            "work_email": "cskh@moitruongatld.vn"
        },
        
        # Phòng An toàn Vệ sinh Lao động (5)
        {
            "name": "Ngô Thanh Bình",
            "department": "Phòng An toàn Vệ sinh Lao động",
            "job_title": "Trưởng phòng ATVSLĐ",
            "work_phone": "028-3844-5685",
            "mobile_phone": "0929123456",
            "work_email": "tpatvs@moitruongatld.vn"
        },
        {
            "name": "Trương Văn Nam",
            "department": "Phòng An toàn Vệ sinh Lao động",
            "job_title": "Kỹ sư An toàn Lao động",
            "work_phone": "028-3844-5686",
            "mobile_phone": "0929234567",
            "work_email": "ksatld@moitruongatld.vn"
        },
        {
            "name": "Lý Thị Mai Anh",
            "department": "Phòng An toàn Vệ sinh Lao động",
            "job_title": "Chuyên viên Vệ sinh Lao động",
            "work_phone": "028-3844-5687",
            "mobile_phone": "0929345678",
            "work_email": "cvvsld@moitruongatld.vn"
        },
        {
            "name": "Bùi Đức Hải",
            "department": "Phòng An toàn Vệ sinh Lao động",
            "job_title": "Kỹ thuật viên Đo môi trường LĐ",
            "work_phone": "028-3844-5688",
            "mobile_phone": "0929456789",
            "work_email": "ktv.domtld@moitruongatld.vn"
        },
        {
            "name": "Phan Thị Ngọc",
            "department": "Phòng An toàn Vệ sinh Lao động",
            "job_title": "Nhân viên Đánh giá rủi ro",
            "work_phone": "028-3844-5689",
            "mobile_phone": "0929567890",
            "work_email": "danhgiaruiro@moitruongatld.vn"
        },
        
        # Phòng Quan trắc - Phân tích (5)
        {
            "name": "Hoàng Văn Tuấn",
            "department": "Phòng Quan trắc - Phân tích",
            "job_title": "Trưởng phòng Quan trắc",
            "work_phone": "028-3844-5690",
            "mobile_phone": "0939123456",
            "work_email": "tpquantrac@moitruongatld.vn"
        },
        {
            "name": "Đỗ Thị Hương",
            "department": "Phòng Quan trắc - Phân tích",
            "job_title": "Kỹ thuật viên Lấy mẫu",
            "work_phone": "028-3844-5691",
            "mobile_phone": "0939234567",
            "work_email": "ktv.laymau@moitruongatld.vn"
        },
        {
            "name": "Nguyễn Văn Hùng",
            "department": "Phòng Quan trắc - Phân tích",
            "job_title": "Kỹ thuật viên Phân tích",
            "work_phone": "028-3844-5692",
            "mobile_phone": "0939345678",
            "work_email": "ktv.phantich@moitruongatld.vn"
        },
        {
            "name": "Trần Thị Thu Hà",
            "department": "Phòng Quan trắc - Phân tích",
            "job_title": "Kỹ thuật viên Phân tích Hóa",
            "work_phone": "028-3844-5693",
            "mobile_phone": "0939456789",
            "work_email": "ktv.hoa@moitruongatld.vn"
        },
        {
            "name": "Vũ Minh Khoa",
            "department": "Phòng Quan trắc - Phân tích",
            "job_title": "Nhân viên QA/QC",
            "work_phone": "028-3844-5694",
            "mobile_phone": "0939567890",
            "work_email": "qaqc@moitruongatld.vn"
        },
        
        # Phòng Tư vấn - Thiết kế (4)
        {
            "name": "Lâm Quốc Việt",
            "department": "Phòng Tư vấn - Thiết kế",
            "job_title": "Trưởng phòng Tư vấn",
            "work_phone": "028-3844-5695",
            "mobile_phone": "0949123456",
            "work_email": "tptuvan@moitruongatld.vn"
        },
        {
            "name": "Nguyễn Thị Lan Anh",
            "department": "Phòng Tư vấn - Thiết kế",
            "job_title": "Chuyên viên Tư vấn ĐTM",
            "work_phone": "028-3844-5696",
            "mobile_phone": "0949234567",
            "work_email": "tuvan.dtm@moitruongatld.vn"
        },
        {
            "name": "Đinh Văn Toàn",
            "department": "Phòng Tư vấn - Thiết kế",
            "job_title": "Kỹ sư Thiết kế XLMT",
            "work_phone": "028-3844-5697",
            "mobile_phone": "0949345678",
            "work_email": "thietke@moitruongatld.vn"
        },
        {
            "name": "Cao Thị Phương",
            "department": "Phòng Tư vấn - Thiết kế",
            "job_title": "Chuyên viên Cấp phép MT",
            "work_phone": "028-3844-5698",
            "mobile_phone": "0949456789",
            "work_email": "capphep@moitruongatld.vn"
        },
        
        # Phòng Hành chính - Nhân sự (2)
        {
            "name": "Lê Thị Thanh Huyền",
            "department": "Phòng Hành chính - Nhân sự",
            "job_title": "Trưởng phòng Hành chính",
            "work_phone": "028-3844-5699",
            "mobile_phone": "0959123456",
            "work_email": "tphcns@moitruongatld.vn"
        },
        {
            "name": "Phan Văn Đạt",
            "department": "Phòng Hành chính - Nhân sự",
            "job_title": "Nhân viên Hành chính",
            "work_phone": "028-3844-5700",
            "mobile_phone": "0959234567",
            "work_email": "hanhchinh@moitruongatld.vn"
        },
        
        # Phòng Kế toán - Tài chính (2)
        {
            "name": "Trương Thị Kim Ngân",
            "department": "Phòng Kế toán - Tài chính",
            "job_title": "Kế toán trưởng",
            "work_phone": "028-3844-5701",
            "mobile_phone": "0969123456",
            "work_email": "ketoan@moitruongatld.vn"
        },
        {
            "name": "Nguyễn Văn Tài",
            "department": "Phòng Kế toán - Tài chính",
            "job_title": "Nhân viên Kế toán",
            "work_phone": "028-3844-5702",
            "mobile_phone": "0969234567",
            "work_email": "nvketoan@moitruongatld.vn"
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
    print("🏢 TẠO CÔNG TY CỔ PHẦN MÔI TRƯỜNG VÀ AN TOÀN LAO ĐỘNG MIỀN NAM")
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
        print("  - Giám đốc: giamdoc@moitruongatld.vn / admin123")
        print("  - PGĐ Kỹ thuật: pgd.kythuat@moitruongatld.vn / admin123")
        print("  - PGĐ Kinh doanh: pgd.kinhdoanh@moitruongatld.vn / admin123")
        print("  - TP Kinh doanh: tpkd@moitruongatld.vn / admin123")
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
