"""
UI utilities for the Cognitive Archaeology Tribunal CLI.
Uses 'rich' library for styled terminal output.
"""
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

# Define custom theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "success": "green",
    "step": "blue"
})

console = Console(theme=custom_theme)

def print_header(title: str, subtitle: str = ""):
    """Print the main application header."""
    console.print()
    console.print(Panel(
        f"[bold white]{title}[/bold white]\n[italic]{subtitle}[/italic]",
        border_style="blue",
        expand=False
    ))
    console.print()

def print_step(step_num: int, total_steps: int, text: str):
    """Print a progress step."""
    console.print(f"\n[step][{step_num}/{total_steps}][/step] [bold]{text}[/bold]")
    console.print("-" * 60, style="dim")

def print_success(text: str):
    """Print a success message."""
    console.print(f"[success]✓[/success] {text}")

def print_error(text: str):
    """Print an error message."""
    console.print(f"[error]✗ {text}[/error]")

def print_warning(text: str):
    """Print a warning message."""
    console.print(f"[warning]![/warning] {text}")

def print_section(text: str):
    """Print a section header."""
    console.print(f"\n[bold underline]{text}[/bold underline]")
