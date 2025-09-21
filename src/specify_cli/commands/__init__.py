"""
Commands module for Specify CLI.

This module contains all command implementations for the CLI application.
"""

from .init import init_command
from .check import check_command
from .mcp import (
    mcp_list_command,
    mcp_presets_command,
    mcp_install_command,
    mcp_recommend_command
)

__all__ = [
    "init_command",
    "check_command", 
    "mcp_list_command",
    "mcp_presets_command",
    "mcp_install_command",
    "mcp_recommend_command",
]
