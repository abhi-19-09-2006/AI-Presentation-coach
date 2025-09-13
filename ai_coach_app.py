"""
AI Coach - Professional Presentation Analysis Platform
A comprehensive app with live video face analysis, user authentication, and subscription management
"""

import streamlit as st
import cv2
import numpy as np
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import threading
from datetime import datetime, timedelta
import json

# Import our modules
from auth import AuthManager, show_login_form, show_register_form, show_user_dashboard, require_auth, require_subscription
from database import AICoachDatabase
from face_analysis import OptimizedFaceAnalyzer, get_face_analyzer
from realtime_analysis import RealtimeAnalysisManager

# Page configuration
st.set_page_config(
    page_title="AI Coach Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .subscription-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        text-align: center;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

class AICoachApp:
    def __init__(self):
        self.auth = AuthManager()
        self.db = AICoachDatabase()
        self.face_analyzer = None
        self.realtime_manager = None
        
        # Initialize session state
        if 'analysis_active' not in st.session_state:
            st.session_state.analysis_active = False
        if 'show_register' not in st.session_state:
            st.session_state.show_register = False
    
    def run(self):
        """Main app runner"""
        # Check authentication
        if not self.auth.is_logged_in():
            self.show_landing_page()
        else:
            self.show_main_app()
    
    def show_landing_page(self):
        """Show landing page for non-authenticated users"""
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>🎯 AI Coach Pro</h1>
            <h3>Professional Presentation Analysis Platform</h3>
            <p>Transform your presentations with real-time AI-powered feedback</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features showcase
        st.markdown("## ✨ Key Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🎭 Live Face Analysis</h4>
                <p>Real-time emotion detection and engagement analysis during your presentations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>📊 Advanced Analytics</h4>
                <p>Detailed performance metrics and actionable insights to improve your skills</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>🎓 Student Discounts</h4>
                <p>Special pricing for students with college verification</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Pricing plans
        st.markdown("## 💰 Pricing Plans")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="subscription-card">
                <h3>🆓 Free</h3>
                <h2>₹0/month</h2>
                <ul style="text-align: left;">
                    <li>Basic face analysis</li>
                    <li>1 month access</li>
                    <li>10 analysis sessions</li>
                    <li>Basic reports</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="subscription-card">
                <h3>⭐ Pro</h3>
                <h2>₹199/month</h2>
                <ul style="text-align: left;">
                    <li>Advanced face analysis</li>
                    <li>Unlimited access</li>
                    <li>Real-time feedback</li>
                    <li>Detailed reports</li>
                    <li>Priority support</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="subscription-card">
                <h3>🎓 Student</h3>
                <h2>₹99/month</h2>
                <ul style="text-align: left;">
                    <li>All Pro features</li>
                    <li>Student discount</li>
                    <li>College verification</li>
                    <li>Academic support</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Authentication section
        st.markdown("## 🔐 Get Started")
        
        if st.session_state.show_register:
            show_register_form()
        else:
            show_login_form()
    
    def show_main_app(self):
        """Show main application for authenticated users"""
        # Sidebar
        self.show_sidebar()
        
        # Main content
        if st.session_state.get('current_page', 'dashboard') == 'dashboard':
            self.show_dashboard()
        elif st.session_state.get('current_page') == 'live_analysis':
            self.show_live_analysis()
        elif st.session_state.get('current_page') == 'history':
            self.show_analysis_history()
        elif st.session_state.get('current_page') == 'subscription':
            self.show_subscription_management()
        elif st.session_state.get('current_page') == 'settings':
            self.show_settings()
    
    def show_sidebar(self):
        """Show sidebar navigation"""
        with st.sidebar:
            st.markdown("## 🎯 AI Coach Pro")
            
            # User info
            user = self.auth.get_current_user()
            subscription = self.auth.check_subscription_status()
            
            st.markdown(f"**Welcome, {user['full_name']}!**")
            st.markdown(f"Plan: {subscription['type'].title()}")
            
            if subscription['type'] != 'free':
                st.markdown(f"Days remaining: {subscription['days_remaining']}")
            
            st.markdown("---")
            
            # Navigation
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.current_page = 'dashboard'
                st.rerun()
            
            if st.button("🎥 Live Analysis", use_container_width=True):
                st.session_state.current_page = 'live_analysis'
                st.rerun()
            
            if st.button("📈 Analysis History", use_container_width=True):
                st.session_state.current_page = 'history'
                st.rerun()
            
            if st.button("💳 Subscription", use_container_width=True):
                st.session_state.current_page = 'subscription'
                st.rerun()
            
            if st.button("⚙️ Settings", use_container_width=True):
                st.session_state.current_page = 'settings'
                st.rerun()
            
            st.markdown("---")
            
            if st.button("🚪 Logout", type="secondary", use_container_width=True):
                self.auth.logout_user()
                st.rerun()
    
    def show_dashboard(self):
        """Show main dashboard"""
        st.markdown("# 📊 Dashboard")
        
        user = self.auth.get_current_user()
        subscription = self.auth.check_subscription_status()
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            remaining_sessions = self.auth.get_remaining_sessions()
            if remaining_sessions == -1:
                st.metric("Sessions", "Unlimited", "Pro/Student Plan")
            else:
                st.metric("Sessions Left", remaining_sessions, "Free Plan")
        
        with col2:
            st.metric("Subscription", subscription['type'].title(), 
                     f"{subscription['days_remaining']} days left" if subscription['type'] != 'free' else "Expired")
        
        with col3:
            # Get recent sessions count
            sessions = self.db.get_user_sessions(user['id'], limit=5)
            st.metric("Recent Sessions", len(sessions), "Last 5")
        
        with col4:
            if subscription['valid']:
                st.metric("Status", "Active", "✅")
            else:
                st.metric("Status", "Expired", "❌")
        
        # Quick actions
        st.markdown("## 🚀 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎥 Start Live Analysis", use_container_width=True, type="primary"):
                st.session_state.current_page = 'live_analysis'
                st.rerun()
        
        with col2:
            if st.button("📈 View History", use_container_width=True):
                st.session_state.current_page = 'history'
                st.rerun()
        
        with col3:
            if st.button("💳 Manage Subscription", use_container_width=True):
                st.session_state.current_page = 'subscription'
                st.rerun()
        
        # Recent activity
        st.markdown("## 📈 Recent Activity")
        
        sessions = self.db.get_user_sessions(user['id'], limit=5)
        if sessions:
            for i, session in enumerate(sessions):
                with st.expander(f"Session {i+1} - {session['created_at'][:19]}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Duration", f"{session['session_duration']:.1f}s")
                    
                    with col2:
                        st.metric("Score", f"{session['overall_score']:.1f}/100")
                    
                    with col3:
                        st.metric("Emotion", session['session_data'].get('dominant_emotion', 'N/A').title())
        else:
            st.info("No analysis sessions yet. Start your first live analysis!")
    
    @require_auth
    def show_live_analysis(self):
        """Show live analysis interface"""
        st.markdown("# 🎥 Live Analysis")
        
        # Check subscription for live analysis
        if not self.auth.can_access_feature('live_analysis'):
            st.error("Live analysis requires Pro or Student subscription")
            self.show_subscription_upgrade()
            return
        
        # Initialize face analyzer
        if self.face_analyzer is None:
            self.face_analyzer = get_face_analyzer()
        
        # Analysis controls
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            if st.button("🎬 Start Analysis", disabled=st.session_state.analysis_active, type="primary"):
                if self.face_analyzer.start_live_analysis():
                    st.session_state.analysis_active = True
                    st.success("Live analysis started!")
                    st.rerun()
                else:
                    st.error("Failed to start analysis. Check camera permissions.")
        
        with col2:
            if st.button("⏹ Stop Analysis", disabled=not st.session_state.analysis_active):
                self.face_analyzer.stop_live_analysis()
                st.session_state.analysis_active = False
                st.success("Analysis stopped!")
                st.rerun()
        
        with col3:
            if st.button("🗑️ Clear Data", type="secondary"):
                if st.session_state.get('confirm_clear_live_data', False):
                    # Clear current analysis data
                    if self.face_analyzer:
                        self.face_analyzer.emotion_history.clear()
                        self.face_analyzer.confidence_history.clear()
                        self.face_analyzer.movement_history.clear()
                        self.face_analyzer.performance_stats = {
                            'frames_processed': 0,
                            'avg_analysis_time': 0.0,
                            'cache_hits': 0,
                            'face_detection_rate': 0.0
                        }
                    st.success("✅ Current analysis data cleared!")
                    st.session_state.confirm_clear_live_data = False
                    st.rerun()
                else:
                    st.session_state.confirm_clear_live_data = True
                    st.warning("⚠️ Click again to confirm clearing current analysis data")
        
        with col4:
            status = "🟢 Active" if st.session_state.analysis_active else "🔴 Inactive"
            st.markdown(f"**Status:** {status}")
        
        # Show confirmation if needed
        if st.session_state.get('confirm_clear_live_data', False):
            st.error("⚠️ **CONFIRMATION REQUIRED**: Click 'Clear Data' again to clear current analysis data.")
        
        # Live analysis display
        if st.session_state.analysis_active:
            self.show_live_analysis_display()
        else:
            st.info("Click 'Start Analysis' to begin live face analysis")
    
    def show_live_analysis_display(self):
        """Show live analysis results"""
        if not self.face_analyzer or not self.face_analyzer.is_analyzing:
            st.warning("Analysis not active")
            return
        
        # Create placeholder for live updates
        placeholder = st.empty()
        
        # Get live analysis data
        analysis_data = self.face_analyzer.get_live_frame_analysis()
        
        if 'error' in analysis_data:
            st.error(f"Analysis error: {analysis_data['error']}")
            return
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            emotion = analysis_data.get('emotion', 'unknown')
            confidence = analysis_data.get('emotion_confidence', 0.0)
            emotion_emoji = self.get_emotion_emoji(emotion)
            st.metric(
                f"{emotion_emoji} Emotion",
                emotion.title(),
                f"{confidence:.2f} confidence"
            )
        
        with col2:
            movement = analysis_data.get('movement_level', 0.0)
            st.metric(
                "🏃 Movement",
                f"{movement:.3f}",
                "Level"
            )
        
        with col3:
            engagement = analysis_data.get('engagement_score', 0.0)
            st.metric(
                "🎯 Engagement",
                f"{engagement:.2f}",
                "Score"
            )
        
        with col4:
            overall_confidence = analysis_data.get('overall_confidence', 0.0)
            st.metric(
                "📈 Confidence",
                f"{overall_confidence:.2f}",
                "Overall"
            )
        
        # Live feedback
        self.show_live_feedback(analysis_data)
        
        # Auto-refresh for live updates
        time.sleep(0.1)
        st.rerun()
    
    def show_live_feedback(self, analysis_data):
        """Show live feedback based on analysis"""
        st.markdown("### 💡 Live Feedback")
        
        emotion = analysis_data.get('emotion', 'neutral')
        confidence = analysis_data.get('emotion_confidence', 0.0)
        movement = analysis_data.get('movement_level', 0.0)
        engagement = analysis_data.get('engagement_score', 0.0)
        
        feedback_col1, feedback_col2 = st.columns(2)
        
        with feedback_col1:
            st.markdown("**🎭 Emotional State**")
            if emotion in ['happy', 'surprise']:
                st.success(f"✨ Great energy! Your {emotion} expression is engaging.")
            elif emotion == 'neutral':
                st.info("😐 Neutral expression detected. Consider adding more emotion.")
            else:
                st.warning(f"😔 {emotion.title()} detected. Try to project more positivity.")
            
            confidence_color = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.4 else "🔴"
            st.markdown(f"{confidence_color} **Confidence Level:** {confidence:.1%}")
        
        with feedback_col2:
            st.markdown("**🏃 Movement & Engagement**")
            if movement < 0.1:
                st.warning("🧘 Very still movement. Consider adding gentle gestures.")
            elif movement <= 0.4:
                st.success("👌 Perfect movement level - calm and controlled.")
            else:
                st.success("🎪 Great animation! Your gestures are engaging.")
            
            engagement_color = "🟢" if engagement > 0.7 else "🟡" if engagement > 0.5 else "🔴"
            st.markdown(f"{engagement_color} **Engagement Score:** {engagement:.1%}")
        
        # Suggestions
        suggestions = self.generate_live_suggestions(analysis_data)
        if suggestions:
            st.markdown("**🚀 Suggestions**")
            for suggestion in suggestions:
                st.markdown(f"• {suggestion}")
    
    def generate_live_suggestions(self, analysis_data):
        """Generate live suggestions based on analysis"""
        suggestions = []
        
        emotion = analysis_data.get('emotion', 'neutral')
        confidence = analysis_data.get('emotion_confidence', 0.0)
        movement = analysis_data.get('movement_level', 0.0)
        engagement = analysis_data.get('engagement_score', 0.0)
        
        if confidence < 0.5:
            suggestions.append("🎯 **Face the camera** - Position yourself for better emotion detection")
        
        if emotion in ['sad', 'angry', 'fear']:
            suggestions.append("😊 **Smile more** - Positive expressions increase engagement")
        
        if emotion == 'neutral':
            suggestions.append("✨ **Show enthusiasm** - Add more expression to captivate your audience")
        
        if movement < 0.1:
            suggestions.append("👋 **Add gestures** - Use hand movements to emphasize points")
        elif movement > 0.8:
            suggestions.append("🧘 **Calm movements** - Slow down gestures for better focus")
        
        if engagement < 0.5:
            suggestions.append("🔥 **Increase energy** - Combine positive emotions with purposeful movement")
        
        if not suggestions:
            suggestions.append("👍 **Great job!** - Continue with your current presentation style")
        
        return suggestions[:3]
    
    def get_emotion_emoji(self, emotion):
        """Get emoji for emotion"""
        emotion_emojis = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'surprise': '😲',
            'fear': '😨',
            'disgust': '🤢',
            'neutral': '😐',
            'no_face_detected': '📹',
            'error': '⚠️'
        }
        return emotion_emojis.get(emotion, '🤖')
    
    @require_auth
    def show_analysis_history(self):
        """Show analysis history"""
        st.markdown("# 📈 Analysis History")
        
        user = self.auth.get_current_user()
        sessions = self.db.get_user_sessions(user['id'], limit=20)
        
        # History controls
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**Total Sessions:** {len(sessions)}")
        
        with col2:
            if st.button("🔄 Refresh", type="secondary"):
                st.rerun()
        
        with col3:
            if st.button("🗑️ Clear All History", type="secondary"):
                if st.session_state.get('confirm_clear_history', False):
                    # Clear all user sessions
                    if self.db.clear_user_data(user['id']):
                        st.success("✅ All analysis history cleared!")
                        st.session_state.confirm_clear_history = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to clear history. Please try again.")
                else:
                    st.session_state.confirm_clear_history = True
                    st.warning("⚠️ Click again to confirm clearing all history")
        
        # Show confirmation if needed
        if st.session_state.get('confirm_clear_history', False):
            st.error("⚠️ **CONFIRMATION REQUIRED**: Click 'Clear All History' again to permanently delete all your analysis history.")
        
        if not sessions:
            st.info("No analysis sessions found. Start your first live analysis!")
            return
        
        # Session list
        for i, session in enumerate(sessions):
            with st.expander(f"Session {i+1} - {session['created_at'][:19]}"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Duration", f"{session['session_duration']:.1f}s")
                
                with col2:
                    st.metric("Overall Score", f"{session['overall_score']:.1f}/100")
                
                with col3:
                    emotion = session['session_data'].get('dominant_emotion', 'N/A')
                    st.metric("Dominant Emotion", emotion.title())
                
                with col4:
                    engagement = session['session_data'].get('average_engagement', 0)
                    st.metric("Engagement", f"{engagement:.1%}")
                
                # Detailed metrics
                if st.button(f"View Details", key=f"details_{i}"):
                    self.show_session_details(session)
    
    def show_session_details(self, session):
        """Show detailed session information"""
        st.markdown("### 📊 Session Details")
        
        session_data = session['session_data']
        
        # Metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Performance Metrics**")
            st.metric("Session Duration", f"{session['session_duration']:.1f}s")
            st.metric("Overall Score", f"{session['overall_score']:.1f}/100")
            st.metric("Frames Analyzed", session_data.get('total_frames_analyzed', 0))
        
        with col2:
            st.markdown("**Emotional Analysis**")
            st.metric("Dominant Emotion", session_data.get('dominant_emotion', 'N/A').title())
            st.metric("Emotion Diversity", session_data.get('emotion_diversity_score', 0))
            st.metric("Average Engagement", f"{session_data.get('average_engagement', 0):.1%}")
        
        # Insights
        insights = session_data.get('insights', [])
        if insights:
            st.markdown("**💡 AI Insights**")
            for insight in insights:
                st.markdown(f"• {insight}")
    
    @require_auth
    def show_subscription_management(self):
        """Show subscription management"""
        st.markdown("# 💳 Subscription Management")
        
        user = self.auth.get_current_user()
        subscription = self.auth.check_subscription_status()
        
        # Current subscription
        st.markdown("## Current Subscription")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Plan", subscription['type'].title())
        
        with col2:
            if subscription['type'] == 'free':
                st.metric("Status", "Active")
            else:
                st.metric("Days Remaining", subscription['days_remaining'])
        
        with col3:
            if subscription['valid']:
                st.metric("Status", "✅ Active")
            else:
                st.metric("Status", "❌ Expired")
        
        # Upgrade options
        st.markdown("## Upgrade Options")
        
        plans = self.db.get_subscription_plans()
        
        col1, col2, col3 = st.columns(3)
        
        for i, plan in enumerate(plans):
            with [col1, col2, col3][i]:
                if plan['name'] == subscription['type']:
                    st.markdown(f"**{plan['name'].title()} (Current)**")
                else:
                    st.markdown(f"**{plan['name'].title()}**")
                
                st.markdown(f"**₹{plan['price']}/month**")
                
                for feature in plan['features']:
                    st.markdown(f"✅ {feature}")
                
                if plan['name'] != subscription['type'] and plan['name'] != 'free':
                    if st.button(f"Upgrade to {plan['name'].title()}", key=f"upgrade_{plan['name']}"):
                        if self.db.upgrade_subscription(user['id'], plan['name']):
                            st.success(f"Successfully upgraded to {plan['name'].title()}!")
                            st.rerun()
                        else:
                            st.error("Upgrade failed. Please try again.")
    
    def show_subscription_upgrade(self):
        """Show subscription upgrade options"""
        st.markdown("## ⭐ Upgrade Your Subscription")
        
        plans = self.db.get_subscription_plans()
        
        col1, col2, col3 = st.columns(3)
        
        for i, plan in enumerate(plans):
            with [col1, col2, col3][i]:
                st.markdown(f"### {plan['name'].title()} Plan")
                st.markdown(f"**₹{plan['price']}/month**")
                
                for feature in plan['features']:
                    st.markdown(f"✅ {feature}")
                
                if plan['name'] != 'free':
                    if st.button(f"Upgrade to {plan['name'].title()}", key=f"upgrade_{plan['name']}"):
                        user = self.auth.get_current_user()
                        if user and self.db.upgrade_subscription(user['id'], plan['name']):
                            st.success(f"Successfully upgraded to {plan['name'].title()}!")
                            st.rerun()
                        else:
                            st.error("Upgrade failed. Please try again.")
    
    @require_auth
    def show_settings(self):
        """Show user settings"""
        st.markdown("# ⚙️ Settings")
        
        user = self.auth.get_current_user()
        
        # User information
        st.markdown("## User Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Username", value=user['username'], disabled=True)
            st.text_input("Email", value=user['email'], disabled=True)
        
        with col2:
            st.text_input("Full Name", value=user['full_name'], disabled=True)
            st.text_input("College", value=user.get('college_name', 'N/A'), disabled=True)
        
        # Data management
        st.markdown("## 📊 Data Management")
        
        # Get user data size
        data_info = self.db.get_user_data_size(user['id'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Analysis Sessions", data_info['session_count'])
        
        with col2:
            st.metric("Data Size", f"{data_info['data_size_mb']} MB")
        
        with col3:
            st.metric("Data Usage", f"{data_info['data_size_bytes']:,} bytes")
        
        # Clear data section
        st.markdown("### 🗑️ Clear Data")
        
        st.warning("⚠️ **Warning**: Clearing data will permanently delete all your analysis sessions and recorded data. This action cannot be undone.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear My Data", type="secondary"):
                if st.session_state.get('confirm_clear_data', False):
                    # Actually clear the data
                    if self.db.clear_user_data(user['id']):
                        st.success("✅ All your data has been cleared successfully!")
                        st.session_state.confirm_clear_data = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to clear data. Please try again.")
                else:
                    st.session_state.confirm_clear_data = True
                    st.warning("⚠️ Click again to confirm data deletion")
        
        with col2:
            if st.button("🔄 Refresh Data Info", type="secondary"):
                st.rerun()
        
        # Show confirmation if needed
        if st.session_state.get('confirm_clear_data', False):
            st.error("⚠️ **CONFIRMATION REQUIRED**: Click 'Clear My Data' again to permanently delete all your analysis data.")
        
        # Account actions
        st.markdown("## Account Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh Session", type="secondary"):
                st.success("Session refreshed!")
                st.rerun()
        
        with col2:
            if st.button("🚪 Logout", type="secondary"):
                self.auth.logout_user()
                st.rerun()

def main():
    """Main application entry point"""
    app = AICoachApp()
    app.run()

if __name__ == "__main__":
    main()
