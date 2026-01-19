"""
Module for handling pronunciation (text-to-speech)
"""
import pyttsx3
import threading


class PronunciationManager:
    """Manages text pronunciation"""
    
    def __init__(self):
        """Initialize PronunciationManager"""
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize TTS engine"""
        try:
            self.engine = pyttsx3.init()
            # Configure voice
            voices = self.engine.getProperty('voices')
            if voices:
                # Find English voice (if available)
                for voice in voices:
                    if 'english' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            # Speech rate
            self.engine.setProperty('rate', 150)
            # Volume
            self.engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"Error initializing TTS engine: {e}")
            self.engine = None
    
    def speak(self, text, language='en'):
        """
        Pronounce text
        
        Args:
            text: Text to pronounce
            language: Language ('en' or 'vi')
        """
        if self.engine is None:
            return
        
        try:
            # Run in separate thread to avoid blocking UI
            thread = threading.Thread(target=self._speak_thread, args=(text, language))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error pronouncing: {e}")
    
    def _speak_thread(self, text, language):
        """Pronunciation thread"""
        try:
            # Try to set voice appropriate for language
            if self.engine:
                voices = self.engine.getProperty('voices')
                if voices:
                    for voice in voices:
                        voice_name_lower = voice.name.lower()
                        if language == 'en' and 'english' in voice_name_lower:
                            self.engine.setProperty('voice', voice.id)
                            break
                        elif language == 'vi' and 'vietnamese' in voice_name_lower:
                            self.engine.setProperty('voice', voice.id)
                            break
                
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            print(f"Error in pronunciation thread: {e}")
    
    def stop(self):
        """Stop pronunciation"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

