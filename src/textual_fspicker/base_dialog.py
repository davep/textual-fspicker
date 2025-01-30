"""The base dialog code for the other dialogs in the library."""

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
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button

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

    BINDINGS = [Binding("full_stop", "hidden"), Binding("escape", "dismiss(None)")]
    """The bindings for the dialog."""

    def __init__(
        self, location: str | Path = ".", title: str = "", select_button: str = ""
    ) -> None:
        """Initialise the dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            select_button: Label for the select button.
        """
        super().__init__()
        self._location = location
        """The starting location."""
        self._title = title
        """The title for the dialog."""
        self._select_button = select_button or "Select"
        """The text prompt for the select button."""

    def _input_bar(self) -> ComposeResult:
        """Provide any widgets for the input bar, before the buttons."""
        yield from ()

    def compose(self) -> ComposeResult:
        """Compose the child widgets.

        Returns:
            The widgets to compose.
        """
        with Dialog() as dialog:
            dialog.border_title = self._title
            with Horizontal():
                if sys.platform == "win32":
                    yield DriveNavigation(self._location)
                yield DirectoryNavigation(self._location)
            with InputBar():
                yield from self._input_bar()
                yield Button(self._select_button, id="select")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        """Focus directory widget on mount."""
        self.query_one(DirectoryNavigation).focus()

    def _set_error(self, message: str = "") -> None:
        """Set or clear the error message.

        Args:
            message: Optional message to show as an error.
        """
        self.query_one(Dialog).border_subtitle = message

    @on(DriveNavigation.DriveSelected)
    def _change_drive(self, event: DriveNavigation.DriveSelected) -> None:
        """Reload DirectoryNavigation in response to drive change."""
        self.query_one(DirectoryNavigation).location = event.drive_root

    @on(DirectoryNavigation.Changed)
    def _clear_error(self) -> None:
        """Clear any error that might be showing."""
        self._set_error()

    @on(DirectoryNavigation.PermissionError)
    def _show_permission_error(self) -> None:
        """Show any permission error bubbled up from the directory navigator."""
        self._set_error("Permission error")

    @on(Button.Pressed, "#cancel")
    def _cancel(self, event: Button.Pressed) -> None:
        """Cancel the dialog.

        Args:
            event: The even to handle.
        """
        event.stop()
        self.dismiss(None)

    def action_hidden(self) -> None:
        """Action for toggling the display of hidden entries."""
        self.query_one(DirectoryNavigation).toggle_hidden()


### base_dialog.py ends here
