"""
UI Utilities for Cognitive Archaeology Tribunal.
Provides styled output using the rich library.
"""

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text

# Define custom theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "green",
    "step": "bold blue",
    "header": "bold magenta",
    "highlight": "bold white",
})

# Initialize console with theme
console = Console(theme=custom_theme)

def print_header(title: str, subtitle: str = None):
    """Prints a styled header panel."""
    text = Text(title, justify="center", style="header")
    if subtitle:
        text.append(f"\n{subtitle}", style="italic white")
    console.print(Panel(text, border_style="blue", expand=False, padding=(1, 4)))
    console.print()

def print_step(message: str):
    """Prints a step indicator."""
    console.print(f"[step]➤[/step] {message}")

def print_success(message: str):
    """Prints a success message."""
    console.print(f"[success]✓[/success] {message}")

def print_error(message: str):
    """Prints an error message."""
    console.print(f"[error]✗[/error] {message}")

def print_warning(message: str):
    """Prints a warning message."""
    console.print(f"[warning]![/warning] {message}")

def print_info(message: str):
    """Prints an info message."""
    console.print(f"[info]ℹ[/info] {message}")
