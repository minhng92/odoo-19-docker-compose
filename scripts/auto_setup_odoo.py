#!/usr/bin/env python3
"""
Automatic Odoo Setup Script
- Creates database automatically
- Waits for Odoo to be ready
- Creates 10 Vietnamese companies
"""

import xmlrpc.client
import time
import sys
import random
import string

# Configuration
ODOO_URL = "http://localhost:10019"
DB_NAME = "odoo19"
ADMIN_EMAIL = "admin"
ADMIN_PASSWORD = "admin"
MASTER_PASSWORD = "minhng.info"
COUNTRY = "Vietnam"
LANGUAGE = "vi_VN"

# Vietnamese Environmental Companies - Southern Provinces
COMPANIES_DATA = [
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


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def wait_for_odoo(max_attempts=30):
    """Wait for Odoo to be ready"""
    print("\n⏳ Waiting for Odoo to start...")
    
    for attempt in range(1, max_attempts + 1):
        try:
            common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
            version = common.version()
            print(f"✅ Odoo is ready! Version: {version['server_version']}")
            return True
        except Exception as e:
            print(f"   Attempt {attempt}/{max_attempts}: Waiting... ({str(e)[:50]})")
            time.sleep(5)
    
    print("❌ Odoo did not start in time!")
    return False


def check_database_exists():
    """Check if database already exists"""
    try:
        db_socket = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/db')
        databases = db_socket.list()
        return DB_NAME in databases
    except Exception as e:
        print(f"⚠️  Could not check databases: {e}")
        return False


def create_database():
    """Create new Odoo database"""
    print("\n📦 Creating database...")
    
    if check_database_exists():
        print(f"⚠️  Database '{DB_NAME}' already exists!")
        response = input("   Do you want to drop and recreate it? (yes/no): ").lower()
        
        if response == 'yes':
            print("🗑️  Dropping existing database...")
            try:
                db_socket = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/db')
                db_socket.drop(MASTER_PASSWORD, DB_NAME)
                print("✅ Database dropped successfully!")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Failed to drop database: {e}")
                return False
        else:
            print("ℹ️  Using existing database...")
            return True
    
    try:
        print(f"   Database name: {DB_NAME}")
        print(f"   Admin email: {ADMIN_EMAIL}")
        print(f"   Language: {LANGUAGE}")
        print(f"   Country: {COUNTRY}")
        
        db_socket = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/db')
        
        # Create database (this may take a while)
        print("   Creating database (this may take 2-3 minutes)...")
        db_socket.create_database(
            MASTER_PASSWORD,
            DB_NAME,
            True,  # demo data
            LANGUAGE,
            ADMIN_PASSWORD,
            ADMIN_EMAIL,
            COUNTRY
        )
        
        print("✅ Database created successfully!")
        print("⏳ Waiting for database initialization to complete...")
        
        # Wait longer for modules to install
        for i in range(6):
            print(f"   Please wait... {(i+1)*10} seconds")
            time.sleep(10)
        
        return True
    
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False


def connect_odoo():
    """Connect to Odoo"""
    try:
        common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        uid = common.authenticate(DB_NAME, ADMIN_EMAIL, ADMIN_PASSWORD, {})
        
        if not uid:
            print("❌ Authentication failed!")
            return None, None
        
        print(f"✅ Connected to Odoo! User ID: {uid}")
        return uid, xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None, None


def get_country_id(models, uid):
    """Get Vietnam country ID"""
    try:
        country_id = models.execute_kw(
            DB_NAME, uid, ADMIN_PASSWORD,
            'res.country', 'search',
            [[['name', '=', 'Vietnam']]]
        )
        return country_id[0] if country_id else False
    except:
        return False


def create_companies(uid, models):
    """Create companies in Odoo"""
    print("\n🏢 Creating 10 Vietnamese companies...")
    
    vietnam_id = get_country_id(models, uid)
    if not vietnam_id:
        print("⚠️  Vietnam country not found, creating without country")
    
    created_companies = []
    
    for idx, company_data in enumerate(COMPANIES_DATA, 1):
        try:
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
            
            company_id = models.execute_kw(
                DB_NAME, uid, ADMIN_PASSWORD,
                'res.company', 'create',
                [odoo_data]
            )
            
            created_companies.append({
                'id': company_id,
                'name': company_data['name']
            })
            
            print(f"  ✅ [{idx}/10] {company_data['name']}")
        
        except Exception as e:
            print(f"  ❌ [{idx}/10] Failed: {company_data['name']} - {str(e)[:50]}")
    
    return created_companies


def main():
    print_header("🚀 Odoo 19 Automatic Setup")
    print(f"\n📋 Configuration:")
    print(f"   • URL: {ODOO_URL}")
    print(f"   • Database: {DB_NAME}")
    print(f"   • Admin Email: {ADMIN_EMAIL}")
    print(f"   • Admin Password: {ADMIN_PASSWORD}")
    print(f"   • Master Password: {MASTER_PASSWORD}")
    
    # Step 1: Wait for Odoo
    print_header("Step 1: Checking Odoo Status")
    if not wait_for_odoo():
        sys.exit(1)
    
    # Step 2: Create database
    print_header("Step 2: Database Setup")
    if not create_database():
        sys.exit(1)
    
    # Step 3: Connect to Odoo
    print_header("Step 3: Connecting to Odoo")
    uid, models = connect_odoo()
    if not uid:
        sys.exit(1)
    
    # Step 4: Create companies
    print_header("Step 4: Creating Companies")
    companies = create_companies(uid, models)
    
    # Summary
    print_header("✨ Setup Completed Successfully!")
    print(f"\n📊 Summary:")
    print(f"   • Database: {DB_NAME}")
    print(f"   • Companies created: {len(companies)}/10")
    print(f"\n🌐 Access Information:")
    print(f"   • URL: {ODOO_URL}")
    print(f"   • Database: {DB_NAME}")
    print(f"   • Email: {ADMIN_EMAIL}")
    print(f"   • Password: {ADMIN_PASSWORD}")
    
    print(f"\n🏢 Created Companies:")
    for company in companies:
        print(f"   • {company['name']} (ID: {company['id']})")
    
    print(f"\n💾 Backup Information:")
    print(f"   • Automatic backup: 4:00 AM daily")
    print(f"   • Retention: 7 days")
    print(f"   • Location: /home/sgc/odoo-19-docker-compose/backups/")
    
    print("\n" + "=" * 70)
    print("✅ All done! You can now use Odoo.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
