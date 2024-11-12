from typing import Any
from pathlib import Path
from commands.command import Command
import constants
from utils.path_utils import get_files_in_directory, resolve_path


class cat(Command):
    """
    NAME
         cat -  display files

     SYNOPSIS
         cat [file1] [file2] ...

     DESCRIPTION
         Read files sequentially and write them to standard output.
         When multiple files are specified, their contents are concatenated.

     NATURAL LANGUAGE COMMANDS
         - Show the contents of file X
         - Display file X
         - Read file X
         - Show me data regarding topic X
         - Print file X contents
         - Let me see what's in file X
         - Show me file X
    """

    def _configure_parser(self) -> None:
        self.parser.add_argument("files", nargs="*", type=Path, help="Files to display", default=None)

    def execute(self, args: Any) -> None:
        filename = None
        if args.query:
            all_paths = get_files_in_directory(constants.CURRENT_DIRECTORY)
            context = "\n".join(f"{f}" for f in all_paths)
            prompt = (
                "Given the file list:\n{context}\n"
                "Which file is most relevant? Return ONLY 1 the path:\n{question}"
                "ONE valid path without explanation: "
            )
            filename = self.run_nlp(context, args.query, prompt)
            filename = filename.replace("'", "").replace('"', "")
            self.print(f"Found: filename: {filename}", style="green")
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
