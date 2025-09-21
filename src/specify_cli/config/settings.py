"""
Dynamic configuration settings and choice generators for Specify CLI.
"""

import os
from typing import Dict

from ..i18n import t
from .constants import (
    AI_ASSISTANT_KEYS,
    SCRIPT_TYPE_KEYS, 
    LANGUAGE_KEYS,
    DEFAULT_SCRIPT_TYPE,
    DEFAULT_LANGUAGE,
    DEFAULT_AI_ASSISTANT
)


def get_ai_choices() -> Dict[str, str]:
    """Get AI assistant choices with translations."""
    return {
        "copilot": t("ai_assistants.copilot"),
        "claude": t("ai_assistants.claude"),
        "gemini": t("ai_assistants.gemini"),
        "cursor": t("ai_assistants.cursor")
    }


def get_script_type_choices() -> Dict[str, str]:
    """Get script type choices with translations."""
    return {
        "sh": t("script_types.sh"),
        "ps": t("script_types.ps")
    }


def get_language_choices() -> Dict[str, str]:
    """Get language choices with translations."""
    return {
        "en": t("languages.en"),
        "zh": t("languages.zh")
    }


def get_tagline() -> str:
    """Get tagline with translation."""
    return t("tagline")


def get_default_script_type() -> str:
    """Get default script type based on OS."""
    return "ps" if os.name == "nt" else DEFAULT_SCRIPT_TYPE


def get_default_language() -> str:
    """Get default language."""
    return DEFAULT_LANGUAGE


def get_default_ai_assistant() -> str:
    """Get default AI assistant."""
    return DEFAULT_AI_ASSISTANT


# Legacy constants for backward compatibility
AI_CHOICES = get_ai_choices()
SCRIPT_TYPE_CHOICES = get_script_type_choices()
LANGUAGE_CHOICES = get_language_choices()
TAGLINE = get_tagline()
