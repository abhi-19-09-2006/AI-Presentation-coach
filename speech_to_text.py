"""Enhanced Speech-to-Text Module for AI Coach

Provides robust audio transcription with multiple fallback options:
- OpenAI Whisper (primary)
- SpeechRecognition library (fallback)
- Audio format validation and conversion
- Enhanced error handling and logging
"""

import os
import warnings
import tempfile
from typing import Optional, Tuple
from pathlib import Path

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings

# Audio processing libraries
try:
    import librosa
    import numpy as np
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

try:
    from pydub import AudioSegment
    from pydub.utils import which
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

# Primary transcription engine
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# Fallback transcription engine
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

class EnhancedTranscriber:
    """Enhanced transcriber with multiple engines and robust error handling"""
    
    def __init__(self):
        self.whisper_model = None
        self.sr_recognizer = None
        self.supported_formats = {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.webm'}
        
        # Initialize Whisper if available
        if WHISPER_AVAILABLE:
            try:
                self.whisper_model = whisper.load_model("base", device="cpu")
                print("✅ Whisper model loaded successfully")
            except Exception as e:
                print(f"⚠️ Whisper model loading failed: {e}")
                self.whisper_model = None
        
        # Initialize SpeechRecognition if available
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.sr_recognizer = sr.Recognizer()
                self.sr_recognizer.energy_threshold = 300
                self.sr_recognizer.dynamic_energy_threshold = True
                print("✅ SpeechRecognition initialized")
            except Exception as e:
                print(f"⚠️ SpeechRecognition initialization failed: {e}")
    
    def validate_audio_file(self, file_path: str) -> Tuple[bool, str]:
        """Validate audio file exists and has basic requirements"""
        try:
            path = Path(file_path)
            
            # Check if file exists
            if not path.exists():
                return False, "Audio file not found"
            
            # Check file size
            file_size = path.stat().st_size
            if file_size < 1000:  # Less than 1KB
                return False, "Audio file too small (less than 1KB)"
            
            if file_size > 50 * 1024 * 1024:  # More than 50MB
                return False, "Audio file too large (over 50MB)"
            
            # Check file extension
            if path.suffix.lower() not in self.supported_formats:
                return False, f"Unsupported format {path.suffix}. Supported: {', '.join(self.supported_formats)}"
            
            return True, "Audio file validation passed"
            
        except Exception as e:
            return False, f"File validation error: {str(e)}"
    
    def load_and_validate_audio(self, file_path: str) -> Tuple[Optional[np.ndarray], int, str]:
        """Load audio file and validate content"""
        try:
            if LIBROSA_AVAILABLE:
                # Use librosa for better audio loading
                audio, sr = librosa.load(file_path, sr=16000)
                
                # Validate audio content
                if len(audio) == 0:
                    return None, 0, "Empty audio detected"
                
                # Check minimum duration (0.1 seconds)
                if len(audio) < sr * 0.1:
                    return None, 0, "Audio too short for analysis (minimum 0.1 seconds)"
                
                # Check for silence (all values near zero)
                if np.max(np.abs(audio)) < 0.001:
                    return None, 0, "Audio appears to be silent"
                
                return audio, sr, "Audio loaded successfully"
            
            elif PYDUB_AVAILABLE:
                # Fallback to pydub
                audio_segment = AudioSegment.from_file(file_path)
                
                if len(audio_segment) < 100:  # Less than 0.1 seconds
                    return None, 0, "Audio too short for analysis"
                
                # Convert to numpy array (simplified)
                samples = audio_segment.get_array_of_samples()
                audio = np.array(samples).astype(np.float32)
                
                if len(audio) > 0:
                    audio = audio / np.max(np.abs(audio))  # Normalize
                
                return audio, audio_segment.frame_rate, "Audio loaded with pydub"
            
            else:
                return None, 0, "No audio loading libraries available"
                
        except Exception as e:
            return None, 0, f"Audio loading error: {str(e)}"
    
    def transcribe_with_whisper(self, file_path: str) -> Tuple[str, bool]:
        """Transcribe using Whisper model"""
        if not self.whisper_model:
            return "Whisper model not available", False
        
        try:
            # Transcribe with Whisper
            result = self.whisper_model.transcribe(
                file_path,
                language="en",  # Force English for consistency
                task="transcribe",
                temperature=0.0,  # Deterministic output
                best_of=1,  # Faster processing
                beam_size=1,  # Faster processing
                patience=1.0,
                length_penalty=1.0,
                suppress_tokens="-1",
                initial_prompt=None,
                condition_on_previous_text=False,
                fp16=False,  # Better compatibility
                compression_ratio_threshold=2.4,
                logprob_threshold=-1.0,
                no_speech_threshold=0.6
            )
            
            # Validate result
            if not isinstance(result, dict) or "text" not in result:
                return "Invalid Whisper result format", False
            
            text = str(result["text"]).strip() if result["text"] else ""
            
            if not text:
                return "No speech detected in audio", False
            
            # Basic text validation
            if len(text) < 2:
                return "Transcription too short", False
            
            return text, True
            
        except Exception as e:
            return f"Whisper transcription error: {str(e)}", False
    
    def transcribe_with_speech_recognition(self, file_path: str) -> Tuple[str, bool]:
        """Transcribe using SpeechRecognition library as fallback"""
        if not self.sr_recognizer:
            return "SpeechRecognition not available", False
        
        try:
            # Convert audio to WAV if needed
            wav_path = file_path
            if not file_path.lower().endswith('.wav') and PYDUB_AVAILABLE:
                try:
                    audio = AudioSegment.from_file(file_path)
                    wav_path = file_path.replace(Path(file_path).suffix, '_temp.wav')
                    audio.export(wav_path, format="wav")
                except Exception:
                    pass  # Use original file
            
            # Load audio file
            with sr.AudioFile(wav_path) as source:
                # Adjust for ambient noise
                self.sr_recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio_data = self.sr_recognizer.record(source)
            
            # Try multiple recognition engines
            engines = [
                ('Google', lambda: self.sr_recognizer.recognize_google(audio_data)),
                ('Sphinx', lambda: self.sr_recognizer.recognize_sphinx(audio_data)),
            ]
            
            for engine_name, recognize_func in engines:
                try:
                    text = recognize_func()
                    if text and len(text.strip()) > 1:
                        return text.strip(), True
                except Exception as e:
                    print(f"⚠️ {engine_name} engine failed: {e}")
                    continue
            
            return "All speech recognition engines failed", False
            
        except Exception as e:
            return f"SpeechRecognition error: {str(e)}", False
        
        finally:
            # Clean up temporary WAV file
            if wav_path != file_path and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except Exception:
                    pass
    
    def transcribe(self, file_path: str) -> str:
        """Main transcription method with fallback chain"""
        # Validate input
        if not file_path:
            return "No file path provided"
        
        # Validate file
        is_valid, validation_msg = self.validate_audio_file(file_path)
        if not is_valid:
            return validation_msg
        
        # Load and validate audio content
        audio_data, sample_rate, load_msg = self.load_and_validate_audio(file_path)
        if audio_data is None:
            return load_msg
        
        # Try Whisper first (primary engine)
        if WHISPER_AVAILABLE and self.whisper_model:
            text, success = self.transcribe_with_whisper(file_path)
            if success:
                return text
            else:
                print(f"⚠️ Whisper failed: {text}")
        
        # Try SpeechRecognition as fallback
        if SPEECH_RECOGNITION_AVAILABLE and self.sr_recognizer:
            text, success = self.transcribe_with_speech_recognition(file_path)
            if success:
                return text
            else:
                print(f"⚠️ SpeechRecognition failed: {text}")
        
        # All engines failed
        return "Transcription failed: No working speech recognition engines available"


# Global transcriber instance
_transcriber = None

def get_transcriber() -> EnhancedTranscriber:
    """Get singleton transcriber instance"""
    global _transcriber
    if _transcriber is None:
        _transcriber = EnhancedTranscriber()
    return _transcriber

def transcribe_audio(file_path: str) -> str:
    """Main transcription function - enhanced with robust error handling"""
    try:
        transcriber = get_transcriber()
        result = transcriber.transcribe(file_path)
        
        # Log successful transcription
        if not result.startswith(("Audio file", "Empty audio", "Audio too short", 
                                "Audio loading error", "Transcription error", 
                                "No speech detected", "Transcription failed")):
            print(f"✅ Transcription successful: {len(result)} characters")
        
        return result
        
    except Exception as e:
        error_msg = f"Transcription system error: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


def test_transcription_system() -> bool:
    """Test the transcription system components"""
    print("🧪 Testing Speech-to-Text System...")
    
    # Check available engines
    engines = []
    if WHISPER_AVAILABLE:
        engines.append("✅ OpenAI Whisper")
    else:
        engines.append("❌ OpenAI Whisper (not available)")
    
    if SPEECH_RECOGNITION_AVAILABLE:
        engines.append("✅ SpeechRecognition")
    else:
        engines.append("❌ SpeechRecognition (not available)")
    
    if LIBROSA_AVAILABLE:
        engines.append("✅ Librosa audio processing")
    else:
        engines.append("❌ Librosa (not available)")
    
    if PYDUB_AVAILABLE:
        engines.append("✅ Pydub audio processing")
    else:
        engines.append("❌ Pydub (not available)")
    
    print("Available components:")
    for engine in engines:
        print(f"  {engine}")
    
    # Test transcriber initialization
    try:
        transcriber = get_transcriber()
        print("✅ Transcriber initialized successfully")
        
        # Basic functionality test
        if transcriber.whisper_model or transcriber.sr_recognizer:
            print("✅ At least one transcription engine is ready")
            return True
        else:
            print("⚠️ No transcription engines available")
            return False
            
    except Exception as e:
        print(f"❌ Transcriber initialization failed: {e}")
        return False


if __name__ == "__main__":
    # Run system test when module is executed directly
    test_transcription_system()
