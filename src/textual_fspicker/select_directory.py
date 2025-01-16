"""Provides a directory selection dialog."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import Button, Label

##############################################################################
# Local imports.
from .base_dialog import FileSystemPickerScreen
from .parts import DirectoryNavigation


##############################################################################
class CurrentDirectory(Label):
    """A widget to show the current directory."""

    DEFAULT_CSS = """
    CurrentDirectory {
        width: 1fr;
        height: 3;
        border: tall $background;
        padding-left: 1;
        padding-right: 1;
    }
    """

    current_directory: var[Path | None] = var(None, always_update=True)
    """The current directory."""

    def watch_current_directory(self) -> None:
        """Watch for the current directory being changed."""
        if (
            len(
                display := ""
                if self.current_directory is None
                else str(self.current_directory)[-self.size.width :]
            )
            >= self.size.width
        ):
            display = "…" + display[1:]
        self.update(display)

    def on_resize(self) -> None:
        self.current_directory = self.current_directory


##############################################################################
class SelectDirectory(FileSystemPickerScreen):
    """A directory selection dialog."""

    def __init__(
        self, location: str | Path = ".", title: str = "Select directory"
    ) -> None:
        """Initialise the dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
        """
        super().__init__(location, title)

    def on_mount(self) -> None:
        """Configure the dialog once the DOM is ready."""
        navigation = self.query_one(DirectoryNavigation)
        navigation.show_files = False
        self.query_one(CurrentDirectory).current_directory = navigation.location

    def _input_bar(self) -> ComposeResult:
        """Provide any widgets for the input before, before the buttons."""
        yield CurrentDirectory()

    @on(DirectoryNavigation.Changed)
    def _show_selected(self, event: DirectoryNavigation.Changed) -> None:
        """Update the display of the current location.

        Args:
            event: The event with the selection information in.
        """
        event.stop()
        self.query_one(CurrentDirectory).current_directory = event.control.location

    @on(Button.Pressed, "#select")
    def _select_directory(self, event: Button.Pressed) -> None:
        """React to the select button being pressed.

        Args:
            event: The button press event.
        """
        event.stop()
        self.dismiss(result=self.query_one(DirectoryNavigation).location)


### select_directory.py ends here
