import streamlit as st
import os
import uuid
from datetime import datetime
import traceback

class FloodReportController:
    def __init__(self):
        print("🔄 Initializing FloodReportController...")
        
        # Import models di dalam init untuk avoid circular imports
        try:
            from models.FloodReportModel import FloodReportModel
            from models.GoogleSheetsModel import GoogleSheetsModel
            from models.GoogleDriveModel import GoogleDriveModel
            
            self.flood_model = FloodReportModel()
            self.sheets_model = GoogleSheetsModel()
            self.drive_model = GoogleDriveModel()
            
            print("✅ All models initialized")
        except Exception as e:
            print(f"⚠️ Model import error: {e}")
            self.flood_model = None
            self.sheets_model = None
            self.drive_model = None
    
    # ============ SUBMIT REPORT ============
    def submit_report(self, address, flood_height, reporter_name, reporter_phone=None, photo_file=None):
        """Submit new flood report"""
        try:
            # Get client IP
            client_ip = self.get_client_ip()
            print(f"🌐 Client IP: {client_ip}")
            
            # Handle photo
            photo_url = None
            if photo_file:
                photo_url = self._handle_photo(photo_file)
            
            # Save to SQLite
            if self.flood_model:
                report_id = self.flood_model.create_report(
                    alamat=address,
                    tinggi_banjir=flood_height,
                    nama_pelapor=reporter_name,
                    no_hp=reporter_phone,
                    photo_url=photo_url,
                    ip_address=client_ip
                )
                
                if report_id:
                    print(f"✅ SQLite saved: ID {report_id}")
            
            # Save to Google Sheets
            if self.sheets_model and hasattr(self.sheets_model, 'save_flood_report'):
                sheets_data = {
                    'address': address,
                    'flood_height': flood_height,
                    'reporter_name': reporter_name,
                    'reporter_phone': reporter_phone or '',
                    'ip_address': client_ip,
                    'photo_url': photo_url or ''
                }
                self.sheets_model.save_flood_report(sheets_data)
                print("✅ Google Sheets saved")
            
            return True, "✅ Laporan berhasil dikirim!"
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False, f"❌ Error: {str(e)}"
    
    def _handle_photo(self, photo_file):
        """Handle photo upload"""
        try:
            # Save to temp file
            file_extension = photo_file.name.split('.')[-1]
            filename = f"{uuid.uuid4()}.{file_extension}"
            
            # In Streamlit Cloud, save to /tmp/
            if 'STREAMLIT_CLOUD' in os.environ:
                save_path = f"/tmp/{filename}"
            else:
                save_path = f"uploads/{filename}"
                
            with open(save_path, "wb") as f:
                f.write(photo_file.getbuffer())
            
            return save_path
        except:
            return None
    
    # ============ REPORT METHODS (WAJIB ADA) ============
    def get_today_reports(self):
        """Get today's reports - METHOD WAJIB ADA"""
        try:
            if self.flood_model and hasattr(self.flood_model, 'get_today_reports'):
                return self.flood_model.get_today_reports()
            else:
                print("⚠️ Flood model not available for get_today_reports")
                return []
        except Exception as e:
            print(f"❌ Error in get_today_reports: {e}")
            return []
    
    def get_month_reports(self):
        """Get month's reports - METHOD WAJIB ADA"""
        try:
            if self.flood_model and hasattr(self.flood_model, 'get_month_reports'):
                return self.flood_model.get_month_reports()
            else:
                print("⚠️ Flood model not available for get_month_reports")
                return []
        except Exception as e:
            print(f"❌ Error in get_month_reports: {e}")
            return []
    
    def get_all_reports(self):
        """Get all reports"""
        try:
            if self.flood_model and hasattr(self.flood_model, 'get_all_reports'):
                return self.flood_model.get_all_reports()
            else:
                return []
        except:
            return []
    
    def get_monthly_statistics(self):
        """Get monthly statistics"""
        try:
            if self.flood_model and hasattr(self.flood_model, 'get_monthly_statistics'):
                return self.flood_model.get_monthly_statistics()
            else:
                return {'total_reports': 0, 'month': ''}
        except:
            return {'total_reports': 0, 'month': ''}
    
    def get_client_ip(self):
        """Get client IP"""
        if 'user_ip' not in st.session_state:
            import random
            st.session_state.user_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
        return st.session_state.user_ip
    
    def check_daily_limit(self, ip_address):
        """Check daily limit"""
        try:
            if self.flood_model and hasattr(self.flood_model, 'get_today_reports_count_by_ip'):
                count = self.flood_model.get_today_reports_count_by_ip(ip_address)
                return count < 10
            return True
        except:
            return True
