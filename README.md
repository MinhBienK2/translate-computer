# Translate Computer - Ứng dụng dịch thuật nhanh

Ứng dụng cho phép bạn chọn text bất kỳ trên máy tính và nhấn **Alt+E** để dịch nhanh với popup hiển thị kết quả.

## Tính năng

- ✅ Chọn text ở bất kỳ đâu trên máy tính (Cursor, Word, Browser, ...)
- ✅ Nhấn **Alt+E** để dịch ngay lập tức
- ✅ Popup hiển thị:
  - Text gốc và bản dịch
  - Phát âm (text-to-speech) cho cả text gốc và bản dịch
  - Định nghĩa chi tiết (nếu là từ đơn tiếng Anh)
  - Các nghĩa theo từng loại từ (noun, verb, adjective, adverb)
- ✅ Tự động phát hiện ngôn ngữ
- ✅ Giao diện đẹp, dễ sử dụng

## Cài đặt

### 1. Cài đặt Python

Đảm bảo bạn đã cài Python 3.7 trở lên.

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Lưu ý trên Windows:**
- Có thể cần chạy PowerShell/CMD với quyền Administrator để cài `keyboard` library
- Nếu gặp lỗi với `keyboard`, thử: `pip install keyboard --user`

## Sử dụng

### Chạy ứng dụng

```bash
python main.py
```

### Cách sử dụng

1. **Chọn text**: Dùng chuột chọn text bất kỳ trên máy tính (ví dụ: trong Cursor, Word, Browser, ...)
2. **Nhấn Alt+E**: Ngay lập tức popup sẽ hiện lên với kết quả dịch
3. **Nghe phát âm**: Click vào icon 🔊 để nghe phát âm
4. **Đóng popup**: 
   - Nhấn **Escape**
   - Click vào nút **✕**
   - Click ra ngoài popup

### Thoát ứng dụng

Nhấn **Ctrl+C** trong terminal để thoát.

## Cấu trúc thư mục

```
translate-computer/
├── src/
│   ├── __init__.py
│   ├── app.py              # Module chính quản lý ứng dụng
│   ├── hotkey_manager.py   # Quản lý hotkey Alt+E và lấy text đã chọn
│   ├── translator.py       # Dịch thuật và lấy thông tin từ điển
│   ├── pronunciation.py    # Xử lý phát âm (TTS)
│   └── popup_gui.py        # GUI popup hiển thị kết quả
├── main.py                 # File chạy chính
├── requirements.txt        # Dependencies
└── README.md              # File này
```

## Các module chính

### `hotkey_manager.py`
- Quản lý hotkey **Alt+E**
- Lấy text đã chọn từ clipboard
- Sử dụng thư viện `keyboard` và `pyperclip`

### `translator.py`
- Dịch thuật sử dụng Google Translate API (qua `deep-translator`)
- Tự động phát hiện ngôn ngữ
- Lấy định nghĩa từ Free Dictionary API

### `pronunciation.py`
- Text-to-speech sử dụng `pyttsx3`
- Hỗ trợ phát âm nhiều ngôn ngữ
- Chạy trong thread riêng để không block UI

### `popup_gui.py`
- Giao diện popup với `tkinter`
- Hiển thị text gốc, bản dịch, định nghĩa
- Nút phát âm cho cả text gốc và bản dịch
- Tự động đặt vị trí ở góc trên bên phải màn hình

### `app.py`
- Quản lý toàn bộ ứng dụng
- Kết nối các module lại với nhau
- Xử lý lifecycle của ứng dụng

## Yêu cầu hệ thống

- Python 3.7+
- Windows 10/11 (đã test trên Windows)
- Kết nối Internet (để dịch và lấy định nghĩa)

## Troubleshooting

### Lỗi khi cài `keyboard` library
- Chạy terminal với quyền Administrator
- Hoặc dùng: `pip install keyboard --user`

### Hotkey không hoạt động
- Đảm bảo ứng dụng đang chạy
- Kiểm tra xem có ứng dụng khác đang dùng Alt+E không
- Thử chạy với quyền Administrator

### Không lấy được text đã chọn
- Đảm bảo bạn đã chọn text trước khi nhấn Alt+E
- Một số ứng dụng có thể không cho phép copy (như một số game)

### Popup không hiện
- Kiểm tra kết nối Internet
- Xem log trong terminal để biết lỗi cụ thể

## Phát triển thêm

Có thể mở rộng thêm:
- Thêm nhiều ngôn ngữ đích
- Lưu lịch sử dịch
- Tùy chỉnh hotkey
- Thêm các API dịch thuật khác
- Cải thiện UI/UX

## License

MIT License

