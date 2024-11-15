from typing import Any
from pathlib import Path
import curses
from futureos.commands.command import Command
from futureos.utils.editor import TextEditor
from futureos.utils.path_utils import get_relative_path, resolve_path
from langchain_core.prompts import ChatPromptTemplate


class nano(Command):
    """
    Command: Text Editor (nano)

    Opens a simple text editor to modify configuration files, update documents, and
    revise existing content. Particularly useful for updating settings and making
    changes to text-based files.

    Natural Language Patterns:
    - "Let's work on document.md for a bit"
    - "Got to update config.yml"
    - "Time to update those database settings in the config"
    - "Got to update where I keep all those passwords"
    - "Should probably revise those project notes"

    Key Concepts:
    - Updating configuration files
    - Revising documents
    - Modifying settings
    - Working on specific files
    - Making changes to cls content

    Context Clues:
    - Mentions of specific file types (.yml, .md)
    - References to updating settings
    - Need to revise or modify content
    - Working with configuration files
    - Updating sensitive information

    Not Used For:
    - Just viewing file contents
    - Listing directory contents
    - Removing files
    - Showing current location
    - Reading without editing
    """

    use_code_editor = True

    def _configure_parser(self) -> None:
        self.parser.add_argument("file", nargs="?", type=str, help="File to edit")

    def generate_filename(self, content: str) -> str:
        """Generate filename using LLM based on content."""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Generate a short filename based on content. Use lowercase letters, numbers, underscores only. Just return filename with extension.",
                ),
                (
                    "user",
                    "Content:\n{content}\nGenerate filename.",
                ),
            ]
        )
        chain = prompt | self.model
        response = self.run_chain(chain, {"content": content[:500]})
        response = response.split(" ")[0].replace("\n", "")
        self.print(f"Generated filename: {response}")
        return response
    def edit_file(self, initial_file_path: Path) -> None:
        if self.use_code_editor:
            import subprocess

            process = subprocess.Popen(
                f"code --wait -n {str(resolve_path(initial_file_path).resolve())}",
                shell=True,
            )
            self.print("[system]Waiting for editor to close...[/system]")
            process.wait()
            regenerate = self.confirm_action(
                "Do you want me to regenerate filename based on content?"
            )
            if regenerate:
                with open(initial_file_path, "r") as f:
                    content = f.read()
                new_filename = self.generate_filename(content)
                new_path = initial_file_path.parent / new_filename
                initial_file_path.rename(new_path)
                initial_file_path = new_path
        else:
            editor = TextEditor(
                initial_file_path, self.generate_filename, self.update_indexes
            )
            editor.edit_file()

    def execute(self, args: Any) -> None:
        file_path = resolve_path(args.file or "untitled.txt")
        if args.query:
            filename = self.get_file(args.query, max_distance=1.6)
            if filename:
                file_path = resolve_path(filename)
            else:
                with open(file_path, "w") as f:
                    f.write("")

        self.edit_file(file_path)
        self.update_indexes("files", [str(get_relative_path(file_path))])
