"""
Module GUI popup hiển thị kết quả dịch
"""
import tkinter as tk
from tkinter import ttk, font
import threading


class TranslationPopup:
    """Popup hiển thị kết quả dịch"""
    
    def __init__(self, translation_info, pronunciation_manager, on_close_callback=None):
        """
        Khởi tạo popup
        
        Args:
            translation_info: Dict chứa thông tin dịch
            pronunciation_manager: PronunciationManager instance
            on_close_callback: Callback khi đóng popup
        """
        self.translation_info = translation_info
        self.pronunciation_manager = pronunciation_manager
        self.on_close_callback = on_close_callback
        
        self.root = None
        self._create_popup()
    
    def _create_popup(self):
        """Tạo popup window"""
        self.root = tk.Tk()
        self.root.title("Translation")
        
        # Cấu hình window
        self.root.overrideredirect(True)  # Bỏ thanh tiêu đề
        self.root.attributes('-topmost', True)  # Luôn ở trên cùng
        
        # Màu sắc
        bg_color = "#FFFFFF"
        header_color = "#F5F5F5"
        text_color = "#333333"
        accent_color = "#4285F4"
        
        # Frame chính
        main_frame = tk.Frame(self.root, bg=bg_color, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header với nút đóng
        header_frame = tk.Frame(main_frame, bg=header_color)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Dropdown ngôn ngữ nguồn
        source_lang = self.translation_info.get('source_language', 'en').upper()
        lang_label = tk.Label(
            header_frame, 
            text=source_lang, 
            bg=header_color, 
            fg=text_color,
            font=('Arial', 10, 'bold')
        )
        lang_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Nút đóng
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
        
        # Text gốc
        original_text = self.translation_info.get('original_text', '')
        original_label = tk.Label(
            main_frame,
            text=original_text,
            bg=bg_color,
            fg=text_color,
            font=('Arial', 16, 'bold'),
            anchor='w'
        )
        original_label.pack(fill=tk.X, pady=(0, 5))
        
        # Frame chứa nút phát âm cho text gốc
        original_pron_frame = tk.Frame(main_frame, bg=bg_color)
        original_pron_frame.pack(fill=tk.X, pady=(0, 15))
        
        pron_btn_original = tk.Button(
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
        pron_btn_original.pack(side=tk.LEFT)
        
        # Ngôn ngữ đích
        target_lang = self.translation_info.get('target_language', 'vi').upper()
        target_lang_label = tk.Label(
            main_frame,
            text=target_lang,
            bg=bg_color,
            fg=text_color,
            font=('Arial', 10, 'bold'),
            anchor='w'
        )
        target_lang_label.pack(fill=tk.X, pady=(5, 5))
        
        # Bản dịch
        translation = self.translation_info.get('translation', '')
        translation_label = tk.Label(
            main_frame,
            text=translation,
            bg=bg_color,
            fg=text_color,
            font=('Arial', 16, 'bold'),
            anchor='w',
            wraplength=400
        )
        translation_label.pack(fill=tk.X, pady=(0, 5))
        
        # Frame chứa nút phát âm cho bản dịch
        translation_pron_frame = tk.Frame(main_frame, bg=bg_color)
        translation_pron_frame.pack(fill=tk.X, pady=(0, 15))
        
        pron_btn_translation = tk.Button(
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
        pron_btn_translation.pack(side=tk.LEFT)
        
        # Hiển thị định nghĩa nếu có
        definitions = self.translation_info.get('definitions')
        if definitions and 'meanings' in definitions:
            meanings = definitions['meanings']
            
            # Separator
            separator = tk.Frame(main_frame, bg="#E0E0E0", height=1)
            separator.pack(fill=tk.X, pady=10)
            
            # Hiển thị các nghĩa theo từng loại từ
            for part_of_speech, def_list in meanings.items():
                # Loại từ (noun, verb, adjective, adverb)
                pos_label = tk.Label(
                    main_frame,
                    text=f"**{part_of_speech}**:",
                    bg=bg_color,
                    fg=text_color,
                    font=('Arial', 11, 'bold'),
                    anchor='w'
                )
                pos_label.pack(fill=tk.X, pady=(5, 2))
                
                # Các định nghĩa
                def_text = ", ".join(def_list[:3])  # Lấy tối đa 3 định nghĩa đầu
                def_label = tk.Label(
                    main_frame,
                    text=def_text,
                    bg=bg_color,
                    fg=text_color,
                    font=('Arial', 10),
                    anchor='w',
                    wraplength=400,
                    justify=tk.LEFT
                )
                def_label.pack(fill=tk.X, pady=(0, 8))
        
        # Tính toán vị trí và kích thước
        self.root.update_idletasks()
        width = 450
        height = self.root.winfo_reqheight()
        
        # Đặt vị trí ở góc trên bên phải màn hình
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - width - 20
        y = 20
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Bind sự kiện click ra ngoài để đóng
        self.root.bind('<Button-1>', self._on_click_outside)
        self.root.focus_set()
        
        # Đóng khi nhấn Escape
        self.root.bind('<Escape>', lambda e: self.close())
    
    def _on_click_outside(self, event):
        """Xử lý click ra ngoài popup"""
        # Chỉ đóng nếu click vào frame chính (không phải các widget con)
        if event.widget == self.root:
            self.close()
    
    def show(self):
        """Hiển thị popup"""
        if self.root:
            self.root.mainloop()
    
    def close(self):
        """Đóng popup"""
        if self.root:
            self.root.quit()
            self.root.destroy()
            if self.on_close_callback:
                self.on_close_callback()

