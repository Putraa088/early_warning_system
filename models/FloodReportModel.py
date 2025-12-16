import sqlite3
from datetime import datetime
import os

class FloodReportModel:
    def __init__(self, db_path='flood_system.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database dengan struktur YANG BENAR"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # BUAT TABEL DENGAN STRUKTUR YANG TEPAT
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS flood_reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        address TEXT NOT NULL,
                        flood_height TEXT NOT NULL,
                        reporter_name TEXT NOT NULL,
                        reporter_phone TEXT,
                        photo_path TEXT,
                        ip_address TEXT,
                        report_date DATE DEFAULT (DATE('now')),
                        report_time TIME DEFAULT (TIME('now')),
                        status TEXT DEFAULT 'pending'
                    )
                ''')
                
                conn.commit()
                print("✅ Database table flood_reports ready")
                
        except Exception as e:
            print(f"❌ Error in init_database: {e}")
            import traceback
            traceback.print_exc()
    
    def create_report(self, address, flood_height, reporter_name, 
                      reporter_phone=None, photo_path=None, ip_address=None):
        """Create new flood report - FIXED"""
        try:
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            report_date = current_time.strftime("%Y-%m-%d")
            report_time = current_time.strftime("%H:%M:%S")
            
            print(f"📝 Creating report: {address}, height: {flood_height}")
            print(f"📅 Date: {report_date}, Time: {report_time}")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO flood_reports 
                    (timestamp, address, flood_height, reporter_name, reporter_phone, 
                     photo_path, ip_address, report_date, report_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (timestamp, address, flood_height, reporter_name, 
                      reporter_phone, photo_path, ip_address, report_date, report_time))
                
                conn.commit()
                last_id = cursor.lastrowid
                print(f"✅ Report created with ID: {last_id}")
                
                # VERIFIKASI DATA MASUK
                cursor.execute('SELECT * FROM flood_reports WHERE id = ?', (last_id,))
                saved_data = cursor.fetchone()
                if saved_data:
                    print(f"✅ Data saved: ID={saved_data[0]}, Address={saved_data[2]}")
                
                return last_id
                
        except Exception as e:
            print(f"❌ Error creating report: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_today_reports_count_by_ip(self, ip_address):
        """Count today's reports by IP address - FIXED"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            print(f"🔍 Counting reports for IP: {ip_address} on {today}")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT COUNT(*) FROM flood_reports 
                    WHERE ip_address = ? AND report_date = ?
                ''', (ip_address, today))
                
                count = cursor.fetchone()[0]
                print(f"📊 Found {count} reports for this IP today")
                return count
                
        except Exception as e:
            print(f"❌ Error counting today's reports by IP: {e}")
            return 0
    
    def get_today_reports(self):
        """Get today's reports - FIXED untuk views"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id,
                        address,
                        flood_height,
                        reporter_name,
                        reporter_phone,
                        photo_path,
                        ip_address,
                        report_date,
                        report_time,
                        timestamp,
                        status
                    FROM flood_reports 
                    WHERE report_date = ?
                    ORDER BY timestamp DESC
                ''', (today,))
                
                rows = cursor.fetchall()
                
                # Convert to dictionary untuk compatibility dengan views
                reports = []
                for row in rows:
                    reports.append({
                        'id': row[0],
                        'address': row[1],
                        'flood_height': row[2],
                        'reporter_name': row[3],
                        'reporter_phone': row[4],
                        'photo_path': row[5],
                        'ip_address': row[6],
                        'report_date': row[7],
                        'report_time': row[8],
                        'timestamp': row[9],
                        'status': row[10]
                    })
                
                print(f"📊 Found {len(reports)} reports for today")
                return reports
                
        except Exception as e:
            print(f"❌ Error getting today's reports: {e}")
            return []
    
    def get_month_reports(self):
        """Get this month's reports - FIXED untuk views"""
        try:
            current_month = datetime.now().strftime("%Y-%m")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id,
                        address,
                        flood_height,
                        reporter_name,
                        reporter_phone,
                        photo_path,
                        ip_address,
                        report_date,
                        report_time,
                        timestamp,
                        status
                    FROM flood_reports 
                    WHERE strftime('%Y-%m', timestamp) = ?
                    ORDER BY timestamp DESC
                ''', (current_month,))
                
                rows = cursor.fetchall()
                
                # Convert to dictionary
                reports = []
                for row in rows:
                    reports.append({
                        'id': row[0],
                        'address': row[1],
                        'flood_height': row[2],
                        'reporter_name': row[3],
                        'reporter_phone': row[4],
                        'photo_path': row[5],
                        'ip_address': row[6],
                        'report_date': row[7],
                        'report_time': row[8],
                        'timestamp': row[9],
                        'status': row[10]
                    })
                
                print(f"📊 Found {len(reports)} reports for month {current_month}")
                return reports
                
        except Exception as e:
            print(f"❌ Error getting month's reports: {e}")
            return []
    
    def get_all_reports(self):
        """Get all reports - FIXED"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id,
                        address,
                        flood_height,
                        reporter_name,
                        reporter_phone,
                        photo_path,
                        ip_address,
                        report_date,
                        report_time,
                        timestamp,
                        status
                    FROM flood_reports 
                    ORDER BY timestamp DESC
                ''')
                
                rows = cursor.fetchall()
                reports = []
                for row in rows:
                    reports.append({
                        'id': row[0],
                        'address': row[1],
                        'flood_height': row[2],
                        'reporter_name': row[3],
                        'reporter_phone': row[4],
                        'photo_path': row[5],
                        'ip_address': row[6],
                        'report_date': row[7],
                        'report_time': row[8],
                        'timestamp': row[9],
                        'status': row[10]
                    })
                
                return reports
                
        except Exception as e:
            print(f"❌ Error getting all reports: {e}")
            return []
    
    def get_monthly_statistics(self):
        """Get monthly statistics - FIXED"""
        try:
            current_month = datetime.now().strftime("%Y-%m")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT COUNT(*) FROM flood_reports 
                    WHERE strftime('%Y-%m', timestamp) = ?
                ''', (current_month,))
                total_reports = cursor.fetchone()[0]
                
                return {
                    'total_reports': total_reports,
                    'month': current_month
                }
                
        except Exception as e:
            print(f"❌ Error getting monthly statistics: {e}")
            return {'total_reports': 0, 'month': ''}
