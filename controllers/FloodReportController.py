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
            if self.sheets_model and self.sheets_model.client:
                print("✅ Google Sheets CONNECTED successfully")
                print(f"📊 Spreadsheet: {self.sheets_model.spreadsheet.title if self.sheets_model.spreadsheet else 'None'}")
            else:
                print("❌ Google Sheets model created but CLIENT is None")
                print("ℹ️ Check: credentials, spreadsheet ID, or permissions")
        except Exception as e:
            print(f"❌ Google Sheets initialization ERROR: {e}")
            self.sheets_model = None
            
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
        """Submit new flood report dengan Google Sheets integration"""
        photo_path = None
        photo_url = None
        
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
                    photo_url = f"uploads/{filename}"  # Simpan path relatif
                    
                except Exception as e:
                    print(f"❌ Error saving photo: {e}")
                    photo_path = None
                    photo_url = None
            
            # Create report in SQLite database
            print("💾 Saving report to SQLite database...")
            report_id = self.flood_model.create_report(
                address=address,
                flood_height=flood_height,
                reporter_name=reporter_name,
                reporter_phone=reporter_phone,
                photo_path=photo_path,
                ip_address=client_ip
            )
            
            if report_id:
                print(f"✅ Report saved to SQLite with ID: {report_id}")
                
                # ========== SIMPAN KE GOOGLE SHEETS ==========
                if self.sheets_model and self.sheets_model.client:
                    try:
                        print("☁️ Saving report to Google Sheets...")
                        
                        # Prepare data for Google Sheets
                        sheets_data = {
                            'address': address,
                            'flood_height': flood_height,
                            'reporter_name': reporter_name,
                            'reporter_phone': reporter_phone or '',
                            'ip_address': client_ip,
                            'photo_url': photo_url or ''
                        }
                        
                        # Save to Google Sheets
                        sheets_success = self.sheets_model.save_flood_report(sheets_data)
                        
                        if sheets_success:
                            print("✅ Report also saved to Google Sheets!")
                        else:
                            print("⚠️ Report saved to SQLite but failed to save to Google Sheets")
                            
                    except Exception as e:
                        print(f"⚠️ Error saving to Google Sheets: {e}")
                        # Lanjutkan meski Google Sheets error
                else:
                    print("ℹ️ Google Sheets not available, saving to SQLite only")
                # ========== END GOOGLE SHEETS ==========
                
                # Cek count setelah submit
                new_count = self.flood_model.get_today_reports_count_by_ip(client_ip)
                print(f"📊 Updated count after submit: {new_count}/10")
                
                return True, "✅ Laporan berhasil dikirim ke sistem!"
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
    
    # ========== FUNGSI UNTUK PREDIKSI ==========
    
    def save_prediction_to_sheets(self, prediction_data):
        """Save prediction data to Google Sheets"""
        if self.sheets_model and self.sheets_model.client:
            try:
                success = self.sheets_model.save_prediction(prediction_data)
                return success
            except Exception as e:
                print(f"❌ Error saving prediction to Google Sheets: {e}")
                return False
        return False
    
    def update_monthly_statistics(self):
        """Update monthly statistics in Google Sheets"""
        if self.sheets_model and self.sheets_model.client:
            try:
                # Hitung statistik sederhana
                current_month = datetime.now().strftime("%Y-%m")
                reports = self.flood_model.get_month_reports()
                total_reports = len(reports)
                
                stats_data = {
                    'total_reports': total_reports,
                    'avg_risk': 0.35,  # Contoh, bisa dihitung dari prediksi
                    'high_risk_days': 0,
                    'most_affected_area': self.get_most_affected_area(),
                    'response_time_avg': 45
                }
                
                success = self.sheets_model.update_statistics(stats_data)
                return success
            except Exception as e:
                print(f"❌ Error updating monthly statistics: {e}")
                return False
        return False
    
    def get_most_affected_area(self):
        """Get most affected area from reports"""
        try:
            reports = self.flood_model.get_month_reports()
            if not reports:
                return "Tidak ada data"
            
            # Simple logic: count by address
            address_count = {}
            for report in reports:
                addr = report.get('address', '')
                if addr:
                    address_count[addr] = address_count.get(addr, 0) + 1
            
            if address_count:
                return max(address_count, key=address_count.get)[:50]  # Limit length
            return "Tidak terdeteksi"
        except:
            return "Error"
    
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
    
    def get_google_sheets_stats(self):
        """Get statistics from Google Sheets"""
        if self.sheets_model:
            return self.sheets_model.get_statistics()
        return {}
    
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

