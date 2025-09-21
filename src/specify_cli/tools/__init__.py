"""
Tools module for Specify CLI.

This module contains utilities for checking tool availability, Git operations,
command execution, and template downloading.
"""

from .checker import check_tool, check_tool_for_tracker
from .git import is_git_repo, init_git_repo
from .command import run_command
from .downloader import (
    download_template_from_github,
    download_and_extract_template,
    ensure_executable_scripts
)

__all__ = [
    # Tool checking
    "check_tool",
    "check_tool_for_tracker",
    # Git operations
    "is_git_repo", 
    "init_git_repo",
    # Command execution
    "run_command",
    # Template downloading
    "download_template_from_github",
    "download_and_extract_template", 
    "ensure_executable_scripts",
]
