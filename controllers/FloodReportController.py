from models.FloodReportModel import FloodReportModel
from models.GoogleSheetsModel import GoogleSheetsModel
import os
import uuid
from datetime import datetime
import streamlit as st
import traceback
import sqlite3
from datetime import timedelta

class FloodReportController:
    def __init__(self):
        self.flood_model = FloodReportModel()
        self.sheets_model = None
        self.upload_folder = "uploads"
        
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
        """Submit new flood report dengan struktur baru"""
        photo_url = None
        photo_filename = None
        
        try:
            client_ip = self.get_client_ip()
            print(f"🌐 Client IP: {client_ip}")
            
            if not self.check_daily_limit(client_ip):
                return False, "❌ Mohon maaf batas laporan harian telah mencapai batas, silahkan kembali lagi besok."
            
            if photo_file is not None:
                try:
                    file_extension = photo_file.name.split('.')[-1].lower()
                    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
                    
                    if file_extension not in valid_extensions:
                        return False, f"❌ Format file tidak didukung. Gunakan: {', '.join(valid_extensions)}"
                    
                    photo_filename = f"{uuid.uuid4()}.{file_extension}"
                    photo_path = os.path.join(self.upload_folder, photo_filename)
                    
                    print(f"📸 Saving photo to: {photo_path}")
                    
                    with open(photo_path, "wb") as f:
                        f.write(photo_file.getbuffer())
                    
                    photo_url = photo_path
                    print(f"✅ Photo saved: {photo_filename}")
                    
                except Exception as e:
                    print(f"⚠️ Error saving photo: {e}")
                    photo_url = None
                    photo_filename = None
            
            
            report_id = self.flood_model.create_report(
                alamat=address,  
                tinggi_banjir=flood_height,  
                nama_pelapor=reporter_name,  
                no_hp=reporter_phone,  
                photo_url=photo_url,  
                ip_address=client_ip  
            )
            
            if not report_id:
                print("❌ Failed to save to SQLite")
                if photo_url and os.path.exists(photo_url):
                    try:
                        os.remove(photo_url)
                    except:
                        pass
                return False, "❌ Gagal menyimpan laporan ke database lokal."
            
            if self.sheets_model and self.sheets_model.client:
                try:
                    print("📊 Saving to Google Sheets...")
                    
                    sheets_data = {
                        'address': str(address),
                        'flood_height': str(flood_height),
                        'reporter_name': str(reporter_name),
                        'reporter_phone': str(reporter_phone) if reporter_phone else '',
                        'ip_address': str(client_ip),
                        'photo_url': photo_url if photo_url else ''
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
            
            today_reports = self.flood_model.get_today_reports()
            print(f"✅ Verification: Total reports today = {len(today_reports)}")
            
            return True, f"✅ Informasi anda telah terkirim! Terimakasih atas laporannya."
                
        except Exception as e:
            print(f"❌ CRITICAL Error in submit_report: {e}")
            traceback.print_exc()
            
            if photo_url and os.path.exists(photo_url):
                try:
                    os.remove(photo_url)
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
    
    def get_yearly_statistics(self):
        """Get yearly flood report statistics for the last 12 months"""
        try:
            conn = sqlite3.connect('flood_system.db')
            cursor = conn.cursor()
            
            current_date = datetime.now()
            current_year_month = current_date.strftime('%Y-%m')
            
            months_data = []
            for i in range(11, -1, -1):  
                month_offset = i
                target_date = current_date - timedelta(days=30*month_offset)
                year_month = target_date.strftime('%Y-%m')
                month_name = target_date.strftime('%b')  
                
                query = """
                SELECT COUNT(*) as report_count
                FROM flood_reports 
                WHERE strftime('%Y-%m', report_date) = ?
                """
                
                cursor.execute(query, (year_month,))
                result = cursor.fetchone()
                report_count = result[0] if result else 0
                
                is_current = (year_month == current_year_month)
                
                months_data.append({
                    'year_month': year_month,
                    'month_name': month_name,
                    'report_count': report_count,
                    'is_current': is_current
                })
            
            conn.close()
            
            total_reports = sum(item['report_count'] for item in months_data)
            avg_per_month = total_reports / len(months_data) if months_data else 0
            
            if months_data:
                max_item = max(months_data, key=lambda x: x['report_count'])
                max_month = max_item['month_name']
                max_count = max_item['report_count']
            else:
                max_month = "Tidak ada data"
                max_count = 0
            
            return {
                'months_data': months_data,
                'total_reports': total_reports,
                'avg_per_month': round(avg_per_month, 1),
                'max_month': max_month,
                'max_count': max_count,
                'current_year_month': current_year_month
            }
            
        except Exception as e:
            print(f"❌ Error getting yearly statistics: {e}")
            traceback.print_exc()
            return {
                'months_data': [],
                'total_reports': 0,
                'avg_per_month': 0,
                'max_month': "Error",
                'max_count': 0,
                'current_year_month': ""
            }
    
    def get_client_ip(self):
        """Get client IP address"""
        try:
            if 'user_ip' not in st.session_state:
                import random
                st.session_state.user_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
            
            ip = st.session_state.user_ip
            print(f"🖥️ Using IP: {ip}")
            return ip
            
        except Exception as e:
            print(f"⚠️ Error getting IP: {e}")
            return "unknown_user"
