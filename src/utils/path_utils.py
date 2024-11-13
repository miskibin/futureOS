from itertools import chain
from pathlib import Path
import constants


def get_relative_path(path: Path) -> str:
    return str(path).replace(str(constants.BASE_PATH), "").lstrip("/")


def resolve_path(path: Path) -> Path:
    path_str = str(path).replace("\\", "/").strip()
    if path_str.startswith("/"):
        path = path_str.lstrip("/")
        return (Path(constants.BASE_PATH) / Path(path)).resolve()
    if path_str.startswith("~"):
        path = path_str.lstrip("~")
        return (constants.BASE_PATH / "home" / path).resolve()
    return (constants.CURRENT_DIRECTORY / path).resolve()


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
        for p in constants.BASE_PATH.rglob("*"):
            if p.is_dir():
                files = [f.name for f in p.iterdir() if f.is_file()]
                directories[
                    str(p.relative_to(constants.BASE_PATH)).replace("\\", "/")
                ] = files
        return directories
    except Exception as e:
        print(f"Error reading directory structure: {e}")
        return {}


def get_files_in_directory(directory: Path) -> list[Path]:
    """
    Get all files in the specified directory and its subdirectories.
    """
    return [
        str(f).lower().replace(str(constants.BASE_PATH.resolve()).lower(), "")
        for f in directory.rglob("*")
        if f.is_file()
    ]
