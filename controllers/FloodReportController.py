import base64
import uuid
import os
from datetime import datetime
import streamlit as st
from models.FloodReportModel import FloodReportModel
from models.GoogleSheetsModel import GoogleSheetsModel

class FloodReportController:
    def __init__(self):
        self.flood_model = FloodReportModel()
        self.sheets_model = None
        self.upload_folder = "uploads"
        
        # Initialize Google Sheets
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
        
        # Create upload folder
        self._ensure_upload_folder()
    
    def _ensure_upload_folder(self):
        """Ensure upload folder exists"""
        try:
            if not os.path.exists(self.upload_folder):
                os.makedirs(self.upload_folder)
                print(f"✅ Created upload folder: {self.upload_folder}")
        except Exception as e:
            print(f"❌ Error creating upload folder: {e}")
    
    def submit_report(self, address, flood_height, reporter_name, reporter_phone=None, photo_file=None):
        """Submit new flood report with Base64 photo encoding"""
        try:
            # Get client IP
            client_ip = self.get_client_ip()
            print(f"🌐 Client IP: {client_ip}")
            
            # Handle photo upload and convert to Base64
            photo_base64 = None
            photo_filename = None
            photo_saved_path = None
            
            if photo_file is not None:
                try:
                    file_extension = photo_file.name.split('.')[-1].lower()
                    valid_extensions = ['jpg', 'jpeg', 'png']
                    
                    if file_extension not in valid_extensions:
                        return False, f"❌ Format file tidak didukung. Gunakan: {', '.join(valid_extensions)}"
                    
                    # Generate filename
                    photo_filename = f"{uuid.uuid4()}.{file_extension}"
                    photo_saved_path = os.path.join(self.upload_folder, photo_filename)
                    
                    # Save file locally (for backup and possible local display)
                    print(f"📸 Saving photo locally: {photo_saved_path}")
                    with open(photo_saved_path, "wb") as f:
                        f.write(photo_file.getbuffer())
                    
                    # Convert to Base64 for Google Sheets
                    print(f"🔤 Converting to Base64...")
                    photo_bytes = photo_file.getvalue()
                    photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
                    
                    # Truncate if too long (Google Sheets cell limit ~50K chars)
                    if len(photo_base64) > 45000:  # Leave some buffer
                        print("⚠️ Photo too large, truncating Base64")
                        photo_base64 = photo_base64[:45000] + "...[TRUNCATED]"
                    
                    print(f"✅ Photo converted to Base64 ({len(photo_base64)} chars)")
                    
                except Exception as e:
                    print(f"⚠️ Error processing photo: {e}")
                    # Continue without photo
                    photo_base64 = None
                    photo_filename = None
                    photo_saved_path = None
            
            # Save to SQLite database (local backup)
            print(" Saving to SQLite database...")
            report_id = self.flood_model.create_report(
                address=address,
                flood_height=flood_height,
                reporter_name=reporter_name,
                reporter_phone=reporter_phone,
                photo_path=photo_saved_path,  # Local path for backup
                photo_base64=photo_base64,     # Base64 for quick access
                ip_address=client_ip
            )
            
            if not report_id:
                print("❌ Failed to save to SQLite")
                # Cleanup
                if photo_saved_path and os.path.exists(photo_saved_path):
                    try:
                        os.remove(photo_saved_path)
                    except:
                        pass
                return False, "❌ Gagal menyimpan laporan ke database lokal."
            
            print(f"✅ SQLite save successful! Report ID: {report_id}")
            
            # Save to Google Sheets (if available)
            if self.sheets_model and self.sheets_model.client:
                try:
                    print(" Saving to Google Sheets...")
                    
                    sheets_data = {
                        'address': str(address),
                        'flood_height': str(flood_height),
                        'reporter_name': str(reporter_name),
                        'reporter_phone': str(reporter_phone) if reporter_phone else '',
                        'ip_address': str(client_ip),
                        'photo_filename': photo_filename or '',
                        'photo_base64': photo_base64 or ''  # Base64 string
                    }
                    
                    success = self.sheets_model.save_flood_report(sheets_data)
                    if success:
                        print("✅ Report saved to Google Sheets (with Base64 photo)")
                        gs_status = " (dan Google Sheets dengan foto)"
                    else:
                        print("⚠️ Failed to save to Google Sheets")
                        gs_status = " (Google Sheets gagal)"
                except Exception as e:
                    print(f"⚠️ Error saving to Google Sheets: {e}")
                    gs_status = " (Google Sheets error)"
            else:
                print("ℹ️ Google Sheets not available")
                gs_status = ""
            
            return True, f" Laporan berhasil dikirim! Data telah disimpan di database{gs_status}."
                
        except Exception as e:
            print(f"❌ CRITICAL Error in submit_report: {e}")
            import traceback
            traceback.print_exc()
            
            # Cleanup on error
            if photo_saved_path and os.path.exists(photo_saved_path):
                try:
                    os.remove(photo_saved_path)
                except:
                    pass
            
            return False, f"❌ Error sistem: {str(e)}"
    
    # ... [other methods remain the same]
