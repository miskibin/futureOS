from typing import Any
from pathlib import Path
from commands.command import Command
import constants


class cat(Command):
    """
    NAME
        cat - concatenate and print files

    SYNOPSIS
        cat [file1] [file2] ...

    DESCRIPTION
        Reads files sequentially and writes them to standard output.

    NATURAL LANGUAGE COMMANDS
        - Show the contents of file X
        - Display file X
        - Read file X
    """

    def _configure_parser(self) -> None:
        self.parser.add_argument("files", nargs="+", type=Path, help="Files to display")

    def execute(self, args: Any) -> None:
        for file_path in args.files:
            resolved_path = (constants.CURRENT_DIRECTORY / file_path).resolve()

            # Ensure the path is within BASE_PATH
            if not str(resolved_path).startswith(str(constants.BASE_PATH)):
                self.print(f"Access denied: {file_path}", style="red")
                continue

            if resolved_path.is_file():
                try:
                    with open(resolved_path, "r") as file:
                        self.print(file.read())
                except Exception as e:
                    self.print(f"Error reading {file_path}: {str(e)}", style="red")
            else:
                self.print(f"'{resolved_path}' is not a file", style="red")
