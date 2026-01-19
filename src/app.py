"""
Module chính quản lý ứng dụng
"""
from hotkey_manager import HotkeyManager
from translator import Translator
from pronunciation import PronunciationManager
from popup_gui import TranslationPopup
import threading


class TranslateApp:
    """Ứng dụng dịch thuật chính"""
    
    def __init__(self):
        """Khởi tạo ứng dụng"""
        self.translator = Translator()
        self.pronunciation_manager = PronunciationManager()
        self.hotkey_manager = HotkeyManager(self.on_text_selected)
        self.current_popup = None
    
    def on_text_selected(self, text):
        """
        Callback khi có text được chọn và nhấn Alt+E
        
        Args:
            text: Text đã chọn
        """
        print(f"Đang dịch: {text}")
        
        # Lấy thông tin dịch
        translation_info = self.translator.get_translation_info(text)
        
        # Đóng popup cũ nếu có
        if self.current_popup:
            try:
                self.current_popup.close()
            except:
                pass
        
        # Hiển thị popup mới trong thread riêng
        thread = threading.Thread(
            target=self._show_popup,
            args=(translation_info,),
            daemon=True
        )
        thread.start()
    
    def _show_popup(self, translation_info):
        """Hiển thị popup trong thread riêng"""
        try:
            self.current_popup = TranslationPopup(
                translation_info,
                self.pronunciation_manager,
                on_close_callback=self._on_popup_closed
            )
            self.current_popup.show()
        except Exception as e:
            print(f"Lỗi khi hiển thị popup: {e}")
    
    def _on_popup_closed(self):
        """Callback khi popup đóng"""
        self.current_popup = None
    
    def start(self):
        """Bắt đầu ứng dụng"""
        print("Ứng dụng dịch thuật đã khởi động!")
        print("Hướng dẫn:")
        print("1. Chọn text trên màn hình (bất kỳ đâu)")
        print("2. Nhấn Alt+E để dịch")
        print("3. Nhấn Escape hoặc click ra ngoài để đóng popup")
        print("\nNhấn Ctrl+C để thoát ứng dụng.\n")
        
        self.hotkey_manager.start()
        
        try:
            # Giữ ứng dụng chạy
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Dừng ứng dụng"""
        print("\nĐang dừng ứng dụng...")
        self.hotkey_manager.stop()
        self.pronunciation_manager.stop()
        if self.current_popup:
            try:
                self.current_popup.close()
            except:
                pass
        print("Ứng dụng đã dừng.")

