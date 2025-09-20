"""
Console utilities for Specify CLI.
"""

from rich.console import Console

# Create a default console instance
console = Console()

def get_console() -> Console:
    """Get the default console instance."""
    return console
