import sys
import chromadb
from loguru import logger


import constants
from utils.path_utils import (
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


def initialize_commands(command_list):
    for name, command in command_list.items():
        logger.info(f"Indexing command: {name}")
        COMMANDS_COLLECTION.add(documents=[command.__doc__], ids=[name])


def initialize_files_collection():
    files = get_files_in_directory(constants.BASE_PATH)
    for file in files:
        path = resolve_path(file)
        with open(path, "r") as f:
            content = f.read()
        logger.info(f"Indexing file {file}")
        FILES_COLLECTION.add(
            documents=[f"FILE: {file}\n\nCONTENT:\n{content}"], ids=[file]
        )


def initialize_directories_collection():
    directories = get_all_directories()
    for dir_path, files in directories.items():
        dir_name = dir_path.split("/")[-1]
        subdirs = [
            str(get_relative_path(d)).split(dir_name)[-1]
            for d in directories.keys()
            if d.startswith(f"{dir_path}/")
        ]
        document = (
            f"DIRECTORY: {get_relative_path(dir_path)}\n"
            f"Directory name: {dir_name}\n"
            f"Is parent directory of: {subdirs}\n"
            f"Files: {files}"
        )
        logger.info(f"Indexing directory {dir_path}")
        DIRECTORIES_COLLECTION.add(documents=[document], ids=[dir_path])
