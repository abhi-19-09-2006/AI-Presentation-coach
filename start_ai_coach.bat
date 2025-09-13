@echo off
title AI Coach Pro - Professional Presentation Analysis Platform
color 0A

echo.
echo ======================================================================
echo 🎯 AI COACH PRO - PROFESSIONAL PRESENTATION ANALYSIS PLATFORM
echo ======================================================================
echo ✨ Features: Live Face Analysis | User Authentication | Subscriptions
echo 🔒 Security: Password Hashing | Session Management | Data Protection
echo 💰 Plans: Free | Pro (₹199/month) | Student (₹99/month)
echo ======================================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python is installed
echo.

echo Checking if this is the first run...
if not exist "ai_coach.db" (
    echo 🆕 First time setup detected
    echo.
)

echo Installing/updating dependencies...
echo This may take a few minutes on first run...
echo.

pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo.
    echo ❌ Error installing dependencies
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully
echo.

echo 🚀 Starting AI Coach Pro...
echo ======================================================================
echo 🌐 The application will open in your default browser
echo 📍 URL: http://localhost:8501
echo ⏹️ Press Ctrl+C to stop the application
echo ======================================================================
echo.

python launch_ai_coach.py

echo.
echo 👋 AI Coach Pro has been stopped
echo Thank you for using AI Coach Pro!
echo.
pause