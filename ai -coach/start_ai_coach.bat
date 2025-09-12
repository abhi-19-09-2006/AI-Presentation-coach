@echo off
title AI Coach - Professional Voice Analysis Platform

echo.
echo ===============================================
echo AI Coach - Professional Voice Analysis Platform
echo ===============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is available
echo.

REM Check if we're in the right directory
if not exist "app.py" (
    echo ❌ app.py not found
    echo Please run this script from the AI Coach directory
    pause
    exit /b 1
)

echo ✅ AI Coach files found
echo.

REM Run the launcher
echo 🚀 Starting AI Coach...
echo.
python run_ai_coach.py

echo.
echo Application closed.
pause