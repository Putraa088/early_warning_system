"""
RUN SISTEM PERINGATAN DINI BANJIR
==================================
File utama untuk menjalankan aplikasi Streamlit
"""

import subprocess
import sys
import os

def main():
    """Main function to run the flood warning system"""
    print("=" * 50)
    print("🌊 SISTEM PERINGATAN DINI BANJIR")
    print("=" * 50)
    
    # Periksa database
    if not os.path.exists('flood_system.db'):
        print("🔄 Database belum ada. Inisialisasi database...")
        try:
            from init_tables import init_database
            init_database()
            print("✅ Database berhasil diinisialisasi!")
        except Exception as e:
            print(f"❌ Gagal inisialisasi database: {e}")
            print("⚠️ Pastikan file init_tables.py ada di direktori yang sama")
    
    # Periksa requirements
    print("\n🔍 Memeriksa dependencies...")
    try:
        import streamlit
        import numpy
        import pandas
        print("✅ Semua dependencies terinstall dengan baik!")
    except ImportError as e:
        print(f"❌ Dependency error: {e}")
        print("⚠️ Jalankan: pip install -r requirements.txt")
        return
    
    # Jalankan aplikasi
    print("\n🚀 Menjalankan aplikasi Streamlit...")
    print("📱 Buka browser dan akses: http://localhost:8501")
    print("⏸️ Tekan Ctrl+C untuk menghentikan aplikasi\n")
    
    try:
        # Jalankan streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Aplikasi dihentikan oleh pengguna")
    except Exception as e:
        print(f"❌ Error menjalankan aplikasi: {e}")

if __name__ == "__main__":
    main()