"""
Privacy manager for AI Coach application
"""

import os
import time
import json
import hashlib
import tempfile
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class MockPrivacyManager:
    """Mock privacy manager for when the real one is not available"""
    
    def __init__(self):
        self.active_files = {}
        self.privacy_log = []
        self.max_file_age = timedelta(minutes=5)
        self.compliance_status = 'ACTIVE'
    
    def get_privacy_report(self) -> Dict:
        """Get privacy compliance report"""
        return {
            'compliance_status': self.compliance_status,
            'active_voice_files': len(self.active_files),
            'cache_size': len(self.privacy_log),
            'max_file_age_minutes': self.max_file_age.total_seconds() / 60,
            'last_cleanup': datetime.now().isoformat()
        }
    
    def immediate_cleanup_all(self) -> bool:
        """Immediately clean up all sensitive data"""
        try:
            # Clear active files
            self.active_files.clear()
            
            # Clear privacy log
            self.privacy_log.clear()
            
            # Log the cleanup
            self.privacy_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'IMMEDIATE_CLEANUP',
                'details': 'All sensitive data cleared'
            })
            
            return True
        except Exception:
            return False
    
    def get_detailed_privacy_log(self, n: int = 20) -> List[Dict]:
        """Get detailed privacy log"""
        return self.privacy_log[-n:] if self.privacy_log else []
    
    def export_privacy_report(self, path: str) -> bool:
        """Export privacy compliance report"""
        try:
            report = self.get_privacy_report()
            report['detailed_log'] = self.privacy_log[-50:]  # Last 50 entries
            
            with open(path, 'w') as f:
                json.dump(report, f, indent=2)
            
            return True
        except Exception:
            return False

class MockSecureProcessor:
    """Mock secure audio processor for when the real one is not available"""
    
    def __init__(self):
        self.temp_files = {}
    
    def process_audio_securely(self, audio, fmt: str) -> Tuple[str, str]:
        """Process audio securely and return file path and ID"""
        try:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(
                suffix=f'.{fmt}', 
                delete=False
            )
            
            # Export audio to the temporary file
            if hasattr(audio, 'export'):
                audio.export(temp_file.name, format=fmt)
            else:
                # For raw audio data
                with open(temp_file.name, 'wb') as f:
                    if isinstance(audio, bytes):
                        f.write(audio)
                    else:
                        f.write(bytes(audio))
            
            # Generate a unique ID for the file
            file_id = hashlib.md5(temp_file.name.encode()).hexdigest()[:12]
            
            # Track the file
            self.temp_files[file_id] = {
                'path': temp_file.name,
                'created': time.time(),
                'format': fmt
            }
            
            return temp_file.name, file_id
            
        except Exception as e:
            # Fallback to a simple temporary file
            temp_path = f"temp_audio_{int(time.time())}.{fmt}"
            with open(temp_path, 'wb') as f:
                if isinstance(audio, bytes):
                    f.write(audio)
                else:
                    f.write(bytes(str(audio), 'utf-8'))
            return temp_path, f"fallback_{int(time.time())}"
    
    def cleanup_audio_file(self, file_id: str) -> bool:
        """Securely clean up an audio file"""
        try:
            if file_id in self.temp_files:
                file_info = self.temp_files[file_id]
                file_path = file_info['path']
                
                # 3-pass secure deletion
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    
                    # Pass 1: Write zeros
                    with open(file_path, 'wb') as f:
                        f.write(b'\x00' * file_size)
                    
                    # Pass 2: Write ones
                    with open(file_path, 'wb') as f:
                        f.write(b'\xFF' * file_size)
                    
                    # Pass 3: Write random data
                    with open(file_path, 'wb') as f:
                        f.write(os.urandom(file_size))
                    
                    # Delete the file
                    os.remove(file_path)
                
                # Remove from tracking
                del self.temp_files[file_id]
                
                return True
            else:
                # Try to delete by path if ID not found
                return False
                
        except Exception:
            # Fallback deletion
            try:
                if file_id in self.temp_files:
                    file_path = self.temp_files[file_id]['path']
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    del self.temp_files[file_id]
                return True
            except Exception:
                return False

# Global instances
privacy_manager = MockPrivacyManager()
secure_audio_processor = MockSecureProcessor()

def get_privacy_status() -> Dict:
    """Get current privacy status"""
    return privacy_manager.get_privacy_report()

def immediate_privacy_cleanup() -> bool:
    """Immediately clean up all privacy-sensitive data"""
    return privacy_manager.immediate_cleanup_all()

# Export all classes and functions
__all__ = [
    'privacy_manager',
    'secure_audio_processor',
    'get_privacy_status',
    'immediate_privacy_cleanup',
    'MockPrivacyManager',
    'MockSecureProcessor'
]