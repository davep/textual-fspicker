"""Base file-oriented dialog."""

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
from textual.widgets import Button, Input, Select

##############################################################################
# Local imports.
from .base_dialog import ButtonLabel, FileSystemPickerScreen
from .parts import DirectoryNavigation, DriveNavigation
from .path_filters import Filters
from .path_maker import MakePath


##############################################################################
class FileFilter(Select[int]):
    """The file filter."""


##############################################################################
class BaseFileDialog(FileSystemPickerScreen):
    """The base dialog for file-oriented picking dialogs."""

    DEFAULT_CSS = """
    BaseFileDialog InputBar {
        Input {
            width: 2fr;
        }
        Select {
            width: 1fr;
        }
    }
    """

    ERROR_A_FILE_MUST_BE_CHOSEN = "A file must be chosen"
    """An error to show the user when a file should be chosen."""

    def __init__(
        self,
        location: str | Path = ".",
        title: str = "Open",
        select_button: ButtonLabel = "",
        cancel_button: ButtonLabel = "",
        *,
        filters: Filters | None = None,
        default_file: str | Path | None = None,
    ) -> None:
        """Initialise the base dialog dialog.

        Args:
            location: Optional starting location.
            title: Optional title.
            select_button: The label for the select button.
            cancel_button: The label for the cancel button.
            filters: Optional filters to show in the dialog.
            default_file: The default filename to place in the input.
        """
        super().__init__(
            location, title, select_button=select_button, cancel_button=cancel_button
        )
        self._filters = filters
        """The filters for the dialog."""
        self._default_file = default_file
        """The default filename to put in the input field."""

    def _input_bar(self) -> ComposeResult:
        """Provide any widgets for the input before, before the buttons."""
        yield Input(Path(self._default_file or "").name)
        if self._filters:
            yield FileFilter(
                self._filters.selections,
                prompt="File filter",
                value=0,
                allow_blank=False,
            )

    @on(Mount)
    def _initial_filter(self) -> None:
        """Set the initial filter once the DOM is ready."""
        if self._filters:
            self.query_one(DirectoryNavigation).file_filter = self._filters[0]

    @on(DirectoryNavigation.Selected)
    def _select_file(self, event: DirectoryNavigation.Selected) -> None:
        """Handle a file being selected in the picker.

        Args:
            event: The event to handle.
        """
        file_name = self.query_one(Input)
        file_name.value = str(event.path.name)
        file_name.focus()

    @on(Input.Changed)
    def _clear_error(self) -> None:
        """Clear any error that might be showing."""
        super()._clear_error()

    @on(Select.Changed)
    def _change_filter(self, event: Select.Changed) -> None:
        """Handle a change in the filter.

        Args:
            event: The event to handle.
        """
        if self._filters is not None and isinstance(event.value, int):
            self.query_one(DirectoryNavigation).file_filter = self._filters[event.value]
        else:
            self.query_one(DirectoryNavigation).file_filter = None
        self.query_one(DirectoryNavigation).focus()

    def _should_return(self, candidate: Path) -> bool:
        """Final check on a picked file before returning it to the caller.

        Args:
            candidate: The file to check.

        Returns:
            `True` if the file should be returned, `False` if not.

        Note:
            This method is designed to be called as a final check; this is a
            good place to set up the display of an error before returning
            `False`, for example.
        """
        del candidate
        return True

    @on(Input.Submitted)
    @on(Button.Pressed, "#select")
    def _confirm_file(self, event: Input.Submitted | Button.Pressed) -> None:
        """Confirm the selection of the file in the input box.

        Args:
            event: The event to handle.
        """
        event.stop()
        file_name = self.query_one(Input)

        # Only even try and process this if there's some input.
        if not file_name.value:
            self._set_error(self.ERROR_A_FILE_MUST_BE_CHOSEN)
            return

        # If it looks like the user is typing in some sort of home
        # directory path... (does pathlib let me test for this, or at
        # least ask what the home character is? Docs don't mention this;
        # so for now I'm going to hard-code this).
        if file_name.value.startswith("~"):
            # ...let's simply expand and go with that.
            try:
                chosen = MakePath.of(file_name.value).expanduser()
            except RuntimeError as error:
                self._set_error(str(error))
                return
        else:
            # It's not a home directory path, so let's combine with the
            # location of the directory navigator widget.
            chosen = (
                self.query_one(DirectoryNavigation).location / file_name.value
            ).resolve()

        # If it's a directory, approach it like it's the user simply
        # doing a "cd".
        try:
            if chosen.is_dir():
                if sys.platform == "win32":
                    if drive := MakePath.of(file_name.value).drive:
                        self.query_one(DriveNavigation).drive = drive
                self.query_one(DirectoryNavigation).location = chosen
                self.query_one(DirectoryNavigation).focus()
                self.query_one(Input).value = ""
                return
        except PermissionError:
            self._set_error(self.ERROR_PERMISSION_ERROR)
            return

        # If the chosen file passes the final tests...
        if self._should_return(chosen):
            # ...return it.
            self.dismiss(result=chosen)


### file_dialog.py ends here
