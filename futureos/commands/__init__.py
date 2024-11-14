from .ls import ls
from .pwd import pwd
from .cd import cd
from .cat import cat
from .nano import nano
from .answer import answer
from .rm import rm
from .cls import cls

COMMAND_LIST = {
    "cd": cd,
    "ls": ls,
    "cat": cat,
    "nano": nano,
    "answer": answer,
    "rm": rm,
    "cls": cls,
    # "pwd": pwd,
}


def get_command(command_name: str):
    command = COMMAND_LIST.get(command_name)
    if command is None:
        return
    return command()
