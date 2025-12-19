from models.FloodReportModel import FloodReportModel
from models.GoogleSheetsModel import GoogleSheetsModel
from models.GoogleDriveModel import GoogleDriveModel
import os
import uuid
from datetime import datetime
import streamlit as st
import traceback

class FloodReportController:
    def __init__(self):
        self.flood_model = FloodReportModel()
        self.sheets_model = None
        self.drive_model = None
        
        # Initialize services
        self._initialize_services()
        
        print("✅ FloodReportController initialized")
    
    def _initialize_services(self):
        """Initialize semua services"""
        # Google Sheets
        try:
            self.sheets_model = GoogleSheetsModel()
            if self.sheets_model and hasattr(self.sheets_model, 'client') and self.sheets_model.client:
                print("✅ Google Sheets connected")
            else:
                print("⚠️ Google Sheets offline")
                self.sheets_model = None
        except Exception as e:
            print(f"⚠️ Google Sheets init error: {e}")
            self.sheets_model = None
        
        # Google Drive
        try:
            self.drive_model = GoogleDriveModel()
            if self.drive_model and self.drive_model.service:
                print("✅ Google Drive connected")
            else:
                print("⚠️ Google Drive offline")
                self.drive_model = None
        except Exception as e:
            print(f"⚠️ Google Drive init error: {e}")
            self.drive_model = None
    
    def submit_report(self, address, flood_height, reporter_name, reporter_phone=None, photo_file=None):
        """Submit new flood report dengan Google Drive untuk foto"""
        photo_info = None
        
        try:
            # Get client IP
            client_ip = self.get_client_ip()
            print(f"🌐 Client IP: {client_ip}")
            
            # Check daily limit
            if not self.check_daily_limit(client_ip):
                return False, "❌ Anda telah mencapai batas maksimal 10 laporan per hari."
            
            # Handle photo upload ke Google Drive
            if photo_file is not None:
                photo_info = self._handle_photo_upload_drive(photo_file)
                if photo_info is False:  # Jika ada error validasi
                    return False, "❌ Error uploading photo"
            
            # STEP 1: Coba save ke Google Sheets (PRIMARY)
            gs_success = False
            gs_message = ""
            
            if self.sheets_model and hasattr(self.sheets_model, 'client') and self.sheets_model.client:
                try:
                    print("📊 Saving to Google Sheets...")
                    
                    # Prepare data
                    sheets_data = {
                        'address': str(address),
                        'flood_height': str(flood_height),
                        'reporter_name': str(reporter_name),
                        'reporter_phone': str(reporter_phone) if reporter_phone else '',
                        'ip_address': str(client_ip),
                        'photo_url': photo_info['view_url'] if photo_info else ''
                    }
                    
                    gs_success = self.sheets_model.save_flood_report(sheets_data)
                    
                    if gs_success:
                        print("✅ Report saved to Google Sheets")
                        gs_message = "Google Sheets"
                    else:
                        print("⚠️ Failed to save to Google Sheets")
                        gs_message = " (Google Sheets gagal)"
                        
                except Exception as e:
                    print(f"⚠️ Error saving to Google Sheets: {e}")
                    gs_message = " (Google Sheets error)"
            else:
                print("ℹ️ Google Sheets not available")
                gs_message = ""
            
            # STEP 2: Coba save ke SQLite (BACKUP - opsional)
            sqlite_success = False
            sqlite_message = ""
            
            try:
                if self.flood_model:
                    print("💾 Saving to SQLite (backup)...")
                    
                    # Gunakan Google Drive URL jika ada
                    photo_url_for_sqlite = photo_info['direct_url'] if photo_info else None
                    
                    report_id = self.flood_model.create_report(
                        alamat=address,
                        tinggi_banjir=flood_height,
                        nama_pelapor=reporter_name,
                        no_hp=reporter_phone,
                        photo_url=photo_url_for_sqlite,
                        ip_address=client_ip
                    )
                    
                    if report_id:
                        sqlite_success = True
                        sqlite_message = "SQLite backup"
                        print(f"✅ SQLite backup saved (ID: {report_id})")
                    else:
                        print("⚠️ SQLite backup failed")
            except Exception as e:
                print(f"⚠️ SQLite error: {e}")
            
            # STEP 3: Prepare success message
            messages = []
            if gs_success:
                messages.append("Google Sheets")
            if sqlite_success:
                messages.append("SQLite backup")
            if photo_info:
                messages.append("Google Drive (foto)")
            
            if messages:
                success_message = f"✅ Laporan berhasil dikirim! Tersimpan di: {', '.join(messages)}"
                
                # Jika ada foto di Google Drive, tambahkan info
                if photo_info:
                    success_message += f"\n📷 Foto dapat dilihat di: {photo_info['view_url']}"
                
                return True, success_message
            else:
                return False, "❌ Gagal menyimpan laporan ke semua sistem"
                
        except Exception as e:
            print(f"❌ CRITICAL Error in submit_report: {e}")
            traceback.print_exc()
            
            # Cleanup: Hapus foto dari Google Drive jika upload gagal
            if photo_info and 'file_id' in photo_info:
                try:
                    self.drive_model.delete_file(photo_info['file_id'])
                except:
                    pass
            
            return False, f"❌ Error sistem: {str(e)}"
    
    def _handle_photo_upload_drive(self, photo_file):
        """Upload photo ke Google Drive"""
        try:
            # Validasi file
            file_extension = photo_file.name.split('.')[-1].lower()
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            
            if file_extension not in valid_extensions:
                print(f"❌ Invalid file extension: {file_extension}")
                return False
            
            # Check file size (max 5MB)
            photo_file.seek(0, os.SEEK_END)
            file_size = photo_file.tell()
            photo_file.seek(0)
            
            if file_size > 5 * 1024 * 1024:
                print("❌ File too large (max 5MB)")
                return False
            
            # Baca file bytes
            file_bytes = photo_file.getbuffer().tobytes()
            
            # Generate unique filename
            filename = f"{uuid.uuid4()}.{file_extension}"
            
            # Upload ke Google Drive
            if self.drive_model and self.drive_model.service:
                upload_result = self.drive_model.upload_photo(file_bytes, filename)
                
                if upload_result:
                    print(f"✅ Photo uploaded to Google Drive: {upload_result['view_url']}")
                    return upload_result
                else:
                    print("❌ Google Drive upload failed")
                    return None
            else:
                print("⚠️ Google Drive not available")
                return None
                
        except Exception as e:
            print(f"❌ Error in photo upload: {e}")
            return None
    
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
    
    # ============ FUNGSI UNTUK VIEWS ============
    
    def get_today_reports(self):
        """Get today's flood reports"""
        try:
            return self.flood_model.get_today_reports()
        except Exception as e:
            print(f"⚠️ Error getting today reports: {e}")
            return []
    
    def get_month_reports(self):
        """Get this month's flood reports"""
        try:
            return self.flood_model.get_month_reports()
        except Exception as e:
            print(f"⚠️ Error getting month reports: {e}")
            return []
    
    def get_all_reports(self):
        """Get all flood reports"""
        try:
            return self.flood_model.get_all_reports()
        except Exception as e:
            print(f"⚠️ Error getting all reports: {e}")
            return []
    
    def get_monthly_statistics(self):
        """Get monthly statistics for reports"""
        try:
            return self.flood_model.get_monthly_statistics()
        except Exception as e:
            print(f"⚠️ Error getting statistics: {e}")
            return {'total_reports': 0, 'month': ''}
    
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
    
    def is_google_sheets_available(self):
        """Check if Google Sheets is available"""
        return (self.sheets_model is not None and 
                hasattr(self.sheets_model, 'client') and 
                self.sheets_model.client is not None)
    
    def is_google_drive_available(self):
        """Check if Google Drive is available"""
        return (self.drive_model is not None and 
                self.drive_model.service is not None)
