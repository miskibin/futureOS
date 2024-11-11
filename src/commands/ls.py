from pathlib import Path
from typing import Any
from commands.command import Command
import constants
from utils.get_all_paths import (
    get_all_paths,
)  # Replace 'from constants import CURRENT_DIRECTORY, BASE_PATH'


class ls(Command):
    """
    NAME
        ls - list directory contents

    SYNOPSIS
        ls [directory]
        --graph (-g) Display all files in the file system
    DESCRIPTION
        List information about the files in the current directory.
        If a directory is specified, list contents of that directory.

    NATURAL LANGUAGE COMMANDS
        - Show files in directory X
        - List contents of folder X
        - What is in directory X
    """

    def _configure_parser(self) -> None:
        self.parser.add_argument(
            "directory",
            nargs="?",
            type=Path,
            help="Directory to list",
        )
        self.parser.add_argument(
            "--graph",
            "-g",
            action="store_true",
            help="Display all files in the file system",
        )
        self.parser.add_argument(
            '--query',
            '-q',
            type=str,
            help='Natural language query to filter paths'
        )
        

    def execute(self, args: Any) -> None:
        try:
            if args.query:
                all_paths = get_all_paths()
                context = "\n".join(all_paths)
                prompt_template = (
                    "Given the following list of file paths:\n"
                    "{context}\n\n"
                    "Answer the following question and provide only the relevant paths:\n"
                    "{question}"
                )
                result = self.run_nlp(context, args.query, prompt_template)
                self.print(result)
                return

            if args.graph:# ONLY FOR DEBUGGING
                self.print("\n".join(get_all_paths()))
                return
            if not args.directory:
                target_path = constants.CURRENT_DIRECTORY
            else:
                target_path = (constants.CURRENT_DIRECTORY / args.directory).resolve()

            # Ensure the target path is within BASE_PATH
            if not str(target_path).startswith(str(constants.BASE_PATH)):
                raise Exception("Access denied: Cannot access outside of base path.")

            if target_path.is_dir():
                files = [f.name for f in target_path.iterdir()]
                self.print("\n".join(files))
            else:
                self.print(f"Error: '{args.directory}' is not a directory", style="red")
        except Exception as e:
            self.print(f"Error: {str(e)}", style="red")
