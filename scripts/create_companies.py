#!/usr/bin/env python3
"""
Script to create 10 realistic Vietnamese companies in Odoo 19
Uses XML-RPC API to connect to Odoo
"""

import xmlrpc.client
import sys

# Odoo connection settings
ODOO_URL = "http://localhost:10019"
DATABASE = input("Enter database name (e.g., odoo19_db): ")
USERNAME = input("Enter admin email: ")
PASSWORD = input("Enter admin password: ")

# Vietnamese Environmental Companies - Southern Provinces
COMPANIES_DATA = [
    {
        'name': 'Công ty TNHH Quan Trắc Môi Trường Xanh',
        'street': '123 Đường Nguyễn Văn Linh',
        'street2': 'Phường Tân Thuận Đông, Quận 7',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'country_id': 'Vietnam',
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
        'country_id': 'Vietnam',
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
        'country_id': 'Vietnam',
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
        'country_id': 'Vietnam',
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
        'country_id': 'Vietnam',
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
        'country_id': 'Vietnam',
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
        'country_id': 'Vietnam',
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
        'country_id': 'Vietnam',
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
        'country_id': 'Vietnam',
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
        'country_id': 'Vietnam',
        'phone': '+84 296 3567 890',
        'email': 'research@envitech.vn',
        'website': 'https://envitech.vn',
        'vat': '3200012345',
    },
]


def connect_odoo():
    """Connect to Odoo using XML-RPC"""
    try:
        common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        uid = common.authenticate(DATABASE, USERNAME, PASSWORD, {})
        
        if not uid:
            print("❌ Authentication failed. Please check your credentials.")
            sys.exit(1)
        
        print(f"✅ Connected to Odoo successfully! User ID: {uid}")
        return uid, xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    
    except Exception as e:
        print(f"❌ Connection error: {e}")
        sys.exit(1)


def get_country_id(models, uid, country_name):
    """Get country ID by name"""
    try:
        country_id = models.execute_kw(
            DATABASE, uid, PASSWORD,
            'res.country', 'search',
            [[['name', '=', country_name]]]
        )
        return country_id[0] if country_id else False
    except:
        return False


def create_companies(uid, models):
    """Create companies in Odoo"""
    print("\n🏢 Creating companies...")
    
    # Get Vietnam country ID
    vietnam_id = get_country_id(models, uid, 'Vietnam')
    if not vietnam_id:
        print("⚠️  Vietnam country not found, will create without country")
    
    created_companies = []
    
    for idx, company_data in enumerate(COMPANIES_DATA, 1):
        try:
            # Prepare company data
            odoo_data = {
                'name': company_data['name'],
                'street': company_data['street'],
                'street2': company_data['street2'],
                'city': company_data['city'],
                'zip': company_data['zip'],
                'phone': company_data['phone'],
                'email': company_data['email'],
                'website': company_data['website'],
                'vat': company_data['vat'],
            }
            
            if vietnam_id:
                odoo_data['country_id'] = vietnam_id
            
            # Create company
            company_id = models.execute_kw(
                DATABASE, uid, PASSWORD,
                'res.company', 'create',
                [odoo_data]
            )
            
            created_companies.append({
                'id': company_id,
                'name': company_data['name']
            })
            
            print(f"  ✅ [{idx}/10] Created: {company_data['name']}")
        
        except Exception as e:
            print(f"  ❌ [{idx}/10] Failed to create {company_data['name']}: {e}")
    
    return created_companies


def main():
    print("=" * 70)
    print("🚀 Odoo 19 - Create 10 Vietnamese Companies")
    print("=" * 70)
    
    # Connect to Odoo
    uid, models = connect_odoo()
    
    # Create companies
    companies = create_companies(uid, models)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"✨ Summary: Successfully created {len(companies)} companies!")
    print("=" * 70)
    
    for company in companies:
        print(f"  🏢 {company['name']} (ID: {company['id']})")
    
    print("\n✅ Done! You can now view these companies in Odoo.")
    print(f"   Access Odoo at: {ODOO_URL}")


if __name__ == "__main__":
    main()
