from typing import Any
from futureos.commands.command import Command
from futureos.utils.console_manager import future_console as console


class cls(Command):
    """
    Command: Clear Screen (cls)

    Clears the console screen. This command helps you clean up the terminal
    display by removing all previous outputs.

    Natural Language Patterns:
    - "Clear the screen"
    - "Clean the terminal"
    - "Wipe the display"
    - "Clear the console"

    Key Concepts:
    - Clearing the screen
    - Cleaning the terminal
    - Wiping the display
    """

    def execute(self, args: Any) -> None:
        console.clear()
