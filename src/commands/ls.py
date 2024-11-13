from abc import ABC, abstractmethod
from typing import Optional, Any
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from commands.command import Command
import constants
from utils.path_utils import get_all_directories, get_relative_path, resolve_path


class ls(Command):
    """
    ls: list directory contents

    DIRECTORY TERMS:
    list-files show-files directory-contents folder-contents list-directory
    file-list folder-list directory-items folder-items list-contents

    FILE LISTING PATTERNS:
    files-in-X contents-of-X items-in-X files-here list-everything
    show-files display-files what-files list-files show-contents

    RETURNS: list of files and folders only
    NOT FOR: file contents, file paths, file editing
    """

    def _configure_parser(self) -> None:
        self.parser.add_argument(
            "directory", nargs="?", type=Path, help="Directory to list"
        )
        self.parser.add_argument(
            "--graph", "-g", action="store_true", help="Display file system graph"
        )

    def execute(self, args: Any) -> None:
        directory = args.directory
        if args.query:
            directory = self.get_directory(args.query)
            if directory:
                directory = Path(directory)
            else:
                self.print("No matching directory found.", style="red")
                return

        if args.graph:
            for dir_path, files in get_all_directories().items():
                self.print(
                    f"[blue]{dir_path}[/blue]: [green]{', '.join(files)}[/green]"
                )
            return
        target_path = resolve_path(directory if directory else ".")

        if target_path.is_dir():
            self.print("\n".join(f.name for f in target_path.iterdir()))
        else:
            self.print(f"Error: {target_path} Not a directory", style="red")
