import chromadb

from commands import COMMAND_LIST

chroma_client = chromadb.Client()
COMMANDS_COLLECTION = chroma_client.create_collection(name="commands")


def initialize_commands():
    for name, command in COMMAND_LIST.items():
        COMMANDS_COLLECTION.add(documents=[name], ids=[command.__doc__])

