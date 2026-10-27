"""Provides a directory selection dialog."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
import sys
from pathlib import Path

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.events import Mount
from textual.widgets import Button, Input

##############################################################################
# Local imports.
from .base_dialog import ButtonLabel, FileSystemPickerScreen
from .parts import CurrentDirectory, DirectoryNavigation, DriveNavigation
from .path_maker import MakePath
from .suggest_path import SuggestPath


##############################################################################
class SelectDirectory(FileSystemPickerScreen):
    """A directory selection dialog."""

    DEFAULT_CSS = """
    SelectDirectory InputBar {
        Input {
            width: 2fr;
        }
        Select {
            width: 1fr;
        }
    }
    """

    ERROR_A_DIRECTORY_MUST_EXIST = "The directory must exist"
    """An error to show the user when a typed directory doesn't exist."""

    def __init__(
        self,
        location: str | Path = ".",
        title: str = "Select directory",
        *,
        select_button: ButtonLabel = "",
        cancel_button: ButtonLabel = "",
        double_click_directories: bool = True,
        suggest_completions: bool = True,
    ) -> None:
        """Initialise the dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            select_button: The label for the select button.
            cancel_button: The label for the cancel button.
            double_click_directories: Double click to open directories.
            suggest_completions: Should the `Input` suggest completions?

        Notes:
            `select_button` and `cancel_button` can either be strings that
            set the button label, or they can be functions that take the
            default button label as a parameter and return the label to use.
        """
        super().__init__(
            location,
            title,
            select_button=select_button,
            cancel_button=cancel_button,
            double_click_directories=double_click_directories,
        )
        self._suggest_path = (
            SuggestPath(directories_only=True) if suggest_completions else None
        )
        """The object that suggests paths in the input field."""

    def on_mount(self) -> None:
        """Configure the dialog once the DOM is ready."""
        navigation = self.query_one(DirectoryNavigation)
        navigation.show_files = False

    def _header_area(self) -> ComposeResult:
        """Populate the header area with the current directory path."""
        yield CurrentDirectory()

    def _input_bar(self) -> ComposeResult:
        """Provide any widgets for the input before, before the buttons."""
        yield Input(suggester=self._suggest_path)

    @on(DirectoryNavigation.Changed)
    @on(Mount)
    def _update_current_directory(self) -> None:
        """Update the current directory display."""
        self.query_one(CurrentDirectory).current_directory = (
            location := self.query_one(DirectoryNavigation).location
        )
        if self._suggest_path is not None:
            self._suggest_path.root = location

    @on(Input.Changed)
    def _clear_input_error(self) -> None:
        """Clear any error that might be showing."""
        self._set_error()

    @on(Input.Submitted)
    def _go_to_directory(self, event: Input.Submitted) -> None:
        """Navigate to the directory typed into the input.

        Args:
            event: The event with the typed directory in.
        """
        event.stop()

        # Only even try and process this if there's some input.
        if not event.value:
            return

        # Combine what was typed with the location of the directory
        # navigator. Note that if what was typed is an absolute path, that
        # is what will win out here; and if it's a home directory path it
        # will be expanded.
        navigation = self.query_one(DirectoryNavigation)
        try:
            typed = MakePath.of(event.value).expanduser()
            chosen = (navigation.location / typed).resolve()
        except RuntimeError as error:
            self._set_error(str(error))
            return

        # Approach it like the user is simply doing a "cd".
        try:
            if chosen.is_dir():
                if sys.platform == "win32":
                    if drive := MakePath.of(event.value).drive:
                        self.query_one(DriveNavigation).drive = drive
                navigation.location = chosen
                navigation.focus()
                event.input.value = ""
            else:
                self._set_error(self.ERROR_A_DIRECTORY_MUST_EXIST)
        except PermissionError:
            self._set_error(self.ERROR_PERMISSION_ERROR)

    @on(Button.Pressed, "#select")
    def _select_directory(self, event: Button.Pressed) -> None:
        """React to the select button being pressed.

        Args:
            event: The button press event.
        """
        event.stop()
        self.dismiss(result=self.query_one(DirectoryNavigation).location)


### select_directory.py ends here
