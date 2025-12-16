import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import os
import json

class GoogleSheetsModel:
    def __init__(self):
        """Initialize Google Sheets connection"""
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self.setup_connection()
    
    def setup_connection(self):
        """Setup connection to Google Sheets with multiple fallbacks"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = None
            
            # OPTION 1: Streamlit Secrets (for Streamlit Cloud)
            if 'GOOGLE_SHEETS' in st.secrets:
                print("🔑 Using Streamlit secrets for Google Sheets")
                secrets = st.secrets["GOOGLE_SHEETS"]
                
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
                spreadsheet_id = secrets.get("SPREADSHEET_ID")
            
            # OPTION 2: Local credentials.json file
            elif os.path.exists('credentials.json'):
                print("🔑 Using local credentials.json")
                creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
                
                # Get spreadsheet ID from secrets or default
                if 'GOOGLE_SHEETS' in st.secrets:
                    spreadsheet_id = st.secrets["GOOGLE_SHEETS"].get("SPREADSHEET_ID")
                else:
                    # Default spreadsheet ID (replace with yours)
                    spreadsheet_id = "1wdys3GzfDfl0ohCQjUHRyJVbKQcM0VSIMgCryHB0-mc"
            
            else:
                print("❌ No Google Sheets credentials found")
                return
            
            # Authorize client
            self.client = gspread.authorize(creds)
            print("✅ Google Sheets API authorized")
            
            # Open spreadsheet
            if not spreadsheet_id:
                print("❌ No spreadsheet ID provided")
                return
            
            self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            print(f"✅ Spreadsheet opened: {self.spreadsheet.title}")
            
            # Get or create worksheet
            self.worksheet = self.get_or_create_worksheet("flood_reports")
            if self.worksheet:
                print(f"✅ Worksheet ready: {self.worksheet.title}")
                print(f"📊 Current rows: {self.worksheet.row_count}")
            
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            import traceback
            traceback.print_exc()
            self.client = None
    
    def get_or_create_worksheet(self, sheet_name):
        """Get existing worksheet or create new one with headers"""
        try:
            # Try to get existing worksheet
            worksheet = self.spreadsheet.worksheet(sheet_name)
            print(f"✅ Existing worksheet found: {sheet_name}")
            
            # Ensure headers exist
            headers = worksheet.row_values(1)
            expected_headers = ["Timestamp", "Alamat", "Tinggi Banjir", "Nama Pelapor", 
                              "No HP", "IP Address", "Photo URL", "Status"]
            
            if not headers or len(headers) < 8:
                print("⚠️ Worksheet missing headers, adding...")
                worksheet.insert_row(expected_headers, 1)
            
            return worksheet
            
        except gspread.exceptions.WorksheetNotFound:
            print(f"⚠️ Worksheet '{sheet_name}' not found, creating...")
            try:
                # Create new worksheet
                worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=10)
                
                # Add headers
                headers = ["Timestamp", "Alamat", "Tinggi Banjir", "Nama Pelapor", 
                          "No HP", "IP Address", "Photo URL", "Status"]
                worksheet.insert_row(headers, 1)
                
                print(f"✅ New worksheet created: {sheet_name}")
                return worksheet
                
            except Exception as e:
                print(f"❌ Error creating worksheet: {e}")
                return None
    
    def save_flood_report(self, report_data):
        """Save flood report to Google Sheets"""
        try:
            if not self.worksheet:
                print("❌ Worksheet not available")
                return False
            
            # Prepare data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            row = [
                timestamp,  # Timestamp
                report_data.get('address', ''),
                report_data.get('flood_height', ''),
                report_data.get('reporter_name', ''),
                report_data.get('reporter_phone', ''),
                report_data.get('ip_address', ''),
                report_data.get('photo_url', ''),
                'pending'  # Status
            ]
            
            print(f"📊 Saving to Google Sheets: {row[1]} by {row[3]}")
            
            # Append row
            self.worksheet.append_row(row)
            
            # Get updated count
            all_values = self.worksheet.get_all_values()
            print(f"✅ Saved! Total rows: {len(all_values)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving to Google Sheets: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_recent_reports(self, limit=50):
        """Get recent reports from Google Sheets"""
        try:
            if not self.worksheet:
                return []
            
            all_values = self.worksheet.get_all_values()
            if len(all_values) <= 1:  # Only headers or empty
                return []
            
            # Skip header row and get recent rows
            data_rows = all_values[1:][-limit:] if len(all_values) > 1 else []
            
            reports = []
            for row in data_rows:
                if len(row) >= 8:
                    reports.append({
                        'timestamp': row[0],
                        'address': row[1],
                        'flood_height': row[2],
                        'reporter_name': row[3],
                        'reporter_phone': row[4],
                        'ip_address': row[5],
                        'photo_url': row[6],
                        'status': row[7]
                    })
            
            return reports
            
        except Exception as e:
            print(f"❌ Error getting reports from Google Sheets: {e}")
            return []
