from itertools import chain
from pathlib import Path
from constants import CURRENT_DIRECTORY, BASE_PATH


def resolve_directory(directory: Path) -> Path:
    """
    Resolve the directory path, ensuring it is within the base path.
    """
    directory_str = str(directory)
    if directory_str.startswith("\\") or directory_str.startswith("/"):
        directory_str = directory_str.lstrip("\\").lstrip("/")
    target_path = (CURRENT_DIRECTORY / directory_str).resolve()
    if not str(target_path).lower().startswith(str(BASE_PATH).lower()):
        raise Exception(
            f"Access denied: Cannot access outside of base path {BASE_PATH}"
        )
    return target_path


def get_all_directories() -> dict[str, list[str]]:
    """
    response format
    {
        "dir1": ["file1", "file2", "file3"],
        "dir1/subdir1": ["file1", "file2", "file3"]
    }
    """
    try:
        directories = {}
        for p in chain(
            [p for p in BASE_PATH.iterdir() if p.is_dir()], BASE_PATH.rglob("*/*")
        ):
            if p.is_dir():
                files = [f.name for f in p.iterdir() if f.is_file()]
                directories[str(p.relative_to(BASE_PATH)).replace("\\", "/")] = files
        return directories

    except Exception as e:
        print(f"Error reading directory structure: {e}")
        return {}
