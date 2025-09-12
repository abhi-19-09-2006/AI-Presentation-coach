import streamlit as st
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import threading
import cv2
import numpy as np

# Face analysis integration
FACE_ANALYSIS_AVAILABLE = False
OptimizedFaceAnalyzer = None
get_face_analyzer = None

try:
    from face_analysis import OptimizedFaceAnalyzer
    FACE_ANALYSIS_AVAILABLE = True
    
    # Create a global analyzer instance
    _global_analyzer = None
    
    def _get_face_analyzer_func():
        global _global_analyzer
        if _global_analyzer is None and OptimizedFaceAnalyzer is not None:
            _global_analyzer = OptimizedFaceAnalyzer()
        return _global_analyzer
        
    # Assign the function
    get_face_analyzer = _get_face_analyzer_func
except ImportError:
    pass

# Privacy protection imports
try:
    from privacy_manager import privacy_manager
    PRIVACY_AVAILABLE = True
except ImportError:
    PRIVACY_AVAILABLE = False

# Define immediate_privacy_cleanup function
def immediate_privacy_cleanup():
    try:
        from privacy_manager import immediate_privacy_cleanup as _cleanup
        return _cleanup()
    except ImportError:
        return True

# Enhanced realtime analysis manager with face analysis integration
class RealtimeAnalysisManager:
    def __init__(self):
        self.is_active = False
        self.camera = None
        self.analysis_thread = None
        self.stop_event = threading.Event()
        self.face_analyzer = None
        self.session_data = {
            'start_time': None,
            'end_time': None,
            'total_frames': 0,
            'session_summary': None
        }
        
    def start_realtime_analysis(self):
        """Start real-time multimodal analysis with face detection"""
        if not self.is_active:
            self.is_active = True
            self.stop_event.clear()
            
            try:
                # Initialize camera
                self.camera = cv2.VideoCapture(0)
                if not self.camera.isOpened():
                    self.is_active = False
                    raise Exception("Could not access camera. Please check camera permissions.")
                
                # Initialize face analyzer if available
                if FACE_ANALYSIS_AVAILABLE and get_face_analyzer is not None:
                    self.face_analyzer = get_face_analyzer()
                
                self.session_data['start_time'] = time.time()
                self.session_data['total_frames'] = 0
                self.session_data['session_summary'] = None
                
                # Start analysis thread
                self.analysis_thread = threading.Thread(target=self._analysis_loop)
                self.analysis_thread.start()
                
                return True
            except Exception as e:
                self.is_active = False
                if self.camera:
                    self.camera.release()
                raise e
        return False
    
    def stop_realtime_analysis(self) -> bool:
        """Stop analysis and generate comprehensive session summary"""
        if self.is_active:
            self.is_active = False
            self.stop_event.set()
            self.session_data['end_time'] = time.time()
            
            # Generate enhanced session summary
            self.session_data['session_summary'] = self._generate_enhanced_session_summary()
            
            # Cleanup
            if self.camera:
                self.camera.release()
            if self.analysis_thread:
                self.analysis_thread.join(timeout=2)
            
            # Privacy protection: Clean up any data
            if PRIVACY_AVAILABLE:
                immediate_privacy_cleanup()
            
            return True
        return False
    
    def _analysis_loop(self):
        """Main analysis loop with face analysis integration"""
        frame_count = 0
        
        while self.is_active and not self.stop_event.is_set():
            try:
                if self.camera and self.camera.isOpened():
                    ret, frame = self.camera.read()
                    if ret and frame is not None:
                        frame_count += 1
                        
                        # Process every 3rd frame for performance
                        if frame_count % 3 == 0:
                            if FACE_ANALYSIS_AVAILABLE and self.face_analyzer:
                                # Real face analysis
                                self.face_analyzer.analyze_frame_complete(frame)
                            
                            self.session_data['total_frames'] += 1
                        
                        time.sleep(0.1)  # 10 FPS analysis
                    else:
                        time.sleep(0.5)
                else:
                    time.sleep(0.5)
            except Exception as e:
                print(f"Analysis error: {str(e)}")
                time.sleep(1)
    
    def _generate_enhanced_session_summary(self):
        """Generate comprehensive session summary with face analysis data"""
        try:
            duration = self.session_data['end_time'] - self.session_data['start_time'] if self.session_data['start_time'] else 0
            
            if FACE_ANALYSIS_AVAILABLE and self.face_analyzer:
                # Get real analysis data
                trends_data = {
                    'emotion_history': list(self.face_analyzer.emotion_history),
                    'movement_history': list(self.face_analyzer.movement_history),
                    'confidence_history': list(self.face_analyzer.confidence_history)
                }
                
                # Calculate statistics
                emotion_history = trends_data['emotion_history']
                if emotion_history:
                    emotion_counts = {}
                    for emotion in emotion_history:
                        if emotion and emotion != 'no_face_detected':
                            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                    
                    dominant_emotion = max(emotion_counts.keys(), key=lambda k: emotion_counts[k]) if emotion_counts else 'neutral'
                    emotion_diversity = len(emotion_counts)
                else:
                    emotion_counts = {'neutral': 100}
                    dominant_emotion = 'neutral'
                    emotion_diversity = 1
                
                # Movement and engagement calculations
                movement_history = trends_data['movement_history']
                avg_movement = sum(movement_history) / len(movement_history) if movement_history else 0.3
                
                confidence_history = trends_data['confidence_history']
                avg_confidence = sum(confidence_history) / len(confidence_history) if confidence_history else 0.8
                
                # Get performance stats
                perf_stats = self.face_analyzer.get_performance_stats()
                
            else:
                # Fallback mock data
                emotion_counts = {'happy': 60, 'neutral': 30, 'surprise': 10}
                dominant_emotion = 'happy'
                emotion_diversity = 3
                avg_movement = 0.3
                avg_confidence = 0.85
                perf_stats = {'avg_analysis_time_ms': 45, 'face_detection_rate': 95}
            
            # Generate insights
            insights = self._generate_enhanced_insights(
                dominant_emotion, emotion_diversity, avg_movement, 
                avg_confidence, duration, perf_stats
            )
            
            return {
                'session_duration': duration,
                'total_frames_analyzed': self.session_data['total_frames'],
                'analysis_fps': self.session_data['total_frames'] / duration if duration > 0 else 0,
                'dominant_emotion': dominant_emotion,
                'emotion_distribution': emotion_counts,
                'emotion_diversity_score': emotion_diversity,
                'average_movement': avg_movement,
                'movement_range': {'min': max(0, avg_movement - 0.2), 'max': min(1, avg_movement + 0.2)},
                'average_engagement': min((avg_confidence + avg_movement) / 2, 1.0),
                'confidence_average': avg_confidence,
                'emotion_trend': 'improving' if avg_confidence > 0.7 else 'stable',
                'movement_trend': 'animated' if avg_movement > 0.2 else 'calm',
                'insights': insights,
                'overall_score': min((avg_confidence * 40 + emotion_diversity * 15 + avg_movement * 200 + 45), 100),
                'performance_stats': perf_stats,
                'face_analysis_enabled': FACE_ANALYSIS_AVAILABLE
            }
            
        except Exception as e:
            return {'error': f'Failed to generate summary: {str(e)}'}
    
    def _generate_enhanced_insights(self, emotion, diversity, movement, confidence, duration, perf_stats):
        """Generate enhanced insights with performance data"""
        insights = []
        
        # Performance insights
        if perf_stats.get('avg_analysis_time_ms', 100) < 50:
            insights.append("🚀 **Excellent Performance**: Ultra-fast analysis (< 50ms per frame)")
        elif perf_stats.get('avg_analysis_time_ms', 100) < 100:
            insights.append("⚡ **Good Performance**: Fast analysis maintaining 60fps UI")
        
        # Face detection insights
        face_detection_rate = perf_stats.get('face_detection_rate', 95)
        if face_detection_rate > 90:
            insights.append("📹 **Excellent Face Detection**: Consistent tracking throughout session")
        elif face_detection_rate > 70:
            insights.append("📹 **Good Face Detection**: Mostly consistent tracking")
        else:
            insights.append("📹 **Face Detection**: Consider better lighting or camera positioning")
        
        # Emotion and engagement insights
        if emotion == 'happy':
            insights.append("😊 **Positive Energy**: Outstanding! Your expressions create strong audience connection")
        elif emotion == 'neutral':
            insights.append("😐 **Neutral Expression**: Consider adding more emotional variety for better engagement")
        
        if diversity >= 4:
            insights.append("🎭 **Excellent Variety**: Great emotional range demonstrated")
        elif diversity >= 2:
            insights.append("📊 **Good Expression Range**: Nice variety, try expanding further")
        
        # Movement insights optimized for presentations
        if movement < 0.1:
            insights.append("🧘 **Static Presentation**: Add gentle gestures for better engagement")
        elif 0.1 <= movement <= 0.4:
            insights.append("👌 **Optimal Movement**: Perfect balance for professional presentations")
        else:
            insights.append("🎪 **High Energy**: Great animation! Ensure movements support your message")
        
        # Confidence insights
        if confidence >= 0.8:
            insights.append("🌟 **High Confidence**: Exceptional analysis quality and consistency")
        elif confidence >= 0.6:
            insights.append("👍 **Good Confidence**: Solid performance with room for optimization")
        
        return insights
    
    def get_session_summary(self):
        """Get the session summary if available"""
        return self.session_data.get('session_summary')

def create_realtime_dashboard():
    """Create real-time multimodal analysis dashboard"""
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.subheader("🔴 Real-Time Demo Dashboard")
    
    # Initialize session state
    if 'realtime_manager' not in st.session_state:
        st.session_state.realtime_manager = RealtimeAnalysisManager()
    
    manager = st.session_state.realtime_manager
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🎥 Start Demo", disabled=manager.is_active):
            try:
                if manager.start_realtime_analysis():
                    st.success("Demo analysis started!")
                    st.rerun()
            except Exception as e:
                st.error(f"Failed to start demo: {str(e)}")
    
    with col2:
        if st.button("⏹ Stop Demo", disabled=not manager.is_active):
            try:
                if manager.stop_realtime_analysis():
                    st.success("Demo stopped! Generating session report...")
                    st.rerun()
            except Exception as e:
                st.error(f"Failed to stop demo: {str(e)}")
    
    with col3:
        status_color = "🟢" if manager.is_active else "🔴"
        status_text = "ACTIVE" if manager.is_active else "INACTIVE"
        st.markdown(f"**Status:** {status_color} {status_text}")
    
    # Live analysis display or session report
    if manager.is_active:
        display_live_analysis()
    else:
        # Check if we have a session summary to display
        session_summary = manager.get_session_summary()
        if session_summary and 'error' not in session_summary:
            display_session_report(session_summary)
        elif session_summary and 'error' in session_summary:
            st.error(f"Session report error: {session_summary['error']}")
        else:
            # Show getting started message when no session data
            st.info("📹 **Ready to Start**: Click 'Start Demo' to begin demo analysis.")
            st.markdown("**Demo features:**")
            st.markdown("- 🎭 Mock emotion detection")
            st.markdown("- 🏃 Movement simulation")
            st.markdown("- 📊 Live engagement metrics")
            st.markdown("- 📈 Visual feedback dashboard")
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_live_analysis():
    """Display live analysis results"""
    try:
        # Get current analysis with error handling
        current_data = get_realtime_analysis()
        trends_data = get_analysis_trends()
        
        if not current_data:
            st.warning("⚠️ No analysis data available yet. Starting analysis...")
            return
        
        # Create metrics dashboard
        st.markdown("### 📊 Live Demo Dashboard")
        
        # Normal metrics display
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            emotion = current_data.get('emotion', 'unknown')
            confidence = current_data.get('emotion_confidence', 0.0)
            emotion_emoji = get_emotion_emoji(emotion)
            st.metric(
                f"{emotion_emoji} Emotion", 
                emotion.title(),
                f"{confidence:.2f} confidence"
            )
        
        with metric_col2:
            movement = current_data.get('movement_level', 0.0)
            movement_trend = trends_data.get('movement_trend', 'unknown')
            st.metric(
                "🏃 Movement", 
                f"{movement:.3f}",
                f"{movement_trend}"
            )
        
        with metric_col3:
            engagement = current_data.get('engagement_score', 0.0)
            emotion_trend = trends_data.get('emotion_trend', 'stable')
            st.metric(
                "🎯 Engagement", 
                f"{engagement:.2f}",
                f"{emotion_trend}"
            )
        
        with metric_col4:
            overall_confidence = current_data.get('overall_confidence', 0.0)
            avg_confidence = trends_data.get('confidence_average', 0.0)
            st.metric(
                "📈 Confidence", 
                f"{overall_confidence:.2f}",
                f"Avg: {avg_confidence:.2f}"
            )
        
        # Create real-time visualization
        create_realtime_visualization(current_data, trends_data)
        
        # Live feedback panel
        create_live_feedback_panel(current_data, trends_data)
        
    except Exception as e:
        st.error(f"Live analysis display error: {str(e)}")
        st.info("🔄 Demo is running. Data will appear shortly...")

def create_realtime_visualization(current_data, trends_data):
    """Create real-time visualization charts"""
    
    # Create subplots for multiple metrics
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Emotion Confidence', 'Movement Level', 'Engagement Score', 'Overall Confidence'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Prepare data for visualization
    timestamps = list(range(len(trends_data.get('emotion_history', []))))
    
    # Emotion confidence over time
    emotion_history = trends_data.get('emotion_history', [])
    emotion_confidences = [0.8 if emotion in ['happy', 'surprise'] else 
                          0.6 if emotion == 'neutral' else 0.4 
                          for emotion in emotion_history]
    
    fig.add_trace(
        go.Scatter(
            x=timestamps, 
            y=emotion_confidences,
            mode='lines+markers',
            name='Emotion Confidence',
            line=dict(color='#4F46E5', width=2),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    
    # Movement level over time
    movement_history = trends_data.get('movement_history', [])
    fig.add_trace(
        go.Scatter(
            x=timestamps[-len(movement_history):] if movement_history else [],
            y=movement_history,
            mode='lines+markers',
            name='Movement Level',
            line=dict(color='#10B981', width=2),
            marker=dict(size=4)
        ),
        row=1, col=2
    )
    
    # Engagement score (calculated)
    engagement_scores = [calculate_engagement_from_emotion(emotion) for emotion in emotion_history]
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=engagement_scores,
            mode='lines+markers',
            name='Engagement Score',
            line=dict(color='#F59E0B', width=2),
            marker=dict(size=4)
        ),
        row=2, col=1
    )
    
    # Overall confidence trend
    confidence_trend = [0.5 + (i * 0.02) for i in range(len(timestamps))]  # Simulated trend
    fig.add_trace(
        go.Scatter(
            x=timestamps,
            y=confidence_trend,
            mode='lines+markers',
            name='Overall Confidence',
            line=dict(color='#EF4444', width=2),
            marker=dict(size=4)
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=400,
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Update all axes
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_xaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)', row=i, col=j)
            fig.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)', row=i, col=j)
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def create_live_feedback_panel(current_data, trends_data):
    """Create live feedback panel with actionable insights"""
    st.markdown("### 💡 Live Demo Feedback")
    
    feedback_col1, feedback_col2 = st.columns(2)
    
    with feedback_col1:
        st.markdown("**🎭 Emotional State**")
        emotion = current_data.get('emotion', 'neutral')
        confidence = current_data.get('emotion_confidence', 0.0)
        
        if emotion in ['happy', 'surprise']:
            st.success(f"✨ Great energy! Your {emotion} expression is engaging.")
        elif emotion == 'neutral':
            st.info("😐 Neutral expression detected. Consider adding more emotion.")
        else:
            st.warning(f"😔 {emotion.title()} detected. Try to project more positivity.")
        
        # Confidence indicator
        confidence_color = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.4 else "🔴"
        st.markdown(f"{confidence_color} **Confidence Level:** {confidence:.1%}")
    
    with feedback_col2:
        st.markdown("**🏃 Movement & Engagement**")
        movement = current_data.get('movement_level', 0.0)
        engagement = current_data.get('engagement_score', 0.0)
        movement_trend = trends_data.get('movement_trend', 'unknown')
        
        if movement_trend == 'static':
            st.warning("🧘 Very still movement. Consider adding gentle gestures.")
        elif movement_trend == 'calm':
            st.success("👌 Perfect movement level - calm and controlled.")
        elif movement_trend == 'animated':
            st.success("🎪 Great animation! Your gestures are engaging.")
        else:
            st.info("📊 Analyzing movement patterns...")
        
        # Engagement indicator
        engagement_color = "🟢" if engagement > 0.7 else "🟡" if engagement > 0.5 else "🔴"
        st.markdown(f"{engagement_color} **Engagement Score:** {engagement:.1%}")
    
    # Real-time suggestions
    st.markdown("**🚀 Demo Suggestions**")
    suggestions = generate_realtime_suggestions(current_data, trends_data)
    for suggestion in suggestions:
        st.markdown(f"• {suggestion}")

def display_session_report(session_summary):
    """Display comprehensive session report after analysis stops"""
    st.markdown("### 📄 Demo Session Report")
    st.markdown("---")
    
    # Session Overview
    st.markdown("#### 📊 Session Overview")
    
    overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
    
    with overview_col1:
        duration_minutes = session_summary['session_duration'] / 60
        st.metric("⏱️ Duration", f"{duration_minutes:.1f} min")
    
    with overview_col2:
        st.metric("🎬 Frames Analyzed", f"{session_summary['total_frames_analyzed']:,}")
    
    with overview_col3:
        st.metric("📈 Analysis FPS", f"{session_summary['analysis_fps']:.1f}")
    
    with overview_col4:
        overall_score = session_summary['overall_score']
        score_emoji = "🏆" if overall_score >= 80 else "🌟" if overall_score >= 60 else "💪"
        st.metric(f"{score_emoji} Overall Score", f"{overall_score:.1f}/100")
    
    # Performance Metrics
    st.markdown("#### 🎯 Performance Metrics")
    
    metrics_col1, metrics_col2 = st.columns(2)
    
    with metrics_col1:
        st.markdown("**🎭 Emotional Analysis**")
        
        # Dominant emotion
        emotion_emoji = get_emotion_emoji(session_summary['dominant_emotion'])
        st.markdown(f"**Dominant Emotion:** {emotion_emoji} {session_summary['dominant_emotion'].title()}")
        
        # Emotion distribution
        if session_summary['emotion_distribution']:
            st.markdown("**Emotion Distribution:**")
            for emotion, count in session_summary['emotion_distribution'].items():
                percentage = (count / sum(session_summary['emotion_distribution'].values())) * 100
                emoji = get_emotion_emoji(emotion)
                st.markdown(f"- {emoji} {emotion.title()}: {percentage:.1f}% ({count} frames)")
        
        # Emotion diversity score
        diversity_score = session_summary['emotion_diversity_score']
        diversity_color = "green" if diversity_score >= 4 else "orange" if diversity_score >= 2 else "red"
        st.markdown(f"**Emotion Variety:** :{diversity_color}[{diversity_score}/7 emotions detected]")
    
    with metrics_col2:
        st.markdown("**🏃 Movement Analysis**")
        
        # Average movement
        avg_movement = session_summary['average_movement']
        movement_level = "High" if avg_movement > 0.6 else "Moderate" if avg_movement > 0.2 else "Low"
        st.markdown(f"**Average Movement:** {movement_level} ({avg_movement:.3f})")
        
        # Movement range
        movement_range = session_summary['movement_range']
        st.markdown(f"**Movement Range:** {movement_range['min']:.3f} - {movement_range['max']:.3f}")
        
        # Movement trend
        movement_trend = session_summary['movement_trend']
        trend_emoji = "📊" if movement_trend == "animated" else "📉" if movement_trend == "static" else "🔄"
        st.markdown(f"**Movement Pattern:** {trend_emoji} {movement_trend.title()}")
        
        # Engagement metrics
        st.markdown("**🎯 Engagement Metrics**")
        engagement_pct = session_summary['average_engagement'] * 100
        confidence_pct = session_summary['confidence_average'] * 100
        st.markdown(f"**Average Engagement:** {engagement_pct:.1f}%")
        st.markdown(f"**Average Confidence:** {confidence_pct:.1f}%")
    
    # Insights and Recommendations
    st.markdown("#### 💡 AI-Generated Insights")
    
    insights = session_summary.get('insights', [])
    if insights:
        for i, insight in enumerate(insights, 1):
            st.markdown(f"**{i}.** {insight}")
    else:
        st.info("🤔 No specific insights generated for this session.")

# Enhanced mock functions with real face analysis integration
def get_realtime_analysis():
    """Get realtime analysis data with face analysis integration"""
    if FACE_ANALYSIS_AVAILABLE and get_face_analyzer is not None:
        try:
            analyzer = get_face_analyzer()
            if analyzer is not None:
                return analyzer.get_current_analysis()
        except Exception:
            pass
    
    # Fallback mock data
    return {
        'emotion': 'happy',
        'emotion_confidence': 0.85,
        'movement_level': 0.3,
        'engagement_score': 0.8,
        'overall_confidence': 0.82,
        'face_detected': True,
        'timestamp': time.time(),
        'analysis_time_ms': 45
    }

def get_analysis_trends():
    """Get analysis trends with face analysis integration"""
    if FACE_ANALYSIS_AVAILABLE and get_face_analyzer is not None:
        try:
            analyzer = get_face_analyzer()
            if analyzer is not None:
                return {
                    'emotion_trend': analyzer.get_emotion_trend(),
                    'movement_trend': analyzer.get_movement_trend(),
                    'confidence_average': analyzer.get_confidence_average(),
                    'emotion_history': list(analyzer.emotion_history),
                    'movement_history': list(analyzer.movement_history),
                    'performance_stats': analyzer.get_performance_stats()
                }
        except Exception:
            pass
    
    # Fallback mock data
    return {
        'emotion_trend': 'improving',
        'movement_trend': 'animated',
        'confidence_average': 0.8,
        'emotion_history': ['happy', 'surprise', 'neutral', 'happy'],
        'movement_history': [0.2, 0.3, 0.4, 0.3],
        'performance_stats': {'avg_analysis_time_ms': 45, 'face_detection_rate': 95}
    }

def get_emotion_emoji(emotion):
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

def calculate_engagement_from_emotion(emotion):
    """Calculate engagement score from emotion"""
    engagement_scores = {
        'happy': 0.9,
        'surprise': 0.8,
        'neutral': 0.6,
        'sad': 0.4,
        'angry': 0.3,
        'fear': 0.2,
        'disgust': 0.2
    }
    return engagement_scores.get(emotion, 0.5)

def generate_realtime_suggestions(current_data, trends_data):
    """Generate real-time actionable suggestions"""
    suggestions = []
    
    emotion = current_data.get('emotion', 'neutral')
    confidence = current_data.get('emotion_confidence', 0.0)
    movement = current_data.get('movement_level', 0.0)
    engagement = current_data.get('engagement_score', 0.0)
    
    # Emotion-based suggestions
    if confidence < 0.5:
        suggestions.append("🎯 **Face the camera** - Position yourself for better emotion detection")
    
    if emotion in ['sad', 'angry', 'fear']:
        suggestions.append("😊 **Smile more** - Positive expressions increase engagement")
    
    if emotion == 'neutral':
        suggestions.append("✨ **Show enthusiasm** - Add more expression to captivate your audience")
    
    # Movement-based suggestions
    if movement < 0.1:
        suggestions.append("👋 **Add gestures** - Use hand movements to emphasize points")
    elif movement > 0.8:
        suggestions.append("🧘 **Calm movements** - Slow down gestures for better focus")
    
    # Engagement-based suggestions
    if engagement < 0.5:
        suggestions.append("🔥 **Increase energy** - Combine positive emotions with purposeful movement")
    
    # Default suggestions if none triggered
    if not suggestions:
        suggestions.append("👍 **Great job!** - Continue with your current presentation style")
        suggestions.append("📈 **Maintain consistency** - Your demo signals are well-balanced")
    
    return suggestions[:3]  # Return top 3 suggestions
