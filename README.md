# Translate Computer - Fast Translation Application

An application that allows you to select any text on your computer and press **Alt+E** to quickly translate with a popup displaying the results.

## Features

- ✅ Select text anywhere on your computer (Cursor, Word, Browser, ...)
- ✅ Press **Alt+E** to translate instantly
- ✅ Popup displays:
  - Original text and translation
  - Pronunciation (text-to-speech) for both original and translated text
  - Detailed definitions (if it's a single English word)
  - Meanings by word type (noun, verb, adjective, adverb)
- ✅ Automatic language detection
- ✅ Beautiful, user-friendly interface

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
uv run python main.py
```

Or if you've already synced dependencies:
```bash
uv run main.py
```

**Note:** `uv run` will automatically use the created virtual environment.

### How to use

1. **Select text**: Use your mouse to select any text on your computer (e.g., in Cursor, Word, Browser, ...)
2. **Press hotkey** (default: **Alt+E**): The popup will immediately appear with the translation result
3. **Listen to pronunciation**: Click the 🔊 icon to hear the pronunciation
4. **Close popup**: 
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
│   ├── hotkey_manager.py   # Manages hotkey and gets selected text
│   ├── translator.py       # Translation and dictionary information
│   ├── pronunciation.py    # Pronunciation handling (TTS)
│   ├── popup_gui.py        # GUI popup displaying results
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

### `hotkey_manager.py`
- Manages hotkey (configurable, default: **Alt+E**)
- Gets selected text from clipboard
- Uses `keyboard` and `pyperclip` libraries

### `config_manager.py`
- Manages application configuration
- Loads and saves settings from `config.json`
- Provides default configuration if file doesn't exist

### `translator.py`
- Translation using Google Translate API (via `deep-translator`)
- Automatic language detection
- Gets definitions from Free Dictionary API

### `pronunciation.py`
- Text-to-speech using `pyttsx3`
- Supports multiple languages
- Runs in a separate thread to avoid blocking UI

### `popup_gui.py`
- Popup interface using `tkinter`
- Displays original text, translation, definitions
- Pronunciation button for both original and translated text
- Automatically positions at top-right corner of screen

### `app.py`
- Manages the entire application
- Connects all modules together
- Handles application lifecycle

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
