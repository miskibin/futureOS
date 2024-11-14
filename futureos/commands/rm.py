from typing import Any
from pathlib import Path
from futureos.commands.command import Command
from futureos.utils.path_utils import get_relative_path, resolve_path


class rm(Command):
    """
    Command: Remove Files (rm)

    PERMANENTLY DELETES files. Use when you want to remove unwanted files
    or clean up unnecessary content.

    Natural Language Patterns:
    - "Need to get rid of report.txt"
    - "Got to delete this file"
    - "There are some project notes I don't need anymore"
    - "Help me clean up these old files"
    - "Need to remove some sensitive data files"

    Key Concepts:
    - DELETING files
    - REMOVING content
    - CLEANING UP space
    - Getting rid of files

    Context Clues:
    - Mentions of deletion/removal
    - Cleaning up files
    - Getting rid of content
    - No longer needed files

    NOT For:
    - Viewing file contents (use 'cat')
    - Checking directory contents (use 'ls')
    - Editing files (use 'nano')
    """

    def _configure_parser(self) -> None:
        self.parser.add_argument(
            "files", nargs="*", type=Path, help="Files to remove", default=None
        )

    def execute(self, args: Any) -> None:
        filename = None
        if args.query:
            filename = self.get_file(args.query, max_distance=1.7)
            if filename is None:
                self.print("I could not find the file you are looking for", style="red")
                return

        files = [filename] if filename else args.files
        for file_path in files:
            resolved_path = resolve_path(file_path)
            if resolved_path.is_file():
                if self.confirm_action(
                    f"Are you sure you want to delete '{resolved_path.name}'?"
                ):
                    try:
                        resolved_path.unlink()
                        self.print(f"Deleted {resolved_path}", style="green")
                        self.update_indexes(
                            "files",
                            ids=[str(get_relative_path(resolved_path))]
                        )
                    except Exception as e:
                        self.print(f"Error deleting {file_path}: {str(e)}", style="red")
            else:
                self.print(f"'{resolved_path}' is not a file", style="red")
