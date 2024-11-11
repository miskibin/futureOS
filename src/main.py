import os
import shlex
from pathlib import Path
from typing import List, Optional
from commands import get_command, COMMAND_LIST
from commands.command import Command
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from constants import BASE_PATH
import constants


def get_prompt() -> str:
    """Generate the shell prompt string."""
    try:
        # Use CURRENT_DIRECTORY relative to BASE_PATH
        path = str(constants.CURRENT_DIRECTORY).replace(str(BASE_PATH), "~")
        return f"{path} $ "
    except Exception:
        return f"{constants.CURRENT_DIRECTORY} $ "


def show_help(args: Optional[List[str]] = None) -> None:
    """Show help for all commands or a specific command."""
    console = Console()

    if args and args[0] in COMMAND_LIST:
        # Show help for specific command
        command = get_command(args[0])
        command(["--help"])
        return

    # Show general help
    table = Table(title="Available Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")

    # Add built-in commands
    table.add_row("help", "Show this help message")
    table.add_row("exit/quit", "Exit the shell")

    # Add all registered commands
    for cmd_name, cmd_class in sorted(COMMAND_LIST.items()):
        doc = cmd_class.__doc__ or ""
        description = next(
            (
                line.strip()
                for line in doc.split("\n")
                if line.strip() and not line.strip().startswith("NAME")
            ),
            "No description available",
        )
        table.add_row(cmd_name, description)

    console.print(table)


def main():
    console = Console()

    # Show welcome message
    console.print("Type 'help' for a list of commands", style="blue")

    # Main shell loop
    while True:
        try:
            # Get command from user
            command_line = Prompt.ask(get_prompt())
            # Handle empty input
            if not command_line.strip():
                continue

            # Parse command and arguments
            try:
                parts = shlex.split(command_line)
                command_name = parts[0].lower()
                args = parts[1:]
            except ValueError as e:
                console.print(f"Error: Invalid command syntax: {e}", style="red")
                continue

            # Handle built-in commands
            if command_name in ("exit", "quit"):
                console.print("Goodbye!", style="blue bold")
                break
            elif command_name == "help":
                show_help(args if args else None)
                continue

            # Get and execute command
            try:
                command = get_command(command_name)
                command(args)
            except ValueError as e:
                console.print(f"Error: Unknown command: '{command_name}'", style="red")
            except Exception as e:
                console.print(f"Error executing command: {str(e)}", style="red")

        except KeyboardInterrupt:
            console.print("\nUse 'exit' or 'quit' to exit the shell", style="yellow")
        except Exception as e:
            console.print(f"\nUnexpected error: {str(e)}", style="red bold")


if __name__ == "__main__":
    main()
