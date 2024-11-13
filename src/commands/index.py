from typing import Any
from commands.command import Command
from init.create_collections import initialize_directories_collection, initialize_files_collection


class index(Command):
    """
    NAME
        index - rebuild the file system search index

    DESCRIPTION
        Administrative command that rebuilds the internal search index
        for all files in the system. This is a maintenance operation
        that should only be run when:
        - New files have been added outside the shell
        - Search results seem incorrect or outdated
        - The index needs to be rebuilt from scratch

        This command does not search, list, or display files.
        Use 'ls' to list files or 'find' to search files.

    NATURAL LANGUAGE COMMANDS
        - Rebuild the search index
        - Reindex the file system
        - Update the file index
        - Regenerate the search index
        - Rebuild file system index

    EXAMPLES
        > index
        Reindexing all files...
        Reindexing completed.
    """

    def _configure_parser(self) -> None:
        pass

    def execute(self, *args: Any, **kwargs: Any) -> None:
        self.print("Reindexing all files...", style="yellow")
        initialize_files_collection()
        initialize_directories_collection()
        self.print("Reindexing completed.", style="green")
