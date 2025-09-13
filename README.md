# AI Coach - Professional Voice Analysis Platform

A modern, professional voice analysis platform with advanced features for voice coaching, presentation training, and communication improvement.

## ✨ Features

### 🎤 Voice Analysis
- **Advanced Speech-to-Text**: OpenAI Whisper + SpeechRecognition fallback
- **Comprehensive Text Analysis**: Real NLP-based scoring with 14+ metrics
- **Speaking Pace Analysis**: WPM calculation with optimization tips
- **Multi-format Audio Support**: WAV, MP3, M4A, FLAC, OGG, WebM

### 🎭 Advanced Analytics
- **Face Emotion Analysis**: Real-time emotion and movement detection
- **Performance Tracking**: Session history and improvement trends
- **Custom Scoring**: Context-aware feedback for different speaking scenarios
- **Interactive Visualizations**: Radar charts, trend analysis, live dashboards

### 🎨 Professional UI
- **8 Professional Themes**: Dark/Light modes with custom color schemes
- **Responsive Design**: Optimized for all screen sizes
- **Real-time Feedback**: Live performance indicators
- **Export Options**: PDF reports with detailed analysis

### 🔒 Privacy & Security
- **Auto-deletion**: Voice and face data deleted after analysis
- **Secure Processing**: 3-pass file overwriting for complete removal
- **Privacy Dashboard**: Real-time compliance monitoring
- **GDPR Compliant**: Meets data protection requirements

## 🚀 Quick Start

### Method 1: Easy Launcher (Recommended)
```bash
# Windows users - double-click:
start_ai_coach.bat

# Or run the Python launcher:
python run_ai_coach.py
```

### Method 2: Direct Streamlit
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Method 3: Development Mode
```bash
# Install in development mode
pip install -e .

# Run with hot reload
streamlit run app.py --server.runOnSave true
```

## 📋 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for models
- **Webcam**: Optional, for face analysis

### Python Dependencies
All dependencies are automatically installed via `requirements.txt`:

**Core Framework:**
- streamlit>=1.28.0
- plotly>=5.15.0
- numpy>=1.24.0
- pandas>=2.0.0

**Audio Processing:**
- openai-whisper>=20230918
- SpeechRecognition>=3.10.0
- librosa>=0.10.0
- pydub>=0.25.1

**Text Analysis:**
- nltk>=3.8.1
- language-tool-python>=2.8.0

**Face Analysis:**
- deepface>=0.0.79
- opencv-python>=4.8.0
- tensorflow>=2.13.0

## 🎯 Usage Guide

### Basic Voice Analysis
1. **Record Audio**: Use the built-in recorder or upload audio file
2. **Select Analysis Type**: Choose focus area (Public Speaking, Interview, etc.)
3. **Run Analysis**: Get comprehensive feedback with actionable tips
4. **Export Results**: Download PDF report with detailed metrics

### Advanced Features
- **Real-time Dashboard**: Enable face analysis for live feedback
- **Performance Tracking**: Monitor improvement over multiple sessions
- **Custom Themes**: Personalize interface with 8 professional themes
- **Privacy Controls**: Monitor and control data usage

### Analysis Metrics
- **Clarity**: Pronunciation and enunciation quality
- **Vocabulary**: Word choice and diversity
- **Grammar**: Language correctness and structure
- **Confidence**: Assertiveness and conviction
- **Engagement**: Audience connection and interaction
- **Fluency**: Smoothness and flow
- **Pace**: Speaking rate optimization
- **Energy**: Enthusiasm and dynamics

## 🛠️ Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Update pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Audio Issues:**
```bash
# Install audio dependencies
pip install pyaudio soundfile
# On Windows, may need: pip install pipwin && pipwin install pyaudio
```

**Face Analysis Issues:**
```bash
# Install computer vision dependencies
pip install opencv-python tensorflow deepface
```

**Performance Issues:**
- Close other applications to free memory
- Use shorter audio clips (< 2 minutes)
- Disable face analysis if not needed
- Clear browser cache

### Module Testing
```bash
# Test individual modules
python -c "from speech_to_text import test_transcription_system; test_transcription_system()"
python -c "from text_analysis_module import analyze_text; print(analyze_text('Hello world test'))"
python -c "from face_analysis import test_face_analysis_performance; test_face_analysis_performance()"
```

## 🏗️ Architecture

### Module Structure
```
ai-coach/
├── app.py                    # Main Streamlit application
├── speech_to_text.py         # Enhanced speech recognition
├── text_analysis_module.py   # Advanced NLP analysis
├── face_analysis.py          # Computer vision features
├── optimization_utils.py     # Performance monitoring
├── privacy_manager.py        # Data protection
├── realtime_analysis.py      # Live dashboard
├── requirements.txt          # Dependencies
├── run_ai_coach.py          # Python launcher
└── start_ai_coach.bat       # Windows launcher
```

### Key Improvements Made
- **Enhanced Error Handling**: Robust fallback systems
- **Performance Optimization**: Caching and resource monitoring
- **Code Quality**: Removed duplications, improved structure
- **Real NLP Analysis**: Replaced random scoring with actual algorithms
- **Better Documentation**: Comprehensive inline comments
- **Security Features**: Privacy-first data handling
- **User Experience**: Easy launchers and clear feedback

## 🤝 Contributing

### Development Setup
```bash
# Clone and setup
git clone <repository>
cd ai-coach
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Code formatting
black . && flake8 .
```

### Adding Features
1. **New Analysis Metrics**: Extend `text_analysis_module.py`
2. **UI Themes**: Add themes in `app.py` CSS section
3. **Export Formats**: Enhance `generate_pdf_report()`
4. **Real-time Features**: Extend `realtime_analysis.py`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
1. Check the troubleshooting section above
2. Review module test functions for diagnostics
3. Check system requirements and dependencies
4. Use the built-in performance monitor for issues

## 🎉 Version History

### Latest Version (Debugged & Enhanced)
- ✅ Fixed all import and dependency issues
- ✅ Enhanced text analysis with real NLP algorithms
- ✅ Improved speech recognition with fallback systems
- ✅ Added comprehensive error handling
- ✅ Created easy-to-use launchers
- ✅ Optimized performance and resource usage
- ✅ Enhanced privacy and security features
- ✅ Improved code structure and documentation

---

**Ready to improve your communication skills? Launch AI Coach and start your journey to better speaking!** 🚀🎤