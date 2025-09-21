"""
Git repository operations for Specify CLI.
"""

import os
import subprocess
from pathlib import Path

from ..i18n import t
from ..ui import console


def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()
    
    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(project_path: Path, quiet: bool = False) -> bool:
    """Initialize a git repository in the specified path.
    quiet: if True suppress console output (tracker handles status)
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print(f"[cyan]{t('git.initializing')}[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Specify template"], check=True, capture_output=True)
        if not quiet:
            console.print(f"[green]✓[/green] {t('git.initialized')}")
        return True
        
    except subprocess.CalledProcessError as e:
        if not quiet:
            console.print(f"[red]{t('git.init_error', error=str(e))}[/red]")
        return False
    finally:
        os.chdir(original_cwd)
