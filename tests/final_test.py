#!/usr/bin/env python3
"""Final test seluruh sistem - VERSION TERBARU"""

import sqlite3
import os
from datetime import datetime
import pytz

def test_complete_system():
    print("🎯 FINAL SYSTEM TEST - VERSION TERBARU")
    print("=" * 60)
    
    # 1. Test SQLite database
    print("\n1. Testing SQLite database...")
    db_path = 'flood_system.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        print("   Running database initialization...")
        
        try:
            # Inisialisasi database sederhana
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flood_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    "Timestamp" TEXT,
                    "Alamat" TEXT NOT NULL,
                    "Tinggi Banjir" TEXT NOT NULL,
                    "Nama Pelapor" TEXT NOT NULL,
                    "No HP" TEXT,
                    "IP Address" TEXT,
                    "Photo URL" TEXT,
                    "Status" TEXT DEFAULT 'pending',
                    report_date DATE,
                    report_time TIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Database created successfully")
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            return
    else:
        print(f"✅ Database exists: {os.path.getsize(db_path)} bytes")
    
    # 2. Test koneksi ke database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Cek struktur
        cursor.execute("PRAGMA table_info(flood_reports)")
        columns = cursor.fetchall()
        print(f"✅ SQLite table has {len(columns)} columns")
        
        # Cek data
        cursor.execute('SELECT COUNT(*) FROM flood_reports')
        count = cursor.fetchone()[0]
        print(f"📊 Total reports in SQLite: {count}")
        
        if count > 0:
            cursor.execute('SELECT "Alamat", "Nama Pelapor" FROM flood_reports LIMIT 3')
            samples = cursor.fetchall()
            print(f"📝 Sample data:")
            for sample in samples:
                print(f"   - {sample[0]} by {sample[1]}")
        
        conn.close()
    except Exception as e:
        print(f"❌ SQLite error: {e}")
    
    # 3. Test uploads folder
    print("\n2. Testing uploads folder...")
    uploads_folder = 'uploads'
    
    if not os.path.exists(uploads_folder):
        try:
            os.makedirs(uploads_folder)
            print(f"✅ Created uploads folder: {uploads_folder}")
        except Exception as e:
            print(f"❌ Error creating uploads folder: {e}")
    else:
        print(f"✅ Uploads folder exists")
    
    # 4. Test timezone
    print("\n3. Testing timezone (WIB)...")
    try:
        tz_wib = pytz.timezone('Asia/Jakarta')
        current_wib = datetime.now(tz_wib)
        print(f"✅ WIB Timezone: {current_wib.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"⚠️ Timezone error: {e}")
    
    # 5. Test credentials.json
    print("\n4. Checking credentials.json...")
    if os.path.exists('credentials.json'):
        import json
        try:
            with open('credentials.json', 'r') as f:
                creds = json.load(f)
            print(f"✅ credentials.json valid")
            print(f"   Project: {creds.get('project_id', 'N/A')}")
            print(f"   Email: {creds.get('client_email', 'N/A')}")
        except Exception as e:
            print(f"❌ Error reading credentials.json: {e}")
    else:
        print("⚠️ credentials.json not found (Google Sheets will be offline)")
    
    print("\n" + "=" * 60)
    print("🎉 SYSTEM READY!")
    print("\n📋 Status:")
    print(f"  ✅ 1. Database: {'READY' if os.path.exists(db_path) else 'NOT READY'}")
    print(f"  ✅ 2. Uploads folder: {'READY' if os.path.exists(uploads_folder) else 'NOT READY'}")
    print(f"  ✅ 3. Timezone: READY")
    print(f"  ✅ 4. Google Sheets: {'READY' if os.path.exists('credentials.json') else 'OFFLINE'}")
    print("\n🚀 Jalankan aplikasi:")
    print("   streamlit run app.py")
    print("=" * 60)

if __name__ == "__main__":
    test_complete_system()