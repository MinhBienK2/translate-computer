"""
Module for translation and getting dictionary information
"""
from deep_translator import GoogleTranslator
import requests
import json


class Translator:
    """Manages translation and dictionary information"""
    
    def __init__(self, source_lang='en', target_lang='vi'):
        """
        Initialize Translator
        
        Args:
            source_lang: Source language (default: 'en')
            target_lang: Target language (default: 'vi')
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translator = GoogleTranslator(source=source_lang, target=target_lang)
    
    def detect_language(self, text):
        """
        Automatically detect the language of text
        
        Args:
            text: Text to detect language for
            
        Returns:
            str: Language code (e.g., 'en', 'vi')
        """
        try:
            detected = GoogleTranslator().detect(text)
            return detected
        except:
            return 'en'  # Default to English
    
    def translate(self, text, source_lang=None, target_lang=None):
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            source_lang: Source language (None to auto-detect)
            target_lang: Target language (None to use default)
            
        Returns:
            str: Translated text
        """
        try:
            if source_lang is None:
                source_lang = self.detect_language(text)
            
            if target_lang is None:
                target_lang = self.target_lang
            
            # If source and target languages are the same, no need to translate
            if source_lang == target_lang:
                return text
            
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated = translator.translate(text)
            return translated
        except Exception as e:
            print(f"Error translating: {e}")
            return text
    
    def get_word_definitions(self, word, source_lang='en'):
        """
        Get word definitions and meanings (using Free Dictionary API)
        
        Args:
            word: Word to look up
            source_lang: Language of the word
            
        Returns:
            dict: Definition information with parts of speech
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
                    
                    # Get meanings by part of speech
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
            print(f"Error getting definitions: {e}")
        
        return None
    
    def get_translation_info(self, text):
        """
        Get complete translation and definition information for text
        
        Args:
            text: Text to translate
            
        Returns:
            dict: Complete information including translation, definitions, etc.
        """
        # Detect language
        detected_lang = self.detect_language(text)
        
        # Determine target language (if English, translate to Vietnamese, otherwise)
        if detected_lang == 'vi':
            target_lang = 'en'
        else:
            target_lang = 'vi'
        
        # Translate text
        translated = self.translate(text, source_lang=detected_lang, target_lang=target_lang)
        
        # Get definitions if it's a single word (no spaces)
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

