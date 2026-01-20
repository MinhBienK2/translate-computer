"""
Module for managing application configuration
"""
import json
import os
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration"""
    
    DEFAULT_CONFIG = {
        "hotkey": "alt+e",
        "source_language": "en",
        "target_language": "vi",
        "popup_position": "top-right",
        "popup_width": 450,
        "auto_pronounce": False
    }
    
    def __init__(self, config_file="config.json"):
        """
        Initialize ConfigManager
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file, create default if not exists
        
        Returns:
            dict: Configuration dictionary
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with default to ensure all keys exist
                    merged_config = self.DEFAULT_CONFIG.copy()
                    merged_config.update(config)
                    return merged_config
            except Exception as e:
                print(f"Error loading config: {e}. Using default configuration.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save_config(self.DEFAULT_CONFIG.copy())
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Dict[str, Any] = None):
        """
        Save configuration to file
        
        Args:
            config: Configuration dictionary (uses self.config if None)
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """
        Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set configuration value
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
        self.save_config()
    
    def get_hotkey(self) -> str:
        """
        Get hotkey combination
        
        Returns:
            str: Hotkey combination (e.g., "alt+e")
        """
        return self.get("hotkey", "alt+e")
    
    def set_hotkey(self, hotkey: str):
        """
        Set hotkey combination
        
        Args:
            hotkey: Hotkey combination (e.g., "alt+e", "ctrl+shift+t")
        """
        self.set("hotkey", hotkey.lower())
    
    def get_source_language(self) -> str:
        """Get source language"""
        return self.get("source_language", "en")
    
    def get_target_language(self) -> str:
        """Get target language"""
        return self.get("target_language", "vi")

