import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import json
import os

class GoogleSheetsModel:
    def __init__(self):
        """Initialize Google Sheets connection"""
        self.setup_connection()
    
    def setup_connection(self):
        """Setup connection to Google Sheets"""
        try:
            # Scope yang diperlukan
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Dapatkan credentials dari Streamlit Secrets atau file lokal
            creds = None
            
            if 'GOOGLE_SHEETS' in st.secrets:
                # Jika di Streamlit Cloud (pakai secrets)
                credentials_dict = {
                    "type": "service_account",
                    "project_id": st.secrets["GOOGLE_SHEETS"]["project_id"],
                    "private_key_id": st.secrets["GOOGLE_SHEETS"]["private_key_id"],
                    "private_key": st.secrets["GOOGLE_SHEETS"]["private_key"].replace('\\n', '\n'),
                    "client_email": st.secrets["GOOGLE_SHEETS"]["client_email"],
                    "client_id": st.secrets["GOOGLE_SHEETS"]["client_id"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": st.secrets["GOOGLE_SHEETS"]["client_x509_cert_url"]
                }
                creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
            elif os.path.exists('credentials.json'):
                # Jika lokal (pakai file credentials.json)
                creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
            else:
                print("⚠️ Google Sheets credentials tidak ditemukan")
                self.client = None
                return
            
            # Authorize client
            self.client = gspread.authorize(creds)
            
            # Buka spreadsheet (ID dari secrets atau hardcode)
            spreadsheet_id = st.secrets.get("GOOGLE_SHEETS", {}).get("SPREADSHEET_ID", "YOUR_SPREADSHEET_ID_HERE")
            self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            
            print("✅ Google Sheets connected successfully")
            
        except Exception as e:
            print(f"❌ Error connecting to Google Sheets: {e}")
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
        """Save flood report to Google Sheets"""
        try:
            ws = self.get_worksheet("flood_reports")
            if not ws:
                print("❌ Worksheet 'flood_reports' not found")
                return False
            
            # Prepare data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [
                timestamp,                           # Timestamp
                report_data.get('address', ''),      # Alamat
                report_data.get('flood_height', ''), # Tinggi Banjir
                report_data.get('reporter_name', ''), # Nama Pelapor
                report_data.get('reporter_phone', ''), # No HP
                report_data.get('ip_address', ''),   # IP Address
                report_data.get('photo_url', ''),    # Photo URL
                'pending'                           # Status
            ]
            
            # Append to sheet
            ws.append_row(row)
            print(f"✅ Report saved to Google Sheets at {timestamp}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving to Google Sheets: {e}")
            return False
    
    def get_recent_reports(self, limit=100):
        """Get recent flood reports from Google Sheets"""
        try:
            ws = self.get_worksheet("flood_reports")
            if not ws:
                return []
            
            # Get all data (skip header row)
            all_data = ws.get_all_values()
            if len(all_data) <= 1:  # Only header or empty
                return []
            
            # Convert to list of dictionaries
            headers = all_data[0]
            rows = all_data[1:]  # Skip header
            
            # Get latest reports (reverse order)
            recent_rows = rows[-limit:] if len(rows) > limit else rows
            recent_rows.reverse()  # Newest first
            
            reports = []
            for row in recent_rows:
                report = {headers[i]: row[i] if i < len(row) else '' for i in range(len(headers))}
                reports.append(report)
            
            return reports
            
        except Exception as e:
            print(f"❌ Error getting reports from Google Sheets: {e}")
            return []
    
    def save_prediction(self, prediction_data):
        """Save prediction data to Google Sheets"""
        try:
            ws = self.get_worksheet("predictions")
            if not ws:
                return False
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [
                timestamp,
                prediction_data.get('location', ''),
                prediction_data.get('rainfall', 0),
                prediction_data.get('water_level', 0),
                prediction_data.get('humidity', 0),
                prediction_data.get('temp_min', 0),
                prediction_data.get('temp_max', 0),
                prediction_data.get('risk_level', 0),
                prediction_data.get('status', ''),
                prediction_data.get('message', '')
            ]
            
            ws.append_row(row)
            print(f"✅ Prediction saved to Google Sheets")
            return True
            
        except Exception as e:
            print(f"❌ Error saving prediction: {e}")
            return False
    
    def update_statistics(self, stats_data):
        """Update monthly statistics in Google Sheets"""
        try:
            ws = self.get_worksheet("monthly_stats")
            if not ws:
                return False
            
            current_month = datetime.now().strftime("%Y-%m")
            
            # Cek apakah bulan ini sudah ada
            all_data = ws.get_all_values()
            month_exists = False
            
            for i, row in enumerate(all_data):
                if i == 0:  # Skip header
                    continue
                if row and row[0] == current_month:
                    # Update existing row
                    ws.update(f'A{i+1}:D{i+1}', [[
                        current_month,
                        stats_data.get('total_reports', 0),
                        stats_data.get('avg_risk', 0),
                        stats_data.get('high_risk_days', 0)
                    ]])
                    month_exists = True
                    break
            
            if not month_exists:
                # Add new row
                ws.append_row([
                    current_month,
                    stats_data.get('total_reports', 0),
                    stats_data.get('avg_risk', 0),
                    stats_data.get('high_risk_days', 0)
                ])
            
            print(f"✅ Statistics updated for {current_month}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating statistics: {e}")
            return False
