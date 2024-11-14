from pathlib import Path
from typing import Any
from futureos.commands.command import Command
import futureos.constants


class pwd(Command):
    """
    Command: Print Working Directory (pwd)
    
    Tells you where you currently are in the file system by showing the complete path 
    to your current location. Helps you understand your position in the directory structure.
    
    Natural Language Patterns:
    - "Where am I right now?"
    - "Show me my current path"
    - "What folder am I working in?"
    - "Tell me where I'm located"
    - "Need to know my current directory"
    
    Key Concepts:
    - Working directory
    - System location
    - Current position
    
    Not Used For:
    - Showing directory contents
    - Changing directories
    - File operations
    - Finding files
    """


    def execute(self, args: Any) -> None:
        path = str(constants.CURRENT_DIRECTORY).replace(str(constants.BASE_PATH), "~")
        self.print(path, style="bold blue")
