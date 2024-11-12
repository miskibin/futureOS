import chromadb
import chromadb.utils.embedding_functions as embedding_functions

from commands import COMMAND_LIST

# ollama_ef = embedding_functions.OllamaEmbeddingFunction(
#     url="http://localhost:11434/api/embeddings",
#     model_name="nomic-embed-text",
# )

chroma_client = chromadb.Client()
COMMANDS_COLLECTION = chroma_client.create_collection(name="commands")

def initialize_commands():
    for name, command in COMMAND_LIST.items():
        COMMANDS_COLLECTION.add(documents=[command.__doc__], ids=[name])
