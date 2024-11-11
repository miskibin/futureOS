from abc import ABC, abstractmethod
from typing import Optional, Any
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from commands.command import Command
import constants
from utils.path_utils import resolve_directory, get_all_directories


class ls(Command):
    """
     NAME
        ls - list directory contents

    SYNOPSIS
        ls [directory]
        --graph (-g) Display all files in the file system
        --query (-q) Natural language query

    DESCRIPTION
        List information about the files in the current directory.
        If a directory is specified, list contents of that directory.
        Use --graph to show a visual representation of the file system.

    NATURAL LANGUAGE COMMANDS
        - Show files in directory X
        - List contents of folder X
        - List all files in directory X
        - What is in directory X
        - Display files in directory X
        - Show what's in folder X
    """

    def _configure_parser(self) -> None:
        self.parser.add_argument(
            "directory", nargs="?", type=Path, help="Directory to list"
        )
        self.parser.add_argument(
            "--graph", "-g", action="store_true", help="Display file system graph"
        )

    def execute(self, args: Any) -> None:
        self.print(args, constants.CURRENT_DIRECTORY)
        directory = args.directory
        if args.query:
            all_paths = get_all_directories()
            context = "\n".join(
                f"{d}: {', '.join(f)}" for d, f in all_paths.items()
            )
            prompt = (
                "Given the directory list:\n{context}\n"
                "Which directory is most relevant? Return only the path:\n{question}"
            )
            directory = self.run_nlp(context, args.query, prompt)
            # if directory is file go to ../
            if directory in all_paths:
                directory = Path(directory)
            else:
                directory = Path(directory).parent
            self.print(f"Found: directory: {directory}", style="green")

        if args.graph:
            for dir_path, files in get_all_directories().items():
                self.print(
                    f"[blue]{dir_path}[/blue]: [green]{', '.join(files)}[/green]"
                )
            return
        target_path = resolve_directory(
            directory if directory else constants.CURRENT_DIRECTORY
        )

        if target_path.is_dir():
            self.print("\n".join(f.name for f in target_path.iterdir()))
        else:
            self.print(f"Error: Not a directory", style="red")