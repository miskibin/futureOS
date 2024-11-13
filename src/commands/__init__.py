from .ls import ls
from .pwd import pwd
from .cd import cd
from .cat import cat
from .nano import nano
from .index import index
from .answer import answer
from .rm import rm

COMMAND_LIST = {
    "cd": cd,
    "ls": ls,
    "cat": cat,
    "nano": nano,
    "index": index,
    "answer": answer,
    "rm": rm,
    # "pwd": pwd,
}


def get_command(command_name: str):
    command = COMMAND_LIST.get(command_name)
    if command is None:
        return
    return command()
