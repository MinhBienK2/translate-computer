"""
Ứng dụng dịch thuật - Translate Computer
Chọn text và nhấn Alt+E để dịch
"""
import sys
import os

# Thêm thư mục src vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import TranslateApp


def main():
    """Hàm main"""
    try:
        app = TranslateApp()
        app.start()
    except Exception as e:
        print(f"Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

