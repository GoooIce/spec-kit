#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
Specify CLI - Setup tool for Specify projects

Usage:
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init --here
    uvx specify-cli.py --help

Or install globally:
    uv tool install --from specify-cli.py specify-cli
    specify init <project-name>
    specify init --here
    specify --help
"""

import sys
from pathlib import Path

import typer

# Import configuration and UI components
from .config import BANNER, get_tagline
from .ui import BannerGroup, console, show_banner
from .i18n import t

# Import command implementations
from .commands import (
    init_command,
    check_command
)

# Create the main Typer app
app = typer.Typer(
    name="specify",
    help="Setup tool for Specify spec-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)

@app.callback()
def callback(ctx: typer.Context):
    """Show banner and help when no subcommand is provided."""
    # Show full help when no subcommand and no help flag
    # (help is handled by BannerGroup)
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        # Show help instead of just banner
        print(ctx.get_help())
        raise typer.Exit()


@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here)"),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, copilot, or cursor"),
    script_type: str = typer.Option(None, "--script", help="Script type to use: sh or ps"),
    language: str = typer.Option(None, "--lang", help="Template language to use: en (English) or zh (Chinese)"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"),
    debug: bool = typer.Option(False, "--debug", help="Show verbose diagnostic output for network and extraction failures"),
):
    """
    Initialize a new Specify project from the latest template.
    
    Examples:
        specify init my-project
        specify init my-project --ai claude
        specify init my-project --ai gemini --lang zh
        specify init --here --ai claude
    """
    init_command(
        project_name=project_name,
        ai_assistant=ai_assistant,
        script_type=script_type,
        language=language,
        ignore_agent_tools=ignore_agent_tools,
        no_git=no_git,
        here=here,
        skip_tls=skip_tls,
        debug=debug,
    )


@app.command()
def check():
    """Check that all required tools are installed."""
    check_command()



def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()