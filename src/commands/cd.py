import os
from pathlib import Path
from typing import Any
from commands.command import Command
import constants
from utils.path_utils import resolve_directory, get_all_directories


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
            directory = args.directory
            if args.query:
                all_paths = get_all_directories()
                context = "\n".join(f"{d}: {', '.join(f)}" for d, f in all_paths.items())
                prompt = ("Given the directory list:\n{context}\n"
                          "Which directory is most relevant? Return only the path:\n{question}")
                directory = self.run_nlp(context, args.query, prompt)
                self.print(f"Found: directory: {directory}", style="green")

            if directory == "~":
                target_path = constants.BASE_PATH / Path("home")
            else:
                target_path = resolve_directory(directory)

            if target_path.is_dir():
                constants.CURRENT_DIRECTORY = target_path
                self.print(f"Changed to {target_path}", style="green")
            else:
                self.print(f"Error: '{target_path}' is not a directory", style="red")
        except Exception as e:
            self.print(f"Error: {str(e)}", style="red")