"""
Module for managing hotkey and getting selected text from clipboard
"""
import keyboard
import pyperclip
import time


class HotkeyManager:
    """Manages hotkey and gets selected text"""
    
    def __init__(self, callback, hotkey='alt+e'):
        """
        Initialize HotkeyManager
        
        Args:
            callback: Callback function called when hotkey is pressed
            hotkey: Hotkey combination (e.g., 'alt+e', 'ctrl+shift+t')
        """
        self.callback = callback
        self.hotkey = hotkey
        self.is_running = False
    
    def get_selected_text(self):
        """
        Get selected text by copying to clipboard
        
        Returns:
            str: Selected text, or None if no text is selected
        """
        # Save current clipboard
        old_clipboard = pyperclip.paste()
        
        try:
            # Copy selected text (Ctrl+C)
            keyboard.send('ctrl+c')
            time.sleep(0.2)  # Wait for clipboard to update
            
            # Get text from clipboard
            selected_text = pyperclip.paste()
            
            # Restore old clipboard if text hasn't changed
            if selected_text == old_clipboard:
                return None
            
            # Check if there's valid text
            if selected_text and selected_text.strip():
                return selected_text.strip()
            
            return None
            
        except Exception as e:
            print(f"Error getting selected text: {e}")
            return None
        finally:
            # Restore old clipboard
            try:
                pyperclip.copy(old_clipboard)
            except:
                pass
    
    def on_hotkey_pressed(self):
        """Handle when hotkey is pressed"""
        selected_text = self.get_selected_text()
        if selected_text:
            self.callback(selected_text)
    
    def start(self):
        """Start listening for hotkey"""
        if not self.is_running:
            try:
                keyboard.add_hotkey(self.hotkey, self.on_hotkey_pressed)
                self.is_running = True
                hotkey_display = self.hotkey.upper().replace('+', '+')
                print(f"✓ Hotkey {hotkey_display} activated. Press {hotkey_display} to translate selected text.")
            except Exception as e:
                print(f"✗ Error registering hotkey '{self.hotkey}': {e}")
                print("Please check if the hotkey format is correct or try running as Administrator.")
                raise
    
    def update_hotkey(self, new_hotkey):
        """
        Update hotkey combination
        
        Args:
            new_hotkey: New hotkey combination (e.g., 'alt+e', 'ctrl+shift+t')
        """
        was_running = self.is_running
        if was_running:
            self.stop()
        
        self.hotkey = new_hotkey.lower()
        
        if was_running:
            self.start()
    
    def stop(self):
        """Stop listening for hotkey"""
        if self.is_running:
            keyboard.unhook_all()
            self.is_running = False
            print("Hotkey has been stopped.")

