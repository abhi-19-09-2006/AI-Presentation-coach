# 🚀 AI Coach Pro - Launch Guide

## Quick Start (Recommended)

### Windows Users
1. **Double-click `start_ai_coach.bat`**
2. Wait for dependencies to install (first time only)
3. The app will open in your browser automatically

### All Platforms
1. **Run the launcher:**
   ```bash
   python launch_ai_coach.py
   ```

2. **Or run directly:**
   ```bash
   streamlit run ai_coach_app.py
   ```

## 🔧 Prerequisites

- **Python 3.8 or higher** (Download from https://python.org)
- **Webcam access** (for live analysis)
- **Modern web browser** (Chrome, Firefox, Edge, Safari)

## 📋 First Time Setup

1. **Install Python** (if not already installed)
   - Download from https://python.org
   - Make sure to check "Add Python to PATH" during installation

2. **Run the application**
   - Double-click `start_ai_coach.bat` (Windows)
   - Or run `python launch_ai_coach.py`

3. **Wait for setup**
   - Dependencies will be installed automatically
   - Database will be initialized
   - Camera access will be tested

4. **Access the app**
   - Browser will open automatically to http://localhost:8501
   - If not, manually open this URL

## 🎯 Using the App

### 1. Create Account
- Click "New User? Register"
- Fill in your details
- Choose between regular or student account
- Students need college name and student ID

### 2. Start Analysis
- Go to "Live Analysis" in the sidebar
- Click "Start Analysis"
- Allow camera permissions when prompted
- View real-time feedback and metrics

### 3. View Results
- Check "Analysis History" for past sessions
- View detailed metrics and insights
- Track your progress over time

### 4. Manage Subscription
- Go to "Subscription" to view your plan
- Upgrade to Pro or Student plans
- Monitor your usage and remaining sessions

## 🗑️ Clear Data Features

### Clear Current Analysis
- In Live Analysis page, click "Clear Data"
- Clears current session data only
- Requires confirmation

### Clear All History
- In Analysis History page, click "Clear All History"
- Permanently deletes all your analysis sessions
- Requires confirmation

### Clear All Data
- In Settings page, click "Clear My Data"
- Permanently deletes all your data
- Requires confirmation

## 🔒 Security Features

- **Password Protection**: All passwords are securely hashed
- **Session Management**: Secure token-based authentication
- **Data Privacy**: Your data stays on your device
- **Access Control**: Users can only access their own data

## 💰 Subscription Plans

### Free Plan - ₹0/month
- Basic face analysis
- 1 month access
- 10 analysis sessions
- Basic reports

### Pro Plan - ₹199/month
- Advanced face analysis
- Unlimited access
- Real-time feedback
- Detailed reports
- Priority support

### Student Plan - ₹99/month
- All Pro features
- Student discount
- College verification required
- Academic support

## 🛠️ Troubleshooting

### Common Issues

1. **"Python not found"**
   - Install Python from https://python.org
   - Make sure to check "Add Python to PATH"

2. **"Camera not accessible"**
   - Check camera permissions in browser
   - Close other applications using camera
   - Try refreshing the page

3. **"Dependencies failed to install"**
   - Check internet connection
   - Run: `pip install -r requirements.txt`
   - Try running as administrator

4. **"App won't start"**
   - Run the test script: `python test_app.py`
   - Check for error messages
   - Ensure all files are in the same directory

### Test the Installation
Run this command to test all components:
```bash
python test_app.py
```

## 📁 File Structure

```
ai-coach/
├── ai_coach_app.py          # Main application
├── auth.py                  # Authentication
├── database.py              # Database management
├── face_analysis.py         # Face analysis engine
├── launch_ai_coach.py       # Application launcher
├── start_ai_coach.bat       # Windows batch file
├── test_app.py              # Test script
├── requirements.txt         # Dependencies
├── README_AI_COACH_PRO.md   # Documentation
├── LAUNCH_GUIDE.md          # This file
└── ai_coach.db             # Database (created automatically)
```

## 🎉 Ready to Launch!

Your AI Coach Pro application is now ready to use! 

**Quick Start:**
1. Double-click `start_ai_coach.bat` (Windows)
2. Or run `python launch_ai_coach.py`
3. Open http://localhost:8501 in your browser
4. Register an account and start analyzing!

**Features Available:**
- ✅ Live video face analysis
- ✅ User authentication and security
- ✅ Subscription management
- ✅ Data clearing functionality
- ✅ Professional UI
- ✅ Student verification
- ✅ Session tracking and history

**Support:**
- Check the troubleshooting section above
- Run `python test_app.py` to diagnose issues
- Ensure all prerequisites are met

Welcome to AI Coach Pro - where presentations meet artificial intelligence! 🎯✨
