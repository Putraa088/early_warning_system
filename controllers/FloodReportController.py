from models.FloodReportModel import FloodReportModel
import os
import uuid
from datetime import datetime
import streamlit as st

class FloodReportController:
    def __init__(self):
        self.flood_model = FloodReportModel()
        self.upload_folder = "uploads"
        
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
            print(f"✅ Created upload folder: {self.upload_folder}")

    def check_daily_limit(self, ip_address):
        """Check if daily limit (10 reports per IP) has been reached"""
        try:
            print(f"\n🔍 CHECKING LIMIT for IP: {ip_address}")
            
            # Hitung laporan hari ini
            today_count = self.flood_model.get_today_reports_count_by_ip(ip_address)
            
            print(f"📊 Today's reports count: {today_count}")
            print(f"📊 Limit: 10")
            print(f"📊 Can submit? {today_count < 10}")
            
            return today_count < 10
                
        except Exception as e:
            print(f"⚠️ Error in check_daily_limit: {e}")
            return True

    def submit_report(self, address, flood_height, reporter_name, reporter_phone=None, photo_file=None):
        """Submit new flood report dengan limit validation"""
        photo_path = None
        
        try:
            # Get client IP
            client_ip = self.get_client_ip()
            print(f"\n" + "="*50)
            print(f"📤 SUBMITTING NEW REPORT")
            print(f"🌐 IP Address: {client_ip}")
            print(f"📍 Address: {address}")
            print(f"📏 Flood Height: {flood_height}")
            print(f"👤 Reporter: {reporter_name}")
            print("="*50)
            
            # Check daily limit BEFORE submitting
            if not self.check_daily_limit(client_ip):
                return False, "❌ Anda telah mencapai batas maksimal 10 laporan per hari. Silakan kembali besok."
            
            # Handle photo upload
            if photo_file is not None:
                try:
                    file_extension = photo_file.name.split('.')[-1].lower()
                    filename = f"{uuid.uuid4()}.{file_extension}"
                    photo_path = os.path.join(self.upload_folder, filename)
                    
                    print(f"📸 Saving photo to: {photo_path}")
                    
                    with open(photo_path, "wb") as f:
                        f.write(photo_file.getbuffer())
                    
                    print("✅ Photo saved successfully")
                    
                except Exception as e:
                    print(f"❌ Error saving photo: {e}")
                    photo_path = None
            
            # Create report in database
            print("💾 Saving report to database...")
            report_id = self.flood_model.create_report(
                address=address,
                flood_height=flood_height,
                reporter_name=reporter_name,
                reporter_phone=reporter_phone,
                photo_path=photo_path,
                ip_address=client_ip
            )
            
            if report_id:
                print(f"✅ Report saved successfully with ID: {report_id}")
                
                # Cek count setelah submit
                new_count = self.flood_model.get_today_reports_count_by_ip(client_ip)
                print(f"📊 Updated count after submit: {new_count}/10")
                
                return True, "✅ Laporan berhasil dikirim!"
            else:
                print("❌ Failed to save report to database")
                if photo_path and os.path.exists(photo_path):
                    os.remove(photo_path)
                    print("🗑️ Deleted photo due to database error")
                return False, "❌ Gagal menyimpan laporan ke database"
                
        except Exception as e:
            print(f"❌ Error in submit_report: {e}")
            if photo_path and os.path.exists(photo_path):
                os.remove(photo_path)
            return False, f"❌ Error: {str(e)}"

    # ============ FUNGSI UNTUK VIEWS ============
    
    def get_today_reports(self):
        """Get today's flood reports"""
        return self.flood_model.get_today_reports()

    def get_month_reports(self):
        """Get this month's flood reports"""
        return self.flood_model.get_month_reports()

    def get_all_reports(self):
        """Get all flood reports"""
        return self.flood_model.get_all_reports()
    
    def get_monthly_statistics(self):
        """Get monthly statistics for reports"""
        return self.flood_model.get_monthly_statistics()
    
    def get_client_ip(self):
        """Get client IP address - Streamlit compatible"""
        try:
            # Dalam Streamlit, gunakan session state untuk simulasi IP
            if 'user_ip' not in st.session_state:
                # Generate simulated IP untuk testing
                import random
                st.session_state.user_ip = f"192.168.1.{random.randint(1, 255)}"
            
            return st.session_state.user_ip
        except:
            # Fallback untuk development
            return "user_local_test"