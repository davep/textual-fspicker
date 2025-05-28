"""The base dialog code for the other dialogs in the library."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
import sys
from pathlib import Path
from typing import Callable, TypeAlias

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label

##############################################################################
# Local imports.
from .parts import DirectoryNavigation, DriveNavigation


##############################################################################
class Dialog(Vertical):
    """Layout class for the main dialog area."""


##############################################################################
class InputBar(Horizontal):
    """The input bar area of the dialog."""


##############################################################################
ButtonLabel: TypeAlias = str | Callable[[str], str]
"""The type for a button label value."""


##############################################################################
class FileSystemPickerScreen(ModalScreen[Path | None]):
    """Base screen for the dialogs in this library."""

    DEFAULT_CSS = """
    FileSystemPickerScreen {
        align: center middle;

        Dialog {
            width: 80%;
            height: 80%;
            border: $border;
            background: $panel;
            border-title-color: $text;
            border-title-background: $panel;
            border-subtitle-color: $text;
            border-subtitle-background: $error;

            OptionList, OptionList:focus {
                background: $panel;
                background-tint: $panel;
            }
        }

        #current_path_display {
            width: 1fr;
            padding: 0 1;
            margin-bottom: 1; /* Optional: add some space below the path */
            overflow: hidden;
            text-overflow: ellipsis;
            color: $text-muted; /* Optional: make it less prominent */
        }

        DirectoryNavigation {
            height: 1fr;
        }

        InputBar {
            height: auto;
            align: right middle;
            padding-top: 1;
            padding-right: 1;
            padding-bottom: 1;
            Button {
                margin-left: 1;
            }
        }
    }
    """

    ERROR_PERMISSION_ERROR = "Permission error"
    """Error to tell there user there was a problem with permissions."""

    BINDINGS = [Binding("full_stop", "hidden"), Binding("escape", "dismiss(None)")]
    """The bindings for the dialog."""

    def __init__(
        self,
        location: str | Path = ".",
        title: str = "",
        select_button: ButtonLabel = "",
        cancel_button: ButtonLabel = "",
    ) -> None:
        """Initialise the dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            select_button: Label or format function for the select button.
            cancel_button: Label or format function for the cancel button.
        """
        super().__init__()
        self._location = location
        """The starting location."""
        self._title = title
        """The title for the dialog."""
        self._select_button = select_button
        """The text prompt for the select button, or a function to format it."""
        self._cancel_button = cancel_button
        """The text prompt for the cancel button, or a function to format it."""

    def _input_bar(self) -> ComposeResult:
        """Provide any widgets for the input bar, before the buttons."""
        yield from ()

    @staticmethod
    def _label(label: ButtonLabel, default: str) -> str:
        """Create a label for use with a button.

        Args:
            label: The label value for the button.
            default: The default label for the button.

        Returns:
            The formatted label.
        """
        # If the label is callable, then call it with the default as a
        # parameter; otherwise use it as-is as it'll be a string.
        return label(default) if callable(label) else label or default

    def compose(self) -> ComposeResult:
        """Compose the child widgets.

        Returns:
            The widgets to compose.
        """
        with Dialog() as dialog:
            dialog.border_title = self._title
            yield Label(id="current_path_display")
            with Horizontal():
                if sys.platform == "win32":
                    yield DriveNavigation(self._location)
                yield DirectoryNavigation(self._location)
            with InputBar():
                yield from self._input_bar()
                yield Button(self._label(self._select_button, "Select"), id="select")
                yield Button(self._label(self._cancel_button, "Cancel"), id="cancel")

    def on_mount(self) -> None:
        """Focus directory widget on mount and set initial path."""
        dir_nav = self.query_one(DirectoryNavigation)
        current_path_label = self.query_one("#current_path_display", Label)
        current_path_label.update(str(dir_nav.location))
        dir_nav.focus()

    def _set_error(self, message: str = "") -> None:
        """Set or clear the error message.

        Args:
            message: Optional message to show as an error.
        """
        self.query_one(Dialog).border_subtitle = message

    @on(DriveNavigation.DriveSelected)
    def _change_drive(self, event: DriveNavigation.DriveSelected) -> None:
        """Reload DirectoryNavigation in response to drive change."""
        """Reload DirectoryNavigation in response to drive change."""
        dir_nav = self.query_one(DirectoryNavigation)
        dir_nav.location = event.drive_root

    @on(DirectoryNavigation.Changed)
    def _on_directory_changed(self, event: DirectoryNavigation.Changed) -> None:
        """Clear any error and update the path display."""
        self._set_error()
        current_path_label = self.query_one("#current_path_display", Label)
        current_path_label.update(str(event.control.location))

    @on(DirectoryNavigation.Changed)
    def _clear_error(self) -> None:
        """Clear any error that might be showing."""
        self._set_error()

    @on(DirectoryNavigation.PermissionError)
    def _show_permission_error(self) -> None:
        """Show any permission error bubbled up from the directory navigator."""
        self._set_error(self.ERROR_PERMISSION_ERROR)

    @on(Button.Pressed, "#cancel")
    def _cancel(self, event: Button.Pressed) -> None:
        """Cancel the dialog.

        Args:
            event: The even to handle.
        """
        event.stop()
        self.dismiss(None)

    def _action_hidden(self) -> None:
        """Action for toggling the display of hidden entries."""
        self.query_one(DirectoryNavigation).toggle_hidden()


### base_dialog.py ends here
