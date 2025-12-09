import sqlite3
import hashlib
import os
from datetime import datetime
import re

class UserModel:
    _initialized = False  # ✅ Tambahkan flag untuk mencegah inisialisasi berulang
    
    def __init__(self):
        self.db_path = 'flood_system.db'
        if not UserModel._initialized:
            self.init_database()
            UserModel._initialized = True  # ✅ Set flag setelah inisialisasi

    def init_database(self):
        """Initialize database and tables for users"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create users table
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
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_email ON users(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_role ON users(role)')
            
            # Insert default users if not exists
            default_users = [
                ('admin@banjir.com', self._hash_password('admin123'), 'Administrator Sistem', 'admin'),
                ('user@banjir.com', self._hash_password('user123'), 'User Demo', 'user'),
                ('guest@banjir.com', self._hash_password('guest123'), 'Guest User', 'user')
            ]
            
            for email, pwd_hash, full_name, role in default_users:
                cursor.execute('''
                    INSERT OR IGNORE INTO users (email, password_hash, full_name, role)
                    VALUES (?, ?, ?, ?)
                ''', (email, pwd_hash, full_name, role))
            
            conn.commit()
            conn.close()
            print("✅ Database users initialized successfully")
        except Exception as e:
            print(f"❌ Database initialization error: {e}")

    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def _hash_password(self, password):
        """Simple password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password, password_hash):
        """Verify password against hash"""
        return self._hash_password(password) == password_hash

    def authenticate_user(self, email, password):
        """Authenticate user with email and password"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, email, password_hash, full_name, role, is_active
                FROM users 
                WHERE email = ? AND is_active = 1
            ''', (email,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user and self.verify_password(password, user[2]):
                # Update last login
                self.update_last_login(user[0])
                
                return {
                    'id': user[0],
                    'email': user[1],
                    'full_name': user[3],
                    'role': user[4],
                    'is_active': user[5]
                }
            return None
            
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return None

    def update_last_login(self, user_id):
        """Update user's last login timestamp"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users 
                SET last_login = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Error updating last login: {e}")

    def create_user(self, email, password, full_name, role='user'):
        """Create new user"""
        try:
            if not self._is_valid_email(email):
                raise Exception("Format email tidak valid")
                
            conn = self.get_connection()
            cursor = conn.cursor()
            
            password_hash = self._hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (email, password_hash, full_name, role)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, full_name, role))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            raise Exception("Email sudah terdaftar")
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return None

    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, email, full_name, role, is_active, created_at, last_login
                FROM users 
                WHERE email = ?
            ''', (email,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'email': user[1],
                    'full_name': user[2],
                    'role': user[3],
                    'is_active': user[4],
                    'created_at': user[5],
                    'last_login': user[6]
                }
            return None
            
        except Exception as e:
            print(f"❌ Error getting user: {e}")
            return None

    def _is_valid_email(self, email):
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None