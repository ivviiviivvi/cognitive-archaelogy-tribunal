"""
UI utility module for rich CLI output with fallback.
"""
try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

class UI:
    """Helper class for CLI output with rich support and fallback."""

    @staticmethod
    def header(title, sub=""):
        if HAS_RICH:
            console.print(Panel(f"[bold blue]{title}[/]\n{sub}", expand=False))
        else:
            print(f"{'='*70}\n{title}\n{sub}\n{'='*70}")

    @staticmethod
    def section(title):
        if HAS_RICH:
            console.print(f"\n[bold cyan]{title}[/]")
            console.rule(style="cyan")
        else:
            print(f"\n{title}\n{'-'*70}")

    @staticmethod
    def success(msg):
        if HAS_RICH:
            console.print(f"[green]✓ {msg}[/]")
        else:
            print(f"✓ {msg}")

    @staticmethod
    def error(msg):
        if HAS_RICH:
            console.print(f"[bold red]✗ {msg}[/]")
        else:
            print(f"✗ {msg}")

    @staticmethod
    def info(msg):
        if HAS_RICH:
            console.print(msg)
        else:
            print(msg)
