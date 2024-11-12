from typing import Any
from pathlib import Path
from commands.command import Command
from utils.path_utils import get_files_in_directory, resolve_path


class cat(Command):
    """
    cat: read file contents

    FILE CONTENT TERMS:
    file-contents read-file show-contents file-text content-of-file
    inside-file written-in-file file-data text-content read-contents

    CONTENT PATTERNS:
    read-from-X contents-of-X written-in-X inside-X data-in-X
    whats-in-file show-text display-content read-data show-inside

    RETURNS: contents of files only
    NOT FOR: directory contents, file paths, file editing
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
