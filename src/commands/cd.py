import os
from pathlib import Path
from typing import Any
from commands.command import Command
import constants


class cd(Command):
    """
    NAME
        cd - change the current working directory

    SYNOPSIS
        cd [directory]

    DESCRIPTION
        Change the current working directory to the specified directory.
        If no directory is specified, return to the root directory.

    NATURAL LANGUAGE COMMANDS
        - Change directory to X
        - Go to folder X
        - Move to directory X
    """

    def _configure_parser(self) -> None:
        self.parser.add_argument(
            "directory",
            nargs="?",
            default="~",
            type=str,
            help="Directory to change to",
        )

    def execute(self, args: Any) -> None:
        try:
            if args.directory == "~":
                target_path = constants.BASE_PATH / Path("root")
            else:
                target_path = (
                    constants.CURRENT_DIRECTORY / Path(args.directory)
                ).resolve()

            # Ensure the target path is within BASE_PATH
            if not str(target_path).startswith(str(constants.BASE_PATH)):
                raise Exception("Access denied: Cannot navigate outside of base path.")

            if target_path.is_dir():
                constants.CURRENT_DIRECTORY = target_path
                self.print(f"Changed to {target_path}", style="green")
            else:
                self.print(f"Error: '{target_path}' is not a directory", style="red")
        except Exception as e:
            self.print(f"Error: {str(e)}", style="red")
