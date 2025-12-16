import sqlite3
import os

def init_database():
    """Initialize database tables"""
    db_path = 'flood_system.db'
    
    # Remove existing database if exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Old database removed")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create flood_reports table
    cursor.execute('''
        CREATE TABLE flood_reports (
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
    
    # Create indexes
    cursor.execute('''
        CREATE INDEX idx_timestamp ON flood_reports(timestamp)
    ''')
    cursor.execute('''
        CREATE INDEX idx_ip ON flood_reports(ip_address)
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

if __name__ == "__main__":
    init_database()
