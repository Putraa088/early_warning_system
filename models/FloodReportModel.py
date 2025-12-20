import sqlite3
from datetime import datetime
import os
import traceback
import pytz  

class FloodReportModel:
    def __init__(self, db_path='flood_system.db'):
        self.db_path = db_path
        print(f"📂 Database path: {os.path.abspath(db_path)}")
        
        self.tz_wib = pytz.timezone('Asia/Jakarta')
        
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"❌ Cannot connect to database: {e}")
            return None
    
    def init_database(self):
        """Initialize database dengan struktur baru"""
        try:
            if os.path.exists(self.db_path):
                print(f"ℹ️ Database exists: {os.path.getsize(self.db_path)} bytes")
            
            conn = self.get_connection()
            if not conn:
                conn = sqlite3.connect(self.db_path)
            
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flood_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    "Timestamp" TEXT,
                    "Alamat" TEXT NOT NULL,
                    "Tinggi Banjir" TEXT NOT NULL,
                    "Nama Pelapor" TEXT NOT NULL,
                    "No HP" TEXT,
                    "IP Address" TEXT,
                    "Photo URL" TEXT,
                    "Status" TEXT DEFAULT 'pending',
                    report_date DATE,
                    report_time TIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
            cursor.execute("PRAGMA table_info(flood_reports)")
            columns = cursor.fetchall()
            print(f"✅ Table 'flood_reports' ready with {len(columns)} columns")
            
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error in init_database: {e}")
            traceback.print_exc()
            return False
    
    def create_report(self, alamat, tinggi_banjir, nama_pelapor, 
                    no_hp=None, photo_url=None, ip_address=None):
        """Create new flood report dengan waktu WIB"""
        try:
            current_time_wib = datetime.now(self.tz_wib)
            timestamp = current_time_wib.strftime("%Y-%m-%d %H:%M:%S")
            report_date = current_time_wib.strftime("%Y-%m-%d")
            report_time = current_time_wib.strftime("%H:%M:%S")
            
            print(f"📝 Creating report (WIB Time):")
            print(f"  Timestamp: {timestamp}")
            print(f"  Alamat: {alamat}")
            print(f"  Tinggi Banjir: {tinggi_banjir}")
            print(f"  Nama Pelapor: {nama_pelapor}")
            print(f"  No HP: {no_hp}")
            print(f"  Photo URL: {photo_url}")
            print(f"  IP Address: {ip_address}")
            
            conn = self.get_connection()
            if not conn:
                print("❌ No database connection")
                return None
            
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO flood_reports 
                ("Timestamp", "Alamat", "Tinggi Banjir", "Nama Pelapor", 
                "No HP", "IP Address", "Photo URL", "Status",
                report_date, report_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                str(alamat) if alamat else "",
                str(tinggi_banjir) if tinggi_banjir else "",
                str(nama_pelapor) if nama_pelapor else "",
                str(no_hp) if no_hp else None,
                str(ip_address) if ip_address else "unknown",
                str(photo_url) if photo_url else None,
                'pending',
                report_date,
                report_time
            ))
            
            conn.commit()
            last_id = cursor.lastrowid
            print(f"✅ Report created with ID: {last_id}")
            
            cursor.execute('SELECT COUNT(*) FROM flood_reports')
            count = cursor.fetchone()[0]
            print(f"✅ Total reports in database: {count}")
            
            conn.close()
            return last_id
            
        except Exception as e:
            print(f"❌ Error creating report: {e}")
            traceback.print_exc()
            return None
    
    def get_today_reports_count_by_ip(self, ip_address):
        """Count today's reports by IP address"""
        try:
            today = datetime.now(self.tz_wib).strftime("%Y-%m-%d")
            
            conn = self.get_connection()
            if not conn:
                return 0
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM flood_reports 
                WHERE "IP Address" = ? AND report_date = ?
            ''', (ip_address, today))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            print(f"📊 Today's reports for IP {ip_address}: {count}")
            return count
            
        except Exception as e:
            print(f"❌ Error counting reports: {e}")
            return 0
    
    def get_today_reports(self):
        """Get today's reports"""
        try:
            today = datetime.now(self.tz_wib).strftime("%Y-%m-%d")
            
            conn = self.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM flood_reports 
                WHERE report_date = ?
                ORDER BY "Timestamp" DESC
            ''', (today,))
            
            rows = cursor.fetchall()
            conn.close()
            
            reports = []
            for row in rows:
                reports.append({
                    'id': row['id'],
                    'Alamat': row['Alamat'],
                    'Tinggi Banjir': row['Tinggi Banjir'],
                    'Nama Pelapor': row['Nama Pelapor'],
                    'No HP': row['No HP'],
                    'IP Address': row['IP Address'],
                    'Photo URL': row['Photo URL'],
                    'Status': row['Status'],
                    'report_date': row['report_date'],
                    'report_time': row['report_time'],
                    'Timestamp': row['Timestamp']
                })
            
            print(f"📊 Today's reports: {len(reports)}")
            return reports
            
        except Exception as e:
            print(f"❌ Error getting today's reports: {e}")
            return []
    
    def get_month_reports(self):
        """Get this month's reports"""
        try:
            current_month = datetime.now(self.tz_wib).strftime("%Y-%m")
            
            conn = self.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM flood_reports 
                WHERE strftime('%Y-%m', report_date) = ?
                ORDER BY "Timestamp" DESC
            ''', (current_month,))
            
            rows = cursor.fetchall()
            conn.close()
            
            reports = []
            for row in rows:
                reports.append({
                    'id': row['id'],
                    'Alamat': row['Alamat'],
                    'Tinggi Banjir': row['Tinggi Banjir'],
                    'Nama Pelapor': row['Nama Pelapor'],
                    'No HP': row['No HP'],
                    'IP Address': row['IP Address'],
                    'Photo URL': row['Photo URL'],
                    'Status': row['Status'],
                    'report_date': row['report_date'],
                    'report_time': row['report_time'],
                    'Timestamp': row['Timestamp']
                })
            
            print(f"📊 Month's reports: {len(reports)}")
            return reports
            
        except Exception as e:
            print(f"❌ Error getting month's reports: {e}")
            return []
    
    def get_all_reports(self):
        """Get all reports"""
        try:
            conn = self.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM flood_reports ORDER BY "Timestamp" DESC')
            
            rows = cursor.fetchall()
            conn.close()
            
            reports = []
            for row in rows:
                reports.append({
                    'id': row['id'],
                    'Alamat': row['Alamat'],
                    'Tinggi Banjir': row['Tinggi Banjir'],
                    'Nama Pelapor': row['Nama Pelapor'],
                    'No HP': row['No HP'],
                    'IP Address': row['IP Address'],
                    'Photo URL': row['Photo URL'],
                    'Status': row['Status'],
                    'Timestamp': row['Timestamp']
                })
            
            return reports
            
        except Exception as e:
            print(f"❌ Error getting all reports: {e}")
            return []
    
    def get_monthly_statistics(self):
        """Get monthly statistics"""
        try:
            current_month = datetime.now(self.tz_wib).strftime("%Y-%m")
            
            conn = self.get_connection()
            if not conn:
                return {'total_reports': 0, 'month': current_month}
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM flood_reports 
                WHERE strftime('%Y-%m', report_date) = ?
            ''', (current_month,))
            
            total = cursor.fetchone()[0]
            conn.close()
            
            return {
                'total_reports': total,
                'month': current_month
            }
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {'total_reports': 0, 'month': ''}
