import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import os
import pytz
import time
import socket
import json

class GoogleSheetsModel:
    def __init__(self):
        """Initialize Google Sheets connection untuk Streamlit Cloud dan Local"""
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self.tz_wib = pytz.timezone('Asia/Jakarta')
        self.max_retries = 3
        self.retry_delay = 2
        self.setup_connection()
    
    def setup_connection(self):
        """Setup Google Sheets connection dengan Streamlit Secrets atau file lokal"""
        for attempt in range(self.max_retries):
            try:
                print(f"🔄 Setting up Google Sheets connection (Attempt {attempt + 1}/{self.max_retries})...")
                
                scope = [
                    'https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive'
                ]
                
                credentials_data = None
                
                # ============ OPTION 1: Streamlit Secrets (Cloud) ============
                if 'GOOGLE_SHEETS' in st.secrets:
                    print("🔑 Using Streamlit Secrets for Google Sheets")
                    gs_secrets = st.secrets['GOOGLE_SHEETS']
                    
                    # Bangun credentials dictionary dari secrets
                    credentials_data = {
                        "type": "service_account",
                        "project_id": gs_secrets.get('project_id', ''),
                        "private_key_id": gs_secrets.get('private_key_id', ''),
                        "private_key": gs_secrets.get('private_key', '').replace('\\n', '\n'),
                        "client_email": gs_secrets.get('client_email', ''),
                        "client_id": gs_secrets.get('client_id', ''),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "client_x509_cert_url": gs_secrets.get('client_x509_cert_url', '')
                    }
                    
                    print(f"✅ Loaded from Streamlit Secrets: {credentials_data['client_email']}")
                
                # ============ OPTION 2: credentials.json (Local Development) ============
                elif os.path.exists('credentials.json'):
                    print("🔑 Using credentials.json (local development)")
                    with open('credentials.json', 'r') as f:
                        credentials_data = json.load(f)
                    print(f"✅ Loaded from credentials.json: {credentials_data['client_email']}")
                
                else:
                    print("❌ No Google Sheets credentials found")
                    print("   Streamlit Secrets not set and credentials.json not found")
                    self.client = None
                    return
                
                # Set socket timeout untuk mencegah hang
                socket.setdefaulttimeout(30)
                
                # Authorize dengan credentials
                creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_data, scope)
                self.client = gspread.authorize(creds)
                print("✅ Google Sheets API authorized")
                
                # Get spreadsheet ID dari secrets atau gunakan default
                spreadsheet_id = None
                
                # Coba dari Streamlit Secrets
                if 'GOOGLE_SHEETS' in st.secrets and 'SPREADSHEET_ID' in st.secrets['GOOGLE_SHEETS']:
                    spreadsheet_id = st.secrets['GOOGLE_SHEETS']['SPREADSHEET_ID']
                    print(f"📊 Using Spreadsheet ID from secrets")
                
                # Fallback ke default ID
                if not spreadsheet_id:
                    spreadsheet_id = "1wdys3GzfDfl0ohCQjUHRyJVbKQcM0VSIMgCryHB0-mc"
                    print(f"📊 Using default Spreadsheet ID: {spreadsheet_id}")
                
                # Open spreadsheet
                self.spreadsheet = self.client.open_by_key(spreadsheet_id)
                print(f"✅ Spreadsheet opened: {self.spreadsheet.title}")
                
                # Get atau buat worksheet 'flood_reports'
                try:
                    self.worksheet = self.spreadsheet.worksheet('flood_reports')
                    print(f"✅ Worksheet found: {self.worksheet.title}")
                    print(f"📊 Current rows: {self.worksheet.row_count}")
                    
                    # Cek headers
                    headers = self.worksheet.row_values(1)
                    expected_headers = ["Timestamp", "Alamat", "Tinggi Banjir", "Nama Pelapor", 
                                       "No HP", "IP Address", "Photo URL", "Status"]
                    
                    if len(headers) < 8 or headers[:8] != expected_headers:
                        print("⚠️ Headers tidak sesuai, memperbaiki...")
                        self._fix_worksheet_headers()
                    
                except gspread.exceptions.WorksheetNotFound:
                    print("⚠️ Worksheet 'flood_reports' not found, creating...")
                    self._create_worksheet_with_headers()
                
                # Reset timeout
                socket.setdefaulttimeout(None)
                print("🎉 Google Sheets connection successful!")
                return  # Exit jika berhasil
                    
            except socket.timeout as e:
                print(f"⚠️ Timeout on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    print("❌ Max retries reached, Google Sheets offline")
                    self.client = None
                    
            except ConnectionError as e:
                print(f"⚠️ Connection error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    print("❌ Connection failed after retries")
                    self.client = None
                    
            except Exception as e:
                print(f"❌ Google Sheets connection failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    print("⚠️ Google Sheets offline - using SQLite only")
                    self.client = None
    
    def _create_worksheet_with_headers(self):
        """Create worksheet dengan headers yang benar"""
        try:
            # Add new worksheet
            self.worksheet = self.spreadsheet.add_worksheet(
                title='flood_reports', 
                rows=1000, 
                cols=8
            )
            
            # Add headers
            headers = [
                "Timestamp", 
                "Alamat", 
                "Tinggi Banjir", 
                "Nama Pelapor", 
                "No HP", 
                "IP Address", 
                "Photo URL", 
                "Status"
            ]
            
            self.worksheet.insert_row(headers, 1)
            print(f"✅ Created worksheet 'flood_reports' with headers")
            
        except Exception as e:
            print(f"❌ Error creating worksheet: {e}")
            # Coba worksheet yang sudah ada
            try:
                self.worksheet = self.spreadsheet.sheet1
                print(f"✅ Using existing sheet: {self.worksheet.title}")
            except:
                self.worksheet = None
    
    def _fix_worksheet_headers(self):
        """Fix worksheet headers jika tidak sesuai"""
        try:
            # Clear existing data (keep first row)
            all_data = self.worksheet.get_all_values()
            if len(all_data) > 1:
                # Keep only first row
                self.worksheet.clear()
            
            # Insert correct headers
            headers = [
                "Timestamp", 
                "Alamat", 
                "Tinggi Banjir", 
                "Nama Pelapor", 
                "No HP", 
                "IP Address", 
                "Photo URL", 
                "Status"
            ]
            self.worksheet.insert_row(headers, 1)
            print("✅ Fixed worksheet headers")
            
        except Exception as e:
            print(f"❌ Error fixing headers: {e}")
    
    def save_flood_report(self, report_data):
        """Save report to Google Sheets dengan hyperlink untuk foto"""
        if not self.worksheet:
            print("❌ Worksheet not available, trying to reconnect...")
            self.setup_connection()
            if not self.worksheet:
                print("❌ Still cannot connect to worksheet")
                return False
        
        for attempt in range(self.max_retries):
            try:
                # Waktu WIB
                current_time_wib = datetime.now(self.tz_wib)
                timestamp_wib = current_time_wib.strftime("%Y-%m-%d %H:%M:%S")
                
                print(f"📅 Attempt {attempt + 1}/{self.max_retries}: Saving to Google Sheets...")
                
                # ============ PHOTO URL PROCESSING ============
                photo_url = str(report_data.get('photo_url', ''))
                
                # Format photo URL untuk Google Sheets
                if photo_url:
                    if 'drive.google.com' in photo_url:
                        # Google Drive URL - buat hyperlink
                        photo_cell = f'=HYPERLINK("{photo_url}", "📷 Lihat Foto")'
                    elif photo_url.startswith('http'):
                        # Other HTTP URL - buat hyperlink
                        photo_cell = f'=HYPERLINK("{photo_url}", "📷 Link Foto")'
                    else:
                        # Local path atau filename saja
                        photo_cell = photo_url
                else:
                    photo_cell = 'Tidak ada foto'
                
                # ============ PREPARE ROW DATA ============
                row = [
                    timestamp_wib,                              # A: Timestamp (WIB)
                    str(report_data.get('address', '')).strip(),     # B: Alamat
                    str(report_data.get('flood_height', '')).strip(), # C: Tinggi Banjir
                    str(report_data.get('reporter_name', '')).strip(), # D: Nama Pelapor
                    str(report_data.get('reporter_phone', '')).strip() if report_data.get('reporter_phone') else '', # E: No HP
                    str(report_data.get('ip_address', '')).strip(),   # F: IP Address
                    photo_cell,                                 # G: Photo URL (dengan hyperlink jika ada)
                    'pending'                                   # H: Status
                ]
                
                # Log data yang akan disimpan (tanpa URL panjang)
                log_data = row.copy()
                if len(log_data[6]) > 50:  # Potong URL panjang untuk log
                    log_data[6] = log_data[6][:50] + "..."
                
                print(f"📊 Saving to Google Sheets:")
                print(f"   📍 Alamat: {log_data[1]}")
                print(f"   👤 Pelapor: {log_data[3]}")
                print(f"   📅 Waktu: {log_data[0]}")
                print(f"   📸 Foto: {'Ya' if 'HYPERLINK' in row[6] or row[6] != 'Tidak ada foto' else 'Tidak'}")
                
                # Set timeout untuk operasi network
                socket.setdefaulttimeout(30)
                
                # Append row ke Google Sheets
                self.worksheet.append_row(row)
                
                # Reset timeout
                socket.setdefaulttimeout(None)
                
                print("✅ Successfully saved to Google Sheets!")
                
                # Verifikasi data tersimpan
                try:
                    all_values = self.worksheet.get_all_values()
                    last_row = all_values[-1] if all_values else []
                    if last_row and last_row[1] == row[1]:  # Cek alamat sama
                        print(f"✅ Verified: Data saved in row {len(all_values)}")
                except:
                    pass  # Skip verification jika error
                
                return True
                
            except socket.timeout as e:
                print(f"⚠️ Timeout saat menyimpan (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    print(f"🔄 Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    
                    # Reconnect
                    print("🔁 Reconnecting to Google Sheets...")
                    self.setup_connection()
                else:
                    print("❌ Timeout setelah semua percobaan")
                    socket.setdefaulttimeout(None)
                    return False
                    
            except ConnectionError as e:
                print(f"⚠️ Connection error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    print(f"🔄 Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    self.setup_connection()
                else:
                    print("❌ Connection failed setelah retries")
                    socket.setdefaulttimeout(None)
                    return False
                    
            except Exception as e:
                print(f"❌ Error saving to Google Sheets (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    print(f"🔄 Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    self.setup_connection()
                else:
                    print("❌ All attempts failed")
                    socket.setdefaulttimeout(None)
                    return False
        
        return False
    
    def get_recent_reports(self, limit=50):
        """Get recent reports dari Google Sheets"""
        for attempt in range(self.max_retries):
            try:
                if not self.worksheet:
                    return []
                
                socket.setdefaulttimeout(30)
                all_values = self.worksheet.get_all_values()
                socket.setdefaulttimeout(None)
                
                if len(all_values) <= 1:  # Hanya header
                    return []
                
                # Ambil data terbaru (exclude header)
                data_rows = all_values[1:][-limit:] if len(all_values) > 1 else []
                
                reports = []
                for i, row in enumerate(data_rows):
                    if len(row) >= 8:
                        # Parse hyperlink jika ada
                        photo_url = row[6]
                        if photo_url.startswith('=HYPERLINK('):
                            # Extract URL dari formula HYPERLINK
                            try:
                                # Format: =HYPERLINK("URL", "Teks")
                                url_start = photo_url.find('"') + 1
                                url_end = photo_url.find('"', url_start)
                                photo_url = photo_url[url_start:url_end]
                            except:
                                pass
                        
                        reports.append({
                            'row_number': i + 2,  # +2 karena header + 1-based index
                            'timestamp': row[0],
                            'address': row[1],
                            'flood_height': row[2],
                            'reporter_name': row[3],
                            'reporter_phone': row[4],
                            'ip_address': row[5],
                            'photo_url': photo_url,
                            'status': row[7] if len(row) > 7 else 'pending'
                        })
                
                print(f"✅ Retrieved {len(reports)} reports from Google Sheets")
                return reports
                
            except Exception as e:
                print(f"❌ Error getting reports (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    self.setup_connection()
                else:
                    return []
    
    def update_report_status(self, row_number, status):
        """Update status report di Google Sheets"""
        try:
            if not self.worksheet:
                return False
            
            # Kolom H adalah status (index 7, 0-based)
            self.worksheet.update_cell(row_number, 8, status)
            print(f"✅ Updated row {row_number} status to '{status}'")
            return True
            
        except Exception as e:
            print(f"❌ Error updating status: {e}")
            return False
    
    def is_connected(self):
        """Check if Google Sheets is connected"""
        return self.client is not None and self.worksheet is not None
    
    def get_worksheet_info(self):
        """Get worksheet information"""
        if not self.is_connected():
            return "Not connected"
        
        try:
            all_values = self.worksheet.get_all_values()
            row_count = len(all_values)
            data_count = max(0, row_count - 1)  # Exclude header
            
            return {
                'title': self.worksheet.title,
                'row_count': row_count,
                'data_count': data_count,
                'last_updated': datetime.now(self.tz_wib).strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            return f"Error: {str(e)}"
