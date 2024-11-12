from typing import Any
from pathlib import Path
from commands.command import Command
from utils.path_utils import get_files_in_directory, resolve_path


class cat(Command):
    """
    NAME
         cat - display file contents

     DESCRIPTION
         Read files and print them to standard output.
         When multiple files are specified, their contents are concatenated.

     NATURAL LANGUAGE COMMANDS
         - Show the contents of file X
         - Show me X file
         - Display file X
         - Read file X
         - Show me data regarding topic X
         - Print file X contents
         - Let me see what's in file X
         - Show me file X
         - Read the contents of file X
         - Display the data in file X
    """

    def _configure_parser(self) -> None:
        self.parser.add_argument(
            "files", nargs="*", type=Path, help="Files to display", default=None
        )

    def execute(self, args: Any) -> None:
        filename = None
        if args.query:
            filename = self.get_file(args.query)
        files = [filename] if filename else args.files
        for file_path in files:
            resolved_path = resolve_path(file_path)
            if resolved_path.is_file():
                try:
                    with open(resolved_path, "r") as file:
                        self.print(file.read())
                except Exception as e:
                    self.print(f"Error reading {file_path}: {str(e)}", style="red")
            else:
                self.print(f"'{resolved_path}' is not a file", style="red")
