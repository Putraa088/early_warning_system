import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
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
                print("❌ No Google Sheets credentials found")
                return
            
            # Authorize
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            spreadsheet_id = st.secrets["GOOGLE_SHEETS"]["SPREADSHEET_ID"]
            self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            
            print(f"✅ Google Sheets connected: {self.spreadsheet.title}")
            
            # Test connection
            ws = self.get_worksheet("flood_reports")
            if ws:
                print(f"✅ Worksheet found: {ws.title}")
                print(f"✅ Row count: {ws.row_count}, Col count: {ws.col_count}")
            else:
                print("❌ Worksheet 'flood_reports' not found")
            
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            self.client = None
            self.spreadsheet = None
    
    def get_worksheet(self, sheet_name):
        """Get worksheet by name"""
        if not self.spreadsheet:
            return None
        
        try:
            return self.spreadsheet.worksheet(sheet_name)
        except Exception as e:
            print(f"❌ Error getting worksheet '{sheet_name}': {e}")
            return None
    
    def save_flood_report(self, report_data):
        """Save flood report to Google Sheets - SESUAIKAN DENGAN KOLOM"""
        try:
            ws = self.get_worksheet("flood_reports")
            if not ws:
                print("❌ Worksheet 'flood_reports' not found")
                return False
            
            # Prepare data row sesuai dengan kolom di Google Sheets
            # Kolom: Timestamp | Alamat | Tinggi Banjir | Nama Pelapor | No HP | IP Address | Photo URL | Status
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            row = [
                timestamp,  # A: Timestamp
                report_data.get('address', ''),  # B: Alamat
                report_data.get('flood_height', ''),  # C: Tinggi Banjir
                report_data.get('reporter_name', ''),  # D: Nama Pelapor
                report_data.get('reporter_phone', ''),  # E: No HP
                report_data.get('ip_address', ''),  # F: IP Address
                report_data.get('photo_url', ''),  # G: Photo URL
                'pending'  # H: Status
            ]
            
            print(f"📊 Preparing Google Sheets row:")
            print(f"  A: Timestamp: {row[0]}")
            print(f"  B: Alamat: {row[1]}")
            print(f"  C: Tinggi Banjir: {row[2]}")
            print(f"  D: Nama Pelapor: {row[3]}")
            print(f"  E: No HP: {row[4]}")
            print(f"  F: IP Address: {row[5]}")
            print(f"  G: Photo URL: {row[6]}")
            print(f"  H: Status: {row[7]}")
            
            # Append to sheet
            ws.append_row(row)
            print("✅ Data appended to Google Sheets")
            
            # Verify the row was added
            all_values = ws.get_all_values()
            if all_values:
                last_row = all_values[-1]
                print(f"✅ Last row in sheet: {last_row}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving flood report to Google Sheets: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_recent_reports(self, limit=20):
        """Get recent reports from Google Sheets"""
        try:
            ws = self.get_worksheet("flood_reports")
            if not ws:
                return []
            
            # Get all values
            all_values = ws.get_all_values()
            if len(all_values) <= 1:  # Hanya header atau kosong
                return []
            
            # Skip header row
            data_rows = all_values[1:]  
            
            # Convert to list of dictionaries
            reports = []
            for row in data_rows[:limit]:
                if len(row) >= 8:  # Pastikan ada 8 kolom
                    reports.append({
                        'timestamp': row[0] if len(row) > 0 else '',
                        'address': row[1] if len(row) > 1 else '',
                        'flood_height': row[2] if len(row) > 2 else '',
                        'reporter_name': row[3] if len(row) > 3 else '',
                        'reporter_phone': row[4] if len(row) > 4 else '',
                        'ip_address': row[5] if len(row) > 5 else '',
                        'photo_url': row[6] if len(row) > 6 else '',
                        'status': row[7] if len(row) > 7 else ''
                    })
            
            return reports
            
        except Exception as e:
            print(f"❌ Error getting recent reports: {e}")
            return []
