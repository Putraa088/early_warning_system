import sqlite3
import os

class VisitorModel:
    _initialized = False  
    
    def __init__(self):
        self.db_path = 'flood_system.db'
        if not VisitorModel._initialized:
            self.init_database()
            VisitorModel._initialized = True  

    def init_database(self):
        """Initialize database and tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS visitor_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    page_visited VARCHAR(255),
                    visit_date DATE,
                    visit_time TIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS popular_pages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    page_url VARCHAR(255),
                    page_title VARCHAR(255),
                    visit_count INTEGER DEFAULT 0,
                    last_visited DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_visit_date ON visitor_stats(visit_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_page_visited ON visitor_stats(page_visited)')
            
            conn.commit()
            conn.close()
            print("✅ Database visitor_stats initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")

    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def record_visit(self, page_visited=''):
        """Record new visit"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            ip_address = self.get_client_ip()
            user_agent = self.get_user_agent()
            visit_date = self.get_current_date()
            visit_time = self.get_current_time()
            
            cursor.execute('''
                INSERT INTO visitor_stats (ip_address, user_agent, page_visited, visit_date, visit_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (ip_address, user_agent, page_visited, visit_date, visit_time))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error recording visit: {e}")
            return False

    def update_popular_page(self, page_url, page_title):
        """Update popular pages count"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, visit_count FROM popular_pages WHERE page_url = ?', (page_url,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute('''
                    UPDATE popular_pages 
                    SET visit_count = visit_count + 1, last_visited = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (existing[0],))
            else:
                cursor.execute('''
                    INSERT INTO popular_pages (page_url, page_title, visit_count) 
                    VALUES (?, ?, 1)
                ''', (page_url, page_title))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating popular page: {e}")
            return False

    def get_today_visitors(self):
        """Get today's unique visitors"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(DISTINCT ip_address) as count 
                FROM visitor_stats 
                WHERE visit_date = ?
            ''', (self.get_current_date(),))
            
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting today visitors: {e}")
            return 0

    def get_month_visitors(self):
        """Get this month's unique visitors"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            first_day = self.get_current_date()[:8] + '01'  
            last_day = self.get_current_date()[:8] + '31'   
            
            cursor.execute('''
                SELECT COUNT(DISTINCT ip_address) as count 
                FROM visitor_stats 
                WHERE visit_date BETWEEN ? AND ?
            ''', (first_day, last_day))
            
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting month visitors: {e}")
            return 0

    def get_online_visitors(self):
        """Get online visitors (last 5 minutes)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(DISTINCT ip_address) as count 
                FROM visitor_stats 
                WHERE datetime(created_at) >= datetime('now', '-5 minutes')
            ''')
            
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting online visitors: {e}")
            return 0

    def get_today_popular_pages(self, limit=5):
        """Get today's popular pages"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT page_visited, COUNT(*) as visit_count 
                FROM visitor_stats 
                WHERE visit_date = ? AND page_visited != ''
                GROUP BY page_visited 
                ORDER BY visit_count DESC 
                LIMIT ?
            ''', (self.get_current_date(), limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [{'page_visited': row[0], 'visit_count': row[1]} for row in results]
        except Exception as e:
            print(f"Error getting popular pages: {e}")
            return []

    def get_client_ip(self):
        """Get client IP address"""
        try:
            if 'HTTP_X_FORWARDED_FOR' in os.environ:
                return os.environ['HTTP_X_FORWARDED_FOR']
            elif 'REMOTE_ADDR' in os.environ:
                return os.environ['REMOTE_ADDR']
            else:
                return '0.0.0.0'
        except:
            return '0.0.0.0'

    def get_user_agent(self):
        """Get user agent"""
        try:
            return os.environ.get('HTTP_USER_AGENT', 'Unknown')
        except:
            return 'Unknown'

    def get_current_date(self):
        """Get current date in YYYY-MM-DD format"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')

    def get_current_time(self):
        """Get current time in HH:MM:SS format"""
        from datetime import datetime
        return datetime.now().strftime('%H:%M:%S')
