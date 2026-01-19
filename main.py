"""
Translation application - Translate Computer
Select text and press Alt+E to translate
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import TranslateApp


def main():
    """Main function"""
    try:
        app = TranslateApp()
        app.start()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

