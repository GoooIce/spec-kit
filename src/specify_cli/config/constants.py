"""
Constants and static configuration for Specify CLI.
"""

from pathlib import Path

# ASCII Art Banner
BANNER = """
███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝ 
╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝  
███████║██║     ███████╗╚██████╗██║██║        ██║   
╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝   
"""

MINI_BANNER = """
╔═╗╔═╗╔═╗╔═╗╦╔═╗╦ ╦
╚═╗╠═╝║╣ ║  ║╠╣ ╚╦╝
╚═╝╩  ╚═╝╚═╝╩╚   ╩ 
"""

# Claude CLI local installation path after migrate-installer
CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"

# Release configuration
DEFAULT_REPO_OWNER = "GoooIce"
DEFAULT_REPO_NAME = "spec-kit"

# Default settings
DEFAULT_SCRIPT_TYPE = "sh"  # Will be overridden to "ps" on Windows
DEFAULT_LANGUAGE = "en"
DEFAULT_AI_ASSISTANT = "copilot"

# Supported choices
AI_ASSISTANT_KEYS = ["copilot", "claude", "gemini", "cursor"]
SCRIPT_TYPE_KEYS = ["sh", "ps"]
LANGUAGE_KEYS = ["en", "zh"]

# Path utilities
def get_templates_dir() -> Path:
    """Get the templates directory path."""
    # Get the package root directory
    package_root = Path(__file__).parent.parent.parent.parent
    return package_root / "templates"
