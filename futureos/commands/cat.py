from typing import Any
from pathlib import Path
from futureos.commands.command import Command
from futureos.utils.path_utils import get_files_in_directory, resolve_path


class cat(Command):
    """
    Command: File Content Reader (cat)
    
    Shows the CONTENTS INSIDE a specific file. Used when you need to see what 
    information is stored in a particular file, especially configuration details,
    credentials, or saved data.
    
    Natural Language Patterns:
    - "Got to check what API keys I put in here"
    - "Need to verify these configuration details"
    - "What's written in this file?"
    - "Can you read this out for me?"
    - "Show me content of work log"
    - "What does this file contain?"
    - "Print content of file with database settings"
    
    Key Concepts:
    - Reading SPECIFIC file contents
    - Checking saved credentials/settings
    - Viewing stored configuration
    - Examining file contents
    
    Context Clues:
    - Reference to specific file content (API keys, passwords, settings)
    - Wanting to see what's saved IN a file
    - Verifying stored information
    - Reading/showing file contents
    
    NOT For:
    - Seeing what files exist in a directory (use 'ls')
    - Making changes to files (use 'nano')
    - Deleting files (use 'rm')
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
