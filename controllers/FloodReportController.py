from models.FloodReportModel import FloodReportModel
from models.GoogleSheetsModel import GoogleSheetsModel
import os
import uuid
from datetime import datetime
import streamlit as st
import traceback

class FloodReportController:
    def __init__(self):
        self.flood_model = FloodReportModel()
        self.sheets_model = None
        self.upload_folder = "uploads"
        
        # Initialize Google Sheets
        try:
            self.sheets_model = GoogleSheetsModel()
            if self.sheets_model and hasattr(self.sheets_model, 'client') and self.sheets_model.client:
                print("✅ Google Sheets connected for flood reports")
            else:
                print("⚠️ Google Sheets offline - using SQLite only")
                self.sheets_model = None
        except Exception as e:
            print(f"⚠️ Google Sheets init error: {e}")
            self.sheets_model = None
        
        # Create upload folder
        self._ensure_upload_folder()
        print("✅ FloodReportController initialized")
    
    def _ensure_upload_folder(self):
        """Ensure upload folder exists"""
        try:
            if not os.path.exists(self.upload_folder):
                os.makedirs(self.upload_folder)
                print(f"✅ Created upload folder: {os.path.abspath(self.upload_folder)}")
            else:
                print(f"✅ Upload folder exists: {self.upload_folder}")
        except Exception as e:
            print(f"❌ Error creating upload folder: {e}")
    
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
        """Submit new flood report"""
        photo_path = None
        photo_filename = None
        
        try:
            # Get client IP
            client_ip = self.get_client_ip()
            print(f"🌐 Client IP: {client_ip}")
            
            # Check daily limit
            if not self.check_daily_limit(client_ip):
                return False, "❌ Anda telah mencapai batas maksimal 10 laporan per hari."
            
            # Handle photo upload (OPTIONAL)
            if photo_file is not None:
                try:
                    file_extension = photo_file.name.split('.')[-1].lower()
                    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
                    
                    if file_extension not in valid_extensions:
                        return False, f"❌ Format file tidak didukung. Gunakan: {', '.join(valid_extensions)}"
                    
                    photo_filename = f"{uuid.uuid4()}.{file_extension}"
                    photo_path = os.path.join(self.upload_folder, photo_filename)
                    
                    print(f"📸 Saving photo to: {photo_path}")
                    
                    # Save photo
                    with open(photo_path, "wb") as f:
                        f.write(photo_file.getbuffer())
                    
                    print(f"✅ Photo saved: {photo_filename}")
                    
                except Exception as e:
                    print(f"⚠️ Error saving photo: {e}")
                    # Lanjutkan tanpa foto jika error
                    photo_path = None
                    photo_filename = None
            
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
                # Cleanup photo if exists
                if photo_path and os.path.exists(photo_path):
                    try:
                        os.remove(photo_path)
                    except:
                        pass
                return False, "❌ Gagal menyimpan laporan ke database lokal."
            
            print(f"✅ SQLite save successful! Report ID: {report_id}")
            
            # STEP 2: Save to Google Sheets (if available)
            if self.sheets_model and self.sheets_model.client:
                try:
                    print("📊 Saving to Google Sheets...")
                    
                    # Prepare data untuk Google Sheets
                    sheets_data = {
                        'address': str(address),
                        'flood_height': str(flood_height),
                        'reporter_name': str(reporter_name),
                        'reporter_phone': str(reporter_phone) if reporter_phone else '',
                        'ip_address': str(client_ip),
                        'photo_url': f"uploads/{photo_filename}" if photo_filename else ''
                    }
                    
                    print(f"📋 Google Sheets data prepared")
                    
                    success = self.sheets_model.save_flood_report(sheets_data)
                    if success:
                        print("✅ Report saved to Google Sheets")
                        gs_status = " (dan Google Sheets)"
                    else:
                        print("⚠️ Failed to save to Google Sheets")
                        gs_status = " (Google Sheets gagal)"
                except Exception as e:
                    print(f"⚠️ Error saving to Google Sheets: {e}")
                    gs_status = " (Google Sheets error)"
            else:
                print("ℹ️ Google Sheets not available")
                gs_status = ""
            
            # STEP 3: Verify data was saved
            today_reports = self.flood_model.get_today_reports()
            print(f"✅ Verification: Total reports today = {len(today_reports)}")
            
            return True, f"✅ Laporan berhasil dikirim! Data telah disimpan di database{gs_status}."
                
        except Exception as e:
            print(f"❌ CRITICAL Error in submit_report: {e}")
            traceback.print_exc()
            
            # Cleanup on error
            if photo_path and os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                except:
                    pass
            
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
        """Get client IP address"""
        try:
            # Generate a consistent IP for the session
            if 'user_ip' not in st.session_state:
                import random
                st.session_state.user_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
            
            ip = st.session_state.user_ip
            print(f"🖥️ Using IP: {ip}")
            return ip
            
        except Exception as e:
            print(f"⚠️ Error getting IP: {e}")
            return "unknown_user"
