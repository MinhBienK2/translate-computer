"""
Module xử lý phát âm (text-to-speech)
"""
import pyttsx3
import threading


class PronunciationManager:
    """Quản lý phát âm text"""
    
    def __init__(self):
        """Khởi tạo PronunciationManager"""
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """Khởi tạo TTS engine"""
        try:
            self.engine = pyttsx3.init()
            # Cấu hình giọng nói
            voices = self.engine.getProperty('voices')
            if voices:
                # Tìm giọng nói tiếng Anh (nếu có)
                for voice in voices:
                    if 'english' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            # Tốc độ nói
            self.engine.setProperty('rate', 150)
            # Âm lượng
            self.engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"Lỗi khi khởi tạo TTS engine: {e}")
            self.engine = None
    
    def speak(self, text, language='en'):
        """
        Phát âm text
        
        Args:
            text: Text cần phát âm
            language: Ngôn ngữ ('en' hoặc 'vi')
        """
        if self.engine is None:
            return
        
        try:
            # Chạy trong thread riêng để không block UI
            thread = threading.Thread(target=self._speak_thread, args=(text, language))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Lỗi khi phát âm: {e}")
    
    def _speak_thread(self, text, language):
        """Thread phát âm"""
        try:
            # Cố gắng set giọng nói phù hợp với ngôn ngữ
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
            print(f"Lỗi trong thread phát âm: {e}")
    
    def stop(self):
        """Dừng phát âm"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

