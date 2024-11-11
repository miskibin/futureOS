from pathlib import Path
from constants import BASE_PATH
from itertools import chain

def get_all_paths() -> list[str]:
    try:
        paths = ['/']
        paths.extend(
            '/' + str(p.relative_to(BASE_PATH)).replace('\\', '/')
            for p in chain([p for p in BASE_PATH.iterdir()], BASE_PATH.rglob("*/*"))
        )
        
        return sorted(paths)
        
    except Exception as e:
        print(f"Error reading directory structure: {e}")
        return []