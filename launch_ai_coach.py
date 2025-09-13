"""
AI Coach Pro Launcher
Professional Presentation Analysis Platform
Complete launcher with dependency checking and error handling
"""

import subprocess
import sys
import os
import time
import platform

def print_banner():
    """Print application banner"""
    print("=" * 70)
    print("🎯 AI COACH PRO - PROFESSIONAL PRESENTATION ANALYSIS PLATFORM")
    print("=" * 70)
    print("✨ Features: Live Face Analysis | User Authentication | Subscription Management")
    print("🔒 Security: Password Hashing | Session Management | Data Protection")
    print("💰 Plans: Free | Pro (₹199/month) | Student (₹99/month)")
    print("=" * 70)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = {
        'streamlit': 'streamlit',
        'opencv-python': 'cv2',
        'numpy': 'numpy',
        'plotly': 'plotly',
        'pandas': 'pandas',
        'Pillow': 'PIL',
        'deepface': 'deepface',
        'tensorflow': 'tensorflow'
    }
    
    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - Missing")
            missing_packages.append(package_name)
    
    return missing_packages

def install_dependencies(packages):
    """Install missing dependencies"""
    print(f"\n📦 Installing {len(packages)} missing packages...")
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package, '--quiet'
            ])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def check_camera_access():
    """Check if camera is accessible"""
    print("\n📹 Checking camera access...")
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
            print("⚠️ Camera not accessible - check permissions")
            return False
    except Exception as e:
        print(f"⚠️ Camera check failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Setting up directories...")
    
    directories = ['logs', 'temp', 'exports']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory}/ directory")
        else:
            print(f"✅ {directory}/ directory exists")

def check_database():
    """Check database initialization"""
    print("\n🗄️ Checking database...")
    try:
        from database import AICoachDatabase
        db = AICoachDatabase()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def launch_application():
    """Launch the Streamlit application"""
    print("\n🚀 Launching AI Coach Pro...")
    print("=" * 70)
    print("🌐 The application will open in your default browser")
    print("📍 URL: http://localhost:8501")
    print("⏹️ Press Ctrl+C to stop the application")
    print("=" * 70)
    
    try:
        # Launch with optimized settings
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'ai_coach_app.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false',
            '--server.headless', 'false',
            '--server.enableCORS', 'false',
            '--server.enableXsrfProtection', 'false'
        ])
    except KeyboardInterrupt:
        print("\n\n👋 AI Coach Pro stopped by user")
        print("Thank you for using AI Coach Pro!")
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")
        print("Please check the error message above and try again")

def main():
    """Main launcher function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        input("\nPress Enter to exit...")
        return
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️ Missing {len(missing)} required packages")
        response = input("Do you want to install them automatically? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            if not install_dependencies(missing):
                print("\n❌ Failed to install some dependencies")
                print("Please install manually: pip install -r requirements.txt")
                input("\nPress Enter to exit...")
                return
        else:
            print("\n❌ Cannot proceed without required dependencies")
            print("Please install manually: pip install -r requirements.txt")
            input("\nPress Enter to exit...")
            return
    
    # Setup
    create_directories()
    
    # Check database
    if not check_database():
        print("\n❌ Database initialization failed")
        input("\nPress Enter to exit...")
        return
    
    # Check camera (optional)
    camera_ok = check_camera_access()
    if not camera_ok:
        print("\n⚠️ Camera access issues detected")
        print("The app will work but live analysis may not function properly")
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response not in ['y', 'yes']:
            print("Please check camera permissions and try again")
            input("\nPress Enter to exit...")
            return
    
    # Launch application
    time.sleep(1)
    launch_application()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")
