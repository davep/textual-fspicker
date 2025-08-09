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
from textual.widgets import Button

##############################################################################
# Local imports.
from .base_dialog import ButtonLabel, FileSystemPickerScreen
from .parts import CurrentDirectory, DirectoryNavigation


##############################################################################
class SelectDirectory(FileSystemPickerScreen):
    """A directory selection dialog."""

    DEFAULT_CSS = """
    SelectDirectory CurrentDirectory {
        height: 3;
        border: tall $background;
    }
    """

    def __init__(
        self,
        location: str | Path = ".",
        title: str = "Select directory",
        *,
        select_button: ButtonLabel = "",
        cancel_button: ButtonLabel = "",
    ) -> None:
        """Initialise the dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            select_button: The label for the select button.
            cancel_button: The label for the cancel button.

        Notes:
            `select_button` and `cancel_button` can either be strings that
            set the button label, or they can be functions that take the
            default button label as a parameter and return the label to use.
        """
        super().__init__(
            location, title, select_button=select_button, cancel_button=cancel_button
        )

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
