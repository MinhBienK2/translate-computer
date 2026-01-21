"""
Module for GUI popup displaying translation results
"""
import tkinter as tk
from tkinter import ttk, font
import threading
import pyperclip


class TranslationPopup:
    """Popup displaying translation results"""
    
    def __init__(self, translation_info, pronunciation_manager, on_close_callback=None, auto_pronounce=False):
        """
        Initialize popup
        
        Args:
            translation_info: Dict containing translation information
            pronunciation_manager: PronunciationManager instance
            on_close_callback: Callback when popup is closed
            auto_pronounce: Whether to automatically pronounce translation when popup opens
        """
        self.translation_info = translation_info
        self.pronunciation_manager = pronunciation_manager
        self.on_close_callback = on_close_callback
        self.auto_pronounce = auto_pronounce
        
        self.root = None
        self.main_frame = None
        self.widgets = {}  # Store widget references for updating
        
        # Variables for drag functionality
        self._drag_start_x = 0
        self._drag_start_y = 0
        
        self._create_popup()
    
    def _create_popup(self):
        """Create popup window"""
        self.root = tk.Tk()
        self.root.title("Translation")
        
        # Configure window
        self.root.overrideredirect(True)  # Remove title bar
        self.root.attributes('-topmost', True)  # Always on top
        
        # Colors
        bg_color = "#FFFFFF"
        header_color = "#F5F5F5"
        text_color = "#333333"
        accent_color = "#4285F4"
        
        # Main frame
        self.main_frame = tk.Frame(self.root, bg=bg_color, padx=20, pady=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame = self.main_frame
        
        # Header with close button
        header_frame = tk.Frame(main_frame, bg=header_color, cursor='fleur')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Bind drag events to header frame
        header_frame.bind('<Button-1>', self._start_drag)
        header_frame.bind('<B1-Motion>', self._on_drag)
        
        # Source language dropdown
        source_lang = self.translation_info.get('source_language', 'en').upper()
        self.widgets['lang_label'] = tk.Label(
            header_frame, 
            text=source_lang, 
            bg=header_color, 
            fg=text_color,
            font=('Arial', 10, 'bold'),
            cursor='fleur'
        )
        self.widgets['lang_label'].pack(side=tk.LEFT, padx=5, pady=5)
        
        # Bind drag events to language label
        self.widgets['lang_label'].bind('<Button-1>', self._start_drag)
        self.widgets['lang_label'].bind('<B1-Motion>', self._on_drag)
        
        # Close button
        close_btn = tk.Button(
            header_frame,
            text="✕",
            command=self.close,
            bg=header_color,
            fg=text_color,
            font=('Arial', 12, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=5,
            pady=2
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Original text
        original_text = self.translation_info.get('original_text', '')
        self.widgets['original_label'] = tk.Label(
            main_frame,
            text=original_text,
            bg=bg_color,
            fg=text_color,
            font=('Arial', 16, 'bold'),
            anchor='w',
            wraplength=400
        )
        self.widgets['original_label'].pack(fill=tk.X, pady=(0, 5))
        
        # Frame containing pronunciation and copy buttons for original text
        original_pron_frame = tk.Frame(main_frame, bg=bg_color)
        original_pron_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.widgets['pron_btn_original'] = tk.Button(
            original_pron_frame,
            text="🔊",
            command=lambda: self.pronunciation_manager.speak(
                original_text, 
                self.translation_info.get('source_language', 'en')
            ),
            bg=bg_color,
            fg=accent_color,
            font=('Arial', 14),
            relief=tk.FLAT,
            cursor='hand2',
            padx=5
        )
        self.widgets['pron_btn_original'].pack(side=tk.LEFT)
        
        # Copy button for original text
        self.widgets['copy_btn_original'] = tk.Button(
            original_pron_frame,
            text="📋",
            command=lambda: self._copy_text(original_text),
            bg=bg_color,
            fg=accent_color,
            font=('Arial', 14),
            relief=tk.FLAT,
            cursor='hand2',
            padx=5
        )
        self.widgets['copy_btn_original'].pack(side=tk.LEFT)
        
        # Target language
        target_lang = self.translation_info.get('target_language', 'vi').upper()
        self.widgets['target_lang_label'] = tk.Label(
            main_frame,
            text=target_lang,
            bg=bg_color,
            fg=text_color,
            font=('Arial', 10, 'bold'),
            anchor='w'
        )
        self.widgets['target_lang_label'].pack(fill=tk.X, pady=(5, 5))
        
        # Translation
        translation = self.translation_info.get('translation', '')
        self.widgets['translation_label'] = tk.Label(
            main_frame,
            text=translation,
            bg=bg_color,
            fg=text_color,
            font=('Arial', 16, 'bold'),
            anchor='w',
            wraplength=400
        )
        self.widgets['translation_label'].pack(fill=tk.X, pady=(0, 5))
        
        # Frame containing pronunciation button for translation
        translation_pron_frame = tk.Frame(main_frame, bg=bg_color)
        translation_pron_frame.pack(fill=tk.X, pady=(0, 15))
        self.widgets['translation_pron_frame'] = translation_pron_frame
        
        self.widgets['pron_btn_translation'] = tk.Button(
            translation_pron_frame,
            text="🔊",
            command=lambda: self.pronunciation_manager.speak(
                translation,
                self.translation_info.get('target_language', 'vi')
            ),
            bg=bg_color,
            fg=accent_color,
            font=('Arial', 14),
            relief=tk.FLAT,
            cursor='hand2',
            padx=5
        )
        self.widgets['pron_btn_translation'].pack(side=tk.LEFT)
        
        # Display definitions if available
        self.widgets['definitions_container'] = None
        self.widgets['definitions_frame'] = None
        definitions = self.translation_info.get('definitions')
        if definitions and 'meanings' in definitions:
            self._create_definitions(main_frame, definitions, bg_color, text_color)
        
        # Calculate position and size
        self.root.update_idletasks()
        width = 450
        height = self.root.winfo_reqheight()
        
        # Position at top-right corner of screen
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - width - 20
        y = 20
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Bind click outside event to close
        self.root.bind('<Button-1>', self._on_click_outside)
        self.root.focus_set()
        
        # Close when pressing Escape
        self.root.bind('<Escape>', lambda e: self.close())
        
        # Auto pronounce if enabled
        if self.auto_pronounce:
            # Use after() to ensure popup is fully rendered before pronouncing
            self.root.after(100, self._auto_pronounce)
    
    def _on_click_outside(self, event):
        """Handle click outside popup"""
        # Only close if clicking on main frame (not child widgets)
        if event.widget == self.root:
            self.close()
    
    def _start_drag(self, event):
        """Start dragging the popup"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
    
    def _on_drag(self, event):
        """Handle dragging motion"""
        # Calculate new position
        x = self.root.winfo_x() + event.x - self._drag_start_x
        y = self.root.winfo_y() + event.y - self._drag_start_y
        
        # Update window position
        self.root.geometry(f"+{x}+{y}")
    
    def _copy_text(self, text):
        """Copy text to clipboard"""
        try:
            pyperclip.copy(text)
            # Optional: Show feedback (you could add a toast notification here)
            print(f"Copied to clipboard: {text}")
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
    
    def _create_definitions(self, parent, definitions, bg_color, text_color):
        """Create definitions section"""
        meanings = definitions.get('meanings', {})
        if not meanings:
            return
        
        # Remove old definitions container if exists
        if self.widgets.get('definitions_container'):
            self.widgets['definitions_container'].destroy()
        
        # Container for separator and definitions
        self.widgets['definitions_container'] = tk.Frame(parent, bg=bg_color)
        self.widgets['definitions_container'].pack(fill=tk.X)
        
        # Separator
        separator = tk.Frame(self.widgets['definitions_container'], bg="#E0E0E0", height=1)
        separator.pack(fill=tk.X, pady=10)
        
        # Frame for definitions
        self.widgets['definitions_frame'] = tk.Frame(self.widgets['definitions_container'], bg=bg_color)
        self.widgets['definitions_frame'].pack(fill=tk.X)
        
        # Display meanings by part of speech
        for part_of_speech, def_list in meanings.items():
            # Part of speech (noun, verb, adjective, adverb)
            pos_label = tk.Label(
                self.widgets['definitions_frame'],
                text=f"**{part_of_speech}**:",
                bg=bg_color,
                fg=text_color,
                font=('Arial', 11, 'bold'),
                anchor='w'
            )
            pos_label.pack(fill=tk.X, pady=(5, 2))
            
            # Definitions
            def_text = ", ".join(def_list[:3])  # Get maximum 3 first definitions
            def_label = tk.Label(
                self.widgets['definitions_frame'],
                text=def_text,
                bg=bg_color,
                fg=text_color,
                font=('Arial', 10),
                anchor='w',
                wraplength=400,
                justify=tk.LEFT
            )
            def_label.pack(fill=tk.X, pady=(0, 8))
    
    def update_content(self, translation_info, auto_pronounce=False):
        """Update popup content without recreating the window"""
        if not self.root:
            return
        
        self.translation_info = translation_info
        self.auto_pronounce = auto_pronounce
        
        # Update source language
        source_lang = translation_info.get('source_language', 'en').upper()
        if 'lang_label' in self.widgets:
            self.widgets['lang_label'].config(text=source_lang)
        
        # Update original text
        original_text = translation_info.get('original_text', '')
        if 'original_label' in self.widgets:
            self.widgets['original_label'].config(text=original_text)
        
        # Update pronunciation button for original text
        if 'pron_btn_original' in self.widgets:
            self.widgets['pron_btn_original'].config(
                command=lambda: self.pronunciation_manager.speak(
                    original_text,
                    translation_info.get('source_language', 'en')
                )
            )
        
        # Update copy button for original text
        if 'copy_btn_original' in self.widgets:
            self.widgets['copy_btn_original'].config(
                command=lambda: self._copy_text(original_text)
            )
        
        # Update target language
        target_lang = translation_info.get('target_language', 'vi').upper()
        if 'target_lang_label' in self.widgets:
            self.widgets['target_lang_label'].config(text=target_lang)
        
        # Update translation
        translation = translation_info.get('translation', '')
        if 'translation_label' in self.widgets:
            self.widgets['translation_label'].config(text=translation)
        
        # Update pronunciation button for translation
        if 'pron_btn_translation' in self.widgets:
            self.widgets['pron_btn_translation'].config(
                command=lambda: self.pronunciation_manager.speak(
                    translation,
                    translation_info.get('target_language', 'vi')
                )
            )
        
        # Update definitions
        definitions = translation_info.get('definitions')
        if definitions and 'meanings' in definitions:
            self._create_definitions(
                self.main_frame,
                definitions,
                "#FFFFFF",
                "#333333"
            )
        elif 'definitions_container' in self.widgets and self.widgets['definitions_container']:
            # Remove definitions if not available
            self.widgets['definitions_container'].destroy()
            self.widgets['definitions_container'] = None
            self.widgets['definitions_frame'] = None
        
        # Update window size while preserving position
        self.root.update_idletasks()
        height = self.root.winfo_reqheight()
        width = 450
        
        # Preserve current position
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Auto pronounce if enabled
        if self.auto_pronounce:
            self.root.after(100, self._auto_pronounce)
    
    def _auto_pronounce(self):
        """Automatically pronounce original text when popup opens"""
        if self.auto_pronounce:
            original_text = self.translation_info.get('original_text', '')
            source_language = self.translation_info.get('source_language', 'en')
            if original_text:
                self.pronunciation_manager.speak(original_text, source_language)
    
    def show(self):
        """Show popup"""
        if self.root:
            self.root.mainloop()
    
    def close(self):
        """Close popup"""
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
                if self.on_close_callback:
                    self.on_close_callback()
            except:
                pass

