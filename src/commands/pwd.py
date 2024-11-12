from pathlib import Path
from typing import Any
from commands.command import Command
import constants


class pwd(Command):
    """
    pwd: print working directory path

    PATH TERMS:
    pwd working-directory absolute-path filesystem-path directory-path path-only
    /home/user/directory /root/path /current/path print-working-directory pwd-command

    PATH QUESTIONS:
    where-am-i which-directory current-directory show-pwd print-pwd pwd-location

    RETURNS: filesystem path only
    NOT FOR: file contents, directory contents, file editing
    """

    def _configure_parser(self) -> None:
        pass

    def execute(self, args: Any) -> None:
        path = str(constants.CURRENT_DIRECTORY).replace(str(constants.BASE_PATH), "~")
        self.print(path, style="bold blue")
