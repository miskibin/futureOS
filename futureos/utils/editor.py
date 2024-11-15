from typing import Any
from pathlib import Path
import curses
from futureos.commands.command import Command
from futureos.utils.path_utils import get_relative_path, resolve_path
from langchain_core.prompts import ChatPromptTemplate
from rich.status import Status
from rich.console import Console


class TextEditor:
    def __init__(self, initial_file_path: Path, generate_filename, update_indexes):
        self.file_path = initial_file_path
        self.generate_filename = generate_filename
        self.update_indexes = update_indexes
        self.generating_filename = False

    def init_curses(self) -> None:
        """Initialize curses settings."""
        # curses.start_color()
        # curses.use_default_colors()  # This allows for transparent background
        # curses.init_pair(1, curses.COLOR_WHITE, -1)  # Normal text
        # curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Status bar
        # curses.init_pair(3, curses.COLOR_BLUE, -1)  # Border

    def draw_border(self, stdscr, height: int, width: int) -> None:
        """Draw border around the editor."""
        try:
            stdscr.attron(curses.color_pair(3))
            stdscr.box()
            stdscr.attroff(curses.color_pair(3))
        except curses.error:
            pass

    def safe_addstr(self, stdscr, y: int, x: int, string: str, attr=0) -> None:
        """Safely add a string to the screen, truncating if necessary."""
        height, width = stdscr.getmaxyx()
        if y < 0 or y >= height:
            return

        # Truncate the string to fit the screen width
        if x < 0:
            string = string[-x:]
            x = 0
        if x + len(string) > width:
            string = string[: width - x]

        if string:  # Only try to add if there's something to add
            try:
                stdscr.addstr(y, x, string, attr)
            except curses.error:
                pass

    def draw_status_bar(
        self, stdscr, height: int, width: int, status: str, file_path: str
    ) -> None:
        """Draw status bar at the bottom of the screen."""
        status_bar = f" {status} | File: {file_path} "
        try:
            # Draw status line
            self.safe_addstr(
                stdscr, height - 2, 0, " " * (width - 1), curses.color_pair(2)
            )
            self.safe_addstr(
                stdscr, height - 2, 0, status_bar[: width - 1], curses.color_pair(2)
            )

            # Draw command help line
            help_text = "^X Exit | ^S Save | ^A AI filename"
            self.safe_addstr(
                stdscr, height - 1, 0, " " * (width - 1), curses.color_pair(2)
            )
            self.safe_addstr(stdscr, height - 1, 0, help_text, curses.color_pair(2))
        except curses.error:
            pass

    def edit_file(self) -> None:
        class EditorState:
            def __init__(self):
                self.file_path = self.file_path
                self.generating_filename = False

        editor_state = EditorState()

        def main(stdscr) -> None:
            self.init_curses()
            curses.curs_set(1)  # Show cursor
            stdscr.keypad(True)

            # Initialize content
            content = []
            if editor_state.file_path.exists():
                with open(editor_state.file_path, "r", encoding="utf-8") as f:
                    content = f.read().splitlines()
            if not content:
                content = [""]

            cursor_y = cursor_x = 0
            scroll_y = 0
            saved = True
            message = ""

            while True:
                try:
                    # Get terminal dimensions
                    height, width = stdscr.getmaxyx()
                    text_height = height - 3  # Reserve space for border and status bar

                    # Clear screen
                    stdscr.clear()

                    # Draw border
                    self.draw_border(stdscr, height, width)

                    # Draw content
                    for i in range(min(text_height, len(content) - scroll_y)):
                        line = content[scroll_y + i]
                        self.safe_addstr(
                            stdscr, i + 1, 1, line[: width - 2], curses.color_pair(1)
                        )

                    # Update status
                    status = f"{'[Modified]' if not saved else '[Saved]'} | Line {cursor_y + 1}"
                    if message:
                        status = message + " | " + status
                    if editor_state.generating_filename:
                        status = "Generating filename... | " + status
                    self.draw_status_bar(
                        stdscr, height, width, status, str(editor_state.file_path)
                    )

                    # Position cursor
                    try:
                        cursor_screen_y = cursor_y - scroll_y + 1
                        if 0 <= cursor_screen_y < height - 2:
                            cursor_screen_x = min(cursor_x + 1, width - 2)
                            stdscr.move(cursor_screen_y, cursor_screen_x)
                    except curses.error:
                        pass

                    # Handle input
                    ch = stdscr.getch()

                    if ch == 24:  # Ctrl+X
                        if not saved:
                            self.safe_addstr(
                                stdscr,
                                height - 2,
                                0,
                                "Save before exit? (Y/N) ".ljust(width - 1),
                                curses.color_pair(2),
                            )
                            stdscr.refresh()
                            if chr(stdscr.getch()).lower() == "y":
                                with open(
                                    editor_state.file_path, "w", encoding="utf-8"
                                ) as f:
                                    f.write("\n".join(content))
                        break

                    elif ch == 19:  # Ctrl+S
                        with open(editor_state.file_path, "w", encoding="utf-8") as f:
                            f.write("\n".join(content))
                        saved = True
                        message = "Saved"

                    elif ch == 1:  # Ctrl+A
                        editor_state.generating_filename = True
                        stdscr.refresh()
                        curses.endwin()  # Temporarily end curses mode
                        new_filename = self.generate_filename("\n".join(content))
                        new_file_path = resolve_path(new_filename.strip())
                        editor_state.file_path.rename(new_file_path)
                        self.update_indexes(
                            "files",
                            [
                                str(get_relative_path(editor_state.file_path)),
                                str(get_relative_path(new_file_path)),
                            ],
                        )
                        editor_state.file_path = new_file_path
                        message = f"New filename: {editor_state.file_path}"
                        editor_state.generating_filename = False
                        curses.initscr()  # Reinitialize curses
                        self.init_curses()  # Reinitialize colors

                    elif ch == curses.KEY_LEFT and cursor_x > 0:
                        cursor_x -= 1
                    elif ch == curses.KEY_RIGHT and cursor_x < len(content[cursor_y]):
                        cursor_x += 1
                    elif ch == curses.KEY_UP and cursor_y > 0:
                        cursor_y -= 1
                        if cursor_y < scroll_y:
                            scroll_y = cursor_y
                        cursor_x = min(cursor_x, len(content[cursor_y]))
                    elif ch == curses.KEY_DOWN and cursor_y < len(content) - 1:
                        cursor_y += 1
                        if cursor_y >= scroll_y + text_height:
                            scroll_y = cursor_y - text_height + 1
                        cursor_x = min(cursor_x, len(content[cursor_y]))

                    elif ch in (10, 13):  # Enter
                        line = content[cursor_y]
                        content[cursor_y] = line[:cursor_x]
                        content.insert(cursor_y + 1, line[cursor_x:])
                        cursor_y += 1
                        if cursor_y >= scroll_y + text_height:
                            scroll_y += 1
                        cursor_x = 0
                        saved = False

                    elif ch in (8, 127, curses.KEY_BACKSPACE):  # Backspace
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
                            if cursor_y < scroll_y:
                                scroll_y = cursor_y
                            saved = False

                    elif 32 <= ch <= 126:  # Printable characters
                        line = content[cursor_y]
                        content[cursor_y] = line[:cursor_x] + chr(ch) + line[cursor_x:]
                        cursor_x += 1
                        saved = False

                    message = ""

                except curses.error as e:
                    message = f"Error: {str(e)}"

                stdscr.refresh()

        curses.wrapper(main)
