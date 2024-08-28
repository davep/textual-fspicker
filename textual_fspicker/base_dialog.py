"""The base dialog code for the other dialogs in the library."""

##############################################################################
# Python imports.
from __future__ import annotations
from pathlib import Path
from typing import Optional
import os

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Select

##############################################################################
# Local imports.
from .parts import DirectoryNavigation
from .path_maker import MakePath


##############################################################################
class Dialog(Vertical):
    """Layout class for the main dialog area."""


##############################################################################
class InputBar(Horizontal):
    """The input bar area of the dialog."""


##############################################################################
class FileSystemPickerScreen(ModalScreen[Optional[Path]]):
    """Base screen for the dialogs in this library."""

    DEFAULT_CSS = """
    FileSystemPickerScreen {
        align: center middle;
    }

    FileSystemPickerScreen Dialog {
        width: 80%;
        height: 80%;
        border: panel $panel-lighten-2;
        background: $panel-lighten-1;
        border-title-color: $text;
        border-title-background: $panel-lighten-2;
        border-subtitle-color: $text;
        border-subtitle-background: $error;
    }

    FileSystemPickerScreen DirectoryNavigation {
        height: 1fr;
    }

    FileSystemPickerScreen InputBar {
        height: auto;
        align: right middle;
        padding-top: 1;
        padding-right: 1;
        padding-bottom: 1;
    }

    FileSystemPickerScreen InputBar Button {
        margin-left: 1;
    }
    """

    BINDINGS = [Binding("full_stop", "hidden"), Binding("escape", "dismiss(None)")]
    """The bindings for the dialog."""

    select_Changed = False

    def __init__(
        self, location: str | Path = ".", title: str = "", select_button: str = "", drives: list[str] = []
    ) -> None:
        """Initialise the dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            select_button: Label for the select button.
        """
        super().__init__()

        if os.name == 'nt':
            import win32api
            drivesStr = win32api.GetLogicalDriveStrings()
            self.drives = drivesStr.split('\x00')[:-1]
        else:
            self.drives = "/"
        
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
            currentDrive = str(os.path.splitdrive(MakePath.of(self._location).expanduser().absolute())[0]+'\\').upper()
            yield Select.from_values(self.drives, value=currentDrive)
            yield DirectoryNavigation(self._location)
            with InputBar():
                yield from self._input_bar()
                yield Button("Cancel", id="cancel", variant="error")
                yield Button(self._select_button, id="select", variant="primary")
                

    def _set_error(self, message: str = "") -> None:
        """Set or clear the error message.

        Args:
            message: Optional message to show as an error.
        """
        self.query_one(Dialog).border_subtitle = message

    @on(Select.Changed)
    def _select(self, event: Select.Changed) -> None:
        """Handle the select button being pressed.
        change the directory disk

        Args:
            event: The event to handle.
        """

        if not self.select_Changed:
            self.select_Changed = True
            return

        self._location = event.value
        self.query_one(DirectoryNavigation).location = self._location
        self.query_one(DirectoryNavigation).refresh()

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
