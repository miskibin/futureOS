from typing import Any
from pathlib import Path
import platform
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from commands.command import Command
from utils.path_utils import resolve_path, get_files_in_directory
import constants


class nano(Command):
    """
    NAME
        nano - simple text editor

    SYNOPSIS
        nano [file]

    DESCRIPTION
        A simple text editor for creating and modifying text files.
        Use Ctrl+S to save, Ctrl+X to exit.

    NATURAL LANGUAGE COMMANDS
        - Edit file X
        - Open file X in editor
        - Create new file X
        - Modify file X
    """

    def _configure_parser(self) -> None:
        self.parser.add_argument("file", nargs="?", type=str, help="File to edit")

    def get_key(self) -> str:
        """Get a single keypress."""
        if platform.system() == "Windows":
            import msvcrt

            char = msvcrt.getch()
            try:
                return char.decode("utf-8")
            except UnicodeDecodeError:
                if char == b"\xe0":  # Arrow keys
                    char = msvcrt.getch()
                    return {b"H": "up", b"P": "down", b"K": "left", b"M": "right"}.get(
                        char, ""
                    )
                return ""
        else:
            import sys, tty, termios

            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                char = sys.stdin.read(1)
                if char == "\x1b":
                    char = sys.stdin.read(2)
                    return {"[A": "up", "[B": "down", "[C": "right", "[D": "left"}.get(
                        char, ""
                    )
                return char
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def edit_file(self, file_path: Path) -> None:
        # Load file content
        content = []
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().splitlines()
        if not content:
            content = [""]

        cursor_y = cursor_x = 0
        saved = True
        message = ""

        def render() -> Panel:
            display = Text()
            # Show content and cursor
            for i, line in enumerate(content):
                if i == cursor_y:
                    display.append(line[:cursor_x], style="white")
                    display.append("█", style="white on white")
                    display.append(line[cursor_x:], style="white")
                else:
                    display.append(line, style="white")
                display.append("\n")

            status = f"{'[Modified]' if not saved else '[Saved]'} | Line {cursor_y + 1}"
            if message:
                status = message + " | " + status

            display.append("\n^X Exit | ^S Save", style="black on white")
            return Panel(
                display, title=str(file_path), subtitle=status, border_style="blue"
            )

        with Live(render(), refresh_per_second=10, screen=True) as live:
            while True:
                try:
                    char = self.get_key()

                    # Handle cursor movement
                    if char == "left" and cursor_x > 0:
                        cursor_x -= 1
                    elif char == "right" and cursor_x < len(content[cursor_y]):
                        cursor_x += 1
                    elif char == "up" and cursor_y > 0:
                        cursor_y -= 1
                        cursor_x = min(cursor_x, len(content[cursor_y]))
                    elif char == "down" and cursor_y < len(content) - 1:
                        cursor_y += 1
                        cursor_x = min(cursor_x, len(content[cursor_y]))

                    # Handle control keys
                    elif char in ("\x18", "\x03"):  # Ctrl+X or Ctrl+C
                        if not saved:
                            message = "Save? (Y/N)"
                            live.update(render())
                            if self.get_key().lower() == "y":
                                with open(file_path, "w", encoding="utf-8") as f:
                                    f.write("\n".join(content))
                        break

                    elif char == "\x13":  # Ctrl+S
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write("\n".join(content))
                        saved = True
                        message = "Saved"

                    # Handle text editing
                    elif char in ("\r", "\n"):  # Enter
                        line = content[cursor_y]
                        content[cursor_y] = line[:cursor_x]
                        content.insert(cursor_y + 1, line[cursor_x:])
                        cursor_y += 1
                        cursor_x = 0
                        saved = False

                    elif char in ("\x7f", "\x08"):  # Backspace
                        if cursor_x > 0:
                            line = content[cursor_y]
                            content[cursor_y] = line[: cursor_x - 1] + line[cursor_x:]
                            cursor_x -= 1
                            saved = False
                        elif cursor_y > 0:
                            cursor_x = len(content[cursor_y - 1])
                            content[cursor_y - 1] += content[cursor_y]
                            content.pop(cursor_y)
                            cursor_y -= 1
                            saved = False

                    elif char and char.isprintable():  # Regular characters
                        line = content[cursor_y]
                        content[cursor_y] = line[:cursor_x] + char + line[cursor_x:]
                        cursor_x += 1
                        saved = False

                    message = ""
                    live.update(render())

                except Exception as e:
                    message = f"Error: {str(e)}"
                    live.update(render())

    def execute(self, args: Any) -> None:
        if args.query:
            files = get_files_in_directory(constants.CURRENT_DIRECTORY)
            context = "\n".join(f"- {f}" for f in files)
            prompt = (
                "Given these files:\n"
                "{context}\n\n"
                "Find file for: {question}\n"
                "RESPOND WITH ONLY THE FULL PATH. NO EXPLANATIONS OR QUOTES:"
            )
            result = self.run_nlp(context, args.query, prompt).strip()
            filename = result.split("\n")[0].replace("`", "").strip("'\" ").split()[0]

            if filename in files:
                self.print(f"Opening: {filename}", style="green")
            else:
                self.print(f"Creating: {filename}", style="yellow")
            file_path = resolve_path(filename)
        else:
            file_path = resolve_path(args.file or "untitled.txt")

        self.edit_file(file_path)
