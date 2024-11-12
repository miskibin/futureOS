import os
from pathlib import Path
from typing import Optional
from commands.command import Command

def initialize_filesystem(base_path: Optional[Path] = None) -> None:
    if base_path is None:
        base_path = Path.cwd() / "FileSystem"
    os.makedirs(base_path, exist_ok=True)
    root_path = base_path / "root"
    os.makedirs(root_path, exist_ok=True)
    
    Command.set_base_path(base_path)
    
    return base_path