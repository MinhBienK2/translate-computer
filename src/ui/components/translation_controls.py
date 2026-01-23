"""
Translation controls component - language selection, swap, translate button
"""
import tkinter as tk
from tkinter import ttk


class TranslationControls:
    """Controls for language selection and translation"""
    
    def __init__(self, parent, bg_color, accent_color, text_color, callbacks):
        """
        Initialize translation controls
        
        Args:
            parent: Parent widget
            bg_color: Background color
            accent_color: Accent color
            text_color: Text color
            callbacks: Dict with callbacks:
                - on_source_lang_change
                - on_target_lang_change
                - on_swap
                - on_translate
                - on_ai_explain
                - on_status_update
        """
        self.parent = parent
        self.bg_color = bg_color
        self.accent_color = accent_color
        self.text_color = text_color
        self.callbacks = callbacks
        
        self.widgets = {}
        self._create_controls()
    
    def _create_controls(self):
        """Create control widgets"""
        control_frame = tk.Frame(self.parent, bg=self.bg_color)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Source language dropdown
        self.widgets['source_lang_var'] = tk.StringVar(value="English")
        source_lang_menu = ttk.Combobox(
            control_frame,
            textvariable=self.widgets['source_lang_var'],
            values=["English", "Vietnamese"],
            state='readonly',
            width=15,
            font=('Segoe UI', 10)
        )
        source_lang_menu.pack(side=tk.LEFT, padx=(0, 10))
        source_lang_menu.bind('<<ComboboxSelected>>', self.callbacks.get('on_source_lang_change'))
        
        # Swap button
        swap_btn = tk.Button(
            control_frame,
            text="⇄",
            command=self.callbacks.get('on_swap'),
            bg=self.bg_color,
            fg=self.accent_color,
            font=('Arial', 16, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=10,
            borderwidth=1
        )
        swap_btn.pack(side=tk.LEFT, padx=5)
        
        # Target language dropdown
        self.widgets['target_lang_var'] = tk.StringVar(value="Vietnamese")
        target_lang_menu = ttk.Combobox(
            control_frame,
            textvariable=self.widgets['target_lang_var'],
            values=["English", "Vietnamese"],
            state='readonly',
            width=15,
            font=('Segoe UI', 10)
        )
        target_lang_menu.pack(side=tk.LEFT, padx=(5, 20))
        target_lang_menu.bind('<<ComboboxSelected>>', self.callbacks.get('on_target_lang_change'))
        
        # Translate button
        translate_btn = tk.Button(
            control_frame,
            text="Translate",
            command=self.callbacks.get('on_translate'),
            bg=self.accent_color,
            fg="#FFFFFF",
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=25,
            pady=8
        )
        translate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # AI Explain button (placeholder)
        ai_explain_btn = tk.Button(
            control_frame,
            text="🌐 AI Explain ▼",
            command=lambda: self.callbacks.get('on_status_update', lambda x: None)("AI Explain feature coming soon"),
            bg=self.bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10),
            relief=tk.SOLID,
            borderwidth=1,
            cursor='hand2',
            padx=15,
            pady=7
        )
        ai_explain_btn.pack(side=tk.LEFT)
    
    def get_source_lang(self):
        """Get source language code"""
        lang_name = self.widgets['source_lang_var'].get()
        return 'en' if lang_name == "English" else 'vi'
    
    def get_target_lang(self):
        """Get target language code"""
        lang_name = self.widgets['target_lang_var'].get()
        return 'en' if lang_name == "English" else 'vi'
    
    def set_source_lang(self, lang_name):
        """Set source language"""
        self.widgets['source_lang_var'].set(lang_name)
    
    def set_target_lang(self, lang_name):
        """Set target language"""
        self.widgets['target_lang_var'].set(lang_name)
    
    def swap_languages(self):
        """Swap source and target languages in UI"""
        source_val = self.widgets['source_lang_var'].get()
        target_val = self.widgets['target_lang_var'].get()
        self.widgets['source_lang_var'].set(target_val)
        self.widgets['target_lang_var'].set(source_val)
