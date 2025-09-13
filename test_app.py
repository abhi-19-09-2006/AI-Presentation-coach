"""
AI Coach Pro Test Script
Quick test to verify all components are working
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit")
    except ImportError as e:
        print(f"❌ Streamlit: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV")
    except ImportError as e:
        print(f"❌ OpenCV: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("✅ Plotly")
    except ImportError as e:
        print(f"❌ Plotly: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas")
    except ImportError as e:
        print(f"❌ Pandas: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow")
    except ImportError as e:
        print(f"❌ Pillow: {e}")
        return False
    
    try:
        import deepface
        print("✅ DeepFace")
    except ImportError as e:
        print(f"❌ DeepFace: {e}")
        return False
    
    try:
        import tensorflow as tf
        print("✅ TensorFlow")
    except ImportError as e:
        print(f"❌ TensorFlow: {e}")
        return False
    
    return True

def test_database():
    """Test database functionality"""
    print("\n🗄️ Testing database...")
    
    try:
        from database import AICoachDatabase
        db = AICoachDatabase()
        print("✅ Database initialization")
        
        # Test user creation
        test_user = db.create_user("test_user", "test@example.com", "testpass123", "Test User")
        if test_user:
            print("✅ User creation")
        else:
            print("⚠️ User creation (may already exist)")
        
        # Test authentication
        auth_user = db.authenticate_user("test_user", "testpass123")
        if auth_user:
            print("✅ User authentication")
        else:
            print("❌ User authentication")
            return False
        
        # Test subscription check
        sub_status = db.check_subscription_status(auth_user['id'])
        print(f"✅ Subscription check: {sub_status['type']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_face_analysis():
    """Test face analysis functionality"""
    print("\n🎭 Testing face analysis...")
    
    try:
        from face_analysis import OptimizedFaceAnalyzer
        analyzer = OptimizedFaceAnalyzer()
        print("✅ Face analyzer initialization")
        
        # Test with dummy frame
        import numpy as np
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        result = analyzer.analyze_frame_complete(dummy_frame)
        print("✅ Face analysis (dummy frame)")
        
        return True
        
    except Exception as e:
        print(f"❌ Face analysis test failed: {e}")
        return False

def test_camera():
    """Test camera access"""
    print("\n📹 Testing camera access...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✅ Camera access confirmed")
                return True
            else:
                print("⚠️ Camera detected but cannot capture frames")
                return False
        else:
            print("⚠️ Camera not accessible")
            return False
            
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎯 AI Coach Pro - Component Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test database
    if not test_database():
        all_tests_passed = False
    
    # Test face analysis
    if not test_face_analysis():
        all_tests_passed = False
    
    # Test camera (optional)
    camera_ok = test_camera()
    if not camera_ok:
        print("⚠️ Camera test failed - live analysis may not work")
    
    print("\n" + "=" * 50)
    
    if all_tests_passed:
        print("🎉 All core tests passed! AI Coach Pro is ready to launch.")
        print("Run 'python launch_ai_coach.py' to start the application.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
