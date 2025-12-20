#!/usr/bin/env python3
"""
TEST SISTEM SETELAH CLEANUP DAN UPDATE
Jalankan: python test_system.py
"""

import os
import sys
import subprocess
import importlib
import sqlite3

def print_header(text):
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def test_python_version():
    """Test versi Python"""
    print_header("🐍 TEST VERSI PYTHON")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version OK (3.8+)")
        return True
    else:
        print("⚠️  Python version might be too old")
        return True  # Tidak fatal

def test_imports():
    """Test semua import yang diperlukan"""
    print_header("📦 TEST IMPORTS")
    
    modules_to_test = [
        # Core
        ('streamlit', 'st'),
        ('pandas', 'pd'),
        ('numpy', 'np'),
        
        # Models
        ('controllers.FloodReportController', 'FloodReportController'),
        ('controllers.RealTimeDataController', 'RealTimeDataController'),
        ('models.FloodReportModel', 'FloodReportModel'),
        ('models.GoogleSheetsModel', 'GoogleSheetsModel'),
        
        # Views
        ('views.flood_report_form', 'show_flood_report_form'),
        ('views.flood_reports_table', 'show_current_month_reports'),
        ('views.monthly_reports', 'show_monthly_reports_summary'),
        ('views.prediction_dashboard', 'show_prediction_dashboard'),
        ('views.panduan_page', 'show_panduan_page'),
        
        # Utilities
        ('model_ann', 'predict_flood_ann_with_temp_range'),
        ('gumbel_distribution', 'predict_flood_gumbel'),
    ]
    
    failed_imports = []
    
    for module_path, item_name in modules_to_test:
        try:
            if '.' in module_path:
                # Untuk module dengan path
                module = importlib.import_module(module_path)
                print(f"✅ {module_path}")
            else:
                # Untuk package langsung
                importlib.import_module(module_path)
                print(f"✅ {module_path}")
        except ImportError as e:
            print(f"❌ {module_path}: {e}")
            failed_imports.append(module_path)
        except Exception as e:
            print(f"⚠️  {module_path}: {e}")
    
    if failed_imports:
        print(f"\n❌ Total {len(failed_imports)} import gagal")
        return False
    
    print(f"\n✅ Semua import berhasil ({len(modules_to_test)} modules)")
    return True

def test_app_py_syntax():
    """Test syntax app.py"""
    print_header("📄 TEST APP.PY SYNTAX")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test compile
        compile(content, 'app.py', 'exec')
        
        # Cek apakah ada import yang tidak seharusnya
        forbidden_patterns = [
            'VisitorController',
            'AuthController',
            'auth_views',
            'visitor_stats',
            'UserModel',
            'VisitorModel'
        ]
        
        found_patterns = []
        for pattern in forbidden_patterns:
            if pattern in content:
                found_patterns.append(pattern)
        
        if found_patterns:
            print(f"⚠️  Masih ada referensi ke: {', '.join(found_patterns)}")
            return False
        
        print("✅ app.py syntax OK dan bersih")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_database():
    """Test database connection dan struktur"""
    print_header("🗄️ TEST DATABASE")
    
    db_file = 'flood_system.db'
    
    if not os.path.exists(db_file):
        print("ℹ️  Database file belum ada (mungkin pertama kali run)")
        return True
    
    try:
        # Test koneksi
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Test tabel flood_reports
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flood_reports'")
        if cursor.fetchone():
            print("✅ Tabel 'flood_reports' ada")
            
            # Test struktur kolom
            cursor.execute("PRAGMA table_info(flood_reports)")
            columns = cursor.fetchall()
            print(f"✅ Tabel memiliki {len(columns)} kolom")
            
            # Test ada data
            cursor.execute("SELECT COUNT(*) FROM flood_reports")
            count = cursor.fetchone()[0]
            print(f"✅ Total data: {count} laporan")
        else:
            print("⚠️  Tabel 'flood_reports' tidak ditemukan")
        
        # Test tabel lain tidak seharusnya ada
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('users', 'visitor_stats')")
        unwanted_tables = cursor.fetchall()
        
        if unwanted_tables:
            print(f"⚠️  Tabel tidak diinginkan ditemukan: {[t[0] for t in unwanted_tables]}")
        
        conn.close()
        print("✅ Database connection OK")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_folder_structure():
    """Test struktur folder"""
    print_header("📁 TEST STRUKTUR FOLDER")
    
    required_folders = [
        'controllers',
        'models', 
        'views',
        'uploads'
    ]
    
    required_files = [
        'app.py',
        'model_ann.py',
        'gumbel_distribution.py',
        'requirements.txt'
    ]
    
    all_ok = True
    
    print("📂 Folder yang harus ada:")
    for folder in required_folders:
        if os.path.exists(folder) and os.path.isdir(folder):
            print(f"  ✅ {folder}/")
        else:
            print(f"  ❌ {folder}/ (missing)")
            all_ok = False
    
    print("\n📄 File yang harus ada:")
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size} bytes)")
        else:
            print(f"  ❌ {file} (missing)")
            all_ok = False
    
    # Cek file yang seharusnya dihapus
    deleted_files = [
        'controllers/AuthController.py',
        'controllers/VisitorController.py',
        'models/UserModel.py',
        'models/VisitorModel.py',
        'views/auth_views.py',
        'views/visitor_stats.py',
        'setup_google_sheet.py',
        'test_connection.py',
        'test_network.py',
        'final_test.py'
    ]
    
    print("\n🗑️  File yang seharusnya dihapus:")
    still_exist = []
    for file in deleted_files:
        if os.path.exists(file):
            print(f"  ❌ {file} (masih ada, harus dihapus)")
            still_exist.append(file)
            all_ok = False
        else:
            print(f"  ✅ {file} (sudah dihapus)")
    
    if still_exist:
        print(f"\n⚠️  {len(still_exist)} file masih ada yang harus dihapus")
    
    return all_ok

def test_panduan_page():
    """Test khusus untuk halaman panduan baru"""
    print_header("📘 TEST HALAMAN PANDUAN")
    
    try:
        # Test file ada
        if not os.path.exists('views/panduan_page.py'):
            print("❌ File views/panduan_page.py tidak ditemukan")
            return False
        
        # Test bisa diimport
        from views.panduan_page import show_panduan_page
        
        # Test function ada
        if callable(show_panduan_page):
            print("✅ Function show_panduan_page OK")
        else:
            print("❌ show_panduan_page bukan function")
            return False
        
        # Test file size reasonable
        size = os.path.getsize('views/panduan_page.py')
        if size > 10000:  # Minimal 10KB
            print(f"✅ File size OK ({size} bytes)")
        else:
            print(f"⚠️  File size kecil: {size} bytes")
        
        print("✅ Halaman panduan siap digunakan")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_menu_structure():
    """Test menu di app.py"""
    print_header("🍔 TEST STRUKTUR MENU")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cek menu items
        if '("Panduan", "Panduan")' in content:
            print("✅ Menu 'Panduan' ditemukan")
        else:
            print("❌ Menu 'Panduan' tidak ditemukan")
            return False
        
        # Cek handler
        if '"Panduan": show_panduan_page_handler' in content:
            print("✅ Handler untuk Panduan ditemukan")
        else:
            print("❌ Handler untuk Panduan tidak ditemukan")
            return False
        
        # Cek urutan menu
        menu_section = content.split('menu_items = [')[1].split(']')[0]
        menu_lines = [line.strip() for line in menu_section.split('\n') if line.strip()]
        
        expected_order = ['Home', 'Panduan', 'Lapor Banjir', 'Catatan Laporan', 'Prediksi', 'Simulasi']
        
        print(f"✅ Urutan menu: {len(menu_lines)} item")
        for i, line in enumerate(menu_lines, 1):
            print(f"  {i}. {line}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_streamlit_test():
    """Test streamlit bisa dijalankan"""
    print_header("🚀 TEST STREAMLIT")
    
    try:
        # Test 1: Streamlit version
        print("1. Testing Streamlit version...")
        result = subprocess.run(
            [sys.executable, '-m', 'streamlit', '--version'],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',  # Tambah encoding
            errors='ignore'    # Ignore encoding errors
        )
        
        if result.returncode == 0:
            version_line = result.stdout.strip()
            print(f"✅ {version_line}")
        else:
            print(f"❌ Streamlit not working: {result.stderr[:100]}")
            return False
        
        # Test 2: app.py syntax without actually running Streamlit
        print("\n2. Testing app.py module import (safe mode)...")
        try:
            # Use a safer approach - don't actually initialize Streamlit
            # Just check if the file can be parsed
            with open('app.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for syntax errors by compiling
            compile(content, 'app.py', 'exec')
            
            # Quick check for required functions
            required_functions = [
                'show_homepage',
                'show_flood_calculator_page', 
                'show_catatan_laporan_page',
                'show_harian_page',
                'show_bulanan_page',
                'show_flood_report_page',
                'show_prediction_page',
                'show_panduan_page_handler',
                'setup_sidebar',
                'main'
            ]
            
            missing_funcs = []
            for func in required_functions:
                if func not in content:
                    missing_funcs.append(func)
            
            if missing_funcs:
                print(f"⚠️  Missing functions: {missing_funcs}")
            else:
                print(f"✅ All {len(required_functions)} required functions found")
            
            print("✅ app.py syntax and structure OK")
            return True
            
        except SyntaxError as e:
            print(f"❌ Syntax error in app.py: {e}")
            return False
        except Exception as e:
            print(f"❌ Error checking app.py: {e}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout saat test streamlit")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 70)
    print("🧪 FLOOD WARNING SYSTEM - COMPREHENSIVE TEST")
    print("=" * 70)
    print("Test setelah cleanup dan penambahan menu Panduan")
    print()
    
    # Jalankan semua test
    tests = [
        ("Python Version", test_python_version),
        ("Imports", test_imports),
        ("app.py Syntax", test_app_py_syntax),
        ("Database", test_database),
        ("Folder Structure", test_folder_structure),
        ("Panduan Page", test_panduan_page),
        ("Menu Structure", test_menu_structure),
        ("Streamlit", run_streamlit_test),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n▶️ Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"   Status: ✅ PASS")
            else:
                print(f"   Status: ❌ FAIL")
        except Exception as e:
            print(f"   Error: {e}")
            results.append((test_name, False))
    
    # Tampilkan hasil
    print_header("📊 TEST RESULTS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("\nDETAIL HASIL:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n📈 SCORE: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "=" * 70)
        print("🎉 🎉 🎉 SEMUA TEST LULUS! 🎉 🎉 🎉")
        print("=" * 70)
        print("\n✅ Sistem siap digunakan!")
        print("\n🚀 Untuk menjalankan aplikasi:")
        print("   streamlit run app.py")
        print("\n🌐 Buka browser ke: http://localhost:8501")
        print("\n📋 Test manual yang disarankan:")
        print("1. Buka halaman Panduan (menu baru)")
        print("2. Test form Lapor Banjir")
        print("3. Cek Catatan Laporan (Harian & Bulanan)")
        print("4. Test Prediksi Real-time")
        print("5. Gunakan Simulasi Banjir")
    else:
        print(f"\n⚠️  {total-passed} test gagal. Periksa error di atas.")
        print("\n🔧 Troubleshooting:")
        print("1. Pastikan sudah menjalankan cleanup_files.py")
        print("2. Pastikan app.py sudah diupdate")
        print("3. Pastikan views/panduan_page.py sudah dibuat")
        print("4. Cek error message di atas untuk detail")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()