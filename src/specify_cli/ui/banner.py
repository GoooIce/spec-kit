"""
Banner display utilities for Specify CLI.
"""

from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.table import Table
from typer.core import TyperGroup

from ..config import BANNER, get_tagline
from ..i18n import t


def show_banner(console: Console = None):
    """Display the ASCII art banner."""
    if console is None:
        console = Console()
    
    # Create gradient effect with different colors
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]
    
    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)
    
    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(get_tagline(), style="italic bright_yellow")))
    console.print()


def show_examples(console: Console = None):
    """Display usage examples in a beautiful panel."""
    if console is None:
        console = Console()
    
    # Create examples table
    examples_table = Table.grid(padding=(0, 2))
    examples_table.add_column(style="bright_cyan", justify="left")
    examples_table.add_column(style="dim", justify="left")
    
    examples_table.add_row("specify init my-project", "Initialize a new project")
    examples_table.add_row("specify init my-project --ai claude", "Initialize with Claude AI assistant")
    examples_table.add_row("specify init --ai gemini --lang zh", "Initialize with Gemini AI in Chinese")
    examples_table.add_row("specify init --here", "Initialize in current directory")
    
    # Create the panel
    panel = Panel(
        examples_table,
        title="[bold bright_blue]Usage Examples[/bold bright_blue]",
        title_align="left",
        border_style="bright_blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""
    
    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)
        
        # Show examples after help
        show_examples()
