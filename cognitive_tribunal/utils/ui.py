"""
UI utilities for the Cognitive Archaeology Tribunal CLI.
Uses 'rich' library for styled output.
"""
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

# Custom theme for consistent styling
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "green",
    "step": "bold blue",
})

# Initialize console with the custom theme
console = Console(theme=custom_theme)

def print_header(title, subtitle=None):
    """Prints a styled header panel."""
    console.print()
    console.print(Panel(
        f"[bold white]{title}[/bold white]" + (f"\n[dim]{subtitle}[/dim]" if subtitle else ""),
        style="blue",
        expand=False
    ))
    console.print()

def print_step(message):
    """Prints a step header."""
    console.print(f"\n[step]➜[/step] [bold]{message}[/bold]")
    console.print("[dim]" + "-" * 40 + "[/dim]")

def print_success(message):
    """Prints a success message."""
    console.print(f"[success]✓[/success] {message}")

def print_error(message):
    """Prints an error message."""
    console.print(f"[error]✗[/error] {message}")

def print_warning(message):
    """Prints a warning message."""
    console.print(f"[warning]![/warning] {message}")

def print_info(message):
    """Prints an info message."""
    console.print(f"[info]i[/info] {message}")
