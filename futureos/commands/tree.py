from pathlib import Path
from typing import Any
from futureos.commands.command import Command
from futureos.utils.path_utils import resolve_path


class tree(Command):
    """
    Command: Tree Viewer (tree)

    Displays a tree view of all files and directories in the specified directory.

    Natural Language Patterns:
    - "Show me the directory structure"
    - "Display a tree view of my files"
    - "What does my project structure look like?"

    Key Action Words:
    - Tree
    - Structure
    - Hierarchy
    - View

    Context Clues:
    - Asking about directory structure
    - Wanting to see a hierarchical view of files
    - References to project or directory layout

    Not For:
    - Listing files without structure
    - Reading file contents
    - Modifying files or directories
    """

    def _configure_parser(self) -> None:
        self.parser.add_argument(
            "directory", nargs="?", type=Path, help="Directory to display tree view"
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

        target_path = resolve_path(directory if directory else ".")
        if target_path.is_dir():
            self.tree_view(target_path)
        else:
            self.print(f"Error: {target_path} Not a directory", style="red")

    def tree_view(self, path: Path, prefix: str = "") -> None:
        """Recursively print the tree view of the directory."""
        self.print(f"{prefix}[path]{path.name}[/path]")
        prefix += "    "
        for child in path.iterdir():
            if child.is_dir():
                self.tree_view(child, prefix)
            else:
                self.print(f"{prefix}[gray]{child.name}[/gray]")
