from commands import get_command, pwd
from init.create_collections import initialize_commands, COMMANDS_COLLECTION
from pprint import pprint

from init.initialize_filesyste import initialize_filesystem
initialize_commands()
initialize_filesystem()
pwd_cmd = pwd()
pwd_cmd([])  # Sh

res = COMMANDS_COLLECTION.query(
    query_texts=["show all files in the current dir"],
    n_results=1,
)
pprint(res["documents"][0][0])

# pwd = get_command("pwd")

# pwd.execute({})
