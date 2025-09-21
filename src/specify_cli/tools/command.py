"""
Command execution utilities for Specify CLI.
"""

import subprocess
from typing import Optional, List, Union

from ..i18n import t
from ..ui import console


def run_command(
    cmd: Union[List[str], str], 
    check_return: bool = True, 
    capture: bool = False, 
    shell: bool = False
) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            cmd_str = cmd if isinstance(cmd, str) else ' '.join(cmd)
            console.print(f"[red]{t('errors.command_error', command=cmd_str)}[/red]")
            console.print(f"[red]{t('errors.exit_code', code=e.returncode)}[/red]")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]{t('errors.error_output', output=e.stderr)}[/red]")
            raise
        return None
