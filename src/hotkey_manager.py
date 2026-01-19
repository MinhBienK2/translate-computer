"""
Module quản lý hotkey và lấy text đã chọn từ clipboard
"""
import keyboard
import pyperclip
import time


class HotkeyManager:
    """Quản lý hotkey Alt+E và lấy text đã chọn"""
    
    def __init__(self, callback):
        """
        Khởi tạo HotkeyManager
        
        Args:
            callback: Hàm callback được gọi khi nhấn Alt+E
        """
        self.callback = callback
        self.is_running = False
    
    def get_selected_text(self):
        """
        Lấy text đã chọn bằng cách copy vào clipboard
        
        Returns:
            str: Text đã chọn, hoặc None nếu không có text nào được chọn
        """
        # Lưu clipboard hiện tại
        old_clipboard = pyperclip.paste()
        
        try:
            # Copy text đã chọn (Ctrl+C)
            keyboard.send('ctrl+c')
            time.sleep(0.1)  # Đợi clipboard cập nhật
            
            # Lấy text từ clipboard
            selected_text = pyperclip.paste()
            
            # Khôi phục clipboard cũ nếu text không thay đổi
            if selected_text == old_clipboard:
                return None
            
            # Kiểm tra xem có text hợp lệ không
            if selected_text and selected_text.strip():
                return selected_text.strip()
            
            return None
            
        except Exception as e:
            print(f"Lỗi khi lấy text đã chọn: {e}")
            return None
        finally:
            # Khôi phục clipboard cũ
            try:
                pyperclip.copy(old_clipboard)
            except:
                pass
    
    def on_hotkey_pressed(self):
        """Xử lý khi nhấn hotkey Alt+E"""
        selected_text = self.get_selected_text()
        if selected_text:
            self.callback(selected_text)
    
    def start(self):
        """Bắt đầu lắng nghe hotkey"""
        if not self.is_running:
            keyboard.add_hotkey('alt+e', self.on_hotkey_pressed)
            self.is_running = True
            print("Hotkey Alt+E đã được kích hoạt. Nhấn Alt+E để dịch text đã chọn.")
    
    def stop(self):
        """Dừng lắng nghe hotkey"""
        if self.is_running:
            keyboard.unhook_all()
            self.is_running = False
            print("Hotkey đã được tắt.")

