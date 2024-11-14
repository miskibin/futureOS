from abc import ABC, abstractmethod
from typing import Optional, Any
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from futureos.commands.command import Command
from futureos import constants
from futureos.utils.path_utils import get_all_directories, get_relative_path, resolve_path


class ls(Command):
    """
    Command: Directory Viewer (ls)
    
    Lists files and documents in the current working directory. Shows available
    files without displaying their contents, useful for finding documents to work on.
    
    Natural Language Patterns:
    - "Been working on some documents, can you list them for me?"
    - "What is in my code directory"
    - "what is inside this directory?"
    - "Show me what documents I have"
    - "List available files"
    - "Show me what's in this folder"
    - "What files do I have here"
    
    Key Action Words:
    - List
    - Show
    - Find
    - Display
    - What is in
    
    Context Clues:
    - Asking about multiple documents/files
    - Questions about directory contents
    - Wanting to see available options
    - References to folders or directories
    - General inquiries about what files exist
    
    Not For:
    - Reading file contents
    - Updating configurations
    - Working on specific documents
    - Removing files
    - Getting current directory path
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
