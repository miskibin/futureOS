from .ls import ls
from .pwd import pwd
from .cd import cd
from .cat import cat

COMMAND_LIST = {
    "pwd": pwd,
    "cd": cd,
    "ls": ls,
    "cat": cat,
}


def get_command(command_name: str):
    command = COMMAND_LIST.get(command_name)
    if command is None:
        raise ValueError(f"Command '{command_name}' not found.")
    return command()
