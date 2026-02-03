#!/usr/bin/env python3
"""
Create users for 10 Environmental companies
Each company gets an admin user with simple credentials
"""

import xmlrpc.client
import sys

# Configuration
ODOO_URL = "http://localhost:10019"
DB_NAME = input("Enter database name: ").strip()
ADMIN_EMAIL = input("Enter super admin email: ").strip()
ADMIN_PASSWORD = input("Enter super admin password: ").strip()

# Users data for 10 companies
USERS_DATA = [
    {
        'company_name': 'Công ty TNHH Quan Trắc Môi Trường Xanh',
        'user_name': 'Admin Quan Trắc Xanh',
        'login': 'quantrac.xanh',
        'email': 'admin@quantracxanh.vn',
        'password': 'xanh2025',
    },
    {
        'company_name': 'Công ty Cổ phần Môi Trường và An Toàn Lao Động Miền Nam',
        'user_name': 'Admin MTLD Miền Nam',
        'login': 'mtld.miennam',
        'email': 'admin@mtldmiennam.vn',
        'password': 'laodong2025',
    },
    {
        'company_name': 'Công ty TNHH Xử Lý Nước Thải Công Nghiệp Đồng Nai',
        'user_name': 'Admin Nước Thải Đồng Nai',
        'login': 'nuocthai.dongnai',
        'email': 'admin@dongnaiwater.vn',
        'password': 'nuoc2025',
    },
    {
        'company_name': 'Trung Tâm Tư Vấn Môi Trường và Năng Lượng Bền Vững',
        'user_name': 'Admin Tư Vấn Bền Vững',
        'login': 'tuvan.benvung',
        'email': 'admin@moitruongbenvung.vn',
        'password': 'benvung2025',
    },
    {
        'company_name': 'Công ty TNHH Kiểm Kê Khí Nhà Kính và Tín Chỉ Carbon',
        'user_name': 'Admin Khí Carbon',
        'login': 'khi.carbon',
        'email': 'admin@ghginventory.vn',
        'password': 'carbon2025',
    },
    {
        'company_name': 'Công ty Cổ phần Phân Tích Môi Trường Miền Tây',
        'user_name': 'Admin Phân Tích Miền Tây',
        'login': 'phantich.mientay',
        'email': 'admin@envilab-mt.vn',
        'password': 'lab2025',
    },
    {
        'company_name': 'Công ty TNHH Quan Trắc Môi Trường Lao Động An Toàn',
        'user_name': 'Admin Quan Trắc Vũng Tàu',
        'login': 'quantrac.vungtau',
        'email': 'admin@ohsmonitoring.vn',
        'password': 'ohs2025',
    },
    {
        'company_name': 'Công ty TNHH Giải Pháp Xử Lý Nước Thải Đô Thị',
        'user_name': 'Admin Giải Pháp Nước',
        'login': 'giaiphap.nuoc',
        'email': 'admin@urbancleaning.vn',
        'password': 'urban2025',
    },
    {
        'company_name': 'Công ty Cổ phần Tư Vấn và Đánh Giá Tác Động Môi Trường',
        'user_name': 'Admin Đánh Giá EIA',
        'login': 'danhgia.eia',
        'email': 'admin@enviconsulting.vn',
        'password': 'eia2025',
    },
    {
        'company_name': 'Trung Tâm Nghiên Cứu và Ứng Dụng Công Nghệ Môi Trường',
        'user_name': 'Admin Nghiên Cứu MT',
        'login': 'nghiencuu.mt',
        'email': 'admin@envitech.vn',
        'password': 'tech2025',
    },
]

print("=" * 80)
print("👥 TẠO USERS CHO 10 CÔNG TY MÔI TRƯỜNG")
print("=" * 80)

try:
    # Connect to Odoo
    print("\n🔌 Connecting to Odoo...")
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(DB_NAME, ADMIN_EMAIL, ADMIN_PASSWORD, {})
    
    if not uid:
        print("❌ Authentication failed!")
        sys.exit(1)
    
    print(f"✅ Connected! User ID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    
    # Get all companies
    print("\n🏢 Fetching companies...")
    companies = models.execute_kw(
        DB_NAME, uid, ADMIN_PASSWORD,
        'res.company', 'search_read',
        [[]],
        {'fields': ['id', 'name']}
    )
    
    company_dict = {comp['name']: comp['id'] for comp in companies}
    print(f"✅ Found {len(companies)} companies")
    
    # Get internal user group
    print("\n👤 Getting user groups...")
    internal_user_group = models.execute_kw(
        DB_NAME, uid, ADMIN_PASSWORD,
        'res.groups', 'search',
        [[['name', '=', 'Internal User']]]
    )
    
    # Create users
    print("\n👥 Creating users...")
    print("-" * 80)
    
    created = []
    failed = []
    
    for idx, user_data in enumerate(USERS_DATA, 1):
        try:
            company_name = user_data['company_name']
            
            # Find company ID
            company_id = company_dict.get(company_name)
            
            if not company_id:
                print(f"⚠️  [{idx:2d}/10] Company not found: {company_name}")
                failed.append({'user': user_data['user_name'], 'reason': 'Company not found'})
                continue
            
            # Check if user already exists
            existing_user = models.execute_kw(
                DB_NAME, uid, ADMIN_PASSWORD,
                'res.users', 'search',
                [[['login', '=', user_data['login']]]]
            )
            
            if existing_user:
                print(f"⚠️  [{idx:2d}/10] User already exists: {user_data['login']}")
                continue
            
            # Create user
            user_vals = {
                'name': user_data['user_name'],
                'login': user_data['login'],
                'email': user_data['email'],
                'password': user_data['password'],
                'company_id': company_id,
                'company_ids': [(6, 0, [company_id])],
                'groups_id': [(6, 0, internal_user_group)] if internal_user_group else [],
            }
            
            user_id = models.execute_kw(
                DB_NAME, uid, ADMIN_PASSWORD,
                'res.users', 'create',
                [user_vals]
            )
            
            created.append({
                'id': user_id,
                'name': user_data['user_name'],
                'login': user_data['login'],
                'company': company_name
            })
            
            print(f"✅ [{idx:2d}/10] {user_data['user_name']}")
            print(f"         Login: {user_data['login']} | Password: {user_data['password']}")
        
        except Exception as e:
            failed.append({'user': user_data['user_name'], 'reason': str(e)[:60]})
            print(f"❌ [{idx:2d}/10] {user_data['user_name']}")
            print(f"         Error: {str(e)[:60]}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully created: {len(created)} users")
    print(f"❌ Failed: {len(failed)} users")
    
    if created:
        print("\n👥 Created Users:")
        for user in created:
            print(f"   • {user['name']} ({user['login']})")
    
    if failed:
        print("\n❌ Failed Users:")
        for user in failed:
            print(f"   • {user['user']}: {user['reason']}")
    
    print("\n" + "=" * 80)
    print("📄 Login information saved in: COMPANY_LOGIN_INFO.md")
    print("=" * 80)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    sys.exit(1)
