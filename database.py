"""
AI Coach Database Management
Handles user authentication, subscriptions, and data storage
"""

import sqlite3
import hashlib
import secrets
import datetime
from typing import Optional, Dict, List, Tuple
import json

class AICoachDatabase:
    def __init__(self, db_path: str = "ai_coach.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT NOT NULL,
                subscription_type TEXT DEFAULT 'free',
                subscription_start_date TEXT,
                subscription_end_date TEXT,
                is_student BOOLEAN DEFAULT FALSE,
                college_name TEXT,
                student_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login TEXT,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Sessions table for security
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Analysis sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_data TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                session_duration REAL,
                overall_score REAL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Subscription plans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscription_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_name TEXT UNIQUE NOT NULL,
                price_monthly REAL NOT NULL,
                features TEXT NOT NULL,
                max_sessions INTEGER,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Insert default subscription plans
        cursor.execute('''
            INSERT OR IGNORE INTO subscription_plans (plan_name, price_monthly, features, max_sessions) VALUES
            ('free', 0.0, '["Basic face analysis", "1 month access", "Limited sessions"]', 10),
            ('pro', 199.0, '["Advanced face analysis", "Unlimited access", "Real-time feedback", "Detailed reports"]', -1),
            ('student', 99.0, '["Advanced face analysis", "Unlimited access", "Student discount", "College verification required"]', -1)
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str, salt: str = None) -> Tuple[str, str]:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return password_hash.hex(), salt
    
    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verify password against stored hash"""
        password_hash, _ = self.hash_password(password, salt)
        return password_hash == stored_hash
    
    def create_user(self, username: str, email: str, password: str, full_name: str, 
                   is_student: bool = False, college_name: str = None, student_id: str = None) -> bool:
        """Create new user account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                conn.close()
                return False
            
            # Hash password
            password_hash, salt = self.hash_password(password)
            
            # Set subscription based on student status
            subscription_type = 'student' if is_student else 'free'
            subscription_start = datetime.datetime.now().isoformat()
            subscription_end = (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, salt, full_name, 
                                 subscription_type, subscription_start_date, subscription_end_date,
                                 is_student, college_name, student_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, salt, full_name, subscription_type,
                  subscription_start, subscription_end, is_student, college_name, student_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, password_hash, salt, full_name, subscription_type,
                       subscription_start_date, subscription_end_date, is_student, college_name,
                       student_id, is_active
                FROM users WHERE username = ? AND is_active = TRUE
            ''', (username,))
            
            user = cursor.fetchone()
            if not user:
                conn.close()
                return None
            
            # Verify password
            if not self.verify_password(password, user[3], user[4]):
                conn.close()
                return None
            
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = ? WHERE id = ?
            ''', (datetime.datetime.now().isoformat(), user[0]))
            
            conn.commit()
            conn.close()
            
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[5],
                'subscription_type': user[6],
                'subscription_start_date': user[7],
                'subscription_end_date': user[8],
                'is_student': user[9],
                'college_name': user[10],
                'student_id': user[11],
                'is_active': user[12]
            }
            
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def create_session(self, user_id: int) -> str:
        """Create user session token"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Generate session token
            session_token = secrets.token_urlsafe(32)
            expires_at = (datetime.datetime.now() + datetime.timedelta(hours=24)).isoformat()
            
            # Deactivate old sessions
            cursor.execute('''
                UPDATE user_sessions SET is_active = FALSE WHERE user_id = ?
            ''', (user_id,))
            
            # Create new session
            cursor.execute('''
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES (?, ?, ?)
            ''', (user_id, session_token, expires_at))
            
            conn.commit()
            conn.close()
            
            return session_token
            
        except Exception as e:
            print(f"Error creating session: {e}")
            return None
    
    def validate_session(self, session_token: str) -> Optional[Dict]:
        """Validate session token and return user data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT u.id, u.username, u.email, u.full_name, u.subscription_type,
                       u.subscription_start_date, u.subscription_end_date, u.is_student,
                       u.college_name, u.student_id, u.is_active, s.expires_at
                FROM users u
                JOIN user_sessions s ON u.id = s.user_id
                WHERE s.session_token = ? AND s.is_active = TRUE AND u.is_active = TRUE
            ''', (session_token,))
            
            user = cursor.fetchone()
            if not user:
                conn.close()
                return None
            
            # Check if session is expired
            expires_at = datetime.datetime.fromisoformat(user[11])
            if datetime.datetime.now() > expires_at:
                # Deactivate expired session
                cursor.execute('''
                    UPDATE user_sessions SET is_active = FALSE WHERE session_token = ?
                ''', (session_token,))
                conn.commit()
                conn.close()
                return None
            
            conn.close()
            
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3],
                'subscription_type': user[4],
                'subscription_start_date': user[5],
                'subscription_end_date': user[6],
                'is_student': user[7],
                'college_name': user[8],
                'student_id': user[9],
                'is_active': user[10]
            }
            
        except Exception as e:
            print(f"Error validating session: {e}")
            return None
    
    def logout_user(self, session_token: str) -> bool:
        """Logout user by deactivating session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE user_sessions SET is_active = FALSE WHERE session_token = ?
            ''', (session_token,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error logging out user: {e}")
            return False
    
    def check_subscription_status(self, user_id: int) -> Dict:
        """Check user's subscription status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT subscription_type, subscription_start_date, subscription_end_date
                FROM users WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            if not user:
                conn.close()
                return {'valid': False, 'type': 'free', 'days_remaining': 0}
            
            subscription_type = user[0]
            subscription_end = datetime.datetime.fromisoformat(user[2])
            days_remaining = (subscription_end - datetime.datetime.now()).days
            
            is_valid = days_remaining > 0 or subscription_type == 'pro'
            
            conn.close()
            
            return {
                'valid': is_valid,
                'type': subscription_type,
                'days_remaining': max(0, days_remaining),
                'expires_at': user[2]
            }
            
        except Exception as e:
            print(f"Error checking subscription: {e}")
            return {'valid': False, 'type': 'free', 'days_remaining': 0}
    
    def upgrade_subscription(self, user_id: int, new_plan: str) -> bool:
        """Upgrade user subscription"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get plan details
            cursor.execute('''
                SELECT price_monthly FROM subscription_plans WHERE plan_name = ?
            ''', (new_plan,))
            
            plan = cursor.fetchone()
            if not plan:
                conn.close()
                return False
            
            # Calculate new subscription dates
            start_date = datetime.datetime.now().isoformat()
            if new_plan == 'pro':
                end_date = (datetime.datetime.now() + datetime.timedelta(days=365)).isoformat()
            else:  # student
                end_date = (datetime.datetime.now() + datetime.timedelta(days=365)).isoformat()
            
            # Update user subscription
            cursor.execute('''
                UPDATE users 
                SET subscription_type = ?, subscription_start_date = ?, subscription_end_date = ?
                WHERE id = ?
            ''', (new_plan, start_date, end_date, user_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error upgrading subscription: {e}")
            return False
    
    def save_analysis_session(self, user_id: int, session_data: Dict) -> bool:
        """Save analysis session data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO analysis_sessions (user_id, session_data, session_duration, overall_score)
                VALUES (?, ?, ?, ?)
            ''', (user_id, json.dumps(session_data), 
                  session_data.get('session_duration', 0),
                  session_data.get('overall_score', 0)))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error saving analysis session: {e}")
            return False
    
    def get_user_sessions(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's analysis sessions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT session_data, created_at, session_duration, overall_score
                FROM analysis_sessions 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            
            sessions = []
            for row in cursor.fetchall():
                sessions.append({
                    'session_data': json.loads(row[0]),
                    'created_at': row[1],
                    'session_duration': row[2],
                    'overall_score': row[3]
                })
            
            conn.close()
            return sessions
            
        except Exception as e:
            print(f"Error getting user sessions: {e}")
            return []
    
    def get_subscription_plans(self) -> List[Dict]:
        """Get available subscription plans"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT plan_name, price_monthly, features, max_sessions
                FROM subscription_plans WHERE is_active = TRUE
            ''')
            
            plans = []
            for row in cursor.fetchall():
                plans.append({
                    'name': row[0],
                    'price': row[1],
                    'features': json.loads(row[2]),
                    'max_sessions': row[3]
                })
            
            conn.close()
            return plans
            
        except Exception as e:
            print(f"Error getting subscription plans: {e}")
            return []
    
    def clear_user_data(self, user_id: int) -> bool:
        """Clear all user data including analysis sessions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clear analysis sessions
            cursor.execute('DELETE FROM analysis_sessions WHERE user_id = ?', (user_id,))
            
            # Clear user sessions (logout all devices)
            cursor.execute('DELETE FROM user_sessions WHERE user_id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error clearing user data: {e}")
            return False
    
    def clear_all_analysis_data(self) -> bool:
        """Clear all analysis data from all users (admin function)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clear all analysis sessions
            cursor.execute('DELETE FROM analysis_sessions')
            
            # Clear all user sessions
            cursor.execute('DELETE FROM user_sessions')
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error clearing all analysis data: {e}")
            return False
    
    def get_user_data_size(self, user_id: int) -> Dict:
        """Get user data size information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count analysis sessions
            cursor.execute('SELECT COUNT(*) FROM analysis_sessions WHERE user_id = ?', (user_id,))
            session_count = cursor.fetchone()[0]
            
            # Get total data size (approximate)
            cursor.execute('''
                SELECT SUM(LENGTH(session_data)) FROM analysis_sessions WHERE user_id = ?
            ''', (user_id,))
            data_size_bytes = cursor.fetchone()[0] or 0
            data_size_mb = data_size_bytes / (1024 * 1024)
            
            conn.close()
            
            return {
                'session_count': session_count,
                'data_size_mb': round(data_size_mb, 2),
                'data_size_bytes': data_size_bytes
            }
            
        except Exception as e:
            print(f"Error getting user data size: {e}")
            return {'session_count': 0, 'data_size_mb': 0, 'data_size_bytes': 0}
