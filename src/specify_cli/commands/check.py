"""
Check command implementation for Specify CLI.

This module contains the logic for checking tool availability.
"""

from ..i18n import t
from ..ui import show_banner, StepTracker, console
from ..tools import check_tool_for_tracker


def check_command() -> None:
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    # Create tracker for checking tools
    tracker = StepTracker(t("tools.check_title"))
    
    # Add all tools we want to check
    tracker.add("git", t("tools.git"))
    tracker.add("claude", t("tools.claude"))
    tracker.add("gemini", t("tools.gemini"))
    tracker.add("code", t("tools.code"))
    tracker.add("cursor-agent", t("tools.cursor_agent"))
    
    # Check each tool
    git_ok = check_tool_for_tracker("git", "https://git-scm.com/downloads", tracker)
    claude_ok = check_tool_for_tracker("claude", "https://docs.anthropic.com/en/docs/claude-code/setup", tracker)  
    gemini_ok = check_tool_for_tracker("gemini", "https://github.com/google-gemini/gemini-cli", tracker)
    # Check for VS Code (code or code-insiders)
    code_ok = check_tool_for_tracker("code", "https://code.visualstudio.com/", tracker)
    if not code_ok:
        code_ok = check_tool_for_tracker("code-insiders", "https://code.visualstudio.com/insiders/", tracker)
    cursor_ok = check_tool_for_tracker("cursor-agent", "https://cursor.sh/", tracker)
    
    # Render the final tree
    console.print(tracker.render())
    
    # Summary
    console.print(f"\n[bold green]{t('summary.specify_ready')}[/bold green]")
    
    # Recommendations
    if not git_ok:
        console.print(f"[dim]{t('summary.install_git_tip')}[/dim]")
    if not (claude_ok or gemini_ok):
        console.print(f"[dim]{t('summary.install_ai_tip')}[/dim]")
