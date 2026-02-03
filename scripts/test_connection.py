#!/usr/bin/env python3
"""
Test connection to Odoo database
"""
import xmlrpc.client
import time

ODOO_URL = "http://localhost:10019"
DB_NAME = "odoo19_production"
ADMIN_EMAIL = "admin@odoo19.local"
ADMIN_PASSWORD = "Admin@2025!"

print("Testing Odoo connection...")
print(f"URL: {ODOO_URL}")
print(f"Database: {DB_NAME}")
print(f"Email: {ADMIN_EMAIL}")

max_attempts = 20
for attempt in range(1, max_attempts + 1):
    try:
        common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        print(f"\nAttempt {attempt}/{max_attempts}:")
        
        # Try to authenticate
        uid = common.authenticate(DB_NAME, ADMIN_EMAIL, ADMIN_PASSWORD, {})
        
        if uid:
            print(f"✅ SUCCESS! User ID: {uid}")
            print(f"\nYou can now use these credentials:")
            print(f"  URL: {ODOO_URL}")
            print(f"  Database: {DB_NAME}")
            print(f"  Email: {ADMIN_EMAIL}")
            print(f"  Password: {ADMIN_PASSWORD}")
            break
        else:
            print(f"❌ Authentication failed - waiting 15 seconds...")
            time.sleep(15)
    
    except Exception as e:
        print(f"⚠️  Error: {str(e)[:100]}")
        print(f"   Waiting 15 seconds...")
        time.sleep(15)
else:
    print("\n❌ Could not connect after all attempts")
    print("The database might still be initializing. Please wait a few more minutes.")
