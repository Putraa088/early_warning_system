import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import os
import pytz
import json
import sys

class GoogleSheetsModel:
    def __init__(self):
        """Initialize Google Sheets connection"""
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self.tz_wib = pytz.timezone('Asia/Jakarta')
        self.setup_connection()
    
    def setup_connection(self):
        """Setup Google Sheets connection dengan safe access ke st.secrets"""
        try:
            print("🔄 Setting up Google Sheets connection...")
            
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials_data = None
            
            # ============ OPTION 1: Streamlit Secrets (Cloud) ============
            # Gunakan try-except untuk handle session state yang belum siap
            try:
                # Cek apakah st.secrets sudah tersedia
                if hasattr(st, 'secrets') and 'GOOGLE_SHEETS' in st.secrets:
                    print("🔑 Using Streamlit Secrets for Google Sheets")
                    gs_secrets = st.secrets['GOOGLE_SHEETS']
                    
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
                    
                    # Get spreadsheet ID dari secrets
                    spreadsheet_id = gs_secrets.get('SPREADSHEET_ID', '1wdys3GzfDfl0ohCQjUHRyJVbKQcM0VSIMgCryHB0-mc')
                    
            except Exception as secrets_error:
                print(f"⚠️ Error accessing Streamlit Secrets: {secrets_error}")
                print("🔄 Trying credentials.json...")
            
            # ============ OPTION 2: credentials.json (Local Development) ============
            if not credentials_data and os.path.exists('credentials.json'):
                try:
                    print("🔑 Using credentials.json (local development)")
                    with open('credentials.json', 'r') as f:
                        credentials_data = json.load(f)
                    print(f"✅ Loaded from credentials.json: {credentials_data['client_email']}")
                    
                    # Gunakan default spreadsheet ID untuk local
                    spreadsheet_id = "1wdys3GzfDfl0ohCQjUHRyJVbKQcM0VSIMgCryHB0-mc"
                    
                except Exception as file_error:
                    print(f"❌ Error reading credentials.json: {file_error}")
            
            # ============ FALLBACK: Use environment variable ============
            if not credentials_data:
                print("❌ No Google Sheets credentials found")
                print("⚠️ Google Sheets will be offline")
                self.client = None
                return
            
            # Authorize dengan credentials
            creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_data, scope)
            self.client = gspread.authorize(creds)
            print("✅ Google Sheets API authorized")
            
            # Open spreadsheet
            self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            print(f"✅ Spreadsheet opened: {self.spreadsheet.title}")
            
            # Get worksheet
            try:
                self.worksheet = self.spreadsheet.worksheet('flood_reports')
                print(f"✅ Worksheet ready: {self.worksheet.title}")
                print(f"📊 Current rows: {self.worksheet.row_count}")
            except gspread.exceptions.WorksheetNotFound:
                print("⚠️ Worksheet 'flood_reports' not found, creating...")
                self._create_worksheet_with_headers()
            except Exception as e:
                print(f"⚠️ Error getting worksheet: {e}")
                self.worksheet = None
            
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            print("⚠️ Google Sheets offline - using SQLite only")
            self.client = None
    
    def _create_worksheet_with_headers(self):
        """Create worksheet dengan headers"""
        try:
            self.worksheet = self.spreadsheet.add_worksheet(
                title='flood_reports', 
                rows=1000, 
                cols=8
            )
            
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
            self.worksheet = None
    
    def save_flood_report(self, report_data):
        """Save report to Google Sheets"""
        try:
            if not self.worksheet:
                print("❌ Worksheet not available")
                return False
            
            # Waktu WIB
            current_time_wib = datetime.now(self.tz_wib)
            timestamp_wib = current_time_wib.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"📊 Saving to Google Sheets...")
            
            # Row data
            row = [
                timestamp_wib,                      # A: Timestamp
                str(report_data.get('address', '')),     # B: Alamat
                str(report_data.get('flood_height', '')), # C: Tinggi Banjir
                str(report_data.get('reporter_name', '')), # D: Nama Pelapor
                str(report_data.get('reporter_phone', '')), # E: No HP
                str(report_data.get('ip_address', '')),   # F: IP Address
                str(report_data.get('photo_url', '')),    # G: Photo URL
                'pending'                           # H: Status
            ]
            
            print(f"📊 Data to save: {row[1]} by {row[3]}")
            
            # Append row
            self.worksheet.append_row(row)
            print("✅ Saved to Google Sheets!")
            return True
            
        except Exception as e:
            print(f"❌ Error saving to Google Sheets: {e}")
            return False
