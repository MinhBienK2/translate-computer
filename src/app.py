"""
Main application management module
"""
from features.hotkey_manager import HotkeyManager
from core.translator import Translator
from core.pronunciation import PronunciationManager
from ui.popup_gui import TranslationPopup
from ui.main_window import MainWindow
from core.config_manager import ConfigManager
import threading


class TranslateApp:
    """Main translation application"""
    
    def __init__(self):
        """Initialize application"""
        self.config = ConfigManager()
        self.translator = Translator(
            source_lang=self.config.get_source_language(),
            target_lang=self.config.get_target_language()
        )
        self.pronunciation_manager = PronunciationManager()
        
        # Main window (primary feature)
        self.main_window = None
        
        # Hotkey manager (secondary feature - for quick popup translation)
        hotkey = self.config.get_hotkey()
        self.hotkey_manager = HotkeyManager(self.on_text_selected, hotkey=hotkey)
        self.current_popup = None
    
    def on_text_selected(self, text):
        """
        Callback when text is selected and hotkey is pressed
        
        Args:
            text: Selected text
        """
        print(f"Translating: {text}")
        
        try:
            # Get translation information
            translation_info = self.translator.get_translation_info(text)
            
            # If popup is already open, just update its content
            if self.current_popup and self.current_popup.root:
                try:
                    auto_pronounce = self.config.get("auto_pronounce", False)
                    self.current_popup.update_content(translation_info, auto_pronounce)
                    return
                except Exception as e:
                    print(f"Error updating popup: {e}")
                    # If update fails, close and recreate
                    try:
                        self.current_popup.close()
                    except:
                        pass
                    self.current_popup = None
            
            # Show new popup in separate thread
            thread = threading.Thread(
                target=self._show_popup,
                args=(translation_info,),
                daemon=True
            )
            thread.start()
        except Exception as e:
            print(f"Error translating: {e}")
    
    def _show_popup(self, translation_info):
        """Show popup in separate thread"""
        try:
            auto_pronounce = self.config.get("auto_pronounce", False)
            self.current_popup = TranslationPopup(
                translation_info,
                self.pronunciation_manager,
                on_close_callback=self._on_popup_closed,
                auto_pronounce=auto_pronounce
            )
            self.current_popup.show()
        except Exception as e:
            print(f"Error showing popup: {e}")
    
    def _on_popup_closed(self):
        """Callback when popup is closed"""
        self.current_popup = None
    
    def _on_main_window_closed(self):
        """Callback when main window is closed - exit entire application"""
        print("\nMain window closed. Exiting application...")
        self.stop()
    
    def start(self):
        """Start application"""
        print("=" * 60)
        print("Translate Computer - Starting...")
        print("=" * 60)
        
        # Start hotkey manager in background (secondary feature)
        hotkey = self.config.get_hotkey()
        hotkey_display = hotkey.upper().replace('+', '+')
        print(f"✓ Hotkey feature enabled: Press {hotkey_display} to translate selected text")
        self.hotkey_manager.start()
        
        # Create and show main window (primary feature)
        print("✓ Opening main window...")
        self.main_window = MainWindow(
            self.translator,
            self.pronunciation_manager,
            self.config,
            on_close_callback=self._on_main_window_closed
        )
        
        # Show main window (this will block until window is closed)
        self.main_window.show()
    
    def stop(self):
        """Stop application"""
        print("\nStopping application...")
        
        # Stop hotkey manager
        if self.hotkey_manager:
            self.hotkey_manager.stop()
        
        # Stop pronunciation manager
        if self.pronunciation_manager:
            self.pronunciation_manager.stop()
        
        # Close popup if open
        if self.current_popup:
            try:
                self.current_popup.close()
            except:
                pass
        
        # Close main window if open
        if self.main_window:
            try:
                self.main_window.close()
            except:
                pass
        
        print("Application has stopped.")
        
        # Force exit
        import sys
        sys.exit(0)

