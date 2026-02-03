#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script thiết lập phân quyền theo cấp bậc trong Odoo 19
Dựa trên cấu trúc tổ chức và nghiệp vụ thực tế

CẤU TRÚC PHÂN QUYỀN:
1. Cấp Lãnh đạo (BGD) - Administrator
2. Khối Kinh doanh: TPKD → Trưởng đội → NVKD
3. Khối Vận hành: TP Kỹ thuật, TP Thí nghiệm, TP Tư vấn
4. Khối Mua hàng: TP Mua hàng → NV Mua hàng
5. Khối Tài chính: Kế toán trưởng → NV Kế toán
6. Khối Hỗ trợ: HR, Pháp lý
"""

import xmlrpc.client

# Cấu hình
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

def get_or_create_group(uid, models, name, category_name="Phân quyền tùy chỉnh"):
    """Tạo hoặc lấy group quyền"""
    # Tìm hoặc tạo group (không cần category)
    group_ids = models.execute_kw(
        DB, uid, PASSWORD,
        'res.groups', 'search',
        [[['name', '=', name]]]
    )
    
    if group_ids:
        print(f"  ✅ Group đã tồn tại: {name}")
        return group_ids[0]
    
    group_id = models.execute_kw(
        DB, uid, PASSWORD,
        'res.groups', 'create',
        [{'name': name}]
    )
    
    print(f"  ✅ Đã tạo group: {name} (ID: {group_id})")
    return group_id

def get_base_groups(uid, models):
    """Lấy các group cơ bản của Odoo"""
    print("\n🔍 Đang lấy các group cơ bản của Odoo...")
    
    groups = {}
    
    # Các group quan trọng - tìm bằng tên
    group_names = {
        'sales_user': 'User: Own Documents Only',
        'sales_manager': 'Administrator',
        'crm_user': 'User',
        'project_user': 'User',
        'project_manager': 'Administrator',
        'purchase_user': 'User',
        'purchase_manager': 'Purchase Manager',
        'stock_user': 'User',
        'stock_manager': 'Administrator',
        'account_user': 'Billing',
        'account_manager': 'Advisor',
        'hr_user': 'Officer',
        'hr_manager': 'Officer',
        'employee': 'Internal User',
        'settings': 'Settings',
    }
    
    for key, name in group_names.items():
        try:
            group_ids = models.execute_kw(
                DB, uid, PASSWORD,
                'res.groups', 'search',
                [[['name', '=', name]]],
                {'limit': 1}
            )
            if group_ids:
                groups[key] = group_ids[0]
                print(f"  ✅ {key}: {group_ids[0]}")
            else:
                print(f"  ⚠️  Không tìm thấy '{name}'")
        except Exception as e:
            print(f"  ⚠️  Lỗi tìm {key}: {str(e)}")
    
    return groups

def create_permission_structure(uid, models, base_groups):
    """Tạo cấu trúc phân quyền"""
    print("\n" + "="*80)
    print("📋 TẠO CẤU TRÚC PHÂN QUYỀN")
    print("="*80)
    
    permission_groups = {}
    
    # 1. CẤP LÃNH ĐẠO - BGD (Dùng group Administrator sẵn có)
    print("\n1️⃣  CẤP LÃNH ĐẠO - BAN GIÁM ĐỐC")
    permission_groups['bgd'] = base_groups.get('settings')
    print(f"  ✅ Sử dụng group Administrator (ID: {permission_groups['bgd']})")
    
    # 2. KHỐI KINH DOANH
    print("\n2️⃣  KHỐI KINH DOANH")
    
    # Trưởng phòng Kinh doanh
    permission_groups['tpkd'] = get_or_create_group(
        uid, models, 
        "Trưởng phòng Kinh doanh (TPKD)",
        "Khối Kinh doanh"
    )
    
    # Trưởng đội Kinh doanh
    permission_groups['truong_doi_kd'] = get_or_create_group(
        uid, models,
        "Trưởng đội Kinh doanh",
        "Khối Kinh doanh"
    )
    
    # Nhân viên Kinh doanh
    permission_groups['nvkd'] = get_or_create_group(
        uid, models,
        "Nhân viên Kinh doanh (NVKD)",
        "Khối Kinh doanh"
    )
    
    # Nhân viên Marketing
    permission_groups['marketing'] = get_or_create_group(
        uid, models,
        "Nhân viên Marketing",
        "Khối Kinh doanh"
    )
    
    # 3. KHỐI VẬN HÀNH / KỸ THUẬT
    print("\n3️⃣  KHỐI VẬN HÀNH / KỸ THUẬT")
    
    # Trưởng phòng Kỹ thuật
    permission_groups['tp_ky_thuat'] = get_or_create_group(
        uid, models,
        "Trưởng phòng Kỹ thuật",
        "Khối Vận hành"
    )
    
    # Nhân viên Kỹ thuật
    permission_groups['nv_ky_thuat'] = get_or_create_group(
        uid, models,
        "Nhân viên Kỹ thuật",
        "Khối Vận hành"
    )
    
    # Trưởng phòng Thí nghiệm
    permission_groups['tp_thi_nghiem'] = get_or_create_group(
        uid, models,
        "Trưởng phòng Thí nghiệm (PTN)",
        "Khối Vận hành"
    )
    
    # Nhân viên Thí nghiệm
    permission_groups['nv_thi_nghiem'] = get_or_create_group(
        uid, models,
        "Nhân viên Thí nghiệm",
        "Khối Vận hành"
    )
    
    # Phòng Tư vấn
    permission_groups['tu_van'] = get_or_create_group(
        uid, models,
        "Phòng Tư vấn",
        "Khối Vận hành"
    )
    
    # Quản lý Dự án (PM)
    permission_groups['pm'] = get_or_create_group(
        uid, models,
        "Quản lý Dự án (PM)",
        "Khối Vận hành"
    )
    
    # 4. KHỐI MUA HÀNG & KHO VẬN
    print("\n4️⃣  KHỐI MUA HÀNG & KHO VẬN")
    
    # Trưởng phòng Mua hàng
    permission_groups['tp_mua_hang'] = get_or_create_group(
        uid, models,
        "Trưởng phòng Mua hàng",
        "Khối Mua hàng"
    )
    
    # Nhân viên Mua hàng
    permission_groups['nv_mua_hang'] = get_or_create_group(
        uid, models,
        "Nhân viên Mua hàng",
        "Khối Mua hàng"
    )
    
    # Nhân viên Kho
    permission_groups['nv_kho'] = get_or_create_group(
        uid, models,
        "Nhân viên Kho",
        "Khối Mua hàng"
    )
    
    # 5. KHỐI TÀI CHÍNH - KẾ TOÁN
    print("\n5️⃣  KHỐI TÀI CHÍNH - KẾ TOÁN")
    
    # Kế toán trưởng
    permission_groups['ke_toan_truong'] = get_or_create_group(
        uid, models,
        "Kế toán trưởng",
        "Khối Tài chính"
    )
    
    # Nhân viên Kế toán
    permission_groups['nv_ke_toan'] = get_or_create_group(
        uid, models,
        "Nhân viên Kế toán",
        "Khối Tài chính"
    )
    
    # 6. KHỐI HỖ TRỢ
    print("\n6️⃣  KHỐI HỖ TRỢ")
    
    # Nhân viên Pháp lý
    permission_groups['phap_ly'] = get_or_create_group(
        uid, models,
        "Nhân viên Pháp lý",
        "Khối Hỗ trợ"
    )
    
    # Nhân viên Nhân sự (HR)
    permission_groups['nv_hr'] = get_or_create_group(
        uid, models,
        "Nhân viên Nhân sự",
        "Khối Hỗ trợ"
    )
    
    return permission_groups

def assign_base_permissions(uid, models, permission_groups, base_groups):
    """Gán quyền cơ bản từ Odoo vào các group tùy chỉnh"""
    print("\n" + "="*80)
    print("🔐 GÁN QUYỀN CƠ BẢN CHO CÁC NHÓM")
    print("="*80)
    
    # Mapping: custom_group -> [base_groups_to_inherit]
    permission_mappings = {
        # KHỐI KINH DOANH
        'tpkd': ['sales_manager', 'crm_user', 'project_user', 'employee'],
        'truong_doi_kd': ['sales_user', 'crm_user', 'employee'],
        'nvkd': ['sales_user', 'crm_user', 'employee'],
        'marketing': ['crm_user', 'employee'],
        
        # KHỐI VẬN HÀNH
        'tp_ky_thuat': ['project_manager', 'employee'],
        'nv_ky_thuat': ['project_user', 'employee'],
        'tp_thi_nghiem': ['project_manager', 'employee'],
        'nv_thi_nghiem': ['project_user', 'employee'],
        'tu_van': ['project_user', 'employee'],
        'pm': ['project_manager', 'employee'],
        
        # KHỐI MUA HÀNG
        'tp_mua_hang': ['purchase_manager', 'stock_manager', 'employee'],
        'nv_mua_hang': ['purchase_user', 'stock_user', 'employee'],
        'nv_kho': ['stock_user', 'employee'],
        
        # KHỐI TÀI CHÍNH
        'ke_toan_truong': ['account_manager', 'employee'],
        'nv_ke_toan': ['account_user', 'employee'],
        
        # KHỐI HỖ TRỢ
        'phap_ly': ['employee'],
        'nv_hr': ['hr_manager', 'employee'],
    }
    
    for custom_key, base_keys in permission_mappings.items():
        if custom_key not in permission_groups:
            continue
            
        custom_group_id = permission_groups[custom_key]
        implied_ids = []
        
        for base_key in base_keys:
            if base_key in base_groups:
                implied_ids.append(base_groups[base_key])
        
        if implied_ids:
            try:
                models.execute_kw(
                    DB, uid, PASSWORD,
                    'res.groups', 'write',
                    [[custom_group_id], {'implied_ids': [(6, 0, implied_ids)]}]
                )
                print(f"  ✅ {custom_key}: Đã gán {len(implied_ids)} quyền cơ bản")
            except Exception as e:
                print(f"  ❌ {custom_key}: Lỗi - {str(e)}")

def assign_users_to_groups(uid, models, permission_groups):
    """Phân quyền cho các nhân viên dựa trên phòng ban"""
    print("\n" + "="*80)
    print("👥 PHÂN QUYỀN CHO NHÂN VIÊN")
    print("="*80)
    
    # Lấy danh sách tất cả nhân viên
    employees = models.execute_kw(
        DB, uid, PASSWORD,
        'hr.employee', 'search_read',
        [[]],
        {'fields': ['name', 'department_id', 'job_title', 'work_email']}
    )
    
    print(f"\n📊 Tìm thấy {len(employees)} nhân viên")
    
    # Mapping phòng ban -> group quyền
    dept_mappings = {
        'Phòng Quan Trắc Môi Trường (QT)': {
            'Trưởng phòng': 'tp_ky_thuat',
            'default': 'nv_ky_thuat'
        },
        'Phòng Phân Tích Hóa (PTH)': {
            'Trưởng phòng': 'tp_thi_nghiem',
            'default': 'nv_thi_nghiem'
        },
        'Phòng Phân Tích Sinh (PTS)': {
            'Trưởng phòng': 'tp_thi_nghiem',
            'default': 'nv_thi_nghiem'
        },
        'Phòng Kinh Doanh': {
            'Trưởng phòng': 'tpkd',
            'Trưởng đội': 'truong_doi_kd',
            'default': 'nvkd'
        },
        'Phòng Kỹ Thuật': {
            'Trưởng phòng': 'tp_ky_thuat',
            'default': 'nv_ky_thuat'
        },
        'Phòng Hành Chính Nhân Sự': {
            'Trưởng phòng': 'nv_hr',
            'default': 'nv_hr'
        },
        'Phòng Kế Toán Tài Chính': {
            'Trưởng phòng': 'ke_toan_truong',
            'default': 'nv_ke_toan'
        },
        'Phòng IT': {
            'Trưởng phòng': 'bgd',  # IT thường có quyền cao
            'default': 'employee'
        },
        'Phòng QA/QC': {
            'Trưởng phòng': 'pm',
            'default': 'project_user'
        },
    }
    
    assigned_count = 0
    
    for emp in employees:
        if not emp.get('work_email'):
            print(f"  ⚠️  {emp['name']}: Không có email, bỏ qua")
            continue
        
        # Tìm hoặc tạo user
        user_ids = models.execute_kw(
            DB, uid, PASSWORD,
            'res.users', 'search',
            [[['login', '=', emp['work_email']]]]
        )
        
        if not user_ids:
            # Tạo user mới
            try:
                user_id = models.execute_kw(
                    DB, uid, PASSWORD,
                    'res.users', 'create',
                    [{
                        'name': emp['name'],
                        'login': emp['work_email'],
                        'password': 'admin123',  # Password mặc định
                        'employee_id': emp['id'],
                    }]
                )
                print(f"  ✅ Tạo user: {emp['name']} ({emp['work_email']})")
            except Exception as e:
                print(f"  ❌ Không thể tạo user cho {emp['name']}: {str(e)}")
                continue
        else:
            user_id = user_ids[0]
        
        # Xác định group phù hợp
        dept_name = emp['department_id'][1] if emp['department_id'] else None
        job_title = emp['job_title'] or ''
        
        group_key = None
        
        if dept_name and dept_name in dept_mappings:
            dept_map = dept_mappings[dept_name]
            
            # Kiểm tra chức vụ
            if 'Trưởng phòng' in job_title:
                group_key = dept_map.get('Trưởng phòng')
            elif 'Trưởng đội' in job_title:
                group_key = dept_map.get('Trưởng đội')
            else:
                group_key = dept_map.get('default')
        
        if group_key and group_key in permission_groups:
            group_id = permission_groups[group_key]
            
            try:
                # Thêm user vào group
                models.execute_kw(
                    DB, uid, PASSWORD,
                    'res.groups', 'write',
                    [[group_id], {'users': [(4, user_id)]}]
                )
                assigned_count += 1
                print(f"  ✅ {emp['name']} → {group_key}")
            except Exception as e:
                print(f"  ❌ Lỗi gán quyền cho {emp['name']}: {str(e)}")

    print(f"\n✅ Đã phân quyền cho {assigned_count}/{len(employees)} nhân viên")

def create_record_rules(uid, models, permission_groups):
    """Tạo các quy tắc truy cập dữ liệu (Record Rules)"""
    print("\n" + "="*80)
    print("📜 TẠO QUY TẮC TRUY CẬP DỮ LIỆU (RECORD RULES)")
    print("="*80)
    
    # Quy tắc cho Nhân viên Kinh doanh: Chỉ xem được cơ hội/báo giá của mình
    try:
        # Rule cho CRM Lead
        models.execute_kw(
            DB, uid, PASSWORD,
            'ir.rule', 'create',
            [{
                'name': 'NVKD: Chỉ xem Lead/Opportunity của mình',
                'model_id': models.execute_kw(
                    DB, uid, PASSWORD,
                    'ir.model', 'search',
                    [[['model', '=', 'crm.lead']]]
                )[0],
                'domain_force': "[('user_id', '=', user.id)]",
                'groups': [(6, 0, [permission_groups['nvkd']])],
                'perm_read': True,
                'perm_write': True,
                'perm_create': True,
                'perm_unlink': False,
            }]
        )
        print("  ✅ Tạo rule: NVKD chỉ xem Lead của mình")
    except Exception as e:
        print(f"  ⚠️  Không thể tạo rule CRM: {str(e)}")
    
    # Quy tắc cho Nhân viên: Chỉ xem được task của mình
    try:
        models.execute_kw(
            DB, uid, PASSWORD,
            'ir.rule', 'create',
            [{
                'name': 'Nhân viên: Chỉ xem Task được gán cho mình',
                'model_id': models.execute_kw(
                    DB, uid, PASSWORD,
                    'ir.model', 'search',
                    [[['model', '=', 'project.task']]]
                )[0],
                'domain_force': "['|', ('user_ids', 'in', [user.id]), ('create_uid', '=', user.id)]",
                'groups': [(6, 0, [
                    permission_groups['nv_ky_thuat'],
                    permission_groups['nv_thi_nghiem'],
                ])],
                'perm_read': True,
                'perm_write': True,
                'perm_create': False,
                'perm_unlink': False,
            }]
        )
        print("  ✅ Tạo rule: Nhân viên chỉ xem Task của mình")
    except Exception as e:
        print(f"  ⚠️  Không thể tạo rule Task: {str(e)}")

def print_summary(permission_groups):
    """In tóm tắt phân quyền"""
    print("\n" + "="*80)
    print("📊 TÓM TẮT CẤU TRÚC PHÂN QUYỀN")
    print("="*80)
    
    structure = {
        "🏢 CẤP LÃNH ĐẠO": ['bgd'],
        "💼 KHỐI KINH DOANH": ['tpkd', 'truong_doi_kd', 'nvkd', 'marketing'],
        "🔧 KHỐI VẬN HÀNH": ['tp_ky_thuat', 'nv_ky_thuat', 'tp_thi_nghiem', 'nv_thi_nghiem', 'tu_van', 'pm'],
        "📦 KHỐI MUA HÀNG": ['tp_mua_hang', 'nv_mua_hang', 'nv_kho'],
        "💰 KHỐI TÀI CHÍNH": ['ke_toan_truong', 'nv_ke_toan'],
        "🤝 KHỐI HỖ TRỢ": ['phap_ly', 'nv_hr'],
    }
    
    for category, keys in structure.items():
        print(f"\n{category}")
        for key in keys:
            if key in permission_groups:
                print(f"  ✅ {key} (ID: {permission_groups[key]})")

def main():
    """Hàm main"""
    print("\n" + "="*80)
    print("🔐 THIẾT LẬP PHÂN QUYỀN CHO HỆ THỐNG ODOO 19")
    print("="*80)
    print(f"🌐 URL: {URL}")
    print(f"🗄️  Database: {DB}")
    print("="*80)
    
    try:
        # Kết nối
        print("\n🔌 Đang kết nối tới Odoo...")
        uid, models = connect_odoo()
        print(f"✅ Kết nối thành công! User ID: {uid}")
        
        # Lấy các group cơ bản
        base_groups = get_base_groups(uid, models)
        
        # Tạo cấu trúc phân quyền
        permission_groups = create_permission_structure(uid, models, base_groups)
        
        # Gán quyền cơ bản
        assign_base_permissions(uid, models, permission_groups, base_groups)
        
        # Phân quyền cho nhân viên
        assign_users_to_groups(uid, models, permission_groups)
        
        # Tạo record rules
        create_record_rules(uid, models, permission_groups)
        
        # In tóm tắt
        print_summary(permission_groups)
        
        print("\n" + "="*80)
        print("✅ HOÀN TẤT THIẾT LẬP PHÂN QUYỀN!")
        print("="*80)
        print("\n📌 Thông tin quan trọng:")
        print("   • Password mặc định cho tất cả user: admin123")
        print("   • Đăng nhập bằng email công ty (work_email)")
        print("   • Truy cập: Settings → Users & Companies → Users để xem")
        print("\n📂 Xem phân quyền:")
        print("   Settings → Users & Companies → Groups")
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
