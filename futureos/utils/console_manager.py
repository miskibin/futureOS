import sys
from typing import Optional, Any
from rich.console import Console
from rich.status import Status
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.theme import Theme
from loguru import logger


class FutureConsole:
    """Simplified console manager for FutureOS."""

    def __init__(self):
        self.theme = Theme(
            {
                # Essential styles
                "info": "cyan2",
                "success": "green3",
                "error": "red1 bold",
                "warning": "yellow2",
                "system": "blue bold",
                "path": "#a78bfa",  # Purple
                # Table styles
                "table.header": "blue bold",
                "table.cell": "white",
            }
        )

        self.console = Console(theme=self.theme)
        self._configure_logger()

    def _configure_logger(self):
        """Configure minimal logging format."""
        logger.remove()
        logger.add(
            sys.stderr,
            format="{time:HH:mm:ss} | {level: <8} | {message}",
            level="INFO",
            colorize=True,
        )

    def print(self, message: str, style: Optional[str] = None) -> None:
        """Print a message with optional styling."""
        self.console.print(message, style=style)

    def status(self, message: str) -> Status:
        """Create a status spinner with message."""
        return self.console.status(message, spinner="dots")

    def prompt(self, message: str, password: bool = False) -> str:
        """Get user input with optional password masking."""
        return Prompt.ask(message, password=password, console=self.console)

    def show_table(self, title: str, columns: list, rows: list) -> None:
        """Display data in a formatted table."""
        table = Table(title=title)
        for col in columns:
            table.add_column(col, style="table.header")
        for row in rows:
            table.add_row(*row)
        self.console.print(table)

    def show_panel(self, content: str, title: Optional[str] = None) -> None:
        """Display content in a panel."""
        self.console.print(Panel(content, title=title))

    def error(self, message: str) -> None:
        """Display an error message."""
        self.print(f"Error: {message}", style="error")

    def success(self, message: str) -> None:
        """Display a success message."""
        self.print(message, style="success")

    def warning(self, message: str) -> None:
        """Display a warning message."""
        self.print(message, style="warning")

    def system(self, message: str) -> None:
        """Display a system message."""
        self.print(message, style="system")

    def info(self, message: str) -> None:
        """Display an info message."""
        self.print(message, style="info")

    def path(self, path: str) -> None:
        """Display a file system path."""
        self.print(path, style="path")

    def clear(self) -> None:
        """Clear the console screen."""
        self.console.clear()

    def exit(self, message: Optional[str] = None) -> None:
        """Exit the system with optional message."""
        if message:
            self.system(message)
        self.clear()
        sys.exit(0)


# Create a global console instance
future_console = FutureConsole()
