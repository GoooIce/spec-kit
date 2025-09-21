"""
MCP command implementation for Specify CLI.

This module contains commands for managing MCP tools and presets.
"""

from pathlib import Path
from typing import Optional, List
import json
import shutil

import typer
from rich.table import Table
from rich.panel import Panel

from ..ui import console, select_with_arrows
from ..config import get_templates_dir


def mcp_list_command(
    category: Optional[str] = None,
    show_disabled: bool = False
) -> None:
    """List available MCP tools."""
    templates_dir = get_templates_dir()
    mcp_dir = templates_dir / "mcp"
    
    if not mcp_dir.exists():
        console.print("[yellow]No MCP templates found.[/yellow]")
        return
    
    # Get available MCP configurations
    config_files = list(mcp_dir.glob("**/*.json"))
    
    if not config_files:
        console.print("[yellow]No MCP configurations found.[/yellow]")
        return
    
    table = Table(title="Available MCP Tools")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Type", style="green")
    table.add_column("Status", style="white")
    table.add_column("Description", style="dim")
    
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            tool_name = config_file.stem
            status = "✓ Available"
            status_style = "green"
            description = f"MCP configuration for {tool_name}"
            
            table.add_row(
                tool_name,
                "Configuration",
                f"[{status_style}]{status}[/{status_style}]",
                description
            )
        except (json.JSONDecodeError, OSError) as e:
            console.print(f"[red]Error reading {config_file}: {e}[/red]")
    
    console.print(table)


def mcp_presets_command() -> None:
    """List available MCP tool presets."""
    # Define available presets based on template system
    presets = {
        "basic": {
            "tools": ["serena"],
            "description": "Basic MCP setup with Serena AI assistant"
        },
        "development": {
            "tools": ["serena"],
            "description": "Development-focused MCP tools for coding assistance"
        },
        "full": {
            "tools": ["serena"],
            "description": "Full MCP setup with all available tools"
        }
    }
    
    if not presets:
        console.print("[yellow]No MCP presets available.[/yellow]")
        return
    
    table = Table(title="Available MCP Presets")
    table.add_column("Preset", style="cyan", no_wrap=True)
    table.add_column("Tools", style="green")
    table.add_column("Description", style="dim")
    
    for preset_name, preset_info in presets.items():
        table.add_row(
            preset_name,
            ", ".join(preset_info["tools"]),
            preset_info["description"]
        )
    
    console.print(table)


def mcp_install_command(
    preset_name: str,
    project_path: Optional[str] = None
) -> None:
    """Install MCP tools from a preset."""
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)
    
    if not project_path.exists():
        console.print(f"[red]Project path does not exist: {project_path}[/red]")
        raise typer.Exit(1)
    
    # Define available presets
    presets = {
        "basic": ["serena"],
        "development": ["serena"],
        "full": ["serena"]
    }
    
    tool_names = presets.get(preset_name)
    if not tool_names:
        console.print(f"[red]Preset '{preset_name}' not found.[/red]")
        available_presets = list(presets.keys())
        if available_presets:
            console.print(f"Available presets: {', '.join(available_presets)}")
        raise typer.Exit(1)
    
    console.print(f"[cyan]Installing MCP preset '{preset_name}' to {project_path}[/cyan]")
    
    # Create MCP config directory
    mcp_config_dir = project_path / "mcp" / "config"
    mcp_config_dir.mkdir(parents=True, exist_ok=True)
    
    templates_dir = get_templates_dir()
    source_mcp_dir = templates_dir / "mcp"
    
    installed_tools = []
    failed_tools = []
    
    for tool_name in tool_names:
        try:
            # Copy configuration file from templates
            source_config = source_mcp_dir / "config" / f"{tool_name}.json"
            target_config = mcp_config_dir / f"{tool_name}.json"
            
            if source_config.exists():
                shutil.copy2(source_config, target_config)
                console.print(f"  ✓ Configured {tool_name} at {target_config}")
                installed_tools.append(tool_name)
            else:
                failed_tools.append(f"{tool_name}: Template not found")
            
        except Exception as e:
            failed_tools.append(f"{tool_name}: {str(e)}")
    
    # Summary
    console.print()
    if installed_tools:
        console.print(f"[green]Successfully installed {len(installed_tools)} MCP tools:[/green]")
        for tool_name in installed_tools:
            console.print(f"  • {tool_name}")
    
    if failed_tools:
        console.print(f"[yellow]Failed to install {len(failed_tools)} tools:[/yellow]")
        for failure in failed_tools:
            console.print(f"  • {failure}")


def mcp_recommend_command(
    project_type: Optional[str] = None
) -> None:
    """Get MCP tool recommendations for a project type."""
    if project_type is None:
        # Interactive selection
        project_types = {
            "python": "Python project",
            "javascript": "JavaScript/Node.js project", 
            "typescript": "TypeScript project",
            "web": "Web development project",
            "documentation": "Documentation project",
            "testing": "Testing-focused project",
            "general": "General purpose project"
        }
        
        project_type = select_with_arrows(
            project_types,
            "Select your project type",
            "general"
        )
    
    # Define recommendations based on project type
    recommendations = {
        "python": "development",
        "javascript": "development", 
        "typescript": "development",
        "web": "development",
        "documentation": "basic",
        "testing": "development",
        "general": "basic"
    }
    
    preset_descriptions = {
        "basic": "Basic MCP setup with Serena AI assistant for general development tasks",
        "development": "Development-focused MCP tools optimized for coding and project management",
        "full": "Complete MCP setup with all available tools for advanced development workflows"
    }
    
    recommended_preset = recommendations.get(project_type, "basic")
    
    console.print(f"[cyan]For a {project_type} project, we recommend the '[bold]{recommended_preset}[/bold]' preset.[/cyan]")
    
    preset_description = preset_descriptions.get(recommended_preset, "No description available")
    console.print(f"\n[dim]{preset_description}[/dim]")
    
    # Define presets and their tools
    presets = {
        "basic": ["serena"],
        "development": ["serena"],
        "full": ["serena"]
    }
    
    tool_names = presets.get(recommended_preset, [])
    
    if tool_names:
        console.print(f"\nThis preset includes:")
        for tool_name in tool_names:
            console.print(f"  ✓ [cyan]{tool_name}[/cyan] - MCP configuration for {tool_name}")
    
    console.print(f"\nTo install this preset, run:")
    console.print(f"[yellow]specify mcp install {recommended_preset}[/yellow]")
