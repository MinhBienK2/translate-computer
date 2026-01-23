"""
Text areas component - input and output text areas with toolbars
"""
import tkinter as tk
from tkinter import scrolledtext


class TextAreas:
    """Input and output text areas with toolbars"""
    
    def __init__(self, parent, bg_color, border_color, text_color, accent_color, secondary_color, callbacks):
        """
        Initialize text areas
        
        Args:
            parent: Parent widget
            bg_color: Background color
            border_color: Border color
            text_color: Text color
            accent_color: Accent color
            secondary_color: Secondary color
            callbacks: Dict with callbacks:
                - on_char_count_update
                - on_pronounce_source
                - on_copy_source
                - on_copy_translation
        """
        self.parent = parent
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        self.accent_color = accent_color
        self.secondary_color = secondary_color
        self.callbacks = callbacks
        
        self.widgets = {}
        self._create_text_areas()
    
    def _create_text_areas(self):
        """Create input and output text areas"""
        # Source text section
        source_label_frame = tk.Frame(self.parent, bg=self.bg_color)
        source_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        source_label = tk.Label(
            source_label_frame,
            text="Source text",
            bg=self.bg_color,
            fg=self.text_color,
            font=('Segoe UI', 11, 'bold'),
            anchor='w'
        )
        source_label.pack(side=tk.LEFT)
        
        # Speaker icon for source text
        source_speaker_btn = tk.Button(
            source_label_frame,
            text="🔊",
            command=self.callbacks.get('on_pronounce_source'),
            bg=self.bg_color,
            fg=self.accent_color,
            font=('Arial', 12),
            relief=tk.FLAT,
            cursor='hand2',
            padx=5
        )
        source_speaker_btn.pack(side=tk.LEFT, padx=(10, 5))
        
        # Copy icon for source text
        source_copy_btn = tk.Button(
            source_label_frame,
            text="📋",
            command=self.callbacks.get('on_copy_source'),
            bg=self.bg_color,
            fg=self.accent_color,
            font=('Arial', 12),
            relief=tk.FLAT,
            cursor='hand2',
            padx=5
        )
        source_copy_btn.pack(side=tk.LEFT)
        
        # Source text toolbar
        source_toolbar = tk.Frame(self.parent, bg=self.bg_color)
        source_toolbar.pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(
            source_toolbar,
            text="✏️ Highlight",
            bg=self.bg_color,
            fg=self.secondary_color,
            font=('Segoe UI', 9),
            relief=tk.FLAT,
            cursor='hand2',
            padx=8,
            pady=3
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            source_toolbar,
            text="📝 Edit",
            bg=self.bg_color,
            fg=self.secondary_color,
            font=('Segoe UI', 9),
            relief=tk.FLAT,
            cursor='hand2',
            padx=8,
            pady=3
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            source_toolbar,
            text="➕ Add",
            bg=self.bg_color,
            fg=self.secondary_color,
            font=('Segoe UI', 9),
            relief=tk.FLAT,
            cursor='hand2',
            padx=8,
            pady=3
        ).pack(side=tk.LEFT)
        
        # Input text area with frame for border
        input_container = tk.Frame(self.parent, bg=self.border_color, padx=1, pady=1)
        input_container.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        input_inner = tk.Frame(input_container, bg=self.bg_color)
        input_inner.pack(fill=tk.BOTH, expand=True)
        
        self.widgets['input_text'] = scrolledtext.ScrolledText(
            input_inner,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg="#FFFFFF",
            fg=self.text_color,
            relief=tk.FLAT,
            padx=12,
            pady=12,
            borderwidth=0
        )
        self.widgets['input_text'].pack(fill=tk.BOTH, expand=True)
        self.widgets['input_text'].bind('<KeyRelease>', self.callbacks.get('on_char_count_update'))
        
        # Character counter
        char_count_frame = tk.Frame(input_inner, bg=self.bg_color)
        char_count_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.widgets['char_count_label'] = tk.Label(
            char_count_frame,
            text="0/5000",
            bg=self.bg_color,
            fg=self.secondary_color,
            font=('Segoe UI', 9),
            anchor='e'
        )
        self.widgets['char_count_label'].pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Translation output section
        output_label_frame = tk.Frame(self.parent, bg=self.bg_color)
        output_label_frame.pack(fill=tk.X, pady=(10, 5))
        
        output_label = tk.Label(
            output_label_frame,
            text="Translation",
            bg=self.bg_color,
            fg=self.text_color,
            font=('Segoe UI', 11, 'bold'),
            anchor='w'
        )
        output_label.pack(side=tk.LEFT)
        
        # Question mark icon
        tk.Label(
            output_label_frame,
            text="❓",
            bg=self.bg_color,
            fg=self.secondary_color,
            font=('Arial', 10),
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=(10, 5))
        
        # Copy icon for translation
        output_copy_btn = tk.Button(
            output_label_frame,
            text="📋",
            command=self.callbacks.get('on_copy_translation'),
            bg=self.bg_color,
            fg=self.accent_color,
            font=('Arial', 12),
            relief=tk.FLAT,
            cursor='hand2',
            padx=5
        )
        output_copy_btn.pack(side=tk.LEFT)
        
        # Edit button
        tk.Button(
            output_label_frame,
            text="📝 Edit",
            bg=self.bg_color,
            fg=self.secondary_color,
            font=('Segoe UI', 9),
            relief=tk.FLAT,
            cursor='hand2',
            padx=8,
            pady=3
        ).pack(side=tk.RIGHT)
        
        # Output text area with frame for border
        output_container = tk.Frame(self.parent, bg=self.border_color, padx=1, pady=1)
        output_container.pack(fill=tk.BOTH, expand=True)
        
        self.widgets['output_text'] = scrolledtext.ScrolledText(
            output_container,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg="#F8F9FA",
            fg=self.text_color,
            relief=tk.FLAT,
            padx=12,
            pady=12,
            state=tk.DISABLED,
            borderwidth=0
        )
        self.widgets['output_text'].pack(fill=tk.BOTH, expand=True)
    
    def get_input_text(self):
        """Get input text"""
        return self.widgets['input_text'].get("1.0", tk.END).strip()
    
    def set_input_text(self, text):
        """Set input text"""
        self.widgets['input_text'].delete("1.0", tk.END)
        self.widgets['input_text'].insert("1.0", text)
    
    def get_output_text(self):
        """Get output text"""
        return self.widgets['output_text'].get("1.0", tk.END).strip()
    
    def set_output_text(self, text):
        """Set output text"""
        self.widgets['output_text'].config(state=tk.NORMAL)
        self.widgets['output_text'].delete("1.0", tk.END)
        self.widgets['output_text'].insert("1.0", text)
        self.widgets['output_text'].config(state=tk.DISABLED)
    
    def update_char_count(self):
        """Update character counter"""
        text = self.get_input_text()
        char_count = len(text)
        self.widgets['char_count_label'].config(text=f"{char_count}/5000")
        
        # Optionally limit to 5000 characters
        if char_count > 5000:
            self.widgets['input_text'].delete("1.0", tk.END)
            self.widgets['input_text'].insert("1.0", text[:5000])
            self.widgets['char_count_label'].config(text="5000/5000")
