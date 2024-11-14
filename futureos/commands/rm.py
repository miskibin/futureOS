
from typing import Any
from pathlib import Path
from commands.command import Command
from utils.path_utils import resolve_path

class rm(Command):
    """
    Command: Remove Files (rm)
    
    Permanently deletes files from the system. This command helps you remove unwanted 
    or unnecessary files to clean up your storage space.
    
    Natural Language Patterns:
    - "Delete this file"
    - "Remove [filename]"
    - "Get rid of this document"
    - "I need to delete [filename]"
    - "Take this file out"
    - "Clean up these files"
    - "Remove these old documents"
    - "Delete unwanted files"
    
    Key Concepts:
    - File deletion
    - Removing content
    - Cleaning up files
    - Getting rid of documents
    - Deleting data
    
    Not Used For:
    - Deleting directories
    - Moving files
    - Hiding files
    - Editing content
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
                if self.confirm_action(f"Are you sure you want to delete '{resolved_path.name}'?"):
                    try:
                        resolved_path.unlink()
                        self.print(f"Deleted {resolved_path}", style="green")
                    except Exception as e:
                        self.print(f"Error deleting {file_path}: {str(e)}", style="red")
                else:
                    self.print(f"Skipped deleting {resolved_path}", style="yellow")
            else:
                self.print(f"'{resolved_path}' is not a file", style="red")