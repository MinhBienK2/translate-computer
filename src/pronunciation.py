"""
Module for handling pronunciation (text-to-speech)
"""
import pyttsx3
import threading


class PronunciationManager:
    """Manages text pronunciation"""
    
    def __init__(self):
        """Initialize PronunciationManager"""
        self.lock = threading.Lock()  # Lock to prevent concurrent pronunciation
        self.current_engine = None
    
    def speak(self, text, language='en'):
        """
        Pronounce text
        
        Args:
            text: Text to pronounce
            language: Language ('en' or 'vi')
        """
        if not text or not text.strip():
            return
        
        try:
            # Run in separate thread to avoid blocking UI
            thread = threading.Thread(target=self._speak_thread, args=(text, language))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error pronouncing: {e}")
    
    def _speak_thread(self, text, language):
        """Pronunciation thread - creates new engine instance for each call"""
        # Use lock to prevent concurrent pronunciation
        if not self.lock.acquire(blocking=False):
            # If another pronunciation is running, skip this one
            return
        
        engine = None
        try:
            # Create a new engine instance for this thread to avoid "run loop already started" error
            engine = pyttsx3.init()
            
            # Configure voice based on language
            voices = engine.getProperty('voices')
            if voices:
                voice_found = False
                if language == 'en':
                    # For English, prioritize English voices
                    # Try to find English voice (check for 'english' in name)
                    for voice in voices:
                        voice_name_lower = voice.name.lower()
                        if 'english' in voice_name_lower or 'en' in voice_name_lower:
                            engine.setProperty('voice', voice.id)
                            voice_found = True
                            break
                    
                    # If no English voice found, use first available voice (usually default is English on Windows)
                    if not voice_found and voices:
                        engine.setProperty('voice', voices[0].id)
                elif language == 'vi':
                    # For Vietnamese, try to find Vietnamese voice
                    for voice in voices:
                        voice_name_lower = voice.name.lower()
                        if 'vietnamese' in voice_name_lower or 'vi' in voice_name_lower:
                            engine.setProperty('voice', voice.id)
                            voice_found = True
                            break
                    
                    # If Vietnamese voice not found, use default
                    if not voice_found and voices:
                        engine.setProperty('voice', voices[0].id)
                else:
                    # For other languages, use default voice
                    if voices:
                        engine.setProperty('voice', voices[0].id)
            
            # Speech rate
            engine.setProperty('rate', 150)
            # Volume
            engine.setProperty('volume', 0.9)
            
            # Pronounce text
            engine.say(text)
            engine.runAndWait()
            
        except Exception as e:
            print(f"Error in pronunciation thread: {e}")
        finally:
            # Clean up engine
            if engine:
                try:
                    engine.stop()
                except:
                    pass
            # Release lock
            self.lock.release()
    
    def stop(self):
        """Stop pronunciation"""
        # The lock will prevent new pronunciations, and existing ones will finish naturally
        pass

