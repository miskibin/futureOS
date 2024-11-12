from typing import Any
from pathlib import Path
import platform
import os
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from commands.command import Command
from utils.path_utils import resolve_path
from langchain_core.prompts import ChatPromptTemplate


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
            while True:
                if msvcrt.kbhit():
                    char = msvcrt.getch()
                    # Handle special keys
                    if char in (b'\x00', b'\xe0'):  # Arrow keys
                        char = msvcrt.getch()
                        return {
                            b'H': 'up',
                            b'P': 'down',
                            b'K': 'left',
                            b'M': 'right'
                        }.get(char, '')
                    # Handle control keys
                    try:
                        char = char.decode('utf-8')
                    except:
                        return ''
                    return char
        else:
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                char = sys.stdin.read(1)
                if char == '\x1b':
                    next_char = sys.stdin.read(1)
                    if next_char == '[':
                        code = sys.stdin.read(1)
                        return {
                            'A': 'up',
                            'B': 'down',
                            'C': 'right',
                            'D': 'left'
                        }.get(code, '')
                return char
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def generate_filename(self, content: str) -> str:
        """Generate filename using LLM based on content."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Generate a short filename with .txt extension based on content. Use lowercase letters, numbers, underscores only. Just return filename."),
            ("user", "Content:\n{content}\nGenerate filename:")
        ])
        chain = prompt | self.model
        return self.run_chain(chain, {"content": content[:500]})

    def edit_file(self, file_path: Path) -> None:
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

            display.append("\n^X Exit | ^S Save | ^A AI filename", style="black on white")
            return Panel(display, title=str(file_path), subtitle=status, border_style="blue")

        with Live(render(), refresh_per_second=10, screen=True) as live:
            while True:
                try:
                    char = self.get_key()

                    if char == '\x18':  # Ctrl+X
                        if not saved:
                            message = "Save? (Y/N)"
                            live.update(render())
                            if self.get_key().lower() == 'y':
                                with open(file_path, "w", encoding="utf-8") as f:
                                    f.write("\n".join(content))
                        break

                    elif char == '\x13':  # Ctrl+S
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write("\n".join(content))
                        saved = True
                        message = "Saved"

                    elif char == '\x01':  # Ctrl+A
                        new_filename = self.generate_filename("\n".join(content))
                        file_path = resolve_path(new_filename.strip())
                        message = f"New filename: {file_path}"

                    elif char in ('left', 'right', 'up', 'down'):
                        if char == 'left' and cursor_x > 0:
                            cursor_x -= 1
                        elif char == 'right' and cursor_x < len(content[cursor_y]):
                            cursor_x += 1
                        elif char == 'up' and cursor_y > 0:
                            cursor_y -= 1
                            cursor_x = min(cursor_x, len(content[cursor_y]))
                        elif char == 'down' and cursor_y < len(content) - 1:
                            cursor_y += 1
                            cursor_x = min(cursor_x, len(content[cursor_y]))

                    elif char in ('\r', '\n'):  # Enter
                        line = content[cursor_y]
                        content[cursor_y] = line[:cursor_x]
                        content.insert(cursor_y + 1, line[cursor_x:])
                        cursor_y += 1
                        cursor_x = 0
                        saved = False

                    elif char in ('\x7f', '\x08'):  # Backspace
                        if cursor_x > 0:
                            line = content[cursor_y]
                            content[cursor_y] = line[:cursor_x - 1] + line[cursor_x:]
                            cursor_x -= 1
                            saved = False
                        elif cursor_y > 0:
                            cursor_x = len(content[cursor_y - 1])
                            content[cursor_y - 1] += content[cursor_y]
                            content.pop(cursor_y)
                            cursor_y -= 1
                            saved = False

                    elif char and char.isprintable():
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
        file_path = resolve_path(args.file or "untitled.txt")
        if args.query:
            filename = self.get_file(args.query, max_distance=1.6)
            if filename:
                self.print(f"Opening: {filename}", style="green")
                file_path = resolve_path(filename)
        self.edit_file(file_path)