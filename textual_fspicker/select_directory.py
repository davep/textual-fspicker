"""Provides a directory selection dialog."""

##############################################################################
# Python imports.
from __future__ import annotations
from pathlib import Path

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, Label

##############################################################################
# Local imports.
from .base_dialog import FileSystemPickerScreen
from .parts import DirectoryNavigation


##############################################################################
class SelectDirectory(FileSystemPickerScreen):
    """A directory selection dialog."""

    DEFAULT_CSS = """
    SelectDirectory > Dialog > InputBar > Label {
        width: 1fr;
        border: tall $background;
        padding-left: 1;
        padding-right: 1;
    }
    """

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
        self._set_current(navigation.location)

    def _input_bar(self) -> ComposeResult:
        """Provide any widgets for the input before, before the buttons."""
        yield Label()

    def _set_current(self, location: Path) -> None:
        """Set the current location.

        Args:
            location: The location to indicate.
        """
        current_selection = self.query_one("InputBar > Label", Label)
        # TODO: A nicer way of indicating we're looking at just the tail.
        current_selection.update(str(location)[-current_selection.size.width :])

    @on(DirectoryNavigation.Changed)
    def _show_selected(self, event: DirectoryNavigation.Changed) -> None:
        """Update the display of the current location.

        Args:
            event: The event with the selection information in.
        """
        event.stop()
        self._set_current(event.control.location)

    @on(Button.Pressed, "#select")
    def _select_directory(self, event: Button.Pressed) -> None:
        """React to the select button being pressed.

        Args:
            event: The button press event.
        """
        event.stop()
        self.dismiss(result=self.query_one(DirectoryNavigation).location)


### select_directory.py ends here
