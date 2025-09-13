"""
AI Coach Authentication Module
Handles user login, registration, and session management
"""

import streamlit as st
import hashlib
import secrets
from database import AICoachDatabase
from typing import Optional, Dict
import datetime

class AuthManager:
    def __init__(self):
        self.db = AICoachDatabase()
    
    def hash_password(self, password: str) -> str:
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return 'user_session' in st.session_state and st.session_state.user_session is not None
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged in user"""
        if self.is_logged_in():
            return st.session_state.user_session
        return None
    
    def login_user(self, username: str, password: str) -> bool:
        """Login user and create session"""
        try:
            user = self.db.authenticate_user(username, password)
            if user:
                # Create session token
                session_token = self.db.create_session(user['id'])
                if session_token:
                    # Store in session state
                    st.session_state.user_session = user
                    st.session_state.session_token = session_token
                    return True
            return False
        except Exception as e:
            st.error(f"Login error: {str(e)}")
            return False
    
    def logout_user(self) -> bool:
        """Logout current user"""
        try:
            if 'session_token' in st.session_state:
                self.db.logout_user(st.session_state.session_token)
            
            # Clear session state
            if 'user_session' in st.session_state:
                del st.session_state.user_session
            if 'session_token' in st.session_state:
                del st.session_state.session_token
            
            return True
        except Exception as e:
            st.error(f"Logout error: {str(e)}")
            return False
    
    def register_user(self, username: str, email: str, password: str, full_name: str,
                     is_student: bool = False, college_name: str = None, student_id: str = None) -> bool:
        """Register new user"""
        try:
            # Validate input
            if not username or not email or not password or not full_name:
                st.error("All fields are required")
                return False
            
            if len(password) < 6:
                st.error("Password must be at least 6 characters long")
                return False
            
            if is_student and (not college_name or not student_id):
                st.error("College name and Student ID are required for student accounts")
                return False
            
            # Create user
            success = self.db.create_user(username, email, password, full_name, is_student, college_name, student_id)
            if success:
                st.success("Account created successfully! Please login.")
                return True
            else:
                st.error("Username or email already exists")
                return False
                
        except Exception as e:
            st.error(f"Registration error: {str(e)}")
            return False
    
    def check_subscription_status(self) -> Dict:
        """Check current user's subscription status"""
        user = self.get_current_user()
        if not user:
            return {'valid': False, 'type': 'free', 'days_remaining': 0}
        
        return self.db.check_subscription_status(user['id'])
    
    def can_access_feature(self, feature: str) -> bool:
        """Check if user can access specific feature based on subscription"""
        subscription = self.check_subscription_status()
        
        if not subscription['valid']:
            return False
        
        # Free tier limitations
        if subscription['type'] == 'free':
            if feature in ['unlimited_sessions', 'advanced_analysis', 'detailed_reports']:
                return False
        
        return True
    
    def get_remaining_sessions(self) -> int:
        """Get remaining sessions for free users"""
        subscription = self.check_subscription_status()
        
        if subscription['type'] in ['pro', 'student']:
            return -1  # Unlimited
        
        # For free users, check session count
        user = self.get_current_user()
        if not user:
            return 0
        
        try:
            sessions = self.db.get_user_sessions(user['id'], limit=1000)
            used_sessions = len(sessions)
            return max(0, 10 - used_sessions)  # Free users get 10 sessions
        except:
            return 0

def show_login_form():
    """Display login form"""
    st.markdown("### 🔐 Login to AI Coach")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_clicked = st.form_submit_button("Login", use_container_width=True)
        with col2:
            register_clicked = st.form_submit_button("New User? Register", use_container_width=True)
    
    if login_clicked:
        auth = AuthManager()
        if auth.login_user(username, password):
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")
    
    if register_clicked:
        st.session_state.show_register = True
        st.rerun()

def show_register_form():
    """Display registration form"""
    st.markdown("### 📝 Create New Account")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="Enter your email")
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
        
        with col2:
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
        
        # Student verification
        st.markdown("#### 🎓 Student Verification (Optional)")
        is_student = st.checkbox("I am a student and want student pricing")
        
        college_name = None
        student_id = None
        if is_student:
            college_name = st.text_input("College/University Name", placeholder="Enter your college name")
            student_id = st.text_input("Student ID", placeholder="Enter your student ID")
        
        col1, col2 = st.columns(2)
        with col1:
            register_clicked = st.form_submit_button("Create Account", use_container_width=True)
        with col2:
            back_clicked = st.form_submit_button("Back to Login", use_container_width=True)
    
    if register_clicked:
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            auth = AuthManager()
            if auth.register_user(username, email, password, full_name, is_student, college_name, student_id):
                st.session_state.show_register = False
                st.rerun()
    
    if back_clicked:
        st.session_state.show_register = False
        st.rerun()

def show_user_dashboard():
    """Display user dashboard with subscription info"""
    auth = AuthManager()
    user = auth.get_current_user()
    subscription = auth.check_subscription_status()
    
    if not user:
        return
    
    # User info
    st.markdown("### 👤 User Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Username", user['username'])
        st.metric("Full Name", user['full_name'])
    
    with col2:
        st.metric("Subscription", subscription['type'].title())
        if subscription['type'] != 'free':
            st.metric("Days Remaining", subscription['days_remaining'])
    
    with col3:
        remaining_sessions = auth.get_remaining_sessions()
        if remaining_sessions == -1:
            st.metric("Sessions", "Unlimited")
        else:
            st.metric("Sessions Left", remaining_sessions)
    
    # Subscription status
    if subscription['valid']:
        if subscription['type'] == 'free':
            st.info("🆓 You're using the free version. Upgrade to Pro for unlimited access!")
        elif subscription['type'] == 'student':
            st.success("🎓 Student account active! Enjoy your discounted pricing!")
        else:
            st.success("⭐ Pro account active! You have full access to all features!")
    else:
        st.error("❌ Your subscription has expired. Please renew to continue using AI Coach.")
    
    # Logout button
    if st.button("🚪 Logout", type="secondary"):
        auth.logout_user()
        st.rerun()

def require_auth(func):
    """Decorator to require authentication for functions"""
    def wrapper(*args, **kwargs):
        auth = AuthManager()
        if not auth.is_logged_in():
            st.error("Please login to access this feature")
            show_login_form()
            return None
        return func(*args, **kwargs)
    return wrapper

def require_subscription(subscription_type: str = 'pro'):
    """Decorator to require specific subscription level"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            auth = AuthManager()
            if not auth.is_logged_in():
                st.error("Please login to access this feature")
                show_login_form()
                return None
            
            subscription = auth.check_subscription_status()
            if not subscription['valid'] or subscription['type'] not in ['pro', 'student']:
                st.error(f"This feature requires {subscription_type.title()} subscription")
                show_subscription_upgrade()
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def show_subscription_upgrade():
    """Display subscription upgrade options"""
    st.markdown("### ⭐ Upgrade Your Subscription")
    
    auth = AuthManager()
    plans = auth.db.get_subscription_plans()
    
    col1, col2, col3 = st.columns(3)
    
    for i, plan in enumerate(plans):
        with [col1, col2, col3][i]:
            st.markdown(f"#### {plan['name'].title()} Plan")
            st.markdown(f"**₹{plan['price']}/month**")
            
            for feature in plan['features']:
                st.markdown(f"✅ {feature}")
            
            if plan['name'] == 'free':
                st.markdown("**Current Plan**")
            else:
                if st.button(f"Upgrade to {plan['name'].title()}", key=f"upgrade_{plan['name']}"):
                    user = auth.get_current_user()
                    if user and auth.db.upgrade_subscription(user['id'], plan['name']):
                        st.success(f"Successfully upgraded to {plan['name'].title()}!")
                        st.rerun()
                    else:
                        st.error("Upgrade failed. Please try again.")
