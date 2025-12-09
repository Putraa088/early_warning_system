import sqlite3
import os
import sys

def init_database():
    print("🔄 Initializing database tables...")
    
    db_file = 'flood_system.db'
    
    # Hapus database lama jika ada dan tidak sedang digunakan
    if os.path.exists(db_file):
        try:
            # Test if database is locked
            conn = sqlite3.connect(db_file)
            conn.close()
            os.remove(db_file)
            print("🗑️ Old database removed")
        except:
            print("⚠️ Database sedang digunakan, membuat backup...")
            backup_name = f"{db_file}.backup"
            if os.path.exists(backup_name):
                os.remove(backup_name)
            os.rename(db_file, backup_name)
            print(f"📁 Database lama di-backup sebagai: {backup_name}")
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # 1. Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default users
        import hashlib
        def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
        
        default_users = [
            ('admin@banjir.com', hash_pw('admin123'), 'Administrator', 'admin'),
            ('user@banjir.com', hash_pw('user123'), 'User Demo', 'user'),
            ('guest@banjir.com', hash_pw('guest123'), 'Guest User', 'user')
        ]
        
        for email, pwd, name, role in default_users:
            cursor.execute('''
                INSERT OR IGNORE INTO users (email, password_hash, full_name, role)
                VALUES (?, ?, ?, ?)
            ''', (email, pwd, name, role))
        
        # 2. Create flood_reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flood_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                flood_height TEXT NOT NULL,
                reporter_name TEXT NOT NULL,
                reporter_phone TEXT,
                photo_path TEXT,
                ip_address TEXT,
                report_date DATE DEFAULT CURRENT_DATE,
                report_time TIME DEFAULT CURRENT_TIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        # 3. Create visitor_stats table
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
        
        # 4. Create popular_pages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS popular_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_url VARCHAR(255),
                page_title VARCHAR(255),
                visit_count INTEGER DEFAULT 0,
                last_visited DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized with 4 tables")
        print("📋 Tables created: users, flood_reports, visitor_stats, popular_pages")
        print("👥 Default users added:")
        print("   - admin@banjir.com / admin123")
        print("   - user@banjir.com / user123")
        print("   - guest@banjir.com / guest123")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)