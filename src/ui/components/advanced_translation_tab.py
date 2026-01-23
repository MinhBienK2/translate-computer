"""
Advanced translation tab component
"""
import tkinter as tk
from .translation_controls import TranslationControls
from .text_areas import TextAreas


class AdvancedTranslationTab:
    """Advanced translation tab with controls and text areas"""
    
    def __init__(self, parent, translator, pronunciation_manager, callbacks):
        """
        Initialize advanced translation tab
        
        Args:
            parent: Parent widget
            translator: Translator instance
            pronunciation_manager: PronunciationManager instance
            callbacks: Dict with callbacks:
                - on_status_update
                - on_translate
                - on_source_lang_change
                - on_target_lang_change
                - on_swap
        """
        self.parent = parent
        self.translator = translator
        self.pronunciation_manager = pronunciation_manager
        self.callbacks = callbacks
        
        # Colors
        self.bg_color = "#FFFFFF"
        self.border_color = "#DEE2E6"
        self.text_color = "#212529"
        self.accent_color = "#0D6EFD"
        self.secondary_color = "#6C757D"
        
        self.widgets = {}
        self.source_lang = 'en'
        self.target_lang = 'vi'
        self.current_translation_source = "google"
        
        self._create_tab()
    
    def _create_tab(self):
        """Create tab content"""
        # Translation controls
        controls_callbacks = {
            'on_source_lang_change': self._on_source_lang_change,
            'on_target_lang_change': self._on_target_lang_change,
            'on_swap': self._swap_languages,
            'on_translate': self._translate,
            'on_ai_explain': None,
            'on_status_update': self.callbacks.get('on_status_update')
        }
        self.controls = TranslationControls(
            self.parent,
            self.bg_color,
            self.accent_color,
            self.text_color,
            controls_callbacks
        )
        
        # Text areas
        text_areas_callbacks = {
            'on_char_count_update': self._update_char_count,
            'on_pronounce_source': self._pronounce_source,
            'on_copy_source': self._copy_source,
            'on_copy_translation': self._copy_translation
        }
        self.text_areas = TextAreas(
            self.parent,
            self.bg_color,
            self.border_color,
            self.text_color,
            self.accent_color,
            self.secondary_color,
            text_areas_callbacks
        )
        
        # Translation source tabs
        source_tabs_frame = tk.Frame(self.parent, bg=self.bg_color)
        source_tabs_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.widgets['google_tab'] = tk.Button(
            source_tabs_frame,
            text="Google",
            command=lambda: self._switch_translation_source("google"),
            bg=self.accent_color,
            fg="#FFFFFF",
            font=('Segoe UI', 9),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=5
        )
        self.widgets['google_tab'].pack(side=tk.LEFT, padx=(0, 5))
        
        self.widgets['microsoft_tab'] = tk.Button(
            source_tabs_frame,
            text="Microsoft",
            command=lambda: self._switch_translation_source("microsoft"),
            bg="#E9ECEF",
            fg=self.text_color,
            font=('Segoe UI', 9),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=5
        )
        self.widgets['microsoft_tab'].pack(side=tk.LEFT, padx=(0, 5))
        
        self.widgets['ai_tab'] = tk.Button(
            source_tabs_frame,
            text="AI",
            command=lambda: self._switch_translation_source("ai"),
            bg="#E9ECEF",
            fg=self.text_color,
            font=('Segoe UI', 9),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=5
        )
        self.widgets['ai_tab'].pack(side=tk.LEFT, padx=(0, 5))
        
        self.widgets['ipa_tab'] = tk.Button(
            source_tabs_frame,
            text="IPA",
            command=lambda: self._switch_translation_source("ipa"),
            bg="#E9ECEF",
            fg=self.text_color,
            font=('Segoe UI', 9),
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=5
        )
        self.widgets['ipa_tab'].pack(side=tk.LEFT)
        
        # Bind Ctrl+Enter to translate
        self.text_areas.widgets['input_text'].bind('<Control-Return>', lambda e: self._translate())
    
    def _switch_translation_source(self, source):
        """Switch translation source (Google, Microsoft, AI, IPA)"""
        self.current_translation_source = source
        
        # Update tab styles
        tabs = {
            'google': self.widgets['google_tab'],
            'microsoft': self.widgets['microsoft_tab'],
            'ai': self.widgets['ai_tab'],
            'ipa': self.widgets['ipa_tab']
        }
        
        for name, tab in tabs.items():
            if name == source:
                tab.config(bg="#0D6EFD", fg="#FFFFFF")
            else:
                tab.config(bg="#E9ECEF", fg="#212529")
        
        # Re-translate if there's content
        input_text = self.text_areas.get_input_text()
        if input_text and self.text_areas.get_output_text():
            self._translate()
    
    def _on_source_lang_change(self, event=None):
        """Handle source language change"""
        self.source_lang = self.controls.get_source_lang()
    
    def _on_target_lang_change(self, event=None):
        """Handle target language change"""
        self.target_lang = self.controls.get_target_lang()
    
    def _swap_languages(self):
        """Swap source and target languages"""
        # Swap language codes
        self.source_lang, self.target_lang = self.target_lang, self.source_lang
        
        # Update dropdowns
        self.controls.swap_languages()
        
        # Swap input and output text
        input_text = self.text_areas.get_input_text()
        output_text = self.text_areas.get_output_text()
        
        self.text_areas.set_input_text(output_text)
        self.text_areas.set_output_text(input_text)
        
        self._update_char_count()
        self.callbacks.get('on_status_update', lambda x: None)("Languages swapped")
    
    def _update_char_count(self, event=None):
        """Update character counter"""
        self.text_areas.update_char_count()
    
    def _translate(self):
        """Translate input text"""
        input_text = self.text_areas.get_input_text()
        
        if not input_text:
            self.callbacks.get('on_status_update', lambda x: None)("Please enter text to translate")
            return
        
        self.callbacks.get('on_status_update', lambda x: None)(f"Translating with {self.current_translation_source.capitalize()}...")
        
        # Call the main translate callback
        self.callbacks.get('on_translate')(input_text, self.source_lang, self.target_lang)
    
    def _pronounce_source(self):
        """Pronounce source text"""
        text = self.text_areas.get_input_text()
        if text:
            self.pronunciation_manager.speak(text, self.source_lang)
            self.callbacks.get('on_status_update', lambda x: None)("Pronouncing source text...")
        else:
            self.callbacks.get('on_status_update', lambda x: None)("No text to pronounce")
    
    def _copy_source(self):
        """Copy source text to clipboard"""
        import pyperclip
        text = self.text_areas.get_input_text()
        if text:
            try:
                pyperclip.copy(text)
                self.callbacks.get('on_status_update', lambda x: None)("Source text copied to clipboard")
            except:
                self.callbacks.get('on_status_update', lambda x: None)("Failed to copy to clipboard")
        else:
            self.callbacks.get('on_status_update', lambda x: None)("No text to copy")
    
    def _copy_translation(self):
        """Copy translation to clipboard"""
        import pyperclip
        text = self.text_areas.get_output_text()
        if text:
            try:
                pyperclip.copy(text)
                self.callbacks.get('on_status_update', lambda x: None)("Translation copied to clipboard")
            except:
                self.callbacks.get('on_status_update', lambda x: None)("Failed to copy to clipboard")
        else:
            self.callbacks.get('on_status_update', lambda x: None)("No translation to copy")
    
    def set_input_text(self, text):
        """Set input text programmatically"""
        self.text_areas.set_input_text(text)
        self._update_char_count()
        self._translate()
