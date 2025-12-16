from models.FloodReportModel import FloodReportModel
from models.GoogleSheetsModel import GoogleSheetsModel
import os
import uuid
import streamlit as st

class FloodReportController:
    def __init__(self):
        self.flood_model = FloodReportModel()
        self.sheets_model = None
        self.upload_folder = "uploads"
        
        # Initialize Google Sheets hanya untuk TAB 1
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
        
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def check_daily_limit(self, ip_address):
        """Check if daily limit (10 reports per IP) has been reached - TANPA PERUBAHAN"""
        try:
            today_count = self.flood_model.get_today_reports_count_by_ip(ip_address)
            return today_count < 10
        except Exception as e:
            print(f"⚠️ Error in check_daily_limit: {e}")
            return True

def submit_report(self, address, flood_height, reporter_name, reporter_phone=None, photo_file=None):
    """Submit new flood report"""
    photo_path = None
    photo_url = None
    
    try:
        # Get client IP
        client_ip = self.get_client_ip()
        
        # Check daily limit
        if not self.check_daily_limit(client_ip):
            return False, "❌ Anda telah mencapai batas maksimal 10 laporan per hari."
        
        # Handle photo upload
        if photo_file is not None:
            try:
                file_extension = photo_file.name.split('.')[-1].lower()
                filename = f"{uuid.uuid4()}.{file_extension}"
                photo_path = os.path.join(self.upload_folder, filename)
                
                with open(photo_path, "wb") as f:
                    f.write(photo_file.getbuffer())
                
                photo_url = f"uploads/{filename}"
                
            except Exception as e:
                print(f"❌ Error saving photo: {e}")
        
        # Create report in SQLite database
        report_id = self.flood_model.create_report(
            address=address,
            flood_height=flood_height,
            reporter_name=reporter_name,
            reporter_phone=reporter_phone,
            photo_path=photo_path,
            ip_address=client_ip
        )
        
        # DEBUG: Print untuk melihat apa yang terjadi
        print(f"DEBUG: report_id = {report_id}")
        print(f"DEBUG: address = {address}")
        print(f"DEBUG: flood_height = {flood_height}")
        print(f"DEBUG: photo_path = {photo_path}")
        print(f"DEBUG: ip_address = {client_ip}")
        
        if report_id:
            # SIMPAN KE GOOGLE SHEETS
            if self.sheets_model and self.sheets_model.client:
                try:
                    sheets_data = {
                        'address': address,
                        'flood_height': flood_height,
                        'reporter_name': reporter_name,
                        'reporter_phone': reporter_phone or '',
                        'ip_address': client_ip,
                        'photo_url': photo_url or ''
                    }
                    
                    success = self.sheets_model.save_flood_report(sheets_data)
                    if success:
                        print("✅ Report saved to Google Sheets")
                except Exception as e:
                    print(f"⚠️ Error saving to Google Sheets: {e}")
            
            return True, "✅ Laporan berhasil dikirim!"
        else:
            if photo_path and os.path.exists(photo_path):
                os.remove(photo_path)
            return False, "❌ Gagal menyimpan laporan"  # <-- INI YANG MUNCUL
            
    except Exception as e:
        print(f"❌ Error in submit_report: {e}")
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)
        return False, f"❌ Error: {str(e)}"
    
    # ============ FUNGSI UNTUK VIEWS - TANPA PERUBAHAN ============
    
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
        """Get client IP address"""
        try:
            if 'user_ip' not in st.session_state:
                import random
                st.session_state.user_ip = f"192.168.1.{random.randint(1, 255)}"
            return st.session_state.user_ip
        except:
            return "user_local_test"

