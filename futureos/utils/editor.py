import curses
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class EditorState:
    """Class to maintain editor state."""

    file_path: Path
    content: List[str]
    cursor_x: int = 0
    cursor_y: int = 0
    scroll_y: int = 0
    saved: bool = True
    message: str = ""

    @classmethod
    def from_file(cls, file_path: Path) -> "EditorState":
        """Create EditorState from a file."""
        content = []
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().splitlines()
        if not content:
            content = [""]

        return cls(file_path=file_path, content=content)

    def save(self) -> None:
        """Save content to file."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.content))
        self.saved = True
        self.message = "Saved"

    def update_cursor(self, new_x: int, new_y: int, text_height: int) -> None:
        """Update cursor position with bounds checking."""
        # Update Y position
        if 0 <= new_y < len(self.content):
            self.cursor_y = new_y
            # Update scroll if necessary
            if self.cursor_y < self.scroll_y:
                self.scroll_y = self.cursor_y
            elif self.cursor_y >= self.scroll_y + text_height:
                self.scroll_y = self.cursor_y - text_height + 1

        # Update X position
        max_x = len(self.content[self.cursor_y])
        self.cursor_x = max(0, min(new_x, max_x))


class KeyBindings:
    CTRL_X = 24  # Exit
    CTRL_S = 19  # Save
    CTRL_A = 1  # AI filename
    ENTER = (10, 13)
    BACKSPACE = (8, 127, curses.KEY_BACKSPACE)
    ARROW_KEYS = {
        curses.KEY_UP: "up",
        curses.KEY_DOWN: "down",
        curses.KEY_LEFT: "left",
        curses.KEY_RIGHT: "right",
    }

