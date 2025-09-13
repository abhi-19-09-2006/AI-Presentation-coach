# 🎯 AI Coach Pro - Professional Presentation Analysis Platform

A comprehensive AI-powered presentation analysis platform with live video face analysis, user authentication, and subscription management.

## ✨ Features

### 🎭 Live Face Analysis
- Real-time emotion detection during presentations
- Movement and engagement analysis
- Live feedback and suggestions
- Hardware-accelerated processing for smooth performance

### 🔐 Secure Authentication
- User registration and login system
- Password hashing with salt for security
- Session management with token-based authentication
- Account protection against unauthorized access

### 💳 Subscription Management
- **Free Plan**: Basic analysis, 1 month access, 10 sessions
- **Pro Plan**: ₹199/month - Unlimited access, advanced features
- **Student Plan**: ₹99/month - All Pro features with college verification

### 📊 Advanced Analytics
- Detailed performance metrics
- Session history and tracking
- Comprehensive reports and insights
- Trend analysis over time

### 🎓 Student Verification
- Special pricing for students
- College ID verification system
- Academic support features

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam access
- Modern web browser

### Installation

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd ai-coach
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**
   ```bash
   python launch_ai_coach.py
   ```
   
   Or directly with Streamlit:
   ```bash
   streamlit run ai_coach_app.py
   ```

4. **Access the app**
   - Open your browser to `http://localhost:8501`
   - Register a new account or login
   - Start your first live analysis!

## 📁 Project Structure

```
ai-coach/
├── ai_coach_app.py          # Main application
├── auth.py                  # Authentication module
├── database.py              # Database management
├── face_analysis.py         # Face analysis engine
├── realtime_analysis.py     # Real-time analysis manager
├── launch_ai_coach.py       # Application launcher
├── requirements.txt         # Dependencies
├── README_AI_COACH_PRO.md   # This file
└── ai_coach.db             # SQLite database (created automatically)
```

## 🔧 Configuration

### Database
The app uses SQLite for data storage. The database file (`ai_coach.db`) is created automatically on first run.

### Camera Settings
- Default camera index: 0
- Resolution: Auto-detected
- Frame rate: Optimized for 10 FPS analysis

### Security Settings
- Password hashing: PBKDF2 with SHA-256
- Session tokens: 32-byte URL-safe tokens
- Session expiry: 24 hours

## 🎯 Usage Guide

### 1. Account Setup
- Register with username, email, and password
- Choose between regular or student account
- Student accounts require college name and student ID

### 2. Live Analysis
- Click "Live Analysis" in the sidebar
- Ensure camera permissions are granted
- Click "Start Analysis" to begin
- View real-time metrics and feedback
- Click "Stop Analysis" when finished

### 3. Viewing Results
- Check "Analysis History" for past sessions
- View detailed metrics and insights
- Track performance over time

### 4. Subscription Management
- Access "Subscription" to view current plan
- Upgrade to Pro or Student plans
- Monitor usage and remaining sessions

## 🔒 Security Features

### Authentication Security
- Passwords are hashed using PBKDF2 with SHA-256
- Each password has a unique salt
- Session tokens are cryptographically secure
- Automatic session expiry

### Data Protection
- User data is stored securely in SQLite
- No sensitive data is logged
- Camera access is only used for analysis
- No data is sent to external servers

### Access Control
- Users can only access their own data
- Subscription-based feature access
- Secure session management

## 💰 Pricing Plans

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

## 🛠️ Technical Details

### Face Analysis Engine
- Uses OpenCV for face detection
- DeepFace for emotion analysis
- Hardware-accelerated processing
- Optimized for real-time performance

### Database Schema
- Users table with authentication data
- Sessions table for security
- Analysis sessions for tracking
- Subscription plans configuration

### Performance Optimization
- Frame skipping for better performance
- Caching for repeated analysis
- Hardware acceleration when available
- Memory-efficient data structures

## 🐛 Troubleshooting

### Common Issues

1. **Camera not detected**
   - Check camera permissions
   - Ensure camera is not used by another application
   - Try different camera index in code

2. **Analysis not working**
   - Verify all dependencies are installed
   - Check if DeepFace models are downloaded
   - Ensure sufficient lighting

3. **Login issues**
   - Verify username and password
   - Check if account is active
   - Clear browser cache if needed

4. **Performance issues**
   - Close other applications using camera
   - Reduce analysis frame rate
   - Check system resources

### Getting Help
- Check the console for error messages
- Verify all requirements are installed
- Ensure camera permissions are granted
- Check system compatibility

## 🔄 Updates and Maintenance

### Database Maintenance
- Database is automatically maintained
- No manual intervention required
- Regular cleanup of expired sessions

### Performance Monitoring
- Built-in performance metrics
- Automatic optimization
- Resource usage tracking

## 📝 License

This project is proprietary software. All rights reserved.

## 🤝 Support

For technical support or questions:
- Check the troubleshooting section
- Review error messages in console
- Ensure all dependencies are properly installed

## 🎉 Getting Started

1. **Install the application** following the installation guide
2. **Create an account** with your details
3. **Start your first analysis** to see AI Coach in action
4. **Explore the features** and upgrade as needed

Welcome to AI Coach Pro - where presentations meet artificial intelligence! 🎯✨
