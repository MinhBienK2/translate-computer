"""
Main application management module
"""
from hotkey_manager import HotkeyManager
from translator import Translator
from pronunciation import PronunciationManager
from popup_gui import TranslationPopup
from config_manager import ConfigManager
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
            
            # Close old popup if exists
            if self.current_popup:
                try:
                    self.current_popup.close()
                except:
                    pass
            
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
            self.current_popup = TranslationPopup(
                translation_info,
                self.pronunciation_manager,
                on_close_callback=self._on_popup_closed
            )
            self.current_popup.show()
        except Exception as e:
            print(f"Error showing popup: {e}")
    
    def _on_popup_closed(self):
        """Callback when popup is closed"""
        self.current_popup = None
    
    def start(self):
        """Start application"""
        hotkey = self.config.get_hotkey()
        hotkey_display = hotkey.upper().replace('+', '+')
        print("=" * 60)
        print("Translation application has started!")
        print("=" * 60)
        print("Instructions:")
        print("1. Select text on screen (anywhere)")
        print(f"2. Press {hotkey_display} to translate")
        print("3. Press Escape or click outside to close popup")
        print(f"\nCurrent hotkey: {hotkey_display} (from config.json)")
        print("To change hotkey, edit config.json file and restart the application.")
        print("\nPress Ctrl+C to exit the application.\n")
        
        self.hotkey_manager.start()
        
        try:
            # Keep application running
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop application"""
        print("\nStopping application...")
        self.hotkey_manager.stop()
        self.pronunciation_manager.stop()
        if self.current_popup:
            try:
                self.current_popup.close()
            except:
                pass
        print("Application has stopped.")

