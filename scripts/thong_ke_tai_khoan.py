#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script thống kê toàn bộ công ty, nhân viên và tài khoản đăng nhập
"""

import xmlrpc.client
from collections import defaultdict

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
    print("\n" + "="*100)
    print("📊 THỐNG KÊ TOÀN BỘ CÔNG TY VÀ TÀI KHOẢN ĐĂNG NHẬP")
    print("="*100)
    
    try:
        uid, models = connect_odoo()
        print("✅ Kết nối Odoo thành công!\n")
        
        # Lấy tất cả công ty (trừ My Company nếu muốn)
        all_companies = models.execute_kw(
            DB, uid, PASSWORD,
            'res.company', 'search_read',
            [[]],
            {'fields': ['name', 'street', 'city', 'phone', 'email', 'website'], 'order': 'id'}
        )
        
        print(f"🏢 Tổng số công ty: {len(all_companies)}\n")
        
        total_employees = 0
        total_users = 0
        all_accounts = []
        
        for idx, company in enumerate(all_companies, 1):
            company_id = company['id']
            company_name = company['name']
            
            # Bỏ qua My Company nếu muốn tập trung vào các công ty tạo mới
            if company_name == "My Company":
                continue
            
            print("="*100)
            print(f"{idx}. 🏢 {company_name}")
            print("="*100)
            
            if company.get('street'):
                print(f"📍 {company.get('street', '')}, {company.get('city', '')}")
            if company.get('phone'):
                print(f"☎️  {company.get('phone', '')}")
            if company.get('email'):
                print(f"📧 {company.get('email', '')}")
            if company.get('website'):
                print(f"🌐 {company.get('website', '')}")
            
            # Lấy phòng ban của công ty
            departments = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.department', 'search_read',
                [[['company_id', '=', company_id]]],
                {'fields': ['name', 'total_employee'], 'order': 'name'}
            )
            
            # Lấy nhân viên của công ty
            employees = models.execute_kw(
                DB, uid, PASSWORD,
                'hr.employee', 'search_read',
                [[['company_id', '=', company_id]]],
                {'fields': ['name', 'department_id', 'job_title', 'work_email', 'mobile_phone'], 'order': 'department_id, name'}
            )
            
            company_employee_count = len(employees)
            total_employees += company_employee_count
            
            print(f"\n📂 Phòng ban: {len([d for d in departments if d['total_employee'] > 0])} phòng")
            print(f"👥 Nhân viên: {company_employee_count} người\n")
            
            # Nhóm nhân viên theo phòng ban
            dept_employees = defaultdict(list)
            for emp in employees:
                dept_name = emp['department_id'][1] if emp['department_id'] else "Chưa có phòng ban"
                dept_employees[dept_name].append(emp)
            
            print("─" * 100)
            print(f"{'Phòng ban':<40} {'Họ tên':<30} {'Chức vụ':<30}")
            print("─" * 100)
            
            for dept_name in sorted(dept_employees.keys()):
                emps = dept_employees[dept_name]
                for i, emp in enumerate(emps):
                    dept_display = dept_name if i == 0 else ""
                    print(f"{dept_display:<40} {emp['name']:<30} {emp.get('job_title', 'N/A'):<30}")
            
            print("─" * 100)
            
            # Lấy tài khoản user của công ty
            print(f"\n🔐 TÀI KHOẢN ĐĂNG NHẬP ({company_employee_count} tài khoản):")
            print("─" * 100)
            print(f"{'Email đăng nhập':<50} {'Tên':<30} {'Mật khẩu':<15}")
            print("─" * 100)
            
            for emp in employees:
                if emp.get('work_email'):
                    email = emp['work_email']
                    name = emp['name']
                    password = "admin123"  # Password mặc định đã set
                    
                    print(f"{email:<50} {name:<30} {password:<15}")
                    all_accounts.append({
                        'company': company_name,
                        'email': email,
                        'name': name,
                        'password': password
                    })
                    total_users += 1
            
            print("─" * 100)
            print()
        
        # Tổng kết cuối cùng
        print("\n" + "="*100)
        print("📈 TỔNG KẾT TOÀN HỆ THỐNG")
        print("="*100)
        print(f"🏢 Tổng số công ty: {len(all_companies)} công ty")
        print(f"👥 Tổng số nhân viên: {total_employees} người")
        print(f"🔐 Tổng số tài khoản: {total_users} tài khoản")
        print("="*100)
        
        # Xuất file CSV cho dễ dùng
        print("\n📄 Xuất danh sách tài khoản ra file...")
        
        csv_content = "STT,Công ty,Email,Tên nhân viên,Mật khẩu,URL\n"
        for idx, acc in enumerate(all_accounts, 1):
            csv_content += f"{idx},\"{acc['company']}\",{acc['email']},{acc['name']},{acc['password']},http://localhost:10019\n"
        
        with open('DANH_SACH_TAI_KHOAN.csv', 'w', encoding='utf-8-sig') as f:
            f.write(csv_content)
        
        print("✅ Đã xuất file: DANH_SACH_TAI_KHOAN.csv")
        
        # Xuất file text đơn giản hơn
        txt_content = "="*100 + "\n"
        txt_content += "DANH SÁCH TÀI KHOẢN ĐĂNG NHẬP TOÀN BỘ HỆ THỐNG ODOO\n"
        txt_content += "="*100 + "\n\n"
        txt_content += f"URL: http://localhost:10019\n"
        txt_content += f"Database: odoo19\n"
        txt_content += f"Mật khẩu chung: admin123\n\n"
        
        current_company = ""
        for acc in all_accounts:
            if acc['company'] != current_company:
                current_company = acc['company']
                txt_content += f"\n{'='*100}\n"
                txt_content += f"🏢 {current_company}\n"
                txt_content += f"{'='*100}\n\n"
            
            txt_content += f"  📧 {acc['email']:<50} | 👤 {acc['name']}\n"
        
        txt_content += f"\n{'='*100}\n"
        txt_content += f"Tổng số: {total_users} tài khoản\n"
        txt_content += f"{'='*100}\n"
        
        with open('DANH_SACH_TAI_KHOAN.txt', 'w', encoding='utf-8') as f:
            f.write(txt_content)
        
        print("✅ Đã xuất file: DANH_SACH_TAI_KHOAN.txt")
        
        print("\n" + "="*100)
        print("✅ HOÀN TẤT! Bạn có thể sử dụng các file trên để quản lý tài khoản.")
        print("="*100 + "\n")
        
        # Thống kê theo từng loại công ty
        print("\n" + "="*100)
        print("📊 PHÂN LOẠI CÔNG TY THEO LĨNH VỰC")
        print("="*100 + "\n")
        
        company_types = {
            "Quan trắc môi trường": [],
            "Xử lý nước thải": [],
            "An toàn lao động": [],
            "Tư vấn môi trường": [],
            "Phân tích môi trường": [],
            "Khác": []
        }
        
        for company in all_companies:
            name = company['name']
            if "My Company" in name:
                continue
            
            if "Quan trắc" in name or "Quan Trắc" in name:
                company_types["Quan trắc môi trường"].append(name)
            elif "Xử lý" in name or "Xử Lý" in name or "XLNT" in name:
                company_types["Xử lý nước thải"].append(name)
            elif "An toàn" in name or "An Toàn" in name or "ATVS" in name:
                company_types["An toàn lao động"].append(name)
            elif "Tư vấn" in name or "Tư Vấn" in name or "ĐTM" in name:
                company_types["Tư vấn môi trường"].append(name)
            elif "Phân tích" in name or "Phân Tích" in name:
                company_types["Phân tích môi trường"].append(name)
            else:
                company_types["Khác"].append(name)
        
        for category, companies in company_types.items():
            if companies:
                print(f"🏷️  {category} ({len(companies)} công ty):")
                for comp in companies:
                    print(f"   • {comp}")
                print()
        
        print("="*100 + "\n")
        
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
