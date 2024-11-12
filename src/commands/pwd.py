from pathlib import Path
from typing import Any
from commands.command import Command
import constants


class pwd(Command):
    """
    NAME
        pwd - print working directory

    SYNOPSIS
        pwd

    DESCRIPTION
        Print the full pathname of the current working directory.
        The path starts from the root directory (/).

    NATURAL LANGUAGE COMMANDS
        - Where am I?
        - Display current location
        - What folder am I in?
        - Print current directory path
    """

    def _configure_parser(self) -> None:
        pass

    def execute(self, args: Any) -> None:
        path = str(constants.CURRENT_DIRECTORY).replace(str(constants.BASE_PATH), "~")
        self.print(path, style="bold blue")
