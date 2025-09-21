"""
Tool availability checking utilities for Specify CLI.
"""

import shutil

from ..config import CLAUDE_LOCAL_PATH
from ..i18n import t
from ..ui import StepTracker, console


def check_tool_for_tracker(tool: str, install_hint: str, tracker: StepTracker) -> bool:
    """Check if a tool is installed and update tracker."""
    if shutil.which(tool):
        tracker.complete(tool, t("common.available"))
        return True
    else:
        tracker.error(tool, f"{t('common.not_found')} - {install_hint}")
        return False


def check_tool(tool: str, install_hint: str) -> bool:
    """Check if a tool is installed."""
    
    # Special handling for Claude CLI after `claude migrate-installer`
    # See: https://github.com/github/spec-kit/issues/123
    # The migrate-installer command REMOVES the original executable from PATH
    # and creates an alias at ~/.claude/local/claude instead
    # This path should be prioritized over other claude executables in PATH
    if tool == "claude":
        if CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
            return True
    
    if shutil.which(tool):
        return True
    else:
        console.print(f"[yellow]⚠️  {t('tools.not_found_template', tool=tool)}[/yellow]")
        console.print(f"   {t('tools.install_with', hint=install_hint)}")
        return False
