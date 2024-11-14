from typing import Any
from futureos.commands.command import Command
from futureos.init.create_collections import initialize_directories_collection, initialize_files_collection


class index(Command):
    """
    Command: Rebuild Search Index (index)
    
    Updates the system's internal search database to include new files and reflect recent 
    changes. This command helps keep file searching fast and accurate.
    
    Natural Language Patterns:
    - "Search isn't working right"
    - "Update the search system"
    - "Refresh the file index"
    - "Fix the search feature"
    - "Make search work again"
    - "Rebuild the file database"
    - "Search needs updating"
    - "Refresh file searching"
    
    Key Concepts:
    - Updating search
    - Rebuilding index
    - Refreshing system
    - Fixing search
    - Maintaining database
    
    Not Used For:
    - Finding files
    - Listing contents
    - Reading files
    - File operations
    """

    def _configure_parser(self) -> None:
        pass

    def execute(self, *args: Any, **kwargs: Any) -> None:
        self.print("Reindexing all files...", style="yellow")
        initialize_files_collection()
        initialize_directories_collection()
        self.print("Reindexing completed.", style="green")
