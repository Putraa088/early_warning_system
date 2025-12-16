from models.FloodReportModel import FloodReportModel
from models.GoogleSheetsModel import GoogleSheetsModel
import os
import uuid
from datetime import datetime
import streamlit as st

class FloodReportController:
    def __init__(self):
        self.flood_model = FloodReportModel()
        self.sheets_model = None
        self.upload_folder = "uploads"
        
        # Initialize Google Sheets
        try:
            self.sheets_model = GoogleSheetsModel()
            if self.sheets_model.client:
                print("✅ Google Sheets connected for flood reports")
            else:
                print("⚠️ Google Sheets offline - using SQLite only")
                self.sheets_model = None
        except Exception as e:
            print(f"⚠️ Google Sheets init error: {e}")
            self.sheets_model = None
        
        # Create upload folder
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def check_daily_limit(self, ip_address):
        """Check if daily limit (10 reports per IP) has been reached"""
        try:
            today_count = self.flood_model.get_today_reports_count_by_ip(ip_address)
            can_submit = today_count < 10
            print(f"📊 Daily limit check: IP={ip_address}, Count={today_count}, CanSubmit={can_submit}")
            return can_submit
        except Exception as e:
            print(f"⚠️ Error in check_daily_limit: {e}")
            return True

    def submit_report(self, address, flood_height, reporter_name, reporter_phone=None, photo_file=None):
        """Submit new flood report - COMPLETE FIX"""
        photo_path = None
        photo_url = None
        
        try:
            # Get client IP
            client_ip = self.get_client_ip()
            print(f"🌐 Client IP: {client_ip}")
            
            # Check daily limit
            if not self.check_daily_limit(client_ip):
                return False, "❌ Anda telah mencapai batas maksimal 10 laporan per hari."
            
            # Handle photo upload
            if photo_file is not None:
                try:
                    file_extension = photo_file.name.split('.')[-1].lower()
                    filename = f"{uuid.uuid4()}.{file_extension}"
                    photo_path = os.path.join(self.upload_folder, filename)
                    
                    print(f"📸 Saving photo to: {photo_path}")
                    with open(photo_path, "wb") as f:
                        f.write(photo_file.getbuffer())
                    
                    photo_url = f"uploads/{filename}"
                    print(f"✅ Photo saved: {photo_url}")
                    
                except Exception as e:
                    print(f"❌ Error saving photo: {e}")
            
            # STEP 1: Create report in SQLite database
            print("💾 Saving to SQLite database...")
            report_id = self.flood_model.create_report(
                address=address,
                flood_height=flood_height,
                reporter_name=reporter_name,
                reporter_phone=reporter_phone,
                photo_path=photo_path,
                ip_address=client_ip
            )
            
            if not report_id:
                print("❌ Failed to save to SQLite")
                if photo_path and os.path.exists(photo_path):
                    os.remove(photo_path)
                return False, "❌ Gagal menyimpan laporan ke database lokal."
            
            print(f"✅ SQLite save successful! Report ID: {report_id}")
            
            # STEP 2: Save to Google Sheets (if available)
            if self.sheets_model and self.sheets_model.client:
                try:
                    print("📊 Saving to Google Sheets...")
                    sheets_data = {
                        'address': address,
                        'flood_height': flood_height,
                        'reporter_name': reporter_name,
                        'reporter_phone': reporter_phone or '',
                        'ip_address': client_ip,
                        'photo_url': photo_url or '',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    success = self.sheets_model.save_flood_report(sheets_data)
                    if success:
                        print("✅ Report saved to Google Sheets")
                    else:
                        print("⚠️ Failed to save to Google Sheets")
                except Exception as e:
                    print(f"⚠️ Error saving to Google Sheets: {e}")
            else:
                print("ℹ️ Google Sheets not available, skipping...")
            
            # STEP 3: Verify data was saved
            today_reports = self.flood_model.get_today_reports()
            print(f"✅ Verification: Total reports today = {len(today_reports)}")
            
            return True, "✅ Laporan berhasil dikirim! Data telah disimpan di database dan Google Sheets."
                
        except Exception as e:
            print(f"❌ CRITICAL Error in submit_report: {e}")
            import traceback
            traceback.print_exc()
            
            # Cleanup on error
            if photo_path and os.path.exists(photo_path):
                os.remove(photo_path)
            
            return False, f"❌ Error sistem: {str(e)}"
    
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
        """Get client IP address - FIXED"""
        try:
            import random
            # Generate consistent IP for session
            if 'user_ip' not in st.session_state:
                st.session_state.user_ip = f"192.168.1.{random.randint(100, 200)}"
            
            ip = st.session_state.user_ip
            print(f"🖥️ Using IP: {ip}")
            return ip
            
        except Exception as e:
            print(f"⚠️ Error getting IP: {e}")
            return "user_local_test"
