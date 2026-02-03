#!/usr/bin/env python3
import xmlrpc.client
import csv
import os

url = "http://localhost:10019"
db = "odoo19"
username = "admin"
password = "admin"

print("=" * 70)
print("CẤU HÌNH CÔNG TY, THUẾ VÀ ĐƠN VỊ TÍNH")
print("=" * 70)
print()

# Kết nối
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("❌ Không thể đăng nhập!")
    exit(1)

print(f"✅ Đã đăng nhập: uid={uid}")
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# ============================================
# PHẦN 1: CẤU HÌNH THÔNG TIN CÔNG TY
# ============================================
print()
print("=" * 70)
print("PHẦN 1: CẤU HÌNH THÔNG TIN CÔNG TY")
print("=" * 70)
print()

try:
    # Tìm My Company
    company_ids = models.execute_kw(db, uid, password,
        'res.company', 'search', [[['name', '=', 'My Company']]])
    
    if company_ids:
        company_id = company_ids[0]
        
        # Cập nhật thông tin công ty
        company_data = {
            'name': 'My Company',
            'vat': '0123456789',  # Mã số thuế
            'phone': '+84 28 1234 5678',
            'email': 'info@mycompany.vn',
            'website': 'https://www.mycompany.vn',
            'street': '123 Đường ABC',
            'street2': 'Phường XYZ',
            'city': 'Hồ Chí Minh',
            'zip': '700000',
            'country_id': models.execute_kw(db, uid, password,
                'res.country', 'search', [[['code', '=', 'VN']]])[0],  # Vietnam
        }
        
        models.execute_kw(db, uid, password,
            'res.company', 'write', [[company_id], company_data])
        
        print("✅ Đã cập nhật thông tin công ty:")
        print(f"   Tên: {company_data['name']}")
        print(f"   MST: {company_data['vat']}")
        print(f"   Điện thoại: {company_data['phone']}")
        print(f"   Email: {company_data['email']}")
        print(f"   Website: {company_data['website']}")
        print(f"   Địa chỉ: {company_data['street']}, {company_data['city']}")
    else:
        print("⚠️  Không tìm thấy công ty")
except Exception as e:
    print(f"❌ Lỗi cấu hình công ty: {str(e)[:100]}")

# ============================================
# PHẦN 2: IMPORT THUẾ TỪ CSV
# ============================================
print()
print("=" * 70)
print("PHẦN 2: IMPORT THUẾ TỪ CSV")
print("=" * 70)
print()

tax_csv_path = '/home/sgc/odoo-19-docker-compose/data/Cấu hình thuế.csv'

if os.path.exists(tax_csv_path):
    print(f"📄 Đọc file: {tax_csv_path}")
    
    created_count = 0
    updated_count = 0
    error_count = 0
    
    with open(tax_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                tax_name = row['name']
                tax_rate = float(row['rate'])
                tax_type = row['type_tax_use']
                tax_desc = row.get('description', '')
                
                # Kiểm tra xem thuế đã tồn tại chưa
                existing_tax = models.execute_kw(db, uid, password,
                    'account.tax', 'search',
                    [[['name', '=', tax_name]]])
                
                tax_data = {
                    'name': tax_name,
                    'amount': tax_rate,
                    'amount_type': 'percent',
                    'type_tax_use': tax_type,
                    'description': tax_desc,
                    'active': True,
                }
                
                if existing_tax:
                    # Cập nhật
                    models.execute_kw(db, uid, password,
                        'account.tax', 'write', [[existing_tax[0]], tax_data])
                    print(f"   ↻ Cập nhật: {tax_name} - {tax_rate}%")
                    updated_count += 1
                else:
                    # Tạo mới
                    models.execute_kw(db, uid, password,
                        'account.tax', 'create', [tax_data])
                    print(f"   ✓ Tạo mới: {tax_name} - {tax_rate}%")
                    created_count += 1
                    
            except Exception as e:
                print(f"   ❌ Lỗi: {tax_name} - {str(e)[:60]}")
                error_count += 1
    
    print()
    print(f"📊 Kết quả import thuế:")
    print(f"   ✅ Tạo mới: {created_count}")
    print(f"   ↻ Cập nhật: {updated_count}")
    print(f"   ❌ Lỗi: {error_count}")
else:
    print(f"❌ Không tìm thấy file: {tax_csv_path}")
    print("   Tạo file CSV mẫu với các cột: name,rate,type_tax_use,description")

# ============================================
# PHẦN 3: IMPORT ĐƠN VỊ TÍNH TỪ CSV
# ============================================
print()
print("=" * 70)
print("PHẦN 3: IMPORT ĐƠN VỊ TÍNH TỪ CSV")
print("=" * 70)
print()

uom_csv_path = '/home/sgc/odoo-19-docker-compose/data/Đơn vị tính.csv'

if os.path.exists(uom_csv_path):
    print(f"📄 Đọc file: {uom_csv_path}")
    
    created_count = 0
    updated_count = 0
    error_count = 0
    
    # Odoo 19 uses relative_uom_id instead of categories
    # First pass: create reference UOMs (those without reference_uom)
    # Second pass: create dependent UOMs (those with reference_uom)
    
    uom_cache = {}  # To store created UOM IDs
    
    with open(uom_csv_path, 'r', encoding='utf-8') as f:
        csv_data = list(csv.DictReader(f))
    
    # Pass 1: Reference UOMs (no parent)
    print("\n📌 Pass 1: Creating reference UOMs...")
    for row in csv_data:
        try:
            uom_name = row['name']
            reference_uom = row['reference_uom'].strip()
            relative_factor = float(row['relative_factor'])
            uom_rounding = float(row['rounding'])
            
            # Skip if this has a reference (will be created in pass 2)
            if reference_uom:
                continue
            
            # Check if already exists
            existing_uom = models.execute_kw(db, uid, password,
                'uom.uom', 'search',
                [[['name', '=', uom_name]]])
            
            uom_data = {
                'name': uom_name,
                'relative_factor': relative_factor,
                'rounding': uom_rounding,
                'active': True,
            }
            
            if existing_uom:
                # Update
                models.execute_kw(db, uid, password,
                    'uom.uom', 'write', [[existing_uom[0]], uom_data])
                print(f"   ↻ Cập nhật: {uom_name} (reference)")
                uom_cache[uom_name] = existing_uom[0]
                updated_count += 1
            else:
                # Create new
                uom_id = models.execute_kw(db, uid, password,
                    'uom.uom', 'create', [uom_data])
                print(f"   ✓ Tạo mới: {uom_name} (reference)")
                uom_cache[uom_name] = uom_id
                created_count += 1
                    
        except Exception as e:
            print(f"   ❌ Lỗi: {uom_name} - {str(e)[:60]}")
            error_count += 1
    
    # Pass 2: Dependent UOMs (with reference_uom)
    print("\n📌 Pass 2: Creating dependent UOMs...")
    for row in csv_data:
        try:
            uom_name = row['name']
            reference_uom = row['reference_uom'].strip()
            relative_factor = float(row['relative_factor'])
            uom_rounding = float(row['rounding'])
            
            # Skip if this is a reference UOM (already created in pass 1)
            if not reference_uom:
                continue
            
            # Find reference UOM ID
            if reference_uom in uom_cache:
                ref_uom_id = uom_cache[reference_uom]
            else:
                # Search for it
                ref_uom = models.execute_kw(db, uid, password,
                    'uom.uom', 'search',
                    [[['name', '=', reference_uom]]])
                if not ref_uom:
                    print(f"   ⚠️  Bỏ qua: {uom_name} - Không tìm thấy reference UOM: {reference_uom}")
                    error_count += 1
                    continue
                ref_uom_id = ref_uom[0]
                uom_cache[reference_uom] = ref_uom_id
            
            # Check if already exists
            existing_uom = models.execute_kw(db, uid, password,
                'uom.uom', 'search',
                [[['name', '=', uom_name]]])
            
            uom_data = {
                'name': uom_name,
                'relative_uom_id': ref_uom_id,
                'relative_factor': relative_factor,
                'rounding': uom_rounding,
                'active': True,
            }
            
            if existing_uom:
                # Update
                models.execute_kw(db, uid, password,
                    'uom.uom', 'write', [[existing_uom[0]], uom_data])
                print(f"   ↻ Cập nhật: {uom_name} → {reference_uom}")
                updated_count += 1
            else:
                # Create new
                models.execute_kw(db, uid, password,
                    'uom.uom', 'create', [uom_data])
                print(f"   ✓ Tạo mới: {uom_name} → {reference_uom}")
                created_count += 1
                    
        except Exception as e:
            print(f"   ❌ Lỗi: {uom_name} - {str(e)[:60]}")
            error_count += 1
    
    print()
    print(f"📊 Kết quả import đơn vị tính:")
    print(f"   ✅ Tạo mới: {created_count}")
    print(f"   ↻ Cập nhật: {updated_count}")
    print(f"   ❌ Lỗi: {error_count}")
else:
    print(f"❌ Không tìm thấy file: {uom_csv_path}")
    print("   Tạo file CSV mẫu với các cột: name,category,uom_type,factor,rounding")

# ============================================
# TÓM TẮT
# ============================================
print()
print("=" * 70)
print("✅ HOÀN TẤT CẤU HÌNH!")
print("=" * 70)
print()
print("📋 ĐÃ CẤU HÌNH:")
print("   ✅ Thông tin công ty (My Company)")
print("   ✅ Thuế GTGT theo chuẩn Việt Nam")
print("   ✅ Đơn vị tính phổ biến")
print()
print("🔍 KIỂM TRA:")
print("   1. Vào Settings → Companies → My Company")
print("   2. Vào Accounting → Configuration → Taxes")
print("   3. Vào Inventory → Configuration → Units of Measure")
print()
print("📝 CHỈNH SỬA:")
print("   - Sửa file CSV trong: /home/sgc/odoo-19-docker-compose/data/")
print("   - Chạy lại script này để cập nhật")
print()
