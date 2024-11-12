import shlex
from pathlib import Path
from typing import Optional
from utils.console_manager import future_console as console
from constants import BASE_PATH, CURRENT_DIRECTORY
from commands import answer, get_command, COMMAND_LIST
from init.create_collections import (
    COMMANDS_COLLECTION,
    initialize_commands,
    initialize_files_collection,
)


def get_prompt() -> str:
    """Generate the shell prompt string."""
    try:
        path = str(CURRENT_DIRECTORY).replace(str(BASE_PATH), "")
        username = "user"  # You could make this dynamic
        hostname = "futureOS"  # You could make this dynamic
        return f"[user]{username}[/user]@[system]{hostname}[/system] [path]{path}[/path] $ "
    except Exception:
        return f"[path]{CURRENT_DIRECTORY}[/path] $ "


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
    initialize_commands(COMMAND_LIST)
    initialize_files_collection()

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
    except KeyboardInterrupt:
        console.exit("👋 Goodbye!")
