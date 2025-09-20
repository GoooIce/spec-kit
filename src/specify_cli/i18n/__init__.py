"""
Internationalization (i18n) module for Specify CLI.

This module provides translation support for multiple languages including
English (en) and Chinese (zh).

Usage:
    from specify_cli.i18n import t, set_language
    
    # Basic translation
    message = t('welcome')
    
    # Translation with parameters
    error = t('errors.invalid_ai', ai='invalid_name')
    
    # Set language manually
    set_language('zh')
"""

import os
import json
import locale
from pathlib import Path
from typing import Dict, Any, Optional


class I18n:
    """Internationalization handler for Specify CLI."""
    
    def __init__(self):
        self.current_language = 'en'  # Default language
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.locales_dir = Path(__file__).parent / 'locales'
        self._load_translations()
        self._detect_language()
    
    def _load_translations(self) -> None:
        """Load all translation files."""
        if not self.locales_dir.exists():
            return
            
        for locale_file in self.locales_dir.glob('*.json'):
            lang_code = locale_file.stem
            try:
                with open(locale_file, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                # Fallback silently, use English as default
                print(f"Warning: Could not load {lang_code} translations: {e}")
    
    def _detect_language(self) -> None:
        """Detect system language and set it if supported."""
        try:
            # Try environment variables first
            system_lang = (
                os.environ.get('SPECIFY_LANG') or  # Custom environment variable
                os.environ.get('LANG', '').split('.')[0] or
                locale.getdefaultlocale()[0] or
                'en'
            )
            
            # Extract language code (e.g., 'zh_CN' -> 'zh')
            lang_code = system_lang.split('_')[0].lower()
            
            # Use detected language if we have translations for it
            if lang_code in self.translations:
                self.current_language = lang_code
        except Exception:
            # Fallback to English silently
            self.current_language = 'en'
    
    def set_language(self, lang_code: str) -> bool:
        """
        Set the current language.
        
        Args:
            lang_code: Language code ('en', 'zh', etc.)
            
        Returns:
            True if language was set successfully, False otherwise
        """
        if lang_code in self.translations:
            self.current_language = lang_code
            return True
        return False
    
    def get_language(self) -> str:
        """Get the current language code."""
        return self.current_language
    
    def get_available_languages(self) -> list[str]:
        """Get list of available language codes."""
        return list(self.translations.keys())
    
    def _get_nested_value(self, data: dict, key: str) -> Any:
        """
        Get value from nested dictionary using dot notation.
        
        Args:
            data: Dictionary to search in
            key: Key with dot notation (e.g., 'errors.invalid_ai')
            
        Returns:
            The value if found, None otherwise
        """
        keys = key.split('.')
        current = data
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
        
        return current
    
    def t(self, key: str, **kwargs):
        """
        Get translated content.
        
        Args:
            key: Translation key (supports dot notation for nested keys)
            **kwargs: Parameters for string interpolation (only applied to string content)
            
        Returns:
            Translated content (string, list, or dict), fallback to key if not found
        """
        # Get translations for current language
        current_translations = self.translations.get(self.current_language, {})
        
        # Try to get translation
        text = self._get_nested_value(current_translations, key)
        
        # Fallback to English if not found in current language
        if text is None and self.current_language != 'en':
            english_translations = self.translations.get('en', {})
            text = self._get_nested_value(english_translations, key)
        
        # Ultimate fallback to the key itself
        if text is None:
            text = key
        
        # Perform parameter interpolation only for string content
        if kwargs and isinstance(text, str):
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                # If interpolation fails, return the original text
                pass
        
        return text


# Global i18n instance
_i18n = I18n()

# Export main functions
def t(key: str, **kwargs) -> str:
    """
    Get translated text.
    
    Args:
        key: Translation key (supports dot notation for nested keys)
        **kwargs: Parameters for string interpolation
        
    Returns:
        Translated and interpolated text
        
    Examples:
        >>> t('welcome')
        'Welcome to Specify CLI'
        
        >>> t('errors.invalid_ai', ai='unknown')
        "Invalid AI assistant 'unknown'"
        
        >>> t('project_created', name='my-project')
        "Project 'my-project' created successfully"
    """
    return _i18n.t(key, **kwargs)


def set_language(lang_code: str) -> bool:
    """
    Set the current language.
    
    Args:
        lang_code: Language code ('en', 'zh', etc.)
        
    Returns:
        True if language was set successfully, False otherwise
    """
    return _i18n.set_language(lang_code)


def get_language() -> str:
    """Get the current language code."""
    return _i18n.get_language()


def get_available_languages() -> list[str]:
    """Get list of available language codes."""
    return _i18n.get_available_languages()


def detect_system_language() -> str:
    """Get detected system language."""
    return _i18n.current_language
