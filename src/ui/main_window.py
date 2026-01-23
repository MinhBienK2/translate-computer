"""
Main window GUI for translation application
"""
import tkinter as tk
import threading
from .components.advanced_translation_tab import AdvancedTranslationTab
from .components.dictionary_tab import DictionaryTab


class MainWindow:
    """Main window for translation application"""
    
    def __init__(self, translator, pronunciation_manager, config_manager, on_close_callback=None):
        """
        Initialize main window
        
        Args:
            translator: Translator instance
            pronunciation_manager: PronunciationManager instance
            config_manager: ConfigManager instance
            on_close_callback: Callback function when window is closed
        """
        self.translator = translator
        self.pronunciation_manager = pronunciation_manager
        self.config_manager = config_manager
        self.on_close_callback = on_close_callback
        
        self.root = None
        self.widgets = {}
        self.current_tab = "advanced"  # "advanced" or "dictionary"
        self.advanced_tab = None
        self.dictionary_tab = None
        
        self._create_window()
    
    def _create_window(self):
        """Create main window"""
        self.root = tk.Tk()
        self.root.title("Translate Computer")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Colors
        bg_color = "#FFFFFF"
        tab_bg = "#F8F9FA"
        active_tab_bg = "#FFFFFF"
        text_color = "#212529"
        secondary_color = "#6C757D"
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Main container
        main_container = tk.Frame(self.root, bg=bg_color)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Tab bar
        tab_bar = tk.Frame(main_container, bg=tab_bg, height=50)
        tab_bar.pack(fill=tk.X, side=tk.TOP)
        tab_bar.pack_propagate(False)
        
        # Advanced translation tab
        self.widgets['advanced_tab'] = tk.Button(
            tab_bar,
            text="  A  Advanced translation",
            command=lambda: self._switch_tab("advanced"),
            bg=active_tab_bg,
            fg=text_color,
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            cursor='hand2',
            anchor='w',
            padx=20,
            pady=10,
            borderwidth=0,
            highlightthickness=0
        )
        self.widgets['advanced_tab'].pack(side=tk.LEFT, fill=tk.Y, padx=(10, 2))
        
        # Dictionary tab
        self.widgets['dictionary_tab'] = tk.Button(
            tab_bar,
            text="  Aa  Dictionary",
            command=lambda: self._switch_tab("dictionary"),
            bg=tab_bg,
            fg=secondary_color,
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            cursor='hand2',
            anchor='w',
            padx=20,
            pady=10,
            borderwidth=0,
            highlightthickness=0
        )
        self.widgets['dictionary_tab'].pack(side=tk.LEFT, fill=tk.Y, padx=2)
        
        # Content area
        content_frame = tk.Frame(main_container, bg=bg_color, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Advanced translation content (default visible)
        self.widgets['advanced_content'] = tk.Frame(content_frame, bg=bg_color)
        self.widgets['advanced_content'].pack(fill=tk.BOTH, expand=True)
        
        # Create advanced translation tab
        callbacks = {
            'on_status_update': self._update_status,
            'on_translate': self._do_translate
        }
        self.advanced_tab = AdvancedTranslationTab(
            self.widgets['advanced_content'],
            self.translator,
            self.pronunciation_manager,
            callbacks
        )
        
        # Dictionary content (hidden by default)
        self.widgets['dictionary_content'] = tk.Frame(content_frame, bg=bg_color)
        self.dictionary_tab = DictionaryTab(
            self.widgets['dictionary_content'],
            bg_color,
            text_color
        )
        
        # Status bar (at bottom of window)
        self.widgets['status_label'] = tk.Label(
            self.root,
            text="Ready",
            bg="#F8F9FA",
            fg=secondary_color,
            font=('Segoe UI', 9),
            anchor='w',
            padx=15,
            pady=8
        )
        self.widgets['status_label'].pack(side=tk.BOTTOM, fill=tk.X)
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _switch_tab(self, tab_name):
        """Switch between tabs"""
        self.current_tab = tab_name
        
        if tab_name == "advanced":
            self.widgets['advanced_tab'].config(bg="#FFFFFF", fg="#212529")
            self.widgets['dictionary_tab'].config(bg="#F8F9FA", fg="#6C757D")
            self.widgets['dictionary_content'].pack_forget()
            self.widgets['advanced_content'].pack(fill=tk.BOTH, expand=True)
        else:
            self.widgets['advanced_tab'].config(bg="#F8F9FA", fg="#6C757D")
            self.widgets['dictionary_tab'].config(bg="#FFFFFF", fg="#212529")
            self.widgets['advanced_content'].pack_forget()
            self.widgets['dictionary_content'].pack(fill=tk.BOTH, expand=True)
    
    def _do_translate(self, text, source_lang, target_lang):
        """Perform translation"""
        # Run translation in separate thread
        thread = threading.Thread(
            target=self._translate_thread,
            args=(text, source_lang, target_lang),
            daemon=True
        )
        thread.start()
    
    def _translate_thread(self, text, source_lang, target_lang):
        """Perform translation in background thread"""
        try:
            # Currently only Google Translate is implemented
            # TODO: Add Microsoft, AI, IPA translation sources
            translated = self.translator.translate(text, source_lang=source_lang, target_lang=target_lang)
            
            # Update output text in main thread
            self.root.after(0, self.advanced_tab.text_areas.set_output_text, translated)
            self.root.after(0, self._update_status, "Translation completed")
        except Exception as e:
            self.root.after(0, self._update_status, f"Error: {str(e)}")
    
    def _update_status(self, message):
        """Update status bar message"""
        if 'status_label' in self.widgets:
            self.widgets['status_label'].config(text=message)
    
    def set_input_text(self, text):
        """Set input text programmatically (for popup integration)"""
        if self.root and self.advanced_tab:
            self.advanced_tab.set_input_text(text)
    
    def _on_window_close(self):
        """Handle window close event"""
        if self.on_close_callback:
            self.on_close_callback()
        self.close()
    
    def show(self):
        """Show main window"""
        if self.root:
            self.root.mainloop()
    
    def close(self):
        """Close main window"""
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
