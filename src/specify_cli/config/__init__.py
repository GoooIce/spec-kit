"""
Configuration module for Specify CLI.

This module contains constants, settings, and configuration utilities.
"""

from .constants import (
    BANNER,
    MINI_BANNER,
    CLAUDE_LOCAL_PATH,
    DEFAULT_REPO_OWNER,
    DEFAULT_REPO_NAME,
    AI_ASSISTANT_KEYS,
    SCRIPT_TYPE_KEYS,
    LANGUAGE_KEYS,
    get_templates_dir,
)

from .settings import (
    get_ai_choices,
    get_script_type_choices,
    get_language_choices,
    get_tagline,
    get_default_script_type,
    get_default_language,
    get_default_ai_assistant,
    # Legacy exports for backward compatibility
    AI_CHOICES,
    SCRIPT_TYPE_CHOICES,
    LANGUAGE_CHOICES,
    TAGLINE,
)

__all__ = [
    # Constants
    "BANNER",
    "MINI_BANNER", 
    "CLAUDE_LOCAL_PATH",
    "DEFAULT_REPO_OWNER",
    "DEFAULT_REPO_NAME",
    "AI_ASSISTANT_KEYS",
    "SCRIPT_TYPE_KEYS",
    "LANGUAGE_KEYS",
    "get_templates_dir",
    # Settings functions
    "get_ai_choices",
    "get_script_type_choices", 
    "get_language_choices",
    "get_tagline",
    "get_default_script_type",
    "get_default_language",
    "get_default_ai_assistant",
    # Legacy exports
    "AI_CHOICES",
    "SCRIPT_TYPE_CHOICES",
    "LANGUAGE_CHOICES", 
    "TAGLINE",
]
