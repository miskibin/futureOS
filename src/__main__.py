import os
import shlex
import sys
from pathlib import Path
from typing import List, Optional
from loguru import logger
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from constants import BASE_PATH, CURRENT_DIRECTORY
from commands import get_command, COMMAND_LIST
from init.create_collections import (
    COMMANDS_COLLECTION,
    initialize_commands,
    initialize_files_collection,
)

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


def execute_command(command_line: str) -> None:
    """Execute a command with the full command line input."""
    try:
        # First try to parse as a direct command
        parts = shlex.split(command_line)
        command_name = parts[0].lower()
        args = parts[1:]

        command = get_command(command_name)
        if command:
            # Direct command match found, execute normally
            command(args)
            return

        # No direct match, use embedding search on full command line
        with console.status("Finding best command match..."):
            results = COMMANDS_COLLECTION.query(query_texts=[command_line], n_results=1)
            cmd_id = results["ids"][0][0]
            command = get_command(cmd_id)

        logger.info(
            f"Best match for command line '{command_line}': {cmd_id} similarity: {results['distances'][0][0]}"
        )
        if results["distances"][0][0] > 1.6:
            console.print(
                f"I don't think i can help you with that.",
                style="red",
            )
        else:
            command(["-q", command_line])

    except ValueError as e:
        console.print(f"Error: Invalid syntax: {e}", style="red")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")


def cleanup_and_exit():
    """Clean up resources and exit properly."""
    console.print("\nGoodbye!", style="blue bold")
    console.clear()
    sys.exit(0)


def main():
    initialize_commands(COMMAND_LIST)
    initialize_files_collection()
    console.print("Type 'help' for available commands", style="blue")

    while True:
        try:
            command_line = Prompt.ask(get_prompt())
            command_line = command_line.strip()

            if not command_line:
                continue

            if command_line.lower() in ("exit", "quit", "q"):
                cleanup_and_exit()
            elif command_line.startswith("help"):
                parts = shlex.split(command_line)
                show_help(parts[1] if len(parts) > 1 else None)
            else:
                execute_command(command_line)

        except KeyboardInterrupt:
            cleanup_and_exit()
        except Exception as e:
            console.print(f"\nUnexpected error: {str(e)}", style="red bold")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup_and_exit()
