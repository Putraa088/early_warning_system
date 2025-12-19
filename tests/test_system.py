#!/usr/bin/env python3
"""
Test sistem secara manual di VS Code
"""

import os
import sys
import sqlite3
from datetime import datetime

print("=" * 60)
print("🧪 MANUAL SYSTEM TEST - VS CODE")
print("=" * 60)

# Add current directory to path
sys.path.insert(0, os.getcwd())

# 1. Cek struktur folder
print("\n📂 Folder structure:")
print(f"  Current dir: {os.getcwd()}")
files = os.listdir('.')
print(f"  Files: {len(files)} files")
print(f"  Dirs: {[d for d in os.listdir('.') if os.path.isdir(d)]}")

# 2. Test database
db_file = 'flood_system.db'
print(f"\n🗄️  Database test:")
print(f"  File: {os.path.abspath(db_file)}")
print(f"  Exists: {os.path.exists(db_file)}")

if os.path.exists(db_file):
    # Hapus untuk test fresh
    try:
        os.remove(db_file)
        print("  ✅ Old database removed")
    except:
        print("  ❌ Cannot remove database, mungkin sedang digunakan")

# 3. Buat database baru
print("\n🔄 Creating fresh database...")
try:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flood_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            address TEXT NOT NULL,
            flood_height TEXT NOT NULL,
            reporter_name TEXT NOT NULL,
            reporter_phone TEXT,
            photo_path TEXT,
            ip_address TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Test insert
    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO flood_reports 
        (timestamp, address, flood_height, reporter_name, ip_address)
        VALUES (?, ?, ?, ?, ?)
    ''', (test_time, "Jl. Test VS Code", "Setinggi lutut", "VS Code User", "192.168.1.100"))

    conn.commit()

    # Verifikasi
    cursor.execute('SELECT COUNT(*) FROM flood_reports')
    count = cursor.fetchone()[0]
    print(f"  ✅ Test insert: {count} records")

    cursor.execute('SELECT * FROM flood_reports')
    rows = cursor.fetchall()
    print(f"  ✅ Data in database:")
    for row in rows:
        print(f"    ID: {row[0]}, Address: {row[2]}, Name: {row[4]}, Time: {row[1]}")

    conn.close()
    print("  ✅ Database test passed")
    
except Exception as e:
    print(f"  ❌ Database test failed: {e}")
    import traceback
    traceback.print_exc()

# 4. Test model
print("\n🧪 Testing FloodReportModel...")
try:
    # Create models folder and __init__.py if not exists
    if not os.path.exists('models'):
        os.makedirs('models')
    if not os.path.exists('models/__init__.py'):
        with open('models/__init__.py', 'w') as f:
            f.write('')
    
    from models.FloodReportModel import FloodReportModel
    
    model = FloodReportModel()
    print("  ✅ Model initialized")
    
    # Test create report
    report_id = model.create_report(
        address="Jl. Model Test 456",
        flood_height="Setinggi betis",
        reporter_name="Model Test User",
        reporter_phone="08123456789",
        photo_path=None,
        ip_address="192.168.1.200"
    )
    
    if report_id:
        print(f"  ✅ Model create_report: ID {report_id}")
        
        # Test get reports
        reports = model.get_today_reports()
        print(f"  ✅ Today's reports: {len(reports)}")
        
        if reports:
            for report in reports[:3]:  # Show first 3
                print(f"    - ID {report['id']}: {report['address'][:30]}... by {report['reporter_name']}")
        else:
            print("    ℹ️ No reports found")
    else:
        print("  ❌ Model create_report failed!")
        
except Exception as e:
    print(f"  ❌ Model test error: {e}")
    import traceback
    traceback.print_exc()

# 5. Test controller
print("\n🧪 Testing FloodReportController...")
try:
    # Create controllers folder and __init__.py if not exists
    if not os.path.exists('controllers'):
        os.makedirs('controllers')
    if not os.path.exists('controllers/__init__.py'):
        with open('controllers/__init__.py', 'w') as f:
            f.write('')
    
    from controllers.FloodReportController import FloodReportController
    
    controller = FloodReportController()
    print("  ✅ Controller initialized")
    
    # Test methods
    print("  ℹ️ Testing controller methods...")
    
    # Test get today reports
    reports = controller.get_today_reports()
    print(f"  ✅ Controller get_today_reports: {len(reports)} reports")
    
    # Test monthly stats
    stats = controller.get_monthly_statistics()
    print(f"  ✅ Monthly statistics: {stats}")
    
    print("  ℹ️ Controller ready for form submission")
    
except Exception as e:
    print(f"  ❌ Controller test error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("🎯 TESTING INSTRUCTION:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Jalankan: streamlit run app.py")
print("3. Buka browser ke http://localhost:8501")
print("4. Pilih menu 'Lapor Banjir'")
print("5. Isi form (tanpa foto dulu)")
print("6. Klik 'Kirim Laporan'")
print("7. Cek terminal untuk debug output")
print("8. Cek halaman 'Laporan Harian' untuk verifikasi")
print("=" * 60)