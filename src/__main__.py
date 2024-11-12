import os
import shlex
import sys
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from constants import BASE_PATH, CURRENT_DIRECTORY
from commands import get_command, COMMAND_LIST
from init.create_collections import COMMANDS_COLLECTION, initialize_commands

console = Console()  # Global console instance


def get_prompt() -> str:
    """Generate the shell prompt string."""
    try:
        path = str(CURRENT_DIRECTORY).replace(str(BASE_PATH), "")
        return f"{path} $ "
    except Exception:
        return f"{CURRENT_DIRECTORY} $ "


def show_help(command: Optional[str] = None) -> None:
    """Show help for all commands or a specific command."""
    if command and command in COMMAND_LIST:
        get_command(command)(["--help"])
        return

    table = Table(title="Available Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")

    # Add built-in commands
    table.add_row("help", "Show this help message")
    table.add_row("exit/quit", "Exit the shell")

    # Add registered commands
    for cmd_name, cmd_class in sorted(COMMAND_LIST.items()):
        desc = next(
            (
                line.strip()
                for line in (cmd_class.__doc__ or "").split("\n")
                if line.strip() and not line.strip().startswith("NAME")
            ),
            "No description available",
        )
        table.add_row(cmd_name, desc)

    console.print(table)

def execute_command(command_name: str, args: List[str]) -> None:
    """Execute a command with given arguments."""
    command = get_command(command_name)
    if not command:  # Run AI command search
        cmd_id = None
        with console.status("Finding best command match..."):
            results = COMMANDS_COLLECTION.query(
                query_texts=f"{command_name} {' '.join(args)}", 
                n_results=1
            )
            cmd_id = results["ids"][0][0]
            command = get_command(cmd_id)
        
        # Execute command without status message for editor
        command(["-q", f"'{command_name} {' '.join(args)}'"])
    else:
        command(args)


def cleanup_and_exit():
    """Clean up resources and exit properly."""
    console.print("\nGoodbye!", style="blue bold")
    console.clear()
    sys.exit(0)


def main():
    initialize_commands()
    console.print("Type 'help' for available commands", style="blue")

    while True:
        try:
            command_line = Prompt.ask(get_prompt())

            if not command_line.strip():
                continue

            try:
                parts = shlex.split(command_line)
                command_name = parts[0].lower()
                args = parts[1:]

                if command_name in ("exit", "quit", "q"):
                    cleanup_and_exit()
                elif command_name == "help":
                    show_help(args[0] if args else None)
                else:
                    execute_command(command_name, args)

            except ValueError as e:
                console.print(f"Error: Invalid syntax: {e}", style="red")
            except Exception as e:
                console.print(f"Error: {str(e)}", style="red")

        except KeyboardInterrupt:
            cleanup_and_exit()
        except Exception as e:
            console.print(f"\nUnexpected error: {str(e)}", style="red bold")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup_and_exit()
