#!/usr/bin/env python3
"""
AI Coach - Professional Voice Analysis Platform
Main Launcher Script

This script provides an easy way to start the AI Coach application with 
proper error checking and system validation.

Usage:
    python run_ai_coach.py
    
Or simply double-click this file if Python is configured for .py files.
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_streamlit_installation():
    """Check if Streamlit is installed"""
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
        return True
    except ImportError:
        print("❌ Streamlit is not installed")
        return False


def check_required_files():
    """Check if required application files exist"""
    required_files = [
        'app.py',
        'speech_to_text.py', 
        'text_analysis_module.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"✅ Found: {file}")
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    return True


def install_requirements():
    """Install requirements if needed"""
    print("\n🔧 Installing/updating requirements...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Requirements installation completed")
            return True
        else:
            print(f"❌ Requirements installation failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Requirements installation timed out")
        return False
    except Exception as e:
        print(f"❌ Requirements installation error: {e}")
        return False


def test_core_modules():
    """Test if core modules can be imported"""
    modules_to_test = [
        ('speech_to_text', 'Speech-to-Text module'),
        ('text_analysis_module', 'Text Analysis module'),
    ]
    
    print("\n🧪 Testing core modules...")
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description}")
        except ImportError as e:
            print(f"❌ {description}: {e}")
            return False
        except Exception as e:
            print(f"⚠️ {description}: Warning - {e}")
    
    return True


def get_streamlit_command():
    """Get the appropriate Streamlit command"""
    # Try different ways to run Streamlit
    commands = [
        [sys.executable, '-m', 'streamlit', 'run', 'app.py'],
        ['streamlit', 'run', 'app.py'],
        ['python', '-m', 'streamlit', 'run', 'app.py']
    ]
    
    return commands[0]  # Use the most reliable option


def run_application():
    """Run the AI Coach application"""
    print("\n🚀 Starting AI Coach Application...")
    print("📌 The application will open in your default web browser")
    print("📌 Press Ctrl+C to stop the application")
    print("=" * 60)
    
    try:
        cmd = get_streamlit_command()
        
        # Add Streamlit configuration for better performance
        env = os.environ.copy()
        env['STREAMLIT_SERVER_HEADLESS'] = 'true'
        env['STREAMLIT_SERVER_PORT'] = '8501'
        env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
        
        subprocess.run(cmd, env=env)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")
        print("\n💡 Try running manually with: streamlit run app.py")


def main():
    """Main launcher function"""
    print("🤖 AI Coach - Professional Voice Analysis Platform")
    print("=" * 60)
    
    # Step 1: Check Python version
    if not check_python_version():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 2: Check required files
    if not check_required_files():
        print("\n💡 Make sure you're running this script from the AI Coach directory")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Step 3: Check Streamlit installation
    if not check_streamlit_installation():
        print("\n🔧 Installing Streamlit and other requirements...")
        if not install_requirements():
            print("\n❌ Failed to install requirements automatically")
            print("💡 Try manually running: pip install -r requirements.txt")
            input("\nPress Enter to exit...")
            sys.exit(1)
    
    # Step 4: Test core modules
    if not test_core_modules():
        print("\n⚠️  Some modules have issues, but attempting to run anyway...")
        time.sleep(2)
    
    # Step 5: Run the application
    run_application()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("\n📋 System Information:")
        print(f"   Python: {sys.version}")
        print(f"   Platform: {sys.platform}")
        print(f"   Working Directory: {os.getcwd()}")
        
        input("\nPress Enter to exit...")
        sys.exit(1)