from pathlib import Path
from typing import Any
from commands.command import Command
from constants import CURRENT_DIRECTORY, BASE_PATH


class pwd(Command):
    """
    NAME
        pwd - print name of current/working directory

    SYNOPSIS
        pwd

    DESCRIPTION
        Print the full filename of the current working directory.

    NATURAL LANGUAGE COMMANDS
        - Where am I?
        - Show my current directory
    """

    def _configure_parser(self) -> None:
        pass

    def execute(self, args: Any) -> None:
        path = str(CURRENT_DIRECTORY).replace(str(BASE_PATH), "~")
        self.print(path, style="bold blue")


