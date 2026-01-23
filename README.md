# Translate Computer - Translation Application

A professional translation application with a main window GUI and quick select-to-translate popup feature.

## Features

### Main Window (Primary Feature)
- ✅ Clean, modern interface with tabs (Advanced Translation, Dictionary)
- ✅ Large input and output text areas
- ✅ Language selection dropdowns (English ↔ Vietnamese)
- ✅ Swap languages button
- ✅ Multiple translation sources: Google, Microsoft, AI, IPA
- ✅ Pronunciation buttons for source and target text
- ✅ Copy to clipboard functionality
- ✅ Character counter (5000 character limit)
- ✅ Keyboard shortcut: Ctrl+Enter to translate
- ✅ Status bar showing translation progress

### Quick Translate (Secondary Feature)
- ✅ Select text anywhere on your computer (Cursor, Word, Browser, ...)
- ✅ Press hotkey (default: **F2**) to open translation popup
- ✅ Draggable popup that remembers position
- ✅ Popup displays:
  - Original text and translation
  - Pronunciation (text-to-speech) for both original and translated text
  - Detailed definitions (if it's a single English word)
  - Meanings by word type (noun, verb, adjective, adverb)
- ✅ Automatic language detection

## Installation

### 1. Install Python

Make sure you have Python 3.7 or higher installed.

### 2. Install uv

`uv` is an extremely fast package manager and project manager for Python.

**On Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**On Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or install via pip:
```bash
pip install uv
```

See more at: https://github.com/astral-sh/uv

### 3. Install dependencies

`uv` will automatically create a virtual environment and install all dependencies:

```bash
uv sync
```

Or if you want to use `requirements.txt`:
```bash
uv pip install -r requirements.txt
```

**Note on Windows:**
- You may need to run PowerShell/CMD as Administrator to install the `keyboard` library
- If you encounter errors with `keyboard`, try: `uv pip install keyboard --user`

## Usage

### Run the application

With `uv`, you don't need to activate a virtual environment. Just run:

```bash
uv run main.py
```

**Note:** `uv run` will automatically use the created virtual environment.

### How to use

#### Main Window (Primary Feature)

1. **Launch the application**: Run `uv run main.py` - the main window will open automatically
2. **Enter or paste text**: Type or paste text in the "Source text" area
3. **Select languages**: Use the dropdown menus to select source and target languages
4. **Swap languages**: Click the **⇄** button to reverse translation direction
5. **Translate**: Click the "Translate" button or press **Ctrl+Enter**
6. **Listen to pronunciation**: Click the 🔊 icons to hear text read aloud
7. **Copy translation**: Click the 📋 icon to copy to clipboard
8. **Switch translation source**: Click tabs (Google, Microsoft, AI, IPA) to compare translations
9. **Exit**: Click the **X** button on the window to close the application

#### Quick Translate Popup (Secondary Feature)

While the main window is open, you can also use the quick translate feature:

1. **Select text**: Use your mouse to select any text on your computer (anywhere)
2. **Press hotkey** (default: **F2**): A popup will appear with the translation
3. **Drag popup**: Click and hold the header to move the popup anywhere
4. **Listen to pronunciation**: Click the 🔊 icon to hear the pronunciation
5. **Close popup**: 
   - Press **Escape**
   - Click the **✕** button
   - Click outside the popup

### Configuration

You can customize the application by editing the `config.json` file (created automatically on first run). If the file doesn't exist, copy `config.json.example` to `config.json`.

**Available settings:**

```json
{
    "hotkey": "alt+e",           // Hotkey combination (e.g., "alt+e", "ctrl+shift+t")
    "source_language": "en",     // Default source language
    "target_language": "vi",      // Default target language
    "popup_position": "top-right", // Popup position (not yet implemented)
    "popup_width": 450            // Popup width in pixels
}
```

**Hotkey format:**
- Use `+` to combine keys: `"alt+e"`, `"ctrl+shift+t"`, `"ctrl+alt+q"`
- Supported modifiers: `alt`, `ctrl`, `shift`, `win`
- Supported keys: letters (`a-z`), numbers (`0-9`), function keys (`f1-f12`), etc.

**Example configurations:**
- `"alt+e"` - Alt + E (default)
- `"ctrl+shift+t"` - Ctrl + Shift + T
- `"ctrl+alt+q"` - Ctrl + Alt + Q
- `"f9"` - Function key F9

**Note:** After changing the config file, restart the application for changes to take effect.

### Exit the application

Press **Ctrl+C** in the terminal to exit.

## Directory Structure

```
translate-computer/
├── src/
│   ├── __init__.py
│   ├── app.py              # Main application management module
│   ├── main_window.py      # Main window GUI (primary feature)
│   ├── popup_gui.py        # Quick translate popup (secondary feature)
│   ├── hotkey_manager.py   # Manages hotkey and gets selected text
│   ├── translator.py       # Translation and dictionary information
│   ├── pronunciation.py    # Pronunciation handling (TTS)
│   └── config_manager.py   # Configuration management
├── .venv/                  # Virtual environment (auto-created by uv, not committed)
├── main.py                 # Main entry point
├── pyproject.toml          # Project configuration (uv uses this file)
├── requirements.txt        # Dependencies (backup, uv prioritizes pyproject.toml)
├── config.json             # User configuration (auto-created, not committed)
├── config.json.example     # Example configuration file
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Main Modules

### `main_window.py`
- Main window GUI using `tkinter`
- Professional interface with tabs (Advanced Translation, Dictionary)
- Input and output text areas
- Language selection and swap functionality
- Multiple translation sources (Google, Microsoft, AI, IPA)
- Character counter and status bar
- Primary feature of the application

### `popup_gui.py`
- Quick translate popup interface using `tkinter`
- Displays original text, translation, definitions
- Pronunciation buttons for both original and translated text
- Draggable popup that remembers position
- Secondary feature activated by hotkey

### `hotkey_manager.py`
- Manages hotkey (configurable, default: **F2**)
- Gets selected text from clipboard
- Uses `keyboard` and `pyperclip` libraries
- Enables quick translate popup feature

### `translator.py`
- Translation using Google Translate API (via `deep-translator`)
- Automatic language detection
- Gets definitions from Free Dictionary API
- Supports multiple language pairs

### `pronunciation.py`
- Text-to-speech using `pyttsx3`
- Supports multiple languages
- Runs in a separate thread to avoid blocking UI

### `config_manager.py`
- Manages application configuration
- Loads and saves settings from `config.json`
- Provides default configuration if file doesn't exist

### `app.py`
- Manages the entire application
- Connects all modules together
- Handles application lifecycle
- Coordinates main window and popup features

## System Requirements

- Python 3.7+
- uv (package manager) - see installation instructions above
- Windows 10/11 (tested on Windows)
- Internet connection (for translation and getting definitions)

## Troubleshooting

### Error installing `keyboard` library
- Run terminal as Administrator
- Or use: `uv pip install keyboard --user`

### Error installing uv
- On Windows: You may need to run PowerShell as Administrator
- Or install via pip: `pip install uv`
- See more: https://github.com/astral-sh/uv

### Hotkey not working
- Make sure the application is running
- Check if another application is using Alt+E
- Try running as Administrator

### Cannot get selected text
- Make sure you've selected text before pressing Alt+E
- Some applications may not allow copying (like some games)

### Popup not showing
- Check your Internet connection
- Check the terminal logs for specific errors

## Future Development

Possible enhancements:
- Add more target languages
- Save translation history
- Customize hotkey
- Add other translation APIs
- Improve UI/UX

## License

MIT License
