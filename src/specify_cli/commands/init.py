"""
Init command implementation for Specify CLI.

This module contains the logic for initializing new Specify projects.
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional

import typer
import httpx
from rich.panel import Panel
from rich.live import Live
from rich.align import Align

from ..config import (
    get_ai_choices,
    get_script_type_choices, 
    get_language_choices,
    get_default_script_type,
    get_default_language,
    get_default_ai_assistant
)
from ..i18n import t, set_language
from ..ui import (
    show_banner,
    select_with_arrows,
    StepTracker,
    console
)
from ..tools import (
    check_tool,
    is_git_repo,
    init_git_repo,
    download_and_extract_template,
    ensure_executable_scripts
)


def init_command(
    project_name: Optional[str] = None,
    ai_assistant: Optional[str] = None,
    script_type: Optional[str] = None,
    language: Optional[str] = None,
    ignore_agent_tools: bool = False,
    no_git: bool = False,
    here: bool = False,
    skip_tls: bool = False,
    debug: bool = False,
) -> None:
    """
    Initialize a new Specify project from the latest template.
    
    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant (Claude Code, Gemini CLI, GitHub Copilot, or Cursor)
    3. Download the appropriate template from GitHub
    4. Extract the template to a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Optionally set up AI assistant commands
    """
    # Show banner first
    show_banner()
    
    # Validate arguments
    if here and project_name:
        console.print(f"[red]Error:[/red] {t('project.no_both')}")
        raise typer.Exit(1)
    
    if not here and not project_name:
        console.print(f"[red]Error:[/red] {t('project.name_required')}")
        raise typer.Exit(1)
    
    # Determine project directory
    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()
        
        # Check if current directory has any files
        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]Warning:[/yellow] {t('project.not_empty_warning', count=len(existing_items))}")
            console.print(f"[yellow]{t('project.merge_warning')}[/yellow]")
            
            # Ask for confirmation
            response = typer.confirm(t('project.continue_prompt'))
            if not response:
                console.print(f"[yellow]{t('common.operation_cancelled')}[/yellow]")
                raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        # Check if project directory already exists
        if project_path.exists():
            console.print(f"[red]Error:[/red] {t('project.directory_exists', name=project_name)}")
            raise typer.Exit(1)
    
    # Check git only if we might need it (not --no-git)
    git_available = True
    if not no_git:
        git_available = check_tool("git", "https://git-scm.com/downloads")
        if not git_available:
            console.print(f"[yellow]{t('git.not_found_skip')}[/yellow]")

    # AI assistant selection
    if ai_assistant:
        if ai_assistant not in get_ai_choices():
            console.print(f"[red]Error:[/red] {t('errors.invalid_ai', ai=ai_assistant, choices=', '.join(get_ai_choices().keys()))}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Use arrow-key selection interface
        selected_ai = select_with_arrows(
            get_ai_choices(), 
            t("selection.choose_ai"), 
            get_default_ai_assistant()
        )
    
    # Check agent tools unless ignored
    if not ignore_agent_tools:
        agent_tool_missing = False
        if selected_ai == "claude":
            if not check_tool("claude", "Install from: https://docs.anthropic.com/en/docs/claude-code/setup"):
                console.print(f"[red]Error:[/red] {t('errors.claude_required')}")
                agent_tool_missing = True
        elif selected_ai == "gemini":
            if not check_tool("gemini", "Install from: https://github.com/google-gemini/gemini-cli"):
                console.print(f"[red]Error:[/red] {t('errors.gemini_required')}")
                agent_tool_missing = True

        if agent_tool_missing:
            console.print(f"\n[red]{t('errors.missing_ai_tool')}[/red]")
            console.print(f"[yellow]Tip:[/yellow] {t('errors.ignore_tools_tip')}")
            raise typer.Exit(1)
    
    # Determine script type (explicit, interactive, or OS default)
    if script_type:
        if script_type not in get_script_type_choices():
            console.print(f"[red]Error:[/red] {t('errors.invalid_script', script=script_type, choices=', '.join(get_script_type_choices().keys()))}")
            raise typer.Exit(1)
        selected_script = script_type
    else:
        # Auto-detect default
        default_script = get_default_script_type()
        # Provide interactive selection similar to AI if stdin is a TTY
        if sys.stdin.isatty():
            selected_script = select_with_arrows(get_script_type_choices(), t("selection.choose_script"), default_script)
        else:
            selected_script = default_script
    
    # Determine language (explicit, interactive, or default)
    if language:
        if language not in get_language_choices():
            console.print(f"[red]Error:[/red] {t('errors.invalid_language', language=language, choices=', '.join(get_language_choices().keys()))}")
            raise typer.Exit(1)
        selected_language = language
    else:
        # Default to English
        default_language = get_default_language()
        # Provide interactive selection if stdin is a TTY
        if sys.stdin.isatty():
            selected_language = select_with_arrows(get_language_choices(), t("selection.choose_language"), default_language)
        else:
            selected_language = default_language
    
    # Set the selected language for i18n before showing results
    set_language(selected_language)
    
    console.print(f"[cyan]{t('summary.selected_ai', ai=selected_ai)}[/cyan]")
    console.print(f"[cyan]{t('summary.selected_script', script=selected_script)}[/cyan]")
    console.print(f"[cyan]{t('summary.selected_language', language=selected_language)}[/cyan]")
    
    # Download and set up project
    # New tree-based progress (no emojis); include earlier substeps
    tracker = StepTracker(t('project.setup_title'))
    # Flag to allow suppressing legacy headings
    sys._specify_tracker_active = True
    # Pre steps recorded as completed before live rendering
    tracker.add("precheck", t("steps.precheck"))
    tracker.complete("precheck", t("common.ok"))
    tracker.add("ai-select", t("steps.ai_select"))
    tracker.complete("ai-select", f"{selected_ai}")
    tracker.add("script-select", t("steps.script_select"))
    tracker.complete("script-select", selected_script)
    for key, label_key in [
        ("fetch", "steps.fetch"),
        ("download", "steps.download"),
        ("extract", "steps.extract"),
        ("zip-list", "steps.zip_list"),
        ("extracted-summary", "steps.extracted_summary"),
        ("chmod", "steps.chmod"),
        ("cleanup", "steps.cleanup"),
        ("git", "steps.git_init"),
        ("final", "steps.finalize")
    ]:
        tracker.add(key, t(label_key))

    # Use transient so live tree is replaced by the final static render (avoids duplicate output)
    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            # Create a httpx client with verify based on skip_tls
            import ssl
            import truststore
            verify = not skip_tls
            ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT) if verify else False
            local_client = httpx.Client(verify=ssl_context)

            download_and_extract_template(project_path, selected_ai, selected_script, selected_language, here, verbose=False, tracker=tracker, client=local_client, debug=debug)

            # Ensure scripts are executable (POSIX)
            ensure_executable_scripts(project_path, tracker=tracker)

            # Git step
            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", t("git.existing_repo"))
                elif git_available:
                    if init_git_repo(project_path, quiet=True):
                        tracker.complete("git", t("git.initialized"))
                    else:
                        tracker.error("git", "init failed")
                else:
                    tracker.skip("git", t("git.not_available"))
            else:
                tracker.skip("git", t("git.no_git_flag"))

            tracker.complete("final", t("project.ready"))
        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(t("errors.initialization_failed", error=str(e)), title="Failure", border_style="red"))
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("Platform", sys.platform),
                    ("CWD", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="Debug Environment", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            # Force final render
            pass

    # Final static tree (ensures finished state visible after Live context ends)
    console.print(tracker.render())
    console.print(f"\n[bold green]{t('summary.project_ready')}[/bold green]")
    
    # Boxed "Next steps" section
    steps_lines = []
    if not here:
        steps_lines.append(f"1. [bold green]{t('next_steps.cd_project', name=project_name)}[/bold green]")
        step_num = 2
    else:
        steps_lines.append(f"1. {t('next_steps.already_in_dir')}")
        step_num = 2

    if selected_ai == "claude":
        steps_lines.append(f"{step_num}. {t('next_steps.claude_instructions')}")
        for cmd in t('next_steps.claude_commands'):
            steps_lines.append(f"   - {cmd}")
    elif selected_ai == "gemini":
        steps_lines.append(f"{step_num}. {t('next_steps.gemini_instructions')}")
        for cmd in t('next_steps.gemini_commands'):
            steps_lines.append(f"   - {cmd}")
    elif selected_ai == "copilot":
        steps_lines.append(f"{step_num}. {t('next_steps.copilot_instructions')}")

    # Removed script variant step (scripts are transparent to users)
    step_num += 1
    steps_lines.append(f"{step_num}. {t('next_steps.update_constitution')}")

    steps_panel = Panel("\n".join(steps_lines), title=t("next_steps.title"), border_style="cyan", padding=(1,2))
    console.print()  # blank line
    console.print(steps_panel)
