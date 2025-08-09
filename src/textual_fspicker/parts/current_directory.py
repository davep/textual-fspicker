"""A widget for showing the current directory."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.reactive import var
from textual.widgets import Label


##############################################################################
class CurrentDirectory(Label):
    """A widget to show the current directory.

    This widget is used inside a
    [`SelectDirectory`][textual_fspicker.SelectDirectory] dialog to display
    the currently-selected directory.
    """

    DEFAULT_CSS = """
    CurrentDirectory {
        width: 1fr;
        padding-left: 1;
        padding-right: 1;
        border-bottom: $border;
    }
    """

    current_directory: var[Path | None] = var(None, always_update=True)
    """The current directory."""

    def _watch_current_directory(self) -> None:
        """Watch for the current directory being changed."""
        if (
            len(
                display := ""
                if self.current_directory is None
                else str(self.current_directory)[-self.size.width :]
            )
            >= self.size.width
        ):
            display = f"…{display[1:]}"
        self.update(display)

    def _on_resize(self) -> None:
        self.current_directory = self.current_directory


### current_directory.py ends here
