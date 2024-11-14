import sys
import chromadb
import chromadb.server
from loguru import logger
from typing import Optional

from futureos import constants
from futureos.utils.path_utils import (
    get_all_directories,
    get_files_in_directory,
    get_relative_path,
    resolve_path,
)

# make logger messages more minimal
logger.remove()
logger.add(
    sys.stderr,
    format="{time:HH:mm:ss} - {level} - {message}",
    level="DEBUG",
    colorize=True,
)

# ollama_ef = embedding_functions.OllamaEmbeddingFunction(
#     url="http://localhost:11434/api/embeddings",
#     model_name="nomic-embed-text",
# )

chroma_client = chromadb.Client()
COMMANDS_COLLECTION = chroma_client.create_collection(name="commands")
FILES_COLLECTION = chroma_client.create_collection(name="files")
DIRECTORIES_COLLECTION = chroma_client.create_collection(name="directories")


def initialize_commands(command_list, commands_to_update: Optional[list[str]] = None):
    for name, command in command_list.items():
        if commands_to_update and name not in commands_to_update:
            continue
        logger.info(f"Indexing command: {name}")
        COMMANDS_COLLECTION.add(documents=[command.__doc__], ids=[name])


def initialize_files_collection(files_to_update: Optional[list[str]] = None):
    files = get_files_in_directory(constants.BASE_PATH)
    existing_ids = FILES_COLLECTION.get()["ids"]
    for file in files:
        if files_to_update and file not in files_to_update:
            continue
        path = resolve_path(file)
        with open(path, "r") as f:
            content = f.read()
        logger.info(f"Indexing file {file}")
        FILES_COLLECTION.add(
            documents=[f"FILE: {file}\n\nCONTENT:\n{content}"], ids=[file]
        )
    if files_to_update:
        ids_to_remove = [file for file in existing_ids if file not in files]
        logger.debug(f"Removing files from collection: {ids_to_remove}")
        if ids_to_remove:
            remove_from_collection(FILES_COLLECTION, ids_to_remove)


def initialize_directories_collection(
    directories_to_update: Optional[list[str]] = None,
):
    directories = get_all_directories()
    existing_ids = DIRECTORIES_COLLECTION.get()["ids"]
    for dir_path, files in directories.items():
        if directories_to_update and dir_path not in directories_to_update:
            continue
        dir_name = dir_path.split("/")[-1]
        subdirs = [
            str(get_relative_path(d)).split(dir_name)[-1]
            for d in directories.keys()
            if d.startswith(f"{dir_path}/")
        ]
        document = (
            f"DIRECTORY PATH: {get_relative_path(dir_path)}\n"
            f"Directory name: {dir_name}\n"
            f"Is parent directory of: {subdirs}\n"
        )
        logger.info(f"Indexing directory {dir_path}")
        DIRECTORIES_COLLECTION.add(documents=[document], ids=[f"/{dir_path}"])
    if directories_to_update:
        ids_to_remove = [
            dir_path for dir_path in existing_ids if dir_path not in directories
        ]
        if ids_to_remove:
            remove_from_collection(DIRECTORIES_COLLECTION, ids_to_remove)


def remove_from_collection(collection: chromadb.Collection, ids: list[str]):
    collection.delete(ids=ids)
