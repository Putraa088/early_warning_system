import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import os

class GoogleSheetsModel:
    def __init__(self):
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self.setup_connection()
    
    def setup_connection(self):
        """Setup connection to Google Sheets"""
        try:
            # ... [existing setup code remains the same]
            
            # After connecting, ensure worksheet has Base64 column
            self.worksheet = self.get_or_create_worksheet_with_base64("flood_reports")
            
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            self.client = None
    
    def get_or_create_worksheet_with_base64(self, sheet_name):
        """Get existing worksheet or create new one with Base64 column"""
        try:
            # Try to get existing worksheet
            worksheet = self.spreadsheet.worksheet(sheet_name)
            print(f"✅ Existing worksheet found: {sheet_name}")
            
            # Check if Base64 column exists (column I)
            headers = worksheet.row_values(1)
            expected_headers = [
                "Timestamp", "Alamat", "Tinggi Banjir", "Nama Pelapor", 
                "No HP", "IP Address", "Photo Filename", "Photo Base64", "Status"
            ]
            
            if not headers or len(headers) < 9:
                print("⚠️ Worksheet missing headers, adding with Base64 column...")
                worksheet.clear()
                worksheet.insert_row(expected_headers, 1)
            
            return worksheet
            
        except gspread.exceptions.WorksheetNotFound:
            print(f"⚠️ Worksheet '{sheet_name}' not found, creating with Base64 column...")
            try:
                # Create new worksheet with 9 columns (A-I)
                worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=9)
                
                # Add headers including Base64 column
                headers = [
                    "Timestamp", "Alamat", "Tinggi Banjir", "Nama Pelapor", 
                    "No HP", "IP Address", "Photo Filename", "Photo Base64", "Status"
                ]
                worksheet.insert_row(headers, 1)
                
                print(f"✅ New worksheet created with Base64 column: {sheet_name}")
                return worksheet
                
            except Exception as e:
                print(f"❌ Error creating worksheet: {e}")
                return None
    
    def save_flood_report(self, report_data):
        """Save flood report to Google Sheets with Base64 photo"""
        try:
            if not self.worksheet:
                print("❌ Worksheet not available")
                return False
            
            # Prepare data row with Base64
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Get Base64 string (truncate if too long)
            photo_base64 = report_data.get('photo_base64', '')
            if photo_base64 and len(photo_base64) > 45000:
                photo_base64 = photo_base64[:45000] + "...[TRUNCATED]"
                print(f"⚠️ Base64 truncated to {len(photo_base64)} chars")
            
            row = [
                timestamp,  # A: Timestamp
                report_data.get('address', ''),  # B: Alamat
                report_data.get('flood_height', ''),  # C: Tinggi Banjir
                report_data.get('reporter_name', ''),  # D: Nama Pelapor
                report_data.get('reporter_phone', ''),  # E: No HP
                report_data.get('ip_address', ''),  # F: IP Address
                report_data.get('photo_filename', ''),  # G: Photo Filename
                photo_base64,  # H: Photo Base64 (NEW COLUMN)
                'pending'  # I: Status
            ]
            
            print(f"📊 Saving to Google Sheets with Base64: {row[1]} by {row[3]}")
            print(f"   Base64 length: {len(photo_base64)} characters")
            
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
        """Get recent reports from Google Sheets with Base64"""
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
                if len(row) >= 9:  # Now 9 columns with Base64
                    reports.append({
                        'timestamp': row[0],
                        'address': row[1],
                        'flood_height': row[2],
                        'reporter_name': row[3],
                        'reporter_phone': row[4],
                        'ip_address': row[5],
                        'photo_filename': row[6],
                        'photo_base64': row[7],  # Base64 string
                        'status': row[8]
                    })
            
            print(f"📊 Retrieved {len(reports)} reports with Base64 photos")
            return reports
            
        except Exception as e:
            print(f"❌ Error getting reports from Google Sheets: {e}")
            return []
