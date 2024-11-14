import os
import shlex
from pathlib import Path
import sys
from typing import Optional

import chromadb.server
from futureos.init.initialize_filesystem import initialize_filesystem
from futureos.utils.console_manager import future_console as console
import futureos.constants
from futureos.commands import answer, get_command, COMMAND_LIST
from futureos.init.create_collections import (
    COMMANDS_COLLECTION,
    DIRECTORIES_COLLECTION,
    initialize_commands,
    initialize_directories_collection,
    initialize_files_collection,
)


def get_prompt() -> str:
    """Generate the shell prompt string."""
    try:
        path = (
            str(constants.CURRENT_DIRECTORY)
            .lower()
            .replace(str(constants.BASE_PATH).lower(), "")
        )
        username = os.getlogin()
        hostname = "futureOS"  # You could make this dynamic
        return f"[user]{username}[/user]@[system]{hostname}[/system] [path]{path}[/path] $ "
    except Exception:
        return f"[path]{constants.CURRENT_DIRECTORY}[/path] $ "


def show_help(command: Optional[str] = None) -> None:
    """Show help for all commands or a specific command."""
    if command and command in COMMAND_LIST:
        console.show_panel(f"Help for command: {command}", "Command Help")
        get_command(command)(["--help"])
        return

    # Show general help
    console.show_panel(
        "Welcome to FutureOS Help\n"
        "Type 'help <command>' for detailed information about a specific command",
        "FutureOS Help System",
    )

    columns = ["Command", "Description"]
    rows = []

    # Add built-in commands
    rows.append(["help", "Show this help message"])
    rows.append(["exit/quit", "Exit the shell"])

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
        rows.append([cmd_name, desc])

    console.show_table("Available Commands", columns, rows)


def execute_command(command_line: str) -> None:
    """Execute a command with the full command line input."""
    try:
        parts = shlex.split(command_line)
        command_name = parts[0].lower()
        args = parts[1:]

        command = get_command(command_name)
        if command:
            command(args)
            return
        results = COMMANDS_COLLECTION.query(query_texts=[command_line], n_results=1)
        cmd_id = results["ids"][0][0]
        command = get_command(cmd_id)

        if results["distances"][0][0] > 1.7:
            get_command("answer")(["-q", command_line])
            # console.error("I don't think I can help you with that command.")
            # console.info("Try 'help' to see available commands.")
        else:
            command(["-q", command_line])
    except ValueError as e:
        console.error(f"Invalid syntax: {e}")
        console.info("Type 'help' for usage information")
    except Exception as e:
        console.error(str(e))


def main():
    initialize_filesystem(constants.BASE_PATH)
    initialize_commands(COMMAND_LIST)
    initialize_files_collection()
    initialize_directories_collection()
    # Show welcome message
    console.clear()
    console.show_panel(
        "Welcome to [highlight]FutureOS[/highlight]\n"
        "Your AI-powered operating system\n\n"
        "Type [command]help[/command] for available commands",
        "⚡ FutureOS v1.0",
    )

    while True:
        try:
            command_line = console.prompt(get_prompt())
            command_line = command_line.strip()

            if not command_line:
                continue

            if command_line.lower() in ("exit", "quit", "q"):
                console.exit("👋 Thank you for using FutureOS!")
            elif command_line.startswith("help"):
                parts = shlex.split(command_line)
                show_help(parts[1] if len(parts) > 1 else None)
            else:
                execute_command(command_line)

        except KeyboardInterrupt:
            console.exit("👋 Goodbye!")
        except Exception as e:
            console.error(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    try:
        main()
        # initialize_directories_collection()
        # query_text = "Current directory: /home\n list files from the work directory"
        # result = DIRECTORIES_COLLECTION.query(
        #     query_texts=[query_text], n_results=3, include=["documents", "distances"]
        # )
        # print(f"query\n\n{query_text}\nRESULT\n", result)
        # exit()
    except KeyboardInterrupt:
        console.exit("👋 Goodbye!")
