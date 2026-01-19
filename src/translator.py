"""
Module dịch thuật và lấy thông tin từ điển
"""
from deep_translator import GoogleTranslator
import requests
import json


class Translator:
    """Quản lý dịch thuật và thông tin từ điển"""
    
    def __init__(self, source_lang='en', target_lang='vi'):
        """
        Khởi tạo Translator
        
        Args:
            source_lang: Ngôn ngữ nguồn (mặc định: 'en')
            target_lang: Ngôn ngữ đích (mặc định: 'vi')
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translator = GoogleTranslator(source=source_lang, target=target_lang)
    
    def detect_language(self, text):
        """
        Tự động phát hiện ngôn ngữ của text
        
        Args:
            text: Text cần phát hiện ngôn ngữ
            
        Returns:
            str: Mã ngôn ngữ (ví dụ: 'en', 'vi')
        """
        try:
            detected = GoogleTranslator().detect(text)
            return detected
        except:
            return 'en'  # Mặc định là tiếng Anh
    
    def translate(self, text, source_lang=None, target_lang=None):
        """
        Dịch text sang ngôn ngữ đích
        
        Args:
            text: Text cần dịch
            source_lang: Ngôn ngữ nguồn (None để tự động phát hiện)
            target_lang: Ngôn ngữ đích (None để dùng mặc định)
            
        Returns:
            str: Text đã dịch
        """
        try:
            if source_lang is None:
                source_lang = self.detect_language(text)
            
            if target_lang is None:
                target_lang = self.target_lang
            
            # Nếu ngôn ngữ nguồn và đích giống nhau, không cần dịch
            if source_lang == target_lang:
                return text
            
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated = translator.translate(text)
            return translated
        except Exception as e:
            print(f"Lỗi khi dịch: {e}")
            return text
    
    def get_word_definitions(self, word, source_lang='en'):
        """
        Lấy định nghĩa và các nghĩa của từ (sử dụng Free Dictionary API)
        
        Args:
            word: Từ cần tra cứu
            source_lang: Ngôn ngữ của từ
            
        Returns:
            dict: Thông tin định nghĩa với các parts of speech
        """
        try:
            # Free Dictionary API
            url = f"https://api.dictionaryapi.dev/api/v2/entries/{source_lang}/{word.lower()}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    meanings = {}
                    entry = data[0]
                    
                    # Lấy các nghĩa theo từng loại từ
                    if 'meanings' in entry:
                        for meaning in entry['meanings']:
                            part_of_speech = meaning.get('partOfSpeech', '')
                            definitions = []
                            
                            for definition in meaning.get('definitions', []):
                                def_text = definition.get('definition', '')
                                if def_text:
                                    definitions.append(def_text)
                            
                            if definitions:
                                meanings[part_of_speech] = definitions
                    
                    return {
                        'word': entry.get('word', word),
                        'phonetic': entry.get('phonetic', ''),
                        'meanings': meanings
                    }
        except Exception as e:
            print(f"Lỗi khi lấy định nghĩa: {e}")
        
        return None
    
    def get_translation_info(self, text):
        """
        Lấy đầy đủ thông tin dịch và định nghĩa cho text
        
        Args:
            text: Text cần dịch
            
        Returns:
            dict: Thông tin đầy đủ bao gồm translation, definitions, etc.
        """
        # Phát hiện ngôn ngữ
        detected_lang = self.detect_language(text)
        
        # Xác định ngôn ngữ đích (nếu là tiếng Anh thì dịch sang tiếng Việt, ngược lại)
        if detected_lang == 'vi':
            target_lang = 'en'
        else:
            target_lang = 'vi'
        
        # Dịch text
        translated = self.translate(text, source_lang=detected_lang, target_lang=target_lang)
        
        # Lấy định nghĩa nếu là một từ đơn (không có khoảng trắng)
        definitions = None
        if len(text.split()) == 1 and detected_lang == 'en':
            definitions = self.get_word_definitions(text, detected_lang)
        
        return {
            'original_text': text,
            'source_language': detected_lang,
            'target_language': target_lang,
            'translation': translated,
            'definitions': definitions
        }

