#!/usr/bin/env python3
"""
Quick script to create 10 Environmental companies in existing Odoo database
Usage: python3 quick_create_env_companies.py
"""

import xmlrpc.client
import sys

# Configuration - You can edit these values
ODOO_URL = "http://localhost:10019"
DB_NAME = input("Enter database name (e.g., odoo19_production): ").strip()
ADMIN_EMAIL = input("Enter admin email: ").strip()
ADMIN_PASSWORD = input("Enter admin password: ").strip()

# 10 Environmental Companies in Southern Vietnam
COMPANIES = [
    {
        'name': 'Công ty TNHH Quan Trắc Môi Trường Xanh',
        'street': '123 Đường Nguyễn Văn Linh',
        'street2': 'Phường Tân Thuận Đông, Quận 7',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '+84 28 3789 5566',
        'email': 'contact@quantracxanh.vn',
        'website': 'https://quantracxanh.vn',
        'vat': '0312456789',
    },
    {
        'name': 'Công ty Cổ phần Môi Trường và An Toàn Lao Động Miền Nam',
        'street': '456 Đại lộ Hùng Vương',
        'street2': 'Phường 1, Thành phố Mỹ Tho',
        'city': 'Tiền Giang',
        'zip': '860000',
        'phone': '+84 273 3876 222',
        'email': 'info@mtldmiennam.vn',
        'website': 'https://mtldmiennam.com.vn',
        'vat': '1700234567',
    },
    {
        'name': 'Công ty TNHH Xử Lý Nước Thải Công Nghiệp Đồng Nai',
        'street': '789 Đường Phạm Văn Thuận',
        'street2': 'Phường Tân Mai, Thành phố Biên Hòa',
        'city': 'Đồng Nai',
        'zip': '810000',
        'phone': '+84 251 3821 456',
        'email': 'xulynuoc@dongnaiwater.vn',
        'website': 'https://dongnaiwater.vn',
        'vat': '3600345678',
    },
    {
        'name': 'Trung Tâm Tư Vấn Môi Trường và Năng Lượng Bền Vững',
        'street': '234 Lê Duẩn',
        'street2': 'Phường Bình Hòa, Thành phố Thuận An',
        'city': 'Bình Dương',
        'zip': '820000',
        'phone': '+84 274 3555 789',
        'email': 'tuvan@moitruongbenvung.vn',
        'website': 'https://moitruongbenvung.vn',
        'vat': '3700456789',
    },
    {
        'name': 'Công ty TNHH Kiểm Kê Khí Nhà Kính và Tín Chỉ Carbon',
        'street': '567 Đường 3 Tháng 2',
        'street2': 'Phường Xuân Khánh, Quận Ninh Kiều',
        'city': 'Cần Thơ',
        'zip': '900000',
        'phone': '+84 292 3756 888',
        'email': 'carbon@ghginventory.vn',
        'website': 'https://ghginventory.vn',
        'vat': '1800567890',
    },
    {
        'name': 'Công ty Cổ phần Phân Tích Môi Trường Miền Tây',
        'street': '890 Nguyễn Trãi',
        'street2': 'Phường 5, Thành phố Sóc Trăng',
        'city': 'Sóc Trăng',
        'zip': '950000',
        'phone': '+84 299 3621 333',
        'email': 'lab@envilab-mt.vn',
        'website': 'https://envilab-mt.vn',
        'vat': '3400678901',
    },
    {
        'name': 'Công ty TNHH Quan Trắc Môi Trường Lao Động An Toàn',
        'street': '321 Trần Hưng Đạo',
        'street2': 'Phường 2, Thành phố Vũng Tàu',
        'city': 'Bà Rịa - Vũng Tàu',
        'zip': '790000',
        'phone': '+84 254 3856 111',
        'email': 'quantrac@ohsmonitoring.vn',
        'website': 'https://ohsmonitoring.vn',
        'vat': '3500789012',
    },
    {
        'name': 'Công ty TNHH Giải Pháp Xử Lý Nước Thải Đô Thị',
        'street': '654 Quốc lộ 1A',
        'street2': 'Phường Phú Thọ, Thành phố Thủ Dầu Một',
        'city': 'Bình Dương',
        'zip': '820000',
        'phone': '+84 274 3888 456',
        'email': 'xulynt@urbancleaning.vn',
        'website': 'https://urbancleaning.vn',
        'vat': '3700890123',
    },
    {
        'name': 'Công ty Cổ phần Tư Vấn và Đánh Giá Tác Động Môi Trường',
        'street': '147 Lý Thường Kiệt',
        'street2': 'Phường 7, Thành phố Vĩnh Long',
        'city': 'Vĩnh Long',
        'zip': '890000',
        'phone': '+84 270 3824 567',
        'email': 'eia@enviconsulting.vn',
        'website': 'https://enviconsulting.vn',
        'vat': '3300901234',
    },
    {
        'name': 'Trung Tâm Nghiên Cứu và Ứng Dụng Công Nghệ Môi Trường',
        'street': '258 Võ Văn Kiệt',
        'street2': 'Phường 3, Thành phố Long Xuyên',
        'city': 'An Giang',
        'zip': '880000',
        'phone': '+84 296 3567 890',
        'email': 'research@envitech.vn',
        'website': 'https://envitech.vn',
        'vat': '3200012345',
    },
]

print("=" * 80)
print("🌿 TẠO 10 CÔNG TY MÔI TRƯỜNG - MIỀN NAM VIỆT NAM")
print("=" * 80)

# Connect to Odoo
try:
    print("\n🔌 Connecting to Odoo...")
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(DB_NAME, ADMIN_EMAIL, ADMIN_PASSWORD, {})
    
    if not uid:
        print("❌ Authentication failed! Please check your credentials.")
        sys.exit(1)
    
    print(f"✅ Connected successfully! User ID: {uid}")
    
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    
    # Get Vietnam country ID
    print("\n🌍 Finding Vietnam in country list...")
    vietnam_id = models.execute_kw(
        DB_NAME, uid, ADMIN_PASSWORD,
        'res.country', 'search',
        [[['name', '=', 'Vietnam']]]
    )
    vietnam_id = vietnam_id[0] if vietnam_id else False
    
    if vietnam_id:
        print(f"✅ Found Vietnam (ID: {vietnam_id})")
    else:
        print("⚠️  Vietnam not found, will create companies without country")
    
    # Create companies
    print("\n🏢 Creating 10 Environmental companies...")
    print("-" * 80)
    
    created = []
    failed = []
    
    for idx, company in enumerate(COMPANIES, 1):
        try:
            company_data = {
                'name': company['name'],
                'street': company['street'],
                'street2': company['street2'],
                'city': company['city'],
                'zip': company['zip'],
                'phone': company['phone'],
                'email': company['email'],
                'website': company['website'],
                'vat': company['vat'],
            }
            
            if vietnam_id:
                company_data['country_id'] = vietnam_id
            
            company_id = models.execute_kw(
                DB_NAME, uid, ADMIN_PASSWORD,
                'res.company', 'create',
                [company_data]
            )
            
            created.append({'id': company_id, 'name': company['name']})
            print(f"✅ [{idx:2d}/10] {company['name']}")
            print(f"         📍 {company['city']}")
        
        except Exception as e:
            failed.append({'name': company['name'], 'error': str(e)})
            print(f"❌ [{idx:2d}/10] {company['name']}")
            print(f"         Error: {str(e)[:60]}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully created: {len(created)} companies")
    print(f"❌ Failed: {len(failed)} companies")
    
    if created:
        print("\n🏢 Created Companies:")
        for comp in created:
            print(f"   • {comp['name']} (ID: {comp['id']})")
    
    if failed:
        print("\n❌ Failed Companies:")
        for comp in failed:
            print(f"   • {comp['name']}")
            print(f"     Error: {comp['error'][:60]}")
    
    print("\n" + "=" * 80)
    print("✅ DONE! Access Odoo at: " + ODOO_URL)
    print("=" * 80)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    sys.exit(1)
