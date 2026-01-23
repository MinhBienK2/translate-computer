"""
Dictionary tab component
"""
import tkinter as tk


class DictionaryTab:
    """Dictionary tab placeholder"""
    
    def __init__(self, parent, bg_color, text_color):
        """
        Initialize dictionary tab
        
        Args:
            parent: Parent widget
            bg_color: Background color
            text_color: Text color
        """
        self.parent = parent
        self.bg_color = bg_color
        self.text_color = text_color
        
        self._create_tab()
    
    def _create_tab(self):
        """Create tab content"""
        placeholder = tk.Label(
            self.parent,
            text="Dictionary feature coming soon...",
            bg=self.bg_color,
            fg=self.text_color,
            font=('Segoe UI', 14)
        )
        placeholder.pack(expand=True)
