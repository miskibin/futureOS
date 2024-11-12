from pathlib import Path
from typing import Any
from commands.command import Command
import constants


class pwd(Command):
    """
    NAME
        pwd - print working directory path

    DESCRIPTION
        Displays the absolute pathname of the current working directory.
        This command ONLY shows the current directory path and does not list contents
        or show file data. Use 'ls' to list directory contents or 'cat' to show file
        contents.

    NATURAL LANGUAGE COMMANDS
        - where am i? 
        - What is the full path to my current directory?
        - Show me the absolute path of where I am
        - What is my current directory path?
        - Print the path to my current location
        - Display my current directory path
    
    EXAMPLES
        > pwd
        ~/documents/projects
        
        The command always shows the path and nothing else.
    """

    def _configure_parser(self) -> None:
        pass

    def execute(self, args: Any) -> None:
        path = str(constants.CURRENT_DIRECTORY).replace(str(constants.BASE_PATH), "~")
        self.print(path, style="bold blue")
