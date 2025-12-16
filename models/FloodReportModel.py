import sqlite3
from datetime import datetime, timezone, timedelta
import os

class FloodReportModel:
    def __init__(self, db_path='flood_system.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables - PERBAIKAN: Hapus index creation"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create flood_reports table saja
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flood_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    address TEXT NOT NULL,
                    flood_height REAL NOT NULL,
                    reporter_name TEXT NOT NULL,
                    reporter_phone TEXT,
                    photo_path TEXT,
                    ip_address TEXT NOT NULL,
                    status TEXT DEFAULT 'pending'
                )
            ''')
            
            # HAPUS pembuatan index untuk menghindari error
            # cursor.execute('''
            #     CREATE INDEX IF NOT EXISTS idx_timestamp ON flood_reports(timestamp)
            # ''')
            # cursor.execute('''
            #     CREATE INDEX IF NOT EXISTS idx_ip ON flood_reports(ip_address)
            # ''')
            
            conn.commit()
    
    def get_wib_time(self):
        """Get current time in WIB (UTC+7)"""
        # Get UTC time
        utc_now = datetime.now(timezone.utc)
        # Convert to WIB (UTC+7)
        wib_time = utc_now + timedelta(hours=7)
        return wib_time
    
    def create_report(self, address, flood_height, reporter_name, 
                      reporter_phone=None, photo_path=None, ip_address=None):
        """Create new flood report with WIB timestamp"""
        try:
            wib_time = self.get_wib_time()
            timestamp = wib_time.strftime("%Y-%m-%d %H:%M:%S")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO flood_reports 
                    (timestamp, address, flood_height, reporter_name, reporter_phone, photo_path, ip_address)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (timestamp, address, flood_height, reporter_name, 
                      reporter_phone, photo_path, ip_address))
                conn.commit()
                
                return cursor.lastrowid
        except Exception as e:
            print(f"❌ Error creating report: {e}")
            return None
    
    def get_today_reports(self):
        """Get today's reports in WIB time"""
        try:
            wib_time = self.get_wib_time()
            today_date = wib_time.strftime("%Y-%m-%d")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM flood_reports 
                    WHERE date(timestamp) = ?
                    ORDER BY timestamp DESC
                ''', (today_date,))
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error getting today's reports: {e}")
            return []
    
    def get_today_reports_count_by_ip(self, ip_address):
        """Count today's reports by IP address"""
        try:
            wib_time = self.get_wib_time()
            today_date = wib_time.strftime("%Y-%m-%d")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT COUNT(*) FROM flood_reports 
                    WHERE ip_address = ? AND date(timestamp) = ?
                ''', (ip_address, today_date))
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"❌ Error counting today's reports by IP: {e}")
            return 0
    
    def get_month_reports(self):
        """Get this month's reports in WIB time"""
        try:
            wib_time = self.get_wib_time()
            year_month = wib_time.strftime("%Y-%m")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM flood_reports 
                    WHERE strftime('%Y-%m', timestamp) = ?
                    ORDER BY timestamp DESC
                ''', (year_month,))
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error getting month's reports: {e}")
            return []
    
    def get_all_reports(self):
        """Get all reports"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM flood_reports 
                    ORDER BY timestamp DESC
                ''')
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error getting all reports: {e}")
            return []
    
    def get_monthly_statistics(self):
        """Get monthly statistics"""
        try:
            wib_time = self.get_wib_time()
            year_month = wib_time.strftime("%Y-%m")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Total reports this month
                cursor.execute('''
                    SELECT COUNT(*) FROM flood_reports 
                    WHERE strftime('%Y-%m', timestamp) = ?
                ''', (year_month,))
                total_reports = cursor.fetchone()[0]
                
                # Average flood height
                cursor.execute('''
                    SELECT AVG(flood_height) FROM flood_reports 
                    WHERE strftime('%Y-%m', timestamp) = ?
                ''', (year_month,))
                avg_flood_height = cursor.fetchone()[0] or 0
                
                return {
                    'total_reports': total_reports,
                    'avg_flood_height': round(avg_flood_height, 2),
                    'month': year_month
                }
        except Exception as e:
            print(f"❌ Error getting monthly statistics: {e}")
            return {'total_reports': 0, 'avg_flood_height': 0, 'month': year_month}
