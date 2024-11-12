from .ls import ls
from .pwd import pwd
from .cd import cd
from .cat import cat
from .nano import nano
from .index import index
from .answer import answer
COMMAND_LIST = {
    "pwd": pwd,
    "cd": cd,
    "ls": ls,
    "cat": cat,
    "nano": nano,
    "index": index,
    "answer": answer,
}


def get_command(command_name: str):
    command = COMMAND_LIST.get(command_name)
    if command is None:
        return
    return command()
