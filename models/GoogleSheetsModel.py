import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone, timedelta
import streamlit as st
import os

class GoogleSheetsModel:
    def __init__(self):
        """Initialize Google Sheets connection"""
        self.client = None
        self.spreadsheet = None
        self.setup_connection()
    
    def setup_connection(self):
        """Setup connection to Google Sheets"""
        try:
            # Scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = None
            
            # Streamlit Secrets
            if 'GOOGLE_SHEETS' in st.secrets:
                secrets = st.secrets["GOOGLE_SHEETS"]
                
                # Check required keys
                required = ['project_id', 'private_key_id', 'private_key', 'client_email', 'SPREADSHEET_ID']
                if not all(key in secrets for key in required):
                    print("❌ Missing required keys in secrets")
                    return
                
                credentials_dict = {
                    "type": "service_account",
                    "project_id": secrets["project_id"],
                    "private_key_id": secrets["private_key_id"],
                    "private_key": secrets["private_key"].replace('\\n', '\n'),
                    "client_email": secrets["client_email"],
                    "client_id": secrets.get("client_id", ""),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": secrets.get("client_x509_cert_url", "")
                }
                creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
            
            elif os.path.exists('credentials.json'):
                creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
            else:
                return
            
            # Authorize
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            spreadsheet_id = st.secrets["GOOGLE_SHEETS"]["SPREADSHEET_ID"]
            self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            
            print(f"✅ Google Sheets connected: {self.spreadsheet.title}")
            
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            self.client = None
            self.spreadsheet = None
    
    def get_worksheet(self, sheet_name="flood_reports"):
        """Get worksheet by name"""
        if not self.spreadsheet:
            return None
        
        try:
            return self.spreadsheet.worksheet(sheet_name)
        except:
            return None
    
    def get_wib_time(self):
        """Get current time in WIB (UTC+7)"""
        # Get UTC time
        utc_now = datetime.now(timezone.utc)
        # Convert to WIB (UTC+7)
        wib_time = utc_now + timedelta(hours=7)
        return wib_time
    
    # ========== HANYA UNTUK TAB 1: flood_reports ==========
    
    def save_flood_report(self, report_data):
        """Save flood report to Google Sheets TAB 1 dengan waktu WIB"""
        try:
            ws = self.get_worksheet("flood_reports")
            if not ws:
                print("❌ Worksheet 'flood_reports' not found")
                return False
            
            # Prepare data row dengan waktu WIB
            wib_time = self.get_wib_time()
            timestamp = wib_time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Sesuai format kolom yang diminta:
            # timestamp, alamat, tinggi banjir, nama pelapor, no hp, ip address, photo url, status
            row = [
                timestamp,  # Kolom 1: timestamp (WIB)
                report_data.get('address', ''),  # Kolom 2: alamat
                report_data.get('flood_height', ''),  # Kolom 3: tinggi banjir
                report_data.get('reporter_name', ''),  # Kolom 4: nama pelapor
                report_data.get('reporter_phone', ''),  # Kolom 5: no hp
                report_data.get('ip_address', ''),  # Kolom 6: ip address
                report_data.get('photo_url', ''),  # Kolom 7: photo url
                'pending'  # Kolom 8: status
            ]
            
            # Append to sheet
            ws.append_row(row)
            print(f"✅ Report saved to Google Sheets at {timestamp} WIB")
            return True
            
        except Exception as e:
            print(f"❌ Error saving flood report: {e}")
            return False
