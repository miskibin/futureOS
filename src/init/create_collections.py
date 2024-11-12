import sys
import chromadb
from loguru import logger


import constants
from utils.path_utils import get_files_in_directory, resolve_path

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
