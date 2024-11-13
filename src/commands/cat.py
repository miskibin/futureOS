from typing import Any
from pathlib import Path
from commands.command import Command
from utils.path_utils import get_files_in_directory, resolve_path


class cat(Command):
    """
    Command: File Content Reader (cat)
    
    Displays the actual text and information stored within files. Focused on revealing 
    what's written inside individual files, not listing directory contents.
    
    Natural Language Patterns:
    - "What's written in this file?"
    - "Show me what this config contains"
    - "Check what settings are in here"
    - "What did I save in this file?"
    - "Read through this for me"
    - "What does this document say?"
    - "View the contents of this file"
    - "What information is stored here?"
    
    Key Action Words:
    - Read
    - View contents
    - Show text
    - Check information
    - See inside
    
    Context Clues:
    - Wanting to know what's saved/stored
    - Looking for specific information
    - Checking settings or details
    - Reading actual content
    
    Not For:
    - Listing directory contents
    - Showing file names
    - Creating or editing files
    - Searching across files
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
