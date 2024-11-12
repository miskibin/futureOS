from abc import ABC, abstractmethod
from typing import Optional, Any
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from commands.command import Command
import constants
from utils.path_utils import get_all_directories, resolve_path


class ls(Command):
    """
    ls: list directory contents

    DIRECTORY TERMS:
    list-files show-files directory-contents folder-contents list-directory
    file-list folder-list directory-items folder-items list-contents

    FILE LISTING PATTERNS:
    files-in-X contents-of-X items-in-X files-here list-everything
    show-files display-files what-files list-files show-contents

    RETURNS: list of files and folders only
    NOT FOR: file contents, file paths, file editing
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
            all_paths = get_all_directories()
            context = "\n".join(f"{d}: {', '.join(f)}" for d, f in all_paths.items())
            prompt = (
                "Given the directory list:\n{context}\n"
                "You can use . if you want to list the current directory\n"
                "Which directory is most relevant? Return only the path:\n{question}"
            )
            directory = self.run_nlp(context, args.query, prompt)
            # if directory is file go to ../
            # clean ooutput try to get first word that has `<name>` or '<name>'
            if directory.find("`") != -1:
                directory = directory.split("`")[1].split("`")[0]

            if directory in all_paths:
                directory = Path(directory)
            else:
                directory = Path(directory).parent
            self.print(f"Found directory: {directory}", style="green")

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
