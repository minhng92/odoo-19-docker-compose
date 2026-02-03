#!/bin/bash
#
# Complete Odoo Setup Script
# This script will guide you through the complete setup process
#

set -e

SCRIPT_DIR="/home/sgc/odoo-19-docker-compose/scripts"
ODOO_URL="http://localhost:10019"

echo "=================================================================="
echo "  🚀 Odoo 19 Complete Setup"
echo "=================================================================="
echo ""

# Check if Odoo is running
echo "📋 Step 1: Checking Odoo status..."
if ! docker compose ps | grep -q "odoo19.*Up"; then
    echo "   ⚠️  Odoo is not running. Starting..."
    docker compose up -d
    echo "   ⏳ Waiting 30 seconds for Odoo to start..."
    sleep 30
fi
echo "   ✅ Odoo is running!"
echo ""

# Check if database exists
echo "📋 Step 2: Checking database..."
DB_EXISTS=$(docker exec odoo-19-docker-compose-db-1 psql -U odoo -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='odoo19_production'" 2>/dev/null || echo "0")

if [ "$DB_EXISTS" = "1" ]; then
    echo "   ✅ Database 'odoo19_production' exists!"
    echo ""
    echo "   📝 Login credentials:"
    echo "   • URL: $ODOO_URL"
    echo "   • Database: odoo19_production"
    echo "   • Email: admin@odoo19.local"
    echo "   • Password: Admin@2025!"
    echo ""
    
    read -p "   Do you want to create companies now? (y/n): " CREATE_COMPANIES
    
    if [ "$CREATE_COMPANIES" = "y" ] || [ "$CREATE_COMPANIES" = "Y" ]; then
        echo ""
        echo "📋 Step 3: Creating 10 Vietnamese companies..."
        python3 "$SCRIPT_DIR/create_companies.py" <<EOF
odoo19_production
admin@odoo19.local
Admin@2025!
EOF
    fi
else
    echo "   ⚠️  Database does not exist yet!"
    echo ""
    echo "=================================================================="
    echo "  📝 Please create database manually:"
    echo "=================================================================="
    echo ""
    echo "1. Open your browser and go to: $ODOO_URL"
    echo "2. Fill in the database creation form:"
    echo "   • Master Password: minhng.info"
    echo "   • Database Name: odoo19_production"
    echo "   • Email: admin@odoo19.local"
    echo "   • Password: Admin@2025!"
    echo "   • Phone: +84 (leave empty or fill)"
    echo "   • Language: Vietnamese / Tiếng Việt"
    echo "   • Country: Vietnam"
    echo "   • Demo data: ✓ (checked)"
    echo ""
    echo "3. Click 'Create database' and wait 2-3 minutes"
    echo ""
    echo "4. After database is created, run this script again:"
    echo "   $0"
    echo ""
    echo "=================================================================="
fi

echo ""
echo "📋 Backup Information:"
echo "   • Automatic backup: 4:00 AM daily (Vietnam time)"
echo "   • Retention: 7 days"
    echo "   • Location: /home/sgc/odoo-19-docker-compose/backups/"
echo "   • To run backup manually:"
echo "     $SCRIPT_DIR/backup_odoo.sh"
echo ""

echo "=================================================================="
echo "  ✅ Setup script completed!"
echo "=================================================================="
