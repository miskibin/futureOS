from pathlib import Path
from typing import Any
from futureos.commands.command import Command
import futureos.constants
from futureos.utils.path_utils import resolve_path


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
        - go to the X dir
        - Move to directory X
        - Navigate to directory X
        - Switch to directory X
        - Take me to folder X
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
            directory = self.get_directory(args.query) if args.query else args.directory
            target_path = constants.BASE_PATH / Path("home") if directory == "~" else resolve_path(directory)
            if target_path.is_dir():
                constants.CURRENT_DIRECTORY = target_path
                self.print(f"Changed to {target_path}", style="green")
            else:
                self.print(f"Error: '{target_path}' is not a directory", style="red")
        except Exception as e:
            self.print(f"Error: {str(e)}", style="red")
